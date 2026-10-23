# Alignment with the ten pieces of advice in register entry R-10

STATUS: DRAFT, 2026-10-23. A gap list, not a decision. Nothing here changes a rule, a skill or a hook; every "move" is a proposal for the QA Lead (trusted assets).

Source of the advice: the conference talk in `knowledge/register.md` R-10 (a 74-slide deck on avoiding low-quality AI output; speaker not named). Its slide text is CLAIMS of one speaker, unverified (`knowledge/INTAKE.md`: one source is one opinion). The "ours today" column was re-checked against this repository on 2026-10-23 and replaces an earlier version that had gone stale.

Status: MATCH / PARTIAL / GAP.

| # | Advice (paraphrased) | Ours today (checked 2026-10-23) | Status | Proposed move |
|---|---|---|---|---|
| 01 | Check the harness first | Permission floor is active in `.claude/settings.json`; hook scripts exist in `.claude/hooks/`; hooks are registered per machine (`tools/hooks.template.json`, `tools/apply-trusted-changes.sh`); hook firing tests NOT RUN (`evals/hooks-firing.md`) | PARTIAL | run the firing tests; later count tools and instructions per skill |
| 02 | Choose model and effort per task | `docs/MODEL-AND-EFFORT.md` is a proposal table, not yet in any `SKILL.md` frontmatter; `plugins/qabase/_templates/SKILL-CONTRACT.md` has no model or effort line | PARTIAL | add the values to frontmatter after each skill's evals pass (the document's own rule) |
| 03 | Keep the context clean (plan, clear, implement; sub-agent summaries) | `ai-rules.md` 15-16: plan in files, handoff by file; thresholds not adopted until measured; sub-agents off; a `handoff` skill exists | PARTIAL | record `/context` at the start and end of a pilot run before adopting any threshold |
| 04 | Treat instruction files as code: short, path-scoped, human-written | `CLAUDE.md` under 100 lines is checked by `evals/validate_repo.py`; two rules are path-scoped (`paths:` in `playwright-rules.md`, `mobile-rules.md`); change control by approval. **Mismatch:** `CLAUDE.md` and the rules were drafted by an assistant | PARTIAL | the QA Lead rewrites or explicitly adopts each rule in their own words |
| 05 | Procedures in skills, prohibitions in code | Skill contract (13 sections), permission floor, hooks; "hooks fail open" is stated | MATCH | none, apart from finishing hook activation (01) |
| 06 | Brief first, then code | `analyze-requirements` writes a brief from `references/brief-template.md` (status DRAFT until approved); no structured interview step | PARTIAL | add a questioning step before the brief |
| 07 | Acceptance criteria beyond the happy path, with traceability | `qa-rules.md` 15; `create-test-cases` carries `Covers: AC-id` and a matrix check; `review-playwright-test` checks `@AC-` tags | MATCH | none; keep checking in the evals |
| 08 | Check every step; gates leave artifacts | `docs/schemes/02-workflow.md` gates, `runs/QA-RUN.template.md`, `decisions/verification-log.md` | MATCH | none |
| 09 | Test the tests | `evals/sabotage-matrix.md` (deliberate breakage, see whether the suite goes red): NOT RUN | PARTIAL | run it on a test build; it is the equivalent of mutation testing for end-to-end suites |
| 10 | Human last, after lint, tests and agent review; Iron Law | Iron Law = `qa-rules.md` 13; human gates exist; no agent-review step (agents are off); the advice "human last" must not weaken "nothing merges without review" | PARTIAL | keep human review mandatory; add a read-only reviewer only when agents are enabled (`policy/agents-policy.md`) |

## Reading of the pipeline (inference)

The talk's pipeline is: interview, acceptance criteria, plan, code, tests, agent review, QA, human. Ours is: analyze, cases, human review, TMS, manual run, readiness, automate, review, pull request, CI. Differences: no explicit interview or plan node (06 above), and manual QA comes before automation here (`qa-rules.md` 14). Keep the order; consider the first two nodes.

Where the speaker's own first step points (04, 06, 07), our gaps are 04 and 06; 07 is covered.

## Skill candidates named in the same analysis (deferred)

The author decided on 2026-10-13 to defer adopting any of them. None is downloaded; licences and quality are NOT CHECKED. Names only: `grill-with-docs` (a questioning step for the brief; the file seen was a pointer), `qa-requirement-reviewer`, `verification-before-completion`, `systematic-debugging`, `diagnosing-bugs`, `triage`, `test-blindspots`, `ai-qa-review`, `assumption-test`, `eval-audit`, `release-readiness` (later), `ai-system-testing` (later), `qa-methodology` (reference only).

Not taken, with the reason: an observability-driven testing skill (needs production telemetry; production is prohibited); a sprint-report skill that needs a specific test-management MCP; cloud-platform skills; an embedded-systems set (wrong domain). Kits that bring their own commands and hooks are not installed.

Provenance: ai-generated from an earlier analysis and re-checked against the repository, Sonnet 5.5, 2026-10-23; human-confirmed: pending.
