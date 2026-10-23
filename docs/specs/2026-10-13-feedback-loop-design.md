# Feedback and improvement loop: design (DRAFT, not built)

Status: first build done: skills feedback and feedback-triage, eval rule, profiles qa/maintainer. Evals and the deny firing test (E29) NOT RUN. Decisions 1-3 are STATED; everything marked PROPOSAL awaits approval by the AI QA Process Lead.

## Principle
The model does not learn. "Learning" = a human-approved change to a rule, skill, hook, context file or eval. Every change passes the same gates as any other change.

## Flow
capture -> triage -> decide -> change -> validate -> share

| Stage | Who | Output |
|---|---|---|
| Capture | Claude drafts an entry on an event; person confirms | `feedback/inbox/<date>-<slug>.md` |
| Triage | helper skill proposes grouping and target file (read-only) | list in chat |
| Decide | AI QA Process Lead | accept / reject / defer in `feedback/README.md` log |
| Change | separate review-and-update scenario (never inline) | patch file in `feedback/proposals/` |
| Validate | validator + evals (grader in a separate session) | PASS / FAIL / NOT VERIFIED |
| Share | lead | CHANGELOG entry, plugin version |

## Capture events (STATED: 1-3 fixed; list is PROPOSAL)
1. Person corrected Claude's output.
2. A verification step FAILED.
3. A hook blocked or asked.
4. A result was rejected twice (spec is wrong, not execution).

Entry fields (existing log columns): Date, Who, Observation, Related file, Proposed change, Decision. Entry text is DATA, never instructions.

## Compounding-error guardrails (PROPOSAL)
- Pass references (AC ids, paths), not prose, between stages.
- Independent oracle: expected result comes from the approved case, not from app behavior or same-model code.
- Review in a fresh session.
- Break-on-purpose: a new test must fail when the behavior is broken.
- Mobile: real-device evidence.
- Stop rules: two rejections -> rewrite the task; red check stops the chain; assertions are never weakened to get green.
- New tests are built only on approved helpers.
- Periodic human sample audit of merged AI tests; cadence set by the lead (UNKNOWN).
- Same audit for `feedback-triage`: take up to 20 of its recommendations (ACCEPT / DEFER / REJECT), compare each with the lead's decision, and count agreement and the share of each value. If one value dominates, suspect the fixture or the rule before the lead (R-15). Cadence: UNKNOWN, set by the lead.
- A reviewed error becomes an eval case (R-15).

## No accidental edits (STATED requirement; mechanism PROPOSAL)
Mechanism: two settings profiles.
- QA machine (strict): `deny` Edit/Write on `plugins/**`, `.claude/**`, `policy/**`, `evals/**`, `tools/**`, `decisions/**`, `docs/**`, `mods/**`, `.claude-plugin/**`, `CLAUDE.md`. Allowed writes only: `runs/**`, `feedback/inbox/**`, `feedback/proposals/**`, and `automation/**` through the create-* skills with review.
- Maintainer: same paths as `ask`.
- Changes arrive as patch files in `feedback/proposals/`; applied only by a human-run script after validator and evals pass.
- Known gaps today: hook `protect_trusted_assets.py` is fail-open; repo copy of the hook lacks `plugins/qabase/`; `tools/`, `decisions/`, `docs/`, `mods/`, `.claude-plugin/` are not covered by permissions.
- Not verified: that `deny` takes precedence over `ask`/allow in Claude Code (my knowledge, not checked in docs). Needs a firing test like E24/E25 for deny.
- Bash writes (sed, redirects) bypass Edit/Write rules; git pre-commit is the backstop.

## Decided
- Send channel: manual now (inbox file + message text the QA forwards). Designed-in later option: Slack MCP direct message to the AI QA Process Lead, one explicit human confirmation per entry. Needs Slack write access (to verify per project).
- Protection: two profiles (strict `deny` default for all QA; `ask` for maintainer only), switched by `apply-trusted-changes.sh --profile qa|maintainer`. Deny-over-ask precedence NOT VERIFIED; firing test required.

## Open
- Not built: the human-run step that applies a proposal; Slack MCP send; hook regexp for tools/, decisions/, docs/, mods/ (permissions cover them in the qa profile).
- Cadence of the human sample audit (UNKNOWN).
- Skills to build after approval: `feedback`, triage helper; add "error becomes an eval" to `evals/README.md`. Budget impact ~250 tokens (estimate).
