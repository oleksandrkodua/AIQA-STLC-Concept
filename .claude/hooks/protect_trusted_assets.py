#!/usr/bin/env python3
"""PreToolUse hook (DRAFT, EXPERIMENTAL): ask the human before editing trusted assets
(trusted-asset protection): CLAUDE.md, .claude/**, plugins/qabase/**, policy/**, evals/**, context/sources.md.

Decision = "ask" (the user sees a prompt). Bash is checked heuristically: a write-like
command that names a trusted path asks too. Heuristic only; the permission rules are the floor.
Fail-open on internal errors.
"""
import json, re, sys

TRUSTED = re.compile(r"(^|[/\s'\"=])(CLAUDE\.md|\.claude/|plugins/qabase/|policy/|evals/|context/sources\.md)")
WRITE_LIKE = re.compile(r"(\bsed\s+-i|\btee\b|\bmv\b|\bcp\b|\brm\b|\btruncate\b|>>?\s*\S|\bgit\s+(checkout|restore|reset)\b)")

def ask(reason):
    print(json.dumps({"hookSpecificOutput": {"hookEventName": "PreToolUse",
        "permissionDecision": "ask", "permissionDecisionReason": reason}}))
    sys.exit(0)

def main():
    try:
        d = json.load(sys.stdin)
        tool = d.get("tool_name", ""); ti = d.get("tool_input", {}) or {}
        if tool in ("Edit", "Write", "MultiEdit", "NotebookEdit"):
            p = str(ti.get("file_path") or ti.get("notebook_path") or "")
            if TRUSTED.search(p):
                ask(f"'{p}' is a trusted asset. Show the change and rationale; QA Lead approval needed (ai-rules 9).")
        elif tool == "Bash":
            c = str(ti.get("command", ""))
            if TRUSTED.search(c) and WRITE_LIKE.search(c):
                ask("This command may modify a trusted asset (ai-rules 9). Confirm.")
    except SystemExit:
        raise
    except Exception as e:
        sys.stderr.write(f"protect_trusted_assets: internal error, failing open: {e}\n")
    sys.exit(0)

if __name__ == "__main__":
    main()
