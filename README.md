# Rancard Engineering Context

This repository centralizes reusable knowledge and shared agent instructions for Codex and Claude Code.

## Contents

- `AGENTS.md`: Codex guide.
- `CLAUDE.md`: Claude Code guide.
- `.claude/`: Claude Code discovery configuration for canonical repository skills.
- `agent-contracts/`: agent-specific compatibility and extension instructions for Codex and Claude Code.
- `indexes/`: machine-readable catalogues of repository resources.
- `policies/`: shared policies and standards for engineering work.
- `prompts/`: portable prompts for cross-agent setup and reusable workflows.
- `skills/`: canonical reusable skills available to Codex and Claude Code.
- `templates/`: reusable starting points for common engineering tasks and documents.

## Skill Scope

Skills Available:

The skill names link to their canonical instructions. The external links explain the practices behind each skill.

Attribution: `grill-with-docs`, `improve-codebase-architecture`, `to-issues`, and `zoom-out` were adopted and adapted from [Matt Pocock's skills collection](https://github.com/mattpocock/skills/tree/main).

### Technical documentation

| Skill | What it does | Learn more |
| --- | --- | --- |
| [`grill-with-docs`](skills/grill-with-docs/SKILL.md) | Challenges a plan, settles domain vocabulary, and records hard-to-reverse decisions. | [Domain-driven design](https://martinfowler.com/bliki/DomainDrivenDesign.html) and [architecture decision records](https://adr.github.io/) |
| [`human-editor`](skills/human-editor/SKILL.md) | Improves clarity, flow, audience fit, and voice without changing the author's meaning. | [Self-editing technical writing](https://developers.google.com/tech-writing/two/editing) |
| [`pdf`](skills/pdf/SKILL.md) | Reads, creates, and visually verifies PDFs so layout and rendering are preserved. | [About the Portable Document Format](https://www.adobe.com/acrobat/about-adobe-pdf.html) |
| [`to-issues`](skills/to-issues/SKILL.md) | Turns a plan, specification, or product requirements document into independently deliverable tracer-bullet issues. | [Incremental and tracer-bullet development](https://resources.sei.cmu.edu/asset_files/TechnicalReport/2015_005_001_439065.pdf) |
| [`write-asd-ste100`](skills/write-asd-ste100/SKILL.md) | Writes and reviews English technical documents with ASD-STE100 Simplified Technical English. | [ASD-STE100 Issue 9](https://www.asd-ste100.org/assets/files/ASD-STE100_ISSUE9.pdf) |
| [`zoom-out`](skills/zoom-out/SKILL.md) | Moves up a level of abstraction to map the relevant modules and callers. | [C4 abstraction levels](https://c4model.com/abstractions) |

### Code quality

| Skill | What it does | Learn more |
| --- | --- | --- |
| [`apply-domain-driven-design`](skills/apply-domain-driven-design/SKILL.md) | Models business rules, terminology, ownership, and state transitions in the code. | [Domain-driven design](https://martinfowler.com/bliki/DomainDrivenDesign.html) |
| [`improve-codebase-architecture`](skills/improve-codebase-architecture/SKILL.md) | Finds opportunities to create deeper modules with simpler interfaces and better locality. | [A Philosophy of Software Design](https://web.stanford.edu/~ouster/cgi-bin/book.php) |
| [`reliable-messaging`](skills/reliable-messaging/SKILL.md) | Designs asynchronous flows for durable intent, safe retries, idempotency, and recovery. | [Transactional outbox pattern](https://docs.aws.amazon.com/prescriptive-guidance/latest/cloud-design-patterns/transactional-outbox.html) |
| [`solid-codebase-review`](skills/solid-codebase-review/SKILL.md) | Audits a codebase against the five SOLID design principles before approved remediation. | [SOLID principles](https://en.wikipedia.org/wiki/SOLID) |

### Code security

| Platform | Plugin | What it does |
| --- | --- | --- |
| Codex | [Codex Security](https://learn.chatgpt.com/docs/security/plugin) | Scans authorized code for vulnerabilities and validates plausible findings before reporting them. |
| Claude Code | [Claude Security](https://github.com/anthropics/claude-plugins-official/tree/main/plugins/claude-security) | Runs deep vulnerability scans, challenges findings, and can verify targeted patches before they are applied. |
| Claude Code | [Security Guidance](https://github.com/anthropics/claude-plugins-official/tree/main/plugins/security-guidance) | Adds continuous pattern warnings and reviews diffs and commits for common vulnerability classes. |

## Documentation Standard

Agents must apply `write-asd-ste100` to all English technical documents. The root `AGENTS.md` makes this skill automatic in this repository.

Target repositories must copy the same instruction into their `AGENTS.md` file. Team members must install or copy the canonical skill folder into their agent's skill directory.
