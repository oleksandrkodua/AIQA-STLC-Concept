# Playwright in Our Project: Setup and Daily Use

> Note on this copy. Taken from an earlier architecture project; the body is unchanged (draft v0.2, sources checked 2026-09-22). The baseline is Playwright 1.62.1; 1.64.0 is documented as target only. V-numbers are ids of that project's verification log (not included in this base). The two TODO lines in the guide stay open. Not run in this base.

> Status: draft v0.2 · Sources: official Playwright and Claude Code docs, checked 2026-09-22.
> `TODO` marks project-specific details that still need to be filled in.
> `CONFIRM` marks things inferred from our existing instruction files that need a human to confirm.

Every step ends with a **Check** line: what you should see if the step worked. If you don't see it, stop and go to [Troubleshooting](#10-troubleshooting).

Commands are the same on Windows and macOS unless a step says otherwise. On Windows, use **PowerShell** or the VS Code terminal.

**How far this guide has been tested**

| Path | Status |
|---|---|
| macOS, personal machine | Partly walked: project scaffolding and a test run (§2.3, §4) |
| macOS, work machine (managed) | Not walked yet |
| Windows | Not walked yet — written from documentation only |

If you are the first person to walk a path, note what failed and tell the repo owner; the **Check** lines tell you where it broke.

**On a managed work laptop**, expect extra friction that a personal machine does not have: admin rights for global installs (`npm install -g`, Claude Code), a proxy or VPN for downloads, and MDM or antivirus blocking downloaded browser binaries. If a step fails for one of these reasons, record it in [Troubleshooting](#10-troubleshooting) rather than working around it silently.

---

## 0. What you'll have at the end

- Playwright installed in the project and running from the terminal and from VS Code.
- You can record a test with Codegen, debug it, and open the trace of a failed test.
- (Optional) Claude Code can drive a browser through the Playwright CLI.

## 1. Prerequisites

| Tool | Needed for | Requirement | Check |
|---|---|---|---|
| OS | Everything | Windows 11+ (or WSL) · macOS 14 (Sonoma)+ | — |
| Git | Cloning the repo; Claude Code on Windows | Any recent version | `git --version` |
| Node.js | Playwright | Latest 22.x, 24.x or 26.x | `node -v` |
| npm | Installing packages | Comes with Node.js | `npm -v` |
| pnpm | **Only if** the repo uses pnpm (see §2.2) | — | `pnpm -v` |
| VS Code | Editing and running tests | Recent version | — |
| Claude Code | **Only for** §9 (AI-assisted work) | Recent version; paid Claude plan (`CONFIRM`) | `claude --version` |

Playwright's browsers are **not** installed here; `npx playwright install` downloads them in §2.

### 1.1 Install, in this order

Close and reopen the terminal after each install so the new command is on your PATH.

| Step | macOS | Windows |
|---|---|---|
| 1. Git | Run `git --version`; if missing, macOS offers to install Command Line Tools — accept | Install **Git for Windows** from https://git-scm.com/downloads/win (defaults are fine) |
| 2. Node.js | LTS installer from https://nodejs.org | LTS installer from https://nodejs.org |
| 3. VS Code | https://code.visualstudio.com | https://code.visualstudio.com |
| 4. pnpm (only if needed) | `npm install -g pnpm` | `npm install -g pnpm` |
| 5. Claude Code (only for §9) | `curl -fsSL https://claude.ai/install.sh \| bash` | In **PowerShell**: `irm https://claude.ai/install.ps1 \| iex` |

Notes:
- Claude Code's native installer does not need Node.js. On Windows it relies on Git for Windows, which is why Git comes first.
- Using several Node versions for different projects? A version manager (nvm on macOS, nvm-windows on Windows) is an option, but not required for this guide.

`TODO: corporate proxy / VPN — is one needed to download browsers? If yes, document HTTPS_PROXY here.`

**Check:** `git --version`, `node -v` (starts with `v22`, `v24` or `v26`) and `npm -v` all print versions. If you installed them: `pnpm -v` and `claude --version` too.

## 2. Install Playwright

### 2.1 Does the repo already have Playwright?

Our instruction files run tests from a `playwright/` folder (`CONFIRM`). Check from the repo root:

| | Command |
|---|---|
| macOS | `ls playwright/playwright.config.ts` |
| Windows (PowerShell) | `Test-Path playwright\playwright.config.ts` |

- File exists (macOS prints the path, Windows prints `True`) → go to **2.2**.
- File missing → go to **2.3**.

### 2.2 Repo already has Playwright (normal case)

```bash
git clone TODO-repo-url
cd TODO-repo-folder/playwright
npm ci
npx playwright install --with-deps
```

`npm ci` installs exactly the versions pinned in `package-lock.json`, so everyone gets the same setup.

> **npm or pnpm?** Both install packages; pnpm is faster and uses less disk. What matters is using the **same one as the repo**: a `package-lock.json` file means npm, a `pnpm-lock.yaml` file means pnpm. This guide assumes npm (`CONFIRM`).

### 2.3 First-time setup (done once, by the repo owner)

From the folder where tests will live — **a real project folder, never your home directory** (`~`), see [Troubleshooting](#10-troubleshooting):

```bash
mkdir -p ~/projects/<project-name>/playwright   # only if the folder doesn't exist yet
cd ~/projects/<project-name>/playwright
npm init playwright@latest
```

Run it **inside the `playwright/` subfolder**, not in the repo root. The Playwright project
keeps its own `package.json`, lockfile and config so it can later be moved to its own
repository with a single `git subtree split`. A `package.json` in the repo root would tie the
two together.

Answer the prompts:
- TypeScript or JavaScript → **TypeScript**
- Tests folder → `tests`
- Add a GitHub Actions workflow → answer **yes** only if [Appendix A](#appendix-a-project-discovery-repo-owner) shows the repo is on GitHub and nobody objects; otherwise **no**. If yes, the job must run with `working-directory: ./playwright`
- Install Playwright browsers → **yes**

Re-running the command later is safe: it does not overwrite existing tests.

It creates:

```
playwright.config.ts   # browsers, timeouts, retries, reporters
package.json
package-lock.json
tests/
  example.spec.ts      # sample test
```

**Check (both 2.2 and 2.3):** `npx playwright --version` prints a version number.

## 3. VS Code extension

1. Open Extensions (`Ctrl+Shift+X` on Windows, `Cmd+Shift+X` on macOS).
2. Install **Playwright Test for VSCode** by Microsoft (id `ms-playwright.playwright`).
3. Open the **Testing** view (flask icon in the left sidebar).

**Check:** your tests appear in the Testing view, and a green ▶ appears next to each `test(...)` in the editor.

## 4. Run tests

| Task | Command |
|---|---|
| All tests (headless, in parallel) | `npx playwright test` |
| Watch the browser | `npx playwright test --headed` |
| One browser | `npx playwright test --project=chromium` |
| One file | `npx playwright test tests/example.spec.ts` |
| By test title | `npx playwright test -g "title text"` |
| Only last failures | `npx playwright test --last-failed` |
| UI Mode (best for daily work) | `npx playwright test --ui` |
| Open HTML report | `npx playwright show-report` |

**Check:** `npx playwright test` ends with a line like `N passed`, and `show-report` opens a report in your browser.

### 4.1 Cross-browser runs

Each browser is a **project** in `playwright.config.ts`. A plain `npx playwright test` runs every test once **per project**, so three browser projects mean three runs of each test.

| Engine | Project name (default config) | What it stands for |
|---|---|---|
| Chromium | `chromium` | Chrome, Edge |
| Firefox | `firefox` | Firefox |
| WebKit | `webkit` | Safari-like engine |

Things people get wrong:

- **WebKit is not Safari.** It is the engine Safari uses, built by Playwright. Close, but not the same browser. A WebKit pass is not a Safari sign-off.
- **Branded Chrome / Edge** (the real installed browser, not bundled Chromium) are a separate project setting (`channel`). Add them only if the product must be signed off on them.
- **Mobile in the config is emulation** (screen size, touch, user agent), not a real phone.
- **More browsers = longer runs.** CI time grows roughly with the number of projects.
- **A browser-specific skip needs a reason.** `test.skip(browserName === 'webkit', '<reason + ticket>')`, never a silent skip.

`TODO: which browsers the product officially supports → see Appendix A.2. The projects in playwright.config.ts should match that list, not the defaults.`

**Check:** in the HTML report, each test appears once per browser project, with the project name shown next to it.

## 5. Anatomy of a test

```ts
import { test, expect } from '@playwright/test';

test('user sees the dashboard after login', async ({ page }) => {
  await page.goto('/login'); // TODO: set baseURL in playwright.config.ts
  await page.getByLabel('Email').fill('user@example.com');
  await page.getByRole('button', { name: 'Sign in' }).click();
  await expect(page.getByRole('heading', { name: 'Dashboard' })).toBeVisible();
});
```

Three rules people most often get wrong:

1. **No manual waits** (`waitForTimeout`, sleeps). Playwright waits for elements to be ready before acting.
2. **Assert with `await expect(...)`.** These assertions retry until the condition is met or time runs out. `waitForSelector` is *not* an assertion.
3. **Find elements the way a user would:** `getByRole`, `getByLabel`, `getByText`, `getByTestId` — not CSS classes or XPath.

`TODO: project conventions — Page Object Model or not, data-testid policy, folder structure, naming. Will live in qa-project-context.md.`

## 6. Record a test with Codegen

```bash
npx playwright codegen TODO-environment-url
```

- Click around in the browser that opens; code appears in the Inspector window.
- Add assertions with the toolbar buttons: visibility, text, value.
- **Pick Locator**: hover an element to get its locator.
- Copy the code into a test file.

Codegen gives a draft, not a finished test: review assertions and names by hand.

**Check:** the recorded test, pasted into a file, passes with `npx playwright test <file>`.

## 7. Debugging and traces

| Tool | When | Command |
|---|---|---|
| UI Mode | Local work, step-by-step view | `npx playwright test --ui` |
| Inspector | Step through with pauses | `npx playwright test <file>:<line> --debug` |
| Trace | Investigate a failure (especially from CI) | Locally: `npx playwright test --trace on`, then `show-report` → trace icon |

By default the config records a trace on the first retry of a failed test (`trace: 'on-first-retry'`), and retries are enabled only on CI.

**Check:** a failed test in the HTML report has a Traces section that opens.

## 8. Updating Playwright

```bash
npm install -D @playwright/test@latest
npx playwright install --with-deps
npx playwright --version
```

`TODO: who updates the version in the repo, and how often.`

## 9. Using Playwright with Claude Code (optional)

Claude Code can run in three places; all of them are Claude Code:
- the **Claude Code extension** in VS Code,
- the `claude` command in the **VS Code terminal**,
- the **Code** section of the Claude Desktop app.

Prerequisite: Claude Code installed (§1.1, step 5). For the VS Code option, also install the **Claude Code** extension by Anthropic from the Extensions view.

Two different tools can give Claude a browser, and they are not interchangeable:

| Tool | Who uses it | What for |
|---|---|---|
| **Playwright CLI** (`@playwright/cli`) | Claude Code, day to day | Open a page, find a locator, check behaviour while writing or fixing a test |
| **Playwright MCP** | Only the official Playwright Test Agents | Long agentic loops that keep browser state (e.g. the test healer) |

Microsoft's own guidance is that coding agents such as Claude Code are best served by the CLI: it keeps token use lower, because large tool schemas and page snapshots are not loaded into the model's context. We follow that. **We do not add our own MCP server** — the only MCP entries in `.mcp.json` are the ones `npx playwright init-agents` writes for the official agents.

### 9.1 Install the Playwright CLI

```bash
npm install -g @playwright/cli
playwright-cli install --skills
```

`TODO: confirm whether the CLI can be pinned per repo instead of installed globally (see verification log V15), and where --skills installs its skills (V14).`

### 9.2 Verify

**Check:**
1. `playwright-cli --version` prints a version.
2. In a Claude Code session, ask: *"Use the Playwright CLI to open https://example.com and tell me the page heading."* → Claude runs CLI commands and answers with the heading.

### 9.3 Official Test Agents (separate setup)

`npx playwright init-agents --loop=claude` creates agent definitions under `.claude/agents/` and the MCP entries they need. Two rules:

- **Never hand-edit the generated agent files.** They are regenerated on Playwright updates and your edits would be lost. Project-specific rules live in `.claude/rules/playwright-rules.md`, in the seed test, or in our own skills.
- **Keep the agents' artifacts inside `playwright/`.** The default convention puts `specs/` (Markdown plans) and `tests/` in the repo root; point them at `playwright/specs` and `playwright/tests` instead, so the test project stays self-contained.
- Agent definitions themselves stay in the repo-root `.claude/agents/`: they belong to the AI configuration, not to the test project. Test code never references them, so this does not break the split.
- `specs/` holds **working drafts**, not test cases. Test cases live in the TMS. A planner describes the app as it behaves today, so it can record a defect as an expected result.
- Commit the generated files, so `git diff .claude/agents/` after an update shows exactly what Playwright changed.

`TODO: run this once an environment is available; see verification log V1, V2, V8.`

### 9.4 Known limits (not verified for our setup)

- A user-reported bug says MCP servers added from the CLI may not show up in the VS Code extension's MCP list. Check with `claude mcp list` in the terminal.
- Whether the Desktop **Code** section reads project `.mcp.json` and `.claude/skills/` the same way has not been checked.

## 10. Troubleshooting

| Symptom | Likely cause | Fix |
|---|---|---|
| `node` / `npx` not found | Terminal opened before Node was installed | Close and reopen the terminal (restart VS Code) |
| macOS: `EPERM ... scandir '/Users/<you>/.Trash'` or `EACCES ... watch '/Users/<you>/.rnd'` | The command was run from the home directory (`~`). Playwright scans and watches the current folder and hits protected macOS files | `cd` into the project folder first. Never run `npx playwright ...` from `~` (seen on a real macOS install) |
| Windows: URL with `&` gets cut off in a command | PowerShell treats `&` as a command separator | Wrap the URL in quotes |
| Windows: PSReadLine / PowerShell warnings in test output | Terminal noise, unrelated to tests | Ignore; read the Playwright summary line (`X passed / Y failed`) |
| Browser download fails | Proxy or firewall | `TODO: proxy settings` |
| `npm install -g ...` fails with a permissions error | Managed machine without admin rights | `TODO: ask IT, or use a per-project install instead` |
| Playwright browsers install but won't launch | MDM / antivirus blocking downloaded binaries | `TODO: ask IT to allow the Playwright browsers folder` |
| | | `TODO: add real issues as the team hits them` |

## Appendix A. Project discovery (repo owner)

Fill this in once when setting Playwright up in a project. Answers go into `qa-project-context.md` (`TODO: create`), and the `TODO`s above get resolved from it. Each question has a way to find the answer yourself; ask a person only when the check comes back empty.

### A.1 Where the code and CI live

| Question | How to find out | Answer |
|---|---|---|
| Where is the repo hosted? | `git remote -v` → the host in the URL (`github.com`, `gitlab...`, `bitbucket.org`, `dev.azure.com`, other) | `TODO` |
| Is there a CI pipeline already? | Look for CI files in the repo root (commands below) | `TODO` |
| Which CI system? | The file name tells you (table below) | `TODO` |
| Who owns the pipeline? | Last authors of the CI file: `git log --format="%an" -- <ci-file>` | `TODO` |
| Can QA add a job, or is it a request to the owner? | Ask the owner | `TODO` |

Find CI files:

| | Command |
|---|---|
| macOS | `ls -d .github/workflows .gitlab-ci.yml Jenkinsfile azure-pipelines.yml bitbucket-pipelines.yml .circleci 2>/dev/null` |
| Windows (PowerShell) | `Get-Item .github\workflows, .gitlab-ci.yml, Jenkinsfile, azure-pipelines.yml, bitbucket-pipelines.yml, .circleci -ErrorAction SilentlyContinue` |

| File found | CI system |
|---|---|
| `.github/workflows/` | GitHub Actions |
| `.gitlab-ci.yml` | GitLab CI |
| `Jenkinsfile` | Jenkins |
| `azure-pipelines.yml` | Azure DevOps |
| `bitbucket-pipelines.yml` | Bitbucket Pipelines |
| `.circleci/` | CircleCI |
| nothing | No CI yet → the decision goes to whoever owns the repo, not QA |

**Rule of thumb:** use the CI where the repo is hosted. Don't introduce a second CI system for tests only.

### A.2 Project setup

| Question | How to find out | Answer |
|---|---|---|
| Package manager | Lockfile in the Playwright folder: `package-lock.json` = npm, `pnpm-lock.yaml` = pnpm | `TODO` |
| Playwright location | `playwright/playwright.config.ts` exists? (see §2.1) | `TODO` |
| Test environment URL(s) | Ask the team; then set `baseURL` in `playwright.config.ts` | `TODO` |
| Test accounts / auth | Ask the team; never commit passwords | `TODO` |
| Proxy / VPN for downloads | Does `npx playwright install` work on the office network? | `TODO` |
| Admin rights on work laptops | Try `npm install -g pnpm` on a work machine | `TODO` |
| Which OS do teammates use | Ask the team; Windows users need §1.1 Windows column | `TODO` |
| Test management system (TestRail or other) | Ask the team | `TODO` |
| Supported browsers (and versions / OS) | Product support matrix, or ask product owner | `TODO` |
| Which browsers run on every commit vs. nightly | Decide with the CI owner (cost vs. coverage) | `TODO` |

## Sources

- Playwright: https://playwright.dev/docs/intro · /docs/writing-tests · /docs/running-tests · /docs/codegen-intro · /docs/trace-viewer-intro
- Playwright MCP: https://playwright.dev/mcp/introduction
- Claude Code MCP scopes: https://code.claude.com/docs/en/mcp
