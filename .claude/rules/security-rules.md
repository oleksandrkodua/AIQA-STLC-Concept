# Security rules

| Field | Value |
|---|---|
| ID | RULE-SEC |
| Purpose | Secrets, environments, data, trusted-asset protection |
| Scope | Everything. Highest priority. |
| Priority | 1 (overrides all other rules) |
| Owner / approver | QA Lead and the security owner of the employer or client (UNKNOWN until Discovery) |
| Status | DRAFT — not approved |
| Review date | not set |
| Sources | A layered architecture design (security and trusted-asset sections); rules from earlier QA tooling (adapted; validity for a given employer UNCONFIRMED); rule 7: `decisions/PROPOSAL-security-rule-7-2026-10-23.md` |
| Change history | v0.1 created 2026-10-07; neutral base 2026-10-20; rule 7 rewritten and approved 2026-10-23 by Oleksandr Kukhtinov (repository owner, acting as QA Lead) |

## Environments

1. Work only against DEV (start) or other approved non-production environments. Production
   endpoints, production accounts and production data are prohibited.
2. DEV vs SIT naming differs per project. Until it is resolved, use only the environment
   named in `context/discovery.md`.
3. Mobile builds may open on PROD by default. Switching to the test environment is a
   mandatory first step, verified before the run (see `mobile-rules.md`).

## Secrets and data

4. No secrets, tokens, passwords, session cookies or webhook URLs in chat, files, commits,
   logs, screenshots or test data. Use environment variables or the approved secret store.
5. If a secret appears in context: do not reproduce it, do not store it, tell the user to
   rotate it, escalate.
6. No real customer or production data in tests or test data. Use synthetic or anonymised
   data only.
7. Do not read `.env*`, key files, credential stores or token files. Permission deny rules are
   the first layer, not a guarantee: the Claude Code documentation applies Read deny rules to
   Grep, Glob, `@file` mentions and IDE context on a best-effort basis, and to Bash only for
   the file commands it recognizes (not to a command or script that reads files without
   naming them). Hooks are a second layer and let the action proceed on any exit code other
   than 2. For a hard boundary use the OS sandbox where the project allows it. Never
   `@`-mention a secret file. If one is read by mistake, follow rule 5.

## Trusted-asset protection

8. Edits to CLAUDE.md, `.claude/**`, `policy/**` and `evals/**` require explicit human
   approval ("ask", not "allow").
9. Never force-push, rewrite shared history, delete branches or tags, run migrations or
   deploys, or touch shared environments. Destructive local commands are named and confirmed
   first.

## Tools and agents

10. Only approved MCP servers; pin versions where the tool allows it. Third-party skills and
    plugins are read in full before installing.
11. Hooks and mods are EXPERIMENTAL until their acceptance tests pass
    (`evals/hooks-acceptance.md`). A hook is not counted as a control before then.
12. Evidence files (screenshots, logs, videos) may contain employer or client data. They stay out of
    commits (`runs/` ignored) unless reviewed.
