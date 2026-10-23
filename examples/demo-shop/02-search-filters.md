# Story 2: search filters (web)

STATUS: ILLUSTRATIVE, 2026-10-23. Written by hand; not a recorded run.

**Requirement DS-214 (fictional):** "On the search results page a customer can filter by category and price range. Results update without a page reload. The filter state is kept when the customer opens a product and comes back."

| Stage | Skill | What it produces | Human gate |
|---|---|---|---|
| 3 Manual testing | `exploratory-testing-web` | A session note: filters combine correctly; the price range accepts a minimum above the maximum and returns an empty list with no message (finding F-1, Low) | The tester files F-1 only after a second try reproduces it (seen once is an observation) |
| 3 Manual testing | none (a person) | The case "category + price range returns only matching items" is run by hand on DEV, with the build and browser recorded | The tester records PASS with evidence |
| 4 Automation | `automation-readiness-assessment` | See the block below | The tester approves the candidate (or refuses) |
| 4 Automation | `create-playwright-test` | A draft test for the case, locators verified against the running DEV page, tagged with the AC id | The tester reads the draft |
| 4 Automation | `review-playwright-test` | A review: one fixed wait replaced by a wait on the results list; one assertion checks the text of the count, not the items | The tester accepts or rejects each finding |
| 5 CI | none (deterministic) | The test runs on DEV in CI on every merge to the main branch | Nobody decides; a person reads the result |

## The readiness assessment (ILLUSTRATIVE)

```
CASE: filter by category and price range      TARGET: web
MANUAL PASS: tester, 2026-10-23, build 4.2.0-demo, DEV, desktop browser
RECOMMENDATION: AUTOMATE NOW

CRITERIA
- Repeat value: HIGH, runs on every release
- Risk: MEDIUM, a wrong filter shows wrong products
- Stability: HIGH, the filter component has not changed in the last three releases (source: release notes)
- Testability: HIGH, stable test ids on the filter controls
- Oracle: exact, the price range of every item on the page lies inside the chosen range

BLOCKERS / UNKNOWNS
- Test data: needs a fixed catalog on DEV → the DEV data owner

COST I CANNOT SEE
- Maintenance when the catalog seed changes

NEXT STEP: human approval, then create-playwright-test
```

## What this story shows
- Automation starts from a manual pass that is evidenced; the assessment says NOT EVIDENCED otherwise.
- Two gates sit between the model and the main branch: the candidate approval and the pull request review.
- CI is plain code. If the AI service is down on merge day, the test still runs.

## What it does not show
- A real test, a real page or a real CI run. Whether a drafted test would pass review is exactly what the evals, which are NOT RUN, would measure.
