# How to Use This Repo

This repository provides shared engineering instructions and resources for Codex and Claude Code.

Use the repository to:

- Apply shared agent instructions.
- Find and install engineering skills.
- Use shared policies and coding standards.
- Start work from a reusable prompt or template.

## Use the agent instructions

Codex uses [`AGENTS.md`](../AGENTS.md) as the canonical repository guide.

Claude Code uses [`CLAUDE.md`](../CLAUDE.md). This file loads the canonical guide and the Claude Code discovery instructions.

Read [`README.md`](../README.md) to see the repository layout and the available skills.

## Find a skill

Use the **Skills Available** section in [`README.md`](../README.md#skill-scope) to review skills by purpose.

Use [`indexes/skills-index.json`](../indexes/skills-index.json) when an agent or tool needs a machine-readable skill list.

Each entry links to a canonical `SKILL.md` file in the [`skills/`](../skills/) directory.

## Install the skills

Use the installation prompt to install skills for Codex, Claude Code, or both agents.

The installation is at user level. It does not add skill files to your current project.

### Run the installation prompt

1. Open [`prompts/install-engineering-skills.md`](../prompts/install-engineering-skills.md).
2. Copy all the prompt text.
3. Start a task in Codex or Claude Code.
4. Paste the prompt into the task.
5. Change the input values if the defaults are not correct.
6. Submit the prompt.
7. Review the installation report.

The default input values install all indexed skills for the agent that runs the prompt:

```text
Source ref: main
Skills: all
Target agents: current
```

To install selected skills, use a comma-separated list of names from [`indexes/skills-index.json`](../indexes/skills-index.json):

```text
Skills: apply-domain-driven-design,reliable-messaging
```

To install skills for a specified agent, set `Target agents` to one of these values:

| Value | Installation target |
| --- | --- |
| `current` | The agent that runs the prompt |
| `codex` | Codex only |
| `claude` | Claude Code only |
| `both` | Codex and Claude Code |

### Installation locations

The prompt installs complete skill directories in these locations:

- Codex: `~/.agents/skills/<skill-name>/`
- Claude Code: `~/.claude/skills/<skill-name>/`

The installer leaves an identical installed skill unchanged. If an installed skill is different, the installer reports a conflict and does not overwrite the skill.

### Confirm the result

The installation report identifies the source commit and each destination. It also lists installed skills, identical skills, conflicts, and failures.

If the agent does not show a new skill, restart the agent.

## Use the other resources

Use these directories when the task does not require a skill installation:

| Directory | Purpose |
| --- | --- |
| [`agent-contracts/`](../agent-contracts/) | Agent-specific compatibility and extension instructions |
| [`policies/`](../policies/) | Shared engineering policies and standards |
| [`prompts/`](../prompts/) | Portable setup prompts and reusable workflows |
| [`templates/`](../templates/) | Reusable task and technical document structures |
