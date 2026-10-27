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
6. Colour forms: #RGB, #RGBA, #RRGGBBAA, rgb()/rgba()/hsl()/hsla()/hwb() and named colours in colour properties count as
   colours outside the palette too (only #RRGGBB palette values are allowed; `transparent`, `inherit`, `currentColor`, `none` are fine).
7. Contrast: where one inline style or rule sets both a background and a text colour from the palette, the pair must reach 3:1 (the
   large-text floor; the 4.5:1 rule for small text stays with the author, as sizes are not parsed). The gallery :root and the
   extra variables of the decks are checked against the palette as well.
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


NAMED = {"white", "black", "red", "green", "blue", "yellow", "orange", "purple", "pink", "gray", "grey", "brown", "gold", "silver",
         "navy", "teal", "maroon", "olive", "lime", "aqua", "cyan", "magenta", "coral", "tomato", "crimson", "beige", "ivory"}
COLOUR_PROP = r"(?:background(?:-color)?|color|fill|stroke|border(?:-[a-z]+)?(?:-color)?|outline(?:-color)?)"


def lum(hexv):
    c = [int(hexv[i:i + 2], 16) / 255 for i in (1, 3, 5)]
    c = [x / 12.92 if x <= 0.03928 else ((x + 0.055) / 1.055) ** 2.4 for x in c]
    return 0.2126 * c[0] + 0.7152 * c[1] + 0.0722 * c[2]


def ratio(a, b):
    la, lb = sorted((lum(a), lum(b)), reverse=True)
    return (la + 0.05) / (lb + 0.05)


def colour_problems(text):
    """Colours outside the palette in every written form, plus low-contrast background/text pairs in one declaration block."""
    out = set()
    for h in re.findall(r"(?<![&\w])#[0-9A-Fa-f]{3,8}\b", text):
        if len(h) != 7 or h.upper() not in PALETTE: out.add(h.upper())
    out |= {m.lower() for m in re.findall(r"\b(?:rgba?|hsla?|hwb)\([^)]*\)", text, re.I)}
    for m in re.finditer(COLOUR_PROP + r"\s*:\s*([a-zA-Z]+)\s*[;}\"']", text):
        if m.group(1).lower() in NAMED: out.add(m.group(1).lower())
    pairs = set()
    for blk in re.findall(r"\{([^}]*)\}|style=\"([^\"]*)\"", text):
        b = blk[0] or blk[1]
        bg = re.search(r"background(?:-color)?\s*:\s*(#[0-9A-Fa-f]{6})\b", b)
        fg = re.search(r"(?<![\w-])color\s*:\s*(#[0-9A-Fa-f]{6})\b", b)
        if bg and fg and ratio(bg.group(1), fg.group(1)) < 3:
            pairs.add(f"{fg.group(1).upper()} on {bg.group(1).upper()} = {ratio(bg.group(1), fg.group(1)):.1f}:1")
    return sorted(out), sorted(pairs)


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
    body = open(f, encoding="utf-8").read()
    off, low = colour_problems(outside_roots(body))
    if off:
        problems.append(f"{rel(f)}: colours outside the palette: {', '.join(off)}")
    if low:
        problems.append(f"{rel(f)}: low contrast (below 3:1): {'; '.join(low)}")
    for rb in re.findall(r"(?<![\w-]):root\s*\{([^}]*)\}", body):  # every :root block, not only the first
        for name, v in re.findall(r"(--[\w-]+)\s*:\s*([^;]+)", rb):
            if name in EXPECTED or name == "--bg" or not re.search(r"#|rgb|hsl|hwb", v): continue
            offv, _ = colour_problems("color:" + v.strip() + ";")
            if offv: problems.append(f"{rel(f)}: {name} in :root holds a colour outside the palette: {', '.join(offv)}")

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
