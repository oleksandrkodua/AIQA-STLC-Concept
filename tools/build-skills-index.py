#!/usr/bin/env python3
"""Build and check the skills navigator index (DRAFT, see docs/specs/2026-10-13-skills-navigator-design.md).

  python3 tools/build-skills-index.py            write plugins/qabase/skills-index.json (after checking)
  python3 tools/build-skills-index.py --check    check only; exit 1 on any problem or a stale index
  python3 tools/build-skills-index.py --accept <skill>
                                                  record that a person re-read the skill's access sections
                                                  and confirmed `needs` (rewrites access_checked)

Inputs: plugins/qabase/skills/*/SKILL.md (name, description, STATUS), plugins/qabase/skills/*/NAVIGATOR.yaml
(hand-written: sector, intents, needs, access_checked, optional phrases, optional then), plugins/qabase/navigator-sectors.yaml.
Python standard library only. The YAML subset read here: `key: value` lines, `key:` followed by `  - item` lines, `#` comments.
Reads and writes only inside plugins/qabase/. No network."""
import hashlib, json, os, re, sys, glob

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PLUGIN = os.path.join(ROOT, "plugins", "qabase")
SKILLS = os.path.join(PLUGIN, "skills")
SECTORS_FILE = os.path.join(PLUGIN, "navigator-sectors.yaml")
INDEX_FILE = os.path.join(PLUGIN, "skills-index.json")
ALLOWED_KEYS = {"sector", "intents", "needs", "access_checked", "phrases", "then"}
# Sections whose text decides what a skill needs before it can run; a change in any of them makes `needs` stale.
NEEDS_SECTIONS = ("Access", "Preconditions", "Required inputs", "Required context")

def read(p):
    with open(p, encoding="utf-8") as f: return f.read()

def parse_subset(text, where):
    """Returns (dict, errors). Values are str or list[str]."""
    out, errors, cur = {}, [], None
    for n, raw in enumerate(text.splitlines(), 1):
        line = raw.split(" #")[0].rstrip() if " #" in raw else raw.rstrip()
        if not line.strip() or line.lstrip().startswith("#"): continue
        m = re.match(r"^- (.+)$", line.strip()) if line.startswith((" ", "-")) else None
        if m:
            if cur is None or not isinstance(out.get(cur), list):
                errors.append(f"{where}:{n}: list item without a list key"); continue
            out[cur].append(m.group(1).strip().strip('"').strip("'")); continue
        km = re.match(r"^([A-Za-z_][A-Za-z0-9_-]*):\s*(.*)$", line)
        if not km or line.startswith(" "):
            errors.append(f"{where}:{n}: cannot read line: {raw.strip()[:60]}"); continue
        key, val = km.group(1), km.group(2).strip()
        if key in out: errors.append(f"{where}:{n}: duplicate key {key}")
        if val == "": out[key] = []; cur = key
        else: out[key] = val.strip('"').strip("'"); cur = None
    return out, errors

def frontmatter(skill_md):
    # name and description first; other frontmatter keys (checked by evals/validate_repo.py) may follow
    m = re.match(r"---\nname: (.+)\ndescription: (.+)\n(?:(?:[A-Za-z_-]+:.*|[ \t]+.*)\n)*---\n", skill_md)
    if not m: return None, None
    desc = m.group(2).strip()
    if re.fullmatch(r"[>|][+-]?", desc): return None, None  # block scalar: the description would be recorded as ">" or "|"
    return m.group(1).strip(), desc

def needs_hash(skill_md):
    """Hash of the sections that define what the skill needs (whitespace-normalised)."""
    parts = []
    fm = re.match(r"---\n(.*?)\n---\n", skill_md, re.S)
    for key in ("allowed-tools", "disallowed-tools"):  # tool limits are part of what the skill needs
        km = re.search(r"^" + key + r":[ \t]*(.*)$", fm.group(1) if fm else "", re.M)
        if km: parts.append(key + ":" + " ".join(km.group(1).split()))
    for h in NEEDS_SECTIONS:
        m = re.search(r"^## (?:\d+\.\s*)?" + h + r".*?\n(.*?)(?=^## |\Z)", skill_md, re.M | re.S)
        if m: parts.append(h + ":" + " ".join(m.group(1).split()))
    return hashlib.sha256("\n".join(parts).encode("utf-8")).hexdigest()[:12]

def collect():
    errors, sectors = [], []
    if not os.path.exists(SECTORS_FILE):
        return [], [f"missing {os.path.relpath(SECTORS_FILE, ROOT)}"], []
    sec, e = parse_subset(read(SECTORS_FILE), "navigator-sectors.yaml"); errors += e
    for k, v in sec.items():
        if not isinstance(v, str) or not v: errors.append(f"sector {k}: title must be a non-empty text")
        sectors.append({"id": k, "title": v if isinstance(v, str) else ""})
    ids = [s["id"] for s in sectors]
    names = sorted(os.path.basename(d.rstrip("/")) for d in glob.glob(os.path.join(SKILLS, "*/")))
    skills = []
    for name in names:
        d = os.path.join(SKILLS, name)
        sm = os.path.join(d, "SKILL.md")
        if not os.path.exists(sm): errors.append(f"{name}: SKILL.md missing"); continue
        text = read(sm)
        fm_name, desc = frontmatter(text)
        if fm_name != name: errors.append(f"{name}: frontmatter name does not match the folder"); continue
        nav = os.path.join(d, "NAVIGATOR.yaml")
        if not os.path.exists(nav): errors.append(f"{name}: NAVIGATOR.yaml missing (create it: sector, intents, needs, access_checked)"); continue
        data, e = parse_subset(read(nav), f"{name}/NAVIGATOR.yaml"); errors += e
        for k in data:
            if k not in ALLOWED_KEYS: errors.append(f"{name}: unknown key '{k}' in NAVIGATOR.yaml")
        sector = data.get("sector")
        if not isinstance(sector, str) or sector not in ids: errors.append(f"{name}: sector '{sector}' is not one of {ids}")
        intents = data.get("intents")
        if not isinstance(intents, list) or not (2 <= len(intents) <= 4) or any(not i or len(i) > 100 for i in intents):
            errors.append(f"{name}: intents must be 2-4 non-empty phrases of at most 100 characters")
        needs = data.get("needs")
        if not isinstance(needs, str) or not needs: errors.append(f"{name}: needs must be a non-empty text")
        phrases = data.get("phrases", [])
        if not isinstance(phrases, list) or any(not p or len(p) > 100 for p in phrases): errors.append(f"{name}: phrases must be a list of non-empty phrases of at most 100 characters")
        then = data.get("then", [])
        if not isinstance(then, list) or any(t not in names or t == name for t in then):
            errors.append(f"{name}: then must be a list of other existing skill names (got {then})")
        now = needs_hash(text)
        if data.get("access_checked") != now:
            errors.append(f"{name}: needs may be stale: the access/precondition sections changed (hash {now}, recorded {data.get('access_checked')}). "
                          f"Re-read them, fix `needs` if needed, then run: python3 tools/build-skills-index.py --accept {name}")
        status = re.search(r"^STATUS: ?(SKELETON|DRAFT|RESERVED)", text, re.M)
        cut = re.search(r"\b[Nn]ot (for|a|an)\b", desc)
        tail = desc[cut.start():] if cut else ""
        not_for = [n for n in names if n != name and re.search(r"(?<![a-z-])" + re.escape(n) + r"(?![a-z-])", tail)]
        skills.append({"name": name, "sector": sector, "intents": intents, "phrases": phrases, "needs": needs,
                       "not_for": not_for, "then": then, "command": f"/qabase:{name}",
                       "maturity": status.group(1).lower() if status else "unmarked", "description": desc})
    order = {s: i for i, s in enumerate(ids)}
    skills.sort(key=lambda s: (order.get(s["sector"], 99), s["name"]))
    return sectors, errors, skills

def render(sectors, skills):
    return json.dumps({"generated_from": "plugins/qabase/skills/*/NAVIGATOR.yaml and SKILL.md; do not edit by hand",
                       "sectors": sectors, "skills": skills}, indent=1, ensure_ascii=False) + "\n"

def main(argv):
    if argv[:1] == ["--accept"]:
        if len(argv) != 2 or not re.fullmatch(r"[a-z0-9-]+", argv[1]): print("usage: --accept <skill-name>"); return 2
        d = os.path.join(SKILLS, argv[1]); nav = os.path.join(d, "NAVIGATOR.yaml")
        if not (os.path.exists(nav) and os.path.exists(os.path.join(d, "SKILL.md"))): print(f"no such skill or NAVIGATOR.yaml: {argv[1]}"); return 2
        h = needs_hash(read(os.path.join(d, "SKILL.md"))); t = read(nav)
        t2 = re.sub(r"^access_checked:.*$", f"access_checked: {h}", t, flags=re.M)
        if t2 == t and f"access_checked: {h}" not in t: t2 = t.rstrip("\n") + f"\naccess_checked: {h}\n"
        with open(nav, "w", encoding="utf-8") as f: f.write(t2)
        print(f"{argv[1]}: access_checked = {h} (confirm that `needs` is still right)"); return 0
    check_only = argv[:1] == ["--check"]
    if argv and not check_only: print(__doc__); return 2
    sectors, errors, skills = collect()
    if errors:
        for e in errors: print("FAIL " + e)
        return 1
    new = render(sectors, skills)
    if check_only:
        have = read(INDEX_FILE) if os.path.exists(INDEX_FILE) else None
        if have != new: print("FAIL skills-index.json is missing or stale: run python3 tools/build-skills-index.py"); return 1
        print(f"OK {len(skills)} skills, {len(sectors)} sectors, index current"); return 0
    with open(INDEX_FILE, "w", encoding="utf-8") as f: f.write(new)
    print(f"wrote {os.path.relpath(INDEX_FILE, ROOT)}: {len(skills)} skills, {len(sectors)} sectors"); return 0

if __name__ == "__main__": sys.exit(main(sys.argv[1:]))
