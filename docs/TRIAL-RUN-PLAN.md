# Trial Run Plan — unblocking B1

> Note on this copy. Taken from an earlier architecture project; the body is unchanged. V-numbers are ids of that project's verification log (not included in this base); "Section N" refers to its architecture document. The Playwright baseline here is 1.62.1. Nothing in this plan has been run.

**Purpose.** B1 (no app or test environment) blocks V1, V2, V12, V18, V19, V20, V21. None of
them need the client's application. Any public demo application is enough, because every one
of these claims is about tooling behavior, not about the product under test.

**Time.** Half a day, most of it waiting for installs.

**Output.** Each claim moves to PASS or FAIL in `verification-log.md`, with the command and
the observed result written next to it.

---

## Setup

Pick any public demo app that allows automated testing — Playwright's own demo shop, a public
sandbox of a tool you already use, or a local container. Record which one you used; the result
is only meaningful if the reader knows what was tested against.

```bash
mkdir -p ~/dev/trial/playwright && cd ~/dev/trial/playwright
npm init playwright@latest        # accept TypeScript, tests/, no GitHub Actions
git init ..                       # repo root one level up, mirroring qa-ai/
```

**Check.** `npx playwright test` runs the example test. If it does not, stop — nothing below
is meaningful until it does.

---

## V8 — is `--loop=claude` a real value

```bash
npx playwright init-agents --help
```

Record the accepted values verbatim. This one needs no app and no browser; do it first.

- PASS: `claude` appears in the accepted values.
- FAIL: it does not — the guide's setup command must change.

---

## V19 — can agent artifacts live in a subfolder

Run `init-agents` with whatever loop value V8 established, then:

```bash
git status --porcelain
```

Record exactly which paths were created: `.claude/agents/`, `specs/`, `tests/`, `.mcp.json`,
`seed.spec.ts`. Note whether any of them are configurable.

- PASS: `specs/` and `tests/` can be pointed inside `playwright/`.
- FAIL: they are fixed at repository root — section 37 of the architecture needs a decision,
  either accept root artifacts or wrap them.

---

## V2 — does re-running `init-agents` overwrite the seed

```bash
echo "// project setup marker" >> tests/seed.spec.ts
npx playwright init-agents <same args>
git diff tests/seed.spec.ts
```

- PASS: the marker survives.
- FAIL: it is wiped — project setup must not live in the seed, and the guide must say so.

---

## V1 and V20 — do project conventions reach the agent

Put one unmistakable rule where each claim expects it:

- V1: in `CLAUDE.md`, or in the file it references.
- V20: in `.claude/rules/playwright-rules.md`.

Use a rule whose violation is obvious at a glance, for example: *every generated test file is
named `zz-<name>.spec.ts`*. Use a **different** marker for each file so the results cannot be
confused.

Run the generator on one simple case. Inspect the produced file name.

- PASS: the rule was followed. Record which file the rule came from.
- FAIL: it was not — project corrections do not reach the agent, and the review skill becomes
  the only line of defence. Say so in the log; it changes how much the generator can be
  trusted.

---

## V18 — does the generator accept our own test-case format

**This is the one that matters most.** The MVP decision to use the generator behind
`create-playwright-test` depends on it.

Write one test case by hand in the neutral format from `create-test-cases` — Title,
Preconditions, Steps, Expected, Priority — for a flow the demo app supports. Feed it to the
generator without involving the planner.

- PASS: it produces a test that matches the case. Note how closely the steps were followed.
- FAIL: it needs planner output or a specific structure. Record what it expected. The MVP then
  keeps its own generation path, exactly as section 45 already allows for.

---

## V12 — does the healer validate across all browser projects

```bash
# confirm the config has chromium, firefox, webkit (this also settles V13)
npx playwright test          # green baseline across all projects
```

Break one locator deliberately, run the healer, then:

```bash
npx playwright test          # all projects, not just one
```

- PASS: the healed test passes everywhere.
- FAIL: it passes in one engine only — the healer's output must never be merged without a full
  cross-browser run, and that becomes a rule, not a habit.

Also record what the healer does when it cannot fix the test: does it mark it skipped, and how
visible is that in the output.

---

## V21 — do hooks fire inside an agent

Add a `PreToolUse` deny hook at project scope for an obviously forbidden target — a domain the
test must never reach. Run the generator and try to make it touch that target.

- PASS: the call is denied, and the denial is visible.
- FAIL: the hook does not fire inside the subagent — every boundary in section 19 that relies
  on hooks stops covering agents, and permissions become the only floor.

---

## V33 — does a committed test beat an agent-driven session for a repeated flow

This is the central claim of the architecture, and it has not been measured. Do it last: it
needs the earlier steps to have worked, and it takes the longest.

**The claim.** For a flow that is repeated many times, a committed deterministic test costs less
per run and is at least as reliable as an agent driving a browser session.

**Three modes, one flow.**

- **A. Agent, one call per action.** The agent explores and acts through browser tools, one call
  per step.
- **B. Agent, two tiers.** The agent explores one call per action, then puts the known steps into
  one script and runs it, then checks the outcome.
- **C. Committed test.** The same flow written once as a Playwright test through
  `create-playwright-test`, and run by Playwright with no model in the loop.

**Before any run, write down (in `verification-log.md`, row V33):**

- the flow: one flow on the demo app with a clear observable outcome, for example an item added
  to the cart and the total showing a value you know in advance;
- the success criterion, exactly as it will be checked;
- what counts as an *error*: a tool call that returns an error, or a run that ends without the
  criterion met;
- what counts as PASS, FAIL and INCONCLUSIVE (below).

**Runs.** Five runs per mode, each from the same starting state. Keep the same model. Record the
model, the effort level (V30), the Playwright version and the date.

**What to record for every run.**

| Metric | How |
|---|---|
| tool calls | count them, mode A and B only; mode C has none |
| errors | as defined above |
| elapsed time | wall clock from start to verdict |
| tokens | the harness's own usage data or a hook that records it. **Not** a character count. Name the source you used (V31). If none is available, write `NOT MEASURED` |
| verdict correct? | after every agent run, check the real outcome independently, by a person or a scripted check, and record whether the agent's verdict matched. This is the false-pass count |

**Authoring cost, once.** Record the time and tokens spent writing and reviewing the committed
test in mode C. Then the break-even is: authoring cost divided by the per-run cost of mode B. A
committed test pays for itself from the run whose number is that quotient.

**Result.**

- PASS: over five runs, mode C has a lower median elapsed time than mode B, and at least as few
  errors, and no false pass, and mode C uses no model tokens per run.
- FAIL: mode C is slower than mode B, or has more errors.
- INCONCLUSIVE: fewer than four of five runs completed in any mode because of a setup problem
  (the demo app was down, a dependency would not install); or tokens could not be measured, in
  which case report calls and time and mark tokens `NOT MEASURED`. Never turn a broken setup into
  a FAIL.

**Limits to write next to the result.** One flow, one application, five runs per mode. It
supports the claim for that flow only, and a difference of a few percent means nothing at this
sample size. Do not put a percentage on a slide without saying so.

**If it comes out the other way** (the agent is cheaper or more reliable), that is the useful
outcome: it tells you where the deterministic-first rule in sections 31A and 38 should be
relaxed, and for which kind of flow.

---

## Recording the results

For each claim write into `verification-log.md`: the command, the observed result in one line,
the date, and the Playwright version (`npx playwright --version`). Version matters: agent
definitions are regenerated on Playwright updates, so a PASS is a PASS for that version. Name
the conditions too (the demo app, the browser projects): one run under one set of conditions
supports the claim only within them.

Write down what counts as PASS and what counts as FAIL **before** running each experiment.

If something stops the experiment from running (the demo app is down, a dependency will not
install, access is missing), the status is `INCONCLUSIVE` with the missing prerequisite named.
Never turn a broken setup into a FAIL about the tool: that would change a decision on evidence
that does not exist.

Claims that come back FAIL are not failures of the plan — they are the plan working. Each one
that turns FAIL saves a decision made on a wrong assumption.
