# 01 Architecture — layers and who owns what

STATUS: DRAFT scheme of the proposed design. Solid arrows = decided in this repo draft;
labels in brackets = status.

```mermaid
flowchart TB
  subgraph H[Humans]
    QA[QA engineer - reviews, runs manual passes]
    QL[QA Lead - approves rules, skills, hooks]
    CL[Client - agrees AI policy, owns environments]
  end
  subgraph S[Surfaces]
    DSK[Claude Desktop - analysis]
    VSC[VS Code extension - commits, code]
    CLI[CLI - unattended runs, CI]
  end
  subgraph G[Governance layer]
    CM[CLAUDE.md - always loaded]
    RU[rules - qa, ai, security, web, mobile]
    PM[permissions deny/ask - the floor]
    HK[hooks - PreToolUse, PostToolUse]
    PO[policy - AI usage, agents]
  end
  subgraph K[Skills]
    SK1[analyze-requirements]
    SK2[create-test-cases]
    SK3[automation-readiness]
    SK4[create / review web test]
    SK5[create / review mobile test]
  end
  subgraph C[Context]
    CX[context - sources, discovery, project-context]
    KN[knowledge - intake of outside material]
  end
  subgraph X[Deterministic execution - no AI in the loop]
    WEB[automation/web - Playwright]
    MOB[automation/mobile - WDIO + Appium: android, ios scaffold]
    API[automation/api - NEXT]
  end
  ENV[(DEV / approved test env)]
  CI[CI - tool UNKNOWN]
  EV[evals - skills, hooks, governance, injection]

  QA --> DSK & VSC
  QL -->|approves changes| G
  CL -->|agrees| PO
  DSK & VSC & CLI --> G
  G --> K
  C --> K
  K -->|drafts| QA
  QA -->|approves candidates| WEB & MOB
  WEB & MOB --> ENV
  CI --> WEB & MOB
  EV -.tests.-> G
  EV -.tests.-> K
```

Reading it: AI works in the top half and produces drafts; humans approve; the bottom half
runs without AI. The governance layer sits between every surface and every skill.
