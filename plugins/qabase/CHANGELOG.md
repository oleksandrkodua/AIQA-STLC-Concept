# Changelog (plugin level)
## Unreleased
- `xray-test-create` script: a network error or an unreadable response in the middle of `--apply` now still prints the cases already created (before: only `STOP`, created keys lost). New offline test; 11 tests pass. Evals NOT RUN.
- Section 0 (ingested content is data) added to `analyze-requirements`, `create-test-cases`, `automation-readiness-assessment`, `create-playwright-test`, `review-playwright-test`, `create-mobile-test`, `review-mobile-test`, as the skill contract requires; STATUS line added to the four copied skills. Evals NOT RUN after the change.
- New skill `xray-test-create` (DRAFT): creates human-approved test cases in Xray Server/DC through a dry-run-first script; token from the environment only. Script tested offline (10 tests); never run on a real instance; evals NOT RUN. Cloud mode (`JIRA_AUTH=proxy`, token as a network secret) and a read-only `--check`. Permission rules added: `ask` on the script, `deny` on commands that mention `JIRA_PAT`.
- `bug-report`: access now states Jira MCP create and edit rights (author's statement, not verified by a run); edit limited to the issue created in the run; one eval added.

## 0.1.0 — 2026-10-20
- First version of the neutral base, derived from an earlier project-specific plugin. The history of that plugin stays in its own repository.
- 18 skills with evals (web and mobile optional), contract template, hooks, navigator index. Four project-specific lookup skills were removed; the `investigation` sector is empty on purpose.
- Not approved. Evals NOT RUN in this base.
