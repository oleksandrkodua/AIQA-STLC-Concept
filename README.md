# AIQA STLC Concept

An AI-assisted QA process across the software lifecycle: from requirements to release, with a human deciding at every gate. It is both a portfolio project (what I designed and what I verified) and a base that can be implemented on a real project after Discovery.

STATUS: DRAFT v0.1. Nothing here is approved by anyone. Labels used throughout: VERIFIED FACT / EVIDENCE-SUPPORTED INFERENCE / ASSUMPTION / UNKNOWN.

**Author:** Oleksandr Kukhtinov, Senior Manual QA Engineer (13 years), AI-assisted QA. [LinkedIn](https://linkedin.com/in/akukhtinov) · alexx9006@gmail.com
I am a manual QA engineer, not an automation engineer. Claude Code generated the tooling from my specification; I designed the QA logic and verified the results. Generated code is not evidence of automation expertise, and I do not list Selenium, Playwright or Appium as my skills.

## For a reviewer: five minutes

1. [`portfolio/`](portfolio/): the one-page summary and the 14-slide case study (anonymized: client, internal domains and channel names replaced).
2. [`CLAUDE.md`](CLAUDE.md) and [`.claude/rules/`](.claude/rules/): the working rules (evidence labels, verdicts, no production, human approval).
3. [`plugins/qabase/skills/`](plugins/qabase/skills/): the skills, each with written evals.
4. [`evals/`](evals/): how a skill, hook or agent is allowed to be called "working".

## Jira and test management: through skills

| Task | Skill | What it does | State |
|---|---|---|---|
| Bug ticket | `bug-report` | Builds a reproducible bug in the project's Jira fields, checks for duplicates, shows the draft. It creates the ticket through a Jira MCP connection only after the human confirms. | SKELETON v0.0.1. Evals written, NOT RUN. |
| Test cases | `create-test-cases` | Builds a coverage matrix from an approved requirement, designs the oracle separately, returns cases in the test management system's field structure for a human to review and save. | Evals written, NOT RUN. |

- VERIFIED FACT (files read 2026-10-23): no MCP server is connected in this repository (`.mcp.json` is empty), so nothing here talks to Jira or a test management system. The project's Jira fields and TMS structure are UNKNOWN until Discovery.
- VERIFIED FACT: the test-case skill only drafts; a person saves the cases. The bug skill is written to create one issue per human confirmation and to touch nothing else.
- In the earlier system described in the case study, creating test cases in the TMS was blocked by access (no API key) and creating bugs was blocked by a read-only connector. The author states that create and edit rights have since been granted (ASSUMPTION, not verified by a run). The skills still stop at a reviewed draft and a human confirmation, whatever the rights.

## The concept and worked examples

- [`docs/CONCEPT.md`](docs/CONCEPT.md): the stages, who decides, which skill helps, and what is proven.
- [`examples/demo-shop/`](examples/demo-shop/README.md): six worked stories (plus one optional) on a fictional e-commerce project. They are illustrations, not recorded runs; the one real piece is a dry run of the Xray script.
- [`training/materials/`](training/materials/model-harness-agent-glossary.md): example material for the course.

## How the lifecycle is covered

| Stage | Skill | State |
|---|---|---|
| Requirements | `analyze-requirements` | pilot |
| Test design | `create-test-cases` | draft, evals NOT RUN |
| Readiness for automation | `automation-readiness-assessment` | existing, evals NOT RUN |
| Automation (optional) | `create-playwright-test`, `review-playwright-test`, `create-mobile-test`, `review-mobile-test` | optional, mobile is DRAFT |
| Defects | `bug-report` | skeleton |
| Reports and CI | `qa-reporting`, `ci-failure-analysis`, `ci-fix` | skeleton, on hold |

## Map

| Path | What | State |
|---|---|---|
| `CLAUDE.md`, `.claude/rules/` | governance | DRAFT |
| `plugins/qabase/` | the plugin: skills with evals, contract template, hooks | DRAFT, evals NOT RUN |
| `.claude/hooks/`, `.claude/settings*.json` | hook scripts and settings | DRAFT, settings NOT ACTIVE |
| `evals/` | eval plan, hook tests, validator | partly runnable |
| `policy/` | AI usage and agents policy templates | DRAFT |
| `context/`, `knowledge/` | project context templates, intake process | TEMPLATE |
| `automation/`, `ci/` | registry stubs | OPTIONAL, empty |
| `runs/`, `feedback/`, `decisions/` | journal template, feedback loop, decision log | stubs |
| `optional/` | agent layer (off by default), user-level mods | OPTIONAL |
| `training/` | a short course on working with an AI assistant in QA | OPTIONAL, lesson 1 only |
| `examples/demo-shop/` | worked stories on a fictional shop | ILLUSTRATIVE, not recorded runs |
| `portfolio/` | one-pager and case study | see its README |

## What is proven, and what is not

- VERIFIED FACT: `python3 evals/validate_repo.py` gives 229 passed, 0 failed (run 2026-10-23, with the concept files). It checks the structure of the files, not whether the assistant behaves well.
- VERIFIED FACT: hook logic tests passed 20/20 and 9/9 (2026-10-07).
- NOT RUN: skill evals, hook firing tests in Claude Code, any CI.
- UNKNOWN: the real project's tracker, TMS, environments and access (`context/discovery.md`).

## Working from a cloud session

Open the repository in a Claude Code cloud session and use the skills there. Setup, the Jira/Xray environment (token as a network secret, never as a variable), the connection check and the limits are in [`docs/CLOUD-SESSION.md`](docs/CLOUD-SESSION.md). NOT RUN: no cloud session has been started against this repository yet.

## License

MIT, see [`LICENSE`](LICENSE): Copyright (c) 2026 Oleksandr Kukhtinov. Exceptions:
- [`portfolio/`](portfolio/NOTICE.md): personal materials, all rights reserved, for viewing.
- `plugins/qabase/_base/manual-tester/` and `plugins/qabase/_base/exploratory-testing/`: donor skills by other authors, each under its own MIT `LICENSE` kept in its folder.
- Embedded fonts in the lesson files (IBM Plex Sans) keep their own licence (SIL OFL).
Third-party notices: [`THIRD-PARTY-NOTICES.md`](THIRD-PARTY-NOTICES.md).
This is a statement of the author's intent, not legal advice.

## Implementing on a project

Start with `docs/GETTING-STARTED.md`, then fill `context/discovery.md`. The core (rules, skills, hooks, evals) is reused unchanged; the project layer is filled per project. Work only against DEV or another approved non-production environment.
