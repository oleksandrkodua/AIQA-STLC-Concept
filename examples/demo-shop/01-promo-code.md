# Story 1: promo code in the basket

STATUS: ILLUSTRATIVE, 2026-10-23. Everything below except the dry run is written by hand to show the shape of the work.

**Requirement DS-101 (fictional):** "A customer can enter a promo code in the basket. A valid code lowers the total by the code's percentage. One code per order."

| Stage | Skill | What it produces | Human gate |
|---|---|---|---|
| 1 Requirements | `analyze-requirements` | A verdict `READY TO TEST: no`, driven by an unmet blocking criterion (the oracle is not exact). Blocking questions: Q1 before or after delivery? Q2 what does an expired code do? Q3 a second code: replace or refuse? Q4 case sensitivity? Related area to check: sale prices | The product owner answers Q1 to Q4 (here: before delivery; message and no change; refuse; not case sensitive) and approves the brief |
| 2 Test design | `create-test-cases` | Four cases with an oracle each, traced to AC-101-1 to AC-101-4, plus a matrix check and a "not covered deliberately" list (stacking with a sale price: waiting for an answer) | The tester reviews each case: KEEP three, MODIFY one (the lower-case case needs the answer to Q4 quoted as its oracle) |
| 2 Test design | `xray-test-create` | A plan file and the dry run below. Nothing is written | The tester would confirm project, plan hash and host before any write. **In this story nothing is applied: no Xray is connected** |
| 3 Manual testing | none (a person runs the cases on DEV) | Results: cases 1, 2, 3 pass; case 4 fails: `save10` is rejected | The tester decides pass or fail from the evidence |
| 3 Manual testing | `bug-report` | A `BUG DRAFT (not created)`, below | The tester confirms the draft; severity and priority are the human's |

## The real part: the dry run

[`01-promo-code.plan.json`](01-promo-code.plan.json) holds the four approved cases. Run on 2026-10-23, no network, no credentials needed:

```bash
python3 plugins/qabase/skills/xray-test-create/scripts/xray_dc_create.py examples/demo-shop/01-promo-code.plan.json
```

Output, VERIFIED FACT (copied from that run):

```
DRY RUN: nothing sent
project: DEMO   issue type: Test   cases: 4
 1. Promo code: a valid code lowers the basket total by its percentage  [2 steps]  labels: demo-shop, promo-code, ai-drafted
 2. Promo code: an expired code is rejected with a message  [2 steps]  labels: demo-shop, promo-code, ai-drafted
 3. Promo code: a second code is not stacked on the first  [2 steps]  labels: demo-shop, promo-code, ai-drafted
 4. Promo code: the code is not case sensitive  [2 steps]  labels: demo-shop, promo-code, ai-drafted
plan-hash: ae10c3f53c9324a0
```

To write these cases for real, the tester would add the hash and the Jira host to the command (`--apply --plan-hash ae10c3f53c9324a0 --expect-host <host>`) with a connection and a token set up as in `docs/CLOUD-SESSION.md`. The script refuses if the plan changed since the preview or the host was not confirmed.

## The bug draft (ILLUSTRATIVE)

```
BUG DRAFT (not created)
Project / Type / Summary: DEMO / Bug / [Basket] A promo code in lower case is rejected
Assignee / Fix version / Components: UNKNOWN (no project field map)
Severity (suggested): Medium because a normal input is refused, with no data loss
Priority (suggested): Medium because a workaround exists (type the code in capitals)
Environment: web, DEV, build 4.2.0-demo, account: test shopper A
Steps: 1. Add products worth 40.00. 2. Enter "save10". 3. Press Apply.
Expected (source: product answer Q4, AC-101-4): the code is accepted, subtotal 36.00
Actual: "Invalid code", subtotal stays 40.00
Evidence: basket-lowercase.png (to be attached by the tester)
Linked: case 4 of the plan. Duplicates checked: search not run (no Jira connection)
```

## What this story shows
- The skill finds the blocking questions *before* cases are written; the answers come from people.
- Every case names its oracle, so a failing case points at a requirement, not at an opinion.
- Two writes (Xray, Jira) are both behind a preview and a confirmation.

## What it does not show
- A real skill run or a real Jira or Xray call. The duplicate search was not done and the draft says so.
