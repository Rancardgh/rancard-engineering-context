# Implementation recipes

Contents:
1. [New outbox event, end to end](#1-new-outbox-event-end-to-end)
2. [Idempotency guards for task bodies](#2-idempotency-guards-for-task-bodies)
3. [Inbox ledger for inbound callbacks](#3-inbox-ledger-for-inbound-callbacks)
4. [DLQ wiring](#4-dlq-wiring)
5. [Tests](#5-tests)
6. [Review-finding template](#6-review-finding-template)

---

## 1. New outbox event, end to end

Five edits. Work through them in order — the registry raises `KeyError` (and the relay dead-letters the event) if you emit an event type with no handler, so never land the emit without the handler.

### 1.1 Event type

`backend/src/apps/core/models/outbox.py` — add to `OutboxEvent.EventType`. Values are dotted and namespaced by destination, which is what makes the queue classification in step 4 readable:

```python
BUSINESS_ACCESS_GRANTED = (
    "notification.business_access_granted",
    "Business Access Granted",
)
```

Then `makemigrations core` — `EventType` is a `choices` list on a `CharField`, so Django generates an `AlterField`. It is not a schema change, but the migration must exist or CI's missing-migration check fails.

### 1.2 Emit inside the domain transaction

`emit()` raises `TransactionManagementError` unless a transaction is already open, on purpose: it will not let you write durable intent that isn't atomic with the state change that justified it. So the call goes *inside* the same `transaction.atomic()` block as the model writes.

```python
from src.apps.core.models.outbox import OutboxEvent
from src.apps.core.outbox.emitter import emit

with transaction.atomic():
    grant = BusinessAccessGrant.objects.create(...)
    emit(
        event_type=OutboxEvent.EventType.BUSINESS_ACCESS_GRANTED,
        idempotency_key=f"business_access_granted:{grant.pk}",
        payload={"grant_id": grant.pk, "to_email": grant.contact_email},
    )
```

**idempotency_key** is `UNIQUE`. Derive it from the domain fact that must happen at most once — a token, a PK, a provider reference (`user_invitation:{inv.token}`, `investigation_report:{report.pk}`). Never `uuid4()` or a timestamp: that defeats the constraint, which is the thing making a retried caller safe. If the caller legitimately re-emits (invitation token refresh), key it on the *new* token so the new send is a distinct fact.

A duplicate key raises `IntegrityError` out of `emit`'s savepoint with the outer transaction still usable — catch it and return the "already exists" outcome, as `user_invitation_service.py:99` does.

**payload** must be JSON-serializable and self-sufficient: the handler runs later, in another process, possibly after a deploy. Pass IDs plus whatever the handler cannot re-derive. Don't pass model instances, `Decimal`, `datetime` (use `.isoformat()`), or `UUID` (use `str()`). Keep secrets and raw PII out — the row is readable in Django admin and lands in `FailedTask` on dead-lettering.

**From async code** (`adrf` views, async services): wrap the whole write-plus-emit in a sync function and `await sync_to_async(...)()` it — `admin_investigations_view.py:368` and `user_invitation_service.py:68` both do this. Never `sync_to_async(emit)` on its own; that opens a *different* transaction from the domain write and the atomicity you were buying is gone.

### 1.3 Handler

`backend/src/apps/core/outbox/handlers/<event_name>.py`, exporting `handle(payload: dict) -> None`. Handlers are thin: translate payload → the real dispatch. Keep heavy work in the downstream task so relay retries stay cheap.

```python
from src.shared.celery.backpressure import BackpressureRejected, guarded_apply_async
from src.shared.celery.queues import QueueClass
from src.shared.utils.logger import get_logger

logger = get_logger(name=__name__)


def handle(payload: dict) -> None:
    from src.apps.core.tasks.notification_delivery_tasks import deliver_email

    try:
        guarded_apply_async(
            deliver_email,
            queue_class=QueueClass.CRITICAL,
            critical=True,
            source="outbox.business_access_granted",
            args=(email_kwargs,),
        )
    except BackpressureRejected:
        logger.info(
            "Business access notification enqueue rejected by broker pressure",
            caller="business_access_granted.handle",
            source="outbox.business_access_granted",
        )
        raise
```

Two rules that are easy to get backwards:

- **Import the downstream task inside `handle`.** The registry imports every handler module at startup; module-level task imports create cycles.
- **Re-raise `BackpressureRejected` (and any other transient failure).** Raising is what tells the relay to retry with backoff and eventually dead-letter; swallowing it marks the event delivered when nothing was delivered. Compare `user_invitation.py` (critical, re-raises) with a fire-and-forget handler that logs and returns.

Register in `backend/src/apps/core/outbox/registry.py` — add the module to the import list and the entry to `HANDLER_REGISTRY`.

### 1.4 Queue classification

`backend/src/apps/core/tasks/outbox_tasks.py` holds two sets that decide queue and backpressure treatment:

- `_CRITICAL_OUTBOX_TYPES` → `QueueClass.CRITICAL`, `critical=True` (bypasses backpressure shedding). User-facing must-arrive messages: password reset, invitation, registration confirmation.
- `_EXTERNAL_OUTBOX_TYPES` → `QueueClass.EXTERNAL`, isolating third-party latency from internal work. Telco/provider calls.
- Neither → `QueueClass.DEFAULT`.

Add the new type to the right set. Skipping this is silent — it just lands on the default queue.

### 1.5 Verify the loop closes

`sweep_pending_outbox_events` (beat, `src/celery.py`) re-enqueues PENDING events and resets `PROCESSING` locks older than 10 minutes. This is the recovery path when the `on_commit` publish fails or a worker dies mid-handler — it is why the pattern survives broker outages, and why an event stuck in PENDING is a handler bug, not a lost message.

---

## 2. Idempotency guards for task bodies

`task_acks_late=True` is global, so the broker redelivers the *original* message with the *same task ID* when a worker dies after executing and before acking. `self.retry()` allocates a new task ID — which is what makes a `request.id`-keyed guard distinguish a replay from a genuine retry.

**Transient external send** (SMS, email, push) — Redis `SET NX`, mirroring `send_sms_task`:

```python
idempotency_key = f"sms:sent:{self.request.id}"
redis = get_redis_client()
if not redis.set(idempotency_key, 1, ex=_SMS_IDEMPOTENCY_TTL, nx=True):
    logger.info("Skipping duplicate SMS task", caller="send_sms_task", task_id=self.request.id)
    return True
```

TTL comfortably longer than the effect's window (SMS uses 1 hour, "well beyond OTP lifetime").

**DB state transition** — status-gate under a row lock, mirroring `process_outbox_event`:

```python
with transaction.atomic():
    obj = Model.objects.select_for_update(skip_locked=True).get(pk=pk)
    if obj.status in TERMINAL_STATUSES:
        logger.info("Already processed; skipping", pk=pk, status=obj.status)
        return
    obj.status = Model.Status.PROCESSING
    obj.save(update_fields=["status", "updated_at"])
```

`skip_locked=True` means a concurrent worker returns instead of blocking. The read, the check, and the claiming write must be in one transaction — split them and two workers both pass the check.

**Row creation** — unique constraint on the natural key plus `get_or_create`, or catch `IntegrityError`. Prefer letting the database arbitrate over an existence check in Python.

**External API call with a provider-side effect** — send a client-supplied idempotency key or correlation ID if the provider supports one; otherwise gate on local state before calling and record the result immediately after.

---

## 3. Inbox ledger for inbound callbacks

External senders (telcos, partners, identity providers) retry on their own schedule and will replay a callback after a timeout even when you processed it. Dedupe on *their* identifier, in the same transaction as the effect, with a unique constraint — the constraint is the guard; a `.exists()` check alone races.

```python
with transaction.atomic():
    try:
        ProviderCallbackReceipt.objects.create(
            provider="mtn",
            provider_event_id=payload["event_id"],
        )
    except IntegrityError:
        return Response({"status": "duplicate"}, status=200)

    apply_the_effect(payload)
```

Return 2xx for duplicates: a 4xx/5xx makes the provider keep retrying a callback you already handled. Reserve non-2xx for genuinely unprocessable payloads. Handling *inside* the endpoint should stay minimal — persist the receipt, then hand off to a task (which needs its own guard from section 2).

---

## 4. DLQ wiring

```python
from src.shared.celery.dlq_task import DLQTask
from src.shared.celery.queues import QueueClass, queue_name

@shared_task(
    bind=True,
    base=DLQTask,
    max_retries=5,
    queue=queue_name(QueueClass.DEFAULT),
    retry_backoff=True,
    retry_backoff_max=300,
    retry_jitter=True,
)
def my_task(self, ...):
    ...
```

`DLQTask.on_failure` fires only once retries are spent (`retries == max_retries`) and writes a `FailedTask` row with redacted args, exception type/message, traceback, retry count, and correlation ID. Without `max_retries` set, *every* failure dead-letters immediately.

`retry_backoff` + `retry_jitter` matter under broker pressure: synchronized retries from many workers are how a degraded dependency turns into an outage.

Publish with `guarded_apply_async(task, queue_class=..., source="...", critical=...)` rather than `.delay()`/`.apply_async()` — it applies backpressure policy and resolves the queue name. `critical=True` exempts must-arrive work from shedding. Callers must handle `BackpressureRejected`: re-raise inside outbox handlers (the relay retries), log and degrade where the effect is losable.

**Anti-pattern:** `except Exception: logger.error(...)` with no re-raise inside a task. It converts a retryable failure into permanent silence — no retry, no `FailedTask`, no alert. Catch narrowly, or re-raise after logging.

---

## 5. Tests

Mirror the existing suites rather than inventing structure:

| What | Mirror |
|---|---|
| Emit inside/outside transaction, rollback discards event + callback, duplicate key | `backend/src/tests/core/outbox/test_emitter.py` |
| Handler dispatches correctly, re-raises `BackpressureRejected` | `backend/src/tests/core/outbox/test_handlers.py` |
| Relay: locking, status gating, retry, dead-letter, sweep | `backend/src/tests/core/tasks/test_outbox_tasks.py` |
| Service emits the right event with the right idempotency key | `backend/src/tests/core/services/test_user_invitation_outbox.py` |
| Backpressure interaction | `backend/src/tests/core/tasks/test_outbox_backpressure.py` |

The tests worth writing for a new event, beyond happy path:

- **Rollback discards the event.** Raise inside the transaction after `emit`; assert no `OutboxEvent` row and no publish callback. This is the whole point of the pattern.
- **Duplicate emit is safe.** Same idempotency key twice → `IntegrityError`, outer transaction still usable.
- **Replay is a no-op.** Call the task twice with the same `request.id`; assert the effect happened once.

`emit` uses `transaction.on_commit`, which does not fire under pytest-django's default transaction wrapping — use `@pytest.mark.django_db(transaction=True)`, as every test in `test_emitter.py` does. Symptom of forgetting: the publish assertion fails while the event row exists.

Run: `docker compose exec srr_rest_api pytest src/tests/core/outbox/ src/tests/core/tasks/test_outbox_tasks.py`

---

## 6. Review-finding template

When flagging rather than fixing, a finding earns its place by naming the window and the consequence. Keep it to four lines:

> **`src/apps/core/services/business_onboarding_service.py:119`** — dual write. The `BusinessAccessGrant` commits, then the notification is dispatched outside the transaction; a deploy or worker crash in that gap loses the notification with no record that it was owed. The grant looks complete in the database while the customer never hears about it.
> **Fix:** `emit(event_type=BUSINESS_ACCESS_GRANTED, idempotency_key=f"business_access_granted:{grant.pk}", ...)` inside the existing `transaction.atomic()`, plus a handler in `outbox/handlers/`. Want me to implement it?

Rank findings by blast radius: silent loss of a user-facing or money-adjacent effect first, duplicate side effects next, missing DLQ visibility last. Two well-argued findings beat eight generic ones — a reviewer who has to sift noise stops reading.
