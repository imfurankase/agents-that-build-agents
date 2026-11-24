# Agents That Build Agents

**A prompt-first course on building AI agents that create, direct and control other agents, with Claude Code, Google AI Studio and Python.**

Written for a leader with limited coding experience. You will mostly **talk to Claude Code** in VS Code. It reads, runs and changes the code for you. Every lesson tells you exactly what to say.

```
 You ──prompt──> Claude Code ──runs──> Python agents ──create──> more agents
                     │                       │
                     └── subagents, skills   └── all checked by the Governor
                         & hooks (no code)       (budget, limits, approvals, kill switch)
```

---

## Start here (30 minutes)

1. **Set up your computer:** follow [docs/SETUP_WINDOWS.md](docs/SETUP_WINDOWS.md). In short: VS Code + Claude Code extension, Python, Git, the Claude Code CLI, and a free Google AI Studio key.
2. **Open this folder in VS Code**, open the Claude Code panel and type:
   > `/check-setup`
3. **Run your first agent** (free, offline):
   > `/run-lesson 4c`
4. Then follow the lessons in order. Each one has a `README.md` with the prompts to paste.

> **Stuck?** Type `/explain <anything>` in Claude Code, or see [docs/TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md).

---

## What you need: three ways to run things

| You have... | You can do... | Cost |
|---|---|---|
| Nothing yet | All Python lessons in **offline practice mode** (`LLM_PROVIDER=mock`): fake answers, real mechanics | Free |
| A **Google AI Studio** key | All Python lessons with real Gemini answers, plus Google ADK (lesson 09) | Free tier |
| **Claude Code** (VS Code extension, Pro/Max plan) | Everything in the Claude Code track: subagents, skills, `/build-team`, hooks, MCP. With the CLI installed: lessons 01c and 08a | Your plan |
| An **Anthropic API key** (optional) | The `*_claude_api` lessons and the Claude Agent SDK (08b) | Pay per token |

The Python lessons choose a provider automatically: Claude API key → Gemini key → offline mock.

---

## The course map

| # | Lesson | You will learn | Main file |
|---|---|---|---|
| 01 | [First call](lessons/01_first_call/) | What a model call is; tokens; system prompts | `hello_gemini.py` |
| 02 | [Prompting](lessons/02_prompting/) | The #1 skill: role, context, task, format, rules | `prompt_lab.py` |
| 03 | [Tools](lessons/03_tools/) | Giving an AI "hands" | `gemini_tools.py` |
| 04 | [The agent loop](lessons/04_agent_loop/) | The one loop behind every agent | `watch_the_loop.py` |
| 05 | [Multi-agent patterns](lessons/05_multi_agent_patterns/) | Chain, router, parallel, orchestrator, evaluator | `p4_orchestrator_workers.py` |
| 06 | [**Agents that build agents**](lessons/06_agents_that_build_agents/) | Agent specs; the architect; the meta-agent | `b_meta_agent.py` |
| 07 | [**Controlling agents**](lessons/07_controlling_agents/) | Budgets, limits, approvals, kill switch, audit | `governor_demos.py` |
| 08 | [Claude Code as an agent factory](lessons/08_claude_code_agents/) | Subagents, skills, hooks, headless CLI, Agent SDK | `.claude/` + `cli_agent_factory.py` |
| 09 | [Google AI Studio & ADK](lessons/09_google_adk/) | Gemini agents, visual debugging with `adk web` | `adk_team/agent.py` |
| 10 | [MCP](lessons/10_mcp/) | Plugging agents into tools and data | `agent_registry_server.py` |
| 11 | [Evals & safety](lessons/11_evals_and_safety/) | Testing agents; prompt injection | `eval_harness.py` |
| 12 | [**Capstone: Agent Foundry**](lessons/12_capstone_agent_foundry/) | A full governed mission, end to end | `mission.py` |

Run any lesson with `python run.py <id>` (e.g. `python run.py 6b`), or in Claude Code: `/run-lesson 6b`.

---

## Claude Code shortcuts built into this repo

| Type this in Claude Code | What happens |
|---|---|
| `/check-setup` | Checks and fixes your setup, step by step |
| `/run-lesson 6b` | Runs a lesson and explains the output |
| `/explain common/governor.py` | Plain-English explanation of any file or error |
| `/new-agent <description>` | Designs, safety-reviews and saves a new Claude Code subagent |
| `/build-team <goal>` | Designs a team of agents for a goal, runs them, reports |
| `/new-python-agent <description>` | Creates a Python agent in the registry and test-runs it |
| `/review-agent <name>` | Safety review of any agent |
| `/quiz-me 07` | Quiz on a lesson, one question at a time |
| `/audit` | What did the agents do? Costs, tools, blocks, approvals |
| `/stop-all` | **Kill switch**: freezes every agent until you delete `STOP` |

Built-in subagents in [.claude/agents/](.claude/agents/): `agent-architect`, `safety-reviewer`, `code-explainer`, `researcher`, `lesson-tutor`, `test-runner`.

---

## Learning materials

- [prompts/PROMPTING_GUIDE.md](prompts/PROMPTING_GUIDE.md): how to write prompts for models, agents and Claude Code
- [prompts/PROMPT_LIBRARY.md](prompts/PROMPT_LIBRARY.md): 100+ copy-paste prompts, by lesson
- [exercises/EXERCISES.md](exercises/EXERCISES.md): 80+ exercises in three levels; hints in [exercises/HINTS.md](exercises/HINTS.md)
- [docs/LEARNING_PLAN.md](docs/LEARNING_PLAN.md): a 6-week plan, 3-4 hours a week
- [docs/TOOLS.md](docs/TOOLS.md): the recommended toolkit and why
- [docs/CLAUDE_CODE_GUIDE.md](docs/CLAUDE_CODE_GUIDE.md): Claude Code for agent builders
- [docs/AI_STUDIO_GUIDE.md](docs/AI_STUDIO_GUIDE.md): Google AI Studio, no code
- [docs/COSTS_AND_SAFETY.md](docs/COSTS_AND_SAFETY.md): money, data and safety rules
- [docs/GLOSSARY.md](docs/GLOSSARY.md): every term in one page

---

## How the code is organised

```
common/            the shared engine (read llm.py first: the agent loop)
  llm.py           one loop, three providers: Claude, Gemini, offline mock
  toolbox.py       every tool an agent can be given, with risk levels
  spec.py          AgentSpec: an agent written down as data
  foundry.py       designs, hires, runs agents; meta-tools let agents hire agents
  governor.py      the controls: budget, headcount, depth, tool ceiling, approvals, kill switch, audit
  registry.py      saved agents (agent_registry/*.json)
  claude_cli.py    drive Claude Code from Python (uses your subscription)
lessons/           12 lessons, each with a README
prompts/system/    the system prompts the agents load (edit text, change behaviour)
.claude/           Claude Code subagents, skills (slash commands), hooks, settings
tests/             offline tests: python -m pytest -q  (free)
workspace/         the ONLY folder Python agents may write to
logs/              audit logs of every run
```

Safety by design: agents can only touch `workspace/`, can only fetch allow-listed websites, never see `.env`, and every action goes through the Governor and into the audit log.

---

*Model names change often. This course uses `claude-opus-5-5` and `gemini-flash-latest` by default; change them in `.env`.*
