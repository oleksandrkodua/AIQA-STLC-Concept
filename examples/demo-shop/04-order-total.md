# Story 4: order total with a delivery fee

STATUS: ILLUSTRATIVE, 2026-10-23. Written by hand; not a recorded run.

**Requirement DS-322 (fictional):** "Delivery is free for orders above the free-delivery threshold. Otherwise a flat delivery fee is added. The total is shown with two decimals."

| Stage | Skill | What it produces | Human gate |
|---|---|---|---|
| 1 Requirements | `analyze-requirements` | `READY TO TEST: no`. Blocking questions: what is the threshold, and is "above" strict or inclusive? What is the flat fee? How is a discount applied relative to the threshold? How is rounding done (per line or on the total), and is the threshold compared before or after rounding? | The product owner answers from the pricing table |
| 2 Test design | `create-test-cases` | Without the answers it stops: for the boundary cases it writes `Oracle: UNKNOWN, needs the threshold and the rounding rule from the product owner` and does not write an expected total | The tester sends the questions back; no case is saved yet |
| 2 Test design | `create-test-cases` (second pass) | After the answers (illustrative: threshold 50.00, strict "above", fee 4.90, rounding on the total, threshold compared on the unrounded subtotal) five boundary cases: 49.99, 50.00, 50.01, a discounted basket crossing the threshold downwards, a basket of three lines with fractions | The tester reviews each case and checks the arithmetic against the pricing table, not against the model |

## The cases (ILLUSTRATIVE)

| Case | Basket subtotal | Expected delivery | Expected total | Oracle |
|---|---|---|---|---|
| B1 | 49.99 | 4.90 | 54.89 | pricing table, rule "above 50.00" |
| B2 | 50.00 | 4.90 | 54.90 | same; 50.00 is not above 50.00 |
| B3 | 50.01 | 0.00 | 50.01 | same |
| B4 | 55.00 with a 10 percent code = 49.50 | 4.90 | 54.40 | discount applies before the threshold test (answer to Q3) |
| B5 | three lines of 16.667 each = 50.001 | 0.00 | 50.00 (50.001 rounded on the total) | rounding rule and "unrounded subtotal" from the product owner; if the threshold were compared after rounding, the fee would apply and the total would be 54.90 |

## What this story shows
- The oracle is the most valuable column in a test case, and in this story it comes from a person who owns the rule. If the answer is unknown, the honest output is "UNKNOWN", not a plausible number.
- Boundary values are chosen from the rule, and the mismatch (B2) is exactly where a wrong "inclusive" reading would show up.

## What it does not show
- That a model would really refuse to write an expected total. The skill is written to ask (see `create-test-cases`, the oracle rule), but its evals are NOT RUN.
- Real pricing: all numbers here are invented.
