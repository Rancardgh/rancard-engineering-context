# Coding Standards

These standards apply to modernization work in this repository. They are based
on the newer Rancard Bulk Messaging API style, adapted for this legacy codebase.

## General Rules

- Keep code simple and direct.
- Make small, focused commits.
- Preserve existing public API behavior unless a change is explicitly planned.
- Add tests for behavior changes and risky refactors.
- Avoid broad formatting-only rewrites until the codebase has a stable baseline.
- Do not introduce new features until stabilization phases are complete.

## Java And Spring

- Target runtime: Java 21.
- Target Spring Boot line: 3.5.x, pinned to the version used by
  `RANCARD-Bulk-Messaging-API` at the time of upgrade.
- Current Bulk Messaging target observed for this plan: Spring Boot 3.5.13.
- Prefer Spring Boot dependency management over hardcoded dependency versions.
- Do not mix runtime upgrade work with UI redesign or domain refactors.

## Layering Direction

Move gradually toward these package responsibilities:

- `domain`: business concepts, value types, domain rules, and framework-light
  behavior.
- `application`: use cases, orchestration, and ports/interfaces needed by use
  cases.
- `infrastructure`: concrete adapters for databases, HTTP clients, Redis,
  MongoDB, Sentry, mail, files, and external services.
- `interfaces`: web controllers, request/response mapping, frontend-facing
  adapters, and other delivery mechanisms.

The existing code does not need to be moved all at once. Apply the structure
domain by domain as phases introduce tests and safety.

## Interfaces And SOLID

Use interfaces when they define a real boundary:

- database access needed by application use cases,
- external service clients,
- application use cases called by controllers,
- time, storage, mail, Sentry, or other replaceable infrastructure,
- adapters that need mocking in tests.

Do not create one interface for every class by default. If there is only one
small internal implementation and no boundary value, keep it concrete.

Controllers should stay thin:

- accept and validate input,
- call a use case,
- map output to the existing response shape.

Application services should not depend directly on Spring MVC controllers,
raw HTTP clients, JPA entities, or static frontend asset details.

## Reactive Code

Reactive work is incremental.

- New or refactored application flows may use `Mono<T>` and `Flux<T>` when the
  flow benefits from composition, async external calls, or backpressure.
- Existing blocking JPA/JDBC access remains behind ports.
- Blocking adapters must be explicit when called from reactive flows.
- Do not claim blocking MySQL/JPA code is nonblocking.
- Do not convert every controller at once.

## Database Changes

Existing MySQL and MongoDB stores remain in place.

Allowed during stabilization:

- additive MySQL indexes,
- additive Mongo indexes,
- explicit versioned SQL or Mongo index scripts,
- `EXPLAIN` evidence where DB access is available.

Not allowed during stabilization:

- table redesign,
- data migration,
- engine changes,
- destructive schema changes,
- silent schema changes through `ddl-auto=update` as the long-term plan.

## Sentry And Observability

Backend and frontend Sentry integrations must be configurable and safe.

- DSNs are supplied through environment/profile config at the end of execution.
- DSNs are never committed.
- The app must run when DSNs are absent.
- Mask or omit MSISDNs, tokens, passwords, secrets, and raw request bodies.
- Add breadcrumbs/tags around high-value flows only when they help diagnose
  production failures.


## Commit Discipline

Each implementation phase should end with one focused conventional commit.
If a phase becomes too large, split it by subsystem before committing.

Use commit prefixes consistently:

- `docs:` for documentation-only changes.
- `build:` for build/runtime/dependency changes.
- `ci:` for GitHub Actions and automation.
- `test:` for tests.
- `fix:` for user-visible bug fixes.
- `refactor:` for behavior-preserving structure changes.
- `perf:` for performance improvements such as indexes.
- `style:` for UI styling or formatting-only changes.
- `feat:` only after stabilization permits new features.