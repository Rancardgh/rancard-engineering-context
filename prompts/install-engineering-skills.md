# Install Rancard Engineering Skills

Install reusable engineering skills from `https://github.com/Rancardgh/rancard-engineering-context.git` into the Git repository you are currently working on.

## Inputs

- Source ref: `main`
- Skills: `all`
- Target agents: `current`

Override these inputs when needed. `Skills` can be `all` or a comma-separated list of names from `indexes/skills-index.json`. `Target agents` can be `current`, `claude`, `codex`, or `both`.

## Installation Rules

1. Treat the current Git repository as the target. Resolve its root before making changes and follow its local agent instructions.
2. Inspect the target working tree before editing. Preserve unrelated changes and do not stage, commit, push, or open a pull request unless the user explicitly asks.
3. Obtain the source repository at the requested ref. Reuse a verified local checkout when one is available; otherwise, clone it into a temporary directory using existing Git credentials. Do not expose credentials or leave the temporary clone behind.
4. Read the source repository's `AGENTS.md`, `README.md`, and `indexes/skills-index.json` before installing anything.
5. Resolve `Skills: all` exclusively from `indexes/skills-index.json`. Install only names present in that index; do not infer or include excluded skills.
6. Resolve `Target agents: current` from the host that is executing this prompt:
   - Claude Code installs project skills under `<target-repository>/.claude/skills/<skill-name>/`.
   - Codex installs project skills under `<target-repository>/.agents/skills/<skill-name>/`.
   - If the host cannot be identified reliably, stop and ask which target to use.
7. For `claude`, `codex`, or `both`, use the corresponding destinations above regardless of the current host.
8. Copy each selected skill's complete directory from the canonical source `skills/<skill-name>/`. Preserve `SKILL.md` and every supporting file, subdirectory, executable bit, and symbolic link. Never install only `SKILL.md` when the skill has additional resources.
9. Handle each destination safely:
   - If it does not exist, install the skill.
   - If it is byte-for-byte identical to the source, leave it unchanged and report it as already installed.
   - If it exists and differs, do not overwrite, merge, or delete it. Report the conflict with the relevant paths and wait for explicit direction.
10. Do not modify the source repository. Do not create links from the target repository to a temporary clone.

## Verification

After installation:

1. Confirm every installed skill directory contains a readable `SKILL.md` with `name` and `description` frontmatter.
2. Compare every installed directory recursively with its canonical source directory.
3. Report:
   - source repository and resolved commit;
   - target repository;
   - target agent destinations;
   - installed skills;
   - already-identical skills;
   - conflicts or failures;
   - final target Git status.
4. If the host does not detect newly installed skills immediately, tell the user to restart that agent in the target repository.
