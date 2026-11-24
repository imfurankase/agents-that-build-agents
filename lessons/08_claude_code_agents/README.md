# Lesson 08: Claude Code as your agent factory

**Goal:** build, run and control agents **inside Claude Code** (mostly no code), and let Claude Code create agents for you.

Claude Code is itself an agent: a model in a loop with tools (read, edit, run commands, search the web, start subagents). It has five building blocks you can shape with plain text:

| Building block | What it is | Where it lives | Analogy |
|---|---|---|---|
| **CLAUDE.md** | Standing instructions for every session | `CLAUDE.md` | The team handbook |
| **Subagents** | Specialists with their own prompt, tools and fresh context | `.claude/agents/*.md` | Specialist staff |
| **Skills** (slash commands) | Reusable playbooks you trigger with `/name` | `.claude/skills/<name>/SKILL.md` | Standard operating procedures |
| **Hooks** | Code that runs automatically before/after actions; can block | `.claude/settings.json` + `.claude/hooks/` | Security guards |
| **MCP servers** | Plug-ins that add tools and data | `claude mcp add ...` (lesson 10) | Connections to other departments |

## Part A: Subagents (no code)
A subagent is a Markdown file. The top part (frontmatter) says **who it is, when to use it and what tools it may use**; the body is its **system prompt**:
```markdown
---
name: policy-checker
description: Checks a document against our AI usage policy. Use when asked to check, review or vet a document for policy compliance.
tools: Read, Grep, Glob
---
You are a compliance officer... (method, output format, boundaries)
```
- **description** decides *when* Claude delegates. Write it like a job advert with trigger words.
- **tools** is least privilege. Omit only if it truly needs everything.
- Each subagent works in its **own context window** and returns only a summary, so your main conversation stays clean.
- Subagents can start their own subagents (up to 3 levels deep by default). Agents creating agents, built in!
- New or edited files are picked up within seconds. No restart needed.

**This repo ships 6 subagents:** `agent-architect` (writes new agents), `safety-reviewer`, `code-explainer`, `researcher`, `lesson-tutor`, `test-runner`.

### Say this to Claude Code
> Use the agent-architect subagent to create a "meeting-scribe" agent that turns pasted meeting notes into decisions, owners and deadlines. Then use the safety-reviewer on it.

> /new-agent an agent that reviews draft emails for tone and clarity before I send them

> Use the meeting-scribe agent on these notes: ...

> /build-team Produce a one-page briefing on AI agent risks for our leadership team, with sources

> Which subagents exist in this project, what tools does each have, and which one has the most risk?

## Part B: Skills (slash commands, no code)
A skill is a playbook in Markdown. `$ARGUMENTS` is replaced by whatever you type after the command. Look at `.claude/skills/build-team/SKILL.md`: it orchestrates the architect, the reviewer, your approval, the run and the clean-up.

> Create a new skill called /weekly-brief that asks me for this week's notes, uses the researcher for any facts to check, and writes a one-page brief to workspace/briefs/.

## Part C: Hooks, control without trusting the model
`.claude/settings.json` registers two hooks that run before tool calls:
- `guard.py`: blocks reading `.env`, destructive commands, and **everything** while a `STOP` file exists (kill switch).
- `audit_log.py`: writes every tool call to `logs/claude_code_audit.jsonl`.

It also sets **permissions**: some commands always allowed, `git push`/`commit` always ask, `.env` reads denied.

> /stop-all, then ask me to run lesson 4c. Explain what blocked it.

> /audit: what tools did you use in this session?

## Part D: Headless mode, scripts that create Claude Code agents
`claude -p "prompt"` runs Claude Code without the chat window, which is perfect for automation. With `--agents` a script can **define subagents on the fly**. `cli_agent_factory.py`:
1. asks Claude Code to **design** a team (as JSON, guaranteed by `--json-schema`),
2. asks **you** to approve,
3. runs the goal with those agents (`--agents`, `--permission-mode dontAsk`, an allow-list of tools, `--max-turns`), in its own folder,
4. optionally **saves** the agents to `.claude/agents/` (`--save`) so you can reuse them in VS Code.

```
python run.py 8a "Research 3 public examples of AI agents in government and write summary.md" --save
```
Uses your subscription (needs the CLI installed and logged in). The helper removes any `ANTHROPIC_API_KEY` from the call so it does not bill the API by accident.

Useful headless flags: `--output-format json`, `--allowedTools "Read,Grep"`, `--permission-mode dontAsk|plan|acceptEdits`, `--max-turns 10`, `--max-budget-usd 2`, `--append-system-prompt "..."`, `--agents file.json`, `--json-schema '{...}'`, `--model`.

## Part E: The Claude Agent SDK (optional, API key)
The same engine as Claude Code, as a Python library. `sdk_subagents.py` shows `AgentDefinition` (subagents as data), a `PreToolUse` hook that can deny actions, and hard limits (`max_turns`, `max_budget_usd`). Anthropic's terms require an **API key** for SDK-built agents.

## Agent teams (experimental)
Claude Code also has experimental **agent teams**: a lead session spawns teammates that share a task list and message each other. Off by default (`CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1`), uses many more tokens, and runs in the terminal CLI. Try it only after this course.

## Takeaways
1. In Claude Code, agents are **Markdown files**. Anyone who can write a clear brief can build one.
2. **Description = when, tools = what, body = how.**
3. Control comes from **permissions + hooks + limits**, not from asking nicely.
4. Headless mode + `--agents` lets programs (and agents) create Claude Code agents at run time.

**Exercises:** E8.1-E8.12
