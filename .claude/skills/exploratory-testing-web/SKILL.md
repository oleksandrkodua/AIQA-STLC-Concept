---
name: exploratory-testing-web
description: Plan and run a time-boxed exploratory testing session on the WEB shop (charter, heuristics, notes, findings) and hand defects to bug-report. Use when asked to explore, charter or session-test a web feature or flow. Not for the mobile apps (use exploratory-testing-mobile), not for scripted case execution, not for filing bugs (use bug-report).
---

# Exploratory Testing - Web

STATUS: SKELETON v0.0.1. Stage 4 of the plan (separate web and mobile skills).
Base material: `_base/exploratory-testing/` (account skill, unmodified copy). Shared method (charters, sessions, heuristics) is meant to live in one shared reference to avoid drift between the web and mobile skills; where that reference sits is OPEN (see Open items).

## 1. Purpose
Structure a human-led exploratory session on the web shop: a charter, a time box, heuristics, notes, findings. Claude helps plan and record; the tester explores and decides what is a defect.

## 2. Trigger
Explore / charter / session-test a web feature. Not: mobile, scripted execution, bug filing, requirement gaps.

## 3. Inputs
Required: charter or feature under test, build/environment (DEV), browser(s) and viewport(s) used, time box. Optional: requirement, design, risks, known defects.
Input checks: environment not DEV -> STOP. Missing browser/viewport -> ask; emulated viewport is labelled as such.

## 4. Access
Read only on supplied material. Writes: a session note file in `runs/` only. No Jira. No Chrome automation (the Claude Chrome plugin is not allowed at the client).

## 5-13.
Not yet written. Follow `_templates/SKILL-CONTRACT.md`. Steps to design: charter -> heuristics -> notes -> findings list (observed vs inferred) -> hand-off suggestions to `/bug-report` (human confirms).

## 12. Open items
- Where the shared exploratory method lives (shared reference vs duplicated text). - Browser/viewport matrix of the web shop (UNKNOWN). - Evals not written.
