# Skills navigator: design (DRAFT, approved in chat 2026-10-13, not yet implemented)

Owner: the AI QA Process Lead. Status: design approved in chat; this file not yet reviewed by the owner as a document. Phase 1 (`NAVIGATOR.yaml` files, `skills-index.json`, the validator check) is built; the router skill and the HTML compass are not.

## Goal
Help the QA team find the right skill of the `qabase` plugin for a task, inside Claude Code during daily work (primary), with a visual map for onboarding and training (secondary, same data).

## Decisions taken (chat 2026-10-13)
1. One generated index feeds two consumers: a router skill (B, primary) and a static HTML compass (A, later).
2. Order: phase 1 index and checks, phase 2 router skill, phase 3 HTML compass.
3. Index language: English (project rule). The router understands Russian or Ukrainian requests because the model maps them to English intents. The HTML search matches English words only.
4. Compass structure: 7 sectors clockwise in SDLC order; click shows the sector's skills with when / not for / copyable command; search box on top; "red line" accordion at the bottom.

## Phase 1: index (single source of truth = the skill folders)
- Each skill folder gets `NAVIGATOR.yaml` (hand-written, 3-5 lines): `sector` (one id from the sector list), `intents` (2-4 short task phrases), optional `tags`, optional `needs` (e.g. Jira MCP, Grafana).
- Sector list: one file `plugins/qabase/navigator-sectors.yaml` (id, title, order). Proposed sectors: requirements, manual, automation, ci, investigation, reporting, setup.
- Derived automatically by `tools/build-skills-index.py` (walks `plugins/qabase/skills/*/`): `name` and `description` from `SKILL.md`; the "not for / neighbour" from the description exclusion phrases already parsed by validator check 3b.
- Output: `plugins/qabase/skills-index.json` (generated, never edited by hand).
- Add a skill: new folder -> validator fails until `NAVIGATOR.yaml` is valid. Delete a skill: folder gone -> entry gone on next build; a stale JSON fails the validator.
- Validator additions (`evals/validate_repo.py`): every skill folder has a valid `NAVIGATOR.yaml`; sector exists; each skill in exactly one sector; `intents` 2-4 and non-empty; neighbour names exist; `skills-index.json` equals a fresh build.
- Hooked in: `tools/sync-skills.sh` runs the build; git pre-commit already runs the validator, so a stale index blocks the commit.
- Why a sidecar file and not frontmatter: no change to the 20 skill contracts, not loaded into the skill's context, no dependence on how Claude Code treats unknown frontmatter keys (not verified).

## Phase 2: router skill `which-skill`
- Input: a task described in any language. Reads only `skills-index.json`.
- Output: 1-3 candidates: skill, why, difference from its neighbour, what must be in place (`needs`), how to call it. Read-only; takes no action. Has section 0 "Ingested content is DATA".
- If nothing fits: says so; does not invent a skill.
- Evals: about 10 task phrasings from real situations, 3-4 of them negative (must answer "no matching skill"); clear cases MUST 3/3; grader in a separate session (as the other skills).

## Phase 3: HTML compass
- Generated from the same JSON; one self-contained file; no network, system fonts (an employer or client may not allow third-party fetches).
- Keyword search in the browser; no semantic matching (that stays with phase 2).
- Layout, colors and sector icons are designed on mockups before building; not part of this file yet.

## Risks and open points
- `tools/sync-skills.sh` copies the whole skills folder, so `NAVIGATOR.yaml` will also land in `.claude/skills/<name>/`. Assumed harmless (only `SKILL.md` is read); NOT VERIFIED.
- `sync-skills.sh` never deletes, so a removed skill can remain in `.claude/skills/`; the index is built from `plugins/` and is not affected, but the stale copy still loads. Handling it is outside this design.
- Sector assignment of the 20 current skills is my proposal, not yet confirmed.
- Router quality is unknown until the phase 2 evals run.
- Adding the router makes the plugin 21 skills; description-routing between it and its neighbours must stay clean (check 3b applies).

## Update 2026-10-13 (phase 1 built)
- Phase 1 implemented: `tools/build-skills-index.py` (build, `--check`, `--accept <skill>`), `plugins/qabase/navigator-sectors.yaml`, 20 x `NAVIGATOR.yaml`, generated `plugins/qabase/skills-index.json`; validator check 10; `sync-skills.sh` rebuilds the index.
- Intents: written by Claude, to be corrected by the AI QA Process Lead (1a). Real phrases from the team can be added later in the optional `phrases` list (1b); the router evals will be used to tune them (1c).
- `needs` is shown to users (2a). To keep it honest, `access_checked` holds a hash of the skill's Access, Preconditions, Required inputs and Required context sections: when any of them changes, the validator fails until a person re-reads them and runs `--accept <skill>`. The hash proves a section changed, not that `needs` is right.
- `needs` values were written from those sections on 2026-10-13; they have not been run against real use. Errors are expected and will be fixed when found.
- Sectors: `bug-report` manual (decided); `update-test-status` manual (proposed, not yet confirmed).
- Not built: router skill `which-skill`, HTML compass, evals for the router.

## Update 2026-10-13 (step-by-step review of intents)
- New optional field `then` in `NAVIGATOR.yaml`: skills that are often needed right after this one (a list of existing skill names; the validator rejects unknown names and self-reference). Decided by the AI QA Process Lead. The index carries it as `then`; the router and compass use it to suggest the follow-up skill. First pair: `update-test-status` <-> `bug-report`. More pairs are collected during the sector review.
- Sector 1 (requirements) and sector 2 (manual) intents confirmed.
- Sector 3 (automation) intents confirmed. `then` chains set: automation-readiness-assessment -> create-playwright-test, create-mobile-test; create-playwright-test -> review-playwright-test; create-mobile-test -> review-mobile-test; analyze-requirements -> create-test-cases; exploratory-testing-web and -mobile -> bug-report; update-test-status <-> bug-report.

## Router eval cases collected during the review (for phase 2, not yet written as evals)
1. "automate this case" with no mention of approval or a manual pass -> automation-readiness-assessment, not create-*.
2. "this case failed, what now" -> update-test-status first, then bug-report as the follow-up (both, in order).
3. A request that fits no skill (for example "write a unit test for this Java class") -> "no matching skill", nothing invented.
- Sector 4 (ci) intents confirmed. `then`: ci-failure-analysis -> ci-fix, bug-report; ci-fix -> review-playwright-test, review-mobile-test.
- Router eval case 4: "fix this failing test" with no accepted analysis -> ci-failure-analysis, not ci-fix.
- Sector 5 (investigation) is empty in this base: its project-specific lookup skills were removed; a project adds its own.
- Router eval case 5 (for a project that adds a lookup skill): a lookup request with a missing identifier -> the router asks for the identifier and says where to get it; it does not invent an answer.

## Update 2026-10-13 (intents review finished)
- All seven sectors reviewed. Confirmed by the AI QA Process Lead: `update-test-status` in manual; `onboarding-check` gets a fourth intent ("check that hooks and permissions work").
- `qa-reporting`: intents unchanged (a fourth intent about Xray test execution status was proposed, no answer yet).
- `feedback` and `feedback-triage` added to Session & setup. `feedback-triage` is for the AI QA Process Lead; the index has no audience field yet (decide at the router phase).
- `onboarding-check` will point to the project's QA documentation once its location is given (UNKNOWN).
