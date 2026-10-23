# Portfolio

| File | What it is |
|---|---|
| [`Oleksandr_Kukhtinov_AI_QA_One_Pager.html`](Oleksandr_Kukhtinov_AI_QA_One_Pager.html) | one page: background, what I built with Claude Code, who did what, honest status. Open in a browser. |
| [`Oleksandr_Kukhtinov_AI_QA_POC.pdf`](Oleksandr_Kukhtinov_AI_QA_POC.pdf) | one page: the structure of the proof of concept, what exists and what it is for, who did what |
| [`Oleksandr_Kukhtinov_QA_Case_Study.pdf`](Oleksandr_Kukhtinov_QA_Case_Study.pdf) / [`qa-case-study-manual-qa.html`](qa-case-study-manual-qa.html) | 14-slide case study: QA flow behind each decision, oracle and evidence design, failure diagnosis, per-item verification status (slide 11), retrospective |

## Status

- State of the described system: August 2026. The case study is anonymized (client name, internal domains and Slack channel names replaced); architecture, counts and gaps are unedited. ASSUMPTION: anonymization confirmed by the author, not independently checked.
- The documents describe an earlier, separate system. This repository is a neutral base that reuses its approach; it is not that system, and its numbers do not carry over.
- Statements by the author, 2026-10-23 (ASSUMPTION: no run log is kept in this repository):
  - the mobile suites (24 smoke checks on Android: 17 as guest, 7 signed in; the same 24 on iOS) and the six diagnostic skills were re-run after the package was restructured;
  - the web suite still only opens the site; 24 smoke checks are planned;
  - bug creation and test-case creation in Xray are implemented as skills and have not yet been run against a live tracker.
- The per-item status is on slide 11 of the case study; the documents are dated "as of August 2026" and carry that date on purpose.
- Cleared for AI-assisted testing roles, not for pure SDET roles.
- The phone number was removed from the one-page copy in this repository.
- Publication permission from the employer: confirmed by the author (not documented here).
