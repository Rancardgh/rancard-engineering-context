# Implementation recipes

Contents:

1. [Repository discovery](#1-repository-discovery)
2. [Transactional outbox](#2-transactional-outbox)
3. [Relay and recovery](#3-relay-and-recovery)
4. [Consumer idempotency](#4-consumer-idempotency)
5. [Inbound callback inbox](#5-inbound-callback-inbox)
6. [Retries and dead-letter handling](#6-retries-and-dead-letter-handling)
7. [Ordering and concurrency](#7-ordering-and-concurrency)
8. [Verification](#8-verification)
9. [Review-finding template](#9-review-finding-template)

## 1. Repository discovery

Map the actual architecture before choosing an implementation. Search code, configuration, migrations, and operational documentation for:

- queue, broker, worker, consumer, subscriber, publisher, event, task, job, scheduler;
- outbox, inbox, idempotency, deduplication, correlation, replay, reconciliation;
- retry, backoff, timeout, dead letter, failed message, poison message;
- transaction, unit of work, commit hook, row lock, lease, compare-and-set;
- metrics, tracing, structured logs, alerts, dashboards, and admin replay tools.

Record the answers to these questions:

| Question | Evidence to find |
|---|---|
| What commits the source-of-truth state? | Database and transaction API |
| What performs the handoff? | Queue client, event publisher, HTTP client, scheduler |
| What are the delivery guarantees? | Broker configuration and consumer acknowledgement behavior |
| How is a logical message identified? | Event ID, task ID, correlation ID, provider reference |
| What prevents duplicate effects? | Unique constraint, conditional update, inbox, provider key |
| What happens after final failure? | Dead-letter store or queue, alert, owner, replay command |
| How is abandoned work recovered? | Poller, lease expiry, sweeper, reconciliation job |

Do not infer guarantees from library defaults alone. Verify repository configuration and the surrounding transaction flow.

## 2. Transactional outbox

Use the repository's migration and persistence conventions. A minimal outbox record usually needs:

```text
OutboxMessage
  id                 stable unique identifier
  event_type         versioned logical contract name
  aggregate_key      optional ordering or partition key
  idempotency_key    unique domain-derived key
  payload            serialized, minimal, non-secret data
  status             pending | processing | delivered | dead_letter
  attempts           non-negative count
  available_at       next eligible attempt
  claimed_at         nullable lease timestamp
  claimed_by         nullable worker identity
  last_error         redacted summary
  created_at
  delivered_at
```

Write the domain state and message in one transaction:

```text
begin transaction
  change domain state
  insert outbox message(
    idempotency_key = stable key derived from the domain fact,
    event_type = versioned contract,
    payload = identifiers and required immutable values
  )
commit transaction
```

Choose the key from the obligation itself, such as `invoice-issued:<invoice-id>:v2` or `welcome-email:<registration-id>`. A fresh random key on every retry defeats deduplication.

Keep the payload forward-compatible:

- include a schema or event version;
- serialize platform-neutral scalar values;
- pass identifiers and immutable facts, not process-local objects;
- define whether consumers re-read current state or act on the emitted snapshot;
- minimize personal data and never store credentials or access tokens.

If inserting a duplicate key is possible through caller retry, convert the unique-conflict outcome into the repository's established "already recorded" behavior without weakening the surrounding transaction.

## 3. Relay and recovery

The relay must tolerate multiple workers, crashes, and broker outages.

```text
repeat:
  atomically claim eligible pending messages with a bounded lease
  for each claimed message:
    try:
      publish using message.id as the stable message identity
      mark delivered
    catch transient failure:
      increment attempts
      schedule next attempt with exponential backoff and jitter
    catch permanent failure or exhausted retries:
      mark dead_letter and alert
```

Use the database's supported concurrency primitive: row locks with skip-locked semantics, an atomic status update, advisory locks, or a lease token. Ensure only the current lease owner can complete or release a claim.

Recover claims whose lease expires. A crash after publish but before marking delivery can publish twice, so consumers must still be idempotent. An outbox provides at-least-once handoff, not magical exactly-once effects.

An immediate post-commit publish can reduce latency, but a periodic relay or reconciliation path must remain authoritative.

## 4. Consumer idempotency

Choose the guard that matches the effect.

### Durable database effect

Store the receipt and effect atomically:

```text
begin transaction
  insert inbox receipt(message_id) with unique constraint
  if duplicate:
    commit and acknowledge success
  apply durable state change
commit transaction
acknowledge message
```

If processing fails, roll back both the receipt and effect so redelivery can retry.

### State transition

Use an atomic condition or lock:

```text
update entity
set state = next_state, version = version + 1
where id = entity_id
  and state in allowed_predecessors
  and version = expected_version
```

Treat zero updated rows as duplicate, stale, conflicting, or missing according to the domain contract.

### Row creation

Put a unique constraint on the natural business key and use an atomic create-or-return operation. A prior existence query is only an optimization and cannot be the correctness guard.

### External provider effect

Pass the logical message ID as the provider's idempotency or request key. Persist the provider reference and outcome. When the provider lacks idempotency support, distinguish these states explicitly:

- not attempted;
- attempt outcome known successful;
- attempt outcome known failed;
- outcome unknown because the connection failed after submission may have occurred.

Do not blindly retry an unknown outcome when duplication is harmful. Reconcile with the provider or require a safe business decision.

### Ephemeral duplicate suppression

An expiring cache key or distributed lock is suitable only when the effect's duplicate window is bounded and losing the key is acceptable. Document the TTL basis and failure behavior.

## 5. Inbound callback inbox

Validate authentication and schema before deduplication. Use the sender's stable event ID, not a locally generated request ID.

```text
validate signature and payload
begin transaction
  insert callback receipt(provider, provider_event_id) with unique constraint
  if duplicate:
    commit and return the protocol's success response
  apply the durable effect or write an outbox message for later work
commit transaction
return success
```

Return success for an already processed valid callback so the sender stops retrying. Return an error only when the protocol requires retry or the payload cannot be accepted.

If heavy work is handed to a consumer, that consumer still needs its own idempotency guard because callback receipt deduplication and worker redelivery are separate boundaries.

## 6. Retries and dead-letter handling

Define an explicit policy per dependency or message type:

- retryable error classes;
- non-retryable error classes;
- per-attempt timeout;
- maximum attempts or elapsed retry window;
- exponential backoff cap and jitter;
- terminal storage location;
- alert threshold and owner;
- replay or reconciliation procedure.

A durable dead-letter record should include message identity, contract type and version, redacted payload context, correlation identifiers, error classification, attempt history, timestamps, and current disposition. Restrict access and audit replay.

Replay through the normal consumer path so idempotency and validation still apply. Do not edit failed payloads silently; preserve the original and record any corrected replacement.

Avoid broad exception handlers that log and return success. They convert retryable failures into silent loss. Catch narrowly or rethrow after adding context.

## 7. Ordering and concurrency

Choose the smallest ordering scope required by the domain. Prefer per-aggregate ordering over global ordering.

- Partition messages by aggregate key when the broker supports ordered partitions.
- Include aggregate version or sequence in each message.
- Reject or defer stale and future versions explicitly.
- Make state machines monotonic where possible.
- Use reconciliation when messages can arrive permanently out of order.

Document what happens when version 12 arrives before version 11 and when version 11 arrives after version 12.

## 8. Verification

Use the repository's existing test stack. Cover the failure boundaries, not just the happy path:

- rolling back the domain transaction leaves no outbox obligation;
- committing state creates exactly one logical outbox obligation;
- duplicate producer attempts resolve through the unique idempotency key;
- a crash after publish and before acknowledgement causes safe redelivery;
- two consumers racing produce one durable effect;
- a stale lease is recovered;
- transient failures retry with bounded backoff;
- permanent or exhausted failures become observable dead letters;
- replay is safe and audited;
- duplicate callbacks return the expected success response;
- stale or out-of-order messages cannot regress state;
- sensitive values are absent from logs and failure records.

Run focused tests first, then the repository's authoritative broader validation. Verify migrations, schemas, configuration, and operational documentation when they change.

## 9. Review-finding template

Keep each finding concrete:

> **`path/to/producer:line` — dual-write loss window.** The domain record commits before the message is durably recorded. A process crash or broker outage in that gap leaves the record complete while the required side effect is never attempted and no recovery process can discover it. **Fix:** write a uniquely keyed outbox message in the same transaction and publish it through the existing relay or reconciliation mechanism.

Include the consumer location when duplicate delivery or ordering is part of the risk. Rank findings by business impact: money or irreversible external effects, security and identity transitions, user-visible loss, duplicate notifications, then observability gaps.
