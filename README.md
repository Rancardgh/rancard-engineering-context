# Rancard Engineering Context

This repository centralizes reusable knowledge and agent instructions.

## Contents

- `AGENTS.md`: repo-level instructions for coding agents.
- `CLAUDE.md`: Claude Code entrypoint that imports the canonical repo instructions.
- `.claude/skills/`: Claude Code discovery link to the canonical `skills/` directory.
- `agent-contracts/claude/CLAUDE.md`: Claude-specific instructions.
- `agent-contracts/codex/AGENTS.md`: Codex-specific entrypoint.
- `indexes/skills-index.json`: machine-readable index of copied local skills.
- `policies/asd-ste100.md`: required language policy for English technical documents.
- `policies/coding-standards.md`: coding standards already present in this repo.
- `prompts/install-engineering-skills.md`: portable prompt for installing canonical skills globally for Claude Code, Codex, or both.
- `skills/`: copied installed skills, excluding Flutter deployment skills.
- `templates/technical-document-template.md`: optional template for new technical documents.
- `templates/task-template.md`: task template already present in this repo.

## Skill Scope

Skills Available:

- `apply-domain-driven-design`
- `grill-with-docs`
- `human-editor`
- `improve-codebase-architecture`
- `pdf`
- `reliable-messaging`
- `solid-codebase-review`
- `to-issues`
- `write-asd-ste100`
- `zoom-out`

## Documentation Standard

Agents must apply `write-asd-ste100` to all English technical documents. The root `AGENTS.md` makes this skill automatic in this repository.

Target repositories must copy the same instruction into their `AGENTS.md` file. Team members must install or copy the canonical skill folder into the skill directory of their agent.
