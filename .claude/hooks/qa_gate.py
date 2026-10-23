#!/usr/bin/env python3
"""PostToolUse hook (DRAFT, EXPERIMENTAL): after a Write/Edit of a file named *QA-RUN.md,
run qa_run_check.py. Problems -> exit 2 with the list on stderr (a nudge back to the model).
Other files, or a clean journal -> exit 0. Fail-open on internal errors.
Modelled on an earlier QA agent's gate hook (that script was not available to copy, so this is
a new implementation of the described behavior, not a copy).
"""
import json, os, subprocess, sys

def main():
    try:
        d = json.load(sys.stdin)
        ti = d.get("tool_input", {}) or {}
        path = str(ti.get("file_path", ""))
        if not path.endswith("QA-RUN.md") or not os.path.exists(path):
            sys.exit(0)
        chk = os.path.join(os.path.dirname(os.path.abspath(__file__)), "qa_run_check.py")
        p = subprocess.run([sys.executable, chk, path], capture_output=True, text=True, timeout=20)
        if p.returncode == 1:
            sys.stderr.write(p.stdout)
            sys.exit(2)
    except SystemExit:
        raise
    except Exception as e:
        sys.stderr.write(f"qa_gate: internal error, failing open: {e}\n")
    sys.exit(0)

if __name__ == "__main__":
    main()
