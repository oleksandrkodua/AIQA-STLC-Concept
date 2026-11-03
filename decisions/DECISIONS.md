# Decision log

Every decision has a status: STATED (the owner said it), PROPOSED (suggested, not confirmed), VERIFIED (checked against evidence). The owner of decisions is the person named in `context/discovery.md`; Claude proposes and prepares.

## Decisions

| ID | Decision | Status | Basis |
|---|---|---|---|
| D-001 | The author email stays in `portfolio/Oleksandr_Kukhtinov_AI_QA_One_Pager.html`; `README.md` author line keeps LinkedIn only (email removed, commit 2f179db). The email remains in earlier git history on origin. | STATED | Owner, 2026-11-03 |
| D-002 | Mentions of `AGENTS.md` in `training/lessons/` and `knowledge/register.md` are not changed after `AGENTS.md` was removed from the repository: they describe a conference convention and a quoted source (R-20), and none claims the file exists here. | STATED | QA Lead, 2026-11-03 |
| D-003 | Monitoring is not applicable in the MVP: there is no production runtime and work is DEV only. Substitutes: the CI check validate on every pull request, the run journal check, and re-running the evals after each skill change. Revisit when agents or routines are enabled. | STATED | QA Lead, 2026-11-04 |
