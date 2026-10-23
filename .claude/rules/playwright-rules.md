---
paths:
  - "automation/web/**"
---

# Playwright rules (web)

| Field | Value |
|---|---|
| ID | RULE-PW |
| Purpose | Keep web tests deterministic, reviewable and honest about what they assert |
| Scope | `automation/web/**` (loaded only when working there) |
| Priority | After security, qa, ai |
| Owner / approver | QA Lead |
| Status | DRAFT — not approved |
| Sources | A layered architecture design (Playwright section); an earlier web how-to; QA operating disciplines |
| Open check | whether `paths:` scoping loads this file as expected |

## Writing tests

1. Prefer stable, user-facing locators (role, label, text) and project-approved `data-testid`.
   Page objects only where they remove real duplication.
2. No hardcoded waits (`waitForTimeout`, sleeps). Use auto-waiting and explicit conditions.
3. A test asserts the expected result from an approved oracle (requirement or acceptance
   criterion). Never copy the observed behavior into the assertion. No tautological asserts
   (`toBeTruthy` on something that is always truthy).
4. A test that cannot state its oracle is not written. Send the case back.
5. Tests are independent and order-free. Test data lives inside `automation/web`, is
   synthetic, and never includes real customers. Order-freedom can be checked with
   `--shuffle` (1.64+); the printed seed reproduces the order.
6. No self-healing during a run. A test passes its assertions or fails visibly.
7. Credentials come from environment variables. Never in code, config or fixtures.
8. Target only DEV or approved non-production URLs from config. No production URL anywhere.

## Evidence before "done"

9. Type-check (`npx tsc --noEmit` from `automation/web`), run the test, run it again to
   check stability (a test that fails only in parallel: rerun with `retryStrategy: 'isolated'`, 1.62+, to tell a concurrency bug from real flakiness), and break it on purpose once to show it can fail. Report each as PASS /
   FAIL / NOT RUN. A test that has not been seen to fail proves nothing.
10. For a fixed defect: show the test failing on the defective build, then passing on the
    fixed one (Iron Law).

## Review rules (silent coverage loss)

11. A skipped test, a weakened assertion and a changed locator each need an explicit reason
    in the diff. Reviewers treat them as coverage removal until justified.
12. Playwright detects only what is asserted. Known blind spots by default: layout and
    visual changes, performance, accessibility (needs axe), non-Chromium browsers (check the
    config `projects`). Say what a green run does not cover.

## Project hygiene

13. `automation/web` stays self-contained: own `package.json`, `tsconfig.json` and config; no
    imports reaching outside it. Candidate enforcement: dependency-cruiser rule (not yet
    tried).

## Version gating

14. The baseline is the Playwright version the project pins (this base was written against
    1.62.1; see `docs/PLAYWRIGHT-SETUP.md`). Features marked (1.64+) are used only after the
    project moves to 1.64 (a decision of the project owner; not yet tested).
15. Not allowed in committed tests: `page.getByRef()` (refs are ephemeral) and WebMCP
    (`page.webmcp`, experimental). `locator.within()` is allowed only on 1.64+.
