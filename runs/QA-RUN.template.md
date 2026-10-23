# QA RUN: <project / scope>, <date>

<!-- Format from an earlier QA agent setup (template). Checked by .claude/hooks/qa_run_check.py -->

## Why this run exists
<one paragraph: the request, what is at stake, who asked>

## Build fingerprint
Environment: <DEV | other approved> · Platform: <web | android | ios> · Device: <EMULATOR name | DEVICE model>
Build: <version / build number / install source> · Feature flags: <list | UNKNOWN>

## Plan
Depth: <LIGHT | STANDARD | DEEP>

**MUST:** <items, each with a reason>
**SHOULD:** <items>
**Deliberately NOT run:** <non-empty list; for each, the risk accepted>

## Log
<!-- one line per step: - HH:MM | action | outcome -->
- 00:00 | <action> | <outcome>

## Findings
<each: Finding / Evidence (quoted) / Risk / Confidence / Recommendation>

## RECONCILE
| Item | Result |
|---|---|
| <MUST item> | DONE | CARRIED OVER — <why> |

## QA VERDICT — <scope>, <date>
Status: READY | READY WITH RISKS | NOT READY | BLOCKED
Confidence: HIGH | MEDIUM | LOW (derived, see qa-rules 6)
Areas: Requirements / Functional / Validation / API-Network / Regression: PASS | FAIL | NOT TESTED | NOT APPLICABLE | BLOCKED | UNKNOWN

What limited this verdict: <caps hit, tools unavailable, categories untested, emulator-only>

## Limits (final)
Skills used: 0/6 · Re-runs: 0/2 · No-new-finding streak: 0/3
