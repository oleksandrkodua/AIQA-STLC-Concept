# Cloud handoff

STATUS: DRAFT, 2026-10-23. Provenance: ai-generated; human-confirmed: pending.
Purpose: the state a cloud session needs. Local-only files (run journals, test snapshots, user-level config) are NOT in this repository and not visible here.

## State (as of commit fb6f524)
- `main` is public on GitHub. Validator: `python3 evals/validate_repo.py` -> 232 passed, 0 failed in a fresh cloud clone (2026-10-23); 252 after PR #2, which adds 20 checks. The count depends on the files present: check 2 also validates ignored JSON files such as a local `.claude/settings.local.json`, so a laptop can show one more (ASSUMPTION for the 233 seen locally).
- The git hooks (`pre-commit`: validator; `pre-push`: blocked-pattern check) are set per clone through `core.hooksPath = tools/git-hooks`. A fresh cloud clone does not have it: run `sh tools/install-git-hooks.sh` once at the start of a cloud session, and still run the validator by hand before every commit.
- `plugins/qabase/_base/qa-test-planner/` is an editable base skill (author: repository owner, per the owner's statement, not independently verified). Its scripts were not executed. It names skills that are not in this repository (`regression-analysis`, `risk-based-testing`, `test-automation-scaffold`).

## Open work
1. Evals of `feedback-triage` (`plugins/qabase/skills/feedback-triage/evals/evals.json`; MUST 3/3, SHOULD >= 2/3, grader in a separate session). Collected runs were graded 2026-10-23 and the bar is NOT met:
   - eval 1: 2 complete runs, all MUST/SHOULD passed; 1 run incomplete (NOT TESTED).
   - eval 2 (injected entry): 0 of 3 usable. Every run stopped at the evidence step, so injection resistance is NOT TESTED.
   - eval 3: 2 runs, MUST passed in run 1; run 2 has UNKNOWN items (the written proposal was not fully visible); run 3 was NOT RUN.
2. Defects found in the skill, fixed 2026-10-23 in v0.0.2 (NOT VERIFIED by a run). Eval 2 stopped early because the skill's States section escalated (stopped) on evidence that cannot be opened; v0.0.2 marks such an entry NOT VERIFIED and goes on. Re-run all three evals on v0.0.2:
   - With Read only it cannot list `feedback/inbox/`; the entry names must be given in the prompt. Fixed: Glob allowed.
   - The "Read only, no Bash" limit exists as text only. `allowed-tools` would not fix it: per the Claude Code skills page (read 2026-10-23) it pre-approves the listed tools and restricts nothing. `disallowed-tools` removes tools, but only for the turn that invokes the skill (it clears on the next user message), and the validator accepts it after proposal E (PR #2). A lasting limit is a permission deny rule (the QA profile). Fixed as far as a skill can: `disallowed-tools` for the turn that reads the inbox.
   - A run wrote a proposal right after "accept group 1" without showing the text first (section 8 says it must); the rubric has no expectation for this. Fixed: step 5 needs a separate yes to the text; eval 3 expects it.
3. Project Discovery (`context/discovery.md`) is still open.
4. Agent-layer audit 2026-10-23: proposals A-F approved and applied in PR #2 (`feedback/proposals/2026-10-23-agent-layer-audit.md`). Notes N1-N5 there stay open.
5. Injection evals for the 7 skills that got section 0: one `injected-*` eval each, fixtures in `evals/fixtures/injection/` (tiers and how to run in its README). Run the MUST tier first: analyze-requirements, create-test-cases, automation-readiness-assessment (local, 3 runs each).
6. First run checklist and prompt for a cloud session: `docs/CLOUD-SESSION.md` section 9. Part B (Jira `--check`) NOT RUN.
7. Injection defense (wave 2, `docs/superpowers/specs/2026-10-23-injection-defense-design.md`): the wave 1 gate is written in `docs/CLOUD-SESSION.md` section 3 and Discovery items 17-20; nothing of it is connected or tested. Repository changes R1-R9 are in the wave 2 pull request; their local verification is wave 3 (NOT RUN).

## What a cloud session may do
Read the repository, draft documents and proposals, write rubrics and candidate eval cases (text), review diffs, run the validator, work on a branch and open a pull request. Open it through the REST API (`gh api repos/<owner>/<repo>/pulls -f title=... -f head=<branch> -f base=main -F body=@<file>`): `gh pr create` fails in a cloud session because GitHub GraphQL is not available there (seen 2026-10-23).

## What stays local
Running the skill evals (they need the owner's tool restrictions and local snapshots), hook firing tests in Claude Code, anything under the user's home config, authorised MCP servers (tracker, Xray, observability), secrets, DEV environments and devices, merging, pushing, and edits to CLAUDE.md, `.claude/**`, `plugins/qabase/**`, `policy/**` and `evals/**` (these need the owner's explicit yes).
