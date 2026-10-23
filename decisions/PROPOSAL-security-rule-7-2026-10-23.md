# Proposal: rewrite RULE-SEC rule 7

STATUS: APPROVED 2026-10-23, applied in b89afb4 (option A). Approved by Oleksandr Kukhtinov (repository owner, acting as QA Lead). Trusted asset: `.claude/rules/**`, see `ai-rules.md` rule 9.

| Field | Value |
|---|---|
| Target | `.claude/rules/security-rules.md`, rule 7 (plus the Sources and Change history rows) |
| Approver | the QA Lead (in this repository: the AI QA Process Lead) |
| Provenance | ai-generated (Claude Sonnet 5.5), 2026-10-23; human-confirmed: pending |
| Sources | `training/lessons/_specs/2026-10-14-hooks-mods-commands-verification.md` (agent report against Anthropic documentation, fetched 2026-10-14); the permissions page `code.claude.com/docs/en/permissions`, re-read 2026-10-23 for the passages quoted below |

## 1. Current text

> 7. Do not read `.env*`, key files, credential stores or token files. This is enforced by
>    permission deny rules, because hooks can fail open and `@` file references bypass hooks.

## 2. What is wrong with it

| # | Claim in rule 7 | Verdict | Evidence |
|---|---|---|---|
| a | "`@` file references bypass hooks" | NOT FOUND in the documentation | Verification note, hooks table: "NOT FOUND. Docs: Read deny rules apply to @file mentions best-effort". The docs describe a limit of deny rules, not a hook bypass |
| b | "enforced by permission deny rules" | OVERSTATED | Permissions page (2026-10-23): Claude "makes a best-effort attempt to apply `Read` rules to all built-in tools that read files like Grep and Glob, to `@file` mentions in your prompts, and to the selection and open-file context that a connected IDE shares". Read and Edit deny rules apply to built-in file tools and to file commands Claude Code recognizes in Bash (`cat`, `head`, `tail`, `sed`, `tee`) and redirections; they do not apply to a command that reads files without naming them (for example `grep -r pattern .`) or to a script that opens files itself |
| c | "hooks can fail open" | PARTLY CONFIRMED | Verification note: exit code 2 blocks; any other exit code is a non-blocking error and the action proceeds. Behaviour for a missing script or a timeout: NOT FOUND |
| d | Deny rules protect `.env*` today | VERIFIED for the file tools, UNKNOWN for the rest | `.claude/settings.json` (equal to `tools/settings.shared.json`) denies `Read(./.env)`, `Read(./.env.*)`, `Read(**/.env)`, `Read(**/.env.*)`, `*.pem`, `*.key`, `**/secrets/**`, `**/.secrets/**`. No firing test has been run (`evals/hooks-firing.md`: NOT RUN) |

What the docs say to use for a hard boundary (same page, same date): "For OS-level enforcement that blocks all processes from accessing a path, enable the sandbox", and permissions and the sandbox are described as "complementary security layers", to be used together.

Also confirmed: rules are evaluated deny, then ask, then allow; the first match wins.

## 3. Proposed replacement (option A, recommended)

```
7. Do not read `.env*`, key files, credential stores or token files. Permission deny rules are
   the first layer, not a guarantee: the Claude Code documentation applies Read deny rules to
   Grep, Glob, `@file` mentions and IDE context on a best-effort basis, and to Bash only for
   the file commands it recognizes (not to a command or script that reads files without
   naming them). Hooks are a second layer and let the action proceed on any exit code other
   than 2. For a hard boundary use the OS sandbox where the project allows it. Never
   `@`-mention a secret file. If one is read by mistake, follow rule 5.
```

Option B (shorter, same facts):

```
7. Do not read `.env*`, key files, credential stores or token files. Deny rules and hooks are
   best-effort (`@file`, Grep, Glob, IDE context; hooks fail open), not a boundary. The
   boundary is the OS sandbox, where available. Never `@`-mention a secret file.
```

If approved: rule 7 text, the Sources row (adds this proposal) and the Change history row (adds "rule 7 rewritten 2026-10-23, approver: <name>"). Status stays DRAFT. Nothing else in the file changes.

## 4. Not decided here (for the QA Lead)

1. Is the sandbox available and allowed on the machines of a given project? UNKNOWN (Discovery: whether Claude Code is allowed on employer or client machines). If not, the rule should say what replaces it: secrets kept outside the project tree.
2. The `.secrets/` folder: already covered by `Read(**/.secrets/**)` in the permission floor (checked 2026-10-23). Nothing to add.
3. The version of Claude Code on the project: UNKNOWN. The page read describes the current version; older builds are NOT VERIFIED.
4. Not tested on a real machine: whether a deny rule blocks an `@file` mention of `.env` in this repository. A firing test would turn "best-effort" into a measured result.

## 5. Side effects checked

- `CLAUDE.md` does not repeat the "bypass hooks" claim: not affected.
- The remaining mentions of the claim are analyses of it (the verification note and the course mockups), not rules.
- "Hooks fail open" elsewhere in the repository is the confirmed part of the claim and stays valid.
- The permission floor already includes `Bash(*JIRA_PAT*)` as a deny: pattern rules are a floor, not a control (same limit as above).
