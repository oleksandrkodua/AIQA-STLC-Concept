---
name: automation-readiness-assessment
description: Assess whether a test case should be automated now, later, or stay manual, for web or mobile, and say why. Weighs repeat value, risk, stability of the feature, testability, oracle clarity, data and device needs, and maintenance cost, and requires the case to have passed a manual run first. Use whenever someone asks "should we automate this", "is this case worth automating", "what goes into the regression suite", or reviews a regression backlog, even if they never say "readiness". Also for Ukrainian or Russian phrasing such as "чи автоматизувати цей кейс" or "что автоматизировать в регрессии". Not for writing the automated test (use create-playwright-test or create-mobile-test) and not for writing cases (use create-test-cases).
---

# Automation Readiness Assessment

STATUS: DRAFT written on 2026-10-07 from the internal design notes (§9 catalog, §10 triggers) and the
operating rules of this repository. No source SKILL.md was available. Not run.

## 1. Purpose

Decide, per case, whether automation pays off now. The output is a recommendation with
reasons for a human to approve. It never decides alone and never promises a percentage of
automation.

## 2. Trigger

- a new or changed test case;
- a regression backlog candidate or a release candidate review;
- explicit invocation: `/automation-readiness-assessment <case id or path>`.

Negative triggers: do not write the test, do not write cases, do not judge the product.

## 3. Required inputs

- the test case in full (title, preconditions, steps, expected result, oracle);
- evidence that the case passed a manual run: who, when, build, environment. Without it the
  verdict is NOT READY: run it manually first.
- target: `web` or `mobile` (platform: Android / iOS).

## 4. Optional inputs

- defect history for the area; frequency of the flow in releases; owner of the feature;
- stability of the UI/feature (is it about to change?);
- existing automated coverage (to avoid duplicates).

## 5. Required context

- `.claude/rules/qa-rules.md`, `.claude/rules/ai-rules.md`;
- `CLAUDE.md` automation registry; `rules/mobile-rules.md` when target is mobile;
- `context/sources.md` for which source is authoritative for the oracle.

## 6. Preconditions

- the case has an expected result and an oracle. A case with neither is sent back, never
  guessed.

## 7. Steps

1. Check preconditions. Missing manual-pass evidence or oracle → verdict REWORK / NOT READY
   and stop with what is needed.
2. Rate each criterion in step 8 as HIGH / MEDIUM / LOW / UNKNOWN, quoting the fact it rests
   on. UNKNOWN is allowed and counts against automating now.
3. Apply the decision logic in step 9.
4. State the cost you cannot see: data setup, devices, accounts, flakiness sources.
5. Produce the output in step 10.

## 8. Criteria

- **Repeat value**: how often the flow runs (every release, every build, rarely).
- **Risk**: what breaks for the user and the business if this fails.
- **Stability**: is the feature or UI settled, or about to change.
- **Testability**: stable locators or ids, controllable preconditions, observable result.
- **Oracle**: the expected result is exact and comes from an approved source.
- **Data**: synthetic data can be created and cleaned; no real customer data.
- **Environment and devices**: needs only DEV; no real device, biometrics, camera, push,
  payment provider or third-party webview that automation cannot control.
- **Determinism**: known flakiness sources (animations, network, third-party content).
- **Maintenance cost**: how many places break when the UI changes.
- **Human understanding**: depends on wording, visual clarity or judgement → keep manual.

## 9. Decision logic

- AUTOMATE NOW: repeat value and risk at least MEDIUM, stable, testable, exact oracle,
  manual pass evidenced, no UNKNOWN on oracle or testability.
- AUTOMATE LATER: valuable but blocked (feature changing, no stable locator, no test
  data). Name the blocker and who removes it.
- KEEP MANUAL: needs human judgement, a real device capability, or low repeat value.
- REWORK CASE: oracle or expected result missing or ambiguous; return to the case owner.

Mobile note: an emulator run does not prove a device flow. If the case depends on hardware
behavior, the recommendation includes a device check, not only an automated run.

## 10. Outputs

```
CASE: <id / title>      TARGET: web | mobile (android | ios)
MANUAL PASS: <who, when, build, environment> | NOT EVIDENCED
RECOMMENDATION: AUTOMATE NOW | AUTOMATE LATER | KEEP MANUAL | REWORK CASE

CRITERIA
- <criterion>: HIGH | MEDIUM | LOW | UNKNOWN — <fact it rests on>

BLOCKERS / UNKNOWNS
- <item> → <who can resolve it>

COST I CANNOT SEE
- <item>

NEXT STEP: <one line; for AUTOMATE NOW: human approval, then create-playwright-test or create-mobile-test>
PROVENANCE: source case, model and version, this skill, date; status ai-generated
```

## 11. Checkpoints and approval

A human approves every AUTOMATE NOW. Nothing starts automatically. Approver name and date are
recorded on the case.

## 12. Failure and uncertainty handling

- Case incomplete → REWORK CASE, list what is missing.
- Tempted to estimate frequency or stability from the title → mark UNKNOWN.
- Never invent defect history, priorities or release plans.

## 13. Tools

Read-only on the supplied case and approved context.

## 14. Non-goals

Does not write tests, does not estimate effort in hours, does not rank the whole backlog by
a made-up score, does not decide release readiness.
