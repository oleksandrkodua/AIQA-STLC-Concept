---
name: <kebab-case>
description: <what it does, when to use it, when NOT to use it (names the neighbouring skill or agent)>
tools: <minimum set; read-only by default>
---
# <Agent name>

STATUS: DRAFT | AUDITED | ACCEPTED | RETIRED   Version: x.y.z

## 1. Identity and purpose
Name, owner (a named person), one paragraph: what it decides and what it never decides.

## 2. Capability boundary
What it may read; what it may write (default: nothing); what it must never do.

## 3. Tool permissions
Each tool and MCP server, marked read or write, with the permission rule that enforces it. Hooks fail open; permission rules are the floor.

## 4. Guardrails
Deny rules; data it must not see; allowed environments (non-production only).

## 5. Human in the loop
Which outputs a person must approve before anything leaves the session.

## 6. Operating states
- CONTINUE: <inside scope and tolerances>
- ESCALATE: <ambiguity, scope exceeded, conflicting sources, unexpected data: stop and hand to a human with what it saw>
- STOP: <unpredictable behavior or damage: halt>
- Limits: at most <n> tool calls and <n> iterations per run (a number is required; "unlimited" is not allowed). Reaching a limit is STOP, reported with what was done so far.

## 7. Autonomy rung and risk tier
Rung (see `optional/agents/autonomy-ladder.md`) and the actions allowed at each tier. CRITICAL is never autonomous.

## 8. Auditability
What is recorded for every run (input, context read, tools called, output) and where (`runs/`). A decision must be reconstructable.

## 9. Kill switch
The exact steps by which a human revokes the agent immediately.

## 10. Incident response
Who is told when it misbehaves, and what is rolled back.

## 11. Triggers and skills
When it starts and which skills it uses. It never starts another agent.

## 12. Acceptance tests
Link to the filled `optional/agents/acceptance-tests.template.md`.

## 13. Change control and retirement
Who approves a change, when it is reviewed, when it is retired.
