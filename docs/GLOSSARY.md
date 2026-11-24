# Glossary

Every term used in the course, one line each, A–Z.

| Term | Meaning |
|---|---|
| **Agent** | A model running in a loop with tools, choosing its own next steps until a goal is done (or it is stopped). |
| **Agent loop** | Call the model → run the tools it asks for → feed results back → repeat until it answers without asking for tools. |
| **Agent SDK (Claude)** | Python/TypeScript library that gives your programs Claude Code's engine (tools, subagents, hooks). Needs an API key. |
| **Agent teams** | Experimental Claude Code feature: a lead session plus teammates sharing a task list. Off by default. |
| **AgentSpec** | This course's "job description" format for an agent: name, role, instructions, tools, limits (`common/spec.py`). |
| **AgentTool** | Google ADK wrapper that lets one agent call another agent like a function. |
| **Allowlist** | A list of what *is* permitted (e.g. websites `fetch_webpage` may open); everything else is refused. |
| **API key** | A secret password that lets a program use a model provider, billed per use. Lives in `.env`. |
| **Approval gate** | A point where a human must say yes before an action happens. |
| **Architect (agent)** | An agent whose job is to design other agents (`a_architect.py`, `agent-architect` subagent). |
| **Audit log** | A permanent record of every action and decision (`logs/run-*.jsonl`, `logs/claude_code_audit.jsonl`). |
| **Budget** | A spending cap; the Governor stops the run when it is reached. |
| **Caching (prompt caching)** | Re-using an identical prompt prefix so repeated calls are cheaper and faster. |
| **Chain** | Pattern: fixed steps in order, each using the previous output. |
| **Checkpoint / rewind** | Claude Code saves state at each step; you can roll code and/or conversation back. |
| **CLAUDE.md** | Standing instructions Claude Code reads at the start of every session in a project. |
| **Context window** | The maximum text a model can consider in one call (input + output), measured in tokens. |
| **Delegation** | One agent handing a task to another (a subagent, a sub_agent, or via `run_agent`). |
| **Depth limit** | Maximum levels of agents creating agents (orchestrator → child → grandchild). |
| **Effort** | Claude setting (low → max) for how much thinking to spend; higher = better on hard tasks, more tokens. |
| **Eval (evaluation)** | A test suite for an agent: cases + success criteria + a grader; gives a pass rate. |
| **Evaluator-optimizer** | Pattern: a writer and a judge loop until the work passes (or a round limit is hit). |
| **Fallbacks** | Claude API option: if a request is declined by a safety check, retry automatically on a fallback model. |
| **Function calling** | Google's name for tool use. |
| **Governor** | This course's supervisor code that enforces budgets, limits, approvals, kill switch and audit (`common/governor.py`). |
| **Grounding** | Connecting a model to fresh sources (e.g. Google Search) so answers cite real documents. |
| **Guardrail** | Any rule or mechanism that keeps an agent within safe bounds. The strongest are enforced in code. |
| **Hallucination** | A confident but false statement made up by a model. Countered with sources, rules ("say unknown") and checks. |
| **Headcount limit** | Maximum number of new agents per run. |
| **Headless mode** | Running Claude Code without the chat UI: `claude -p "…"`, for scripts and automation. |
| **Hook** | Code that runs automatically before/after an agent action and can block it (exit code 2 in Claude Code). |
| **Human-in-the-loop** | Design where people approve, correct or stop agent actions at key points. |
| **Instructions** | The system prompt of an agent; in AgentSpec, the `instructions` field. |
| **JSON** | A simple text format for structured data: `{"name": "x", "tools": []}`. |
| **JSON schema** | A description of the exact shape JSON must have; used to force structured output. |
| **Kill switch** | Instant stop for all agents. Here: create a file named `STOP` (or `/stop-all`). |
| **Least privilege** | Give each agent only the tools and access its job truly needs. |
| **LLM** | Large language model, the AI that reads and writes text (Claude, Gemini). |
| **LLM judge** | A model used to grade another model's output against criteria. |
| **Max turns** | Cap on how many loop iterations an agent may take. |
| **MCP (Model Context Protocol)** | Open standard for connecting AI apps to tools and data through "servers". |
| **MCP server** | A small program exposing tools/data over MCP (e.g. `agent_registry_server.py`). |
| **Meta-agent** | An agent that creates, directs and retires other agents (the orchestrator in lesson 06). |
| **Meta-tools** | The tools that let an agent manage agents: `create_agent`, `run_agent`, `list_agents`, `retire_agent`. |
| **Mock mode** | `LLM_PROVIDER=mock`: a fake offline model; free, for practising mechanics. |
| **Model** | The specific AI engine, e.g. `claude-opus-5-5`, `gemini-flash-latest`. |
| **Orchestrator** | The manager agent that splits work and coordinates workers. |
| **Orchestrator-workers** | Pattern: a manager decides sub-tasks at run time and delegates them. |
| **Parallelization** | Pattern: independent tasks run at the same time, then results are combined. |
| **Permission mode** | Claude Code setting for how much it may do without asking (Manual, Edit automatically, Plan, Auto; `dontAsk` in headless runs). |
| **Plan mode** | Claude Code reads and proposes a plan but changes nothing until you approve. |
| **Privilege escalation** | An agent gaining more power than it was given (e.g. a child with tools its parent lacks); blocked by the Governor. |
| **Prompt** | The text you give a model: instructions, context, request. |
| **Prompt injection** | Hidden instructions inside data (emails, web pages) that try to hijack an agent. |
| **Provider** | The company/service behind a model: Anthropic (Claude), Google (Gemini), or the mock. |
| **Rate limit** | Maximum requests/tokens per minute or day; exceeding it gives error 429. |
| **Registry** | The folder of saved agent specs (`agent_registry/`); agents as reusable, versioned assets. |
| **Retire (an agent)** | Move an agent out of active use (kept in `agent_registry/retired/` for the record). |
| **Router** | Pattern: classify a request and send it to the right specialist. |
| **Sandbox** | A restricted area where an agent can act safely (here: the `workspace/` folder). |
| **Skill** | Claude Code playbook in `.claude/skills/<name>/SKILL.md`, run with `/name`. |
| **Spawn** | To create and start another agent (`spawn_agents` permission in this course). |
| **Structured output** | Model output forced to follow a JSON schema, so code can use it reliably. |
| **Subagent** | Claude Code specialist defined in `.claude/agents/*.md`, with its own prompt, tools and context. |
| **Sub_agents (ADK)** | ADK option to transfer the conversation to another agent (vs. calling it as a tool). |
| **Subscription** | Your Claude Pro/Max plan: covers Claude Code usage within plan limits; not an API key. |
| **System prompt** | Standing instructions that define an agent's role, method and rules. |
| **Temperature** | Randomness of the output: low = predictable, high = creative. |
| **Token** | The unit models read and write (about ¾ of a word); the unit of cost and limits. |
| **Tool** | A function an agent may ask your code to run (calculator, read_file, another agent…). |
| **Tool ceiling** | The set of tools any agent in a run may ever hold; set in the Governor's Policy. |
| **Tool description** | The text that tells the model what a tool does and when to use it. As important as a prompt. |
| **Toolbox** | All tools available to course agents, with risk levels (`common/toolbox.py`). |
| **Turn** | One model call within the agent loop. |
| **Untrusted input** | Any content not written by you or your code (web, email, uploaded files). Treat it as data, never as orders. |
| **Worker** | An agent that does one sub-task for an orchestrator. |
| **Workflow** | Steps decided in code in advance (vs. an agent, where the model decides steps at run time). |
| **Workspace** | The only folder Python agents may read and write (`workspace/`). |
