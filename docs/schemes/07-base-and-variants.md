# 07 Base and variants — the reusable base

STATUS: WORKING DRAFT. Not the final diagram. One base, three layers. The base = CORE + PROJECT layer, with humans at every gate. An agent variant = the same base + the optional agent layer (`optional/agents/`). Nothing in the agent layer is enabled in this base (`policy/agents-policy.md`). Statuses in brackets are not verified.

## A. Layers (no agent layer by default; see D for the agent variant)

```mermaid
flowchart TB
  subgraph CORE[CORE - copied unchanged into every project]
    C1[CLAUDE.md skeleton + rules: qa, ai, security, web, mobile]
    C2[Skills with contract + evals: analyze-requirements, create-test-cases, automation-readiness, create/review web and mobile test, handoff, onboarding-check]
    C3[Hooks, Python, fail-open: deny_prod_and_secrets, protect_trusted_assets, qa_gate + permissions deny/ask as the floor]
    C4[Git pre-commit + validate_repo.py]
    C5[Process: decisions, proposals, conflicts, verification-log, evals, run journal]
    C6[Policy templates: AI usage, agents]
  end
  subgraph PROJ[PROJECT LAYER - rewritten per project]
    P1[context: sources, discovery, project-context, glossary]
    P2[automation registry, ci, prod-hosts list]
    P3[project-specific skills: lookups in the project's own systems, added when needed]
    P4[access + environment, approved MCP list]
    P5[project decisions in decisions/]
  end
  OPT[OPTIONAL user-level: mods, see optional/mods]
  OPT2[OPTIONAL agent layer: see optional/agents]
  CORE --> PROJ
  OPT -.not required.-> CORE
  OPT2 -.off by default.-> CORE
  %% status colours: training/lessons/_design/README.md (always with the word on the node)
  classDef ok fill:#E4EDDD,stroke:#4E7A3A,color:#1E4A2E
  classDef draft fill:#F6E3B8,stroke:#E0A030,color:#231F1A
  classDef fail fill:#F3D9D1,stroke:#8A2A1A,color:#8A2A1A
  classDef off fill:#F9F3E5,stroke:#4A4339,stroke-dasharray:4 3,color:#4A4339
  classDef gate fill:#FFFBF0,stroke:#231F1A,stroke-width:3px,color:#231F1A
  class OPT,OPT2 off
```

## B. MVP flow (humans at every gate, no agents)

```mermaid
flowchart LR
  R[Requirement] --> AR[analyze-requirements]
  AR --> BR{{Human approves brief}}
  BR --> TC[create-test-cases + AC trace]
  TC --> H1{{Human reviews cases}}
  H1 --> RD[automation-readiness]
  RD --> H2{{Human approves candidate}}
  H2 --> CT[create web / mobile test]
  CT --> RV[review test + weak-assertion check]
  RV --> H3{{Human reviews diff, merges}}
  H3 --> CI[CI: deterministic run, no AI]
  CI --> FA[ci-failure-analysis]
  FA --> H4{{Human decides: defect / test / env}}
  MT[Manual testing in parallel: functional, regression, exploratory, UI/UX] --> RD2{{Human: release decision}}
  H4 --> RD2
  RD2 --> FB[feedback log]
  FB --> H5{{AI QA Process Lead approves rule or skill change}}
```

## C. Full implementation (adds on top of MVP)

```mermaid
flowchart TB
  MVP[MVP flow B]
  MVP --> F1[feedback streams + learning inbox]
  MVP --> F2[API / DB test branch]
  MVP --> F3[reporting: qa-reporting, update-test-status, token tally]
  MVP --> F4[model change control, skill selection and governance tests]
  MVP --> F5[release QA, production signals, impact analysis]
  MVP --> F6[AI improvement loop: feedback, learning candidate, process lead validation, team knowledge, AI evaluation]
  F1 --> AG
  subgraph AG[Agent variant only - controlled autonomy]
    G1[QA intelligence agent: read-only, recommends]
    G2[change / impact watcher: later]
    G3[model behavior monitor: later]
    G4[kill switch + incident response]
  end
  G1 --> HG{{Human gate stays for write, external, production-adjacent actions}}
```

Source check: the stages and gates were compared with an architecture slide set (not included in this base). Its slide about tool roles (CLI / Desktop / VS Code, QA Lead / Middle / Junior duties, repository tree) is not drawn here.

## E. Agents in the full design -> what this base has instead (skills, human-triggered)

| Agent in the full design | This base | Note |
|---|---|---|
| QA Intelligence Agent (test health, failure patterns, release summary, recommendations) | skills `ci-failure-analysis`, `qa-reporting` | read and recommend; a human triggers and decides |
| Change / Impact Watcher | none; a project may add a repository-digest skill | manual only, never scheduled; the human asks |
| Model Behavior Monitor | none yet; `evals/` (skill selection, governance, injection) and the model/effort table | manual runs; no monitor |
| AI Evaluation (behavioral regression, acceptance tests) | `evals/` run by a person; grader in a separate session | not run yet |
| Sub-agents (`.claude/agents/`) | none | `policy/agents-policy.md`; off by default |
| Triggers, scheduled runs | none | every run starts from a person |

## D. What differs between the base and an agent variant

| Part | Base | Agent variant |
|---|---|---|
| Core | same | same |
| Project layer | template, filled per project | same |
| Agents | off; skills + human gates | allowed, per agent file, by maturity ladder (`optional/agents/`) |
| Critical actions (prod writes, privilege, governance) | never automatic | never automatic |
| Mods | optional, user level | optional, user level |
