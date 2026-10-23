# Story 5: wishlist

STATUS: ILLUSTRATIVE, 2026-10-23. Written by hand; not a recorded run.

**Requirement DS-410 (fictional):** "A signed-in customer can add a product to a wishlist from the product page and from the search results. The wishlist is the same on the web and in the mobile app."

| Stage | Skill | What it produces | Human gate |
|---|---|---|---|
| 2 Test design | `create-test-cases` | Seven cases: add, remove, add twice, add when signed out (redirect to sign-in), limit of items (UNKNOWN: no stated limit, a question), sync web to app, sync app to web | The tester reviews; cases 6 and 7 are marked "needs two real devices" |
| 3 Manual testing | none (a person), on a time budget | The plan below | The tester sets the tiers |
| 4 Automation | `automation-readiness-assessment` | Add and remove on web: AUTOMATE LATER (low risk, the page is being redesigned, blocker named). Cross-device sync: KEEP MANUAL (two real devices, low repeat value) | The tester agrees |
| 7 Release QA | `qa-reporting` | The verdict below | A person makes the release decision; this is only an input |

## The plan under a time budget (ILLUSTRATIVE)

Two hours were available.

- **MUST:** add, remove and add-twice on web (core function); signed-out redirect (access); sync web to app on one real device (the stated cross-surface promise).
- **SHOULD:** item limit (waiting for an answer); sync app to web.
- **SKIP, with the risk accepted:** wishlist on the Android emulator (risk accepted: a layout problem on a small screen can be missed); wishlist with a very large number of items (risk accepted: slow page not detected); accessibility of the heart button (risk accepted: a screen-reader user may not be able to operate it, to be covered next cycle).

## The verdict (ILLUSTRATIVE)

| Area | Status | Note |
|---|---|---|
| Add / remove on web | PASS | evidence: run log lines 4-9 |
| Signed-out redirect | PASS | |
| Sync web to app | PASS | one iOS device, one OS version |
| Sync app to web | NOT TESTED | time budget |
| Item limit | UNKNOWN | requirement silent; question open with the product owner |
| Heart button for a screen reader | NOT TESTED | accepted risk, see SKIP |

**Status: READY WITH RISKS.** What limited it: a planned check was not done (confidence capped at MEDIUM), a whole category (accessibility) is untested (the cap on that category is LOW), and the sync result rests on one device. Nothing was marked PASS that was not run.

## What this story shows
- Not testing is a decision with a named risk, not an omission.
- The verdict lists what limited its own confidence.
- A manual-only recommendation is a valid output of the readiness skill.

## What it does not show
- The accessibility consequence rule in full: if the heart button could not be reached or operated at all, that would be a Functional finding, not a cosmetic one (`qa-rules.md`, item 11).
