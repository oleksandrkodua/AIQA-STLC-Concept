---
paths:
  - "automation/mobile/**"
---

# Mobile rules (WebdriverIO + Appium, optional)

| Field | Value |
|---|---|
| ID | RULE-MOB |
| Purpose | Keep mobile automation safe, environment-correct and honest about devices |
| Scope | `automation/mobile/**` (loaded only when working there) |
| Priority | After security, qa, ai |
| Owner / approver | QA Lead |
| Status | DRAFT — not approved |
| Sources | An earlier project's mobile test how-to (read; its code NOT run); QA operating disciplines |
| Open check | whether `paths:` scoping loads this file as expected; whether the project's mobile code runs |

## Environment first

1. A mobile app may open on a production backend by default. Every new build must be switched
   to the test environment before any test (how depends on the app, for example an in-app
   environment switch followed by a restart). The switch may persist only while app data is not
   reset (`noReset: true`). Treat "environment switched" as a precondition to verify, not assume.
2. If the environment cannot be confirmed from the app, stop and report. Do not run.
3. Record the build identity (version, build number, install source) and the active feature
   flags in every run. A result without a build fingerprint cannot be compared later.

## Devices

4. An emulator is not a device. Evidence from an emulator is labelled EMULATOR, from
   hardware DEVICE. A mobile finding from an emulator alone caps confidence at MEDIUM and
   must be re-checked on hardware before it is called confirmed.
5. Android emulator runs use the hardware GPU option, otherwise runs are several times
   slower (a note from an earlier project, not verified here).
6. iOS: execution needs macOS or a cloud device service. An iOS project is a scaffold until a
   working path is demonstrated.

## Writing tests

7. Tests start from a known entry screen (for example Home). The suite's `before` hook launches
   the app and clears onboarding; a new onboarding screen is handled by extending the helper
   list, not by a test-local hack.
8. Import helpers from the project's single helper entry point (a barrel). Prefer accessibility ids over
   text locators for stability; text locators are acceptable to start.
9. Use environment-neutral anchors. Test data on the test environment differs from PROD
   (placeholders, stub products); an assertion that exists only on PROD is wrong.
10. Guest and logged-in suites are separate. The logged-in suite is gated: with no valid
    session its cases SKIP with instructions. SKIP must be visible in the report, never
    counted as PASS.
11. Network oracle: reset the network log before the flow, then fail on unexpected errors
    with an explicit allowlist for expected ones. Each allowlist entry carries a reason.
12. Screenshots and logs go to the run's evidence directory and stay out of commits.
13. No credentials in specs. Sessions are created by hand once under the tester's own
    account or via environment variables.

## Running

14. Run specs one at a time when diagnosing; the full suite only after the single specs are
    stable. Type-check after code changes.
15. A mobile regression run reports: build fingerprint, environment, device or emulator,
    suite, PASS / FAIL / SKIP counts, and what was not run.
