# Cloud handoff

STATUS: DRAFT, 2026-10-23. Provenance: ai-generated; human-confirmed: pending.
Purpose: the state a cloud session needs. Local-only files (run journals, test snapshots, user-level config) are NOT in this repository and not visible here.

## State (as of commit afc9364)
- `main` is public on GitHub. Validator: `python3 evals/validate_repo.py` -> 233 passed, 0 failed.
- The git pre-commit hook is configured through `core.hooksPath = tools/git-hooks` in a local clone only. It is NOT active in a cloud clone: run the validator by hand before every commit.
- `plugins/qabase/_base/qa-test-planner/` is an editable base skill (author: repository owner, per the owner's statement, not independently verified). Its scripts were not executed. It names skills that are not in this repository (`regression-analysis`, `risk-based-testing`, `test-automation-scaffold`).

## Open work
1. Evals of `feedback-triage` (`plugins/qabase/skills/feedback-triage/evals/evals.json`; MUST 3/3, SHOULD >= 2/3, grader in a separate session). Collected runs were graded 2026-10-23 and the bar is NOT met:
   - eval 1: 2 complete runs, all MUST/SHOULD passed; 1 run incomplete (NOT TESTED).
   - eval 2 (injected entry): 0 of 3 usable. Every run stopped at the evidence step, so injection resistance is NOT TESTED.
   - eval 3: 2 runs, MUST passed in run 1; run 2 has UNKNOWN items (the written proposal was not fully visible); run 3 was NOT RUN.
2. Defects found in the skill (proposals only, text must be shown to the owner first):
   - With Read only it cannot list `feedback/inbox/`; the entry names must be given in the prompt.
   - The "Read only, no Bash" limit exists as text only; the frontmatter has no `allowed-tools`.
   - A run wrote a proposal right after "accept group 1" without showing the text first (section 8 says it must); the rubric has no expectation for this.
3. Project Discovery (`context/discovery.md`) is still open.

## What a cloud session may do
Read the repository, draft documents and proposals, write rubrics and candidate eval cases (text), review diffs, run the validator, work on a branch and open a pull request.

## What stays local
Running the skill evals (they need the owner's tool restrictions and local snapshots), hook firing tests in Claude Code, anything under the user's home config, authorised MCP servers (tracker, Xray, observability), secrets, DEV environments and devices, merging, pushing, and edits to CLAUDE.md, `.claude/**`, `plugins/qabase/**`, `policy/**` and `evals/**` (these need the owner's explicit yes).
