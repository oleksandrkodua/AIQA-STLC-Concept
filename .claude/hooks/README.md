# Hooks

STATUS: DRAFT. Nothing here is active. `.claude/settings.draft.json` is not read by Claude
Code. Activating = renaming it to `settings.json` after QA Lead approval AND after the
firing checks below are run. A hook is counted as a control only after the firing checks pass.

## Maturity

All hooks are EXPERIMENTAL: scripts exist and their logic is tested; whether Claude Code fires
them, with which payload, on managed employer or client machines is not verified.

## Hook table

| Hook | Event / matcher | Purpose | Floor underneath | Logic test | Firing test |
|---|---|---|---|---|---|
| `deny_prod_and_secrets.py` | PreToolUse: Bash, Read, Edit, Write, MultiEdit, NotebookEdit, Glob, Grep, WebFetch | Deny secret files and production hosts | `permissions.deny` for `.env*`, keys, webhook files | PASS 11/11 (`evals/hooks/run_hook_tests.py`) | NOT RUN |
| `protect_trusted_assets.py` | PreToolUse: Edit, Write, MultiEdit, NotebookEdit, Bash | Ask before changing CLAUDE.md, `.claude/**`, `policy/**`, `evals/**`, `context/sources.md` | `permissions.ask` | PASS 7/7 | NOT RUN |
| `qa_gate.py` + `qa_run_check.py` | PostToolUse: Write, Edit | Nudge (exit 2) when a `*QA-RUN.md` journal breaks structure or caps | none (advisory) | PASS 9/9 + 2/2 | NOT RUN |
| mobile pre-run environment check | procedure, not a hook | Confirm the app points to the test environment before a mobile run | the run command refuses without an explicit flag (to build in `automation/mobile`) | NOT BUILT | NOT BUILT |
| type-check after edits | PostToolUse | `tsc --noEmit` in the edited project | CI | NOT BUILT | NOT BUILT |
| Stop verification | Stop | Do not close a task without a confirming tool call; block once | none | NOT BUILT | NOT BUILT |
| SessionStart / InstructionsLoaded | SessionStart | Show that CLAUDE.md and rules loaded | none | NOT BUILT | NOT BUILT |
| ConfigChange | ConfigChange | Detect changes to trusted configuration | none | NOT BUILT | NOT BUILT |
| SubagentStop | SubagentStop | Audit agent output when agents exist | n/a (no agents by default) | LATER | LATER |

The logic-test column counts only what `evals/hooks/` runs in a sandbox (re-run in this base on
2026-10-20: 20 and 9 cases passed). The counts are test cases, not coverage of real attacks.

## Design rules

1. Project scope (`.claude/settings.json`), not local or user scope.
2. Deterministic `command` hooks for prohibitions. No model-judged hook blocks anything.
3. Every blocking hook has a permission rule underneath, because hooks fail open and
   `@` file references bypass PreToolUse. The permission rule is the floor.
4. A hook that errors asks and logs to stderr; it never allows silently. A hook that cannot start is blocked (`onFailure: block`). Hooks run per machine (`.claude/settings.local.json`); cloud sessions have none.
5. Hook scripts and their lists (`prod-hosts.txt`) are trusted assets: changes need approval.

## Known gaps

- `prod-hosts.txt` is empty: production hostnames are UNKNOWN until Discovery (Discovery item 5). Prod
  protection by hook is therefore NOT active; only the rules in prose and the deny floor on
  secrets apply.
- `permissions.deny` for `./.env.*` also blocks `.env.example`. Accepted for now.
- The Bash checks are string heuristics. A script that reads a secret internally is not seen.
- Payload field names and the `permissionDecision` protocol follow what the author believes
  the current Claude Code expects. The permission-rule syntax in `settings.draft.json`
  (for example `Read(./.env.*)`, `Bash(rm -rf:*)`) is written from memory of the documentation
  and was not checked against the installed version. The firing test settles both.

## How to run the logic tests

```
python3 evals/hooks/run_hook_tests.py
python3 evals/hooks/run_runcheck_tests.py
```

## Firing test (to do on a machine with Claude Code, in a throwaway copy)

1. Activate the draft settings in the copy.
2. Ask Claude to read `.env` → expect a block. Ask it to edit `CLAUDE.md` → expect a prompt.
3. Record the exact transcript in `evals/runs/` and record PASS or FAIL in `decisions/verification-log.md`.
4. Write down in advance: PASS = both happen with the hook, not only the permission rule.
   Test the hook alone by temporarily removing the permission rule in the copy.
