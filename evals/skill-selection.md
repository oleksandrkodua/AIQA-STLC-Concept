# Skill selection test

STATUS: written 2026-10-07, NOT RUN. Source: an earlier skills inventory (rows 1–10),
extended with mobile rows.

How to run: in the repository, start a fresh session for each prompt. Type it WITHOUT a
slash. Note which skill loads. Repeat 3 times. PASS = the expected skill loads all 3 times.
Written before running: any miss is a FAIL for that row (not "mostly worked").

| # | Prompt | Expected | R1 | R2 | R3 |
|---|---|---|---|---|---|
| 1 | Write test cases for this story: "A shopper can apply one discount code at checkout." | create-test-cases | | | |
| 2 | Is this story ready to test? | analyze-requirements | | | |
| 3 | Review these requirements before we start test design. | analyze-requirements | | | |
| 4 | Automate this approved case in Playwright: expired code is rejected. | create-playwright-test | | | |
| 5 | Review this Playwright test diff and tell me whether it is any good. | review-playwright-test | | | |
| 6 | Should we automate this case, or keep it manual? | automation-readiness-assessment | | | |
| 7 | Напиши тест-кейси для цієї історії. | create-test-cases | | | |
| 8 | Проаналізуй вимоги перед тестуванням. | analyze-requirements | | | |
| 9 | This Playwright test fails in CI, why? | none of ours; must propose a diff, not edit silently | | | |
| 10 | Do a manual smoke test of the login page. | not ours | | | |
| 11 | Automate this approved case on Android with Appium: search for water shows Sort. | create-mobile-test | | | |
| 12 | Review this Appium test diff. | review-mobile-test | | | |
| 13 | Which of these regression cases are worth automating? | automation-readiness-assessment | | | |
| 14 | Write a Playwright test for the Android app. | neither web nor mobile test skill writes it silently: the assistant points out the platform mismatch | | | |

Rows 1–8 and 11–13: ours must win. Rows 10 and 14: ours must not steal or guess. Row 9
tests behavior. A failing row is fixed in this order: make the competing skill manual-only,
sharpen our description, only then remove anything (V27).
