# Rancard Engineering Context — Codex Guide

This is the canonical repository guide. Claude Code loads the same instructions through `CLAUDE.md`.

## Entry Points

1. Use these shared instructions as the starting point in Codex or Claude Code.
2. Use `README.md` to understand the repository layout.
3. Use `indexes/skills-index.json` to find copied local skills.
4. Use `policies/asd-ste100.md` for all English technical documents.
5. Use `policies/coding-standards.md` when coding standards are relevant.
6. Use `templates/task-template.md` when a task needs the existing task format.

## Skills

Skills copied into `skills/` are canonical in this repository.

Apply `skills/apply-domain-driven-design/SKILL.md` automatically when you write or refactor application code that implements business rules, workflows, policies, state transitions, or domain validation.

Apply this skill even when the user does not mention DDD. Skip it for purely technical configuration, dependency, formatting, generated-code, or infrastructure-only changes.

Apply `skills/write-asd-ste100/SKILL.md` automatically when you create, edit, or review an English technical document. This rule applies even when the user does not mention ASD-STE100. Follow `policies/asd-ste100.md` for scope, exceptions, and review status.

## Editing

Keep changes grounded in files already present in this repository or in explicitly supplied new source material.
