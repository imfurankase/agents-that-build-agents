# CLAUDE.md - instructions for Claude Code in this project

## Who you are helping
The learner is a senior leader learning to build AI agents that build and control other agents. They have **limited coding experience** and work mainly by **prompting Claude Code in VS Code**. They may also use the Claude Code CLI, Google AI Studio and PyCharm.

## How to work with them
- Explain in **plain English**. Define any technical word the first time you use it, in one short phrase.
- Before a change: say in 1-2 lines what you will do. After it: summarise in **3 bullets max** what changed and how to see it working.
- Prefer **small, reversible steps**. Show the command you are about to run and why.
- When they ask "how does X work", point to the file and line, then explain the idea before the code.
- End teaching moments with **one suggested next step or exercise** (see `exercises/EXERCISES.md`).
- If a request is ambiguous, ask **one** clarifying question instead of guessing.

## Project map
- `run.py` - launcher: `python run.py` lists every lesson; `python run.py 6b` runs one.
- `lessons/NN_*/` - the 12 lessons, each with a `README.md`. Read it before running the lesson.
- `common/` - shared engine: `llm.py` (the agent loop), `governor.py` (controls), `foundry.py` (agents that build agents), `toolbox.py` (tools agents may get), `spec.py` (AgentSpec).
- `prompts/system/*.md` - system prompts the Python agents load. Edit text here to change behaviour.
- `agent_registry/` - saved Python agents (JSON). `workspace/` - the ONLY folder Python agents may write to. `logs/` - audit logs.
- `final_project/` - the learner's end goal: a personal assistant (calendar, email, free APIs, reminders, chat) on their phone via a Telegram bot. Read `final_project/README.md`. It must stay read-only (no send/forward/delete tools).
- `.claude/agents/` - Claude Code subagents. `.claude/skills/` - slash commands such as `/explain`, `/new-agent`.

## Running things
- Python: use the project virtual environment: `.venv\Scripts\python.exe` on Windows (create it with `uv venv` then `uv pip install -r requirements.txt` if missing).
- Offline, free practice: set `LLM_PROVIDER=mock` in `.env`. Real answers: a `GOOGLE_API_KEY` (free tier) or `ANTHROPIC_API_KEY`.
- Tests: `python -m pytest -q` (offline, free). Run them after any change to `common/`.
- Setup check: `python scripts/check_setup.py`.

## Safety rules (always)
- **Never open, print or edit `.env`**. To check keys, run `python scripts/check_setup.py`, which only says set/not set.
- **Ask before** anything that may cost money in a loop (many model calls), deletes files, or touches anything outside this repo.
- **Never `git push`, publish, or create remote resources** without an explicit "yes" in this conversation.
- New Python agents get the **fewest tools** they need. Never give `run_python` unless asked.
- New Claude Code subagents: least-privilege `tools:` list, a clear `description:` saying WHEN to use them, and a body with method, output format and boundaries. Use the `agent-architect` subagent to write them and `safety-reviewer` to check them.
- If a file called `STOP` exists in the repo root, all agents are frozen on purpose. Tell the learner and do not delete it unless they ask.
