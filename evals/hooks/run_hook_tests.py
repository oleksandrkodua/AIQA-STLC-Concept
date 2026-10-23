#!/usr/bin/env python3
"""Acceptance tests for the hook SCRIPTS' logic (not for Claude Code firing them).
Run from the repository root:  python3 evals/hooks/run_hook_tests.py
Each case: (name, script, stdin JSON, expected decision). Expected values were written
before the first run. Exit code 0 only if every case matches.
What this proves: the script decides as specified for these inputs.
What it does NOT prove: that Claude Code invokes the hook or that the
protocol fields are what the installed version expects.
"""
import json, os, subprocess, sys, tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
H = os.path.join(ROOT, ".claude", "hooks")

def run(script, payload):
    p = subprocess.run([sys.executable, os.path.join(H, script)], input=json.dumps(payload),
                       capture_output=True, text=True, timeout=10)
    out = p.stdout.strip()
    if p.returncode != 0:
        return f"exit{p.returncode}"
    if not out:
        return "allow"
    try:
        return json.loads(out)["hookSpecificOutput"]["permissionDecision"]
    except Exception:
        return "garbled"

SECRETS = "deny_prod_and_secrets.py"; TRUST = "protect_trusted_assets.py"
CASES = [
 ("read .env",             SECRETS, {"tool_name":"Read","tool_input":{"file_path":"/repo/.env"}}, "deny"),
 ("read .env.local",       SECRETS, {"tool_name":"Read","tool_input":{"file_path":"automation/web/.env.local"}}, "deny"),
 ("read .env.example",     SECRETS, {"tool_name":"Read","tool_input":{"file_path":"automation/web/.env.example"}}, "allow"),
 ("write key file",        SECRETS, {"tool_name":"Write","tool_input":{"file_path":"x/server.pem"}}, "deny"),
 ("read normal spec",      SECRETS, {"tool_name":"Read","tool_input":{"file_path":"automation/web/tests/cart.spec.ts"}}, "allow"),
 ("bash cat .env",         SECRETS, {"tool_name":"Bash","tool_input":{"command":"cat .env"}}, "deny"),
 ("bash grep in .env.dev", SECRETS, {"tool_name":"Bash","tool_input":{"command":"grep TOKEN automation/web/.env.dev"}}, "deny"),
 ("bash npm test",         SECRETS, {"tool_name":"Bash","tool_input":{"command":"npm test --prefix automation/web"}}, "allow"),
 ("bash cat .env.example", SECRETS, {"tool_name":"Bash","tool_input":{"command":"cat .env.example"}}, "allow"),
 ("edit CLAUDE.md",        TRUST,   {"tool_name":"Edit","tool_input":{"file_path":"/repo/CLAUDE.md"}}, "ask"),
 ("write rule",            TRUST,   {"tool_name":"Write","tool_input":{"file_path":"/repo/.claude/rules/qa-rules.md"}}, "ask"),
 ("edit policy",           TRUST,   {"tool_name":"Edit","tool_input":{"file_path":"policy/ai-usage-policy.md"}}, "ask"),
 ("edit a spec",           TRUST,   {"tool_name":"Edit","tool_input":{"file_path":"automation/web/tests/cart.spec.ts"}}, "allow"),
 ("bash sed -i on rule",   TRUST,   {"tool_name":"Bash","tool_input":{"command":"sed -i 's/a/b/' .claude/rules/qa-rules.md"}}, "ask"),
 ("bash ls .claude",       TRUST,   {"tool_name":"Bash","tool_input":{"command":"ls .claude/rules"}}, "allow"),
]

def main():
    bad = 0
    for name, script, payload, want in CASES:
        got = run(script, payload)
        ok = got == want
        bad += not ok
        print(f"{'PASS' if ok else 'FAIL'}  {name:26} expected={want:6} got={got}")
    # fail-open: garbage input must not block
    for script in (SECRETS, TRUST):
        p = subprocess.run([sys.executable, os.path.join(H, script)], input="not json",
                           capture_output=True, text=True, timeout=10)
        ok = p.returncode == 0 and p.stdout.strip() == ""
        bad += not ok
        print(f"{'PASS' if ok else 'FAIL'}  {script+' fail-open':26} expected=allow  got=exit{p.returncode}")
    # prod host list: temporary list must trigger deny
    hf = os.path.join(H, "prod-hosts.txt"); orig = open(hf).read()
    try:
        open(hf, "w").write("prod.example.invalid\n")
        got = run(SECRETS, {"tool_name":"Bash","tool_input":{"command":"curl https://prod.example.invalid/api"}})
        ok = got == "deny"; bad += not ok
        print(f"{'PASS' if ok else 'FAIL'}  {'prod host listed':26} expected=deny   got={got}")
    finally:
        open(hf, "w").write(orig)
    # qa_gate: PostToolUse nudge on QA-RUN.md only
    gate = os.path.join(H, "qa_gate.py")
    with tempfile.TemporaryDirectory() as td:
        badj = os.path.join(td, "QA-RUN.md"); open(badj, "w").write("# no plan\n## QA VERDICT\n")
        other = os.path.join(td, "notes.md"); open(other, "w").write("# no plan\n## QA VERDICT\n")
        for name, path, want in (("qa_gate bad journal", badj, 2), ("qa_gate other file", other, 0)):
            p = subprocess.run([sys.executable, gate], input=json.dumps({"tool_name":"Write","tool_input":{"file_path":path}}),
                               capture_output=True, text=True, timeout=20)
            ok = p.returncode == want; bad += not ok
            print(f"{'PASS' if ok else 'FAIL'}  {name:26} expected=exit{want} got=exit{p.returncode}")
    print(f"\n{len(CASES)+5-bad} passed, {bad} failed")
    sys.exit(1 if bad else 0)

if __name__ == "__main__":
    main()
