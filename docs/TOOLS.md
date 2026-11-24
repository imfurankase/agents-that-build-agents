# The recommended toolkit

**Priority:** **Must** = needed for the course · **Should** = strongly recommended · **Nice** = later / optional.

## What you already have

| Tool | Role in this course | Notes |
|---|---|---|
| **Claude Code (VS Code extension)** | Your main workspace: you prompt, it builds and runs | Uses your Claude Pro/Max plan |
| **Google AI Studio** | No-code prototyping + the **free Gemini API key** the Python lessons use | Mind free-tier rate limits and data terms |
| **PyCharm** | Optional second editor for reading code | Claude Code works in its terminal (CLI) and via the JetBrains plugin |

## Recommended additions

| Tool | Why | When you need it | Cost | Priority |
|---|---|---|---|---|
| **Claude Code CLI** | Run Claude Code from a terminal and from scripts (`claude -p`); `--agents` lets scripts create subagents | Lessons 01c, 08a, 10 | Included in your plan | **Must** |
| **Git for Windows** | Version history ("undo" for whole projects); Claude Code uses its Git Bash for commands and hooks | From day 1 | Free | **Must** |
| **Python 3.12** | Runs the course's agents | From lesson 01 | Free | **Must** |
| **uv** | Installs Python packages quickly and reliably | Setup | Free | **Must** |
| **GitHub account** | Get the course, keep your own agents, share with colleagues | Setup, then ongoing | Free | **Should** |
| **GitHub Desktop** | Point-and-click Git for non-coders (commit, sync, history) | If Git commands feel heavy | Free | Nice |
| **Google ADK** (`pip install google-adk`) | Google's multi-agent framework; `adk web` shows a visual trace of which agent did what | Lesson 09 | Free (uses your Gemini key) | **Should** |
| **MCP** + **MCP Inspector** | The standard plug between agents and tools; Inspector lets you click through a server's tools | Lesson 10 | Free | **Should** |
| **Node.js LTS** | Needed to run MCP Inspector (`npx`) and many community MCP servers | Lesson 10 extras | Free | Nice |
| **Windows Terminal** | Tabs, better colours and Unicode than the old console | Any time | Free | Nice |
| **Anthropic Console** (platform.claude.com) | API keys, **spend limits**, usage reports, a prompt Workbench | Only if you want the Claude API | Pay per token | Nice |
| **Claude Agent SDK** (Python) | Claude Code's engine inside your own programs; subagents as data, hooks, budgets | Lesson 08b | API key, pay per token | Nice |
| **Claude Managed Agents** | Anthropic-hosted agents (beta): Anthropic runs the loop and a sandbox per session, with multi-agent "workflows" built in | The "graduate" step: production agents without hosting them yourself | API usage + session runtime | Nice (later) |
| **Docker Desktop** | Sandboxes: run agent-written code in a disposable container | When agents run code for real | Free for small orgs; check licence | Nice |
| **Ollama** | Run open models **locally**: data never leaves the machine | Sensitive data experiments | Free (needs a good PC) | Nice |
| **Langfuse / OpenTelemetry** | Observability: traces, costs and quality across many agent runs | When agents go beyond experiments | Free tiers / self-host | Nice |
| **Mermaid / draw.io** | Draw agent architectures (Claude Code can write Mermaid diagrams for you) | Presentations, design reviews | Free | Nice |

## Claude models used in this course (Anthropic list prices per 1M tokens)

| Model | ID | Input | Output | Good for |
|---|---|---|---|---|
| Claude Opus 5.5 | `claude-opus-5-5` | $4 | $20 | Default: planning, orchestrating, judging |
| Claude Sonnet 5.5 | `claude-sonnet-5-5` | $2 | $10 | Everyday agent work at lower cost |
| Claude Haiku 5.5 | `claude-haiku-5-5` | $0.10 | $0.50 | Simple, high-volume worker tasks |

Prices apply only to API-key usage; your subscription covers Claude Code. Gemini pricing: see Google's pricing page (the free tier is $0 within its limits).

## How the pieces fit
```
 Google AI Studio ──prototype──┐
                               ▼
 You ──prompt──> Claude Code (VS Code / CLI) ──builds & runs──> Python agents (Gemini / Claude / mock)
                    │  subagents, skills, hooks                      │  Governor + audit log
                    └──MCP──> your tools & data <────────────────────┘
                                                     Google ADK (adk web) for visual multi-agent traces
```
