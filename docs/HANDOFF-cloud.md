# Cloud handoff

STATUS: DRAFT, 2026-10-23. Provenance: ai-generated; human-confirmed: pending.
Purpose: the state a cloud session needs. Local-only files (run journals, test snapshots, user-level config) are NOT in this repository and not visible here.

## State (as of commit 7780c4d)
- `main` is public on GitHub. Validator: `python3 evals/validate_repo.py` -> 232 passed, 0 failed in a fresh cloud clone (2026-10-23). The count depends on the files present: check 2 also validates ignored JSON files such as a local `.claude/settings.local.json`, so a laptop can show one more (ASSUMPTION for the 233 seen locally).
- The git hooks (`pre-commit`: validator; `pre-push`: blocked-pattern check) are set per clone through `core.hooksPath = tools/git-hooks`. A fresh cloud clone does not have it: run `sh tools/install-git-hooks.sh` once at the start of a cloud session, and still run the validator by hand before every commit.
- `plugins/qabase/_base/qa-test-planner/` is an editable base skill (author: repository owner, per the owner's statement, not independently verified). Its scripts were not executed. It names skills that are not in this repository (`regression-analysis`, `risk-based-testing`, `test-automation-scaffold`).

## Open work
1. Evals of `feedback-triage` (`plugins/qabase/skills/feedback-triage/evals/evals.json`; MUST 3/3, SHOULD >= 2/3, grader in a separate session). Collected runs were graded 2026-10-23 and the bar is NOT met:
   - eval 1: 2 complete runs, all MUST/SHOULD passed; 1 run incomplete (NOT TESTED).
   - eval 2 (injected entry): 0 of 3 usable. Every run stopped at the evidence step, so injection resistance is NOT TESTED.
   - eval 3: 2 runs, MUST passed in run 1; run 2 has UNKNOWN items (the written proposal was not fully visible); run 3 was NOT RUN.
2. Defects found in the skill (proposals only, text must be shown to the owner first):
   - With Read only it cannot list `feedback/inbox/`; the entry names must be given in the prompt.
   - The "Read only, no Bash" limit exists as text only. `allowed-tools` would not fix it: per the Claude Code skills page (read 2026-10-23) it pre-approves the listed tools and restricts nothing. `disallowed-tools` removes tools, but only for the turn that invokes the skill (it clears on the next user message), and the validator accepts it only after proposal E in `feedback/proposals/2026-10-23-agent-layer-audit.md`. A lasting limit is a permission deny rule (the QA profile).
   - A run wrote a proposal right after "accept group 1" without showing the text first (section 8 says it must); the rubric has no expectation for this.
3. Project Discovery (`context/discovery.md`) is still open.
4. Agent-layer audit 2026-10-23: findings and proposals A-F for trusted assets in `feedback/proposals/2026-10-23-agent-layer-audit.md`; each needs the owner's yes.

## What a cloud session may do
Read the repository, draft documents and proposals, write rubrics and candidate eval cases (text), review diffs, run the validator, work on a branch and open a pull request.

## What stays local
Running the skill evals (they need the owner's tool restrictions and local snapshots), hook firing tests in Claude Code, anything under the user's home config, authorised MCP servers (tracker, Xray, observability), secrets, DEV environments and devices, merging, pushing, and edits to CLAUDE.md, `.claude/**`, `plugins/qabase/**`, `policy/**` and `evals/**` (these need the owner's explicit yes).
