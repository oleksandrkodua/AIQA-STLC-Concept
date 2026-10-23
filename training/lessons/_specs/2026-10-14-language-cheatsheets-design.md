# Language cheat sheets and booklet: specification (DRAFT)

Status: DRAFT v0.1, 2026-10-14. Not approved. Approver: the AI QA Process Lead.
Scope: four new one-page cheat sheets (TypeScript, Playwright, WebdriverIO + Appium, Python) and one combined PDF booklet with the two existing sheets. Language of all sheets: English (same as sheets 1 and 2).
Nothing here is built yet. Sources: `training/lessons/cheatsheets/build_cheatsheets.py`, `cheatsheets/README.md`, `_specs/2026-10-14-colors-design.md` (only lines 1-60 were read; section 5 "Meaning of colours" was NOT read in full), root `CLAUDE.md` (stack table).

## 1. Decisions already made with the author

| Question | Decision |
|---|---|
| Sheets | TypeScript, Playwright, WebdriverIO + Appium, Python. Order of work: in that order. |
| Why WebdriverIO | `CLAUDE.md` names the mobile stack as "WebdriverIO + Appium"; Appium alone does not cover what the team writes. |
| Why Python | Python is in the repository as infrastructure: hooks (`.claude/hooks/*.py`), eval runners (`evals/hooks/run_*_tests.py`), `evals/validate_repo.py`, `tools/build-skills-index.py`, the cheat sheet builder. It is NOT the language of the web/mobile tests (TypeScript). api-agent-kit is a Node project (`package.json`, `package-lock.json`) whose only Python is one stdlib-only linter, `scripts/lint_collection.py` (imports `re`, `sys`, `pathlib`; no `requirements.txt` or `pyproject.toml`). |
| Python check, 2026-10-14 (VERIFIED by grep and file reads) | The eval runners do NOT use pytest: `run_hook_tests.py` imports `json, os, subprocess, sys, tempfile`, `run_runcheck_tests.py` imports `os, subprocess, sys, tempfile`; each runs a hand-written case list and exits 0 only if all match. The only "pytest" hits in this repository are a regex in `mods/verification-guard/hooks/ledger.ts` and a test string in its `logic.test.mjs`, which only RECOGNISE a pytest command. No `requests`, `httpx` or Python API-check plan found: the only API entry is `CLAUDE.md` "api / api-agent-kit / NEXT, not MVP", Node and Bruno. Searched: this repository (`CLAUDE.md`, `context`, `decisions`, `docs`, `policy`, `automation`, `README.md`, `evals`, `tools`, `mods`). NOT searched: other repositories, tickets, chats, client conversations. |
| Length | One A4 landscape page per new sheet. |
| Booklet | One combined PDF for screen and a shared link. Print imposition (fold and staple, A5, A3) is out of scope. |
| Language | English. |
| Reference image | The Playwright cheat sheet image supplied by the author is a structure reference only. Its content is NOT copied (it has typos, a duplicated block and patterns Playwright discourages). |

## 2. Page template

- Page: A4 landscape, 1123x794 (same as sheets 1 and 2). Palette, fonts and measurement code come from `build_cheatsheets.py`; the course palette is not changed.
- Header: title (28 pt), subtitle, amber rule, status chips on the right.
- Body: 3 columns, 6 to 8 blocks per page. Block titles are numbered ("1. Install") and all in the same colour. No per-block colours.
- Block types:
  - TABLE: command to what it does (the existing `table()` helper).
  - CODE: monospace card, at most 8 lines, no syntax colouring; keywords in bold.
  - RULES: beige band with bullets (as on sheet 2).
- Chips: status chips keep exactly the meaning in section 5 of the colours spec: IN USE / confirmed (green), DRAFT / NOT RUN (amber), UNVERIFIED (red), NOT USED (dashed grey). On the language sheets they describe the state of a snippet or of a tool in the project, never advice.
- Advice (do this / don't do this) is NOT a status and gets no status colour. It is shown by the words `PREFER` and `AVOID` on a plain chip (colours spec section 5: "Plain: structure only, no status") and by position: RULES blocks use two labelled lists, "Prefer" and "Avoid". No new chip style is added. Reason: see section 6a.
- Footer on every sheet: `Tool: <name> <version> · checked <date> · source: <link>`. While `automation/` is not ported, the version is written as `version: UNKNOWN`.
- Meaning is never carried by colour alone: every chip has a word and a mark.

## 3. Content (blocks per sheet)

### 3.1 TypeScript for QA
1. Setup: node, `tsconfig` (`strict`), how to run.
2. Types every day: primitives, arrays, union, optional, `type` vs `interface`.
3. Functions and async: `async/await`, `Promise`, return types.
4. Objects and data: destructuring, spread, literal unions, typing JSON.
5. Modules: `import/export`, named vs default.
6. Classes (for Page Object): `constructor`, `private`, `readonly`.
7. Compile errors and fixes: table of typical errors.
8. Rules: PREFER `unknown` and narrow types; AVOID `any`, `@ts-ignore`, unneeded `!`.

### 3.2 Playwright
1. Install and run: main CLI commands.
2. Test structure: `test`, `describe`, hooks, fixtures.
3. Locators: PREFER role, label, test id; AVOID long XPath and CSS chains.
4. Actions.
5. Assertions: web-first with auto-wait; AVOID `waitForTimeout`.
6. Config: `projects`, `retries`, `trace`, `baseURL`.
7. Debug: `--ui`, trace viewer, `codegen`, `--debug`.
8. Page Object skeleton and project rules: DEV only, never production.

### 3.3 WebdriverIO + Appium (mobile)
1. Setup: Appium server, drivers (UiAutomator2, XCUITest), Appium Inspector.
2. Capabilities: `platformName`, `appium:*`, with the warning that a build may open on PROD.
3. Selectors: accessibility id, id, UiAutomator, iOS predicate.
4. Actions and gestures.
5. Waits and assertions.
6. `wdio.conf`: specs, capabilities, services, reporters.
7. Debug: logs, Inspector, `adb` / `xcrun`.
8. Rules: an emulator is not a real device; state which one produced the evidence. iOS is a scaffold only.

### 3.4 Python for QA scripts
1. Setup: venv, pip, running a script.
2. Basics: types, f-strings, comprehensions.
3. Files and paths: `pathlib`, `json`, `csv`.
4. CLI scripts: `argparse`, `subprocess`, exit codes.
5. Regex and logs.
6. Test-runner pattern: a table of cases with expected values, `subprocess.run`, `tempfile`, exit code 0 only if every case matches (the pattern of `evals/hooks/run_hook_tests.py`).
7. stdin / stdout JSON: read JSON from stdin, print JSON, parse another script's output (the hook protocol used by `.claude/hooks/*.py` and their runners).
8. Rules: no secrets in code, environment variables only, never production; stdlib first.

Decided 2026-10-14 from the check in section 1: the earlier HTTP (`requests` / `httpx`) and pytest blocks are DROPPED because nothing in the repository uses them. The footer says "Not covered: pytest, requests/httpx; add a block if either is introduced." Blocks 6 and 7 replace them and describe code that exists here. Block 5 (Regex and logs) also covers the linter pattern (`re` + `pathlib`, as in api-agent-kit's `lint_collection.py`).

## 4. Files

- New: `cheatsheets/build_langsheets.py` (imports `Sheet`, `table`, `box` from `build_cheatsheets.py`), `cheatsheets/content/typescript.py`, `playwright.py`, `wdio_appium.py`, `python.py` (data only), `cheatsheets/build_booklet.py`.
- Output names: `cheatsheet-3-typescript`, `cheatsheet-4-playwright`, `cheatsheet-5-wdio-appium`, `cheatsheet-6-python` (each .svg .png .pdf), and `booklet.pdf`.
- `build_cheatsheets.py` and the outputs of sheets 1 and 2 are NOT modified, with one exception listed in section 7.

## 5. Booklet assembly

- Page order (8 pages): cover; sheet 1 p1; sheet 1 p2; sheet 2; sheets 3, 4, 5, 6.
- The cover carries the title, the contents list with page numbers, the build date and the status DRAFT. There is no separate contents page.
- `build_booklet.py` reads the existing per-sheet PDFs and merges them with PyMuPDF (`insert_pdf`). It does not re-run any sheet build, so sheets 1 and 2 stay byte-identical in their own files.
- The PDF gets bookmarks (outline) per sheet.
- Sheet 2 is still a PLACEHOLDER; the booklet shows it as is and the cover lists it as "placeholder".

## 6. Verification and definition of done

A sheet or the booklet is "built" when all of these are true. Each is checked by running something, not by reading.

1. `python3 build_langsheets.py` and `python3 build_booklet.py` exit 0 and write every file in section 4.
2. Each new sheet is exactly 1 page; `booklet.pdf` has exactly 8 pages and 4 or more bookmarks.
3. Overflow check is part of the builder: every wrapped text must fit its block; the build fails with the block name if not.
4. Palette check: every fill and stroke colour in the new SVGs is in the palette set of `build_cheatsheets.py`. No new colours or chip styles are added. The build fails otherwise.
5. Visual check: each PNG is opened and looked at by the author of the build; the result is reported as "looked at", not as automated.
6. Footer present on every sheet with tool, version, date, source.
7. Every code snippet is either run against a real test or script (no chip) or carries UNVERIFIED. The final report states the count of each. Mobile snippets cannot be VERIFIED without a device or emulator; the report says which one was used or that none was.
8. Source links in footers are fetched at build time, or listed as "not checked".
9. No secrets, no real customer data, no production URLs in the content.
10. The chip mapping in section 2 was checked against section 5 of the colours spec on 2026-10-14 (result in 6a). At build time a check confirms that no chip with a green, amber or red style carries the words PREFER or AVOID.

## 6a. Check against the colours spec section 5 (2026-10-14)

Read in full: section 5 of `_specs/2026-10-14-colors-design.md` (VERIFIED by reading). Note that this section is itself a PROPOSAL, not approved, so this check shows consistency with a draft, not with an approved rule.

The first mapping (PREFER = green IN USE style with a check mark; AVOID = dashed grey NOT USED style with a cross mark) CONFLICTS with section 5 in three places:
1. Green means "in use, confirmed, passed". A green PREFER next to a red UNVERIFIED snippet sends two opposite signals, and a reader can take green as "verified".
2. Dashed grey outline is "always paired with the words NOT USED". AVOID is advice about a technique, not the state "this project does not use it"; the same outline would blur the two.
3. The cross mark is listed under red (failed, blocked). A grey AVOID with a cross breaks that pairing.

Not a conflict: red was already excluded for AVOID.

Decision (PROPOSAL, pending approval of this spec): advice uses the Plain style with the words PREFER / AVOID and two-list position, as in section 2. Trade-off accepted: advice is less eye-catching than a coloured chip. Alternative, not chosen: ask the colours spec owner to add an "advice" row (for example a neutral tint) to section 5; this changes an approved-track document and is out of scope here.

Confidence in the final report is derived from this list: any unchecked item caps it (rule 6 in `.claude/rules/qa-rules.md`).

## 7. Open items (decisions needed, not guessed)

- Sheet 2's subtitle says "Cheat sheet 2 of 2". In a six-sheet series this is wrong. Proposal: change that one string in `build_cheatsheets.py` and rebuild sheets 1 and 2. This edits a file that is not a trusted asset but changes approved-looking output, so it needs your yes.
- Chip mapping PREFER / AVOID: CHECKED 2026-10-14, the first mapping conflicted, replaced by Plain chips (section 6a). Needs your approval of the new mapping.
- Conditional blocks 3.4.6 and 3.4.7: RESOLVED 2026-10-14 (dropped and replaced, see section 3.4). Re-open only if pytest or a Python HTTP library enters the repository or the client's plans.
- `cheatsheets/README.md` table must be updated at implementation (new rows, booklet row).

## 8. Out of scope

Print imposition (folded booklet, A5, A3); dark or projector variants; Russian or Ukrainian versions; syntax-coloured code; sheets for tools not named above (Git, Claude Code commands beyond sheet 1, api-agent-kit); content for iOS beyond "scaffold only".

## 9. Risks accepted

- Tool commands change between versions; until versions are pinned the footer says UNKNOWN and snippets are UNVERIFIED.
- Block choice per sheet comes from general QA practice, not from the team's actual usage (not measured).
- One page per sheet forces cuts; the WDIO + Appium sheet is the tightest.
