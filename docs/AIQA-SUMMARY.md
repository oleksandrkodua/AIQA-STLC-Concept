# AI-Assisted QA — what we are building, in two pages

> Note on this copy. Adapted for this base; the body is unchanged, only this note was added. Read it with these differences:
> - "QA Lead" in this repository means the AI QA Process Lead.
> - The base covers web (Playwright) and mobile (WebdriverIO + Appium), both optional, and has 18 skills, not five; the plugin is `qabase`.
> - One more human gate: the requirement brief is approved before test cases are drafted.
> - "About 700 regression cases" is a figure from an earlier project; NOT VERIFIED here.
> - Agents are off (`policy/agents-policy.md`).

This is the summary for people. The architecture document is written for the model; it is
thorough and long, and nobody should be onboarded from it.

## The idea in four sentences

AI speeds up QA reasoning: analyzing requirements, drafting test cases, judging what is worth
automating, drafting and reviewing Playwright code, explaining failures. Playwright executes
deterministically and runs without AI in the loop, so the day the AI is unavailable the tests
still run and the team still ships. Manual QA does not shrink — it moves earlier, where
judgement pays off most. Humans keep business intent, coverage decisions and the release
decision.

## What the AI actually touches

| Stage | AI | Human |
|---|---|---|
| Requirement | finds gaps, ambiguities, edge cases, testability problems | answers them, decides scope |
| Test cases | drafts in the TMS format | reviews each one, saves into the TMS |
| Automation decision | assesses risk, value, stability, testability | approves the candidate |
| Playwright code | drafts, verifies locators against a live app | reviews the diff, merges |
| CI failure | explains, correlates evidence | decides defect vs test problem vs environment |
| Learning | proposes rule and skill improvements | QA Lead approves before anything changes |

## Rules that never bend

- AI output is a draft, not evidence. Consequential decisions need verifiable sources.
- Nothing merges to `main` without a human review.
- Production access is prohibited; no secrets, no real customer data.
- No silent changes to rules, skills or approved context.
- No self-healing during a test run. A test either passes its assertions or fails visibly.
- Test cases live in the TMS. The repository holds a read-only export.

## Rollout

1. **Discovery.** What is confirmed, what is a target, what is unknown, what needs security
   sign-off. A source-of-truth matrix. No building yet.
2. **Foundation.** One repository: compact `CLAUDE.md`, four rule files, five skills, a
   self-contained Playwright project.
3. **Pilot.** Real stories in a real sprint, with two engineers. Not a demo.
4. **Baseline, then measurement.** Numbers without a baseline are marketing.
5. **Expand on evidence.** What repeats becomes a skill. What needs judgement stays human.

Agents, integrations, regression backlog automation and extended metrics come after the loop
works, not before.

## What we will measure

Acceptance of AI output and major rewrite rate; time to create a test case and to implement an
automated test; pass and flaky rates; escaped defects. And one that answers the sceptical
question directly: **do AI-drafted cases find defects as well as hand-written ones**, measured
by defect yield and maintenance cost. That comparison only works if every case records where it
came from, which is why provenance is set up on day one.

No target percentages are promised before the baseline exists.

## Honest risks

- **Unverified assumptions.** Several decisions depend on tooling behavior nobody has
  confirmed yet. They are tracked in a verification log, each with the experiment that settles
  it. The log is part of the deliverable, not a private note.
- **Nothing is proven without an environment.** Until there is an app to run against, the plan
  is a plan.
- **Review load.** Drafts arrive faster than people read them. If review becomes a rubber
  stamp, the whole model degrades into "AI writes, nobody checks".
- **Single point of approval.** The QA Lead gate is a strength and a bottleneck. It needs a
  deputy before the team grows.
- **Right to the letter, wrong for people.** An AI can produce a case or a text that is
  technically correct and still confuses a real person, for example midnight written as 00:00.
  Cases that depend on human understanding are tried by a person, not only run by a script.
- **Silent coverage loss.** A skipped test, a weakened assertion, a healed locator — each can
  quietly remove coverage. Explicit review rules exist for all three.

## What this is not

Not a replacement for testers. Not a promise of a percentage. Not full automation of the ~700
regression cases — that backlog is for rationalizing, not for mass conversion. Not an
autonomous agent making release decisions.
