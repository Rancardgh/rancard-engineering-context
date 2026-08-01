# Rancard Engineering Context

This repository centralizes reusable knowledge and shared agent instructions for Codex and Claude Code.

## Contents

- `AGENTS.md`: Codex entrypoint and canonical repository instructions shared by both agents.
- `CLAUDE.md`: Claude Code entrypoint that imports the same canonical repository instructions.
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
| [`zoom-out`](skills/zoom-out/SKILL.md) | Moves up a level of abstraction to map the relevant modules and callers. | [C4 abstraction levels](https://c4model.com/abstractions) |

### Code quality

| Skill | What it does | Learn more |
| --- | --- | --- |
| [`apply-domain-driven-design`](skills/apply-domain-driven-design/SKILL.md) | Models business rules, terminology, ownership, and state transitions in the code. | [Domain-driven design](https://martinfowler.com/bliki/DomainDrivenDesign.html) |
| [`improve-codebase-architecture`](skills/improve-codebase-architecture/SKILL.md) | Finds opportunities to create deeper modules with simpler interfaces and better locality. | [A Philosophy of Software Design](https://web.stanford.edu/~ouster/cgi-bin/book.php) |
| [`reliable-messaging`](skills/reliable-messaging/SKILL.md) | Designs asynchronous flows for durable intent, safe retries, idempotency, and recovery. | [Transactional outbox pattern](https://docs.aws.amazon.com/prescriptive-guidance/latest/cloud-design-patterns/transactional-outbox.html) |
| [`solid-codebase-review`](skills/solid-codebase-review/SKILL.md) | Audits a codebase against the five SOLID design principles before approved remediation. | [SOLID principles](https://en.wikipedia.org/wiki/SOLID) |

### Code security

No code security skill is currently bundled in this repository. The following vendor-maintained plugins are available as options:

| Platform | Plugin | What it does |
| --- | --- | --- |
| Codex | [Codex Security](https://learn.chatgpt.com/docs/security/plugin) | Scans authorized code for vulnerabilities and validates plausible findings before reporting them. |
| Claude Code | [Claude Security](https://github.com/anthropics/claude-plugins-official/tree/main/plugins/claude-security) | Runs deep vulnerability scans, challenges findings, and can verify targeted patches before they are applied. |
| Claude Code | [Security Guidance](https://github.com/anthropics/claude-plugins-official/tree/main/plugins/security-guidance) | Adds continuous pattern warnings and reviews diffs and commits for common vulnerability classes. |
