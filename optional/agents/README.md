# Optional: agents

STATUS: DRAFT. Agents are OFF in this base. `.claude/agents/` stays empty until every condition in `policy/agents-policy.md` ("Preconditions to enable any agent or routine") is met. An agent file without its audit, acceptance tests and agreed policy clause is a defect.

## Why optional
Skills plus human gates cover the first version of the process (`docs/schemes/08-mvp-chain.md`). Add an agent only for work that clearly needs its own context window or its own tools, for example a read-only investigation whose full log trail should not fill the main session.

## How to add one (in this order)
1. Agree the clause in `policy/ai-usage-policy.md`.
2. Copy `agent.template.md` to `.claude/agents/<name>.md` and fill every field; write UNKNOWN instead of leaving a field blank.
3. Pick the lowest rung of `autonomy-ladder.md` that does the job. Start at GUIDED.
4. Write the acceptance tests from `acceptance-tests.template.md` before anyone else uses the agent.
5. Test the hook and permission floor (`evals/hooks-firing.md`) and run the audit (`evals/agent-audit.md`).
6. Approval of the agent and of every later change: QA Lead. A change to an agent definition is a trusted-asset change.

## Rules that never change
Agents do not call other agents. Agent output is untrusted until validated. Critical actions (production changes, privilege changes, governance changes, irreversible actions) are never autonomous.

## Source
Derived from the agent sections of a layered architecture design (agent architecture, autonomy model, governance, boundary testing, lifecycle). Not tested in any project.
