---
name: reliable-messaging
description: Design, implement, review, or diagnose reliable asynchronous messaging in any codebase using transactional outbox, idempotent consumer or inbox patterns, bounded retries, and dead-letter recovery. Use when a flow both changes durable state and dispatches a task, event, notification, webhook, or external API call; when creating or modifying workers, queues, event consumers, scheduled jobs, or callback endpoints; or when investigating lost, duplicated, delayed, out-of-order, retried, or stuck work. Inspect and reuse the target codebase's existing transaction, messaging, idempotency, retry, and observability mechanisms instead of assuming a particular language, framework, broker, or schema.
---

# Reliable messaging

Treat reliable messaging as a consistency problem across independently failing systems. Adapt the patterns to the target repository's architecture and delivery guarantees.

## Establish the local contract first

Before proposing or changing code:

1. Identify the durable state store and transaction boundary.
2. Identify every handoff: task queue, event bus, webhook, notification provider, external API, or scheduler.
3. Determine the documented delivery semantics. If they are unclear, design consumers for redelivery.
4. Search for existing outbox, inbox, idempotency, retry, dead-letter, leasing, reconciliation, and observability components.
5. Trace one complete producer-to-consumer flow, including failure and replay paths.

Reuse established local machinery and naming. Do not introduce a parallel reliability framework when the repository already has one. If it has none, implement the smallest coherent mechanism that satisfies the required guarantees.

## Failure model

Check every asynchronous flow for these hazards:

1. **Dual write:** durable state commits but message publication fails, or publication succeeds while state rolls back.
2. **Duplicate delivery:** a broker, scheduler, client, or provider retries work whose first attempt may already have taken effect.
3. **Terminal failure:** retries stop without a durable record, alert, owner, or replay path.
4. **Concurrent or out-of-order handling:** multiple workers apply incompatible transitions or an older message overwrites newer state.

Name the exact failure window and consequence. Avoid generic reliability warnings without a concrete path through the code.

## Choose the minimum sufficient pattern

| Situation | Pattern |
|---|---|
| A committed state change implies an effect that must eventually happen | Transactional outbox written in the same transaction |
| A consumer may receive the same logical message more than once | Durable idempotency key, inbox receipt, state gate, or provider-supported idempotency |
| An external callback may be retried | Inbox receipt keyed by the sender's stable event identifier |
| A failure needs investigation or replay after retries | Bounded retries plus durable dead-letter handling |
| Processing order affects correctness | Aggregate/version key, monotonic transition guard, or partitioned ordering |
| The effect is intentionally losable, such as a best-effort metric or cache warm | Direct dispatch with explicit best-effort semantics |

Do not add infrastructure merely because a pattern exists. First establish the business guarantee: must the effect happen, may it happen more than once, must it happen in order, and who acts when it cannot complete?

## Transactional outbox

Use an outbox when one database transaction creates an obligation to communicate with another system.

- Write the domain change and outbox record atomically.
- Give the event a stable identifier or unique idempotency key derived from the domain fact, not a random value generated on each retry.
- Store a versioned event type, minimal serializable payload, creation time, delivery state, and attempt metadata.
- Publish through a relay that supports safe concurrent claims, retry with backoff, stale-claim recovery, and terminal failure handling.
- Treat post-commit immediate publication as a latency optimization; retain polling or reconciliation as the recovery path.
- Keep secrets and unnecessary personal data out of durable payloads and failure records.

An after-commit callback alone fixes rollback ordering but still leaves a commit-to-publish crash window. It is sufficient only when silent loss is acceptable or another durable reconciliation path exists.

## Idempotent consumers and inboxes

Assume redelivery unless the complete transport contract proves otherwise.

- Prefer a producer-supplied logical event ID that remains stable across retries.
- Enforce deduplication with an atomic primitive: a unique constraint, compare-and-set, conditional update, or transactional state transition.
- Store an inbox receipt in the same transaction as the durable effect when both use the same database.
- For external side effects, pass the logical event ID as the provider's idempotency key when supported.
- Gate state transitions by current state or version so stale and concurrent messages become safe no-ops.
- Use expiring cache locks only for bounded duplicate suppression where losing the guard is acceptable; they are not a substitute for durable idempotency when correctness depends on it.

Never rely on a check-then-act existence query without an atomic constraint. Concurrent consumers can both pass the check.

## Retries and dead-letter recovery

- Retry only failures that may succeed later.
- Use bounded exponential backoff with jitter and explicit timeouts.
- Separate permanent validation or contract failures from transient dependency failures.
- Persist terminal failures with the message identity, safe payload context, error classification, attempt count, timestamps, and correlation data.
- Provide an observable replay or reconciliation path with access control and audit history.
- Make replay safe through the same consumer idempotency mechanism; never depend on operators avoiding duplicate effects manually.
- Redact secrets and sensitive data from logs, dead-letter records, and admin tools.

Self-healing sweepers that re-derive work from durable state may not need their own dead-letter record. Document why a missed or failed run recovers automatically.

## Ordering and concurrency

When order matters, identify the ordering scope: account, order, payment, user, or another aggregate. Use one or more of:

- partitioning by aggregate key;
- sequence or version checks;
- row locks or atomic conditional updates;
- monotonic state machines that reject stale transitions;
- reconciliation against the source of truth.

Do not claim global ordering unless the transport and consumer topology actually provide it.

## How to act

When implementing, build the correct reliability boundary as part of the requested flow and add focused tests for rollback, redelivery, concurrency, retry exhaustion, and replay.

When reviewing or diagnosing, report:

1. the precise producer, handoff, and consumer involved;
2. the concrete failure window;
3. the user or system consequence;
4. the smallest fix compatible with existing architecture;
5. the evidence needed to verify the guarantee.

Respect read-only requests. Do not refactor adjacent messaging code unless it is in scope.

## Implementation reference

Read [references/implementation.md](references/implementation.md) before implementing or substantially redesigning a flow. It provides framework-neutral discovery, data models, algorithms, tests, and review templates. Translate its pseudocode into the repository's established language and conventions.
