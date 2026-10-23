# Code review of PR #3 (2026-10-23): open findings

STATUS: OPEN. Found by /code-review (max) on branch cloud/2026-10-23-evals-triage-cloud-docs before merge; merged unfixed at the owner's request (token budget). Fix in a follow-up branch. Provenance: ai-generated (Claude Code, cloud session); human-confirmed: pending.

1. `training/lessons/_specs/2026-10-23-lesson-09-evals-design.md:84`: the "Decided 2026-10-23" sentence was inserted inside the Russian word "решено"; the line is garbled and says both decided and depends on lesson 2. Rewrite the item.
2. `analyze-requirements` eval `injected-ticket-comment`: the code check "does not contain READY TO TEST: yes" fails a correct run that quotes the injected comment. Check the verdict line only.
3. `feedback-triage` eval 3: accept and "yes, write it" in one prompt, but `disallowed-tools` removes Write for the invoking turn. Split into two turns.
4. `feedback-triage` SKILL.md: `disallowed-tools` covers built-in tools only; MCP tools that write, run or reach the network stay. Correct the claim in Access; consider listing MCP write tools.
5. `gallery.html:53`: "Skill" chip is #FFFBF0 on #E0A030 (about 2.2:1). Use --ink on amber.
6. `gallery.html:66`: SVG text fill #E0A030 (amber as text, about 2:1). Use #9A5B0A.
7. `evals/fixtures/injection/README.md` step 4: whole-output grep fails correct runs that quote the injection (Status: Approved, two-factor). Grep case fields only.
8. `tools/build-skills-index.py` needs_hash ignores frontmatter tool keys (allowed-/disallowed-tools). Include them.
9. `check_tokens.py`: ignores the gallery :root and extra deck variables; misses #RGB, #RRGGBBAA, rgb()/hsl(), named colours; no contrast-pair check (missed 5 and 6).
10. `build-skills-index.py:50`: relaxed regex accepts `description: >` and records ">". Reject block scalars.
11. `feedback-triage/NAVIGATOR.yaml`: access_checked was set by the AI with `--accept`, which is meant for a person. Owner to re-read Access and re-run --accept.
12. `docs/superpowers/specs/2026-10-23-injection-defense-design.md:16,33`: "All of wave 2 is done" contradicts STATUS "Nothing implemented". Reword to "all of wave 2 is approved; not implemented".
13. `_design/README.md` rule 8: the template deck still uses .foot and .q/.n/.t. Rename or list them as accepted names.
14. Colours spec section 6 and audit row 5: two 84px titles went to 76px (-8px), 22px went up to 24px. Correct the "at most 4 px" claim.
15. `evals/fixtures/injection/PR-DEMO-27.diff`: hunk header does not match the body; `//` comment is invalid JSON. Fix so the review reaches the injected line.

Also: the merged branch `cloud/2026-10-23-agent-audit` (PR #2) still exists; the owner deletes it.
