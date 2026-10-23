# 10 Tooling and team roles

STATUS: WORKING DRAFT. Not final. This base has skills and humans at gates, no autonomous agents. Statuses are from the repo state, not from a run.

Source: an architecture slide about tools and roles (not included in this base). Roles of Middle and Junior QA come from that design; for a project the team roles are UNKNOWN until Discovery.

```mermaid
flowchart TB
  subgraph T[Surfaces]
    CLI["Claude Code CLI: execution, CI, quick terminal work"]
    DSK["Claude Desktop: analysis, output is a decision, not a file"]
    VSC["VS Code + Claude plugin: everything that ends in a diff and a commit"]
  end
  subgraph M[Desktop modes]
    CODE["Code / Projects: main loop, bound to the project folder"]
    COW["Cowork: joint debugging of complex failures"]
    CHAT["Chat: brainstorming only, no file risk"]
  end
  subgraph R[Roles]
    PL["AI QA Process Lead: owns CLAUDE.md, base rules, skills, hooks"]
    TM["Team members: roles UNKNOWN until Discovery"]
  end
  DSK --> CODE
  DSK --> COW
  DSK --> CHAT
  RT["Routine: Desktop or VS Code -> request a skill -> review draft -> edit code -> pull request -> process lead review"]
```

Open for a project: does Desktop Code read `.claude/` like the CLI; is VS Code allowed on the employer's or client's machines; who reviews pull requests (team AQA or SDET, not confirmed). The repository tree on the slide (`qa-ai/`, `playwright/`) differs from this base (`automation/web`, `automation/mobile`).
