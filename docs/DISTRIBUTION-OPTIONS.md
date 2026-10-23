# How the package reaches other QAs: two options worked through (DRAFT)

Status: DRAFT by Claude, 2026-10-13. The real route is UNKNOWN (doc Part E open question 7: where the employer's or client's marketplace lives and who approves plugins). Commands marked [mine] come from my general knowledge of Claude Code and are NOT verified against the current docs (the docs check was not run). Verify on the work machine before relying on them.

## What is in the package
- `plugins/qabase/` — the plugin (source of truth for skills).
- `.claude-plugin/marketplace.json` at the repo root — the repository can act as a marketplace with the plugin at `./plugins/qabase`.
- `.claude/skills/` — generated copy of the plugin skills (`tools/sync-skills.sh`), a fallback for a machine without the plugin.
- `.claude/rules/`, `CLAUDE.md`, hooks (applied by `tools/apply-trusted-changes.sh`) — repo-level, work with or without the plugin.

## Option A: client marketplace (plugin installed from it)
| Aspect | Detail |
|---|---|
| Who does what | IT/client approves and hosts the marketplace; each QA installs the plugin from it. |
| Skills come from | the plugin only. |
| `.claude/skills/` copies | NOT wanted: they would be listed a second time (the docs agent said both load; plugin skills are namespaced `/qabase:...`), about +2.8k tokens per session. |
| Repo folder | rules, `CLAUDE.md`, hooks, docs; no skills copy committed. |
| Update | the plugin version in the marketplace; people update the plugin. |
| Risk | the marketplace does not exist yet (Part E Q7); first-day setup depends on IT. |

## Option B: git clone (or an archive) of the folder, no company marketplace
| Aspect | Detail |
|---|---|
| Who does what | each QA clones the repo and opens it in Claude Code. |
| Skills come from | `.claude/skills/` copies (committed and checked) — they work from the first open. Optional upgrade: add the repo itself as a local marketplace and install the plugin from it [mine: `/plugin marketplace add <path or repo>`; not verified]. |
| `.claude/skills/` copies | committed; kept in sync by `tools/sync-skills.sh`; validator and onboarding E26 catch a stale copy. |
| Repo folder | everything, skills copy included. |
| Update | `git pull`, then `bash tools/sync-skills.sh`. |
| Risk | if a person also installs the plugin, skills appear twice; onboarding E28 (`/context`) is the place to notice it. |

## Design that works under both (recommended while the route is unknown)
1. Keep the plugin as the single source; `.claude/skills/` is generated and committed. Nothing changes now.
2. The doc and onboarding tell the person plainly: use ONE of the two. Option B people do not install the plugin; Option A people delete the generated copy [their own action; `rm` on their machine or a documented `tools` script, TBD].
3. Add a small `tools/sync-skills.sh --remove` (or a documented manual step) only after the route is known; not built now.
4. The validator's context budget counts the plugin descriptions once (Option A reality). If Option B is chosen, count them from `.claude/skills/` instead (same number, one copy).
5. The navigator index (`skills-index.json`) is built from `plugins/qabase/skills/` in both options and shipped inside the plugin folder, so it works in both.

## Decision table (fill in when the route is known)
| Question | If marketplace (A) | If git clone (B) |
|---|---|---|
| Commit `.claude/skills/`? | no (add to `.gitignore`, keep the generator) | yes (as now) |
| Onboarding step 0 | "install plugin `qabase` from the marketplace" | "run `bash tools/sync-skills.sh`" |
| E21 | skills appear as `/qabase:...` | skills appear without prefix |
| Duplicate risk | low | present if the plugin is also installed |

## To verify on the work machine (read-only)
1. Fresh session, `/context`: are skills listed once or twice when both exist?
2. Does a local-directory marketplace install work and copy the plugin into the plugin cache (later repo edits need an update)? [mine]
3. What the client's policy says about third-party marketplaces and local plugins (Part E Q7, A12).
