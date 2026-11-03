# Runs

One `QA-RUN.md` journal per run (template: `QA-RUN.template.md`), in its own folder with
evidence. Everything in `runs/` except this file and the template is git-ignored because it
may hold client data. The journal is checked by `.claude/hooks/qa_run_check.py`.

## Kept evidence

The copies of the `.agents/` tree under `eval-kit/work/*/` are kept as evidence and are not deleted (QA Lead decision, 2026-11-03). They are git-ignored; remove them only by written decision of the QA Lead.
