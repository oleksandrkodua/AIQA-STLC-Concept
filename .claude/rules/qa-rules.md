# QA rules

| Field | Value |
|---|---|
| ID | RULE-QA |
| Purpose | How QA reasoning, evidence, verdicts and scope are produced |
| Scope | All QA work in this repository |
| Priority | After security-rules, before playwright/mobile rules |
| Owner / approver | QA Lead (name: UNKNOWN until Discovery) |
| Status | DRAFT — not approved |
| Review date | not set |
| Sources | A layered architecture design (evidence and verdict sections); QA operating disciplines (a template, to be agreed with the team); notes from talks (single-source, see `knowledge/register.md`) |
| Change history | v0.1 created 2026-10-07; neutral base 2026-10-20 |

## Evidence and labels

1. Every substantive claim that affects a decision carries a label: VERIFIED FACT,
   EVIDENCE-SUPPORTED INFERENCE, ASSUMPTION or UNKNOWN. Routine statements need no label.
2. A finding takes this shape: Finding / Evidence (quoted) / Risk / Confidence (and why if not
   High) / Recommendation.
3. Seen once is an OBSERVATION. Seen N times in M tries is a FACT with a frequency. Never
   write "sometimes".
4. "Nothing happened" is the commonest false positive. Re-check after the re-render before
   filing.

## Verdicts

5. Status: READY / READY WITH RISKS / NOT READY / BLOCKED. Per area: PASS / FAIL / NOT
   TESTED / NOT APPLICABLE / BLOCKED / UNKNOWN. NOT TESTED is never collapsed into FAIL, and
   never reported as PASS.
6. Confidence is derived, not asserted. Lowest ceiling applies: anything planned and not done
   caps at MEDIUM; a whole category untested caps at LOW; a key finding resting on one
   unreproduced observation or an emulator caps at MEDIUM.
7. A verdict states what limited it (caps hit, tools missing, categories untested).

## Scope under a time budget

8. Tier work into MUST / SHOULD / SKIP with a reason on each. The SKIP tier is never empty,
   and each SKIP names the risk being accepted.
9. Before a verdict, reconcile: every MUST item is marked done or carried over.

## Severity and priorities

10. Technical severity and severity to this client are different. Rank by the client's stated
    priorities, say that you did, and say what moved and why. Never delete a deprioritised
    finding; demote it.
11. Accessibility is classified by consequence: cannot reach / activate / complete is
    Functional regardless of the brief's UI/UX label.

## Defects and regression

12. Before filing, check the tracker for a duplicate. A closed match is a regression, not a
    new defect (tracker is UNKNOWN until Discovery; until then say the check was not done).
13. Iron Law: a defect gets a failing test first; the fix is accepted only after that test
    passes. Show the failing run against the defective build.
14. Automation is the output of a manual pass. A spec is written only for a case that has
    been confirmed by a manual run.

## Acceptance criteria

15. Do not stop at the happy path. Ask for empty states, invalid input, limits, permissions
    and failure behavior. A criterion is usable only if one test case follows from it
    unambiguously.

## Human understanding

16. A case that depends on human comprehension (wording, time formats, visual clarity) is
    tried by a person, not only run by a script.

## Run limits (template — agree with the team)

17. Per run: at most 6 skills used, 2 re-runs, and stop after 3 consecutive passes with no new
    finding, unless a human raises the cap in writing. A run journal records this
    (`runs/QA-RUN.template.md`).
