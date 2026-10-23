# Animation gallery for the lesson template

STATUS: DRAFT v0.1, 2026-10-07. Not yet used in any published lesson.

- `gallery.html`: 18 animation ideas on one page (open in a browser). Set A = 10 general motion patterns. Set B = 8 ideas reconstructed from the static frames of a reference deck (the original motion was not observed).
- Palette: the course palette (Paper/Amber, `../../_specs/2026-10-14-colors-design.md`), applied 2026-10-23. The earlier "Maple" placeholder values are kept in the table below as history.

## Colour swap table (Maple placeholder → course palette, done 2026-10-23)

| Role | Maple value (old) | Course value (now) |
|---|---|---|
| accent (key word, ring), as a fill or line | `#A93E17` | `--amber` `#E0A030` |
| accent used as text | `#A93E17` | `--amber-text` `#9A5B0A` (amber is never text, spec rule 1) |
| gold (attention, gate) | `#C98A1B` | `--amber-text` `#9A5B0A` |
| green (ok, our repo) | `#5E6B2E` | `--leaf` `#4E7A3A` |
| ink | `#2B1D14` | `--ink` `#231F1A` |
| muted text | `#6B5646` | `--muted` `#4A4339` |
| card | `#FFFAF0` | `--card` `#FFFBF0` |
| line | `#C9B79A` | `--line` `#D9CDB0` |

The minor Maple shades (borders, track of the ring, captions, page background) were mapped to `--line`, `--band`, `--muted` and `--ground`. The gallery now uses only palette values.

## Where each animation is meant to be used

| Slide type | Animation |
|---|---|
| Cover | A5 falling leaves, B2 hourglass |
| Chapter opener | A1 or B7 ring, B1 living line |
| Flow diagram | A2 or B3 dot along arrow, A3 steps rise |
| Gap, cost, growth | B4 two curves, A4 bars grow |
| Errors, variants | B5 branching |
| Review of an answer | B6 glasses sweep |
| Gate (hooks, permissions, evals) | A6 gate |
| Term moves to the map | A8 magic move |
| Key word | A9 underline |
| Homework or recap card | A10 slide in |
| Background | B8 drifting blobs (off by default in PDF) |

## Rules

- At most one ambient and one meaningful animation per slide.
- Every slide must read correctly from its final still frame (PDF/PPTX export shows only that).
- Slides type limits: build-in effects (`fade rise pop drop left right scale`), transitions (`fade push magic`), and live embeds (`x-embed`, up to 16 KB, up to 8 per slide, no network, not clickable). Which of A1–B8 are done as build-in and which as embeds is decided at template build.
- Reduced motion: CSS animations stop under `prefers-reduced-motion`; SMIL (`animateMotion`, `animate`) is not stopped by that CSS rule and needs handling in the build. NOT VERIFIED in the Slides runtime.
- Auto-playing motion longer than 5 s next to other content should be pausable (WCAG 2.2.2 is a web-page rule; whether it applies to a live presentation is a judgment call).

## See also

- `knowledge/register.md` R-18: third-party notes on prompting animations (numbers not adjectives, frame-numbered review notes, contact sheet). Ideas only, unverified, no content copied.
