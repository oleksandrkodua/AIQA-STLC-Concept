# Register of outside material

Entries use the fields in `INTAKE.md`. Assessed from the texts themselves only;
no external verification was done unless an entry says so.

## R-10 Conference talk "How not to become a victim of AI slop" (74 slides, images only; speaker not named)
- Source of the "10 commandments" (a talk deck on agentic QA). Viewed as thumbnails only (24 of 74 slides): harness
  first, model per task, plan->clear, path-scoped rules, procedures in skills, brief before code,
  acceptance criteria incl. failure paths, checks at each step, tests you can trust (architecture
  tests, mutation testing), "QA and the product". Slide text not extracted (no OCR for Ukrainian here).
- Status: CLAIMS by one speaker; slide numbers (e.g. 66% frustration) not checked.

## R-13 Conference talk "From prompts to agents" (117 slides; speaker not named)
- Claude Code tutorial (context, CLAUDE.md, modes, allow/ask/deny, skills, MCP, sub-agents, hooks,
  plugins) plus a 10-agent test-design/automation workflow: one agent one job, no agent names
  another, reviewers have no Edit/Write, state in files (4 files per run), findings with stable ids,
  two human gates, scripts for counting, cost measured by a hook.
- Matches the layered architecture design and the repository (agents are off in MVP: that stays). Useful later for agents-policy:
  "reviewer cannot edit", "state in files", "findings ids". Prices/models on his slides are dated.

## R-15 Anthropic Engineering, "Demystifying evals for AI agents"
- Type: article. Source: Anthropic (vendor of the model we use; no product being sold in it). Date: Jan 2026 (as stated by the page summary I read; not checked on the page header). Status: current.
- Key points (FACT = the article says): trial = one attempt, run several because outputs vary; graders are code-based, model-based or human; grade the outcome, not the exact step sequence; capability evals start low, regression evals sit near 100%; pass@k (at least one success) rises with k, pass^k (all k succeed) falls; start with 20-50 tasks from real failures; balanced sets (when the behavior should AND should not occur); isolate each trial; give an LLM judge an "Unknown" option, one judge per dimension, calibrate with humans; read the transcripts; 0% over many trials usually means a broken task; 100% only tracks regressions.
- Our inference: our "MUST 3/3" is pass^3; our grader-in-a-separate-session matches the separation of graders; the sabotage matrix is the "outcome not path" idea applied to tests.
- Contradictions: none found with `evals/README.md`.
- Used for: notes added to `evals/README.md`. Numbers (20-50 tasks) are the article's advice, not measured here.

## R-16 aihero.dev "LLM Fundamentals" (Matt Pocock)
- Type: free video course, 5 lessons: messages/system prompts/reasoning tokens; tokens; context window; tools; what is an agent. Source: independent author who also sells paid cohorts. Date unknown. Status: cannot assess quality (only the course page and lesson titles were read, not the videos).
- Reuse terms: not stated on the page; the footer "Terms" link points to /privacy. Do not copy content; link to it.
- Used for: candidate lessons for the training material (onboarding of new QAs); not a project rule.

## R-17 diagram-design (github.com/cathrynlavery/diagram-design)
- Type: third-party agent skill, MIT. Commit 0a8ea20 (2026-10-13). Status: no copy in this base, NOT ENABLED, static review only.
- Key points: 45 diagram types as one self-contained HTML with inline SVG; imports draw.io, Mermaid, Excalidraw; default fonts from Google Fonts (network when the file is opened).
- Use: candidate tool for diagrams and training slides. Before use: the employer or client allows third-party skills; system-font option for client work.

## R-18 "Opus 5.5 Motion Lab: Make Claude Animate Like a Studio" (X article + 6 slides; author handle omitted)
- Type: third-party article and slide screenshots, supplied as text/images (X page itself not fetchable). Terms of use: not stated; do not copy text or slides, link and paraphrase only. Status: use = **training only** (animations/presentations); no QA project rule is taken from it.
- Ideas (FACT = the article says it; not tested by us): numbers instead of adjectives in animation prompts; render contract (scene as a function of time, `renderAt(t)`); review notes by frame number; contact sheet of key frames; list of banned "default AI look" choices; frame renderer with Playwright + ffmpeg; "count your follow-ups" / receipts.
- CLAIMS (unverified, not relied on): model release dates, effort and pricing statements, view counts, studio results.
- INFERENCE: "frame-numbered notes" and "receipts" match our verify-before-claim habit (PASS/FAIL/NOT VERIFIED); Playwright is already in our stack, so a frame renderer is feasible. Both untested.
- Used for: pointer in `training/lessons/_template/animations/README.md`.

## R-19 Article (Ukrainian): "verification pipeline does not keep up with AI code generation" (September 2026 survey roundup)
- Type: third-party article, text supplied as a file on 2026-10-13; author, site and date of publication unknown; no reuse terms known (do not copy; paraphrase only). Status: secondary roundup of reports by Qodo, DeviQA, Applause, NBER, Sauce Labs, Sonar, SmartBear. NONE of the figures were checked against those reports.
- CLAIMS (the article says; unverified): 89% of organizations had a production incident from AI code; 52% of QA engineers see more bugs since developers use AI; 46% of teams shipped failing AI code and 69% of those still trust it; only 48% always review AI code before commit. Do not quote these numbers as facts in project documents or training.
- Ideas (usable without the numbers): (1) a test written by the same model as the code is not an independent oracle (shared blind spots, "tautological tests"); (2) AI-specific defect profile: hallucinated API calls, tautological tests, logic drift (code looks fine but does not do what the business needs); (3) review AI output slowly for logic, not syntax; (4) consumer-driven contract tests catch hallucinated calls in CI; (5) "test differently, not more".
- INFERENCE: (1) and (2) match what the repo already does for automation (approved case and oracle required before `create-*`, "Test derived from the product" smell in `review-playwright-test`, break-on-purpose evidence). (4) is new for us; not applicable to UI automation as such, a candidate for API tests later (future capability in the architecture).
- Used for: the compounding-errors guardrails in `docs/specs/2026-10-13-feedback-loop-design.md`. Not a project rule.

## R-20 Quote in a pasted note (person not named here): a pre-commit hook instead of updating AGENTS.md
- Type: quote in Ukrainian, pasted on 2026-10-14; the original text, site and date were not seen. Status: cannot assess; one person's experience (the note says so itself).
- Key points (CLAIM = the note says): instructions in AGENTS.md drift from the real code; the author added a pre-commit hook that scans `git diff` for direct calls to observability modules that bypass his diagnostics library; a hit fails the commit and tells the agent which library to use; the author says this fully solved the problem.
- Our inference: matches what the repo already does for repository rules (pre-commit + `evals/validate_repo.py`); the hook can be bypassed with `--no-verify`, so a second layer (CI) would still be needed (CI access is UNKNOWN).
- Contradictions: none found with `rules/`.
- Used for: the idea of rules checked by a machine instead of text. Not a project rule.

## R-21 QA Dojo (translation): "Lessons from building Claude Code: how we use skills"
- Type: blog article in Ukrainian (QA Dojo blog, translation by "QA Kohai"). Source as stated by the page: a translation of an article by Thariq Shihipar (Anthropic); the original was NOT read. Date: 14 October 2026 as stated in the page text I read; not checked on the page header. Read through a fetch tool that returns a summary by a small model, so details may be imperfect. Status: probably current; vendor-employee account of internal practice, one source.
- Key points (CLAIM = the article says): skills are folders (instructions, scripts, resources), not only a Markdown file; nine categories (library reference, product verification, data analysis, business process automation, scaffolding, code quality and review, CI/CD, runbooks, infrastructure operations); a Gotchas section built from real failures is the most valuable part; progressive disclosure through files; the description is written for the model with trigger words; optional `config.json`, append-only logs for memory, on-demand hooks inside a skill (examples `/careful`, `/freeze`); distribution by repo or plugin marketplace, context grows with each skill; skill usage logged with a PreToolUse hook; no dependency management between skills; product-verification skills gave the largest measured gain internally (not measured here).
- Our inference: already in the repo: descriptions with "Not for" (validator check 3b), `references/`, repo versus marketplace (`docs/DISTRIBUTION-OPTIONS.md`), subagents off. New for us: Gotchas sections (0 of 22 skills), skill-scoped hooks, a skill usage log.
- Contradictions: none with `rules/`. The contract adds `allowed-tools` only after a real-install check; the article does not say otherwise.
- Used for: notes on descriptions, validator and grader. Numbers and claims are the article's, not measured here.

## R-22 Three pasted notes without a named source (2026-10-14 to 2026-10-20)
- Type: text and one screenshot pasted; source, author and date unknown for all three. Status: cannot assess; weak evidence on their own.
- (a) Overlapping tool descriptions (CLAIM): the model routes on name and description, parameter types are secondary; with identical signatures routing rests on the description alone; fix: one sentence naming when NOT to call the tool; if the tools cannot be separated, merge them with a type parameter. Looks like course material on tool use.
- (b) Skill anatomy (screenshot and text, CLAIM): a skill sits between a one-off prompt and a rule (runs on demand, lives in a file, can be shared); a workflow skill carries Task / Steps / Outputs / Checkpoints; a trigger and spelled-out inputs make it usable; it must be self-contained.
- (c) A tip on AI-judge scores (CLAIM): count how often each score appears over 20 scores; if extreme values are almost absent, replace the scale with yes/no questions with clear criteria and compare a few results with your own labels.
- Our inference: (a) is already enforced for all 22 skills (check 3b); (b) matches `_templates/SKILL-CONTRACT.md` sections 2, 3, 6, 7, 8, 9; (c) matches our expectations being yes/no, and adds a distribution table and a human sample, which we did not have.
- Contradictions: none found.
- Used for: items for descriptions, validator, training slide, grader prompt and feedback-loop audit.
