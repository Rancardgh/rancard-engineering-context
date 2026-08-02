# Output model

Use this reference after the assessment identifies the supported project context.

## Project-wide specifications

| File | Create when | Required contents |
| --- | --- | --- |
| `specs/mission.md` | The source identifies a project or product purpose. | Purpose, problem, objectives, principles, success measures, scope boundaries, stakeholders. |
| `specs/tech-stack.md` | The source identifies technologies or architecture choices. | Current and target architecture, component responsibilities, decisions, constraints, and open decisions. |
| `specs/roadmap.md` | The work has more than one delivery stage. | Milestones, dependencies, status, one exit criterion per milestone, and links to milestone records. |
| `specs/input-data-contract.md` | The system accepts external data, events, files, or API messages. | Sources, contracts, ownership, field or schema gaps, sample acceptance, and approval gates. |
| `specs/programme-timeline.md` | An external programme or delivery clock exists. | External timeline, internal milestone crosswalk, acceptance gates, and timing risks. |
| `specs/service-level-objectives.md` | Service, performance, reliability, or support targets exist. | Objective, measurement boundary, target, status, and unresolved measurement rules. |
| `specs/architecture-decisions.md` | Material architecture decisions need a compact record. | Decision, context, alternatives, consequence, evidence, and status. |
| `specs/risk-register.md` | Material delivery or operational risks exist. | Risk, consequence, likelihood, mitigation, owner, trigger, and status. |

Do not create a file merely because it appears in this table. Create it when evidence makes it useful.

## Agent guide structure

Use this order when the evidence supports each section:

1. Project purpose and scope.
2. Required `specs/` reading.
3. Verified development and validation commands.
4. Repository layout.
5. Architecture and implementation constraints.
6. Current phase and its source.
7. Rules for assumptions, scope control, and validation.

Keep detailed design material in `specs/`. Keep runtime-specific instructions limited to the applicable guide.

## Milestone record structure

### `requirements.md`

Include status, goal, in-scope work, out-of-scope work, decisions, constraints, source links, and one exit criterion.

### `plan.md`

List implementation tasks in execution order. Use unchecked items for approved but incomplete work. Do not add tasks that exceed the milestone scope.

### `validation.md`

State the exit criterion first. For each check, record its command or method, result, and evidence. Separate passed checks from failed, blocked, or unrun checks. State merge readiness only when the evidence supports it.
