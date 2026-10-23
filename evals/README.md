# Evals

STATUS: plan + first logic tests. Skills' evals: NOT RUN, except `feedback-triage` (partly run 2026-10-23, bar NOT met; see `docs/HANDOFF-cloud.md`). Hook firing: NOT RUN.

Principle: a skill, hook or agent is "working" only after its evals ran and the result is
recorded. Write the PASS and FAIL criteria before the run. INCONCLUSIVE (setup broken) is
not FAIL and not PASS. Generation is stochastic: run each skill eval 3 times and report the
spread, not the best run.

Term (R-15): "MUST 3/3" is pass^3, all three runs must pass; one success in three (pass@3) is not enough.
A grader or a task that fails every run is first suspected of being broken (R-15); an eval at 100% only guards against regressions.

## Layers

| # | Layer | What | Where | Status |
|---|---|---|---|---|
| 1 | Skill evals | 3 prompts per skill with written expectations; run 3× each | `.claude/skills/<skill>/evals/evals.json` | written for 17 skills (all but `exploratory-testing-web` and `-mobile`); NOT RUN, except `feedback-triage` (partly run, bar NOT met) |
| 2 | Skill selection | 10+ prompts without a slash; the expected skill must load every time | `evals/skill-selection.md` | written; NOT RUN |
| 3 | Hook logic tests | scripts decide as specified for fixed inputs | `evals/hooks/run_hook_tests.py`, `run_runcheck_tests.py` | PASS 20/20 and 9/9 on 2026-10-07 (sandbox) |
| 4 | Hook firing tests | Claude Code actually invokes the hook and honors the decision | `evals/hooks-firing.md` | NOT RUN |
| 5 | Governance deny tests | prod → deny, secret → deny, edit of a rule → ask, unapproved MCP → deny | `evals/governance-tests.md` | written; NOT RUN |
| 6 | Injection tests | text inside a ticket/page/log that tries to instruct the assistant is reported, not obeyed | `evals/injection-tests.md` | written; NOT RUN |
| 7 | Mobile checks | environment switch verified before run; SKIP not counted as PASS; emulator labelled | covered by layer 1 mobile evals + `mobile-rules.md` | partly written |
| 8 | Test-suite quality | sabotage matrix: what do our Playwright/Appium suites actually catch | `evals/sabotage-matrix.md` | written; NOT RUN |
| 9 | Agent audit | LLM Council prompt on each agent/routine description before enabling | `evals/agent-audit.md` | written; NOT RUN; agents are off in MVP |
| 10 | Long session | rules still obeyed after many steps and compaction | architecture design (long sessions) | LATER |
| 11 | Baseline | reference outputs and KPIs measured before any claim | architecture design (metrics) | after pilot |

## Recording results

Create `evals/runs/<date>-<layer>.md` with: what was run, command or prompt, model and
version, raw result per expectation (PASS / FAIL / INCONCLUSIVE), and the decision it
changes in `decisions/verification-log.md`. Do not edit an old result; add a new file.

Before changing a skill or a grader after a FAIL, read the transcript of the failed run and write down whether the skill or the grader was wrong (R-15).
**An error becomes an eval.** When a feedback entry is accepted by the AI QA Process Lead, the proposal carries a candidate eval case: the prompt that went wrong and an expected result taken from an approved source (approved test case, AC, brief), never from what the app or the model produced. The case is added to the touched skill's `evals/evals.json` only through the review-and-update step, then run 3 times (MUST 3/3). Never weaken an assertion to turn a failing eval green; a failing eval means the skill is wrong, the task is wrong, or the grader is broken (read the transcript, R-15).
An LLM judge gets an "Unknown" option, one judge per dimension, and a human spot-check of its verdicts (R-15).

## Commands available now

```
python3 evals/hooks/run_hook_tests.py        # hook script logic
python3 evals/hooks/run_runcheck_tests.py    # run-journal checker, known-good/bad journals
python3 evals/validate_repo.py               # structure checks (CLAUDE.md length, JSON, frontmatter, links)
```
