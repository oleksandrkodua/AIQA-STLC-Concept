# Story 6: a test fails after a release

STATUS: ILLUSTRATIVE, 2026-10-23. Written by hand; not a recorded run.

**Situation:** after release 4.3.0-demo the nightly CI run on DEV shows three red tests. Nobody has looked at them yet.

| Stage | Skill | What it produces | Human gate |
|---|---|---|---|
| 5 CI | none (deterministic) | The red run, logs and traces | None; it is just the result |
| 6 Test analysis | `ci-failure-analysis` | The table below | A person reads it before anyone acts. "PRODUCT" is a hypothesis until a person reproduces it |
| 3 Manual testing | none (a person) | The developer's suspicion for F1 is reproduced by hand on DEV | The tester confirms or rejects the hypothesis |
| 3 Manual testing | `bug-report` | A draft for F1 (see story 1 for the shape) | The tester confirms; the Iron Law applies: the bug gets a failing test first, and the fix is accepted only after it passes |
| 4 Automation | `ci-fix` | A draft change for F2: update a locator that moved in the redesign | The tester reviews the diff and merges |
| 6 Test analysis | none | F3: the DEV database was being reset at the time; rerun after the reset passes | The tester classes it ENVIRONMENT; DevOps is told |
| 9 Feedback | `feedback` | An inbox entry: the redesign broke three locators because the ids changed without notice | The AI QA Process Lead later decides whether this becomes a rule |

## The analysis (ILLUSTRATIVE)

```
CI ANALYSIS - nightly, 4.3.0-demo, 2026-10-23
| Test | Failure (first error) | Class | Evidence | Confidence | Next |
| F1 checkout applies promo code | expected 36.00, received 40.00 | PRODUCT (hypothesis) | assertion failure, screenshot shows no discount line; the same test passed on 4.2.0 | EVIDENCE-SUPPORTED | reproduce by hand, then /bug-report |
| F2 search filter by category | timeout waiting for [data-test=cat-filter] | TEST | the redesign changed the selector; trace shows the element under a new name | EVIDENCE-SUPPORTED | /ci-fix |
| F3 wishlist add | HTTP 500 from the setup call | ENVIRONMENT (possible) | DEV reset job log at the same minute | INFERENCE | ask DevOps, rerun |
GROUPS: F1 and F2 share a release but not a cause   NOT ANALYZED: none
```

## What this story shows
- Three red tests, three different kinds of cause, three different next steps. The skill classifies and gives its evidence; a person decides.
- A product bug starts from a manual reproduction and a failing test, not from the model's guess.
- The failure feeds back into the system as an inbox entry, not as a silent change of a rule.

## What it does not show
- Real logs or traces. FLAKY needs a history of runs; with none, the table says "possible", never "flaky".
