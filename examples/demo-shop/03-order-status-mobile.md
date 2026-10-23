# Story 3: order status in the mobile app

STATUS: ILLUSTRATIVE, 2026-10-23. Written by hand; not a recorded run.

**Requirement DS-305 (fictional):** "In the mobile app a customer sees the status of an order (Placed, Packed, Shipped, Delivered) and receives a push notification when it changes to Shipped."

| Stage | Skill | What it produces | Human gate |
|---|---|---|---|
| 3 Manual testing | none (a person), under `mobile-rules.md` | **Before any run:** the build is installed and the tester verifies it points at the test backend. A mobile build can open on production by default, so the tester checks the environment screen and the first request, and writes the result in the run journal | If the build points at production: STOP, no run |
| 3 Manual testing | `exploratory-testing-mobile` | A session on an Android emulator and one on a real iOS device. Findings: the status chip truncates "Delivered" at the largest font size on the emulator | The tester repeats the truncation on a device before filing it: an emulator is not a device |
| 4 Automation | `automation-readiness-assessment` | The status screen: AUTOMATE LATER (blocker: no stable accessibility ids yet, owner: mobile developer). The push notification: KEEP MANUAL (needs a real device and the platform's notification service) | The tester agrees or overrules |

## The run record (ILLUSTRATIVE)

| Check | Android emulator | iOS real device |
|---|---|---|
| Build points at the test backend | PASS (environment screen and first request seen) | PASS (same) |
| Status chip shows all four states | PASS | PASS |
| Status chip at the largest font size | FAIL, truncated | NOT TESTED, setting not changed on the device |
| Push when status becomes Shipped | NOT TESTED (emulator cannot show this reliably) | PASS, received in about the time of one status poll (not measured) |
| Automated smoke check of the status screen | SKIP, blocked: no stable ids | SKIP, blocked: no stable ids |

**Verdict: READY WITH RISKS.** Limits: the font-size failure is seen on an emulator only; one device model and one OS version; the Android push path is untested. Confidence is capped at MEDIUM because a key finding rests on an emulator and one check is planned but not done.

## What this story shows
- The environment check is the first step, written down, and a stop condition.
- The evidence says which surface produced it: emulator or device.
- A SKIP is reported as SKIP with its reason. It is never counted as PASS, and NOT TESTED is never collapsed into FAIL.

## What it does not show
- A real device lab, real builds or the real behaviour of a push service. Timings in the record are invented for the shape of the example.
