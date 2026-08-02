# Contributing

Thank you for helping to improve the Rancard engineering context.

This repository contains shared instructions, policies, prompts, skills, and templates. Keep each change small, clear, and consistent with the existing resources.

## Before you start

1. Read [`AGENTS.md`](AGENTS.md) for the repository instructions.
2. Read [`README.md`](README.md) to understand the repository structure.
3. Read the policy or template that applies to your change.
4. Check the existing files for the approved terms and structure.

For an English technical document, apply the [`write-asd-ste100`](skills/write-asd-ste100/SKILL.md) skill. Follow the [ASD-STE100 policy](policies/asd-ste100.md).

For application code, follow the [coding standards](policies/coding-standards.md) when they apply.

## Prepare your change

1. Start from the latest `main` branch.
2. Create a focused branch with a short name, such as `feature/add-review-skill`.
3. Change only the files that are necessary for the contribution.
4. Preserve exact commands, identifiers, paths, and source text when fidelity is necessary.

### Change a skill

The [`skills/`](skills/) directory is the canonical source for repository skills.

When you add, remove, or rename a skill, update these catalogues:

- The **Skills Available** section in [`README.md`](README.md#skill-scope).
- The list in [`skills/README.md`](skills/README.md).
- The machine-readable index in [`indexes/skills-index.json`](indexes/skills-index.json).

Keep the complete skill directory in `skills/<skill-name>/`. Keep its name, path, and description consistent in each catalogue.

### Change agent instructions

Use [`AGENTS.md`](AGENTS.md) as the canonical repository guide. Keep [`CLAUDE.md`](CLAUDE.md) as the Claude Code entry point.

Put agent-specific compatibility instructions in [`agent-contracts/`](agent-contracts/). Do not duplicate shared instructions in an agent-specific file.

### Change a technical document

Use the existing structure when it is useful. If no structure applies, start with [`templates/technical-document-template.md`](templates/technical-document-template.md).

Keep the document in `draft` status while an unresolved item can change its meaning. Do not claim `ste-verified` status without the required qualified review.

## Validate your change

Run the checks that apply to the files that you changed.

Check a changed technical document:

```sh
python3 skills/write-asd-ste100/scripts/check_ste.py --mode procedural path/to/document.md
```

Use `--mode descriptive` for descriptive text. The pull request workflow checks changed text documents automatically.

Validate the skills index after a catalogue change:

```sh
jq empty indexes/skills-index.json
```

Check all changes for whitespace errors:

```sh
git diff --check
```

Review the final diff. Confirm that the catalogues, links, paths, and instructions agree.

## Commit your change

Make small, focused commits. Use a [Conventional Commits](https://www.conventionalcommits.org/) subject, such as:

```text
docs: add contribution guide
feat: add architecture review skill
fix: correct skill catalogue path
```

Use the most specific prefix for the change. See the [commit discipline](policies/coding-standards.md#commit-discipline) for the repository prefixes.

## Open a pull request

In the pull request description, include:

- The purpose of the change.
- The main files or resources that changed.
- The validation commands and results.
- Each unresolved decision or known exception.

Keep the pull request focused on one contribution. Resolve failed checks before you request final review.
