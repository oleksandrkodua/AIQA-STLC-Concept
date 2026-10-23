# Model and effort per skill

STATUS: a proposal table. NOT yet in any SKILL.md frontmatter:
they are added after each skill's evals pass (see rule below). Values are an ASSUMPTION, tuned on the pilot.

Mechanism (Claude Code docs, one source: code.claude.com/docs/en/skills): SKILL.md frontmatter `model`
(same values as /model, or `inherit`; applies to the current turn only) and `effort` (low, medium, high,
xhigh, max). An organisation allowlist can silently block a model; the session model then stays. So every
output's provenance line records the model that actually ran.

| Class | Skills | Model | Effort |
|---|---|---|---|
| Analysis and judgement | analyze-requirements, automation-readiness-assessment, review-playwright-test, review-mobile-test | strong | high |
| Generation | create-test-cases, create-playwright-test, create-mobile-test, bug-report, ci-failure-analysis, ci-fix, handoff | middle | medium |
| Lookup and checklists | onboarding-check | cheap | low |
| Not decided (skeleton, on hold) | exploratory-testing-web/-mobile, update-test-status, qa-reporting | decide when built | |

Rule: a skill moves to a cheaper model only if its evals pass 3/3 (MUST) on that model, graded in a
separate session. A skill that fails on the cheaper model stays on the stronger one.
Extended thinking (source: a course checkpoint, one third-party source; not checked against API docs):
- bulk, one-word-answer work (labelling many items): leave thinking off, it multiplies output cost with no accuracy gain;
- dependent multi-step planning (each step needs the previous result): turn it on and budget for the planning step;
- never edit, summarise or strip thinking blocks from a conversation history: the signature fails and the next request is rejected. This concerns code on the API or Agent SDK, not Claude Code skills; manage context with `/clear` and handoff instead.

Check without expertise: open a skill output; its provenance line names the model. After frontmatter is
added: `grep -n "^model:\|^effort:" plugins/qabase/skills/*/SKILL.md`.
