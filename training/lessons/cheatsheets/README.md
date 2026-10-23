# Cheat sheets

STATUS: DRAFT v0.1, 2026-10-14. Nothing here is approved.

The series is 6 sheets (the subtitles say "of 6"), English. Plan and rules: `_specs/2026-10-14-language-cheatsheets-design.md` (DRAFT, not approved).

| Sheet | Pages | Files | Status |
|---|---|---|---|
| 1. Terms, commands, rules (general) | 2 | `cheatsheet-1-terms-p1/p2` (.svg .png), `cheatsheet-1-terms.pdf` | BUILT, draft |
| 2. Project (PLACEHOLDER, fill in when setup is finished) | 1 | `cheatsheet-2-project` (.svg .png .pdf) | BUILT, placeholder |
| 3. TypeScript for QA | 1 | `cheatsheet-3-typescript` (.svg .png .pdf) | PLANNED, not built |
| 4. Playwright | 1 | `cheatsheet-4-playwright` (.svg .png .pdf) | PLANNED, not built |
| 5. WebdriverIO + Appium (mobile) | 1 | `cheatsheet-5-wdio-appium` (.svg .png .pdf) | PLANNED, not built |
| 6. Python for QA scripts | 1 | `cheatsheet-6-python` (.svg .png .pdf) | PLANNED, not built |
| Booklet: cover + sheets 1-6 (8 pages, bookmarks, for screen and a shared link) | 8 | `booklet.pdf` | PLANNED, not built |

Rows marked PLANNED do not exist yet; the files named there are the intended names from the spec.

## Edit
- Text and tables: edit the lists at the top of `build_cheatsheets.py` (LAYERS, GLOSSARY, CMD_*, LABELS, NEVER, REPO, CHAIN, BLANKS, PROJ_RULES), then run `python3 build_cheatsheets.py`. It rewrites every .svg, .png and .pdf.
- Layout: open the .svg in Figma, Inkscape or a text editor. A hand edit of an .svg is lost on the next build.
- Needs PyMuPDF and Pillow. Fonts are measured with Arial and Courier New from macOS.

## Known limits
- The dashed outline for NOT USED is drawn as a solid line in the .png and .pdf (PyMuPDF limitation); it is dashed in a browser, Figma and Inkscape.
- General slash commands (/model, /resume, ...) come from general Claude Code knowledge and are NOT checked on client versions. The tick boxes are for the author.
- The red colour pair is provisional (see `_specs/2026-10-14-colors-design.md`, section 5).
