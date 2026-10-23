# Agents and routines policy — DRAFT

STATUS: DRAFT v0.1. No agent or routine is enabled in this base. Sub-agents are off by default;
how to add one: `optional/agents/README.md`. Routines from earlier QA tooling come back as
skills only after review and evals.

## Preconditions to enable any agent or routine
1. Its clause in `ai-usage-policy.md` is agreed (item 10).
2. Identity and purpose written: name, owner, what it may read, what it may write.
3. Tools listed, minimum set. Writes are off by default. Credentials are never visible to it.
4. Hook and permission floor tested (`evals/hooks-firing.md`).
5. Audit done with the LLM Council prompt (`evals/agent-audit.md`) and the findings answered.
6. Acceptance tests written and PASS: allowed task works, forbidden task refused, injection
   fixtures not obeyed (`evals/injection-tests.md`), failure behaves safely.

## Operating states (every agent defines all three)
- **CONTINUE**: inside scope and tolerances.
- **ESCALATE**: ambiguity, scope exceeded, conflicting sources, unexpected data → stop and
  hand to a human with what it saw.
- **STOP**: unpredictable behavior or damage → halt; a human can revoke it immediately.
  How a human stops it is written in the agent's file (kill switch).

## Rules
- Agents do not call other agents. Orchestration is one defined script or skill.
- Agent output is untrusted until validated; a review agent has no write permission.
- Each decision is reconstructable within 15 minutes: input, context read, tools called,
  output. Run journals in `runs/` carry it. (The 15-minute target is a goal from training
  material, not measured.)
- A change to an agent's definition is a trusted-asset change: QA Lead approval.

## Candidate agents (not enabled)
| Candidate | Source | Purpose | Why not now |
|---|---|---|---|
| qa-orchestrator | QA operating disciplines | run planning, limits, RECONCILE, verdict | skills + rules cover the first version; audit first |
| read-only lookup agent (ownership, logs, traces) | per project | answer "who owns this" or "what happened to this request" without filling the main context | needs approved access to the project's systems |
| tracker digest agent | per project | summarize tickets, read-only | needs tracker access and approval |
