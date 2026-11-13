#!/usr/bin/env python3
"""Rebuild the two treasure-map pictures used in the README.

  python3 tools/build_stlc_map.py [--map stlc|loop] [--minicharts DIR] [--out-dir DIR] [--no-html]

Reads docs/img/<name>.js (the drawing) and writes, next to it by default:
  <name>.svg   static picture for the README
  <name>.html  the same card as an interactive page (touch a station)
The maps: stlc (the QA lifecycle, seven stages) and loop (the improvement loop, nine steps).
Without --map both are built.

Needs node and a local copy of the Minicharts skill (MIT, April Zhu). Neither is a
dependency of the plugin: they are used only to redraw this picture. The folder is taken
from --minicharts, then $MINICHARTS_DIR, then ~/.claude/skills/minicharts.

The drawing is seeded, so the same source gives the same SVG. The SVG stores the SHA-256
of its source.
"""
import argparse
import colorsys
import hashlib
import html
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMG = os.path.join(ROOT, "docs", "img")

MAPS = {
    "stlc": dict(
        file="stlc-map", chart_id="stlcmap",
        title="The QA lifecycle, as a treasure map",
        sub="seven stages, a red X wherever a person decides",
        foot="Illustrative drawing of the process, no data. The numbers are the order on the map, not the stage numbers in docs/CONCEPT.md."),
    "loop": dict(
        file="loop-map", chart_id="loopmap",
        title="The improvement loop, as a treasure map",
        sub="nine steps, a red X where a person decides",
        foot="Illustrative drawing of the process, no data. The numbers are the order on the map."),
}

# Colour softening, copied from Minicharts assets/build.py (MIT, (c) 2026 April Zhu),
# so the static SVG gets the same palette as the page that build.py makes.
SAT, LIFT = .8, .08
PIGMENTS = [(13, .56), (40, .74), (86, .34), (150, .28), (208, .3), (345, .42)]


def soften(m):
    r, g, b = (int(m[0][i:i + 2], 16) / 255 for i in (1, 3, 5))
    h, l, s = colorsys.rgb_to_hls(r, g, b)
    if l > .3:
        l += (.8 - l) * LIFT
    if .2 < l < .58:
        l += (.62 - l) * .42
    if s > .04:
        d, cap = min(PIGMENTS, key=lambda a: min(abs(a[0] - h * 360), 360 - abs(a[0] - h * 360)))
        e = (d - h * 360 + 180) % 360 - 180
        h = ((h * 360 + e * .6) % 360) / 360
        s = min(cap, s * SAT)
    return "#" + "".join(f"{round(v * 255):02x}" for v in colorsys.hls_to_rgb(h, l, s))


def soft(js):
    return re.sub(r"#[0-9a-fA-F]{6}\b", soften, js)


# Draws one card the way Minicharts run.js does, without a browser.
NODE = r"""
const fs = require('fs');
const [dir, chart, id] = process.argv.slice(2);
const src = 'const LIT = {}, ALT = {}, SVGMODE = true;\n' + fs.readFileSync(dir + '/engine.js', 'utf8') + '\n'
  + fs.readFileSync(dir + '/examples.js', 'utf8') + '\n' + fs.readFileSync(chart, 'utf8') + `
;{ const c = CARDS.find(c => c.id === ${JSON.stringify(id)});
  if (!c) throw new Error('no card with id ' + ${JSON.stringify(id)});
  let h = 7; for (const ch of c.id) h = Math.imul(h, 31) + ch.charCodeAt(0) | 0;
  begin(h); LOOSE = .22; OX = 260; OY = 210; c.draw.call(c); flush(); LOOSE = 0;
  globalThis.__r = {body: out.join(''), defs: pencilDefs(), w: SHW, h: SHH, name: c.name, of: c.of}; }`;
(0, eval)(src);
process.stdout.write(JSON.stringify(globalThis.__r));
"""

STYLE = ('text{font-family:Gaegu,"DM Sans","Comic Sans MS","Segoe Print",sans-serif}'
         ".cap{letter-spacing:1px}.it{letter-spacing:.3px}.ser{font-family:Georgia,serif}")
PAD = 12
EXTRA = 62  # room under the sheet for the status line that follows the pirate


def source_hash(text):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def render_svg(minicharts, source_text, m):
    chart_id, TITLE, FOOT = m["chart_id"], m["title"], m["foot"]
    assets = os.path.join(minicharts, "assets")
    with tempfile.TemporaryDirectory() as tmp:
        chart = os.path.join(tmp, "chart.js")
        runner = os.path.join(tmp, "render.js")
        with open(chart, "w", encoding="utf-8") as f:
            f.write(soft(source_text))
        with open(runner, "w", encoding="utf-8") as f:
            f.write(NODE)
        run = subprocess.run(["node", runner, assets, chart, chart_id],
                             capture_output=True, text=True)
    if run.returncode != 0:
        sys.exit("node failed:\n" + run.stderr.strip()[-2000:])
    r = json.loads(run.stdout)
    body = r["body"]
    for bad in ("NaN", "undefined"):
        if bad in body:
            sys.exit(f"the drawing contains {bad}; fix docs/img/{m['file']}.js")
    defs = r["defs"]
    if "<defs" not in defs:
        defs = f"<defs>{defs}</defs>"
    w, h = r["w"], r["h"] + EXTRA
    label = html.escape(f'{r["name"]}: {r["of"]}. {FOOT}', quote=True)
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{-PAD} {-PAD} {w + 2 * PAD} {h + 2 * PAD}" '
        f'width="{2 * (w + 2 * PAD)}" role="img" aria-label="{label}" '
        f'data-source-sha256="{source_hash(source_text)}">\n'
        f"<!-- Generated by tools/build_stlc_map.py from docs/img/{m['file']}.js. Do not edit by hand. "
        "Drawn with Minicharts by April Zhu (MIT). -->\n"
        f"<title>{html.escape(TITLE)}</title>\n<style>{STYLE}</style>\n"
        f'<rect x="{-PAD}" y="{-PAD}" width="{w + 2 * PAD}" height="{h + 2 * PAD}" rx="10" fill="#fbf6ec"/>\n'
        f"{defs}\n{body}\n</svg>\n"
    )


def build(a, m):
    source = os.path.join(IMG, m["file"] + ".js")
    with open(source, encoding="utf-8") as f:
        source_text = f.read()
    os.makedirs(a.out_dir, exist_ok=True)
    svg_path = os.path.join(a.out_dir, m["file"] + ".svg")
    with open(svg_path, "w", encoding="utf-8") as f:
        f.write(render_svg(a.minicharts, source_text, m))
    print("wrote", svg_path)

    if not a.no_html:
        html_path = os.path.join(a.out_dir, m["file"] + ".html")
        run = subprocess.run([sys.executable, os.path.join(a.minicharts, "assets", "build.py"), source,
                              "-o", html_path, "--title", m["title"], "--sub", m["sub"], "--foot", m["foot"]],
                             capture_output=True, text=True)
        if run.returncode != 0:
            sys.exit("build.py failed:\n" + run.stderr.strip()[-2000:])
        # the note under the card follows the pirate: it reads the SVG's own animation clock
        with open(html_path, encoding="utf-8") as f:
            page = f.read()
        script = ("<script>addEventListener('load',()=>{const W=window.STLC_STAGES,c=document.querySelector('.card'),"
                  "sv=c&&c.querySelector('svg'),n=c&&c.querySelector('.note');if(!W||!sv||!n)return;let last=-1;"
                  "setInterval(()=>{const t=(sv.getCurrentTime()%W.dur)/W.dur;let k=W.win.findIndex(w=>t>=w[0]&&t<w[1]);"
                  "if(k<0)k=0;if(k===last)return;last=k;c.dataset.note=W.text[k];"
                  "if(!c.classList.contains('live'))n.textContent=W.text[k];},150);});</script>")
        page = page.replace("</body>", script + "</body>") if "</body>" in page else page + script
        with open(html_path, "w", encoding="utf-8") as f:
            f.write(page)
        print("wrote", html_path)


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--map", choices=sorted(MAPS), help="build one map only (default: both)")
    ap.add_argument("--minicharts", default=os.environ.get("MINICHARTS_DIR")
                    or os.path.expanduser("~/.claude/skills/minicharts"))
    ap.add_argument("--out-dir", default=IMG)
    ap.add_argument("--no-html", action="store_true")
    a = ap.parse_args()

    if not shutil.which("node"):
        sys.exit("node not found: it is needed to redraw the picture")
    for name in ("engine.js", "examples.js", "build.py"):
        if not os.path.isfile(os.path.join(a.minicharts, "assets", name)):
            sys.exit(f"Minicharts not found at {a.minicharts} (missing assets/{name}); "
                     "pass --minicharts DIR or set MINICHARTS_DIR")
    for key in ([a.map] if a.map else sorted(MAPS)):
        build(a, MAPS[key])


if __name__ == "__main__":
    main()
