# Lesson 1 presenter notes (DRAFT v0.2, 2026-10-08)

Not part of the decks: the decks are for viewing only, so the answers stay here.

## Part A (10 slides, ~20 min)
- Slide 3 "Ask the room": answers. 1) No: a chat that only answers is an assistant; an agent repeats plan, act, check on its own and changes things. 2) No: long sessions can degrade; conference material calls it context rot (a speaker claim, not verified by us; Lesson 3). 3) No: a prompt rule is a request to a non-deterministic model; hooks and permissions exist because of this (Lesson 8). Do not reveal answers now; take votes and move on. They come back on Part B slide 12.
- Slide 10 "Pause": match key: 1-D (LLM), 2-F (Token), 3-B (Context), 4-E (Assistant), 5-A (Agent), 6-C (Subagent).
- Slide 5 (LLM): the model sounds equally sure when it is right and when it is wrong; this is why the course is about checking, not trusting.
- Slide 6 (Token and Context): do not quote prices, they change. The "quality drops as the window fills" claim comes from conference material and a Chroma page on context rot; we have not measured it. Lesson 3 shows how to look at your own session.
- Slide 7 (Assistant): tools allowed on the project (assumption): Claude Desktop, CLI, VS Code plugin. Not used: claude.ai (web) and the Chrome plugin. No written source yet (open question); demos use public data only until confirmed.
- Slide 9 (Subagent): the heavy reading happens in its own window, so your main window stays clean; cost: you only get a summary back, and a summary can miss something. Lesson 7 covers when to use it.

## Part B (13 slides, ~20 min; trim candidates: merge Rules into CLAUDE.md, or drop slide 2 when A and B are the same day)
- Slide 3 (CLAUDE.md): test for a good line: would a new colleague be slower or make a mistake without it? If not, delete it. AGENTS.md is the term we are least sure about; check how each tool really reads it before relying on it (Lesson 5).
- Slide 7 (Hook): a prompt rule is a request; a hook is code that runs regardless of what the model decides. Our hooks are drafts: until the firing tests run, we teach how it will work, not how it works.
- Slide 8 (Permissions): both permissions and hooks are drafts until the course owner and the client approve them; changing them is a trusted-asset change that needs approval.
- Slide 9 (Eval): results are PASS, FAIL or INCONCLUSIVE; a case we could not run is NOT VERIFIED, never a pass. The repo validator that passes today checks file structure, not whether the AI behaves well; say this out loud.
- Slide 10 (MCP and Plugin): MCP versus command-line tools is disputed (open conflict C-1); conference material argues for MCP on safety grounds, other material for CLI on cost; we take no side. Mods: install commands and version requirements come from conference material and were not verified.
- Slide 11 (Map): walk the table top to bottom and point at the real folders in a file browser. It doubles as the homework answer key. Refresh statuses before every delivery; the course must not present a draft as a working system.
- Slide 12 (Mistakes): return to the three votes from Part A; ask who changed their mind. The second half of card 3 is design intent while hooks are drafts.
- Slide 13 (Homework): check needs no expertise: list the folder in a file browser or terminal and compare paths with the map slide. Next lesson: where you work (Claude Desktop, CLI, VS Code). Further reading: konasense.com/blog/what-is-a-token-in-ai and trychroma.com/research/context-rot.

## Not verified
Runtime behaviour on the client's machines and versions; speaker claims (context rot, mods, AGENTS.md); keyboard and fullscreen inside the hosted artifact frame (works in plain Chromium).
