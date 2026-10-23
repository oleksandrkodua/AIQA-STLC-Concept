---
name: exploratory-testing-mobile
description: Plan and run a time-boxed exploratory testing session on the iOS and Android apps (charter, heuristics, device and build identity, notes, findings) and hand defects to bug-report. Use when asked to explore, charter or session-test a mobile app feature. Not for the web shop (use exploratory-testing-web), not for scripted case execution, not for filing bugs (use bug-report).
---

# Exploratory Testing - Mobile

STATUS: SKELETON v0.0.1. Stage 4 of the plan.
Base material: `_base/exploratory-testing/`. Mobile specifics to add: device/OS/build identity, real device vs emulator, permissions, interruptions (calls, notifications, background/foreground), network changes, gestures, orientation.

## 1. Purpose
As in the web skill, for the iOS and Android apps. Evidence must say which device or emulator produced it (an emulator is not a real device).

## 2. Trigger
Explore / charter / session-test a mobile feature. Not: web, scripted execution, bug filing.

## 3. Inputs
Required: charter, platform (iOS/Android), device or emulator, OS version, app build, environment, time box.
Input checks: a mobile build opens on PROD by default in the source project -> confirm the app points to the test environment before any session; otherwise STOP.

## 4. Access
Read only on supplied material. Writes: a session note file in `runs/` only. No Jira.

## 5-13.
Not yet written. Follow `_templates/SKILL-CONTRACT.md`.

## 12. Open items
- Shared exploratory method location. - Device matrix (UNKNOWN). - Evals not written.
