# 03 Enforcement — what stops a bad action

STATUS: DRAFT. Whether Claude Code behaves exactly like this on the client's machines is
OPEN until the hook firing tests pass (`evals/hooks-firing.md`). Do not describe hooks as active controls before they pass.

```mermaid
sequenceDiagram
  participant M as Model
  participant P as Permission rules (floor)
  participant H as PreToolUse hooks
  participant U as Human
  participant T as Tool
  M->>P: tool call, e.g. Read .env
  alt matches deny rule
    P-->>M: denied
  else matches ask rule
    P->>U: ask
    U-->>P: approve or reject
  else allowed so far
    P->>H: continue
    alt hook denies
      H-->>M: denied with reason
    else hook asks
      H->>U: ask
      U-->>H: approve or reject
    else hook allows or crashes (fail-open)
      H->>T: run
      T-->>M: result
      Note over M,T: PostToolUse hooks may nudge, e.g. bad QA-RUN.md
    end
  end
```

Why a floor: hooks fail open on errors, and `@` file references bypass PreToolUse, so
anything that must never happen is also a permission rule. Why advisory PostToolUse: it can
nudge the model back, it cannot undo what already ran.
