---
name: solid-codebase-review
description: Audit an entire codebase against SOLID principles, produce evidence-backed findings and an approval-gated remediation plan, then implement only approved changes. Use for explicit SOLID, architecture, maintainability, or code-quality reviews and whenever Codex is asked to write, add, change, fix, refactor, or implement code. Default to the entire application-owned codebase unless the user explicitly narrows the audit scope.
---

# SOLID Codebase Review

Apply SOLID pragmatically across the codebase before changing code. Separate the read-only audit and proposal from implementation with an explicit approval gate.

## Non-negotiable behavior

- Begin in read-only mode. Do not edit files, install dependencies, create branches, commit, or perform other mutations during the audit.
- Audit the entire application-owned codebase unless the user explicitly limits the audit to named files, directories, modules, packages, or services. Do not infer a narrow audit scope merely because the requested implementation concerns one feature.
- Inventory the repository before evaluating it. Do not substitute representative sampling, recent diffs, obvious hotspots, or selected modules for full coverage.
- Read and follow repository instructions such as `AGENTS.md`, contribution guides, architecture documents, and test conventions.
- Inspect the working tree and preserve unrelated or pre-existing changes.
- Present findings and a remediation plan, then stop for explicit approval.
- Treat approval as scoped to named finding IDs or phases. Implement nothing else without returning for approval.
- Do not force abstractions or patterns where the existing design is a reasonable tradeoff.

## Stage 1: Establish scope and coverage

1. Identify repository boundaries, languages, frameworks, packages, applications, entry points, and test suites.
2. Enumerate every relevant application-owned source file and module.
3. Include tests, dependency wiring, configuration, background jobs, commands, adapters, integrations, and shared utilities when they reveal or contribute to design decisions.
4. Exclude generated code, vendored dependencies, build outputs, caches, and third-party code unless the user includes them.
5. Maintain a coverage ledger recording:
   - every relevant directory or module examined;
   - files included;
   - files excluded and the reason;
   - areas that could not be assessed and why.
6. Do not claim completion while relevant areas remain unexamined. State limitations plainly.

For unusually large repositories, continue the inventory and audit in manageable batches while maintaining one cumulative coverage ledger. Ask to narrow scope only when exhaustive review is genuinely infeasible; never silently sample.

## Stage 2: Evaluate SOLID principles

Assess behavior and dependency structure, not superficial size or style.

### Single Responsibility Principle

Identify code with multiple unrelated reasons to change, especially business rules mixed with persistence, transport, presentation, orchestration, logging, or infrastructure.

### Open/Closed Principle

Identify designs that repeatedly require central conditionals, dispatchers, or stable implementations to change when behavior is added. Do not recommend extension points without a demonstrated variation pressure.

### Liskov Substitution Principle

Identify subtypes or implementations that violate contracts, invariants, accepted inputs, outputs, error behavior, or caller expectations. Look for unsupported operations, surprising overrides, and subtype-specific caller branches.

### Interface Segregation Principle

Identify interfaces, protocols, base classes, or service contracts that force consumers to depend on methods or data they do not use. Propose separation only around cohesive consumer needs.

### Dependency Inversion Principle

Identify high-level policy coupled directly to frameworks, databases, network clients, filesystems, global state, or concrete implementations where that coupling materially obstructs testing, replacement, or reuse.

Classify observations as one of:

- confirmed SOLID violation;
- context-dependent concern;
- acceptable tradeoff;
- non-SOLID code-quality issue.

Do not present the latter three as confirmed SOLID violations.

## Stage 3: Produce evidence-backed findings

Give each proposed issue a stable ID such as `SOLID-001`. For every issue include:

- principle and classification;
- severity: critical, high, medium, or low;
- confidence: high, medium, or low;
- exact paths and relevant symbols or line references;
- current responsibility or dependency structure;
- concrete evidence of the violation;
- practical impact on maintainability, testing, extensibility, correctness, or delivery;
- proposed design direction, without prematurely implementing it;
- expected files and components affected;
- effort and implementation risk;
- dependencies or conflicts with other findings;
- tests required to protect behavior;
- compatibility, migration, and rollout concerns.

Avoid vague claims such as "too large," "too complex," or "tightly coupled" without identifying distinct change drivers, broken contracts, consumer burdens, or inverted dependency direction.

## Stage 4: Present the approval package

Report in this order:

1. Repository and architecture summary.
2. Coverage ledger.
3. Executive summary of the most important findings.
4. Detailed findings grouped by SOLID principle.
5. Prioritized remediation plan.
6. Recommended implementation phases.
7. Risks, assumptions, and unresolved questions.
8. Approval checklist listing the finding IDs available for individual or phase approval.

When the user requested new or changed code, connect that requested work to the findings and show how it should be implemented after approval. Include a scoped implementation proposal even when the audit finds no SOLID violation.

Stop after the approval package. Ask the user to approve specific IDs or phases.

## Stage 5: Implement approved work

After explicit approval:

1. Recheck the working tree and approved scope.
2. Implement only the approved findings and requested behavior.
3. Preserve public behavior unless the approved plan explicitly changes it.
4. Prefer focused, incremental refactoring over broad rewrites.
5. Avoid speculative abstractions and unnecessary patterns.
6. Add or update tests that protect behavior and validate the design.
7. Run the relevant formatter, static analysis, unit, integration, and architectural checks.
8. Reassess affected callers and implementations for regressions.
9. Return for approval before materially expanding scope.

After each approved phase, report:

- finding IDs completed;
- files changed;
- key design decisions;
- validation performed and results;
- remaining risks and follow-up work;
- findings revised or invalidated by implementation evidence.

If full validation cannot run, state exactly what was and was not verified.
