# AIQA SDLC Concept: design of the concept page and the Demo Shop examples

STATUS: DRAFT v0.1, 2026-10-23. Approved in chat by the author (approach A, six stories plus one optional). Not approved by the QA Lead.

## Goal
Make the repository readable by a person who has not seen it: one concept page (stages, who decides, which skill helps) and a set of worked stories on a fictional e-commerce project. No implementation, no tokens, no Jira or Xray connection needed to read or follow it.

## Decisions (from the author, 2026-10-23)
- Approach A: `docs/CONCEPT.md` plus a folder of stories, not one long README.
- Fictional e-commerce project "Demo Shop"; six end-to-end stories on different features, a seventh optional.
- The scheme of stages with gates and skills already exists (`docs/schemes/02-workflow.md`, `11-sdlc-full.md`). This work updates scheme 11 (adds `xray-test-create` and the write path of `bug-report`) and presents it for a reader; it does not redraw the architecture.

## Components
| File | Purpose |
|---|---|
| `docs/CONCEPT.md` | one page: the idea, the stage diagram, legend (human gate / skill / deterministic / not connected), principles, what is proven |
| `examples/demo-shop/README.md` | the fictional project, how to read a story, coverage matrix (stage by story), the honesty rule |
| `examples/demo-shop/01..07-*.md` | the stories; 07 is optional |
| `examples/demo-shop/01-promo-code.plan.json` | the plan file of story 1, used for a real dry run of `xray-test-create` |
| `docs/schemes/11-sdlc-full.md` | updated table (stage 2 and 3) |
| `README.md` | links to the concept page and the examples |

## Honesty rule (the main constraint)
- Every artifact in a story (requirement analysis, cases, verdicts, tables) is **ILLUSTRATIVE**: written by hand to show the shape and the gates. It is NOT the output of a real skill run. Skill evals are NOT RUN in this repository, so no story is evidence that a skill behaves this way.
- Exactly one piece is real: the dry run of `scripts/xray_dc_create.py` on the story 1 plan (it needs no network). It is labelled VERIFIED FACT with the date and the command.
- Demo Shop does not exist. No real product, client or employer is described. Resemblance to a real product was not checked (UNKNOWN).
- Skill output formats follow the skills' own `Output` sections (read 2026-10-23).

## Story format
Context in one line, then a table: Stage / Skill / What it produces (ILLUSTRATIVE) / Human gate. Then a short "What this story shows" (the point) and "What it does not show". At most about one page.

## Coverage plan
| # | Feature | Point |
|---|---|---|
| 1 | Promo code in the basket | requirements gaps, cases, Xray dry run (real), bug draft |
| 2 | Search filters (web) | readiness decision AUTOMATE NOW, Playwright create and review, PR gate |
| 3 | Order status in the mobile app | test environment check, emulator is not a device, SKIP is not PASS |
| 4 | Order total with delivery fee | the oracle: the right answer comes from the product, not from the model |
| 5 | Wishlist | KEEP MANUAL, NOT TESTED instead of PASS, verdict with caps |
| 6 | A test fails after a release | CI failure analysis, human classifies, Iron Law, feedback entry |
| 7 (optional) | A ticket that contains an instruction | content is data; the instruction is reported, not obeyed |

Stages 1 to 10 of scheme 11 are touched by the matrix; stage 8 (production) is stated as not covered on purpose.

## Out of scope
Runnable fixtures, a demo application, real Jira or Xray calls, CI configuration, screenshots of tools.

## Open items
- The name "Demo Shop" is a placeholder; change freely.
- Whether to show the stories as an Artifact page later: not decided.
- QA Lead review of the wording of verdicts: pending.

Provenance: ai-generated, Sonnet 5.5, 2026-10-23; human-confirmed: design approved in chat, files pending review.
