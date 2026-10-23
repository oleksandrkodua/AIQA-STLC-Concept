# Automation projects

STATUS: registry only. NOTHING is present or verified. The registry of record is in `CLAUDE.md`. Every project here is optional: add one only when the project needs it.

| Project | What it is | How to add it | Check that ends the step |
|---|---|---|---|
| `web/` | Playwright web tests | create or copy a self-contained project: own `package.json`, `tsconfig.json`, config; no references outside the folder; hosts come from config | `npm ci`, type-check, one smoke spec on the test environment |
| `mobile/android/` | WebdriverIO + Appium Android tests | copy with a helpers folder and any setup or doctor scripts the project has; keep a single helper entry point; document the `noReset` behavior | `npm ci`, `npm run typecheck`, a launch smoke on the test environment, emulator with the hardware GPU option |
| `mobile/ios/` | iOS scaffold | scaffold only | none until a working path is demonstrated |
| `api/` | API tests (tool chosen by the project) | later | later |

Do the copy in the real working repository, outside a cloud-synced folder.

## Requirements on every project
- Self-contained: own `package.json`, config, test data; no imports outside it.
- Reads environment and credentials from environment variables; no secrets in files.
- Targets only the test environment from config; refuses to start when the mobile app's
  environment cannot be confirmed.
- Evidence output goes to a run directory that is git-ignored.
- Has its own README with the "how to run" and "how to add a test", rewritten after the first
  successful run.
