# Test design techniques: catalogue and task for adaptive selection

STATUS: DRAFT, not approved by QA Lead. Written 2026-11-12 for Codex and Claude.

## Source and limits
- The list below is written from the assistant's general knowledge of the ISTQB CTFL v4.0 grouping and common QA literature. It was NOT checked against the syllabus text or any other source in this session. Label: ASSUMPTION until intake.
- Per `knowledge/INTAKE.md` (ai-rules 8) this is not a rule. Before it influences `create-test-cases`, enter the source (ISTQB CTFL v4.0 syllabus, ISTQB glossary) in `knowledge/register.md` and check each row against it.
- The mapping "input type → technique" in the second part is an INFERENCE, not verified on our materials.

## 1. Catalogue (full list)

### Black-box (from requirements / behaviour)
| # | Technique | Idea | Typical input |
|---|---|---|---|
| 1 | Equivalence partitioning (EP) | split values into classes treated the same; one test per class, valid and invalid | fields, ranges, enums |
| 2 | Boundary value analysis (BVA) | test at and next to each boundary (2-value or 3-value) | numeric/date/length limits |
| 3 | Decision table | combinations of conditions → actions | business rules with several conditions |
| 4 | Cause-effect graph | causes and effects as a graph, then a decision table | complex logic, many dependencies |
| 5 | State transition | states, events, guards, transitions; cover states, transitions, sequences | statuses, workflows, wizards |
| 6 | Use case / scenario testing | main flow plus alternate and exception flows | end-to-end user flows |
| 7 | Pairwise / combinatorial (all-pairs, n-wise) | cover every pair of parameter values with few tests | many independent parameters (browsers, settings) |
| 8 | Classification tree | tree of input aspects and classes, combined into tests | wide input spaces |
| 9 | Domain analysis | EP and BVA over several variables at once (on/in/out/off points) | interdependent ranges |
| 10 | Syntax / grammar testing | valid and invalid strings by a format grammar | formats, parsers, search syntax, dates |
| 11 | CRUD matrix | entities × operations × roles | data management, permissions |
| 12 | Requirements-based | one or more tests per requirement/acceptance criterion | any, as the baseline |
| 13 | Model-based testing | tests generated from a behaviour model | formal models |
| 14 | Metamorphic testing | check a relation between outputs of related inputs when no oracle exists | search, ranking, ML, calculations |
| 15 | Random / statistical testing | inputs drawn from a distribution | stress, robustness |

### White-box (from code structure; needs source access, UNKNOWN until Discovery)
| # | Technique | Idea |
|---|---|---|
| 16 | Statement coverage | every statement executed |
| 17 | Branch / decision coverage | every branch outcome taken |
| 18 | Condition coverage | every atomic condition true and false |
| 19 | Modified condition/decision coverage (MC/DC) | each condition shown to affect the decision alone |
| 20 | Multiple condition coverage | all combinations of atomic conditions |
| 21 | Path coverage | every path through the code |
| 22 | Loop testing | 0, 1, many, max iterations |
| 23 | Data-flow testing | definition-use pairs of variables |
| 24 | Mutation testing | seed faults, check that tests catch them (a test-quality measure) |

### Experience-based
| # | Technique | Idea |
|---|---|---|
| 25 | Error guessing | tests from known typical defects |
| 26 | Exploratory testing | simultaneous learning, design, execution; charters, sessions |
| 27 | Checklist-based testing | tests from a maintained checklist |
| 28 | Fault attack | targeted attempts to trigger a listed fault class |
| 29 | Tours / heuristics (SFDPOT, FEW HICCUPPS and similar) | guided exploration by a mnemonic |

### Collaboration-based
| # | Technique | Idea |
|---|---|---|
| 30 | Acceptance-criteria based / ATDD | tests derived from criteria agreed in the team |
| 31 | BDD examples (Given-When-Then) | concrete examples as tests |
| 32 | Example mapping | rules, examples, questions from a story before test design |

### Related but not design techniques (do not confuse)
Risk-based prioritisation (chooses what to test first), fuzzing and property-based testing (generation by tools; fits automation, mostly API/parsers), A/B or canary checks (release practice).

## 2. Task for Codex: make `/create-test-cases` choose the technique

Goal: instead of one fixed approach, the skill selects a technique, or a mix, from the type of the requirement or task, and says which it chose and why.

Hard rules:
- `plugins/qabase/skills/**` and `.claude/skills/**` are trusted assets. Do not change them. Prepare a proposal for QA Lead: file, exact change, reason, consequences. Stop before applying.
- No new tools or directories. A new reference file inside the existing `create-test-cases/references/` is part of the proposal, not done now.
- Do not rename or move files. Do not invent statuses.
- Any change to the skill needs a new eval case in `create-test-cases/evals/` (also proposed, not applied). Until it runs, status stays DRAFT, evals NOT RUN.
- Manual QA stays first: this is test-case design, not automation.

Steps:
1. Intake: register the source for the catalogue in `knowledge/register.md` (R-xx) per INTAKE, verify section 1 against it, fix errors. Result: catalogue marked with the source.
2. Read `plugins/qabase/skills/create-test-cases/SKILL.md` and `references/edge-cases.md`; record which techniques it already uses (it names categories positive, negative, boundary, permission, state, data, concurrency, recovery; no explicit technique choice found by grep on 2026-11-12). Result: a gap list.
3. Draft the selection table (INFERENCE, to validate on real requirements), for example:
   | What the task looks like | First choice | Mix with |
   |---|---|---|
   | field with a range, length, date | EP + BVA | error guessing |
   | several conditions give different outcomes | decision table | BVA on the thresholds |
   | statuses, workflow, wizard | state transition | use case |
   | many independent settings/environments | pairwise | risk-based pick of key combos |
   | roles and permissions over data | CRUD matrix | decision table |
   | free-form input, format, search | syntax testing, error guessing | EP |
   | no oracle (ranking, calculation, ML output) | metamorphic | exploratory |
   | vague or new feature | exploratory charter | checklist, later requirements-based |
   | user story with acceptance criteria | requirements-based / ATDD | the technique of the row that matches each criterion |
4. Define the rule for mixed cases: classify each acceptance criterion separately, pick a technique per criterion, report the chosen technique in the coverage matrix column (one column added to the existing matrix, not a new document).
5. Define "no suitable technique / not enough information": ask or flag the gap, never guess (CLAUDE.md always-on rules).
6. Write the proposal for QA Lead (SKILL.md diff, reference file, eval cases). Stop. After approval: branch, change, `bash tools/sync-skills.sh`, validator on a clean export, PR.

Open questions for the owner:
- Which techniques are in scope for the project: black-box only, or also white-box (needs code access, UNKNOWN until Discovery)?
- Web checklist and mobile Xray formats: one selection table for both, or separate?

Done looks like: catalogue verified against a registered source; a gap list; a proposal in `feedback/proposals/` or `decisions/` format approved or rejected by QA Lead; eval cases listed as NOT RUN.
