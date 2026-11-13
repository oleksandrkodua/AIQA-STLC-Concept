# Proposal: check the create-test-cases matrix with code, and redo only what a reviewer rejected

STATUS: PROPOSED, not approved, NOT APPLIED. Nothing in `plugins/qabase/**`, `.claude/skills/**`, `evals/**` or `tools/` has been changed. Provenance: ai-generated (Claude Code, Sonnet 5.5, 2026-11-13); human-confirmed: pending. Approver: QA Lead (Oleksandr Kukhtinov acts as QA Lead for this repository).

Origin: an idea from a set of slides about a test-automation pipeline (one source, author and date not shown, numbers self-reported; kept locally and not in git). Taken here: "a script does the mechanical check, the model does the judgement" and "repair only what is broken, no full regeneration". Both are ideas to test, not facts about our setup. Per ai-rules 8 they do not become rules without this proposal.

## Why

1. `create-test-cases` section 9 ends with a `MATRIX CHECK` block ("AC without a case: <list or none>", "criteria with positive + negative: <n of n>" and so on). Section 8 lists these as completeness rules. Today the model fills that block about its own output. Read 2026-11-13: nothing in the repository checks it (the skill has "Read access ... No writes", section 12; `evals/validate_repo.py` checks repository structure, not case sets). A self-reported "none" is the false-assurance pattern the repository rules warn about (ai-rules 1, 3).
2. The checks are mechanical: set membership of AC ids, presence of a `Covers` line, presence of one positive and one negative per AC. They need no model and no access to application code.
3. Section 10 gives the reviewer per-case KEEP / MODIFY / REJECT / DEFER decisions, but nothing says what a MODIFY re-run may touch. Without a rule, a rerun can regenerate the whole set, which changes cases the reviewer already accepted and forces a second full review.

## Changes

Files: 1 new tool, 1 edited skill, 4 new fixtures, 1 validator addition. Source of the skill is `plugins/qabase/skills/create-test-cases/`; run `bash tools/sync-skills.sh` and `python3 tools/build-skills-index.py` after.

### 1. NEW `tools/check-test-cases.py` (standard library only)

Usage: `python3 tools/check-test-cases.py <cases.md> --brief <brief.md>`

- `<cases.md>`: the skill output, saved by the reviewer (for example `runs/<id>/cases.md`; `runs/` is git-ignored). `<brief.md>`: the approved brief with its `AC-<id>-n` numbers.
- Reads the `COVERAGE MATRIX` table (columns Criterion, Category, Cases) and the `CASE <n>` blocks (`Covers:` line, `Provenance:` line).
- Checks, each reported as PASS or FAIL with the ids involved:
  1. every AC id of the brief appears in at least one case's `Covers` or in `NOT COVERED`;
  2. every case has a `Covers` line with at least one id that exists in the brief or is marked local;
  3. every AC id that has cases has at least one row with category `positive` and one with `negative`, or is listed in `NOT COVERED`;
  4. every case has a `Provenance` line and none carries `Status: Approved` (drafts only, same as eval 4 MUST).
- Exit code 0: all PASS. 1: at least one FAIL. 2: input could not be parsed. An unparsable input is reported as UNPARSED, never as PASS (fail-closed).
- Does not judge quality, oracles or duplicates. It says only what is mechanically checkable, and says so in its output.

ASSUMPTION to verify when building: the table and case layout in section 9 is stable enough to parse. If real outputs drift, the script exits 2 and the skill's format section is the thing to tighten.

### 2. EDIT `SKILL.md`

2a. Section 9, `MATRIX CHECK` heading. Old:
```
MATRIX CHECK
```
New:
```
MATRIX CHECK (model self-report; the reviewer confirms it with tools/check-test-cases.py)
```

2b. Section 10, after the four decision bullets, add:
```
On MODIFY, the rerun changes only the cases and matrix rows the reviewer named, and the
rows that depend on them. Every other KEEP case stays as it was; the output lists what
changed and what did not. A full regeneration needs the reviewer's explicit request.
```

2c. Status line: add "section 9-10 extended <date of approval> (matrix check by tools/check-test-cases.py, MODIFY scope)". Evals stay NOT RUN.

### 3. NEW fixtures and validator checks (`evals/**`)

Under `evals/fixtures/test-case-check/`: `good.md`, `missing-ac.md` (one AC without a case), `no-negative.md` (one AC with positive only), `unparsable.md`. A brief fixture `brief.md` with three AC ids. `evals/validate_repo.py` gets four checks: the script exits 0 on `good.md`, 1 on each of the two bad ones, 2 on `unparsable.md`. This is the test for the tool: the failing fixtures must fail.

## Consequences

- Behavior of the skill: unchanged except the MODIFY rule (one paragraph) and the relabelled heading. The model still writes the `MATRIX CHECK` block.
- New moving part: a script the reviewer runs by hand (one command). It is not run by Claude, not by CI, not by a hook. Wiring it into CI or the Stop hook is a later, separate decision (see `docs/PLAN-next-steps.md` task A and E).
- Cost: the script and fixtures must be maintained when the section 9 format changes. A format change in the skill without a matching script change fails the validator, which is the intent.
- Validator count rises (4 new checks). Run it on a clean export before the PR.
- Limits: does not catch weak oracles, duplicates, invented values or wrong categories. A green script does not mean the set is good; the human review (section 10) stays the gate.
- No change to rules, hooks, settings, `CLAUDE.md`, `policy/`. The `CLAUDE.md` table row stays true ("DRAFT, evals NOT RUN").
- Interaction with `feedback/proposals/2026-11-12-adaptive-technique-selection.md`: both edit `SKILL.md` section 9 (this one the heading and `MATRIX CHECK`, that one the matrix header and `MATRIX CHECK` content). Apply them in order and rebase the second; the `Technique` column is not checked by the script until it exists, and then the parser needs the column added.

## Alternatives

- Leave as is: no cost, the self-reported block stays unchecked.
- Let the skill run the script: blocked by section 12 (read-only) and ai-rules 14; would also be a model grading its own output.
- Put the checks into `evals/validate_repo.py` only: that file tests the repository, not a given run's output.

## Open questions

1. Who runs the script: the reviewer by hand (proposed), or later CI/Stop hook?
2. Where should reviewers save outputs: `runs/<id>/cases.md` (proposed, git-ignored)?
3. OK to keep fixtures under `evals/fixtures/test-case-check/`?

## How to apply after approval

Branch from `main`; add the tool and fixtures; edit the skill (source dir only); `bash tools/sync-skills.sh`; `python3 tools/build-skills-index.py`; run `python3 evals/validate_repo.py` on a clean export of `git ls-files`; commit without a Co-Authored-By line; the owner pushes and opens the PR.
