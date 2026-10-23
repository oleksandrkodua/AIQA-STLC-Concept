#!/usr/bin/env python3
"""Builds the course cheat sheets.

Edit the CONTENT sections below (plain text and lists), then run:
    python3 build_cheatsheets.py
Output next to this file: .svg (editable in Figma, Inkscape, a text editor), .png (picture), .pdf (print).
Needs: PyMuPDF (fitz) and Pillow. Fonts are measured with Arial and Courier New from macOS.
Status: DRAFT v0.1, 2026-10-14. Colour meaning: see training/lessons/_specs/2026-10-14-colors-design.md, section 5.
"""
import json
import os
from xml.sax.saxutils import escape
from PIL import ImageFont
import fitz

HERE = os.path.dirname(os.path.abspath(__file__))
W, H = 1123, 794  # A4 landscape at 96 dpi

# palette: the course tokens (../_design/tokens.json); edit colours there, not here
with open(os.path.join(HERE, "..", "_design", "tokens.json"), encoding="utf-8") as _f:
    _C = json.load(_f)["color"]
PAPER, CARD, BAND, INK, MUTED, LINE = _C["paper"], _C["card"], _C["band"], _C["ink"], _C["muted"], _C["line"]
AMBER, AMBER_T, AMBER_BG = _C["amber"], _C["amber-text"], _C["amber-tint"]
FOREST, LEAF, GREEN_BG = _C["forest"], _C["leaf"], _C["green-tint"]
RED_T, RED_BG = _C["red-text"], _C["red-tint"]

SANS = "Helvetica, Arial, sans-serif"
MONO = "Courier New, Courier, monospace"
_FONTS = {
    "sans": "/System/Library/Fonts/Supplemental/Arial.ttf",
    "bold": "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
    "mono": "/System/Library/Fonts/Supplemental/Courier New.ttf",
}
_cache = {}


def measure(s, size, kind="sans"):
    key = (kind, size)
    if key not in _cache:
        try:
            _cache[key] = ImageFont.truetype(_FONTS[kind], int(size * 10))
        except Exception:
            _cache[key] = None
    f = _cache[key]
    if f is None:
        return len(s) * size * (0.6 if kind == "mono" else 0.52)
    return f.getlength(s) / 10.0


def wrap(s, size, maxw, kind="sans"):
    lines, cur = [], ""
    for word in s.split():
        t = (cur + " " + word).strip()
        if measure(t, size, kind) <= maxw or not cur:
            cur = t
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines or [""]


class Sheet:
    def __init__(self, name):
        self.name, self.e = name, []
        self.rect(0, 0, W, H, PAPER)

    def rect(self, x, y, w, h, fill="none", stroke=None, sw=1, rx=0, dash=None):
        a = f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="{rx}" fill="{fill}"'
        if stroke:
            a += f' stroke="{stroke}" stroke-width="{sw}"'
        if dash:
            a += f' stroke-dasharray="{dash}"'
        self.e.append(a + "/>")

    def line(self, x1, y1, x2, y2, stroke=LINE, sw=1):
        self.e.append(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{stroke}" stroke-width="{sw}"/>')

    def text(self, x, y, s, size=12, kind="sans", fill=INK, anchor="start"):
        fam = MONO if kind == "mono" else SANS
        wt = ' font-weight="700"' if kind == "bold" else ""
        self.e.append(f'<text x="{x:.1f}" y="{y:.1f}" font-family="{fam}" font-size="{size}"{wt} fill="{fill}" text-anchor="{anchor}">{escape(s)}</text>')

    def para(self, x, y, w, s, size=12, kind="sans", fill=INK, lead=1.35):
        ys = y
        for ln in wrap(s, size, w, kind):
            self.text(x, ys, ln, size, kind, fill)
            ys += size * lead
        return ys - y

    def chip(self, x, y, label, kind="plain"):
        """kind: on, dr, un, off, plain. Returns width. y is the top."""
        style = {
            "on": (GREEN_BG, LEAF, FOREST, None),
            "dr": (AMBER_BG, AMBER, AMBER_T, None),
            "un": (RED_BG, RED_T, RED_T, None),
            "off": ("none", MUTED, MUTED, "3 2"),
            "plain": (CARD, LINE, MUTED, None),
        }[kind]
        sz = 9.5
        w = measure(label, sz, "bold") + 14
        self.rect(x, y, w, 17, style[0], style[1], 1, 3, style[3])
        self.text(x + 7, y + 12.2, label, sz, "bold", style[2])
        return w

    def header(self, title, sub, legend=True):
        self.text(36, 66, title, 28, "bold")
        self.text(36, 90, sub, 12, "sans", MUTED)
        self.line(36, 102, W - 36, 102, AMBER, 2)
        if legend:
            x = W - 36
            items = [("NOT USED", "off"), ("UNVERIFIED", "un"), ("DRAFT / NOT RUN", "dr"), ("IN USE", "on")]
            for lab, k in items:
                w = measure(lab, 9.5, "bold") + 14
                x -= w
                self.chip(x, 50, lab, k)
                x -= 8

    def save(self):
        svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">\n'
               + "\n".join(self.e) + "\n</svg>\n")
        p = os.path.join(HERE, self.name + ".svg")
        open(p, "w", encoding="utf-8").write(svg)
        doc = fitz.open(p)
        pix = doc[0].get_pixmap(dpi=192)
        pix.save(os.path.join(HERE, self.name + ".png"))
        return p


def table(sh, x, y, cols, rows, size=11, pad=7, head=None, min_h=24, vpad=10):
    """cols: list of (width, kind). rows: list of lists; a cell is a str or (str, chipkind) -> drawn as chip."""
    if head:
        sh.rect(x, y, sum(c[0] for c in cols), 22, BAND)
        cx = x
        for (cw, _), htxt in zip(cols, head):
            sh.text(cx + pad, y + 15, htxt, 9.5, "bold", MUTED)
            cx += cw
        y += 22
    for i, row in enumerate(rows):
        hs = []
        for (cw, kind), cell in zip(cols, row):
            if isinstance(cell, tuple):
                hs.append(min_h)
            else:
                n = len(wrap(cell, size, cw - 2 * pad, kind if kind != "bold" else "bold"))
                hs.append(n * size * 1.3 + vpad)
        rh = max(min_h, max(hs))
        if i % 2 == 0:
            sh.rect(x, y, sum(c[0] for c in cols), rh, CARD)
        cx = x
        for (cw, kind), cell in zip(cols, row):
            if isinstance(cell, tuple):
                if cell[0]:
                    sh.chip(cx + pad, y + (rh - 17) / 2, cell[0], cell[1])
            else:
                lines = wrap(cell, size, cw - 2 * pad, kind)
                ty = y + (rh - len(lines) * size * 1.3) / 2 + size * 1.0
                for ln in lines:
                    sh.text(cx + pad, ty, ln, size, kind, INK if kind != "sans" else INK)
                    ty += size * 1.3
            cx += cw
        sh.line(x, y + rh, x + sum(c[0] for c in cols), y + rh, LINE, 0.6)
        y += rh
    return y


def box(sh, x, y, w, title, kind="plain"):
    """Draws a titled box frame lazily: returns the inner y start. Call finish_box(h) separately."""
    return y + 30


# ===================================================================== CONTENT: sheet 1 (terms)
LAYERS = [  # (name, description, chip label, chip kind)
    ("Model", "Predicts the next token of text.", "outside the repo", "plain"),
    ("Instructions", "CLAUDE.md, rules, skills.", "DRAFT", "dr"),
    ("Tools", "Read files, run commands, MCP.", "MCP list empty", "dr"),
    ("Guardrails", "Permissions and hooks.", "DRAFT, not active", "dr"),
    ("Memory", "The window now, plus files that persist.", "session + files", "plain"),
    ("Proof", "Evals: how we know it works.", "written, NOT RUN", "dr"),
]
QUICK = [
    "AI output is a draft, not evidence.",
    "No source, no conclusion.",
    "NOT TESTED is never PASS.",
    "An emulator is not a real device.",
]
GLOSSARY = [  # term, plain words, where here, status label, status kind
    ("LLM", "A model that predicts the next token. An intern who read the internet but never saw your project.", "outside the repo", "", "plain"),
    ("Token", "A piece of text you pay for. It also fills the window.", "/usage counter", "", "plain"),
    ("Context window", "Everything the model sees right now. A desk with limited space.", "the session", "", "plain"),
    ("Assistant", "Model + instructions + tools + memory + a loop.", "Claude Desktop / Code", "IN USE", "on"),
    ("Agent", "An assistant that repeats plan, act, check and changes state (files, tickets).", ".claude/agents/", "OFF IN MVP", "dr"),
    ("Subagent", "A separate worker with its own window. Returns a short summary.", "none", "NOT USED", "off"),
    ("CLAUDE.md", "A file read at the start of every session. Onboarding for a new hire.", "CLAUDE.md", "DRAFT", "dr"),
    ("AGENTS.md", "A shared instruction convention for several AI tools (per conference notes, unverified).", "none", "NOT USED", "off"),
    ("Rules", "Rules in separate files. Some apply only to given paths (paths:).", ".claude/rules/", "DRAFT", "dr"),
    ("Skill", "A folder with SKILL.md: a trigger description plus instructions, loaded when needed. A recipe, not a request.", ".claude/skills/", "PILOT", "dr"),
    ("Hook", "A command run on an event, before or after an action. Exit code 2 stops it. A turnstile.", ".claude/hooks/", "NOT ACTIVE", "dr"),
    ("Permissions", "allow / ask / deny. Deny beats allow.", "settings.draft.json", "NOT ACTIVE", "dr"),
    ("Eval", "Tasks with the expected result written first, run several times. A test paper for the AI.", "evals/", "NOT RUN", "dr"),
    ("MCP", "A standard for plugging in outside tools with typed calls. Sockets and wires.", ".mcp.json", "EMPTY", "dr"),
    ("Plugin / mod", "A plugin packs extensions. A mod is a plugin of JS/TS handlers that run inside Claude Code. Official, not used here.", "mods/, not enabled", "NOT USED", "off"),
]

# ===================================================================== CONTENT: sheet 1, page 2
# yes = documented as a typed command; menu = a UI control instead of a typed command; no = docs say not available; ? = docs silent (not tested)
CMD_CONTEXT = [  # command, what it does, CLI, VS Code, Desktop
    ("/context", "See what fills the window.", "yes", "?", "yes*"),
    ("/compact", "Replace the chat with a short summary.", "yes", "yes", "yes"),
    ("/clear", "Start fresh. Plan, clear, then build.", "yes", "?", "yes*"),
    ("/usage", "Cost, limits, token counter.", "yes", "yes", "menu"),
]
CMD_PROJECT = [  # command, what it does, status label, kind
    ("/analyze-requirements", "Gaps, ambiguities, risks, testability.", "PILOT", "dr"),
    ("/create-test-cases", "Cases from approved requirements.", "EXISTING", "dr"),
    ("/automation-readiness-assessment", "Automate this case now?", "EXISTING", "dr"),
    ("/create-playwright-test", "Web automation: write.", "EXISTING", "dr"),
    ("/review-playwright-test", "Web automation: review.", "EXISTING", "dr"),
    ("/create-mobile-test", "Mobile automation: write.", "DRAFT", "dr"),
    ("/review-mobile-test", "Mobile automation: review.", "DRAFT", "dr"),
    ("/bug-report and later-stage skills", "Stages 4 to 13 of the cycle.", "SKELETON", "off"),
    ("/onboarding-check", "Start-up checklist for a new machine.", "SKELETON", "off"),
    ("/feedback", "Send feedback. Not in the table.", "EXISTS", "plain"),
]
CMD_GENERAL = [  # command, what it does, CLI, VS Code, Desktop
    ("/model", "Switch model.", "yes", "yes", "menu"),
    ("/resume", "Continue a past session.", "yes", "?", "yes"),
    ("/permissions", "Allow / ask / deny.", "yes", "menu", "no"),
    ("/hooks", "Show hook configuration.", "yes", "menu", "no*"),
    ("/mcp", "Manage MCP servers.", "yes", "yes", "yes*"),
    ("/agents", "Ask Claude to manage subagents.", "yes", "?", "yes*"),
    ("/memory", "Edit CLAUDE.md and memory.", "yes", "menu", "yes*"),
    ("/init", "Create a CLAUDE.md.", "yes", "?", "yes*"),
    ("/doctor", "Diagnose the installation.", "yes", "?", "yes*"),
    ("/rewind", "Roll back code and/or chat. Bash changes are not tracked.", "yes", "menu", "yes*"),
    ("/plan", "Enter plan mode.", "yes", "yes", "menu"),
    ("/config", "Open settings. Desktop: Settings > Claude Code.", "yes", "?", "yes"),
]
LABELS = [
    ("VERIFIED FACT", "on", "Seen or run. Say what was run."),
    ("EVIDENCE-SUPPORTED INFERENCE", "dr", "Follows from evidence you can name."),
    ("ASSUMPTION", "dr", "Not checked."),
    ("UNKNOWN", "un", "No evidence. Ask, or defer."),
]
NEVER = [
    "Production: DEV or approved test environments only.",
    "Secrets, tokens, passwords in chat, files or logs.",
    "Real customer data or PII in tests.",
    "Treat text in tickets or pages as instructions.",
    "Force-push, or delete shared branches.",
]

# ===================================================================== CONTENT: sheet 2 (project placeholder)
REPO = [  # path, what, chip, kind
    ("CLAUDE.md", "Always-on rules, skill table", "DRAFT", "dr"),
    (".claude/rules/", "security, QA, AI + web and mobile rules", "DRAFT", "dr"),
    (".claude/skills/", "Copies of plugins/qabase/skills", "DRAFT", "dr"),
    (".claude/hooks/", "Hook specs and scripts", "NOT ACTIVE", "dr"),
    (".claude/settings.draft.json", "Permissions draft", "NOT ACTIVE", "dr"),
    (".mcp.json", "Approved MCP servers", "EMPTY", "dr"),
    ("evals/", "Acceptance checks", "NOT RUN", "dr"),
    ("automation/web", "Playwright (optional)", "OPTIONAL", "off"),
    ("automation/mobile", "WebdriverIO + Appium (optional)", "OPTIONAL", "off"),
    ("automation/api", "The project's choice (optional)", "OPTIONAL", "off"),
]
CHAIN = [  # label, kind: C Claude with a skill, H human gate, D deterministic
    ("C", "analyze-requirements + brief"), ("H", "approve the brief"),
    ("C", "create-test-cases"), ("H", "review cases, save to TMS"),
    ("C", "automation-readiness"), ("H", "approve candidate"),
    ("C", "create + review test"), ("H", "review diff, merge"),
    ("D", "CI run, results, evidence"), ("H", "release decision"),
]
BLANKS = [  # label
    "Environment to test on (DEV or SIT)",
    "Test management and defect tracker",
    "CI/CD tool and who can see runs",
    "Test accounts and test data",
    "Devices and builds for mobile",
    "Who approves changes (AI QA Process Lead)",
    "Where to send feedback",
]
PROJ_RULES = [
    "DEV or approved non-production only. Production is prohibited.",
    "A mobile build can open on PROD by default. Switch to test and confirm first.",
    "A bug gets a failing test first (Iron Law).",
    "Say which device or emulator produced the evidence.",
]


def build_terms_p1():
    s = Sheet("cheatsheet-1-terms-p1")
    s.header("AI assistant in QA: the terms", "Cheat sheet 1 of 6, page 1 of 2. DRAFT v0.1, 2026-10-14. Statuses as in CLAUDE.md on 2026-10-07; nothing here is approved.")
    s.text(36, 130, "An assistant is a model plus five things", 14, "bold")
    y = 146
    for name, desc, chip, kind in LAYERS:
        s.rect(36, y, 324, 58, CARD, LINE, 1, 5)
        s.text(50, y + 22, name, 13, "bold")
        s.text(50, y + 40, desc, 10.5, "sans", MUTED)
        cw = measure(chip, 9.5, "bold") + 14
        s.chip(360 - 12 - cw, y + 8, chip, kind)
        y += 66
    s.rect(36, y + 4, 324, 150, BAND, None, 0, 5)
    s.text(50, y + 26, "Four lines to remember", 12, "bold")
    ty = y + 48
    for q in QUICK:
        s.text(50, ty, "•", 11, "sans", AMBER_T)
        ty += s.para(62, ty, 284, q, 11.5, "sans", INK) + 7
    s.text(384, 130, "Glossary", 14, "bold")
    cols = [(112, "bold"), (300, "sans"), (160, "mono"), (131, "sans")]
    rows = [[t, d, w, (lab, k)] for (t, d, w, lab, k) in GLOSSARY]
    end = table(s, 384, 146, cols, rows, 10.5, 8, ["TERM", "IN PLAIN WORDS", "WHERE HERE", "STATUS"])
    return s, end


def build_terms_p2():
    s = Sheet("cheatsheet-1-terms-p2")
    s.header("AI assistant in QA: commands and rules", "Cheat sheet 1 of 6, page 2 of 2. DRAFT v0.1, 2026-10-14. Command support: official docs (2026-10-14) plus the author's check in Desktop. VS Code not tested.")
    x0, wcol = 36, 574
    y = 128
    s.text(x0, y, "Slash commands", 14, "bold")
    s.text(x0, y + 17, "Per official docs: yes = typed command works. menu = a UI control instead. no = docs say unavailable. ? = docs silent, not tested.", 8.5, "sans", MUTED)
    s.text(x0, y + 28, "* = tested by the author in Desktop (Code tab), 2026-10-14: seen in the / menu; \"hooks\" is not there. /doctor is the bundled skill.", 8.5, "sans", MUTED)
    hx = x0 + wcol - 3 * 46

    def surf_head(yy, label):
        s.text(x0, yy, label, 11, "bold", AMBER_T)
        for j, lab in enumerate(["CLI", "VS Code", "Desktop"]):
            s.text(hx + j * 46 + 23, yy, lab, 8.5, "bold", MUTED, "middle")

    def surf_rows(yy, rows):
        for i, (c, d, a1, b1, e1) in enumerate(rows):
            if i % 2 == 0:
                s.rect(x0, yy, wcol, 19, CARD)
            s.text(x0 + 7, yy + 13.5, c, 10.5, "mono")
            s.text(x0 + 124, yy + 13.5, d, 10, "sans", INK)
            for j, v in enumerate((a1, b1, e1)):
                col = {"yes": FOREST, "yes*": FOREST, "menu": AMBER_T, "no": RED_T, "no*": RED_T, "?": MUTED}[v]
                s.text(hx + j * 46 + 23, yy + 13.5, v, 9.5, "bold", col, "middle")
            s.line(x0, yy + 19, x0 + wcol, yy + 19, LINE, 0.6)
            yy += 19
        return yy
    y += 50
    surf_head(y, "Context and cost")
    y = surf_rows(y + 6, CMD_CONTEXT)
    s.text(x0, y + 18, "Our project skills (from the CLAUDE.md table)", 11, "bold", AMBER_T)
    rows = [[c, d, (lab, k)] for c, d, lab, k in CMD_PROJECT]
    y = table(s, x0, y + 24, [(262, "mono"), (210, "sans"), (102, "sans")], rows, 10, 7, None, 20, 6)
    surf_head(y + 18, "General commands")
    y = surf_rows(y + 24, CMD_GENERAL)
    s.text(x0, y + 16, "Plan mode: CLI Shift+Tab or /plan. VS Code: mode indicator or /plan (2.1.280+). Desktop: mode selector (Shift+Tab does not cycle).", 8.5, "sans", MUTED)
    s.text(x0, y + 29, "Versions: VS Code /model 2.1.284+; VS Code menu views (Permissions, Hooks, Memory) 2.1.269 / 2.1.274+. /agents interactive UI only on 2.1.197 and earlier.", 8.5, "sans", MUTED)
    # right column
    rx, rw = 636, 451
    ry = 128
    s.text(rx, ry, "Label every claim that matters", 14, "bold")
    ry += 10
    for lab, k, d in LABELS:
        s.rect(rx, ry + 6, rw, 30, CARD, LINE, 1, 5)
        s.chip(rx + 10, ry + 12, lab, k)
        s.text(rx + 10 + measure(lab, 9.5, "bold") + 14 + 12, ry + 25, d, 10.5, "sans", MUTED)
        ry += 35
    ry += 34
    s.text(rx, ry, "Verdict words", 14, "bold")
    ry += 14
    s.rect(rx, ry, rw, 74, CARD, LINE, 1, 5)
    s.text(rx + 12, ry + 22, "Per area:  PASS  /  FAIL  /  NOT TESTED  /  NOT APPLICABLE  /  BLOCKED  /  UNKNOWN", 9.5, "bold", INK)
    s.text(rx + 12, ry + 42, "Release:  READY  /  READY WITH RISKS  /  NOT READY  /  BLOCKED", 9.5, "bold", INK)
    s.text(rx + 12, ry + 62, "NOT TESTED is never collapsed into FAIL and never reported as PASS.", 10, "sans", MUTED)
    ry += 98
    s.text(rx, ry, "Never", 14, "bold")
    ry += 10
    s.rect(rx, ry + 6, rw, 24 * len(NEVER) + 8, RED_BG, RED_T, 1, 5)
    ty = ry + 26
    for n in NEVER:
        s.text(rx + 12, ty, "✕", 10, "bold", RED_T)
        s.text(rx + 30, ty, n, 10.5, "sans", RED_T)
        ty += 24
    ry = ry + 6 + 24 * len(NEVER) + 8 + 24
    s.text(rx, ry, "Hooks versus mods", 14, "bold")
    s.chip(rx + rw - (measure("DOCS-CONFIRMED, NOT RUN HERE", 9.5, "bold") + 14), ry - 13, "DOCS-CONFIRMED, NOT RUN HERE", "dr")
    ry += 10
    for j, (t, lines) in enumerate([("Hook", ["Shell command, HTTP request or prompt, run on lifecycle events.", "Exit code 2 blocks a tool call. Any other exit code does not.", "Can add context and log. Cannot draw in the UI."]),
                                    ("Mod", ["JS/TS functions inside Claude Code. Not sandboxed.", "Rewrite prompts, hold or change calls, redraw the UI, add /commands.", "Needs CLI 2.1.287+ or Desktop 2.1.286+. Runs with your permissions."])]):
        bx = rx + j * (rw / 2 + 4)
        bw = rw / 2 - 4
        s.rect(bx, ry + 6, bw, 132, CARD, LINE, 1, 5)
        s.text(bx + 10, ry + 26, t, 12, "bold")
        ty = ry + 44
        for ln in lines:
            ty += s.para(bx + 10, ty, bw - 20, ln, 9.5, "sans", MUTED, 1.3) + 3
    return s


def build_project():
    s = Sheet("cheatsheet-2-project")
    s.header("QA AI base: project cheat sheet", "Cheat sheet 2 of 6. PLACEHOLDER: fill in when the setup is finished. Facts below are from CLAUDE.md; blanks are UNKNOWN until Discovery.")
    # col 1: repo map
    x1, w1 = 36, 340
    s.text(x1, 130, "Where things live", 14, "bold")
    y = 146
    for path, what, chip, kind in REPO:
        s.rect(x1, y, w1, 44, CARD, LINE, 1, 5)
        s.text(x1 + 10, y + 18, path, 10.5, "mono")
        s.text(x1 + 10, y + 34, what, 9.5, "sans", MUTED)
        cw = measure(chip, 9.5, "bold") + 14
        s.chip(x1 + w1 - 10 - cw, y + 13, chip, kind)
        y += 50
    # col 2: chain
    x2, w2 = 400, 330
    s.text(x2, 130, "The chain: Claude, human, deterministic", 14, "bold")
    y = 146
    s.chip(x2, y, "C  Claude with a skill", "plain")
    s.chip(x2 + 150, y, "H  human gate", "plain")
    s.rect(x2 + 150, y, measure("H  human gate", 9.5, "bold") + 14, 17, "none", INK, 2, 3)
    s.chip(x2 + 250, y, "D  no AI", "plain")
    y += 30
    for lab, txt in CHAIN:
        if lab == "H":
            s.rect(x2 + 14, y, w2 - 14, 34, PAPER, INK, 2, 5)
            s.text(x2 + 28, y + 22, "H", 12, "bold")
            s.text(x2 + 52, y + 22, txt, 11, "sans", INK)
        elif lab == "D":
            s.rect(x2 + 14, y, w2 - 14, 34, BAND, LINE, 1, 5)
            s.text(x2 + 28, y + 22, "D", 12, "bold", MUTED)
            s.text(x2 + 52, y + 22, txt, 11, "sans", INK)
        else:
            s.rect(x2 + 14, y, w2 - 14, 34, CARD, LINE, 1, 5)
            s.text(x2 + 28, y + 22, "C", 12, "bold", MUTED)
            s.text(x2 + 52, y + 22, txt, 11, "mono", INK)
        y += 42
    s.text(x2, y + 8, "Manual testing runs in parallel and feeds the release decision.", 9.5, "sans", MUTED)
    s.text(x2, y + 22, "Source: docs/schemes/08-mvp-chain.md (working draft).", 9.5, "sans", MUTED)
    # col 3: blanks and rules
    x3, w3 = 754, 333
    s.text(x3, 130, "Fill in (UNKNOWN until Discovery)", 14, "bold")
    y = 146
    for b in BLANKS:
        s.rect(x3, y, w3, 40, CARD, LINE, 1, 5)
        s.text(x3 + 10, y + 16, b, 10, "sans", MUTED)
        s.line(x3 + 10, y + 33, x3 + w3 - 96, y + 33, MUTED, 0.8)
        s.chip(x3 + w3 - 10 - (measure("UNKNOWN", 9.5, "bold") + 14), y + 20, "UNKNOWN", "un")
        y += 46
    y += 14
    s.text(x3, y, "Rules to keep in view", 14, "bold")
    y += 10
    h = sum(len(wrap(r, 10.5, w3 - 40)) * 14 + 8 for r in PROJ_RULES) + 12
    s.rect(x3, y + 6, w3, h, BAND, None, 0, 5)
    ty = y + 28
    for r in PROJ_RULES:
        s.text(x3 + 12, ty, "•", 11, "sans", AMBER_T)
        ty += s.para(x3 + 26, ty, w3 - 40, r, 10.5, "sans", INK, 1.3) + 8
    return s


def main():
    out = []
    s1, _ = build_terms_p1()
    out.append(s1)
    out.append(build_terms_p2())
    out.append(build_project())
    for s in out:
        s.save()
    # print-ready PDFs
    for pdf, names in [("cheatsheet-1-terms.pdf", ["cheatsheet-1-terms-p1", "cheatsheet-1-terms-p2"]),
                       ("cheatsheet-2-project.pdf", ["cheatsheet-2-project"])]:
        d = fitz.open()
        for n in names:
            sv = fitz.open(os.path.join(HERE, n + ".svg"))
            d.insert_pdf(fitz.open("pdf", sv.convert_to_pdf()))
        d.save(os.path.join(HERE, pdf))
    print("built:", sorted(f for f in os.listdir(HERE) if f.startswith("cheatsheet")))


if __name__ == "__main__":
    main()
