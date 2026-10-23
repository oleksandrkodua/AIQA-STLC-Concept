# 05 Rollout — phases and exit checks

STATUS: DRAFT. No dates: the start depends on confirmation of the return (Discovery item 1).

```mermaid
flowchart LR
  P0[0 Discovery] --> P1[1 Foundation] --> P2[2 Pilot] --> P3[3 Baseline] --> P4[4 Expand]
  P0 -.exit.-> E0[answers in context/discovery.md; policy agreed]
  P1 -.exit.-> E1[settings activated; hook firing tests; skill evals 3x]
  P2 -.exit.-> E2[real stories, 2 engineers; review load measured]
  P3 -.exit.-> E3[baseline numbers recorded before any claim]
  P4 -.exit.-> E4[routines and agents only after their policy and audit]
```

| Phase | Work | Check that ends it |
|---|---|---|
| 0 Discovery | fill `context/discovery.md`, agree `policy/`, get repo access | every item answered with a source, or accepted as UNKNOWN by the owner of decisions |
| 1 Foundation | port web + Android, activate settings in a throwaway copy, run firing tests and skill evals | the open checks in `decisions/verification-log.md` PASS or recorded FAIL |
| 2 Pilot | use the loop on real stories | acceptance and rewrite rates recorded; review time per item recorded |
| 3 Baseline | measure before claiming anything | numbers exist |
| 4 Expand | routines, CI integration, agents, API automation | each passes policy, audit, acceptance tests |
