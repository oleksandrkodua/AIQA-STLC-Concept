# Required access and environment — QA plugin (`qabase`)

STATUS: DRAFT v0.1, 2026-10-20. Not reviewed by a QA Lead. Nothing in this file was run on an employer or client machine.
Language: English. Owner of decisions: the person named in `context/discovery.md`.

This file has two jobs:
1. Tell IT / the client what access the plugin needs (Part A) and which tools a machine needs (Part B).
2. Be the start-up checklist for a new user who opens this folder in Claude Code (CLI, VS Code, Desktop) — Part E. The skill `onboarding-check` runs the safe checks from Part E and reports PASS / FAIL / NOT CHECKED.

## 0. How to read this file

| Marker | Meaning |
|---|---|
| HAD | The access existed in an earlier project (stated by a person). NOT re-checked for this project. |
| CHECK | Not known; verify before relying on it. Do not assume either way. |
| NEW | Did not exist before; has to be requested. |
| UNKNOWN | No information yet. |
| PER-USER | Differs from person to person; every new user runs the check. |

Rules for every check:
- Tokens, passwords and API keys are never typed into the chat and never shown to Claude. The person who owns the credential runs any command that uses it.
- Claude may run only read-only checks (version commands, "does this file exist", one read-only query). Anything that logs in, installs, downloads, or writes is run by the person.
- Commands in Part B are NOT VERIFIED on the target OS unless the row says where they came from. Windows in particular: the earlier project's docs say their own Windows steps were never run on real hardware.
- Environment: DEV only. Production indicated -> stop.

---

## Part A. Access

| ID | Access | Mode | Needed by (skills) | Status | Without it |
|---|---|---|---|---|---|
| A1 | Jira via MCP | read | analyze-requirements, bug-report (duplicate search), update-test-status, qa-reporting | CHECK (read-only), PER-USER | those skills run on pasted text only |
| A2 | Jira via MCP | **write**: create bug, attachments, status change | bug-report, update-test-status | **NEW** | skills stay at "draft only" |
| A3 | Xray | **read + write**: test cases, steps, executions, statuses, plans | create-test-cases (mobile format), update-test-status, qa-reporting | **NEW**; CHECK whether the Atlassian MCP covers it | Xray work is done by hand from drafts |
| A4 | Confluence | read | analyze-requirements | CHECK | none; not a blocker |
| A5 | Figma via MCP | read | analyze-requirements, design-check (reserved) | UNKNOWN; check | design comparison is manual |
| A6 | Slack via MCP | read, public channels; the optional feedback send channel needs write | feedback (optional send channel), onboarding-check | OPTIONAL; CHECK | the feedback text is forwarded by hand |
| A7 | Grafana via `gcx` (OAuth) | read | none in this base; only if the project adds an observability lookup skill | OPTIONAL | no trace investigation |
| A8 | Repository host token (for example GitLab `read_api`) | read | build download for mobile tests; a repository-digest skill if the project adds one | OPTIONAL; CHECK | builds are downloaded by hand |
| A9 | CI (tool not confirmed) | read jobs, logs, artifacts | ci-failure-analysis, ci-fix | CHECK (not verified) | stages 12–13 ON HOLD |
| A10 | Feature-flag CLI / API | read | none in this base; only if the project adds a flag lookup skill | OPTIONAL; CHECK (does it exist at all) | none |
| A11 | DEV environment: URL, test accounts, VPN if needed | use | automation, exploratory | PER-USER | no test runs |
| A12 | Claude Enterprise seat; Claude Code (CLI / VS Code / Desktop); right to install plugins from the employer's or client's marketplace and to connect MCP servers | seat, install | whole plugin | PER-USER; policy not in writing | plugin cannot be used |
| A13 | Network allowlist or proxy for package and tool downloads (Part B, section "Hosts") | outbound | automation setup | PER-USER | installs fail |

### A2/A3 detail — what "write" means here
- v1 of the skills only prepares drafts. Write access is requested NOW so the request does not block v2, but the skills do not need it to start.
- Writes happen only after the person sees the exact change and confirms it. A hook `guard_jira_write` is planned, not built.
- Minimum rights to ask for (to be confirmed with the Jira / Xray admin): create issue in the QA project; add attachment; transition issues in the QA project; create and edit Test, Test Execution and Test Plan issues in the Xray project; no delete; no project administration.

### A3 — is Xray covered by the Atlassian MCP? (CHECK, not assumed)
Not certain: check. Do not decide in advance. Procedure (no expertise needed):
1. Connect the Jira MCP server the employer or client approves (name and URL UNKNOWN).
2. Ask Claude: "list the tools of the Jira/Atlassian MCP server". Write down whether any tool mentions Xray, test executions, test plans or test steps.
3. Give Claude the key of ONE existing Test issue and ask it to read it. Are the test steps visible in the result?
   - Steps visible -> PASS for read. Repeat with a Test Execution key for statuses.
   - Steps or execution results missing -> NOT COVERED. Then the options are: a separate Xray MCP server, or the Xray API with keys kept by the user (Xray flavour Cloud vs Server/DC is UNKNOWN). Ask IT which one is allowed.
4. Writing: only after step 3 passes, and only on a test project / test issue.

### A4 — Confluence (CHECK)
Ask Claude to run one read-only search for a known page title. Result returned -> PASS. No access or nothing relevant -> note it; analyze-requirements works from Jira and pasted text.

---

## Part B. Environment for automation

Source of versions: an earlier project's package files and setup docs (not included in this base). "Declared" = in `package.json`; "run on" = what those docs say it was run on.

### B1. Tools

| ID | Tool | Version | Needed for | What it is and why |
|---|---|---|---|---|
| B1.1 | Claude Code | current (native install auto-updates) | everything | The AI assistant itself (terminal, VS Code, Desktop). Everything in this project runs through it. |
| B1.2 | Git (Windows: Git for Windows = Git Bash) | any current | repo, bootstrap scripts | Version control; on Windows it also gives a bash shell (Git Bash) that the project scripts use. |
| B1.3 | Node.js | declared >=18; run on 24 -> use 24 | web and mobile tests | Runs the web (Playwright) and mobile (WebdriverIO) test projects and Appium. |
| B1.4 | Python 3 | 3.x | hooks, trace_tree.py, check_updates.py, validate_repo.py | Runs the safety hooks and helper scripts (trace_tree, repo digest, repo validation). |
| B1.5 | `curl`, `jq`, `unzip` | any | build download (bootstrap) | Download and unpack app builds; read JSON output. |
| B1.6 | Playwright (`@playwright/test`) + Chromium | ^1.62.1 (declared). BASELINE = 1.62.1 (stays until the project owner decides) | web tests | The web UI test runner and the browser it drives. |
| B1.6a | Playwright TARGET 1.64.0 | documented only, NOT tested | web tests | Newer release (checked 2026-10-13). Features marked (1.64+) in the Playwright rules and skills are used ONLY after the project moves to 1.64; on 1.62.1 they do not exist. Changes to expect: device `screen` is forwarded; elements in hidden iframes count as hidden; JSX follows tsconfig; `--update-snapshots=missing` now passes. No trial run has been done. |
| B1.7 | WebdriverIO (`@wdio/*`), TypeScript | ^9, ^5 (declared) | mobile tests | The mobile UI test runner and the TypeScript compiler; `npm ci` installs them from package.json. |
| B1.8 | JDK Temurin | 17 | Android | Required by the Android tooling and by Appium's Android driver. |
| B1.9 | Android Studio + SDK + Emulator; AVD Pixel (name `Pixel_7_Pro` or set `ANDROID_AVD`), API 34+, x86_64 on Windows | recent | Android | The Android SDK and the emulator the mobile tests run on. |
| B1.10 | Appium 3.x (global) + driver `uiautomator2` | 3.x | Android | The bridge that lets tests control the Android app. |
| B1.11 | Hardware acceleration: Windows Hypervisor Platform or AEHD; SVM on AMD | | Windows emulator | Without it the emulator is too slow to use. |
| B1.12 | Xcode + Simulator + `xcuitest` driver | | macOS only; iOS is a scaffold until a simulator build exists | The iOS simulator; macOS only; iOS tests are not ready yet. |
| B1.13 | `gcx` (Grafana CLI) | current | OPTIONAL: only with an observability lookup skill | Grafana command line such a skill can use to read traces. |

### B2. Install commands

macOS (Terminal, zsh). Windows (PowerShell, normal user, not Administrator unless stated).
Source tags: [doc] = from official documentation checked on 2026-10-13; [earlier project] = from an earlier project's docs; [mine] = my suggestion, not verified.

| ID | macOS | Windows |
|---|---|---|
| B1.1 | `curl -fsSL https://claude.ai/install.sh \| bash` [doc]; or `brew install --cask claude-code` [doc] | `irm https://claude.ai/install.ps1 \| iex` [doc]; or `winget install Anthropic.ClaudeCode` [doc] |
| B1.2 | `xcode-select --install` (Git comes with it) [mine] | `winget install Git.Git` [mine]; installer: git-scm.com [earlier project] |
| B1.3 | `brew install nvm`, follow its shell-config note, then `nvm install 24` [an earlier project suggests nvm; exact steps mine] | `winget install OpenJS.NodeJS.LTS` [earlier project]; then check the version is 24 |
| B1.4 | `brew install python` [mine] | `winget install Python.Python.3.12` [mine]; the launcher is `py`, not `python3` [earlier project] |
| B1.5 | `brew install jq` (curl and unzip ship with macOS) [earlier project] | `curl.exe` ships with Windows 10+; `winget install jqlang.jq` [mine]; unzip: `Expand-Archive` [mine] |
| B1.6 | in `automation/web`: `npm ci` then `npx playwright install chromium` [earlier project] | same |
| B1.7 | in `automation/mobile/android`: `npm ci` (mandatory: rebuild for your OS) then `npm run typecheck` [earlier project] | same |
| B1.8 | `brew install --cask temurin@17` [earlier project] | `winget install EclipseAdoptium.Temurin.17.JDK` [earlier project] |
| B1.9 | `brew install --cask android-studio`, then Device Manager -> Create Virtual Device -> Pixel, API 34+ [mine; steps from an earlier project] | download from developer.android.com/studio, tick SDK + Emulator; Device Manager -> Pixel, API 34+, x86_64 [earlier project] |
| B1.10 | `npm install -g appium` then `appium driver install uiautomator2` [earlier project] | same [earlier project] |
| B1.11 | not needed (Apple silicon uses arm64 images; the earlier project's docs do not cover this) | Windows Features -> Windows Hypervisor Platform, or install AEHD from SDK Manager (HAXM is obsolete); AMD: enable SVM in BIOS [earlier project] |
| B1.12 | install Xcode from the App Store; then `appium driver install xcuitest` [mine] | not possible on Windows; a cloud device service is an option [earlier project] |
| B1.13 | `brew install gcx` or `curl -fsSL https://raw.githubusercontent.com/grafana/gcx/main/scripts/install.sh \| sh` (installs to `~/.local/bin`) [doc] | Windows install is not described on the docs page checked; options: prebuilt binary from the grafana/gcx GitHub releases, or `go install github.com/grafana/gcx/cmd/gcx@latest` with Go 1.24+ [doc, partial] |

### B3. Environment variables

| Variable | Value | macOS | Windows |
|---|---|---|---|
| `JAVA_HOME` | JDK 17 path | `export JAVA_HOME=$(/usr/libexec/java_home -v 17)` in `~/.zshrc` [earlier project] | `[Environment]::SetEnvironmentVariable('JAVA_HOME','<your JDK 17 path>','User')` [earlier project] |
| `ANDROID_HOME` | SDK path | `export ANDROID_HOME=$HOME/Library/Android/sdk` [mine] | `[Environment]::SetEnvironmentVariable('ANDROID_HOME',"$env:LOCALAPPDATA\Android\Sdk",'User')` [earlier project] |
| `PATH` | add `platform-tools`, `emulator`, `~/.local/bin` | `export PATH="$PATH:$ANDROID_HOME/platform-tools:$ANDROID_HOME/emulator:$HOME/.local/bin"` [mine] | read the User PATH, append `...\Android\Sdk\platform-tools;...\emulator`, write it back. NEVER use `setx` (truncates PATH at 1024 chars) [earlier project] |
| `ANDROID_AVD` | AVD name if not `Pixel_7_Pro` | `export ANDROID_AVD=<name>` [earlier project] | `[Environment]::SetEnvironmentVariable('ANDROID_AVD','<name>','User')` [earlier project] |
| `GITLAB_TOKEN` | your own `read_api` token | set it yourself in your shell profile; never paste it anywhere | set it yourself as a User variable; never paste it anywhere |

After changing variables on Windows, close the terminal and open a new one [earlier project].

### B4. Hosts the installs need (from memory, verify against your proxy errors)
npm registry (`registry.npmjs.org`); Playwright browser download (`cdn.playwright.dev`); Android SDK and Gradle (`dl.google.com`, `maven.google.com`, `repo.maven.apache.org`); Homebrew / winget sources; `claude.ai`, `downloads.claude.ai` (Claude Code installer); `raw.githubusercontent.com` and GitHub releases (gcx); the client's internal GitLab host (UNKNOWN). NOT VERIFIED: the exact host list differs by tool version.

### B5. Start-up order (both OS)
1. Claude Code installed; `claude --version` prints a version; log in with the enterprise account.
2. Git, Node 24, Python.
3. Clone / open the repo folder.
4. Web: `npm ci`, `npx playwright install chromium`.
5. Mobile: JDK 17, Android Studio, AVD, env variables, `npm ci`, `npm run typecheck`, Appium + driver; start the emulator by hand (more reliable than letting Appium start it); `npm run setup:sit` once per new emulator or build [earlier project].
6. Setup helpers from an earlier project (doctor scripts that print OK / WARN / FAIL with a hint) are not in this base; port them if the project needs them (see `automation/README.md`).
7. Hooks and permission floor, ONCE PER MACHINE where this folder is opened in Code or VS Code (the hooks file is per machine because the Python launcher differs: `python3` on macOS, usually `py -3` on Windows):
   - first time ever: do it in a COPY of the folder, so a wrong setting cannot damage the working copy;
   - `bash tools/apply-trusted-changes.sh --dry-run` (shows what it would change, writes nothing), then the same command without `--dry-run`; on Windows run it from Git Bash;
   - approval: the AI QA Process Lead. If you are not that person, ask before running it;
   - if you moved the folder from another computer by copying, do not keep that computer's `.claude/settings.local.json` (delete it first, or the script will only write `settings.local.json.proposed`);
   - restart Claude Code in the folder, then run the hook rows E22-E25 below (`/onboarding-check hooks`).
   Verified only in a sandbox so far; real macOS and Windows runs are NOT VERIFIED.
7a. Skills copy, after every `git pull` or any change under `plugins/qabase/skills/` (same command on macOS and on Windows from Git Bash; copies only, deletes nothing):
   - `bash tools/sync-skills.sh`, then `diff -rq plugins/qabase/skills .claude/skills`: it must print nothing about `differ` or `Only in plugins/...`;
   - the copies in `.claude/skills/` are generated, never edit them by hand; approval as for any trusted asset.
8. Run `/onboarding-check` (Part E).

### B5a. Flow per platform (the onboarding skill asks which one you have, then shows only that flow)
Do the steps in this order; a later step may need an earlier one. Install commands are in B2, checks in Part E.

macOS:
1. Claude Code; log in with the enterprise account.
2. Git (`xcode-select --install`).
3. Node 24 via nvm.
4. Python 3 (`python3`).
5. `jq` (curl and unzip are already there).
6. Web tests: `npm ci`, Playwright Chromium.
7. JDK 17.
8. Android Studio, SDK, AVD (an arm64 image on Apple silicon is not covered by the earlier project's docs: NOT VERIFIED).
9. Environment variables in `~/.zshrc`; open a new terminal.
10. Appium and `uiautomator2`.
11. Optional, iOS only: Xcode, simulator, `xcuitest` (iOS tests are not ready yet).
12. `gcx` (Grafana CLI).
13. Hooks and permission floor script (B5 step 7).
14. MCP and access checks (Part E rows E9-E21).

Windows (native; Git for Windows gives Git Bash):
1. Git for Windows first (Git Bash is used by the project scripts).
2. Claude Code from PowerShell; log in.
3. Node 24 via `winget`.
4. Python 3; the launcher is `py -3`.
5. Web tests: `npm ci`, Playwright Chromium.
6. JDK 17.
7. Android Studio, SDK, AVD x86_64, API 34+.
8. Hardware acceleration: Windows Hypervisor Platform or AEHD; SVM in BIOS on AMD. Check with `emulator -accel-check`.
9. Environment variables with `[Environment]::SetEnvironmentVariable` (never `setx`); open a NEW terminal.
10. Appium and `uiautomator2`.
11. `gcx`: no install command is documented for Windows (prebuilt binary or `go install`): NOT VERIFIED.
12. Hooks and permission floor script, from Git Bash (B5 step 7).
13. MCP and access checks (Part E rows E9-E21).
Not available on Windows: Xcode, iOS simulator (iOS needs macOS).
Other setups (WSL, Linux, a remote VM) are NOT covered by this file; the skill says so and does not guess.

### B6. Hooks and the Python launcher (macOS and Windows)
`python3` does not exist on every machine: on Windows it may be missing or a Microsoft Store stub, and the working launcher is `py -3`. The committed `settings.json` therefore carries only the permission floor. The hooks live in `.claude/settings.local.json` (not committed), generated per machine by `tools/apply-trusted-changes.sh`, which tries `python3`, then `py -3`, then `python` and writes the one that actually runs.
- Run it yourself, after QA Lead approval: `bash tools/apply-trusted-changes.sh --dry-run`, then without `--dry-run`. It asks before each write, never overwrites an existing settings file (it writes `*.proposed`), never deletes.
- Windows: run it from Git Bash. The hook command uses `$CLAUDE_PROJECT_DIR`, which assumes a POSIX shell; whether Claude Code runs hooks through Git Bash on Windows is NOT VERIFIED. Rows E24 and E25 below test exactly this.
- Tested in a sandbox only (macOS/Linux behaviour and the `py -3` fallback with a stub); not on a real Windows machine.


### B7. MCP servers cost context
Connect only approved servers that you use now (`.mcp.json`, ai-rules item 12). The definitions of a server's tools take context before the first message, even if no tool is called. Check the cost: `/context` shows the MCP part; disconnect or disable a server you do not need in this session. Source: a course text (third-party, 2026-10-13); the `/context` view is the check, not yet run on a client machine.

---

## Part E. First-open checklist (what `onboarding-check` runs)

Result per row: PASS / FAIL / NOT CHECKED, with the next step. "Claude" = Claude may run it (read-only). "You" = the person runs it, because it involves a login or a credential.

| # | Check | Who | PASS when | If not PASS |
|---|---|---|---|---|
| E1 | `claude --version`; `claude doctor` | You | version printed; doctor shows no errors | reinstall per B2 |
| E2 | `git --version` (Windows also: Git Bash present) | Claude | version printed | install Git |
| E3 | `node -v` | Claude | v24.x (>=18 is the declared minimum) | install Node 24 |
| E4 | Python: macOS `python3 --version`; Windows `py -3 --version` | Claude | 3.x | install Python |
| E5 | `java -version`, `echo $JAVA_HOME` (Windows: `$env:JAVA_HOME`) | Claude | 17.x and path set | install JDK 17 |
| E6 | `adb version`; `emulator -list-avds`; `emulator -accel-check` | Claude | adb prints a version; AVD listed; acceleration reported available | fix Android SDK / acceleration |
| E7 | `appium -v`; `appium driver list --installed` | Claude | 3.x; `uiautomator2` installed | install Appium and driver |
| E8 | in `automation/web`: `npx playwright --version` | Claude | version printed; baseline 1.62.1 (1.64.x only if the project moved, see B1.6a) | `npm ci` |
| E9 | `gcx config check` (login done by You in your own terminal) | Claude (login: You) | check passes | log in with OAuth; ask for Grafana access |
| E10 | GitLab token valid: `curl -s -o /dev/null -w '%{http_code}\n' -H "PRIVATE-TOKEN: $GITLAB_TOKEN" https://<gitlab-host>/api/v4/user` (Windows: `curl.exe`, `$env:GITLAB_TOKEN`). Host UNKNOWN | You | prints 200 | 401 = bad or expired token; 403/404 = no project access; no answer = VPN / network |
| E11 | MCP servers connected: `/mcp` in Claude Code shows each server connected | You | Jira, Slack, Figma (if used) listed as connected | add the server, or ask IT |
| E12 | Jira read: Claude runs ONE read-only search for your own open issues | Claude | issues returned | request A1 |
| E13 | Xray coverage: procedure in A3 with one known Test issue key | Claude (you give the key) | steps visible | see A3 |
| E14 | Confluence read: one search for a known page title | Claude | page found | note; not a blocker |
| E15 | Slack read: one single-keyword channel search | Claude | channels returned | request A6 |
| E16 | Figma read: you give one frame link | Claude | frame content returned | NOT CHECKED without a link |
| E17 | Feature-flag CLI present: `command -v <cli>` (name UNKNOWN) | Claude | found | CHECK with the team whether it exists |
| E18 | CI: open one pipeline page yourself and confirm you can read job logs | You | logs readable | request A9 |
| E19 | DEV: open the DEV URL, log in with your own test account, in your own browser | You | login works | request an account; no accounts are known yet |
| E20 | Network: `npm view @playwright/test version` | Claude | prints a version | proxy / allowlist (A13) |
| E21 | Plugin loaded: skills appear in the `/` menu (as `/qabase:...` if installed as a plugin) | You | skills listed | see plugin README |
| E22 | Permission floor active: `.claude/settings.json` exists and contains the deny rules (e.g. `Read(**/.env)`) and ask rules (e.g. `Edit(CLAUDE.md)`) | Claude (reads the file) | file exists with those rules | run `bash tools/apply-trusted-changes.sh --dry-run`, then without it (B5 step 7), after approval by the AI QA Process Lead |
| E23 | Hooks configured for this machine: `.claude/settings.local.json` exists and its launcher is the one that works here (E4) | Claude (reads the file) | file exists; launcher matches E4 | same script, once per machine (B5 step 7); do not copy another machine's file |
| E24 | Hook firing test, secrets: ask Claude to run `cat .env.hookcheck` (the file does not exist; the test only looks at the block message) | You | Claude reports the call was BLOCKED with the text "Command touches a secret file" | a normal permission prompt or "No such file" = hook did NOT fire: FAIL; check E23, restart Claude Code, see B6 |
| E25 | Hook firing test, trusted assets: ask Claude to run `echo x >> plugins/qabase/CHANGELOG.md`; when the prompt appears READ it, then answer No | You | the prompt text says "This command may modify a trusted asset" | the plain Bash prompt without that text = hook did NOT fire: FAIL |
| E29 | Deny firing test, strict profile (QA machines): after `bash tools/apply-trusted-changes.sh --profile qa`, restart Claude Code and ask Claude to edit `CLAUDE.md` (add a blank line). Do not confirm anything | You | Claude reports the edit was DENIED by a permission rule, with no prompt to approve | a prompt asking to approve = the profile is not active or `deny` did not apply: FAIL; check `.claude/settings.json` equals `tools/settings.qa.json`. Maintainer profile is expected to prompt |
| E26 | Skills copy is current: `diff -rq plugins/qabase/skills .claude/skills` (Git Bash on Windows) | Claude (reads only) | no line with `differ` or `Only in plugins/` | run `bash tools/sync-skills.sh` yourself (B5 step 7a), then repeat the diff |
| E27 | Connected MCP servers and loaded plugins are on the approved list (Part A): paste `/mcp` and the plugin list | You (Claude compares names) | every name is on the approved list | name not on the list: ask the AI QA Process Lead; do not disconnect for them here |
| E28 | Start-up weight: paste `/context` from a fresh session | You (Claude reads the numbers) | recorded as reported by user; note a skill listed twice, large MCP or memory parts | see B7; nothing is changed by the check |

Output of the skill: a table of the rows above with PASS / FAIL / NOT CHECKED, a list of what the person has to do themselves, and a line "not checked: ...". It never prints a token, never logs in, never installs.

## Part F. Open questions

1. Which MCP servers does the client allow, and under what names (Jira, Xray, Figma, Slack, Confluence)? UNKNOWN.
2. Xray flavour (Cloud or Server/DC) and whether the Atlassian MCP covers it: A3 procedure.
3. CI tool (UNKNOWN; see `ci/README.md`).
4. Does a feature-flag CLI/API exist; may production flag state be read?
5. DEV URL and test accounts (no data file exists).
6. Windows work computer: is it Windows? Hooks command (`py` vs `python3`) and every Windows command above are unverified.
7. Where the client's marketplace lives and who approves plugins.

## Sources
- Claude Code install and Windows notes: https://code.claude.com/docs/en/setup (read 2026-10-13)
- gcx install: https://grafana.com/docs/grafana-cloud/as-code/observability-as-code/grafana-cli/gcx/installation.md (read 2026-10-13)
- Earlier project docs (setup guides, package files; not included in this base)
