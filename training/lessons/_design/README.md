# Course design system: how to make a lesson or a presentation

STATUS: DRAFT v0.1, 2026-10-23. Decided by the course owner on 2026-10-23: Paper/Amber is the one design for lessons and course presentations. Not approved by the AI QA Process Lead. Provenance: ai-generated (Claude Code, cloud session; model and version not recorded); human-confirmed: pending.

Files here:
- `tokens.json`: the source of truth (colours, fonts, type scale, radius, stage size).
- `tokens.css`: the same tokens as a `:root` block to paste into a deck.
- `check_tokens.py`: `python3 training/lessons/_design/check_tokens.py` checks that the decks, the mockup, the animation gallery and the cheatsheet builder match the tokens. Exit 1 = drift.

Why the colours are what they are, contrast and the meaning of colours: `../_specs/2026-10-14-colors-design.md`. The audit that led here: `../_specs/2026-10-23-design-system-audit.md`.

## The rules for every new lesson or course presentation

1. **One design.** Paper/Amber only. The Slate design (lesson 1 v0.1, `01-the-map/_archive-v0.1/`) and the "Maple" palette are retired. Personal documents in `portfolio/` are outside this system.
2. **Format.** One folder per lesson, two self-contained files: `lesson-NN-a.html` (Part A) and `lesson-NN-b.html` (Part B), about 20 minutes each, stage 1920x1080, IBM Plex Sans and Mono embedded so the file works offline. A presenter copy may be added as `-lecturer.html`. Start from `01-the-map/lesson-01-a.html`: it carries the stage, the controls, keyboard and touch navigation, the progress dashes and reduced-motion handling.
3. **Colours come from tokens.** Paste `tokens.css` into the deck's `:root`. Use `var(--name)`; no hex value outside `:root`. Allowed colours: `--paper`, `--card`, `--band`, `--ground`, `--ink`, `--muted`, `--amber`, `--amber-text`, `--amber-tint`, `--forest`, `--leaf`, `--green-tint`, `--line`, `--red-text`, `--red-tint`.
4. **Text colour rules** (colours spec section 3): body text `--ink`, secondary `--muted`; `--amber` is a fill or a line, never text; text on an amber fill is `--ink`; amber text is `--amber-text`; prefer `--forest` for green text; red text is `--red-text`. A new text and background pair needs its contrast computed first (4.5:1 for normal text, 3:1 for text of 24 px bold or larger on the stage).
5. **Meaning of colours** (colours spec section 5), always paired with a word or a mark, never colour alone:

   | Signal | Meaning | Word that goes with it |
   |---|---|---|
   | green (`--green-tint` fill, `--leaf` line, `--forest` text) | in use, confirmed, passed | ALLOWED, PASS, in place |
   | amber (`--amber-tint` fill, `--amber` line, `--amber-text` text) | draft, not run, pending, attention | DRAFT, PENDING, not run |
   | red (`--red-tint` fill, `--red-text` text and line) | unverified, blocked, failed, hostile input | UNVERIFIED, FAIL, blocked |
   | dashed grey outline | not used | NOT USED |
   | plain (`--paper` or `--card`, `--line` border, `--ink` text) | structure only | - |
   | thick `--ink` outline | a human step or a gate | the step name |

   Amber is not a brand colour: do not use it for "the assistant" or for a term name.
6. **Type scale.** Use `var(--fs-*)` only:

   | Token | Size | Use |
   |---|---|---|
   | `--fs-label` | 24 px | eyebrow, card label, footer, counter, table header |
   | `--fs-small` | 28 px | chips, small notes |
   | `--fs-body-s` | 32 px | dense body, table rows, bands |
   | `--fs-card` | 36 px | text inside cards |
   | `--fs-body` | 40 px | body text |
   | `--fs-body-l` | 44 px | definitions, lead in two-column slides |
   | `--fs-lead` | 48 px | the one sentence a slide is about |
   | `--fs-stat` | 56 px | a big number or a short statement |
   | `--fs-title-s` | 76 px | long slide titles |
   | `--fs-title` | 88 px | slide titles |
   | `--fs-title-l` | 104 px | short titles, two-column titles |
   | `--fs-display` | 128 px | cover title |

   If a title does not fit, pick the next smaller title step; do not invent a size.
7. **Radius.** `--r-s` 6 px (marks, progress dashes), `--r-m` 16 px (bands, small boxes), `--r-l` 20 px (cards, tables, tiles), `--r-pill` (chips), `50%` for circles.
8. **Component names.** Use these class names: `eyebrow` (mono uppercase label above the title), `title`, `lead`, `card`, `card-label`, `chip` (with a status word), `numbered-item`, `step-number`, `footer`. Do not invent a second name for the same thing. Accepted names in the lesson 1 decks, kept until those decks are rebuilt: `foot` (= `footer`), `q` (= `numbered-item`), `n` (= `step-number`), `t` (the text inside a `numbered-item`). New lessons use the names above.
9. **Motion.** Effects come from `../_template/animations/` (A1-A10, B1-B8). Every slide reads correctly from its last frame (PDF shows only that); CSS animations stop under `prefers-reduced-motion`.
10. **Language and content.** Slide text is English; each slide carries the mini-map of the six slots (Model, Instructions, Tools, Guardrails, Memory, Proof); unverified claims are marked on the slide (`../../COURSE-WORKING-RULES.md`).

## Before you share a deck

1. `python3 training/lessons/_design/check_tokens.py` prints `clean`.
2. Screenshot every slide at 1920x1080 and look for overflow and for lines that wrap badly. With the pre-installed Chromium:
   `chrome --headless=new --hide-scrollbars --force-prefers-reduced-motion --window-size=1920,1080 --screenshot=s1.png "file:///<path>/lesson-NN-a.html#1"` (one call per slide number).
3. Any new colour pair has its contrast written down in the colours spec.
4. If the deck is published as an artifact, publish it from these files, and update the lesson README with the link.

## Changing a token

Change `tokens.json`, then `tokens.css` to the same value, then the `:root` of every deck (the check lists each one that still differs), then run the check and the screenshots again. A colour change also needs its contrast rows in the colours spec updated.

## Diagrams (mermaid)

Schemes in `docs/schemes/` use the default mermaid look. Where a node carries a status word, give it the matching class (labels are `--ink` because diagram text is small; the word stays on the node):

```text
classDef ok fill:#E4EDDD,stroke:#4E7A3A,color:#1E4A2E
classDef draft fill:#F6E3B8,stroke:#E0A030,color:#231F1A
classDef fail fill:#F3D9D1,stroke:#8A2A1A,color:#8A2A1A
classDef off fill:#F9F3E5,stroke:#4A4339,stroke-dasharray:4 3,color:#4A4339
classDef gate fill:#FFFBF0,stroke:#231F1A,stroke-width:3px,color:#231F1A
```

Used in `07-base-and-variants.md` (OPTIONAL nodes: `off`) and `09-mvp-implementation-plan.md` (evals NOT RUN: `draft`). Checked with mermaid-cli 11.4.0 on 2026-10-23; GitHub's own renderer NOT TESTED.
