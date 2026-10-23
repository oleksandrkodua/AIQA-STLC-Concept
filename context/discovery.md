# Discovery checklist

STATUS: all items OPEN. Each answer must name its source (person, document,
date). Until answered, rules and skills treat the item as UNKNOWN and ask rather than assume.

| # | Question | Why it matters | Answer | Source | Log ref |
|---|---|---|---|---|---|
| 1 | Is the engagement confirmed, with scope (web, mobile, AI/automation lead)? | Scope drives which optional parts are used | | | |
| 2 | Is Claude Code allowed (CLI, Desktop, VS Code)? Is claude.ai chat allowed with project data? | Policy | | | |
| 3 | Where is the repository with the project's context and current skills? Access? | Source of project facts | | | |
| 4 | Which environment: DEV, SIT, both? URLs, VPN, accounts | Safety and doctor scripts | | | |
| 5 | Production hostnames to block | Hook list | | | |
| 6 | CI/CD tool, runners, secrets store | Pipeline design (a guess must be labelled as a guess) | | | |
| 7 | TMS and defect tracker; custom fields for provenance; API access | Case delivery, duplicate check | | | |
| 8 | Approved MCP servers (for example Atlassian, Slack, Grafana) and who approves | `.mcp.json` | | | |
| 9 | Mobile: which app builds, how delivered, which devices/OS, real-device access, cloud device service | Mobile scope and the emulator ≠ device rule | | | |
| 10 | Data classification, PII policy, where run evidence may be stored | `runs/` handling | | | |
| 11 | Who is QA Lead / approver and deputy | Approval gates | | | |
| 12 | Language of project documents and the team's working language | Repository language (written in English by assumption) | | | |
| 13 | Are existing automation projects (web, mobile) still current for the app? | Port plan | | | |
| 14 | Existing regression size and its current state | Scope of regression automation; no promised percentage | | | |
| 15 | Which product or customer configurations are in scope on the test environment, and how is one selected in a build (config, flag, separate build)? | Test matrix, rules scope, data | | | |
| 16 | Locales, currencies, regions and regulations in scope | Test data, consent and legal checks | | | |
