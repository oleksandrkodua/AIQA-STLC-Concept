# What is usually forgotten, and how to state a result

Read this when the requirement involves input, several actors, state changes or external
systems. It has three parts: prompts for edge cases, the shape of an expected result, and
data hygiene. Use the prompts that fit the requirement; a checklist run mechanically on every
story produces cases nobody needs.

Every value you put in a case must come from the requirement or be flagged as an assumption.
The prompts tell you where to look, not what the answer is.

## 1. Edge-case prompts

Go through these for each behavior that takes input or changes state.

| Prompt | Ask |
|---|---|
| **Boundaries** | minimum, maximum, zero, negative, one past the limit, overflow |
| **Order and repetition** | sorted, reversed, duplicates, an item already processed, the same request twice |
| **Text and encoding** | accents, emoji, right-to-left scripts, multibyte characters, very long strings, special characters, text that grows when translated (truncation, overflow, wrapping) |
| **Empty** | null, empty, whitespace only, field skipped |
| **Volume** | zero items, one, many, exactly at capacity |
| **Access** | not signed in, session expired, wrong role, someone else's data |
| **Concurrency** | double submit, two users on the same record, a stale page acting on changed data |
| **Failure of dependencies** | timeout, error response, partial success, malformed reply |
| **Environment** | timezone, daylight-saving change, locale, screen size, browser, day boundaries (00:00 versus 24:00, a range that crosses midnight, ambiguous time notation) |
| **State** | every valid move, invalid moves, re-entering a state, leaving halfway |

Two extras when the product requires them: **accessibility** (keyboard only, screen reader,
contrast) and **recovery** (what state remains after a failure, and can the user retry).

**What a script cannot judge.** A case can be technically right and still miss what confuses a
real person: midnight written as 00:00 is correct, and people still cannot tell which night it
means. For behavior like that, say in the case that a person should try it, not only a script,
because the product is used by people.

## 2. Stating an expected result

A single check rarely proves a behavior. For each case, ask what applies of these four, and
write only those:

- **Sees**: what the user observes. Exact text, value or state, not "a message appears".
- **Stored**: what is persisted afterwards, if the behavior changes data.
- **Must not**: what must not happen. No error, no duplicate record, no navigation away, no
  charge. This is the check people forget, and it is where regressions hide.
- **Side effect**: an email sent, an event recorded, a call to an external system.

Prefer business outcomes over mechanics. "The order total is 29.99" is a result; "the
total field is populated" is not.

An invariant is stated once and checked wherever it can break: "a quantity is never
negative", "a total equals the sum of its lines plus tax and shipping", "a user sees only
their own orders". Give each its own case, and consider whether it also belongs in the
"Must not" line of other cases.

## 3. Test data

- Realistic and varied: several names and formats, not one placeholder repeated.
- Email addresses on a reserved example domain, never on a real one.
- A value at a limit is taken from the stated limit. If the limit is not stated, that is a
  question for the requirement, not a number to pick.
- Cases that differ only by data are one case with a data table.
- No real customer data, no production copies, no credentials.

## 4. An illustration of the matrix

Illustration only. It is generic and belongs to no project.

| # | Criterion / invariant | Behavior | Category | Priority | Oracle (source) | Cases |
|---|---|---|---|---|---|---|
| 1 | AC-1 one code per order | apply a valid code | positive | High | approved AC-1 | 1 |
| 2 | AC-1 | apply a second code | negative | High | approved AC-1 | 2 |
| 3 | AC-2 expired code rejected | apply an expired code | negative | Medium | approved AC-2 | 3 |
| 4 | INV-1 total never below zero | discount larger than the subtotal | boundary | High | approved rule INV-1 | 4 |
| 5 | AC-1 | apply the same code from two sessions at once | concurrency | Medium | **unknown, ask** | — |

Row 5 shows the useful behavior of the matrix: a row with no oracle is visible before a case
exists, and it goes back as a question instead of becoming an invented expectation.

## Attribution

The edge-case prompts are informed by the BOUNDARIES checklist and the oracle categories in
the `ai-test-generation` skill of petrkindlmann/qa-skills (MIT). The wording here is our own,
and nothing is copied.
