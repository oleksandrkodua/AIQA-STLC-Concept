# 02 Workflow — one change from requirement to CI, with gates

STATUS: DRAFT. "Gate" = a human decision or an automated check that must pass before moving on.

```mermaid
flowchart TD
  R[Requirement or change] --> A[/analyze-requirements/]
  A --> Q{Questions answered by product / BA?}
  Q -- no --> A
  Q -- yes --> T[/create-test-cases/]
  T --> RV{Human reviews each case}
  RV -- changes --> T
  RV -- ok --> TMS[Human saves cases in the TMS - tool UNKNOWN]
  TMS --> M[Manual run on DEV - evidence: build, env, device]
  M --> RD[/automation-readiness-assessment/]
  RD --> D{Recommendation}
  D -- keep manual / rework --> M
  D -- automate later --> BL[Backlog with named blocker]
  D -- automate now --> AP{Human approves candidate}
  AP -- no --> BL
  AP -- yes --> W{Target}
  W -- web --> CW[/create-playwright-test/]
  W -- mobile --> CM[/create-mobile-test/]
  CW --> RW[/review-playwright-test/]
  CM --> RM[/review-mobile-test/]
  RW & RM --> PR{Human reviews pull request}
  PR -- changes --> W
  PR -- merge --> CI[CI run on DEV]
  CI --> F{Failure?}
  F -- yes --> FA[Claude explains; human decides defect / test / environment]
  F -- no --> OK[Green - covers only what is asserted]
  FA --> FB[feedback log; QA Lead approves any rule or skill change]
  FA --> IL[Iron Law: defect gets a failing test first]
```

Checks attached to the gates: skill evals (layer 1) for every skill box; hooks for secrets,
production and trusted-asset edits on every tool call; run journal (`QA-RUN.md`) for
manual and regression runs; verification log for any claim the flow relies on.
