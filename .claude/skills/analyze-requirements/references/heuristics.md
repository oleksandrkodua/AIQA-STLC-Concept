# Heuristics for vague, solution-shaped or unbounded requirements

Read this when the requirement gives you little to test: it is vague, it describes how instead
of what, it has no boundary, or the acceptance criteria are thin. Each heuristic turns a
fuzzy text into concrete questions. Use the ones that fit; running all of them on a clear
requirement adds noise.

Every question you produce goes to the person who owns the answer. You are not filling the
gap, you are pointing at it.

## 1. Remove the solution

**Use when** the text names a technology, a component or an implementation step.

Rewrite the requirement as "the system must <observable behavior>" with no technology words.
If you cannot, the need is missing and that is the finding. Example shape: "must use a queue"
becomes "messages are not lost if the service restarts".

**Why:** a requirement that prescribes an implementation gives testers nothing to check except
the implementation, and it breaks when the implementation changes for good reasons.

## 2. Specificity ladder

**Use when** the text says "users should be able to…" or leans on adjectives.

Climb: who exactly? doing what exactly? when exactly? under which conditions? with what
result? Stop where the text stops being concrete and ask from that rung. For each vague
acceptance criterion, ask for **one concrete example scenario** from the product owner. Do not
write it yourself: an example you invent becomes a requirement the moment someone nods at it.

## 3. The disappointing implementation

**Use when** the acceptance criteria look complete.

Describe an implementation that satisfies the text word for word and still leaves the user
unhappy. "The export contains all rows" is satisfied by a file that opens with garbled
characters, or one that silently stops at the first page. Each description you can produce
points at a criterion the text does not have yet.

**Why:** the letter of a requirement and its intent drift apart exactly where nobody looked.

## 4. Pre-mortem

**Use when** you need risks and edge cases and the text supplies none.

Imagine the feature shipped and caused a serious incident. Write down the most likely cause,
then the second most likely. Each one becomes a risk, an edge case to cover or a question
about behavior under failure.

## 5. Invalidation question

**Use when** the requirement reads as a solution to a problem that is never named.

Ask what problem this solves, for whom, and what fact would make the requirement wrong or
unnecessary. Direct it to the product owner as a question. It does not replace the requirement
as the authority for expected behavior: a requirement can be right about behavior and still
worth questioning about purpose.

## 6. Scope boundary

**Use when** the text trails off: "and so on", "etc.", "similar cases", "while we're at it".

Ask what is explicitly out of scope and what is deferred. An unset boundary means nobody can
say when testing is finished. Do not rank or cut scope yourself; that is a product decision.

## 7. Assumptions the text relies on

**Use when** the flow starts in the middle of a story.

List what the text takes for granted: the user is signed in, the data exists, a flag is on, a
particular locale or timezone applies, a previous step succeeded. Each item becomes a test
precondition or a question about what happens when it does not hold.

## Shapes worth recognizing quickly

- **Solution specification.** Describes implementation instead of need. Heuristic 1.
- **Premature precision.** Fine-grained detail for behavior nobody has validated yet. Tests
  written against it will churn, so flag low readiness for automation even when the text is
  otherwise clear.
- **Unbounded scope.** Grows by additions without a stated edge. Heuristic 6.
- **Borrowed feature.** Copied from another product with no account of why it exists here.
  Ask what problem it solves in this context.

## Attribution

These techniques are informed by public requirements-analysis material, chiefly the
`requirements-analysis` skill in jwynia/agent-skills (MIT). The wording here is our own, and
nothing is copied.
