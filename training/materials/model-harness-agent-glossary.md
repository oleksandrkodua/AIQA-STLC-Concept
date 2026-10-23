# Model, harness, agent and everything around them

STATUS: DRAFT v0.1, 2026-10-23. Example material for training. Translated into English from the author's Russian note (`claude-glossary.md`); wording lightly edited, meaning unchanged.

Labels: statements are the author's. Model names, effort levels and thinking behaviour come from the note's own source (a Claude API reference built into Claude Code, dated by the author 6 October 2026). They were NOT re-verified when this copy was made (UNKNOWN until checked against current documentation before a lesson uses them). Defaults and levels change between versions: do not quote them as fixed.

Possible conflict with the course (KNOWLEDGE CONFLICT, needs the course owner): this note calls the "Claude" that answers you an agent. Lesson 1 (Part A) teaches that a chat that only answers is an assistant, and an agent repeats plan, act, check on its own and changes things. Choose one definition before this note is used in a lesson.

---

**Model** is the "brain": a neural network that receives text and produces text. On its own it executes nothing, and between calls it remembers nothing. Claude models: Opus 5.5, Sonnet 5.5, Haiku 5.5, Fable 5.1. You can switch the model without changing anything else: for example, `/model` in Claude Code changes the model while the tools and file access stay the same.

**Harness** is the "body": the program around the model. It assembles the context, gives the model tools and runs them, asks for permission, and compresses a long history. The model only *asks* "read the file"; the harness reads it. That is why the same model in the claude.ai web chat cannot see files on your computer, while in Claude Code it can. Examples of harnesses: Claude Code, the claude.ai app, the Claude Agent SDK.

**Agent** is a model inside a harness that has a role, tools and a task. It works in a loop: the model decides, the harness executes, the result goes back to the model, and so on until the answer is ready. The "Claude" that answers you is an agent. The agents you create in Claude Code are a new configuration, not a new model: a file `.claude/agents/<name>.md` that holds the prompt, the allowed tools and, if you want, the model.

## Summary table

| Element | What it is | Analogy | Who turns it on | Example |
|---|---|---|---|---|
| **Model** | Generates text and decisions | Brain | You choose (`/model`) | Opus 5.5, Haiku 5.5 |
| **Effort** | How thoroughly to work: depth of thinking, number of tool calls, length of the answer. Levels: `low` → `medium` → `high` → `xhigh` → `max` | The instruction "do it fast" or "do it properly" | You or the harness (a request parameter; for a subagent it can be set in its file) | `low`: a simple question or a cheap subagent; `max`: a hard bug where a mistake is expensive |
| **Extended thinking** | The model reasons privately before it answers. The draft itself is not shown; only a short summary can be switched on | Thinking it over before speaking | The model decides how long to think (adaptive thinking). On Opus 5.5 it cannot be switched off; only effort controls the depth | Before editing code it weighs three hypotheses about the bug and picks one |
| **Harness** | The program around the model | Body and workplace | n/a | Claude Code, claude.ai |
| **Agent** | Model + harness + role and task, works in a loop | An employee | n/a | "Claude" in a chat |
| **Tools** | Concrete actions | Hands | The model asks, the harness executes | Read, Edit, Bash, WebSearch |
| **MCP / connectors** | Tools for outside services | A pass to other departments | You connect, the model calls | Notion, Slack, GitHub |
| **Skill** | A folder with instructions (SKILL.md), sometimes with scripts | A handbook on the shelf | The model, when the task fits, or you via `/name` | `pdf`: how to fill in a PDF form |
| **Hook** | A script the harness runs on an event | An automatic sensor | The harness, **always**; the model is not asked | A formatter after every Edit; a ban on `rm -rf` |
| **Subagent** | A separate agent with its own context, role and permissions | A helper: takes an assignment, returns a report | The main agent (or you ask for it) | `Explore` searches the code and returns only the result |
| **System prompt** | Role and rules from the harness | A job description | The harness, in every request | "You are Claude Code… do not push without asking" |
| **CLAUDE.md / preferences** | Standing instructions for a project or an account | A note at the workplace | The harness, automatically | "Tests: `npm test`"; your Working Instructions |
| **Your prompt** | A concrete task | An instruction from the manager | You | "Fix the login bug" |
| **Mode** | Level of permission | Level of clearance | You (Shift+Tab) | `default` asks, `acceptEdits` edits without asking, `plan` only plans, `auto` |

## Where people mix things up most often

- **Model or harness.** Memory, internet and file access are credited to the model, but they are abilities of the harness.
- **Skill or hook.** The model uses a skill when it *decides* the skill fits. A hook fires *always*. If a rule must hold with certainty, you need a hook.
- **Skill or subagent.** A skill adds knowledge to the *same* agent. A subagent is a *different* worker with a clean context.
- **Skill or MCP.** MCP gives *access* to a service; a skill gives a *skill* for doing something.
- **Effort or thinking.** Thinking is the process of reasoning itself; effort is the dial for how much work to spend on everything, including that process. Earlier, thinking was set with a fixed token budget (`budget_tokens`). Current models do not have this: the model decides how long to think, and you influence it only through effort. A high effort costs more and is slower, and on simple tasks it usually gives no better result.

## How to check it yourself

In Claude Code type `/agents` and open any agent: it is an ordinary text file with a prompt, not a separate model.

---

*The facts about effort and thinking were taken by the author from the Claude API reference built into Claude Code (updated 6 October 2026). By default effort is usually `high`; for Opus 5.5 and Haiku 5.5 it is `medium`.*

## Use in the course (suggestions, not decisions)

- Lesson 1 (the map) and lesson 3 (context and tokens): the "model vs harness" paragraph is a clear opener.
- Lesson 6 (skills) and lesson 8 (permissions and hooks): the "skill or hook" and "skill or MCP" lines.
- Lesson 7 (agent, subagent, skill): the "skill or subagent" line and the `/agents` check.
- The `/agents` check needs a surface where the command exists. For the Desktop Code tab the commands table in `training/lessons/_specs/2026-10-14-hooks-mods-commands-verification.md` lists it as offered (author test); not run by this note.

Provenance: translated by Claude (Sonnet 5.5, ai-generated) from the author's note, 2026-10-23; human-confirmed: pending.
