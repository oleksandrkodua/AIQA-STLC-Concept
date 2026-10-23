# Optional: user-level mods

STATUS: placeholder. Mods are user-level Claude Code extensions, for example a warning before a command that deletes files. They are not part of this base and no mod code is copied here.

## Why they are not in the base
- They live on one person's machine, not in the project, and the project's rules and evals do not depend on them.
- Mods fail open and are not a security control (`.claude/rules/security-rules.md`, rule 11). The permission floor in `.claude/settings.json` and the git pre-commit check stay the real controls.
- A mod you wrote yourself may belong to you, not to an employer. Check ownership and the licence before adding it to a shared repository.

## How to add one
1. Keep the mod in your own repository and install it on your machine.
2. If the team wants it, copy its folder to `optional/mods/<name>/` with its own `README.md` (what it does, what it does not do, how to install) and a licence line.
3. Record in `decisions/DECISIONS.md` that the mod is an optional convenience, not a control.
4. A mod stays EXPERIMENTAL until its acceptance tests pass (`evals/hooks-acceptance.md` if the project keeps one).
