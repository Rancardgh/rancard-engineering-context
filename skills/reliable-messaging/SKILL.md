---
name: reliable-messaging
description: Route async side effects through the backend's transactional outbox, add consumer idempotency (inbox) guards, and attach dead-letter handling — this repo has ready-made machinery for all three (src/apps/core/outbox/, DLQTask, guarded_apply_async). Use this skill whenever you write, modify, or review backend code that (a) saves Django models and also dispatches a side effect in the same flow — a Celery task (.delay/apply_async/guarded_apply_async), SMS/email/push notification, telco/NIA/ORC/partner API call, or webhook; (b) defines or edits any Celery task (global task_acks_late=True makes delivery at-least-once, so duplicates arrive); (c) adds an endpoint that receives external callbacks or webhooks; or (d) touches retry logic or investigates lost, duplicated, or stuck messages, notifications, or events. Apply it even when the request never mentions reliability — e.g. "send a notification when X happens", "call the telco after registration", "add a background job".
---

# Reliable messaging: transactional outbox, idempotent consumers, DLQ

The backend runs Celery on Redis with `task_acks_late=True` set globally (`backend/src/celery.py`). Three facts follow, and they shape every async flow in this codebase:

1. **A DB write plus a dispatch is two systems with no shared transaction.** Dispatch inside `transaction.atomic()` and a rollback leaves a phantom task already published (or the task races ahead of the commit and can't see the row). Dispatch after the commit and a crash, deploy, or broker outage in the gap loses the side effect — silently, with nothing recorded anywhere.
2. **Every task is delivered at least once.** Acks-late means the broker redelivers the same message (same task ID) if a worker dies after executing but before acking. A task body that isn't replay-safe will double-send, double-call, or double-transition.
3. **Redis has no native dead-letter queue.** A task that exhausts its retries just logs and vanishes unless it writes a durable failure record.

The naive version of any of these flows looks correct and passes tests — the failures only appear under crashes, deploys, and broker pressure. The repo has purpose-built machinery for all three problems. Use it; don't hand-roll alternatives and don't ship naive dispatches.

## Machinery map

| Piece | Path | Role |
|---|---|---|
| `emit()` | `backend/src/apps/core/outbox/emitter.py` | Writes an `OutboxEvent` inside the caller's transaction (raises if there is no active atomic block), publishes via `on_commit` |
| `OutboxEvent` | `backend/src/apps/core/models/outbox.py` | Durable intent: event_type, unique idempotency_key, payload, status machine, attempts |
| Handlers + registry | `backend/src/apps/core/outbox/handlers/`, `registry.py` | One `handle(payload)` module per event type, mapped in `HANDLER_REGISTRY` |
| Relay | `backend/src/apps/core/tasks/outbox_tasks.py` | `process_outbox_event` (locked, status-gated, retried, DLQ'd) + `sweep_pending_outbox_events` beat task that recovers anything the on_commit publish missed |
| `DLQTask` | `backend/src/shared/celery/dlq_task.py` | Base task class; writes a redacted `FailedTask` row on final retry exhaustion |
| FailedTask admin | Django admin → "Failed Tasks (DLQ)" | Operator visibility and replay for dead-lettered work |
| `guarded_apply_async` | `backend/src/shared/celery/backpressure.py` | The sanctioned publish wrapper — backpressure-aware; use instead of bare `.delay()`/`.apply_async()` |
| Exemplars | `user_invitation_service.py` (emit in service), `admin_investigations_view.py` (emit from async view), `send_sms_tasks.py` (acks-late replay guard) | Copy these, not from memory |

## Hazard 1 — dual write → use the outbox

**Detect:** in one logical flow (service method, view, task), a model write (`create`/`save`/`update`/`bulk_*`) *and* a side-effect dispatch: `.delay()`, `.apply_async()`, `guarded_apply_async()`, a `NotificationDispatcher`/`EmailContext`/SMS call, or a direct integration call (telco, NIA, ORC, partner webhook). `transaction.on_commit(...)` around the dispatch is still a detection hit — it fixes ordering and rollback, but the commit→publish crash window remains, and a `BackpressureRejected` raised there is swallowed with no durable record.

**Fix:** call `emit(event_type=..., idempotency_key=..., payload=...)` *inside* the domain transaction, and move the dispatch into an outbox handler. The relay then owns delivery: retries with backoff, stale-lock recovery via the beat sweep, dead-lettering after exhaustion. Full recipe in [references/implementation.md](references/implementation.md).

**When direct dispatch is fine:** the effect is losable by design — ops alerts, metrics, cache warming, log fan-out. Use `guarded_apply_async` (wrapped in `on_commit` if it depends on committed state) and move on. The test: if this dispatch silently never happened, would anyone need to know? "No" → skip the outbox.

## Hazard 2 — at-least-once delivery → guard consumers

**Detect:** any task body with a non-replay-safe effect — external API call, message send, counter increment, state transition, row creation — and no guard. Global acks-late means this applies to *every* task, not just ones with explicit retries. Also detect: inbound webhook/callback endpoints (telcos, partners, payment/identity providers) that apply effects without deduplicating, since external senders retry on their own schedule.

**Fix (pick per effect type):**
- Transient effect (send an SMS): Redis `SET NX` on `self.request.id` — see the guard at the top of `send_sms_task` and its comment about why `self.retry()` still works.
- DB state transition: status-gate inside `select_for_update`, exactly like `process_outbox_event` skipping DELIVERED/DEAD_LETTER events.
- Row creation: unique constraint on a natural key + `get_or_create` / `IntegrityError` handling.
- Inbound callbacks: persist the provider's event ID with a unique constraint in the same transaction as the effect (an inbox ledger); a redelivery becomes a clean no-op response.

## Hazard 3 — retry exhaustion → DLQ

**Detect:** a `@shared_task`/`@app.task` whose failure someone would need to act on, without `base=DLQTask`. Retries without a terminal record (`autoretry_for` + `max_retries` alone). Broad `except Exception` that logs and returns, converting a retryable failure into silence.

**Fix:** `bind=True, base=DLQTask, max_retries=N, retry_backoff=True` (mirror the `process_outbox_event` decorator). Final failure then lands as a `FailedTask` row visible in the admin, with redacted args and a replay path.

**Skip DLQ for:** periodic beat sweepers that re-derive their work from DB state each run (a missed run self-heals), and losable effects per Hazard 1.

## Decision rubric

| Situation | Do |
|---|---|
| DB state change implies an effect that must eventually happen (registration → telco call, grant → notification, reset → email) | `emit()` in the transaction + handler |
| Effect is losable (alert, metric, cache warm) | `guarded_apply_async`, `on_commit` if it reads committed state |
| Writing any task body | Add the matching replay guard — always; acks-late is global |
| Endpoint receives external callbacks | Inbox ledger keyed on the provider's event ID |
| Task failure needs a human or a replay | `base=DLQTask` + bounded retries with backoff |
| Beat sweeper over DB state | No DLQ, no outbox — it self-heals |

## How to act on a finding

**You are writing or modifying the flow:** build it with the correct pattern from the start — don't ship the naive version and then remark on it. Note the choice in one line of your summary ("routed through the outbox as `EventType.X`"); no lecture.

**You are reviewing, diagnosing, or merely near the code:** flag it — `file:line`, the concrete failure scenario in one sentence ("a deploy between this commit and this `.delay()` loses the email, and nothing records that"), the minimal fix, and an offer to implement. Don't drive-by refactor code you weren't asked to touch, and don't pad reviews with generic reliability advice — a finding without a specific failure scenario is noise.

**Don't flag at all:** losable effects (alerts, metrics, cache warming), self-healing beat sweepers, task→task chains whose parent is already durable (e.g. an outbox handler re-raising `BackpressureRejected` so the relay retries — the chain inherits durability from the event row), and read-only flows.

## Implementing

Read [references/implementation.md](references/implementation.md) before writing code. It has the end-to-end recipe for a new outbox event (event type → emit → handler → registry → queue classification → tests), the three idempotency guards with code, the DLQ task template, the inbound-callback inbox recipe, and which existing test files to mirror.
