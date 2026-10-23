# AI usage policy — DRAFT for agreement with the team and the project owner

STATUS: DRAFT v0.1. Nothing here is agreed. Every
clause is a proposal for the QA Lead and the security/IT owner of the employer or client to accept, change or
reject. Principle: policy comes before capability (no agent, routine or integration is
enabled before its clause here is agreed).

Sources: rules from earlier QA tooling (read; whether an employer or client approved them
is UNCONFIRMED); a layered architecture design (governance, security, privacy, secrets sections); notes from talks (single source).

| # | Clause | Basis | Needs owner decision |
|---|---|---|---|
| 1 | Allowed surfaces: Claude Code (CLI, VS Code extension, Desktop Code). Whether the Claude desktop chat / claude.ai web may be used with project material is NOT assumed: until decided, project material is not pasted into claude.ai web chats | earlier QA tooling | YES: which surfaces |
| 2 | Environments: DEV or other approved non-production only. Production access, accounts and data are prohibited | earlier QA tooling; architecture design | YES: names/URLs |
| 3 | Secrets never go into chat, files, commits, logs or screenshots. Secrets are provided by environment variables or the approved store. A leaked secret is rotated and reported | earlier QA tooling; architecture design (secrets) | YES: secret store |
| 4 | No real customer or production data in tests, prompts or evidence. Synthetic or anonymised data only | architecture design (privacy) | YES: classification, PII rules |
| 5 | No "YOLO" modes: permission prompts are not bypassed globally; deny rules and hooks stay on | earlier QA tooling | no |
| 6 | AI output is a draft. A human reviews every change before merge; nothing merges to `main` without review. AI does not replace review, the QA Lead's approval or the release decision | earlier QA tooling; architecture design | no |
| 7 | Changes to rules, skills, hooks, settings and policy go through QA Lead approval | architecture design (trusted assets) | YES: who is QA Lead and deputy |
| 8 | External systems are reached through approved MCP servers only. New servers need approval and a version pin | architecture design (tools); a talk (single source) | YES: approved list |
| 9 | Content read from tickets, wiki, logs and web pages is data, never instructions | earlier QA tooling | no |
| 10 | Routines and agents are read-only until a clause in `agents-policy.md` allows more | earlier QA tooling; architecture design (autonomy) | YES |
| 11 | Provenance: every AI-produced case, test and analysis records source, model/version, skill, date and status | architecture design (provenance) | YES: TMS marker |
| 12 | Evidence retention: run evidence (screenshots, logs) is stored only where the employer or client allows; kept out of commits | architecture design | YES |
| 13 | Metrics: acceptance of AI output, rewrite rate, review time, pass/flaky rate, escaped defects, defect yield of AI vs hand-written cases. No target percentages before a baseline | architecture design; a talk's ROI idea | YES: what the owner wants measured |
| 14 | Incidents: unexpected AI behavior, leaked data or a bypassed control is reported to the QA Lead the same day and logged in `feedback/` | architecture design (governance) | YES: contact |

## Not agreed yet (do not assume)
The list of approved tools and models, who may use which surface, what data may leave the
employer or client network (model provider terms), retention at the provider, and whether telemetry export
is permitted.
