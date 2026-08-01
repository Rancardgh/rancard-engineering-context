# Install Rancard Engineering Skills

Install reusable engineering skills from `https://github.com/Rancardgh/rancard-engineering-context.git` into the current user's global skill directory.

## Inputs

- Source ref: `main`
- Skills: `all`
- Target agents: `current`

Override these inputs when needed. `Skills` can be `all` or a comma-separated list of names from `indexes/skills-index.json`. `Target agents` can be `current`, `claude`, `codex`, or `both`.

## Installation Rules

1. This is a user-level installation. Do not add skill files or agent configuration to the repository currently being worked on.
2. Obtain the source repository at the requested ref. Reuse a verified local checkout when one is available; otherwise, clone it into a temporary directory using existing Git credentials. Do not expose credentials or leave the temporary clone behind.
3. Read the source repository's host guide before installing anything: use `AGENTS.md` in Codex or `CLAUDE.md` in Claude Code. Both load the same canonical repository instructions. Then read `README.md` and `indexes/skills-index.json`.
4. Resolve `Skills: all` exclusively from `indexes/skills-index.json`. Install only names present in that index; do not infer or include excluded skills.
5. Resolve `Target agents: current` from the host that is executing this prompt:
   - Claude Code installs user skills under the current user's `~/.claude/skills/<skill-name>/` directory.
   - Codex installs user skills under the current user's `~/.agents/skills/<skill-name>/` directory.
   - If the host cannot be identified reliably, stop and ask which target to use.
6. For `claude`, `codex`, or `both`, use the corresponding destinations above regardless of the current host.
7. Resolve each destination to an absolute path before writing. Do not use an unresolved home-directory variable as a copy, overwrite, or deletion target.
8. Copy each selected skill's complete directory from the canonical source `skills/<skill-name>/`. Preserve `SKILL.md` and every supporting file, subdirectory, executable bit, and symbolic link. Never install only `SKILL.md` when the skill has additional resources.
9. Handle each destination safely:
   - If it does not exist, install the skill.
   - If it is byte-for-byte identical to the source, leave it unchanged and report it as already installed.
   - If it exists and differs, do not overwrite, merge, or delete it. Report the conflict with the relevant paths and wait for explicit direction.
10. Do not modify the source repository. Do not create links from a global skill directory to a temporary clone.

## Verification

After installation:

1. Confirm every installed skill directory contains a readable `SKILL.md` with `name` and `description` frontmatter.
2. Compare every installed directory recursively with its canonical source directory.
3. Report:
   - source repository and resolved commit;
   - resolved global destination directories;
   - installed skills;
   - already-identical skills;
   - conflicts or failures;
   - confirmation that the current working repository was not modified.
4. If the host does not detect newly installed skills immediately, tell the user to restart that agent.
