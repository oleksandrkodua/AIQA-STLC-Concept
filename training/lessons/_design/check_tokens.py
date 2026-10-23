#!/usr/bin/env python3
"""Check that course files use the design tokens in tokens.json.

    python3 training/lessons/_design/check_tokens.py        exit 0 = clean, 1 = drift

Checks:
1. Every lesson deck (training/lessons/*/lesson-*.html) defines every token of tokens.json in its first :root, with the same value.
2. The diagrams mockup defines its light :root tokens with the same values (`--bg` is its name for `--paper`); its dark theme is
   not part of the palette and is not checked.
3. Decks, the mockup and the animation gallery use no colour outside the palette (outside :root blocks).
4. The cheatsheet builder reads tokens.json instead of its own colour literals.
5. tokens.css holds the same tokens as tokens.json.
Standard library only. Reads files; writes nothing.
"""
import json, os, re, sys, glob

HERE = os.path.dirname(os.path.abspath(__file__))
LESSONS = os.path.dirname(HERE)
T = json.load(open(os.path.join(HERE, "tokens.json"), encoding="utf-8"))
EXPECTED = {f"--{k}": v for k, v in T["color"].items()}
EXPECTED.update({f"--{k}": v for k, v in T["font"].items()})
EXPECTED.update({f"--fs-{k}": v for k, v in T["font-size"].items()})
EXPECTED.update({f"--r-{k}": v for k, v in T["radius"].items()})
PALETTE = {v.upper() for v in T["color"].values()}
problems = []


def norm(v):
    return re.sub(r"\s+", "", v).replace('"', "'").upper()


def first_root(text):
    m = re.search(r"(?<![\w-]):root\s*\{([^}]*)\}", text)
    return dict((k.strip(), v.strip()) for k, v in re.findall(r"(--[\w-]+)\s*:\s*([^;]+)", m.group(1))) if m else {}


def outside_roots(text):
    text = re.sub(r"url\(data:[^)]*\)", "", text)
    text = re.sub(r"@media[^{]*\{\s*:root[^{]*\{[^}]*\}\s*\}", "", text)
    return re.sub(r":root[^{]*\{[^}]*\}", "", text)


def rel(p):
    return os.path.relpath(p, LESSONS)


for f in sorted(glob.glob(os.path.join(LESSONS, "*", "lesson-*.html"))):
    root = first_root(open(f, encoding="utf-8").read())
    for name, value in EXPECTED.items():
        if name not in root:
            problems.append(f"{rel(f)}: {name} missing from :root")
        elif norm(root[name]) != norm(value):
            problems.append(f"{rel(f)}: {name} is {root[name]}, tokens say {value}")

for f in sorted(glob.glob(os.path.join(LESSONS, "_mockups", "*.html"))):
    root = first_root(open(f, encoding="utf-8").read())
    for name, value in root.items():
        key = "--paper" if name == "--bg" else name
        if key in EXPECTED and norm(value) != norm(EXPECTED[key]):
            problems.append(f"{rel(f)}: {name} is {value}, tokens say {EXPECTED[key]}")

files = sorted(glob.glob(os.path.join(LESSONS, "*", "lesson-*.html")) + glob.glob(os.path.join(LESSONS, "_mockups", "*.html"))
               + glob.glob(os.path.join(LESSONS, "_template", "animations", "*.html")))
for f in files:
    off = sorted({h.upper() for h in re.findall(r"#[0-9A-Fa-f]{6}\b", outside_roots(open(f, encoding="utf-8").read()))} - PALETTE)
    if off:
        problems.append(f"{rel(f)}: colours outside the palette: {', '.join(off)}")

css = first_root(open(os.path.join(HERE, "tokens.css"), encoding="utf-8").read())
if {k: norm(v) for k, v in css.items()} != {k: norm(v) for k, v in EXPECTED.items()}:
    problems.append("_design/tokens.css does not match tokens.json (edit both, or regenerate tokens.css from the JSON)")

builder = open(os.path.join(LESSONS, "cheatsheets", "build_cheatsheets.py"), encoding="utf-8").read()
if "tokens.json" not in builder or re.search(r'^PAPER[^\n]*"#', builder, re.M):
    problems.append("cheatsheets/build_cheatsheets.py: palette is not read from _design/tokens.json")

for p in problems:
    print("DRIFT", p)
print(f"checked {len(files)} files: {'clean' if not problems else str(len(problems)) + ' problem(s)'}")
sys.exit(1 if problems else 0)
