# Skills navigator: DRAFT sectors and intents (for approval; nothing is built from this yet)

Proposal by Claude, not approved by the AI QA Process Lead. After approval each row becomes a `NAVIGATOR.yaml` in the skill folder (see `docs/specs/2026-10-13-skills-navigator-design.md`). Intents are short English task phrases a tester would say; 2-4 per skill. `needs` is taken from the skill descriptions, not verified against the skills' access sections.

## Sectors (clockwise, SDLC order)
| id | title | what a person is doing |
|---|---|---|
| requirements | Requirements & design | has a story or change, before testing starts |
| manual | Manual testing | executing, exploring, recording results, reporting defects |
| automation | Automation | deciding, writing, reviewing automated tests |
| ci | CI & failures | a pipeline run is red |
| investigation | Investigation | needs facts about an error, an owner, a flag, a repo change |
| reporting | Reporting | needs numbers for a manager |
| setup | Session & setup | first open, new machine, session getting long |

## Skills
| skill | sector | intents | needs |
|---|---|---|---|
| analyze-requirements | requirements | is this story ready to test; review the acceptance criteria; find gaps in a requirement; a requirement changed, what is at risk | none (pasted text); Jira MCP optional |
| create-test-cases | requirements | write test cases for a story; what should be tested for this change; coverage for a bug fix | approved requirement; Jira/Xray optional |
| exploratory-testing-web | manual | explore a web feature; write a charter for the web shop; session-test a web flow | web test environment |
| exploratory-testing-mobile | manual | explore a mobile feature; write a charter for iOS or Android; session-test the app | device or emulator, build id |
| update-test-status | manual | mark these cases passed or failed; update a test execution; record manual results | Jira/Xray write |
| bug-report | manual | file a bug; write up this defect; check for duplicates before reporting | Jira write |
| automation-readiness-assessment | automation | should we automate this case; what goes into the regression suite; review the regression backlog | a manual pass of the case |
| create-playwright-test | automation | automate this case on web; write a Playwright test | approved candidate; web automation project |
| create-mobile-test | automation | automate this case on mobile; write an Appium or WebdriverIO test | approved candidate; emulator or device; test environment |
| review-playwright-test | automation | review this Playwright diff; is this web test any good | the diff |
| review-mobile-test | automation | review this mobile test diff; audit an Appium test | the diff |
| ci-failure-analysis | ci | why did the pipeline fail; analyze this red CI run; classify these failures | CI access (system unknown) |
| ci-fix | ci | fix this failing automated test; propose a diff for a test defect | an accepted analysis |
| qa-reporting | reporting | build a QA report for a manager; sprint test summary; trend vs last month | Jira/Xray read |
| onboarding-check | setup | check my setup; first time in this project; something is not installed | none |
| handoff | setup | save progress before /clear; hand this session to another person; summarize where we stopped | none (writes runs/<id>/HANDOFF.md) |

## Sector decisions (2026-10-13)
- `bug-report` stays in manual (decided by the AI QA Process Lead).
- A skill has ONE primary sector. `update-test-status` -> manual (proposed; confirm). Cross-sector discovery is covered by intents and tags (search and router find a skill by what the person types, not by sector). An optional `also_in` field (a second sector, shown in both lists) is possible but not planned.

## Questions still open
1. Are the intents what your team would actually type?
2. Should `needs` be shown to users on the card, or kept for the router only?
