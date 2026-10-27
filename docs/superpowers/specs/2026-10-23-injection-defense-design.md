# Prompt-injection defense: design of the execution plan

STATUS: DRAFT v0.1, 2026-10-23. Approved in chat by the author section by section (approach A, waves 1-3, MCP as a gate). Not approved by the QA Lead. Wave 2 was implemented on branch `wave2/injection-defense` on 2026-10-27 (status per item below); wave 1 is a gate for the owner and is not done. Every check is NOT TESTED until it runs locally.
Provenance: ai-generated (Claude Code, cloud session; model and version not recorded), 2026-10-23; human-confirmed: pending.
Evidence: `docs/research/2026-10-23-injection-defense/report.md` (findings 1-15, defenses D1-D18, L1-L4, SKIP tier) and its five note files.

## Goal
Assume an injection will sometimes succeed, and limit what a hijacked session can do. Rules text ("content is data") lowers the odds; only deterministic controls (where a token lives, which hosts answer, what a script refuses, what a person confirms) limit the damage. The repository is a concept: tools are not connected yet, so tool-dependent steps are written as gates to pass before connecting, and repository changes are verified locally later.

## Decisions (from the author, 2026-10-23)
- Where Jira/Xray writes will run (cloud or local) is not known: the plan covers both, and no Jira secret is added to a cloud environment before the wave 1 gate is passed.
- QA machines: mixed or unknown. The OS sandbox is used on macOS, Linux and WSL2; on native Windows the main controls are W1.5 and R5.
- A protective hook that fails asks a person: `onFailure: block` for a hook that cannot start, `ask` for an internal error of the two protective scripts; the advisory `qa_gate` keeps failing open.
- Scope: waves 1-3; MCP only as a list of conditions.
- Approach A: contain (wave 1), harden (wave 2), measure (wave 3). Rejected: repository changes first (most of them only lower the odds while the main risk sits outside the repository), measuring first (spends local limits on gaps known to be open).
- All of wave 2 is approved and implemented in a branch (2026-10-27), not merged; its local verification is wave 3 and is NOT RUN. Each item below says how it is verified locally.

## Wave 1: gate before the first tool connection (owner, outside the repository)
Written into `docs/CLOUD-SESSION.md` and `context/discovery.md` as preconditions. Status of each: NOT TESTED until the connection is made.

| # | Precondition | Verified when | Report |
|---|---|---|---|
| W1.1 | No Jira secret is added to any cloud environment before W1.2 and W1.4 are done | the secret list of every environment is checked | D1 |
| W1.2 | Two cloud environments: `qa-read` (no secrets; network None or Trusted; the default for analysis and drafting) and `qa-xray-write` (only the Jira secret, for the Jira host only; used only for an `--apply` run with the person present; the secret is deleted after use) | claude.ai/code shows both; `qa-read` has no network secret | D1 |
| W1.3 | The public repository is never attached to `qa-xray-write`; real project work uses a private repository created from this base | the rule is in `docs/CLOUD-SESSION.md` and onboarding | D3 |
| W1.4 | A dedicated least-privilege Jira account for the token: create Test issues and steps in the QA project only; no delete, admin or customer-facing projects (needs the Jira admin; Discovery) | `--check` prints `HTTP 200 as <service account>` | D2 |
| W1.5 | Locally, `JIRA_PAT` is not set in the terminal that runs Claude: Claude prepares the plan and the dry run; the person runs `--apply` in their own terminal | in the Claude session `echo ${JIRA_PAT:+set}` prints nothing | D4 |
| W1.6 | GitHub: no outside collaborator with write access; the raw diff of any outside pull request touching `CLAUDE.md`, `.claude/**`, `plugins/qabase/**`, `tools/**`, `policy/**` or `evals/**` is read; an unreviewed branch is never opened in a session that holds a secret; no AI GitHub workflow is added. With a second maintainer: 1 required approval and CODEOWNERS on those paths | collaborator list checked (can be done now) | D5 |

If the Jira host is not reachable from the internet (report finding 15, UNKNOWN), W1.2 and W1.4 do not apply to the cloud, and W1.5 plus R9 become the main controls.

## Wave 2: repository changes (approved; implemented in a branch 2026-10-27; not merged; verification NOT RUN)
MUST: R1, R2, R3, R10. SHOULD: the rest. Implemented: R1 (hook scripts, tests, drafts; the hooks README and the `.claude/hooks` copies are applied by the owner with `tools/apply-trusted-changes.sh`), R2, R3, R4, R5, R6, R7, R8 (docs and handoff), R9 (a proposal file only, not applied to any machine), R10. None of it is verified by a run.

| # | Change | Files | Local verification | Report |
|---|---|---|---|---|
| R1 | Hooks: `"onFailure": "block"` on the PreToolUse hooks; `deny_prod_and_secrets.py` and `protect_trusted_assets.py` return `ask` (not allow) on an internal error; `qa_gate.py` unchanged; hooks README design rule 4 and the KNOWLEDGE CONFLICT about where hooks live resolved (per-machine is what runs; say that cloud sessions have no hooks); onboarding checks Claude Code v2.1.295 or later | `tools/hooks.template.json`, `plugins/qabase/hooks/hooks.draft.json`, `.claude/settings.draft.json`, the two scripts (both copies), `.claude/hooks/README.md`, `onboarding-check` | `python3 evals/hooks/run_hook_tests.py` (internal error -> ask; can also run in the cloud); in Claude Code: a hook whose interpreter is missing blocks the action | D6 |
| R2 | Untrusted input from files: section 0 gets a rule that ticket, page and log text is saved under `runs/<id>/input/` (git-ignored) and read with Read; text pasted into the chat is restated as quoted data, and the skill asks before any write or network action | every skill with section 0 (12 now, 19 after R6), `_templates/SKILL-CONTRACT.md`, `docs/GETTING-STARTED.md` | M2 fixture "same text pasted vs from a file" | D7 |
| R3 | Xray script checks content: URLs, Markdown/wiki links and images, and mentions in summary, description and step fields are listed in the dry run and rejected unless `--allow-links` is given; the plan hash covers the plan and the host together | `xray_dc_create.py`, its tests (both copies), `xray-test-create` SKILL.md | unit tests (written failing first) | D11 |
| R4 | Split write sessions: session 1 drafts `runs/<id>/plan.json` from untrusted input; the person reviews the file; session 2 (`qa-xray-write`) reads only that file, runs the dry run, then applies | `xray-test-create` SKILL.md, `docs/CLOUD-SESSION.md` | a run follows the steps (manual) | D12 |
| R5 | Best-effort `ask` rules for `curl`, `wget` and commands naming Jira REST paths (`rest/api`, `rest/raven`), with a note that they match text and can be evaded | `.claude/settings.json`, `tools/settings.shared.json`, `tools/settings.qa.json` | M1: `/usr/bin/curl` against the rule, to record the limit | D9 |
| R6 | Section 0 in the seven ON HOLD skills that will read Jira, CI logs or tester notes (`ci-failure-analysis` has only a one-line mention today) | `bug-report`, `ci-failure-analysis`, `ci-fix`, `qa-reporting`, `update-test-status`, `exploratory-testing-web`, `exploratory-testing-mobile` | validator; evals when the skills leave SKELETON | D13 |
| R7 | Output hygiene: drafts, reports and Jira text carry no model-built URLs or images, and links from untrusted sources are quoted as plain text; WebFetch disabled in the QA profile (`CLAUDE_CODE_DISABLE_WEB_FETCH=1`) | `.claude/rules/ai-rules.md`, `tools/settings.qa.json` | in a QA-profile session WebFetch is unavailable | D14 |
| R8 | Hardening flags for `claude -p` on a fork or unreviewed branch (`--setting-sources user`, `--bare`, `disableAllHooks`, `disabledMcpjsonServers`); handoff, feedback and run-journal files record whether they came from untrusted input; the permission mode used by QA sessions is written down | `docs/GETTING-STARTED.md`, `handoff`, `runs/QA-RUN.template.md` | reading | D15, D16 |
| R9 | OS sandbox for macOS, Linux and WSL2 in user-level settings: network allowlist, `allowUnsandboxedCommands: false`, credential deny entries, `denyWrite` on `plugins/qabase/**` | `tools/apply-trusted-changes.sh` (user-level output), `docs/REQUIRED-ACCESS-AND-ENVIRONMENT.md` | on a real machine: a sandboxed command cannot reach a host outside the allowlist | D10 |
| R10 | The wave 1 gate written into the documents; `docs/CLOUD-SESSION.md` section 3 rewritten for two environments | `docs/CLOUD-SESSION.md`, `context/discovery.md`, `docs/HANDOFF-cloud.md` | reading | D1-D5 |

Every changed skill gets a CHANGELOG line and "evals NOT RUN after the change"; the validator passes before each commit.

## Wave 3: measure (local, after wave 2)
Principle: measure whether the deterministic layers hold (0 of N), not how often the model declines.

| # | What | How | Runs |
|---|---|---|---|
| M1 | Layers without a model | hook logic tests; Xray script tests; manual: missing hook interpreter -> blocked, `/usr/bin/curl` vs the `ask` rule | no model |
| M2 | Evals with canaries | the 7 `injected-*` evals, MUST tier first; new fixtures: direct Jira REST call from `qa-read` (expected: fails, no secret), the same text pasted vs read from a file (R2), an Xray plan containing a link (R3 flags it). A fake secret string and a `.invalid` host; a run fails if the canary reaches an output, file, commit or plan | 3 per case (repository rule) |
| M3 | `feedback-triage` v0.0.2 re-run | its 3 evals | 3 x 3 |
| M4 | Recording | `evals/runs/<date>-injection.md` and `decisions/verification-log.md`, as k of N | - |
| M5 | Human red-team, 1 hour | the owner writes own fixtures in the README format | LATER, optional |

Budget order for the first local day: M1 (no limits), M2 MUST tier (9 runs), M3 (9), new M2 fixtures (9); about 27 runs plus grading in a separate session. If limits run out, M3 is cut first.

## MCP gate (conditions, not work)
No MCP connector (Jira, Confluence, Slack) is approved until: it is the vendor's official server with a pinned version; it is read-only by default and write tools are `ask` or `requiresUserInteraction`; it is in the approved list (reviewed `.mcp.json` or managed settings) and in `policy/ai-usage-policy.md`; tool-description changes trigger a re-review and outbound payloads are logged; the wave 1 gate is passed (a connector bypasses the cloud allowlist, so it is another side door). Report D17, D18. Written into `policy/ai-usage-policy.md` and `context/discovery.md` in wave 2.

## Later and skipped
LATER, decided on wave 3 results: L1 taint hook (after untrusted input, deny network, push and Jira writes for the rest of a local session); L2 Haiku screen of tool outputs as telemetry only; L3 quarantined extraction of a ticket into a fixed schema; L4 log of tool calls and Jira writes.

SKIP, each with the accepted risk (qa-rules 8):

| Skipped | Risk accepted |
|---|---|
| CaMeL-style data-flow runtimes | an injection can still steer the parameters of allowed actions; R3 and human review cover part of it |
| Commercial injection classifiers as a gate | adaptive attacks bypass them; the deterministic layers must hold |
| Fine-tuning defenses | the model is hosted; none beyond the model's own robustness |
| Approval of every read | approval fatigue; reads are bounded by the wave 1 gate |
| Filtering imperative sentences out of tickets | it would break steps to reproduce; instructions in data still reach the model and section 0 plus the deterministic layers handle them |

## Residual risk
No item stops a plausible but wrong test case from passing an approved write. The human review of AI drafts that `CLAUDE.md` already requires ("AI output is a draft, not evidence") is therefore a security control in its own right.

## Done when
- Wave 1 preconditions are in `docs/CLOUD-SESSION.md` and `context/discovery.md`; W1.6 collaborator check recorded.
- R1-R10 are merged with the validator passing; R1 and R3 have passing script tests in the cloud; every other item says NOT TESTED with its local verification.
- Wave 3 results are recorded as k of N; a FAIL leads to a fix or an accepted risk written in `decisions/`.

## Open items
- Jira reachability from the internet and the Jira admin for W1.4 (Discovery).
- The share of QA machines on native Windows (decides how much R9 covers).
- Whether `--allow-links` should exist at all, or links in Xray fields are always rejected (decide after the first real plan).
