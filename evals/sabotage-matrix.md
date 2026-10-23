# Sabotage matrix — what do our suites actually catch

STATUS: NOT RUN. Method (known-answer): in a throwaway branch of a TEST environment build,
introduce one deliberate breakage at a time and see whether the suite goes red. Source:
an earlier QA agent's Playwright detection matrix (read), generalized to mobile.

Core truth: a suite detects only what it asserts. A green run means "what someone checked
did not break", not "the product works".

| Sabotage | Web (Playwright) | Mobile (Appium) | Caught? (fill) |
|---|---|---|---|
| Remove an event handler (dead button) | only if a test clicks it and asserts the result | same | |
| Break an API response shape | only on the real stack, not against mocks | network oracle may catch | |
| Corrupt state | only if asserted | same | |
| Wrong value (expected 12.00, app shows 10.00) | only if the assertion encodes the oracle | same | |
| Browser/OS specific bug | only if the config runs that project (check `projects`) | only on that device/OS | |
| Layout / visual break | no (needs screenshot comparison) | no | |
| Accessibility regression | no (needs axe) | no (needs accessibility checks) | |
| Performance regression | no | no | |
| Test escape hatch in production code | no | no | |

Use: list what each suite does NOT catch next to each report, and cover those by hand.
Do not run sabotage on any shared or production environment.
