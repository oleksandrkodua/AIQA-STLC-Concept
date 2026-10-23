# Token counting per skill session — design

> Note on this copy. Taken from an earlier architecture project; the body is unchanged. Design only, nothing implemented or run. "§" and V-numbers point to that project's architecture document and verification log (not included in this base).

Date: 2026-09-30. Status: **principle and plan only. Nothing is implemented**, and the method
has not been run.

## Principle

A token count is taken from a record the harness itself wrote, by code, not from the model and
not from a character count. A number that cannot be read reliably is left empty. It is never
estimated, because an estimate that looks like a measurement is worse than a gap.

## What it is for

- the `tokens` field of the session tally (architecture §43);
- the cost comparison of modes in V33 (agent per action, agent two-tier, committed test);
- later, one input to estimating new tickets from past ones (last section but one);
- the AI effectiveness and cost metrics, once a baseline exists.

## Decision

1. **Primary method: a small utility reads the local session transcript.** It is run by a
   person at the end of a measured session. It sums the usage found in the transcript, adds the
   subagents' files, and appends one row to a log file.
2. **OpenTelemetry is not assumed.** Whether the client allows exporting usage data, through a
   collector, and whether managed settings would override it, is a Discovery question
   (environment checklist item 10, V34). If it is allowed, it becomes a second source to
   cross-check the first.
3. **Fallback: a person copies the number from the harness's usage screen.** Slower and
   error-prone, and the row says it was entered by hand.
4. **Rejected:** asking the model (§21A); character counts presented as a measurement (allowed
   only when labelled as a proxy).

## What is known, and how well

All from third-party sources except the OpenTelemetry item. None of it has been run here
(verification-log V31, V30).

- A hook receives `session_id` and `transcript_path`, and **not** the token usage.
- The transcript is a JSONL file with usage on each assistant message.
- Usage is **repeated for each content block** of a message, so a naive sum counts it several
  times. It must be de-duplicated by the message or request identifier.
- Subagent usage is written to **separate files**, not into the main transcript.
- A Stop hook can fire before the last line has been written, so a read may need a short,
  bounded retry.
- The transcript holds tokens, not money.
- Claude Code's own documentation describes built-in OpenTelemetry export of token usage by
  type, cost and per-request events. It needs a collector, and on machines with managed
  settings developer-set endpoints may be removed at startup.

## Data flow

1. The person finishes a skill run and records a decision for every case: KEEP, MODIFY,
   REJECT or DEFER.
2. The person runs the utility. It asks two things: minutes spent reviewing, and a quality
   rating.
3. It locates the transcript of the current session and sums the tokens by type (input,
   output, cache read, cache creation), once per unique message, plus the subagent files.
4. It shows the finished row and asks for confirmation.
5. It appends the row to `feedback/tally/<person>.jsonl`. Each person has their own file, so
   three or four people do not create merge conflicts in one.

The row holds identifiers and numbers only: schema version, date, session id, skills used,
story id or local label, model, effort (may be empty), counts, decisions, minutes, rating,
tokens by type, and the source of the tokens. **No requirement text, prompt, page content or
client data is ever copied out of the transcript.** The price is not stored; it is computed
later from a dated price table, because prices change.

One session gives one row. For a measured run, use one session per skill. If a session used
several skills, the row lists them and the tokens are shared.

## Components

One utility with no dependencies, written in Node.js. Node is already required by the
environment checklist for Playwright; Python may not be present on a client laptop. It runs
locally with no network access.

## Errors

The utility fails loudly. If the transcript cannot be read, is cut off, has an unknown shape,
or no usage is found, it exits with an error and writes nothing. A row with `tokens: null` and
a stated reason is written only when the person asks for it explicitly. A session that already
has a row is refused unless the person says to replace it.

## Checking the counter

1. **Synthetic files** with results worked out by hand: usage repeated across blocks, a
   subagent file, a cut-off last line, a missing usage field, an empty file.
2. **Reconciliation** on three real short sessions against an independent source (the
   provider's usage screen, or OpenTelemetry if it exists). The tolerance is chosen before the
   comparison; 2% is proposed.
3. **Format drift guard.** The utility checks that the fields it relies on are present. After
   a Claude Code update, one short run shows whether the format changed, and it breaks at once
   instead of quietly reporting wrong numbers.

## Same input, more outputs: a session reader

The session transcript is also a record of every tool call and its result. The same reader that
sums tokens can report, after the session: the same call failing repeatedly with no change of
approach; whether the last edit was followed by a type-check or a test run; and whether each
command a claim cites exists and what status it ended with. These are advisory and run after the
fact, so they need no live hook and no early-access interface (architecture §19, "Controlling the
AI's own claims"). They read the same format that has not yet been verified (V31), so the same
fixtures and the format guard apply to them.

## Later: estimating from past tickets (an idea, not started)

The idea, from the project owner: feed the record of finished tickets to the model - how much
time went on each activity, four or five complexity metrics for the ticket, and the tokens
spent. As the record grows, use it to estimate new tickets from similar past ones, in time and
in tokens.

**Principle.** The model does not learn between sessions. The "base" is a dataset we keep, and
the estimate is computed from it.

- The numbers come from code, for example the distribution of time and tokens among the most
  similar past tickets. The model's job is to find similar tickets, show them and explain. A
  figure the model produces from memory is not an estimate.
- An estimate is a range, with the tickets it rests on listed and the sample size stated. Below
  a minimum sample it says there is not enough data. A number is never shown without these.
- It is a forecast for planning, not a target, and never a measure of a person. The estimating
  dataset holds ticket totals and no individual attribution.

**What a record would need.** The metrics are not chosen yet; this is a starting list to be
decided and defined before anything is collected.

- ticket id or local label;
- complexity metrics, each with a written scoring rule so two people score the same ticket the
  same way. Candidates: number of acceptance criteria, number of affected areas, number of roles
  or states, new behavior versus a change, number of integrations or data dependencies;
- time by activity: analysis, case design, automation, review, execution and defect handling;
- tokens by type, with the model and effort they were spent on, because both change the number;
- outcome: defects found, and how many cases were kept, modified or rejected.

**Conditions for trusting it.**

- metrics are scored consistently, and time is recorded the same way by everyone. Self-reported
  time is noisy;
- enough tickets of each kind, dozens rather than a handful. The threshold is decided before
  use;
- it is tested like any other AI output: hold back the most recent tickets, estimate them,
  compare with what happened and report the error before anyone relies on it;
- it is re-checked whenever the model, the effort level or the process changes, because older
  history stops being comparable;
- the data stays in the client's infrastructure, identifiers only.

**Risks.** A small early sample gives confident nonsense. People adjust recorded times and
scores once they know the numbers are used (Goodhart's law). A forecast gets read as a
commitment.

**Status.** An idea. It needs the session tally to have run long enough to hold data, the
complexity metrics to be chosen, and a Discovery answer on whether ticket and time data can be
read from the tracker.

## Not doing

Dashboards, cost in currency inside the row, splitting one session by skill, and anything that
needs infrastructure the client has not agreed to.

## Before it can be built

- **One real, short transcript** from the owner's machine. The format cannot be inferred
  reliably from third-party descriptions. Take a session in an empty folder with a trivial
  message, find the file under `~/.claude/projects`, and read it before sending: a transcript
  can contain parts of the configuration.
- The answers to V31 (what the transcript and the hook really contain), V30 (whether the
  effective effort can be read) and V34 (whether OpenTelemetry is allowed).

## Related

Architecture §43 (session tally), §21A (cost measured outside the model), §36 checklist item
10; verification-log V30, V31, V33, V34.
