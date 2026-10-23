# Working rules for the course materials

STATUS: DRAFT v0.1, 2026-10-23. Rules the course owner gave while the course was being built, collected here so that any session (local or cloud) starts from the same ground. Not approved by the QA Lead.

## 1. Claims about Claude Code are checked against the documentation

Before a statement about Claude Code (hooks, mods, slash commands, where a command works) goes on a slide or a cheat sheet, check it against the official Anthropic documentation (`code.claude.com/docs`). Mark each item as one of:
- docs-confirmed;
- tested by the author (with the date; an asterisk on the sheet);
- unknown (a "?").

Why: several claims in source material and in this project's own rules turned out wrong or unsupported (hooks "passive", the flag `CLAUDE_CODE_ENABLE_FUNCTION_HOOKS`, "`@file` bypasses hooks"), and an earlier session once said a file mentioned something that it did not.

How to apply:
- Grep or read the file before saying where something is mentioned.
- A sub-agent report is model output: re-open at least the key documentation pages yourself and say which ones you re-read.
- The author's own test is evidence; record it as "tested by the author" with the date, not as docs-confirmed. A command being offered in the `/` menu is not a run.
- Do not call a project's own mods "official Anthropic" even if Anthropic has samples with the same names.
- Hooks and mods are not run on a real project yet (`evals/hooks-firing.md`: NOT RUN); say "docs-confirmed, not run here".
- Edits to `CLAUDE.md`, rules, skills and hooks need QA Lead approval: propose, do not apply.

Documentation pages used so far: `commands`, `desktop`, `vs-code`, `hooks-guide`, `permissions`, `checkpointing`, `memory`, `sub-agents`, `skills`, `plugins/mods/overview`, `plugins/mods/reference`, `plugins/cli-reference` (all under `https://code.claude.com/docs/en/`). Results: `lessons/_specs/2026-10-14-hooks-mods-commands-verification.md`.

## 2. Slides and diagrams

- Each lesson slide needs its own layout and its own effect from `lessons/_template/animations` (A1-A10, B1-B8; `RANKING.md`). Fifteen copies of one card template was rejected.
- Deliver visuals as files in the repository or as a published artifact, not as inline widgets in the chat (declined by the course owner).
- Palette: `lessons/_specs/2026-10-14-colors-design.md` (DRAFT): paper `#F9F3E5`, ink `#231F1A`, amber `#E0A030`, forest `#1E4A2E`, IBM Plex Sans and Mono.
- Meaning of colour (proposal, not approved): green = in use, confirmed; amber = draft, not run, attention; red = unverified, blocked, failed; dashed grey = not used; thick ink outline = a human step or gate. Meaning is never carried by colour alone: pair it with a word or a mark.
- The last frame of every effect must read without motion (a PDF shows only that). Animations loop (about every 7 seconds) and need a Replay control and a way to play them when reduced motion is on.
- Slide text is English. Chat replies follow the language of the person writing.
- Each slide carries a mini-map of the six slots: Model, Instructions, Tools, Guardrails, Memory, Proof.

## 3. Building the cheat sheets

Edit the lists at the top of `lessons/cheatsheets/build_cheatsheets.py`, then run `cd training/lessons/cheatsheets && python3 build_cheatsheets.py` (not with `python3 -I`: PyMuPDF is a user-site package). It writes `.svg`, `.png` and `.pdf`. Sheets are SVG because headless Chrome can be blocked by a sandbox and PyMuPDF's HTML renderer drops cell backgrounds and dashes (dashed outlines render solid in PNG and PDF).

Only one session at a time edits `build_cheatsheets.py` and `lessons/_mockups/diagrams-mockup.html`: check file timestamps and re-read before editing.

## 4. Open items carried over (state of 2026-10-14, still open)

| Item | State |
|---|---|
| Course structure | A proposal adds two lessons (session modes with model and effort; how to write a request, with practice on the project skills) and two slides (feedback and change rules; first run and troubleshooting), renumbering the course 0-15. Not confirmed by the course owner; `lessons/COURSE-OUTLINE.md` still has 0-13 plus the bonus |
| Slash commands in VS Code | `/context`, `/clear`, `/resume`, `/agents`, `/init`, `/doctor`: not checked; the table in the verification note keeps "?" |
| `/memory` in the Desktop app | The author's statement, not seen on a screenshot |
| Hooks and mods | Firing tests NOT RUN |
| Contrast of the provisional red pair | Not computed; dark theme and phone width of the published artifact not checked |

Provenance: ai-generated from earlier working notes, 2026-10-23; human-confirmed: pending.
