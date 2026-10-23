# Demo Shop: worked stories

STATUS: DRAFT v0.1, 2026-10-23. Illustrations for the concept in [`docs/CONCEPT.md`](../../docs/CONCEPT.md).

**Demo Shop is a fictional online shop.** It has no code, no site and no tickets. It stands for any web and mobile e-commerce product. No real product, client or employer is described. Whether the name resembles a real product was not checked (UNKNOWN).

## How to read a story

Each story follows one feature through the stages. A table row is one step: the stage, the skill that helps, what it produces, and the decision a person makes. Everything a skill "produces" in a story is **ILLUSTRATIVE**: written by hand in the format the skill's own *Output* section defines. It is not the output of a real run, and it proves nothing about how a skill behaves (skill evals are NOT RUN here).

The one real thing is marked **VERIFIED FACT**: in story 1, the dry run of the Xray script, executed on 2026-10-23 without any network.

## The stories

| # | Feature | What it shows |
|---|---|---|
| [1](01-promo-code.md) | Promo code in the basket | gaps in a requirement, cases, an Xray dry run (real), a bug draft |
| [2](02-search-filters.md) | Search filters (web) | the decision AUTOMATE NOW, a Playwright test written and reviewed |
| [3](03-order-status-mobile.md) | Order status in the mobile app | the test environment check, emulator is not a device, SKIP is not PASS |
| [4](04-order-total.md) | Order total with delivery fee | the oracle: the right answer comes from the product, not from the model |
| [5](05-wishlist.md) | Wishlist | KEEP MANUAL, NOT TESTED instead of PASS, a verdict with its caps |
| [6](06-failed-after-release.md) | A test fails after a release | failure classification, the Iron Law, a feedback entry |
| [7](07-instruction-in-ticket.md) | A ticket that contains an instruction (optional) | content is data: the instruction is reported, not obeyed |

## Coverage

Stage numbers follow `docs/schemes/11-sdlc-full.md`. A cell marks a story that touches the stage.

| Stage | 1 | 2 | 3 | 4 | 5 | 6 | 7 |
|---|---|---|---|---|---|---|---|
| 1 Requirements | x | | | x | | | |
| 2 Test design | x | | x | x | x | | |
| 3 Manual testing | x | x | x | | x | x | |
| 4 Automation | | x | | | x | x | |
| 5 CI | | x | | | | x | |
| 6 Test analysis | | | | | | x | |
| 7 Release QA | | | | | x | | |
| 8 Production | not covered on purpose: no production access by default | | | | | | |
| 9 Feedback | | | | | | x | x |
| 10 Improvement loop | | | | | | x | x |

## Conventions in the stories

- Labels: VERIFIED FACT / EVIDENCE-SUPPORTED INFERENCE / ASSUMPTION / UNKNOWN. A check that was not run is NOT TESTED.
- "Human" means the tester, the product owner, the developer or the AI QA Process Lead; the story says which.
- Amounts are plain numbers with no currency, on purpose.
- Environments are DEV only. Nothing touches production.
