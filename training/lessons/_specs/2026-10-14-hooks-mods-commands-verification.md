# Verification: hooks, mods, slash commands (DRAFT)

Status: DRAFT v0.1, 2026-10-14. Checked by the `claude-code-guide` agent against official Anthropic documentation, fetched 2026-10-14. Nothing was run on our machines (the firing test is still open). The project's Claude Code version is UNKNOWN, so version-dependent items are marked [VER]. This note is the source for the cheat sheet and for lessons on permissions and hooks, and on MCP, plugins and mods.

Sources: `code.claude.com/docs/en/` pages `hooks-guide`, `permissions`, `skills`, `plugins/mods/overview`, `plugins/mods/reference`, `plugins/cli-reference`, `permission-modes`, `commands`, `vs-code`; `claude.com/blog/claude-code-mods`; `anthropic.com/news/donating-the-model-context-protocol-and-establishing-of-the-agentic-ai-foundation`.

## Hooks

| Claim | Verdict | Note |
|---|---|---|
| Run outside the process as commands | PARTLY | Shell commands; docs also list HTTP requests and prompts as hook types |
| Exit code 2 blocks a tool call | CONFIRMED | Any other exit code is a non-blocking error: the action proceeds (exceptions per event, e.g. WorktreeCreate) |
| Can add context or log | CONFIRMED | `additionalContext` on UserPromptSubmit; logging via the script |
| Cannot redraw the UI or rewrite output | PARTLY | UI drawing is a mod capability. "Cannot rewrite model output" is not stated outright |
| Event list | CONFIRMED | SessionStart, UserPromptSubmit, PreToolUse, PostToolUse, Stop, Notification and others; the agent did not read the whole table |
| Fail-open | PARTLY | Non-2 exit: proceeds. Missing script and timeout behaviour: NOT FOUND |
| `@file` references bypass hooks | NOT FOUND | Docs: Read deny rules apply to @file mentions best-effort |
| Deny wins over allow | CONFIRMED | Order: deny, ask, allow. A hook cannot override deny. A mod handling `tool.check` can approve what a deny rule refuses unless managed settings hold the deny [VER] |

## Mods

| Claim | Verdict | Note |
|---|---|---|
| Official feature, 1 Oct 2026 | CONFIRMED | Blog "Customize Claude Code with mods in TypeScript" |
| Run inside the process as JS/TS functions | CONFIRMED | Docs, not the blog |
| Rewrite prompt, hold or change a tool call, redraw UI, /commands without a model turn | CONFIRMED | Events `prompt.submit`, `tool.call`, `ui.render` |
| Flag `CLAUDE_CODE_ENABLE_FUNCTION_HOOKS` | CONTRADICTED | Ignored from 2.1.287; mods are on by default |
| Minimum build | CONFIRMED [VER] | CLI 2.1.287; Desktop 2.1.286 |
| 10-second limit | CONFIRMED, mods only | Settings hooks default to 10 minutes |
| `claude plugin marketplace add`, `claude plugin install <name>@<marketplace>` | CONFIRMED | `plugins/cli-reference` |
| Runs with your permissions | CONFIRMED | Also "mods aren't sandboxed". The phrase "someone else's binary" is not in the docs |
| blast-radius, replay-theater | CONFIRMED as samples | Anthropic sample repo `claude-code-playground`, shared without support, not in the blog post |

## Slash commands by surface

yes = typed command documented; menu = UI control instead; no = docs say unavailable; ? = docs silent (not tested).

| Command | CLI | VS Code | Desktop |
|---|---|---|---|
| /context | yes | ? | yes* |
| /compact | yes | yes | yes |
| /clear | yes | ? | yes* |
| /usage | yes | yes | menu (usage ring) |
| /model | yes | yes [2.1.284+] | menu (dropdown) |
| /resume | yes | ? | yes (local sessions) |
| /permissions | yes | menu [2.1.269+] | no ("isn't available in this environment") |
| /hooks | yes | menu [2.1.269+] | no* |
| /mcp | yes | yes | yes* |
| /agents | yes (reminder text; interactive UI only on 2.1.197 and earlier) | ? | yes* |
| /memory | yes | menu [2.1.274+] | yes* |
| /init | yes | ? | yes* |
| /doctor | yes | ? | yes* (bundled skill, screenshot) |
| /config | yes | mentioned | yes (opens Settings) |
| /rewind (alias /checkpoint, /undo) | yes | menu (checkpoints) | yes* |

\* Author test, Desktop Code tab, 2026-10-14: the author typed `/` and reported that every command above is offered except `/hooks`. Screenshots seen for `/hooks` (no match), `/doctor` (the bundled skill "Health-check the user's Claude Code setup", shown as `doctor`) and `/memory` (the visible results are only skills with "memory" in the name, so the built-in `/memory` is the author's statement, not shown on the screenshot). Presence in the menu is not a run: a dialog command can still answer "isn't available in this environment". Still unknown: VS Code for `/context`, `/clear`, `/resume`, `/agents`, `/init`, `/doctor`. An independent check of the docs (commands, desktop, vs-code, checkpointing, memory, sub-agents, context pages) found no statement on these cells, so the docs cannot settle them.

Plan mode: CLI Shift+Tab, `--permission-mode plan` or `/plan`. VS Code: mode indicator or `/plan` [2.1.280+]. Desktop: mode selector next to the send button; Shift+Tab does not cycle.
Checkpoints do not track file changes made through Bash.

## Other

| Claim | Verdict | Note |
|---|---|---|
| MCP under the Linux Foundation | CONFIRMED | Donated 9 Dec 2025 to the Agentic AI Foundation, a directed fund under the Linux Foundation |
| A2A under the Linux Foundation | UNVERIFIED | Secondary snippets only; the primary source was not read |
| Skills: description always in context, body on invoke | CONFIRMED | The docs do not name "name" and "description" together |

## Consequences for the project (proposals, none applied)

1. `.claude/rules/security-rules.md` rule 7 says "@ file references bypass hooks". Not supported by the docs. Propose a rewrite (QA Lead approval needed; trusted asset). Also note the docs call the @file deny behaviour best-effort, so the rule's reliance on deny rules for `.env` files needs a second look.
2. `mods/README.md` mentions the flag `CLAUDE_CODE_ENABLE_FUNCTION_HOOKS`. Obsolete from 2.1.287; propose a fix.
3. Cheat sheet and lesson mockups updated with these results.

Provenance: ai-generated (agent report, Sonnet 5.5 session), 2026-10-14; human-confirmed: pending.
