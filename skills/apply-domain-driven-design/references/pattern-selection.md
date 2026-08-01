# DDD Pattern Selection

Use this guide only when a tactical pattern, context relationship, or persistence compromise is unclear.

## Contents

- [Decision guide](#decision-guide)
- [Aggregate design](#aggregate-design)
- [Services and ports](#services-and-ports)
- [Domain events](#domain-events)
- [Bounded-context integration](#bounded-context-integration)
- [Persistence compromises](#persistence-compromises)
- [Warning signs](#warning-signs)

## Decision guide

| Question | Prefer | Avoid |
| --- | --- | --- |
| Does a concept have validation, formatting, comparison, or arithmetic rules but no identity? | Value object | Repeating primitive checks across callers |
| Must an object be followed through state changes over time? | Entity | Treating identity as value equality |
| Must several changes succeed atomically to preserve a rule? | One small aggregate | A large object graph based only on database relations |
| Does a rule need state from one aggregate? | Behavior on that aggregate | A stateless service that reaches into its internals |
| Does a business calculation span concepts but belong to none? | Domain service | A generic `Helper` or `Manager` |
| Does a use case coordinate loading, authorization, domain behavior, persistence, and publication? | Application service or command handler | Putting orchestration in the aggregate |
| Does the application need a technical capability? | A port named for the need | An interface mirroring a vendor SDK |
| Did a meaningful business fact occur that other behavior reacts to? | Domain event | An event for every method call or field change |

Prefer a plain function or concrete class when none of these forces apply.

## Aggregate design

Define an aggregate around transactional consistency, not navigation convenience.

- Give one root responsibility for every invariant inside the boundary.
- Modify internal entities only through root behavior when the invariant spans them.
- Reference another aggregate by identity and accept eventual consistency across the boundary.
- Load only the state needed to make the current decision.
- Revisit the boundary when an aggregate requires frequent cross-aggregate locks, grows without bound, or must load a large graph for simple commands.

Do not use an aggregate merely as an object-shaped copy of a relational schema.

## Services and ports

Distinguish three responsibilities:

- Put a pure business operation with domain vocabulary in a domain service when no entity naturally owns it.
- Put use-case sequencing and transaction coordination in an application service.
- Put IO and vendor-specific behavior in an infrastructure adapter behind a port owned by the consuming application or domain side.

Name ports for the capability the model needs, such as `ExchangeRateProvider`, not for a vendor or protocol such as `VendorXHttpClient`.

Do not create an interface solely to make every class mockable. Prefer testing stable behavior through the public domain or application interface.

## Domain events

Use a past-tense business fact such as `OrderCancelled` when it has a concrete consumer, establishes an audit-relevant fact, or decouples work that does not belong in the current transaction.

Define:

- when the event becomes true;
- which context owns its meaning;
- whether delivery must be atomic with persistence;
- how consumers handle duplicates and ordering;
- which data is stable enough to include in the event contract.

Use a reliable publication mechanism such as a transactional outbox when losing the event after committing state would violate the required behavior. Apply the repository's reliable-messaging guidance when asynchronous delivery is part of the change.

Treat “exactly once” as a business-outcome requirement, not a transport property. Achieve it with durable intent, at-least-once retry, and an idempotent consumer or provider operation keyed by a stable command or event identifier. Call ordering alone provides no such guarantee across a database and an external system.

Do not use events to hide a direct, synchronous invariant or to avoid a clear method call within one aggregate.

## Bounded-context integration

Choose the least coupled relationship that preserves meaning:

- Translate an external or legacy model through an anti-corruption layer when its language would distort the consuming context.
- Publish an explicit contract when downstream contexts need stable facts.
- Use a shared kernel only for a deliberately co-owned, small model with coordinated change control.
- Keep separate models when two contexts use the same word with different rules.

Treat database sharing as tight coupling. If it cannot yet be removed, isolate queries behind a local port and keep foreign table shapes out of the domain model.

## Persistence compromises

Choose mapping complexity in proportion to the impedance mismatch:

- Reuse a persistence-mapped domain object when the ORM does not weaken invariants or force infrastructure concepts into business behavior.
- Separate persistence and domain models when lifecycle, lazy loading, serialization constructors, annotations, or schema constraints distort the domain model.
- Keep mapping at the adapter boundary and test it when separate models are justified.
- Persist aggregates through their roots. Do not expose generic table-oriented repositories directly to business code.

Do not create duplicate models automatically. Pay the mapping cost only when it protects a meaningful domain boundary.

## Warning signs

Reconsider the design when it contains:

- nouns copied from database tables instead of business language;
- entities with public setters and all decisions in procedural services;
- one aggregate spanning a large graph or multiple independent transactions;
- repositories for value objects or one repository per table;
- domain objects depending on controllers, transport DTOs, ORM sessions, or vendor SDKs;
- `Manager`, `Processor`, `Helper`, or `Util` classes that hide several domain responsibilities;
- events with no identified consumer or delivery semantics;
- a single shared model forced across contexts with different meanings;
- new abstractions that only pass data through without protecting a rule or isolating a capability.
