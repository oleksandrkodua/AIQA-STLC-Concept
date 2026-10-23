# Project context: <name>

Pattern from an earlier QA agent setup. One file per project/area,
loaded on demand, updated at the end of a run with a short write-back that a human reviews.

## Facts (each with source and date)
- <fact> — <source> — <date> — VERIFIED FACT | OBSERVATION

## Known gotchas (things that cost time before)
- <gotcha> — <how found> — <date>

## Stable vs changing
- Stable: <...>   Changes often: <...>  (findings in changing areas have a short shelf life;
  re-read the build fingerprint before repeating anything)

## Open questions
- <question> — <who>

## Write-back log
| Date | Run | What was added | Reviewed by |
|---|---|---|---|

Pruning: at each review, remove facts no longer true; do not let the file grow without limit.
