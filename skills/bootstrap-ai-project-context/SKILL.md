---
name: bootstrap-ai-project-context
description: Convert technical documentation and repository evidence into an agent-ready project context. Use when a user asks to assess one or more technical documents or folders, create or improve an AGENTS.md or CLAUDE.md guide, establish a specs/ directory, define project milestones, or create requirements, plan, and validation records. Start with read-only assessment unless the user explicitly authorizes generation or revision.
---

# Bootstrap AI project context

Build a reliable project context from evidence. Keep the agent guide concise. Keep detailed project knowledge in `specs/`.

## Select the mode

Use one mode for each request:

| Mode | Purpose | Writes files |
| --- | --- | --- |
| `assess` | Analyze documents and repository context. Propose the project guide and `specs/` structure. | No |
| `bootstrap` | Create the approved agent guide and project-wide specifications. | Yes |
| `plan-milestone` | Create or revise one dated milestone's requirements, plan, and validation records. | Yes |

Treat `assess` as read-only. Do not create, modify, stage, or delete files in this mode.

For `bootstrap` or `plan-milestone`, first perform the applicable assessment. Write files only when the user explicitly requests the change or approves the assessment output.

## Resolve the source boundary

Accept any combination of:

- one or more explicitly named files.
- one or more documentation folders.
- the current repository.
- a repository plus explicitly named technical documents.

Treat explicitly named files as higher-priority sources. For a folder, first inventory files. Read technical documents and relevant repository guidance. Exclude generated output, dependencies, caches, credentials, private keys, and unrelated binary files.

Use available document tools to extract supported document formats. Preserve the source location, document title, and applicable version or date. Do not claim that unreadable or unavailable content supports a finding.

Read repository instructions, existing project guides, specifications, architecture decisions, and build or test definitions before proposing a guide. Inspect source code only as needed to distinguish the current implementation from the target design.

## Select the agent guide

Determine the invoking runtime from the active agent context.

| Invoking runtime | Target guide |
| --- | --- |
| Codex | `AGENTS.md` |
| Claude Code | `CLAUDE.md` |

If the target guide already exists, assess and revise that guide after authorization. If it does not exist, create it during `bootstrap`.

Do not create the other runtime's guide unless the user explicitly requests support for both agents. When the user requests both, create or revise both guides as peers. Keep their shared project rules equivalent. Keep only necessary runtime-specific discovery instructions different.

Treat `specs/` as agent-neutral. Do not designate either agent guide as the authoritative source for the other.

## Build the assessment

Create an evidence ledger before proposing documents. Classify each item as one of:

- confirmed fact.
- approved decision.
- assumption.
- unresolved question.
- conflict.
- external dependency.
- unsupported claim.

For each material item, record the source location. Do not resolve a conflict by selecting one interpretation without approval.

Report these assessment results:

1. Mission, problem statement, outcomes, and scope boundaries.
2. Functional requirements and nonfunctional requirements.
3. Current implementation, target design, and confirmed technology decisions.
4. External contracts, data dependencies, owners, and approval gates.
5. Risks, conflicts, assumptions, and missing information.
6. A milestone roadmap with one measurable exit criterion for each milestone.
7. A proposed project guide and `specs/` file manifest.

Keep detailed future implementation plans limited to the current or next approved milestone. Do not create false precision by planning every future implementation task in detail.

## Create project-wide specifications

Use [references/output-model.md](references/output-model.md) to select and structure output files.

Create only files that the evidence supports. At minimum, create these files when the source supports them:

- `specs/mission.md`
- `specs/tech-stack.md`
- `specs/roadmap.md`

Create conditional specifications only when they apply. Examples include input-data contracts, programme timelines, service-level objectives, architecture decisions, risk records, and regulatory constraints.

Use these rules:

- Separate current state, target state, and planned work.
- Mark unverified claims as assumptions or open decisions.
- Link each milestone to its source requirements and exit criterion.
- State external dependencies and approval gates explicitly.
- Preserve exact contractual, regulatory, legal, source-code, command, and identifier text when required.

## Create the agent guide

Keep the target agent guide short and operational. Include only information that an agent needs before changing the project:

- project purpose and scope.
- required reading in `specs/`.
- repository layout.
- verified development, test, and validation commands.
- implementation constraints and conventions.
- evidence-backed current phase.
- concise behavioral rules for assumptions, scope control, and verification.

Do not invent commands, completion status, dependencies, performance claims, or a current phase. Point to specifications instead of duplicating detailed requirements.

## Create milestone records

Use a dated directory named `specs/YYYY-MM-DD-milestone-name/` unless the repository uses an established alternative.

Create these records:

- `requirements.md` describes the goal, scope, constraints, decisions, and one exit criterion.
- `plan.md` lists the approved implementation work and its status.
- `validation.md` records commands, checks, results, incomplete checks, defects, and merge readiness.

Mark a validation check as passed only when execution evidence exists. Record unavailable environments, unrun checks, and blockers as incomplete. Do not copy planned checks into completed status.

## Validate the result

Before handing off generated or revised files:

1. Verify every cross-reference and file path.
2. Compare every claim with its supporting source.
3. Verify that the agent guide and `specs/` agree about scope, current state, and milestones.
4. Verify that each milestone has one measurable exit criterion.
5. Verify that validation records distinguish passed, failed, and unrun checks.
6. Apply repository documentation policies and templates when they exist.
7. Preserve unrelated repository changes.

Report the source inventory, files changed, unresolved items, and checks run.
