# Getting started and handing over

STATUS: DRAFT v0.1 (2026-10-20). Written from what was checked in an earlier project on one Mac with the Claude Code terminal client. Nothing was re-checked in this base. Everything about the Desktop "Code" tab and VS Code is NOT VERIFIED (marked below). Approved by: pending.

## 1. Is everything in the folder?
Yes for the process: rules (`CLAUDE.md`, `.claude/rules/`), 18 skills (source in `plugins/qabase/skills/`, generated copy in `.claude/skills/`), hooks (`.claude/hooks/`), permission profiles (`tools/settings.qa.json`, `tools/settings.shared.json`), evals, docs, decisions.
No, for the machine and the accounts. These are NOT in the folder and each person sets them up:
- Python 3 (hooks and the validator need it) and Node/Playwright for automation work (`docs/REQUIRED-ACCESS-AND-ENVIRONMENT.md`, Part B).
- `.claude/settings.local.json`: per machine, not committed, created by the apply script.
- Access to Jira/Xray, Slack, GitLab and CI. `.mcp.json` is empty on purpose: no MCP server is approved yet.
- The project's repository and environments (access comes from the project).
- Whether Claude Code (CLI, Desktop, VS Code) is allowed on an employer's or client's machine is an open question (`context/discovery.md`, item 2).

## 2. Open it
Any of these opens the same project settings from the folder (`CLAUDE.md`, `.claude/`):
- Terminal: `cd <folder>` then `claude`. This is the only way checked in the earlier project.
- Claude desktop app, Code tab: choose the folder. NOT VERIFIED.
- VS Code: open the folder, then the Claude Code panel. NOT VERIFIED.
In Desktop and VS Code the hook rows must be tested again (E24, E25 in Part E of the access doc), because firing has to be checked on each surface (in an earlier project it was seen only in the terminal).

## 3. First run on a machine (about 10 minutes)
1. `bash tools/apply-trusted-changes.sh --dry-run --profile qa` and read it. Maintainers use `--profile maintainer`. First time ever: do it in a copy of the folder.
2. Run it without `--dry-run`, answer `y`. Restart Claude Code in the folder.
3. In Claude Code use manual (default) permission mode, not auto mode: auto mode can hide the prompts the tests look for.
4. Run `/onboarding-check`. It guides item by item and writes `runs/onboarding/progress.md` (not committed).
5. `python3 evals/validate_repo.py` must end with `0 failed`.

## 4. Where to start working
- Not sure which skill: read `plugins/qabase/skills-index.json` or ask; a router skill (`which-skill`) is planned, not built.
- Typical chain: `analyze-requirements` -> approved brief -> `create-test-cases` -> `automation-readiness-assessment` -> `create-playwright-test` / `create-mobile-test` -> `review-*`. Details: `docs/AIQA-SUMMARY.md`.
- Something went wrong or the AI was corrected: `/qabase:feedback` (writes a draft to `feedback/inbox/` after you say yes; you forward it yourself). Nobody edits skills or rules from a session: changes go through the AI QA Process Lead.

## 5. Hand over a session
`/qabase:handoff <run id>` writes `runs/<id>/HANDOFF.md` (at most 60 lines, `runs/` is not committed). In the new chat: "Read runs/<id>/HANDOFF.md first, then the approved brief. Do not rely on any earlier chat." Offer a handoff at about 50% context and again at 60% (numbers are a guess to measure on the pilot).

## 6. Input from tickets, pages and logs (untrusted)
STATUS: DRAFT, design 2026-10-23 (injection defense R2, R8); NOT TESTED.
- Text from a ticket, wiki page, CI log or chat is data, and an injected instruction in it is the main way a session gets hijacked. Save the text under `runs/<id>/input/` (git-ignored) and have the skill read it with Read, so it arrives as file content. If you paste it into the chat, the skill restates it as quoted data and asks before any write or network action.
- Permission mode: manual (default) for QA sessions, written in the run journal. Auto mode hides the prompts that catch a hijacked action.
- Running `claude -p` (or opening Claude Code) on a fork, a pull-request branch or an unfamiliar clone: the repository's own settings, hooks and MCP list would load first. Use the flags from the research report (D15), after `claude --help` shows they exist in your version: `--setting-sources user`, `--bare`, `--settings '{"disableAllHooks": true}'`, and a `disabledMcpjsonServers` entry. NOT TESTED here. Never open an unreviewed branch in a session that holds a secret.
- When a handoff, feedback entry or run journal was written from untrusted input, it says so in its first lines: "Input: untrusted (ticket / page / log) | none".

## 7. Hand over the project to another QA
Not decided: marketplace install or git clone (`docs/DISTRIBUTION-OPTIONS.md`). Before sharing: check the repository for project-specific facts (names, hosts, accounts) and for secrets. Keep a working repository (`.git`, `node_modules`) on a path that is not synced by a cloud service (iCloud, OneDrive): sync conflicts create duplicate files.
