#!/usr/bin/env python3
"""Known-good / known-bad journals for .claude/hooks/qa_run_check.py.
Run from the repository root:  python3 evals/hooks/run_runcheck_tests.py
Expected exit codes were written before the first run.
"""
import os, subprocess, sys, tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
CHK = os.path.join(ROOT, ".claude", "hooks", "qa_run_check.py")

GOOD = """# QA RUN: demo
## Plan
**MUST:** login
**Deliberately NOT run:** payment flow (risk accepted: payment untested)
## Log
- 10:00 | opened app | ok
## RECONCILE
| login | DONE |
## QA VERDICT
Status: NOT READY
What limited this verdict: emulator only
Skills used: 2/6 · Re-runs: 0/2 · No-new-finding streak: 1/3
"""
CASES = [
 ("good journal", GOOD, 0),
 ("no NOT-run line", GOOD.replace("**Deliberately NOT run:** payment flow (risk accepted: payment untested)", "**SHOULD:** x"), 1),
 ("empty NOT-run", GOOD.replace("payment flow (risk accepted: payment untested)", ""), 1),
 ("log step without outcome", GOOD.replace("- 10:00 | opened app | ok", "- 10:00 | opened app"), 1),
 ("verdict without RECONCILE", GOOD.replace("## RECONCILE\n| login | DONE |\n", ""), 1),
 ("verdict without limits stated", GOOD.replace("What limited this verdict: emulator only\n", ""), 1),
 ("skills over cap", GOOD.replace("Skills used: 2/6", "Skills used: 7/6"), 1),
 ("re-runs over cap", GOOD.replace("Re-runs: 0/2", "Re-runs: 3/2"), 1),
]

bad = 0
for name, text, want in CASES:
    with tempfile.NamedTemporaryFile("w", suffix="QA-RUN.md", delete=False, encoding="utf-8") as f:
        f.write(text); path = f.name
    got = subprocess.run([sys.executable, CHK, path], capture_output=True, text=True).returncode
    os.unlink(path)
    ok = got == want; bad += not ok
    print(f"{'PASS' if ok else 'FAIL'}  {name:32} expected exit {want}, got {got}")
got = subprocess.run([sys.executable, CHK, "/nonexistent/QA-RUN.md"], capture_output=True, text=True).returncode
ok = got == 2; bad += not ok
print(f"{'PASS' if ok else 'FAIL'}  {'unreadable file':32} expected exit 2, got {got}")
print(f"\n{len(CASES)+1-bad} passed, {bad} failed")
sys.exit(1 if bad else 0)
