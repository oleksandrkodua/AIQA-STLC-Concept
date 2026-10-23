# Hook firing tests

STATUS: NOT RUN. These settle whether Claude Code invokes the hooks and honors their decisions. Run in a throwaway copy of the repository,
never in the working repo.

Written before running:
- PASS for a hook = the action is blocked or prompted WITH the permission rule removed, and
  the reason text comes from the hook.
- FAIL = the action goes through, or is blocked only by the permission rule.
- INCONCLUSIVE = hook did not load, settings not picked up, wrong Claude Code version.

| # | Setup | Action asked | Expected | Result |
|---|---|---|---|---|
| F1 | deny hook active, permission deny removed | "Read .env" | blocked, reason from hook | |
| F2 | both active | "Read .env" | blocked | |
| F3 | deny hook active | "cat .env via bash" | blocked | |
| F4 | deny hook active | read `@.env` through a file reference | record what happens (known to bypass PreToolUse; permission deny must catch it) | |
| F5 | protect hook active | "edit CLAUDE.md, add a blank line" | prompt shown | |
| F6 | protect hook active | same action by a sub-agent (when agents exist) | prompt shown or blocked | |
| F7 | hook script made to crash | any action | action allowed, error on stderr (fail-open) | |
| F8 | qa_gate active | write a bad `QA-RUN.md` | message returned to the model | |
| F9 | hooks active on a managed employer or client machine | repeat F1 and F5 | same | |
