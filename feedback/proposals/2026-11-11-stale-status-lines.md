# Proposal: bring stale status lines in line with the recorded results

STATUS: APPROVED 2026-11-11 by Oleksandr Kukhtinov (QA Lead), changes 1-5; APPLIED on branch `docs/stale-status-lines`. The items under "Not proposed here" stay open. Provenance: ai-generated (Claude Code, Fable 5.2, 2026-11-11), from a read-only audit of `main` 2c1da28; human-confirmed: pending.

## Why

Several status lines contradict newer records in the same repository. The value of this base is that a status can be trusted; a reader who meets two different statuses for one thing cannot tell which is current. No behaviour changes: every edit below is text about state, not an instruction to the model.

Evidence the new text rests on (all read 2026-11-11, none re-run):
- `decisions/verification-log.md` V-001 (PASS, MEDIUM) and V-002 (OPEN).
- `evals/runs/2026-10-28-skill-evals-ft2-inj-ar.md`, `evals/runs/2026-10-28-skill-evals-inj-ar-rerun.md`.
- `.claude/rules/security-rules.md` change history: "`.claude/settings.json` approved 2026-11-03 ... ACTIVE".
- `.claude/settings.json` `_note`: "No hooks here: hooks are per-machine".
- `README.md:58` and `:77`, `CLAUDE.md:69` and `:77` already carry the newer state.

## Changes (exact text)

### 1. `.claude/hooks/README.md` lines 3-5 (protected: `.claude/**`)

Old:
```
STATUS: DRAFT. Nothing here is active. `.claude/settings.draft.json` is not read by Claude
Code. Activating = renaming it to `settings.json` after QA Lead approval AND after the
firing checks below are run. A hook is counted as a control only after the firing checks pass.
```
New:
```
STATUS: DRAFT. No hook is active by default. `.claude/settings.json` (permission floor only,
no hooks) is ACTIVE, approved 2026-11-03. `.claude/settings.draft.json` is not read by Claude
Code. Hooks are installed per machine into `.claude/settings.local.json` from
`tools/hooks.template.json`, after QA Lead approval. A hook is counted as a control only
after the firing checks below pass.
```

### 2. `evals/README.md` line 3 (protected: `evals/**`)

Old:
```
STATUS: plan + first logic tests. Skills' evals: NOT RUN, except `feedback-triage` (partly run 2026-10-23, bar NOT met; see `docs/HANDOFF-cloud.md`). Hook firing: NOT RUN.
```
New:
```
STATUS: plan + first logic tests. Skills' evals: NOT RUN, except `feedback-triage` eval 2 (PASS 3/3, V-001) and `analyze-requirements` eval 6 (3/3 after PR #8, V-002 OPEN); records in `evals/runs/`, limits in `decisions/verification-log.md`. Hook firing: NOT RUN.
```

### 3. `evals/README.md` line 17, Status cell of layer 1 (protected)

Old:
```
written for 17 skills (all but `exploratory-testing-web` and `-mobile`); NOT RUN, except `feedback-triage` (partly run, bar NOT met)
```
New:
```
written for 17 skills (all but `exploratory-testing-web` and `-mobile`); NOT RUN, except `feedback-triage` eval 2 and `analyze-requirements` eval 6 (see line 3)
```

### 4. `plugins/qabase/skills/analyze-requirements/SKILL.md` line 8 (protected: `plugins/qabase/**`)

Old (two fragments of the STATUS line):
```
Evals written, NOT RUN.
```
```
Output template order changed 2026-10-28 (blocking questions before the criteria table); evals NOT RUN after the change.
```
New:
```
Evals written; eval 6 run, the other six NOT RUN.
```
```
Output template order changed 2026-10-28 (blocking questions before the criteria table); after the change only eval 6 was re-run (3/3, V-002 OPEN).
```
Basis: the re-run record, line 39, leaves this edit to the owner.

### 5. `docs/CONCEPT.md` lines 3, 42, 60, 62 (not on the protected list; still the owner's document)

- Line 3, old: `no skill has been evaluated in this repository (evals NOT RUN).` New: `two skill evals have a recorded run (V-001, V-002); the rest are NOT RUN.`
- Line 42, State cell, old: `pilot; evals NOT RUN`. New: `pilot; eval 6 run (V-002 OPEN), other evals NOT RUN`.
- Line 62, old: `- NOT RUN: skill evals, hook firing tests, any CI, any cloud session.` New: `- PARTLY RUN: skill evals (2 cases, see `decisions/verification-log.md`). NOT RUN: hook firing tests.` The parts "any CI, any cloud session" look outdated too (`.github/workflows/validate.yml` exists; `docs/HANDOFF-cloud.md` describes a cloud run): the owner words them.
- Line 60 quotes a validator count of 229 for 2026-10-23. It is dated, so it is not wrong; no change proposed.

## Not proposed here: the owner decides first

- `.claude/hooks/README.md` design rule 1 ("Project scope (`.claude/settings.json`), not local or user scope") and rule 4 ("Hooks run per machine (`.claude/settings.local.json`)") disagree with each other. Which one is intended is a decision, not a wording fix.
- Same file, firing test step 1 ("Activate the draft settings in the copy") and the known gap about permission syntax "written from memory" both describe the time before `settings.json` was active. The install procedure in `tools/apply-trusted-changes.sh` was not read for this proposal, so no replacement text is offered.
- `"status": "NOT RUN"` in the `evals.json` of `analyze-requirements` and `feedback-triage`. `tools/build-skills-index.py` and `evals/validate_repo.py` do not read this field (grep, 2026-11-11), but whether a vocabulary such as PARTLY RUN is wanted is the owner's call.
- `CLAUDE.md:23` says only that `settings.draft.json` is not active. True, and the file is at 99 of 100 lines; left alone.
- Hook logic-test counts (`evals/README.md` "20/20 and 9/9"; hooks README "11/11", "7/7", "9/9 + 2/2"): the scripts print 15 + 5 and 8 + 1 cases. How the README splits them was not reconciled, and the tests were not run.

## Side effects

- Change 4 touches a skill source: run `tools/sync-skills.sh` so `.claude/skills/` matches, and rebuild `plugins/qabase/skills-index.json` if the validator reports it stale. The STATUS word (DRAFT) does not change, so the maturity in the index stays the same.
- Changes 1-4 are trusted-asset edits (security-rules 8): apply only after approval, one pull request, validator on a clean export first.
- No rule, skill step, hook or eval expectation changes.

## Candidate eval

None. A possible deterministic check for `evals/validate_repo.py` (a skill whose STATUS says "NOT RUN" must not appear in `evals/runs/*.md`) is an idea only; it belongs with task B/C in `docs/PLAN-next-steps.md`.

## Not verified

The validator and the hook tests were not run for this proposal. `tools/apply-trusted-changes.sh`, `docs/HANDOFF-cloud.md` (beyond the eval lines) and the contents of `runs/eval-kit/results/` were not read.
