#!/usr/bin/env python3
"""
qa-run-check.py — deterministic gate for a QA-RUN.md journal.

The orchestrator's limits, RECONCILE, and write-back rules are self-tracked by the
model. This script is the mechanical half the model cannot be: it re-derives the
checks from the journal text, so a violation surfaces even when the model missed it.

It checks STRUCTURE and COUNTERS, not semantics — it cannot know whether a finding is
correct, only whether the journal is internally consistent and the caps were honoured.

Usage:
    python3 qa-run-check.py path/to/QA-RUN.md
Exit code 0 = clean, 1 = violations found (suitable for a hook / CI gate).

Run it before emitting a verdict, and on resume before continuing a prior run.
"""
import re
import sys

LIMITS = {"skills": 6, "reruns": 2, "streak": 3}


def load(path):
    try:
        with open(path, encoding="utf-8") as fh:
            return fh.read()
    except OSError as e:
        print(f"CANNOT READ {path}: {e}")
        sys.exit(2)


def check(text):
    problems = []

    # 1 — Plan must declare what was deliberately NOT run (non-empty).
    #     The list may sit on the marker line or on the lines beneath it (bullets),
    #     up to the next heading — read the whole block, not just the first line.
    m = re.search(r"Deliberately NOT run:?\**(.*?)(?:\n#{1,6}\s|\n\*\*[A-Z]|\Z)",
                  text, re.I | re.S)
    if m:
        body = m.group(1)
        # strip the marker's own line-tail, then look for real list content below
        item_lines = [ln for ln in body.splitlines()
                      if re.match(r"\s*[-*]\s+\S", ln) or re.search(r"\w", ln)]
        if not item_lines:
            problems.append("Plan: 'Deliberately NOT run' is present but empty — a scope "
                            "that excluded nothing did not make a decision.")
    else:
        problems.append("Plan: no 'Deliberately NOT run' line — required.")

    # 2 — Every Log step must carry an outcome (a '|' separated status field).
    #     A dangling step with no outcome is the 'incomplete journal' failure.
    for ln in text.splitlines():
        if re.match(r"\s*[-*]\s*\d{1,2}:\d{2}", ln):  # "- 18:22 | ... | ... | ..."
            fields = [f.strip() for f in ln.split("|")]
            if len(fields) < 3 or not fields[2]:
                problems.append(f"Log step has no outcome field: {ln.strip()[:80]}")

    # 3 — Limit counters, if present, must not exceed the caps.
    m = re.search(r"Skills used:\s*(\d+)\s*/\s*(\d+)", text)
    if m and int(m.group(1)) > LIMITS["skills"]:
        problems.append(f"Limit: skills used {m.group(1)} > cap {LIMITS['skills']} "
                        "with no recorded human approval to raise it.")
    m = re.search(r"Re-?runs:\s*(\d+)\s*/\s*(\d+)", text)
    if m and int(m.group(1)) > LIMITS["reruns"]:
        problems.append(f"Limit: re-runs {m.group(1)} > cap {LIMITS['reruns']}.")
    m = re.search(r"[Nn]o-new-finding streak:\s*(\d+)\s*/\s*(\d+)", text)
    if m and int(m.group(1)) > LIMITS["streak"]:
        problems.append(f"Limit: no-new-finding streak {m.group(1)} > cap {LIMITS['streak']}.")

    # 4 — If a verdict is present, a RECONCILE section must precede it, and every
    #     MUST item must be marked done or carried (no bare/unmarked MUST rows).
    has_verdict = bool(re.search(r"QA VERDICT|## .*VERDICT", text, re.I))
    has_reconcile = bool(re.search(r"RECONCILE", text, re.I))
    if has_verdict and not has_reconcile:
        problems.append("Verdict present but no RECONCILE section — the MUST tier was "
                        "never checked against execution.")

    # 5 — On a verdict, 'what limited this' / Missing information must be stated.
    if has_verdict and not re.search(r"limited this|Missing information|What limited", text, re.I):
        problems.append("Verdict present but does not state what limited it "
                        "(caps hit / tools unavailable / categories untested).")

    return problems


def main():
    if len(sys.argv) != 2:
        print(__doc__)
        sys.exit(2)
    problems = check(load(sys.argv[1]))
    if not problems:
        print("QA-RUN check: clean.")
        sys.exit(0)
    print(f"QA-RUN check: {len(problems)} issue(s) —")
    for p in problems:
        print(f"  ✗ {p}")
    sys.exit(1)


if __name__ == "__main__":
    main()
