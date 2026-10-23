# Working from a cloud session

STATUS: DRAFT v0.1, 2026-10-23. Written from Anthropic's documentation ("Use Claude Code in the cloud" and "Configure cloud environments", read 2026-10-23). First cloud session 2026-10-23: the repository was attached mid-session, `CLAUDE.md`, rules and skills then loaded, validator 232 passed. The Jira `--check` (section 4) is NOT RUN. Labels: VERIFIED FACT (documentation read) / ASSUMPTION / UNKNOWN.

Goal: open this repository in a Claude Code cloud session and use the skills, including `bug-report` and `xray-test-create`, without the token ever being visible to the model.

## 1. What the session gets from the repository (VERIFIED FACT, docs)

| Item | In a cloud session | Note |
|---|---|---|
| `CLAUDE.md`, `.claude/rules/` | yes | part of the clone |
| `.claude/skills/` | yes | the copies made by `tools/sync-skills.sh`; keep them in sync before pushing |
| `.claude/settings.json` permission rules | yes (a session with one repository) | `ask` on `xray_dc_create.py`, `deny` on commands that mention `JIRA_PAT` |
| Claude Code hooks (scripts in `.claude/hooks/`, turned on by `settings.local.json`) | no | the scripts are committed; the config that turns them on is per machine and not committed. In the cloud the permission rules are the whole floor |
| `.mcp.json` | yes | empty in this repository, see section 5 |
| Your user skills, user `CLAUDE.md`, MCP added at user scope | no | nothing from your machine |
| Plugins listed in `enabledPlugins` | no | skills come from `.claude/skills/` instead |

## 2. One-time setup

1. The repository must be on GitHub (cloud sessions clone from GitHub). Connect GitHub to your Claude account: install the Claude GitHub App on the repository, or run `/web-setup` in a terminal.
2. Open claude.ai/code, choose the repository, and create or edit a **cloud environment** (section 3).
3. Start a session. First message: `/onboarding-check`, then ask for the `--check` below.

## 3. Cloud environment for Jira and Xray

| Setting | Value | Why |
|---|---|---|
| Environment variable `JIRA_BASE_URL` | `https://<your Jira host>` | not a secret; any command can read variables |
| Environment variable `JIRA_AUTH` | `proxy` | tells the script not to look for a token |
| **Network secret** | name: Jira PAT; allowed website: your Jira host; header `Authorization`, prefix `Bearer`, value: your Jira personal access token | the environment's proxy attaches the token to requests for that host; the token never enters the VM, an environment variable or a file |
| Network access | the level that suits you; the secret's host is reachable regardless | |

- VERIFIED FACT (docs): variables set on an environment are readable by anyone who uses the environment and by every command Claude runs. Never put the token in a variable. That would break the rule "credentials never visible" (`security-rules.md` item 4).
- VERIFIED FACT (docs): network secrets are available on Pro, Max, Team and Enterprise; on Enterprise adding one may need an organization admin role.
- Use your own personal access token and revoke it when you stop. Never paste it into the chat, a file or a commit.
- Do not set a token for Xray separately: Xray Server/DC runs inside Jira on the same host.

## 4. Check before the first real use

In the session, ask: "run the xray-test-create connection check". It runs:

```bash
python3 .claude/skills/xray-test-create/scripts/xray_dc_create.py --check
```

(You will be asked to approve it: the permission rule is `ask`.) Read the result:

| Result | Meaning | Next |
|---|---|---|
| `CHECK <host>: HTTP 200 as <user>` | host reachable, token accepted | go on |
| HTTP 401 / 403 | token rejected or not attached | check the secret's host and header; stop, do not try other credentials |
| network error / timeout | the host is not reachable from the cloud VM | see "Network" below |
| `JIRA_PAT is not set ...` | `JIRA_AUTH=proxy` is missing from the environment | fix the environment |

Network (UNKNOWN for your instance): an Anthropic-hosted cloud environment reaches public hosts only. A Jira Data Center on a private network or behind a VPN is not reachable from it. Options: ask IT whether the Jira host is reachable from the internet and allowed for this use; or use a self-hosted environment (documented by Anthropic, set up by your IT); or work locally in the Claude Desktop or CLI with `JIRA_PAT` in your own shell.

## 5. Bugs through the Jira MCP (UNKNOWN)

`bug-report` creates a ticket through a Jira MCP connection. This repository's `.mcp.json` is empty on purpose: the approved MCP list is a Discovery item (`context/discovery.md`). Whether a connector you added on claude.ai is available inside a cloud session was not verified. Test it in the session: ask Claude to list its Jira tools. If none exist, `bug-report` stops at the draft, which is the intended safe behaviour.

## 6. Daily flow

1. `/create-test-cases` from an approved requirement; review the drafts.
2. Say the drafts are approved; `/xray-test-create` writes the plan file and shows the dry run with `plan-hash`.
3. You confirm project, hash and host; it applies; you open one created case in Xray and compare it with the draft.
4. Cloud sessions can push a branch and open a PR for files the session changed (plan files, notes). Nothing else leaves the session.

## 7. One folder for local and cloud work

The repository on GitHub is the single meeting point. The same folder is used locally; a cloud session clones it from GitHub. Nothing is copied by hand.

| Step | Where | What |
|---|---|---|
| 1 | local | work in the folder; commit; `git push` |
| 2 | cloud | start the session: it clones the pushed branch. Uncommitted local changes do NOT reach it, so push first |
| 3 | cloud | the session works and pushes its own branch; you open a pull request on GitHub |
| 4 | local | merge the pull request; `git pull` in the folder; both sides are the same again |

- Never keep edits only in the cloud session or only uncommitted locally: the other side will not see them.
- Everything pushed is public if the repository is public. Keep real project data out of it: ticket text, Jira hosts and field maps, customer data, evidence files. `runs/`, `.env*` and `evidence/` are git-ignored; put plan files for `xray-test-create` under `runs/` so they are never committed. Real project work belongs in a private repository created from this base.
- Only `refs/heads/main` (and short-lived branches) should ever be pushed. The `pre-push` hook in `tools/git-hooks/` stops any other ref and any push whose tip contains blocked patterns (speaker names, an earlier client's name, a phone number, tokens, keys). It is a floor, not a guarantee; bypassing it needs `--no-verify`.
- Local-only history: the app keeps private snapshots in `refs/time-machine/*`, and the old pre-publication history is kept under `refs/archive/pre-public`. Neither is a branch or a tag; do not push with `--mirror`, and do not copy the `.git` folder to another place.

## 8. What this does not give you

- Claude Code hooks are not active in the cloud: `deny_prod_and_secrets` and the other guards do not run there.
- The git hooks (`pre-commit` runs the validator, `pre-push` stops blocked patterns from reaching this public repository) are off in a fresh cloud clone. Run `sh tools/install-git-hooks.sh` once in the session: it sets `core.hooksPath` for that clone only.
- The permission rules are patterns: a renamed copy of the script or an unusual command shape can escape the `ask`. The plan hash and host confirmation inside the script are the real gates.
- Production is prohibited. The skill cannot know which Jira is production; you confirm the host each time.
- Evals for both skills are NOT RUN. Treat the first runs as trials on a test project.

## 9. First run in a cloud session: checklist and prompt

Two parts. Part A needs no credentials and writes nothing outside the session's clone. Part B needs the environment of section 3 and only reads (`--check`). Neither part creates anything in Jira or Xray.

### 9.1 Before you start (you, once)

- [ ] GitHub is connected: the Claude GitHub App is installed on the repository, or you ran `/web-setup` in a terminal. The repository is listed at claude.ai/code (section 2).
- [ ] Everything the session should see is pushed: `git status -sb` shows no changes and no `[ahead N]`, and `git rev-parse HEAD` prints the same hash as `git ls-remote origin main`. A cloud session sees only pushed work.
- [ ] Part B only: the environment has the two variables and the network secret of section 3. The token is typed into the secret form only: never a variable, never the chat.
- [ ] Start the session with this repository selected, branch `main`, in that environment (for Part A alone the Default environment is enough). A session started without the repository loads none of `CLAUDE.md`, the rules or the skills (seen 2026-10-23); attaching the repository later loads them, but do not rely on that.

### 9.2 Prompt to paste into the cloud session

```
First run of this repository in a cloud session. Short answers. Change no file in the repository.
Part A (no credentials):
A1. Name the repository and branch, and give `git log --oneline -1`.
A2. List the project skills you have loaded (expected: the skills in CLAUDE.md, such as onboarding-check and xray-test-create). If none are loaded, stop and say so.
A3. Read docs/HANDOFF-cloud.md and give its "State" commit in one line.
A4. Run `sh tools/install-git-hooks.sh` (it sets core.hooksPath for this clone only), then `python3 evals/validate_repo.py | tail -1`.
A5. Run `python3 plugins/qabase/skills/xray-test-create/scripts/test_xray_dc_create.py` (offline, fake HTTP).
Part B (only after I say the environment has the Jira settings):
B1. Say whether JIRA_BASE_URL and JIRA_AUTH are set: "set" or "not set" only.
B2. Run: python3 .claude/skills/xray-test-create/scripts/xray_dc_create.py --check (it will ask for approval). Do not retry with other credentials.
For each step write PASS, FAIL or NOT TESTED and the output line that shows it.
```

### 9.3 What counts as ready, and what to do with the result

Part A is ready when A2 lists the project skills, A1 matches your laptop, and A4 and A5 pass. Part B is ready when B2 prints `CHECK <host>: HTTP 200 as <user>`.

| Result | What it means | Next |
|---|---|---|
| A2 lists the project skills | the session loaded this repository's `CLAUDE.md`, rules and skills | go on |
| A2 lists none | the session was started without the repository | start a new session with the repository selected (9.1) |
| A1 commit differs from `git log --oneline -1` on your laptop | one side has work the other has not | push or pull until both match, then start again |
| A4 `N passed, 0 failed` and A5 `OK` | the pushed tree passes its own checks in the cloud | Part A ready: use the session for the work in `docs/HANDOFF-cloud.md` |
| A4 shows a FAIL line, or A5 is not OK | the pushed tree is broken, or the cloud differs from your laptop | fix it locally, push, start again |
| B2 prints any result | see the table in section 4 | follow section 4 |

A laptop can show one more passed check than the cloud: the validator also checks a local, git-ignored `.claude/settings.local.json`.

Provenance: ai-generated, Sonnet 5.5, 2026-10-23; section 9 added 2026-10-23 in a cloud session (ai-generated); human-confirmed: pending.
