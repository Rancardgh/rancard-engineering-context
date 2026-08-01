---
name: apply-domain-driven-design
description: Apply pragmatic Domain-Driven Design while writing or refactoring application code. Use automatically whenever Codex implements business rules, workflows, policies, state transitions, domain validation, use cases, entities, value objects, aggregates, repositories, or domain events—even when the user does not mention DDD. Also use when changing code whose terminology or ownership spans business domains. Do not use for purely technical configuration, dependency bumps, formatting, generated code, or infrastructure with no business behavior.
---

# Apply Domain-Driven Design

Model business decisions explicitly while keeping the implementation no more complex than the domain requires.

## Operating rules

- Start from observable business behavior, not from DDD patterns or package layouts.
- Reuse the project's established language and boundaries before introducing new terms.
- Encode business invariants in the domain model at the point where state can change.
- Keep orchestration in the application layer and technical details behind adapters or existing project seams.
- Choose the smallest useful DDD pattern. Do not manufacture aggregates, repositories, services, events, or interfaces for ceremony.
- Preserve public behavior unless the requested change explicitly alters it.
- Make assumptions visible when they affect business behavior. Do not invent a rule that cannot be recovered from code, tests, specifications, or the user.
- Continue normal implementation without adding an approval gate. Ask only when unresolved domain ambiguity would materially change behavior or data ownership.

## Workflow

### 1. Recover the domain context

Read repository instructions first. Then inspect the narrow business area being changed:

- Read `CONTEXT-MAP.md`, the relevant `CONTEXT.md`, ADRs, specifications, and acceptance criteria when present.
- Trace the existing request or event flow through interfaces, application logic, domain logic, and persistence.
- Read nearby tests to recover expected behavior, edge cases, and established terminology.
- Identify the bounded context that owns the decision. Treat the same word in another context as a different model until the code proves otherwise.
- Record contradictions between documentation, code, and tests instead of silently choosing one.

Do not perform a whole-codebase architecture audit for a scoped implementation task.

### 2. Express the behavior before shaping the model

Reduce the change to one or more concrete scenarios:

```text
Given <business state and preconditions>
When  <actor issues a command or an event arrives>
Then  <business outcome and observable side effects>
And   <invariants that must still hold>
```

Identify:

- the command or intent;
- the business state required to decide;
- the invariant or policy being enforced;
- valid outcomes and domain-specific failures;
- transaction and consistency requirements;
- delivery, retry, and idempotency requirements for external side effects;
- facts that other parts of the system need after the decision.

Use code and tests to answer these questions when possible. Ask the user only for a decision that cannot safely be inferred.

### 3. Classify the change

Classify each piece before adding structure:

| Kind | Put it in | Typical examples |
| --- | --- | --- |
| Business decision | Domain model | eligibility, pricing rule, state transition, invariant |
| Use-case coordination | Application layer | load, invoke domain behavior, save, publish |
| Translation or delivery | Interface/adapter | HTTP DTO mapping, message decoding, presenter |
| Technical capability | Infrastructure adapter | database, clock, email, payment gateway, queue |

Keep domain code framework-light where the repository allows it. Prevent controllers, ORM entities, transport DTOs, and vendor SDK types from becoming the vocabulary of the business model.

### 4. Model the smallest consistency boundary

Select patterns by responsibility:

- Use a value object for a validated, immutable concept whose equality is its value.
- Use an entity only when identity and lifecycle matter.
- Use an aggregate to protect invariants that must remain consistent in one transaction. Keep it small and reference other aggregates by identity.
- Put behavior on the entity or value object that owns the required state.
- Use a domain service only for a domain operation that genuinely belongs to no single entity or value object.
- Use a repository or port for aggregate persistence or an external capability needed by a use case, not as an interface for every class.
- Raise a domain event only for a meaningful past-tense business fact with a real downstream consumer or decoupling need.

Read [references/pattern-selection.md](references/pattern-selection.md) when the correct tactical pattern, context relationship, or persistence compromise is not obvious.

### 5. Implement from domain decision outward

Follow the repository's existing structure while keeping dependencies pointed toward business policy:

1. Add or update executable examples for the invariant and its edge cases.
2. Implement the rule in the owning domain type.
3. Orchestrate the use case in application code.
4. Adapt persistence, messaging, time, and external services at existing or justified seams.
5. Map transport input and output at the system edge.

Prefer intention-revealing operations such as `order.cancel(reason)` over sequences of public setters. Make invalid state difficult to construct, and return domain-specific failures that callers can map without parsing strings.

For an existing anemic or transaction-script codebase, improve the touched slice incrementally. Add characterization tests first when behavior is risky. Do not repackage the whole application or create parallel models merely to appear domain-driven.

Treat a local state change followed by external IO as a distributed consistency boundary. When the requirement says a side effect must happen exactly once, do not infer that guarantee from call ordering. Persist the intent atomically with the domain change, dispatch it with retries, and use a stable idempotency key at the receiving boundary. If the available infrastructure cannot provide the required outcome, state the limitation instead of claiming the guarantee.

### 6. Respect bounded contexts

- Keep one canonical meaning for each term inside a context.
- Translate at the boundary when two contexts use different models or meanings.
- Avoid shared mutable domain models across contexts.
- Depend on another context's explicit contract, not its internal entities or tables.
- Update an existing glossary when a stable term changes. Create new domain documentation only when the repository's conventions call for it or the user requests it.

### 7. Verify at the right levels

- Test domain rules with examples that name the business behavior.
- Test application services for orchestration, authorization decisions, transaction behavior, and requested side effects.
- Test adapters with contract or integration tests where mapping, persistence, or delivery can fail.
- Include invalid transitions, boundary values, duplicate commands or events, and concurrency when the domain makes them relevant.
- Inject a failure before and after each distributed side effect when delivery guarantees matter, then verify retries neither lose nor duplicate the business outcome.
- Run the smallest authoritative test set first, then the repository's required validation.

Verify behavior rather than private method structure. Do not weaken invariants or expose internals solely to make a test convenient.

## Completion standard

Finish the requested implementation and report:

- the business behavior encoded;
- the model boundary and important pattern choices;
- the tests or checks run;
- any unresolved domain assumption or cross-context risk.

Keep this explanation proportional to the change. Do not turn a small implementation into a design document.
