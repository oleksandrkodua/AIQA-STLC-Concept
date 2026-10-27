# Colors for training presentations: specification (DRAFT)

Status: DRAFT v0.2, 2026-10-23. Not approved. Approver: the AI QA Process Lead.
Decision (the author, 2026-10-23): this Paper/Amber palette is the course palette. The Slate design of lesson 1 v0.1 is archived (`01-the-map/_archive-v0.1/`) and the animation gallery is recoloured to this palette. Values live in `../_design/tokens.css` and `../_design/tokens.json`; this spec explains them. Audit: `2026-10-23-design-system-audit.md`.
Source: the `:root` variables of `training/lessons/01-the-map/lesson-01-a.html` and `lesson-01-b.html` (same values in both). Contrast ratios were computed on 2026-10-14 with the WCAG 2 relative-luminance formula; they were not checked in a rendering tool. How the existing slides actually use each color was NOT audited: the "Role" column is an inference from the variable names.

## 1. Palette (lesson 1)

| Variable | Value | Role (inference) |
|---|---|---|
| `--paper` | `#F9F3E5` | slide background |
| `--card` | `#FFFBF0` | card background |
| `--band` | `#F1E7CF` | bands and blocks |
| `--ground` | `#E6DABB` | page background around the 1920x1080 stage |
| `--ink` | `#231F1A` | main text |
| `--muted` | `#4A4339` | secondary text |
| `--amber` | `#E0A030` | accent fill |
| `--amber-text` | `#9A5B0A` | accent text |
| `--amber-tint` | `#F6E3B8` | accent background |
| `--forest` | `#1E4A2E` | second accent: text and fills |
| `--leaf` | `#4E7A3A` | second accent: lighter fills |
| `--green-tint` | `#E4EDDD` | second accent background |
| `--line` | `#D9CDB0` | rules and borders |
| `--red-text` | `#8A2A1A` | status red: text and lines (added 2026-10-23, from the mockups) |
| `--red-tint` | `#F3D9D1` | status red: background (added 2026-10-23) |

Fonts: IBM Plex Sans (text), IBM Plex Mono (code, chips), embedded in the file. Stage 1920x1080.

## 2. Contrast (computed)

| Pair | Ratio |
|---|---|
| `--ink` on `--paper` | 14.8 |
| `--muted` on `--paper` | 8.8 |
| `--forest` on `--green-tint` | 8.4 |
| `--ink` on `--amber` | 7.2 |
| `--amber-text` on `--paper` | 4.9 |
| `--leaf` on `--paper` | 4.6 |
| `--amber-text` on `--amber-tint` | 4.3 |
| `--amber` on `--paper` | 2.1 |
| `--line` on `--paper` | 1.4 |
| `--red-text` on `--paper` | 7.8 (computed 2026-10-23) |
| `--red-text` on `--red-tint` | 6.5 (computed 2026-10-23) |

## 3. Rules (PROPOSAL)

1. `--amber` is a fill and an accent line only. Never use it as text color on `--paper`, `--card` or `--band` (2.1:1).
2. Amber text uses `--amber-text`. On `--amber-tint` it is 4.3:1: allowed for large text (24 px or bigger on the 1920 stage), not for small captions.
3. Text on an `--amber` fill is `--ink` (7.2:1), never white.
4. Body text is `--ink`; secondary text is `--muted`. No other text colors for body copy.
5. `--leaf` text on `--paper` is 4.6:1: allowed, but prefer `--forest` for text and keep `--leaf` for fills.
6. `--line` is decoration. Meaning is never carried by a line color alone.
7. Meaning is never carried by color alone: pair amber or green with a word, a mark or a shape (the lessons already use mono chips).
8. Dark and light variants: none defined. UNKNOWN whether projectors or screen sharing need one.

## 4. Open points

- RESOLVED 2026-10-23: the gallery's "Maple" palette was replaced by this palette (see its README).
- What amber and green mean in the slides (for example amber = caution, green = ok) is not written anywhere; decide before assigning meaning.
- Whether rules 2 and 5 are applied correctly in the existing slides is NOT checked.

## 5. Meaning of colours (PROPOSAL, added 2026-10-14)

Answers the second open point above. Applied in `training/lessons/_mockups/diagrams-mockup.html`. Existing sections 1-4 are unchanged.

| Signal | Meaning | Always paired with |
|---|---|---|
| Green (`--green-tint` fill, `--leaf` line, `--forest` text) | in use, confirmed, passed | a word (ALLOWED, PASS, MATCHED) or a check mark |
| Amber (`--amber-tint` fill, `--amber` line, `--amber-text` text) | draft, not run, pending, needs attention | a word (DRAFT, PENDING, INCONCLUSIVE) |
| Red (tint, line and text) | unverified, blocked, failed, hostile input | a word (UNVERIFIED, FAIL, blocked) or a cross mark |
| Dashed grey outline | not used | the words NOT USED |
| Plain (`--bg` fill, `--line` border, `--ink` text) | structure only, no status | nothing |
| Thick `--ink` outline | a human step or gate | the step name |

- Amber is not a brand or role colour: do not use it for "the assistant" or for a term name. In the mockups that was fixed on lessons 1, 4, 6, 10, 12 and bonus B.
- Red is in the palette since 2026-10-23 (section 1): `--red-text` `#8A2A1A`, `--red-tint` `#F3D9D1`, contrast 7.8:1 on `--paper` and 6.5:1 on its tint (section 2, WCAG 2 formula, not a rendering tool). The mockup's dark-mode pair (`#F0A898` on `#3A1F19`) is not part of the palette: there is no dark variant (rule 8).
- Approver: the AI QA Process Lead. Not approved.

## 6. Beyond colour (added 2026-10-23)

- Tokens: `../_design/tokens.json` is the source of truth (colours of section 1, fonts, type scale, radius, stage 1920x1080); `tokens.css` is its `:root`; `check_tokens.py` fails on drift.
- Type scale (12 steps): 24, 28, 32, 36, 40, 44, 48, 56, 76, 88, 104, 128 px as `--fs-label` ... `--fs-display`. Lesson 1 was moved onto it by rounding every size down by at most 4 px, with two exceptions: two 84 px titles went to 76 px (-8 px) and 22 px went up to 24 px (+2 px), so only that one size grows and no title wraps; checked by screenshots of all 23 slides before and after.
- Radius: `--r-s` 6 px, `--r-m` 16 px, `--r-l` 20 px, `--r-pill`; circles stay `50%`.
- Component names: `eyebrow`, `title`, `lead`, `card`, `card-label`, `chip`, `numbered-item`, `step-number`, `footer` (lesson 1: `kick` became `eyebrow`, `lab` became `card-label`, `ccard` became `card`).
- Diagrams (mermaid): the status classes `ok`, `draft`, `fail`, `off`, `gate` in `../_design/README.md` use these colours with `--ink` labels (small text), always next to the status word.
- How to build a new lesson or presentation: `../_design/README.md`.

Provenance: ai-generated, Sonnet 5.5, 2026-10-14; sections 1, 2, 4, 5 updated and section 6 added 2026-10-23 in a cloud session (ai-generated); human-confirmed: pending.
