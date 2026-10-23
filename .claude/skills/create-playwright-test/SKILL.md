---
name: create-playwright-test
description: Implement an approved automation candidate as a Playwright test, following the project's Playwright rules. Use after a test case has passed automation readiness assessment and a human has approved automating it. Not for mobile tests (use create-mobile-test), not for reviewing a test (use review-playwright-test), not for deciding whether to automate (use automation-readiness-assessment).
---

# Create Playwright Test

## 1. Purpose

Turn an approved automation candidate into deterministic Playwright code that runs without
Claude in the loop. The output is a draft pull request, reviewed by a human before merge.

## 2. Trigger

- a case has passed `/automation-readiness-assessment` with AUTOMATE NOW and a human approved
  it;
- an approved change to an existing test needs implementing;
- explicit invocation: `/create-playwright-test <case id>`.

Negative triggers: not for deciding whether to automate, not for repairing a failing test
(that is a reviewed change, see section 11), not for exploratory scripting.

## 3. Required inputs

- the approved test case: preconditions, steps, expected result;
- the approval itself — who approved automating it, and when.

## 4. Optional inputs

- the readiness assessment, including named testability gaps;
- existing tests, fixtures, helpers and page objects in `automation/web` (registry in CLAUDE.md);
- project `data-testid` conventions.

## 5. Required context

- `.claude/rules/playwright-rules.md`, `.claude/rules/qa-rules.md`;
- the existing structure under `automation/web` (registry in CLAUDE.md) — read before writing, so the test reuses what
  is there instead of inventing a parallel set of helpers;
- `examples/approved-tests/` in this skill directory, if present; approved tests only. An example past its `review_due` date is used only with an explicit flag.

## 6. Preconditions

- the case is approved and its expected result is observable;
- the target environment is a non-production environment;
- if the readiness assessment listed a blocking testability gap, it has been resolved. If it
  has not, stop and say which gap blocks implementation.

## 7. Steps

1. Restate what the test verifies, in one sentence. If the case supports more than one
   sentence, it should be more than one test.
2. Read the existing structure: does a fixture, helper or page object already cover the setup?
3. Choose locators. Prefer stable, user-facing locators and project-approved `data-testid`.
   Verify each locator against the running application rather than assuming it exists.
4. Write the test: arrange, act, assert. One intent per test.
5. Run it locally against a non-production environment. A test that has never run is not a
   deliverable. Type-check first: from `automation/web` (registry in CLAUDE.md) run `npx tsc --noEmit`. Fabricated
   imports, misspelled fixtures and wrong signatures fail here, before anyone spends review
   time on them. Where source access exists, also confirm that each test id and route the
   test uses appears in the source.
6. Run it twice. A test that passes only sometimes is not finished.
7. **Tag it with the AC id** from the case's `Covers` line: `test('<title>', { tag: '@AC-123-2' }, ...)`
   (one tag per AC). No `Covers` line → stop and send the case back.
8. **Sabotage check** for a test the human marked critical in the approval (first three tests
   of the pilot, then by decision): run it once on a throwaway copy with the behavior broken
   from outside the app (for example `page.route` changing a price, a status or hiding an
   element). It must FAIL. Record what was changed and the result. A test that stays green is
   decoration: fix the assertion. Never commit the sabotage.
9. Open a pull request with the test, the case reference and the approval reference.

## 8. Code rules

- **No hardcoded waits.** Use Playwright's built-in waiting and web-first assertions. A
  `waitForTimeout` in a submitted test is a defect in the test.
- **Deterministic.** No dependence on execution order, leftover state, or another test's data.
- **Isolated data.** Each test sets up and tears down what it needs; nothing is shared through
  the environment.
- **POM is optional.** Use page objects, components, fixtures and helpers only where they
  remove real duplication. An abstraction used once is noise.
- **Locators:** stable and user-facing first, project `data-testid` second, fragile CSS or
  XPath only with a written justification in the PR. Check the project's Playwright version
  first (docs B1.6/B1.6a): `locator.within()` is 1.64+ only, so on the 1.62.1 baseline scope with a
  parent locator and chaining. Never commit `page.getByRef()` (refs are ephemeral) or WebMCP
  (`page.webmcp`, experimental).
- **Assertions are meaningful.** Assert the behavior the case describes, not that the page
  rendered something.
- **Assertions come from the case's oracle.** Do not assert whatever the application currently
  returns because it is easy to assert, and do not add assertions the case does not call for.
  If the case states no oracle, stop and send it back.
- **Readable over clever.** The next person to touch this test is debugging it at speed.
- **CI-ready from day one.** No dependency on a Claude session, no local-only paths,
  credentials only from environment variables or secret storage, traces and screenshots as
  artifacts.
- **Cross-browser:** the test belongs to the browser projects the product supports. A
  browser-specific skip carries a reason and a ticket.

## 9. Output

A pull request containing:

```
TEST: <file path>
CASE: <case id / title>
APPROVED BY: <who approved automation, date>

WHAT IT VERIFIES
<one sentence>

LOCATORS
- <locator> — <why this one; verified against the app on <date>>

REUSED
- <fixture / helper / page object already in the repo>

ADDED
- <anything new, and why it was needed>

LOCAL RUN
- type-check: <command> — <result>
- <command> — <result, run twice>
- AC tag: <@AC-... as in the case>
- sabotage (critical tests only): <what was broken> -> <FAILED as expected | stayed green | not required>

OPEN POINTS
- <anything the reviewer must decide>
```

## 10. Checkpoints and approval

The pull request is the gate. A human reviews it — with `/review-playwright-test` as a first
pass — and approves before merge. New shared fixtures, helpers or page objects are an
architecture change and need QA Lead approval, not just a reviewer's.

## 11. Failure and uncertainty handling

- A locator cannot be verified against a running app → say so; do not guess a selector.
- The case is ambiguous → stop; route back to the case, not around it.
- The test passes only intermittently → do not submit it and do not add a wait to stabilize
  it; report the instability and its suspected cause.
- Repairing an existing failing test is a code change like any other: proposed as a diff,
  reviewed, merged. Never a silent fix, never a runtime self-heal, never a skip added to make
  a suite green.
- If the Playwright generator agent produced the draft, its output is treated exactly the
  same: it is a draft in a pull request, subject to every rule above.

## 12. Tools

Read and write inside `automation/web` (registry in CLAUDE.md) only. Browser access to non-production environments for
locator verification and local runs. No production, ever.

## 13. Security and data handling

No credentials in code, fixtures or fixtures' data files. No real customer data. Traces and
screenshots may capture data — treat artifacts as sensitive and keep them out of the
repository.

## 14. Provenance

Record in the PR: source case, approval, model and version, this skill, date, and whether an
agent produced the first draft.

## 15. Non-goals

Does not decide what to automate, does not modify test cases in the TMS, does not touch CI
configuration, does not refactor unrelated tests.
