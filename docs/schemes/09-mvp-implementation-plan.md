# 09 MVP implementation plan — five stages

STATUS: WORKING DRAFT. Not final. This base has skills and humans at gates, no autonomous agents. Statuses are from the repo state, not from a run.

Source: an MVP implementation-plan slide (not included in this base). Statuses are the repo state on 2026-10-20.

```mermaid
flowchart LR
  S1["1 Project discovery - items open in context/discovery.md"] --> S2["2 Rules and context - written, hooks not active"]
  S2 --> S3["3 Core skills - written, evals NOT RUN"]
  S3 --> S4["4 Automation workflows - CI and runner UNKNOWN"]
  S4 --> S5["5 Pilot and learning - not started"]
  AO["Always on: human approval for consequential changes, AI output is not evidence, production restricted, no secrets or PII"]
  %% status colours: training/lessons/_design/README.md (always with the word on the node)
  classDef ok fill:#E4EDDD,stroke:#4E7A3A,color:#1E4A2E
  classDef draft fill:#F6E3B8,stroke:#E0A030,color:#231F1A
  classDef fail fill:#F3D9D1,stroke:#8A2A1A,color:#8A2A1A
  classDef off fill:#F9F3E5,stroke:#4A4339,stroke-dasharray:4 3,color:#4A4339
  classDef gate fill:#FFFBF0,stroke:#231F1A,stroke-width:3px,color:#231F1A
  class S3 draft
```

| Stage | Design says | This base | Evidence / gap |
|---|---|---|---|
| 1 Discovery | audit: CONFIRMED / TARGET / UNKNOWN / SEC GATE; source-of-truth matrix | `context/discovery.md`, all items open | no project repository or environment yet |
| 2 Rules and context | compact CLAUDE.md; rules QA, AI, Playwright, Security; `context/sources.md` | CLAUDE.md 98 lines, rules in `.claude/rules/` | hooks and deny rules inactive until `tools/apply-trusted-changes.sh` is run (not verified) |
| 3 Core skills | 5 core skills | written (plugin 0.1.0) | `evals/` NOT RUN in this base |
| 4 Automation workflows | sprint: readiness -> approval -> Claude + Playwright -> review -> PR -> CI; CI failure -> analysis; regression: readiness -> cleanup | skills exist; CI tool UNKNOWN; web and mobile projects not present | fill per project |
| 5 Pilot and learning | onboarding -> real sprint pilot; single feedback log; QA Lead review | `onboarding-check` written; `feedback/` stub | baseline before measurement (not taken) |

Metrics per slide: stage 3 output acceptance and major rewrite rate; stage 4 implementation time and pass / flaky rate; stage 5 baseline first, manual effort saved. No targets promised.
