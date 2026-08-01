# Agent Instructions

Use this repository as the central source of reusable knowledge and agent instructions.

## Entry Points

1. Read this file first.
2. Use `README.md` to understand the repository layout.
3. Use `indexes/skills-index.json` to find copied local skills.
4. Use `policies/coding-standards.md` when coding standards are relevant.
5. Use `templates/task-template.md` when a task needs the existing task format.

## Skills

Skills copied into `skills/` are canonical in this repository.

Apply `skills/apply-domain-driven-design/SKILL.md` automatically whenever writing or refactoring application code that implements business rules, workflows, policies, state transitions, or domain validation, even when the user does not mention DDD. Skip it for purely technical configuration, dependency, formatting, generated-code, or infrastructure-only changes.

Do not use the Flutter deployment skills from this repository; they are intentionally excluded.

## Editing

Keep changes grounded in files already present in this repository or in explicitly supplied new source material.
