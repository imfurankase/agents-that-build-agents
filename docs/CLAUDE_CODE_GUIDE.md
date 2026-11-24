# Claude Code for agent builders

Claude Code is an **agent**: a Claude model running in a loop with tools (read and edit files, run commands, search the web, start subagents). In this course it is both **your assistant** (it runs and changes the code for you) and **your agent factory** (you build agents with it, in plain English).

---

## 1. Tour of the VS Code panel

| Where | What it does |
|---|---|
| **Chat box** | Type requests. Press `/` for commands and skills, `@` to mention a file. |
| **Mode indicator** | Switch permission modes (see below). |
| **`/` menu** | Built-in commands plus this course's skills (`/check-setup`, `/build-team`, …). Not every CLI command exists in the panel. |
| **Customize** | Edit **Instructions** (CLAUDE.md) and **Hooks** without touching files by hand. |
| **Message hover** | Fork the conversation, or **rewind** code and/or conversation to that point (checkpoints). |
| **Diffs** | Proposed file changes open as side-by-side diffs you can accept or reject. |
| **`/mcp`** | Add, remove, enable or reconnect MCP servers. |
| **`/tasks`** | See running subagents and background work. |

### Permission modes: when to use each

| Mode | What Claude Code may do | Use it when |
|---|---|---|
| **Manual** (ask) | Asks before edits and commands | Learning, or anything unfamiliar. **Start here.** |
| **Edit automatically** | Edits files without asking; still asks for commands | You trust the direction and want speed |
| **Plan** | Only reads and proposes a plan; changes nothing | Before any bigger change. Review the plan first |
| **Auto** | Decides on its own, with built-in safety checks | Routine work in this sandboxed course repo |

### Plan mode
Type `/plan` or pick **Plan** in the mode indicator. Claude Code investigates and writes a plan as Markdown, which you can comment on. Approve it and it starts work. **Use it for anything that touches more than one file.**

### Checkpoints and rewind
Every step is a checkpoint. Hover over an earlier message to **rewind the code**, the **conversation**, or both. That makes experiments safe: try something bold, then rewind if you don't like it.

### @-mentions
`@common/governor.py` attaches a file. You can mention line ranges, or use **Add to Chat** from the Explorer's right-click menu. Precise context gives better answers.

---

## 2. CLAUDE.md: the team handbook
`CLAUDE.md` in the project root is read at the start of every session. It tells Claude Code who you are, how to work, and the safety rules. This course's CLAUDE.md asks for plain English, small steps, and never reading `.env`.

- Create one for any new project with **`/init`** (Claude Code scans the folder and drafts it).
- Edit it via **Customize → Instructions** or by asking: *"Add a rule to CLAUDE.md: always show me the plan first for changes to common/."*
- Keep it short and specific. Rules with reasons work best.

---

## 3. Subagents: specialists as Markdown files
A subagent is a file in `.claude/agents/` (project) or `~/.claude/agents/` (all your projects):

```markdown
---
name: policy-checker
description: Checks a document against our AI usage policy. Use when asked to check, vet or review a document for policy compliance.
tools: Read, Grep, Glob
---
You are a compliance officer...
## Method  1. … 2. …
## Output format  …
## Boundaries  …
```

| Part | Job | Tip |
|---|---|---|
| `description` | **When** Claude delegates to it | Write it like a job advert with trigger words |
| `tools` | **What** it may do | Least privilege. Omitting it means *all* tools |
| body | **How** it works (its system prompt) | Method, output format, boundaries |
| `model` *(optional)* | Which model | e.g. `sonnet`, `opus`, `haiku`, or `inherit` |

Facts worth knowing:
- Each subagent has its **own context window** and returns a summary, so your main chat stays focused.
- Subagents can start subagents **up to 3 levels deep** by default (env var `CLAUDE_CODE_MAX_SUBAGENT_SPAWN_DEPTH` changes it). That makes agents creating agents a built-in feature.
- New or edited agent files are picked up **within seconds, no restart needed**.
- `/agents`: on recent versions it reminds you to create agents by asking Claude or editing files. The easiest way is to **ask**: *"Create a subagent that…"* or use this course's **`/new-agent`**.
- Call one explicitly: *"Use the researcher agent to…"*

---

## 4. Skills: reusable playbooks (slash commands)
A skill is `.claude/skills/<name>/SKILL.md`. You run it by typing `/<name> …`.

```markdown
---
name: weekly-brief
description: Turn my notes into a one-page weekly brief.
argument-hint: "<notes or file>"
disable-model-invocation: true     # only runs when I type it
---
Turn $ARGUMENTS into a one-page brief: ...steps...
```
- `$ARGUMENTS` is replaced by what you type after the command.
- `disable-model-invocation: true` = only **you** can trigger it (good for actions like `/stop-all`).
- Without it, Claude may use the skill by itself when the description matches.
- Older `.claude/commands/*.md` files still work; skills are the recommended form.

This course ships: `/check-setup`, `/run-lesson`, `/explain`, `/new-agent`, `/new-python-agent`, `/build-team`, `/review-agent`, `/quiz-me`, `/audit`, `/stop-all`.

---

## 5. Hooks: control that doesn't depend on the model
Hooks are commands that run automatically at moments like **before a tool call** (`PreToolUse`), after one (`PostToolUse`), or when Claude stops. Configured in `.claude/settings.json` (or **Customize → Hooks**).

- A hook that **exits with code 2 blocks** the action; its error message is shown to Claude.
- This course's hooks:
  - `.claude/hooks/guard.py`: blocks reading `.env`, a few destructive commands, and **everything** while a `STOP` file exists (kill switch).
  - `.claude/hooks/audit_log.py`: logs every tool call to `logs/claude_code_audit.jsonl`.
- **Permissions** in the same file: `allow` (never asks), `ask` (always asks, e.g. `git push`), `deny` (never, e.g. reading `.env`).

---

## 6. MCP: plug in tools and data
- In the panel: **`/mcp`** to see, add, enable or reconnect servers.
- In a terminal: `claude mcp add <name> -- <command> <args>`, for example
  `claude mcp add agent-registry -- .venv\Scripts\python.exe lessons\10_mcp\agent_registry_server.py`
- **Scopes:** `local` (default: just you, this project), `project` (writes `.mcp.json`, shared via git), `user` (all your projects): `--scope project`.
- `.mcp.json` example: see `.mcp.json.example` in the repo root.
- Only add servers from sources you trust. They run on your machine.

---

## 7. Headless mode: Claude Code from scripts
`claude -p "prompt"` runs one task without the chat window and prints the result. The prompt can also come through a pipe: `type task.txt | claude -p`.

| Flag | What it does |
|---|---|
| `--output-format json` | One JSON result (fields like `result`, `num_turns`, `total_cost_usd`, `structured_output`) |
| `--json-schema '{…}'` | Forces the answer to match a JSON schema (`structured_output`) |
| `--agents file.json` | Defines **subagents for this run only** (JSON: name → description, prompt, tools) |
| `--allowedTools "Read,Grep"` | Tools that run without asking |
| `--permission-mode dontAsk` | Anything not allowed is refused automatically (nobody to click "yes") |
| `--permission-mode plan` | Read-only planning |
| `--max-turns 10` | Hard cap on agent loop turns |
| `--max-budget-usd 2` | Cost cap (estimated) |
| `--append-system-prompt "…"` | Extra instructions |
| `--model sonnet` | Choose the model |

**Billing caveats:**
- Headless runs use your **subscription** after you've logged in once, *unless* `ANTHROPIC_API_KEY` is set, in which case the API key is billed. The course helper (`common/claude_cli.py`) removes the key for its calls.
- `--bare` mode **does not use your subscription login**. Don't use it with a subscription.
- Each call loads Claude Code's full toolkit (tens of thousands of tokens of context). Don't call it in tight loops.

See it in action: `lessons/08_claude_code_agents/cli_agent_factory.py`.

---

## 8. Background work and agent teams
- **Background agents/subagents:** long tasks can run in the background while you keep chatting; check them with `/tasks` in the panel.
- **Agent teams (experimental):** a lead session spawns *teammates* that share a task list and message each other. Off by default; enable with the environment variable `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1`. Uses many more tokens, works best in the terminal CLI, and has limits (no nested teams, one team per session). Try it only after finishing the course.

## 9. Usage limits
Your plan has usage windows (per session and per week) shared by chat, subagents and headless runs. Type **`/usage`** to see where you stand. Big multi-agent runs use more; plan them.

---

## 10. The 12 golden rules for prompting Claude Code
1. **Say who you are once** (it's in CLAUDE.md): "I'm not a programmer; explain simply."
2. **One goal per request.** Big goals: ask for a plan first (Plan mode).
3. **Name the files** with `@` mentions. Precise context gives precise work.
4. **Describe "done":** "…and the tests pass" / "…and show me the output".
5. **Ask it to run things**, not just write them: "Run it and show me what happened."
6. **Give the why:** "Keep it simple because I'll present it to my board."
7. **Constrain scope:** "Only change toolbox.py." "Under 30 lines."
8. **Ask for the explanation last:** "Then explain what you changed in 3 bullets."
9. **Use subagents for side quests:** "Use the researcher agent to check…" keeps your chat clean.
10. **Review diffs before accepting**; rewind freely if you don't like the result.
11. **Never paste secrets** into the chat; keys go in `.env`, which you edit yourself.
12. **When stuck, paste the exact error** and ask "explain simply, then fix it."

---

## 11. A day in the life (example session)

> **You:** /run-lesson 6b "Write a one-page guide on safe use of AI chatbots for staff, plus a 5-question quiz"
>
> **Claude Code:** This runs the meta-agent (it will call Gemini with your free key). Running… The orchestrator hired 2 agents: `guide-writer` (tools: save_note) and `quiz-maker` (tools: read_notes). It ran the writer, then the quiz maker, checked the quiz against the guide, and finished in 9 turns for about $0.00 on the free tier. Files: `workspace/team_notes.md`. Audit log: `logs/run-…jsonl`. Suggested exercise: E6.4.
>
> **You:** Open the guide-writer spec and explain it simply.
>
> **Claude Code:** *(uses code-explainer)* In one sentence: it's a job description for a writer who produces one-page staff guides… **Try this:** "Improve guide-writer so it always adds a 'Who to contact' section."
>
> **You:** Do that, then run it again on the same goal.
>
> **Claude Code:** Updated via `c_reuse_agents.py improve` (now version 2). Reran… the guide now ends with a contact section.
>
> **You:** /review-agent guide-writer
>
> **Claude Code:** Rating: LOW. It has only `save_note`, reads no untrusted input, and its prompt has clear boundaries. No changes needed.
>
> **You:** /audit
>
> **Claude Code:** Latest run: 2 agents created by the orchestrator, 0 blocked actions, 0 human decisions, ~14 model calls. Claude Code itself ran 6 commands today, all lesson scripts. Nothing unusual.
