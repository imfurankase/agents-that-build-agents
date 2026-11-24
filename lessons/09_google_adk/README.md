# Lesson 09: Google AI Studio & the Agent Development Kit (ADK)

**Goal:** build Gemini-powered agent teams with Google's framework, and watch them work in a visual UI.

## Part A: Google AI Studio (no code)
[aistudio.google.com](https://aistudio.google.com) is a free playground for Gemini:
- **System instructions**: the agent's prompt. **Temperature/thinking**: creativity vs. precision.
- **Structured output**: paste a JSON schema; the answer must follow it.
- **Function calling**: declare tools; you play the role of the code that runs them.
- **Grounding with Google Search**: answers with sources.
- **Get code**: turns whatever you built into Python you can give to Claude Code.
- **Get API key**: the free key the Python lessons use (`GOOGLE_API_KEY` in `.env`).
- **Build** mode: describe an app in words and AI Studio generates it.

See [docs/AI_STUDIO_GUIDE.md](../../docs/AI_STUDIO_GUIDE.md) for step-by-step walkthroughs.

## Part B: ADK, a team with a visual debugger
`adk_team/agent.py` defines four agents: a **team_lead** that calls a **researcher** (Google Search), a **writer** and a **critic**, each wrapped as a tool (`AgentTool`).

```
cd lessons/09_google_adk
adk web
```
Open http://localhost:8000, choose **adk_team**, and ask: *"Write a half-page briefing on how AI agents are used in public services."* Click the events to see **which agent did what, with which inputs**. This is the best way to *see* multi-agent systems.

ADK ideas to know:
- `Agent(name, model, instruction, description, tools)`: one agent.
- `AgentTool(agent=...)`: call another agent like a function; the caller stays in charge.
- `sub_agents=[...]`: hand the conversation over to another agent (delegation/transfer).
- Workflow agents (sequential, parallel, loop) and graph workflows for fixed pipelines.

## Part C: Agents built at run time (`dynamic_team.py`)
1. **From data:** every saved agent in `agent_registry/` (from lesson 06) becomes an ADK agent. The same spec runs on a different framework.
2. **By an agent:** the lead has a `hire_specialist(name, instructions, task)` tool. It writes a new agent's instructions, and the tool creates and runs that agent on the spot (capped at 2 hires).

```
python run.py 9b "Create a checklist for a safe AI pilot in a 20-person team"
python run.py 9b --dry-run      # build only, no model calls
```

## Say this to Claude Code
> Start adk web for lesson 9 and tell me what to click to see the trace of each agent.

> Explain adk_team/agent.py. What is the difference between AgentTool and sub_agents? Change the writer to be a sub_agent and tell me how the behaviour changes.

> Add a fifth agent "fact_checker" to the ADK team that checks the writer's draft against the researcher's facts.

> Run lesson 9b and show me which specialists came from the registry and which were hired during the run.

> I built a prompt in AI Studio and clicked Get code. Here is the code: ... Turn it into an ADK agent in this repo.

## Takeaways
1. AI Studio = fastest way to try prompts, schemas and tools with no code.
2. ADK gives you a visual trace of multi-agent runs (`adk web`).
3. Agent specs are portable: the same JSON drives Gemini/ADK, Claude, or the mock.

**Exercises:** E9.1-E9.7
