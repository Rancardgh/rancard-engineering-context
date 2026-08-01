# Rancard Engineering Context

This repository centralizes reusable knowledge and agent instructions.

## Contents

- `AGENTS.md`: repo-level instructions for coding agents.
- `CLAUDE.md`: Claude Code entrypoint that imports the canonical repo instructions.
- `.claude/skills/`: Claude Code discovery link to the canonical `skills/` directory.
- `agent-contracts/claude/CLAUDE.md`: Claude-specific instructions.
- `agent-contracts/codex/AGENTS.md`: Codex-specific entrypoint.
- `indexes/skills-index.json`: machine-readable index of copied local skills.
- `policies/coding-standards.md`: coding standards already present in this repo.
- `prompts/install-engineering-skills.md`: portable prompt for installing canonical skills globally for Claude Code, Codex, or both.
- `skills/`: copied installed skills, excluding Flutter deployment skills.
- `templates/task-template.md`: task template already present in this repo.

## Skill Scope

Skills Available:

### Technical documentation

- `grill-with-docs`
- `human-editor`
- `pdf`
- `to-issues`
- `zoom-out`

### Code quality

- `apply-domain-driven-design`
- `improve-codebase-architecture`
- `reliable-messaging`
- `solid-codebase-review`

### Code security

No code security skills are currently included.
