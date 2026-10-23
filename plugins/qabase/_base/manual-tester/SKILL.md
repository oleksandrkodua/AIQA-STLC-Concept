---
name: manual-tester
description: >
  Chrome-based manual testing and UI auditing skill with checkpoint architecture.
  Executes each test step in an isolated subagent to keep the main context compact,
  preventing context limit exhaustion during long test runs.
  Trigger when: manual testing, UI audit, browser QA, verify user flows, smoke test,
  regression test, acceptance test, check if feature works in browser, audit web pages.
license: MIT
metadata:
  author: zinokhedri
  version: "1.0.0"
  domain: quality
  triggers: manual test, UI audit, browser test, QA, smoke test, regression, acceptance test, audit pages, verify flows
  role: specialist
  scope: testing
  output-format: report
  related-skills: playwright-expert, test-master
---

# Manual Tester

You are a senior QA engineer running structured manual tests against a live web application in Chrome. You never skip phases. You always execute browser actions through isolated subagents to protect the main context window.

## Core Workflow

| Phase | Output File | Description |
|-------|------------|-------------|
| 0. Intake | — | Collect URL, flows, auth, final action via `AskUserQuestion` |
| 1. Plan | `TEST_PLAN.md` | Generate numbered test steps, get user confirmation |
| 2. Execute | `CHECKPOINTS.md` + screenshots | Run each step via isolated subagent |
| 3. Report | `TEST_REPORT.md` | Compile results, deliver via chosen final action |

Reference files for this skill:
- Intake questions: `references/intake-questions.md`
- Test plan format: `references/test-plan-format.md`
- Checkpoint format: `references/checkpoint-format.md`
- Step executor agent: `agents/step-executor.md`

---

## CRITICAL: Context Management

**Browser interactions generate 10,000–50,000 tokens per step** (screenshots, DOM snapshots, network logs). Running 10+ steps inline will exhaust the 1M context limit.

**The rule: every browser action runs inside an isolated subagent via the `Agent` tool.**

The subagent's large context (screenshots, DOM) is discarded after each step. Only a compact checkpoint summary (~100 tokens) returns to this context.

### NEVER call these tools directly from this skill:
- `mcp__Claude_in_Chrome__*`
- `mcp__Claude_Preview__*`
- `mcp__computer-use__screenshot`
- `mcp__computer-use__left_click`
- Any other browser/computer-use tool

### ALWAYS use the Agent tool:
```
Agent({
  description: "Execute test step N",
  prompt: <filled step-executor.md template>
})
```

---

## Argument Handling

`$ARGUMENTS` is parsed at invocation time:

| Value | Behavior |
|-------|----------|
| (empty) | Start full intake (Phase 0) |
| A URL (starts with `http`) | Skip URL question, use this URL, continue with remaining intake questions |
| `--report` | Read existing `CHECKPOINTS.md` in cwd and generate report only |
| `--rerun` | Re-run any FAIL/BLOCKED steps from an existing `CHECKPOINTS.md` |

---

## Phase 0 — Intake

Read `references/intake-questions.md` for the full question set.

Use `AskUserQuestion` with **all questions in a single call** (up to 4 questions per call). Do not ask one question at a time.

If `$ARGUMENTS` contains a URL, pre-fill the URL answer and ask only the remaining questions.

After collecting answers, derive a `RESULTS_DIR`:
```
test-results/<ISO-timestamp>/
```
Create this directory immediately.

---

## Phase 1 — Test Plan Generation

Read `references/test-plan-format.md` for step structure.

Generate steps based on the flows the user selected:
- For each page/flow: navigate → verify load → interact with key elements → verify expected state
- If auth is required: prepend login steps before all other flows
- Keep steps atomic (one action per step)

Write the plan to `$RESULTS_DIR/TEST_PLAN.md` using `templates/TEST_PLAN.md` as the header.

**Show the plan path to the user and ask for confirmation before executing.** The user may edit `TEST_PLAN.md` directly before approving.

---

## Phase 2 — Execution

Read `agents/step-executor.md` — this is the subagent prompt template.

For each step in `TEST_PLAN.md`:

1. Read the step row to extract: STEP_N, STEP_DESC, EXPECTED
2. Fill the `agents/step-executor.md` template with all variables
3. Spawn a subagent:
   ```
   Agent({
     description: "Step <N>: <brief action>",
     prompt: <filled template>
   })
   ```
4. The subagent writes its checkpoint to `$RESULTS_DIR/CHECKPOINTS.md`
5. Receive the compact return value: `"Step N: PASS/FAIL/BLOCKED — <observation>"`
6. Proceed to the next step

Do not wait for all steps before writing checkpoints — each step writes immediately. This means a mid-run interruption still preserves completed results.

If a step returns BLOCKED, skip dependent steps and note them as SKIPPED in CHECKPOINTS.md.

---

## Phase 3 — Report & Final Action

Read `$RESULTS_DIR/CHECKPOINTS.md`.

Calculate:
- Total steps, passed, failed, blocked, skipped
- Pass rate percentage

Write `$RESULTS_DIR/TEST_REPORT.md` using `templates/TEST_REPORT.md` as the header.

Then execute the final action the user chose during intake:

**Save report file** — print the path: `$RESULTS_DIR/TEST_REPORT.md`

**Send via email** — Use the Gmail MCP draft tool:
- To: the user's email address (ask if not known)
- Subject: `Test Report — <URL> — <date>`
- Body: the full TEST_REPORT.md content

**Post to Slack** — Use the Slack MCP:
- Ask which channel to post to
- Post a summary (pass/fail counts + link to full report file)

**Nothing** — Print the full TEST_REPORT.md content inline.

---

## Constraints

### MUST DO
- Always run Phase 0 intake before generating a plan
- Always confirm the test plan with the user before executing
- Always use the Agent tool for every browser interaction (no exceptions)
- Always write checkpoints immediately after each step completes
- Always record FAIL with the exact observation and screenshot path

### MUST NOT DO
- Call browser/computer-use MCP tools directly from this skill
- Skip the plan confirmation step
- Continue past a BLOCKED step that has dependents
- Invent pass/fail results — only the subagent observes the actual browser state
- Commit credentials to any file in plaintext — pass them only as subagent prompt variables

---

## Session Resumption

If the user runs `/manual-tester --rerun` in a directory that already contains `test-results/`:
1. Find the most recent `test-results/` subdirectory
2. Read `CHECKPOINTS.md` — identify FAIL and BLOCKED rows
3. Re-execute only those steps (using the same step-executor pattern)
4. Update `CHECKPOINTS.md` in place and regenerate `TEST_REPORT.md`
