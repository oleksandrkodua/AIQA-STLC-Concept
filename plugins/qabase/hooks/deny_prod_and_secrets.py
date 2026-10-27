#!/usr/bin/env python3
"""PreToolUse hook (DRAFT, EXPERIMENTAL): deny reads/writes of secret files and any tool call
that mentions a production host listed in prod-hosts.txt.

Protocol assumed (Claude Code hooks): JSON on stdin with tool_name and tool_input;
deny = JSON on stdout with hookSpecificOutput.permissionDecision = "deny", exit 0.
That protocol is unverified until the hook is observed firing (`evals/hooks-firing.md`).

On any internal error it returns "ask" (a person decides) and writes a note to stderr. The permission
deny rules in settings.draft.json are the floor under this hook.
Limits: heuristic string matching; cannot see inside scripts or `@` file references.
"""
import json, os, re, sys

SECRET_BASENAME = re.compile(
    r"^(\.env(\..+)?|.*\.pem|.*\.key|.*\.p12|id_rsa.*|id_ed25519.*|\.slack_webhook|"
    r"credentials(\..+)?|secrets?(\..+)?|\.netrc)$", re.I)
SAFE_BASENAME = re.compile(r"^\.env\.(example|sample|template)$", re.I)
SECRET_IN_CMD = re.compile(
    r"(^|[\s\"'=/])(\.env(\.[A-Za-z0-9_-]+)?|[^\s\"']+\.(pem|key|p12)|id_rsa[^\s\"']*|\.slack_webhook|\.netrc)(?=$|[\s\"';|&])")
READ_VERBS = re.compile(r"\b(cat|less|more|head|tail|grep|rg|awk|sed|source|bat|strings|xxd|od|cp|mv|scp|curl|base64)\b|^\s*\.\s")

def allow():
    sys.exit(0)

def deny(reason):
    print(json.dumps({"hookSpecificOutput": {"hookEventName": "PreToolUse",
        "permissionDecision": "deny", "permissionDecisionReason": reason}}))
    sys.exit(0)

def ask(reason):
    print(json.dumps({"hookSpecificOutput": {"hookEventName": "PreToolUse",
        "permissionDecision": "ask", "permissionDecisionReason": reason}}))
    sys.exit(0)

def prod_hosts():
    p = os.path.join(os.path.dirname(os.path.abspath(__file__)), "prod-hosts.txt")
    try:
        with open(p, encoding="utf-8") as fh:
            return [l.strip().lower() for l in fh if l.strip() and not l.startswith("#")]
    except OSError:
        return []

def main():
    try:
        data = json.load(sys.stdin)
        tool = data.get("tool_name", "")
        ti = data.get("tool_input", {}) or {}
        flat = json.dumps(ti, ensure_ascii=False).lower()

        for h in prod_hosts():
            if h in flat:
                deny(f"Production host '{h}' is prohibited (security-rules 1). Use the approved test environment.")

        path = ti.get("file_path") or ti.get("path") or ti.get("notebook_path")
        if path and tool in ("Read", "Edit", "Write", "MultiEdit", "NotebookEdit", "Glob", "Grep"):
            base = os.path.basename(str(path))
            if SECRET_BASENAME.match(base) and not SAFE_BASENAME.match(base):
                deny(f"'{base}' looks like a secret file. Secrets are never read or written by the assistant (security-rules 4, 7).")

        if tool == "Bash":
            cmd = str(ti.get("command", ""))
            m = SECRET_IN_CMD.search(cmd)
            if m and READ_VERBS.search(cmd) and not SAFE_BASENAME.match(os.path.basename(m.group(2))):
                deny(f"Command touches a secret file ({m.group(2)}). Blocked by security-rules 4, 7.")
    except SystemExit:
        raise
    except Exception as e:
        sys.stderr.write(f"deny_prod_and_secrets: internal error, asking: {e}\n")
        ask(f"deny_prod_and_secrets: internal error ({type(e).__name__}); the check did not run. Confirm the action.")
    allow()

if __name__ == "__main__":
    main()
