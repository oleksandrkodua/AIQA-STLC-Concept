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

## The improvement loop: how the process itself changes

The flow above is one change to the product. This one is how a rule, skill, hook or eval of this
repository changes. Steps 1-4 and 8 exist today (`/feedback`, `/feedback-triage`, the approval model,
`evals/`). Audit and Learn have no skill of their own yet: audit is done by hooks, `evals/validate_repo.py`
and the run journal, learn by `knowledge/INTAKE.md`.

```mermaid
flowchart LR
  O[1 Observe: feedback entry] --> AN[2 Analyze: /feedback-triage groups entries]
  AN --> RC[3 Recommend: proposal with old and new text and a candidate eval]
  RC --> AP{4 Approve: QA Lead}
  AP -- reject --> O
  AP -- approve --> AC[5 Act: apply only that change]
  AC --> AU[6 Audit: hooks, validator, run journal]
  AU --> LE[7 Learn: knowledge intake]
  LE --> EV[8 Evaluate: evals]
  EV --> IM[9 Improve: next version]
  IM --> O
```

The same loop as a picture: [`docs/img/loop-map.svg`](../img/loop-map.svg), interactive version
[`docs/img/loop-map.html`](../img/loop-map.html). A person decides only at step 4; everything before it is a draft.
