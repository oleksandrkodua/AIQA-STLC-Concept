# Design system audit: training, mockups, cheatsheets, portfolio, schemes

STATUS: DRAFT, 2026-10-23. Read-only audit; nothing was changed. Provenance: ai-generated (Claude Code, cloud session; model and version not recorded); human-confirmed: pending.
Method: a script read every `.html`, `.svg` and the cheatsheet builder in the repository (36 files) and counted colours outside `:root`, font families and sizes, radii, spacing, class names, `lang`, `<title>`, `prefers-color-scheme` and `prefers-reduced-motion`. Contrast was computed with the WCAG 2 relative-luminance formula, not in a rendering tool. The Figma connector was not available in this session, so nothing outside the repository was audited.
Source of truth used: `training/lessons/_specs/2026-10-14-colors-design.md` (13-colour palette, contrast rules, meaning of colours).

## Summary
Visual systems found: 5 | Files: 36 | Issues: 11 (2 high, 5 medium, 4 low) | Score: 36/100 (rubric below; the rubric is this audit's own, not a standard).

| System | Files | Palette | Tokens | Font sizes |
|---|---|---|---|---|
| Lesson 1 decks (`lesson-01-a/b*.html`) | 4 | Paper/Amber/Forest (the spec) | `:root`, 0 hard-coded colours | 27 distinct (15-132 px) |
| Lesson 1 slides (`slides/*.html`, `deck.json`, the hosted deck) | 25 | Slate/Vermilion/Teal (`#F6F4EE`, `#16202B`, `#C8431D`, `#1F7A70`, `#FFFDF8`, `#DDD8CB`, `#5B6670`) | none: inline styles only | 7 (24, 28, 32, 36, 40, 64, 120 px) |
| Diagrams mockup (`_mockups/diagrams-mockup.html`) | 1 | Paper/Amber plus a red pair and a dark mode | own `:root` (16 variables) | SVG units in a 160x90 viewBox |
| Animation gallery (`_template/animations/gallery.html`) | 1 | "Maple" placeholder (`#A93E17`, `#C98A1B`, `#5E6B2E`, `#2B1D14`) | 7 variables, 82 hard-coded colours | 6 |
| Portfolio (`portfolio/*.html`) | 2 | Slate/Teal (`#16232C`, `#52606D`, `#0F6B7A`, white) | own `:root` (8 variables) | 28 distinct, mixing px, pt and em |
| Cheatsheets (`cheatsheets/*`) | 4 | Paper/Amber plus the red pair | Python constants in `build_cheatsheets.py` | - |
| Schemes (`docs/schemes/*.md`) | 11 | Mermaid defaults, no `classDef` | - | - |

## Issues

| # | Severity | Issue | Evidence | Recommendation |
|---|---|---|---|---|
| 1 | High | Lesson 1 exists in two designs. `01-the-map/README.md` names `deck.json` + `slides/` (25 slides, Slate palette, the hosted deck) as the source; the colours spec takes its palette from `lesson-01-a.html` and `lesson-01-b.html` (23 sections, Paper/Amber palette). | file contents | Decide which version is canonical (KNOWLEDGE CONFLICT below), then migrate the other or mark it superseded |
| 2 | High | The course palette is undecided in one place and documented in another. Gallery README: "The palette for the course is NOT decided yet (open: deep forest variant recommended)". Colours spec (2026-10-14) documents Paper/Amber as the lesson-1 palette. Four palettes are in use. | `_template/animations/README.md`; colours spec section 1 | One palette decision, recorded in the colours spec; the gallery swap table then points at it |
| 3 | Medium | Tokens are copied, not shared: the same 13 values are in four `:root` blocks, the mockup has its own 16, the cheatsheet builder has Python constants, the 25 slides hard-code their own. The red pair (`#8A2A1A` / `#F3D9D1`) exists in the mockup and the builder but not in the spec's palette table. | `:root` counts; `build_cheatsheets.py` lines 19-22 | One tokens file (CSS variables plus a JSON copy the builder reads); add red, radius and type-scale tokens |
| 4 | Medium | No type scale in the decks (27 sizes) or the portfolio (28 sizes, three units). The slides already use a clean 7-step scale. | font-size scan | Adopt the slides' scale for the 1920x1080 stage (24, 28, 32, 36, 40, 64, 120 px) as tokens; map deck sizes onto it |
| 5 | Medium | Component names are abbreviations with no shared vocabulary: decks `rise`, `lab`, `kick`, `cnt`, `q`, `n`, `t`, `r`, `lf`, `ccard`; mockup `b`, `fx`, `mu`, `k`, `sf`; the same idea has different names (`chip` / `tag`, `ccard` / `box` / card). The slides have no classes: the card markup is repeated inline in 25 files. | class scan (decks 34 classes, mockup 111, portfolio 48) | A component inventory with names (see below); rename when a file is next touched, not in a big-bang change |
| 6 | Medium | Radius is not a token: decks use 10 values (4, 5, 6, 8, 14, 16, 20, 22, 24 px, 50%, an asymmetric one), slides 16 and 12, gallery 6 values. | radius scan | Three radius tokens (small, card, pill) |
| 7 | Medium | Spec section 5 says the red pair's contrast was "NOT computed". Computed now: `#8A2A1A` on `#F3D9D1` = 6.45:1, on `--paper` = 7.82:1 (AA for body text). | this audit's formula | Record the values and make red official in section 1 |
| 8 | Low | Slides use `data-transition="fade"` on all 25 and declare no `prefers-reduced-motion`; the decks, mockup and gallery do. Whether the hosting deck viewer honours reduced motion is UNKNOWN. | scan | Check the viewer; if it does not, add the media query when slides move to tokens |
| 9 | Low | Mermaid schemes use default styling, so the meaning of colours (green / amber / red / dashed) from spec section 5 is not applied there. Status is carried by words, which is acceptable. | no `classDef` in `docs/schemes/*.md` | Optional: a shared `classDef` set for status, always paired with the word |
| 10 | Low | Two font delivery methods: decks embed IBM Plex as base64 (works offline); slides load IBM Plex Sans from Google Fonts via `deck.json` and fall back to Arial offline. | `deck.json` `faces`; `@font-face` in decks | Note in the delivery checklist: present slides online or accept the fallback |
| 11 | Low | The portfolio is a separate brand (Deck Display / Deck Mono, white, teal). | scan | Decide whether it is in the course design system; if not, say so in `portfolio/README.md` |

What passed (measured text pairs, WCAG 2 AA): every text colour measured is at least 4.5:1, or at least 3:1 where the text is 24 px bold or larger on the 1920 stage. The weakest are the slides' vermilion labels (`#C8431D` on `#F6F4EE`, 4.46:1, 24 px bold uppercase, which counts as large text) and teal on the slide background (4.68:1). `--amber` is never used as a text colour, as spec rule 1 requires. Reduced motion is handled in the decks, mockup and gallery.

```text
KNOWLEDGE CONFLICT - no authoritative resolution found
Source A: training/lessons/01-the-map/README.md: "Source in this folder: deck.json (order, sections) and slides/<id>.html" (Slate palette, 25 slides, the hosted deck)
Source B: training/lessons/_specs/2026-10-14-colors-design.md: "Source: the :root variables of lesson-01-a.html and lesson-01-b.html" (Paper/Amber palette, 23 sections)
Human confirmation required
```

## Component inventory (as found, for naming)

| Component | Decks | Slides | Mockup | Portfolio | Proposed name |
|---|---|---|---|---|---|
| Section label above a title (mono, uppercase, letter-spaced) | `kick` (26 px) | inline `p` 24 px | `k` | `part` | `eyebrow` |
| Label inside a card ("Analogy", "In our project") | `lab` (24 px) | inline `p` 24 px, coloured | not identified | not identified | `card-label` |
| Slide title | `h2` | inline `h2` 64 px | `h` | `h2` | `title` |
| Lead sentence | not identified | inline `p` 40 px | - | `lede` | `lead` |
| Question row with a numbered circle | `q` + `n` + `t` (48 px) | - | - | - | `numbered-item` |
| Card | `ccard` | inline `div` (bg, 1 px line, radius 16, padding 40) | `fx`/`mock` | `box` | `card` |
| Status or term chip | `chip`, `mono` | - | `tag`, `mm-on`/`mm-off` | `tag`, `term` | `chip` (with a `status-*` modifier that always carries a word) |
| Footer | `foot` | - | - | `foot` | `footer` |
| Step number | see `numbered-item` | - | `n`, `cn` | `num`, `n` | `step-number` |

## Score rubric (this audit's own)
Single source of tokens 0/20 (four palettes, copies in three formats); token adoption 10/20 (decks 100 %, slides 0 %, others partial); type scale 8/20 (slides yes, decks and portfolio no); components named and documented 4/20; accessibility 14/20 (contrast passes, meaning paired with words in the spec, reduced motion partial, slide fragments carry no title of their own). Total 36/100.

## Priority actions
1. Decide the canonical lesson-1 version and the one course palette (owner decision; resolves issues 1 and 2).
2. One tokens file for colours (with the red pair), type scale and radius, read by the decks, slides, mockup and the cheatsheet builder (issues 3, 4, 6, 7).
3. Write the component inventory above into the colours spec (or a sibling spec) and use those names for new work (issue 5).
4. Small fixes: record the red contrast in spec section 5, update the gallery README, reduced-motion check for the slide viewer (issues 7, 2, 8).

## Applied 2026-10-23 (the owner chose A, Paper/Amber, and asked to fix all 9 actions)

| # | What was done | Checked |
|---|---|---|
| 1 | Slate lesson 1 v0.1 (`slides/`, `deck.json`) moved to `01-the-map/_archive-v0.1/` with a SUPERSEDED note; lesson and lessons READMEs point to `lesson-01-a/b.html`; the hosted deck is marked as the old version | references searched with `git grep` |
| 2 | Colours spec records the decision; gallery recoloured from "Maple" to the palette (its one text use of the accent became `--amber-text`); gallery README updated | `check_tokens.py`: no colour outside the palette |
| 3 | Red pair in the palette and contrast table (7.8:1 on paper, 6.5:1 on its tint) | computed, WCAG 2 formula |
| 4 | `_design/tokens.json` + `tokens.css`; decks carry every token; the cheatsheet builder reads the JSON; `check_tokens.py` checks decks, mockup, gallery, builder and the CSS copy | check clean; a deliberately broken copy fails; builder palette values identical (the full build was not run here: PyMuPDF and macOS fonts absent) |
| 5 | Type scale of 12 steps (24-128 px); 27 deck sizes rounded down by at most 4 px (22 up to 24); the control bar and notes panel keep their own sizes. The first try (8 steps, nearest size) made a title wrap on B6, so the rule became "round down" | screenshots of all 23 slides before and after, compared by pixel difference and by eye: no overflow, no new wrap |
| 6 | Radius tokens `--r-s` 6, `--r-m` 16, `--r-l` 20, `--r-pill`; circles and the decorative leaf unchanged | same screenshots |
| 7 | Classes `kick`, `lab`, `ccard` renamed to `eyebrow`, `card-label`, `card` in the four lesson-1 files; the mockup keeps its names until it is next edited | the deck script does not use these names (searched) |
| 8 | `portfolio/README.md` says the portfolio is outside the course design system | - |
| 9 | Status classes for mermaid defined in `_design/README.md` and applied to the three nodes that carry a status word (07 OPTIONAL: `off`; 09 evals NOT RUN: `draft`) | rendered with mermaid-cli 11.4.0; GitHub's renderer NOT TESTED |

Also fixed while checking: the mockup's terminal illustration used four colours outside the palette; it now uses `--ink` with `--green-tint`, `--amber-tint` and `--card` text (contrast 12.9 to 15.8:1). The `-lecturer` files got the same CSS changes and were not screenshot-compared separately.
Where the rules for future lessons live: `_design/README.md`, `_specs/2026-10-14-colors-design.md` section 6, `../COURSE-WORKING-RULES.md` section 2, `README.md` of the lessons folder, `../README.md`.
