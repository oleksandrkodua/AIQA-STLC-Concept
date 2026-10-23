# qabase (DRAFT v0.1.0, not approved)

QA skills, one per stage. A neutral base: it carries no project facts. Web and mobile skills are optional; use only those whose automation project the repository registers in `CLAUDE.md`.

Layout:
- `skills/`    — skills that go into the plugin build
- `reserved/`  — kept in repo, NOT in the build (design-check, test-plan-and-regression)
- `_base/`     — donor skills (manual-tester, exploratory-testing; each keeps its own MIT LICENSE), not loaded
- `_templates/SKILL-CONTRACT.md` — 13-section contract every skill must follow
- `hooks/`     — hook scripts; `hooks.draft.json` is INACTIVE (rename to `hooks.json` only after firing test)

Status: skeletons are STATUS SKELETON; evals NOT RUN. Nothing here was tested on a machine of any employer or client.

## Install (local test, NOT VERIFIED on any specific Claude Code version)
From the repo root:
    claude plugin validate plugins/qabase
    claude plugin validate .
Then in Claude Code: `/plugin marketplace add ./` and `/plugin install qabase@qabase-marketplace`.
Skills are then namespaced `/qabase:<skill>`.

## Known limits
- A plugin cannot ship `permissions.deny/ask`; keep the permission floor in repo `.claude/settings.json`.
- Plugin `CLAUDE.md` is not loaded; always-on rules stay in the repo root CLAUDE.md / `.claude/rules/`.
