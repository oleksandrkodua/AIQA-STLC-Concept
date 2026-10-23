#!/usr/bin/env python3
"""Structure checks for the repository. Run from the root: python3 evals/validate_repo.py
Checks structure only; says nothing about whether content is correct or the rules work."""
import json, os, re, sys, glob

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
problems, passed = [], 0

def check(name, ok, detail=""):
    global passed
    if ok: passed += 1; print(f"PASS  {name}")
    else: problems.append(name); print(f"FAIL  {name} {detail}")

# 1 CLAUDE.md length
n = len(open("CLAUDE.md", encoding="utf-8").read().splitlines())
check("CLAUDE.md under 100 lines", n < 100, f"({n} lines)")

# 2 JSON files valid
for f in glob.glob("**/*.json", recursive=True) + glob.glob(".claude/**/*.json", recursive=True) + [".mcp.json"]:
    try: json.load(open(f, encoding="utf-8")); ok = True
    except Exception as e: ok = False
    check(f"valid JSON: {f}", ok)

# 3 skills: frontmatter, folder name, evals
for d in sorted(glob.glob(".claude/skills/*/")):
    name = os.path.basename(d.rstrip("/"))
    p = os.path.join(d, "SKILL.md")
    if not os.path.exists(p): check(f"skill {name}: SKILL.md exists", False); continue
    t = open(p, encoding="utf-8").read()
    m = re.match(r"---\nname: (.+)\ndescription: (.+)\n---\n", t)
    check(f"skill {name}: frontmatter name matches folder", bool(m) and m.group(1).strip() == name)
    check(f"skill {name}: description present and < 1100 chars", bool(m) and 20 < len(m.group(2)) < 1100)
    if re.search(r"^STATUS: SKELETON", t, re.M):
        check(f"skill {name}: SKELETON, evals not required yet (not claimed as working)", True)
    else:
        check(f"skill {name}: evals/evals.json exists", os.path.exists(os.path.join(d, "evals", "evals.json")))

# 3b skill descriptions say when NOT to use the skill (names the neighbour); checked on the plugin source (SKILL-CONTRACT line 10)
EXCL = r"\b(not for|not a|not an|do not use|never use)\b|\(use [a-z-]+\)|use [a-z-]+ instead"
for p in sorted(glob.glob("plugins/qabase/skills/*/SKILL.md")):
    name = os.path.basename(os.path.dirname(p))
    m = re.match(r"---\nname: (.+)\ndescription: (.+)\n---\n", open(p, encoding="utf-8").read())
    check(f"plugin skill {name}: description says when NOT to use it", bool(m) and bool(re.search(EXCL, m.group(2), re.I)))

# 3c a "(use X)" or "use X instead" pointer in a description names a skill that exists (a machine check, not a reader's check)
_skill_names = {os.path.basename(os.path.dirname(p)) for p in glob.glob("plugins/qabase/skills/*/SKILL.md")}
for p in sorted(glob.glob("plugins/qabase/skills/*/SKILL.md")):
    name = os.path.basename(os.path.dirname(p))
    m = re.match(r"---\nname: (.+)\ndescription: (.+)\n---\n", open(p, encoding="utf-8").read())
    refs = [(a or b).lower() for a, b in re.findall(r"\(use ([a-z][a-z-]*)\)|use ([a-z][a-z-]*) instead", m.group(2), re.I)] if m else []
    unknown = [r for r in refs if r not in _skill_names]
    check(f"plugin skill {name}: skills named in its description exist", not unknown, ("(unknown: " + ", ".join(unknown) + ")") if unknown else "")

# 3d every plugin skill has a Tools or Access section It checks that the section exists, not that its text is right: a person reads that.
for p in sorted(glob.glob("plugins/qabase/skills/*/SKILL.md")):
    name = os.path.basename(os.path.dirname(p))
    check(f"plugin skill {name}: has a Tools or Access section", bool(re.search(r"^## (?:\d+\.\s*)?(Access|Tools)\b", open(p, encoding="utf-8").read(), re.M)))

# 4 scoped rules carry paths
for f, glob_ in ((".claude/rules/playwright-rules.md", "automation/web/**"), (".claude/rules/mobile-rules.md", "automation/mobile/**")):
    t = open(f, encoding="utf-8").read()
    check(f"{os.path.basename(f)} scoped to {glob_}", t.startswith("---\npaths:") and glob_ in t.split("---")[1])

# 5 settings draft references existing hook scripts
s = json.load(open(".claude/settings.draft.json"))
cmds = [h["command"] for ev in s["hooks"].values() for blk in ev for h in blk["hooks"]]
for c in cmds:
    m = re.search(r"\.claude/hooks/([\w\-.]+\.py)", c)
    check(f"hook script exists: {m.group(1) if m else c}", bool(m) and os.path.exists(f".claude/hooks/{m.group(1)}"))
# active settings.json is a per-machine install (apply-trusted-changes.sh); when present it must equal one of the two committed profiles
if os.path.exists(".claude/settings.json"):
    _act = open(".claude/settings.json", encoding="utf-8").read()
    check("active .claude/settings.json equals a committed profile (qa or maintainer)",
          _act in (open("tools/settings.qa.json", encoding="utf-8").read(), open("tools/settings.shared.json", encoding="utf-8").read()))
else:
    check("active settings.json absent (not installed on this machine)", True)

# 6 relative paths in READMEs exist (backticked, with a slash or known extension)
SKIP = ("automation/web", "automation/mobile", "automation/api", "evals/runs", "settings.json", "~/", "<", "*", "http", ".claude/hooks/prod")
# descriptive names (what a skill or project contains), not claims that the path exists here
GENERIC = {"SKILL.md", "package.json", "tsconfig.json", "android/", "ios/", "references/", "evals/"}
ALLNAMES = {n + ("/" if os.path.isdir(os.path.join(dp, n)) else "") for dp, dn, fn in os.walk(".") for n in dn + fn}
for f in ("README.md", "CLAUDE.md"):
    for ref in set(re.findall(r"`([A-Za-z0-9_.\-/]+(?:/|\.md|\.json|\.py))`", open(f, encoding="utf-8").read())):
        if any(k in ref for k in SKIP) or ref.startswith(("npm", "npx")) or ref in GENERIC: continue
        if "/" not in ref.rstrip("/"):
            check(f"{f} bare name exists somewhere: {ref}", ref in ALLNAMES); continue
        check(f"{f} references existing path: {ref}", os.path.exists(ref) or os.path.exists(os.path.join(".claude", ref)) or os.path.exists(os.path.join("decisions", ref)) or os.path.exists(os.path.join("evals", ref)))

# 7 no secret-looking strings
pat = re.compile(r"(AKIA[0-9A-Z]{16}|xox[baprs]-[0-9A-Za-z-]{10,}|ghp_[0-9A-Za-z]{30,}|-----BEGIN [A-Z ]*PRIVATE KEY-----|(?i:password|passwd|api[_-]?key|secret|token)\s*[:=]\s*['\"](?![$<{])[^'\"\s]{8,})")
hits = []
# synthetic test inputs that are meant to look like secrets (a redactor's own test); exact file + exact string only
KNOWN_FIXTURES = set()
for f in glob.glob("**/*", recursive=True) + glob.glob(".claude/**/*", recursive=True):
    if os.path.isfile(f) and not f.endswith((".png",)):
        try: t = open(f, encoding="utf-8").read()
        except Exception: continue
        for m in pat.finditer(t):
            if (f, m.group(0)) in KNOWN_FIXTURES: continue
            hits.append((f, m.group(0)[:20]))
check("no secret-looking strings", not hits, str(hits[:3]))

# 8 mermaid blocks present in every scheme
for f in sorted(glob.glob("docs/schemes/*.md")):
    check(f"{f} has a mermaid block", "```mermaid" in open(f, encoding="utf-8").read())

# 9 start-of-session context budget: what is loaded every session (CLAUDE.md + rules without paths: + skill name/description).
# Estimate only: UTF-8 bytes / 4 is NOT a tokenizer count. It does not include the system prompt, user-level MCP/plugins or memory.
BUDGET_TOKENS = 10000  # proposed ceiling (measured 2026-10-13: about 6.5k); change it by a decision, not to silence the check
def _est(text): return len(text.encode("utf-8")) // 4
parts = {"CLAUDE.md": _est(open("CLAUDE.md", encoding="utf-8").read())}
rules = 0
for f in sorted(glob.glob(".claude/rules/*.md")):
    t = open(f, encoding="utf-8").read()
    if not re.match(r"---\npaths:", t): rules += _est(t)
parts["rules without paths:"] = rules
desc = 0
for f in sorted(glob.glob("plugins/qabase/skills/*/SKILL.md")):
    m = re.match(r"---\nname: (.+)\ndescription: (.+)\n---\n", open(f, encoding="utf-8").read())
    if m: desc += _est(m.group(1) + m.group(2))
parts["skill names+descriptions"] = desc
total = sum(parts.values())
check(f"always-loaded context within budget (~{total} of {BUDGET_TOKENS} est. tokens)", total <= BUDGET_TOKENS,
      "(" + ", ".join(f"{k} ~{v}" for k, v in parts.items()) + ")")
print("      breakdown: " + ", ".join(f"{k} ~{v}" for k, v in parts.items()))

# 10 skills navigator: every skill has a valid NAVIGATOR.yaml, needs not stale, skills-index.json current (tools/build-skills-index.py --check)
import subprocess
_r = subprocess.run([sys.executable, "-I", "tools/build-skills-index.py", "--check"], capture_output=True, text=True)
check("skills navigator index valid and current", _r.returncode == 0, "\n      " + (_r.stdout + _r.stderr).strip().replace("\n", "\n      ")[:1500])

# 11 permission profiles: strict QA profile denies every trusted path the maintainer profile only asks about, keeps its deny rules, and the apply script knows both profiles
_qa = json.load(open("tools/settings.qa.json")); _mt = json.load(open("tools/settings.shared.json"))
_qd = set(_qa["permissions"]["deny"])
def _covered(rule):  # exact, or a deny on a parent directory (plugins/** covers plugins/qabase/**)
    tool, path = rule[:-1].split("(", 1)
    return any(d.split("(")[0] == tool and (d == rule or (d[:-1].split("(", 1)[1].endswith("/**") and path.startswith(d[:-1].split("(", 1)[1][:-2]))) for d in _qd)
_missing = [a for a in _mt["permissions"]["ask"] if a.split("(")[0] in ("Edit", "Write") and not _covered(a)]
_lost = [d for d in _mt["permissions"]["deny"] if d not in _qd]
_qa_ask_edit = [a for a in _qa["permissions"].get("ask", []) if a.split("(")[0] in ("Edit", "Write")]
_sh = open("tools/apply-trusted-changes.sh", encoding="utf-8").read()
check("strict QA profile: every maintainer Edit/Write ask is a deny, no deny rule lost, no Edit/Write ask left",
      not _missing and not _lost and not _qa_ask_edit, f"(missing deny: {_missing}; lost: {_lost}; ask left: {_qa_ask_edit})")
check("apply-trusted-changes.sh supports --profile qa|maintainer", "--profile" in _sh and "settings.qa.json" in _sh)

print(f"\n{passed} passed, {len(problems)} failed")
sys.exit(1 if problems else 0)
