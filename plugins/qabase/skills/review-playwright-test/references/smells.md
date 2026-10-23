# Smells in Playwright tests

Read this for any diff bigger than a few lines, or when the code came from an AI. A smell is
a symptom, not a verdict: context decides whether it is harmful. A long test for a complex
flow can be right. When you are unsure, raise it as a question.

Every finding you write says what is wrong, why it matters and what to do instead. "This test
is bad" is not a finding.

## Reliability

| Smell | What it looks like | Ask for |
|---|---|---|
| Fixed wait | `waitForTimeout`, `sleep`, a `setTimeout` used to synchronize | Reject. An explicit wait for the condition, or a web-first assertion |
| Order dependence | passes in the full run, fails alone or in another order | each test creates its own preconditions |
| Shared state | tests read data another test wrote, or leave data behind | isolated data, setup and teardown inside the test |
| Real external service | the test calls a payment provider, an email service or another third party | a stub at that boundary, or move the check to a test built for it |
| Retry hiding a race | retries or loops added until it passes | find the race; do not mask it |

## Diagnostic value

| Smell | What it looks like | Ask for |
|---|---|---|
| Weak assertion | `toBeTruthy`, `toBeDefined`, a bare boolean, "element exists" for a behavior check | an assertion on the actual value or text, so a failure names what was wrong |
| Several reasons to fail | one test walks a whole lifecycle | split it, one behavior per test |
| Failure needs the source | a failure message that says nothing without reading the code | more specific assertions or a short message |

## Design

| Smell | What it looks like | Ask for |
|---|---|---|
| Logic in the test | `if`, `switch` or loops in the test body | a data table, or separate tests |
| Oversized fixture | a huge setup for a small check | setup proportional to what the test needs |
| Over-mocking | everything is stubbed, including things the case is about | stub only what is outside the case |
| Unclear setup | setup that hides what the test depends on | minimal, visible setup |

## Stubbing the thing you claim to verify

The most damaging form of over-mocking, and easy to miss in a Playwright test: a
`page.route(...)` that fulfills the very API call whose result the test then asserts. The
test passes whatever the real service does. Compare each stubbed route with the case: if the
case is about that behavior, it must not be stubbed.

## AI-generated

| Smell | How to spot it | Ask for |
|---|---|---|
| Invented locator | run the test against a real page once; the selector never matches | a locator checked against the page |
| Invented import or helper | the type-check fails, or the symbol is not exported | the type-check result in the PR |
| Placeholder data | `test@test.com`, `John Doe`, `Lorem ipsum`, `password123` | the project's data factory or plausible varied data |
| Test derived from the product | expected values equal whatever the page displays, and nothing in the approved case supplies them | compare each expected value with the case's oracle; ask where it came from |
| Style drift | naming, page objects or fixtures unlike the rest of the suite | follow the local conventions |

Why the fourth one matters: when code and its expectations come from the same source, the test
only describes the product. It cannot catch a wrong behavior, because it was written to match
it. The approved case is the independent source that breaks this loop.

## Coverage

| Smell | What it looks like | Ask for |
|---|---|---|
| Happy path only | every test gives valid input and expects success | the negative and boundary cases from the case, or a note of what is uncovered |
| Missing boundaries | normal values tested, not zero, one, the limit and one past it | data-driven cases at the boundaries |
| Missing failure | no test for what happens when something goes wrong | the failure mode for each happy path |
| Weakened assertion | an existing assertion loosened, for example an exact text changed to a partial match | say it explicitly and ask why |

## Evidence the author should have shown

- type-check result (`npx tsc --noEmit` from `./playwright`);
- a repeated run (`npx playwright test --repeat-each=3 <file>`);
- the test failing after being broken on purpose, for the intended reason;
- for a defect fix, the test failing against the unfixed behavior.

If any of these is missing, list it under NOT CHECKED. A review cannot vouch for what it has
not seen.

## Attribution

The smell buckets and the AI-generated smells are informed by the `ai-qa-review` skill in
petrkindlmann/qa-skills (MIT) and by `test-blindspots` (Neeeophytee, MIT). The wording here is
our own, and nothing is copied.
