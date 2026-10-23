# Checkpoint Format

Checkpoints are written to `$RESULTS_DIR/CHECKPOINTS.md` by each step-executor subagent.

---

## File Structure

```markdown
# Test Checkpoints
**URL**: <url>
**Started**: <ISO timestamp>
**Results Dir**: <path>

---

| Step | Description | Status | Observation | Screenshot |
|------|-------------|--------|-------------|------------|
| 1 | Navigate to https://myapp.com | PASS | Page loaded, title "MyApp", HTTP 200 | screenshots/step-1-after.png |
| 2 | Verify navigation bar | PASS | Nav visible with 4 links | screenshots/step-2-after.png |
| 3 | Click Login link | FAIL | Link not found in nav — nav renders as hamburger menu | screenshots/step-3-after.png |
| 4 | Fill email field | BLOCKED | Could not proceed, login page not reached in step 3 | — |
```

---

## Status Values

| Status | Meaning |
|--------|---------|
| `PASS` | Actual outcome matched expected outcome |
| `FAIL` | Actual outcome did NOT match expected outcome |
| `BLOCKED` | Step could not be attempted (prerequisite step failed or app in unexpected state) |
| `SKIPPED` | Step was skipped by the orchestrator (e.g. depends on a BLOCKED step) |

---

## Observation Rules

- Maximum 20 words
- Describes what actually happened (not what was expected)
- For FAIL: include what was found vs what was expected
- For BLOCKED: state which prerequisite was missing
- For PASS: brief confirmation of the outcome

---

## Screenshot Column

- Path is relative to `$RESULTS_DIR`
- Use `—` if no screenshot was captured (e.g. BLOCKED steps)
- Always use the "after" screenshot as the primary evidence
- "Before" screenshots are saved but not listed in CHECKPOINTS.md (they exist in the screenshots/ dir)

---

## Appending Rows

The step-executor subagent appends exactly one row per execution. It must:
1. Check if the header row exists — write it if not
2. Append the new row at the end of the table
3. Never modify existing rows

The header row (written once, only if file is new or empty):
```
| Step | Description | Status | Observation | Screenshot |
|------|-------------|--------|-------------|------------|
```
