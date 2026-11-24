# Lesson 06: Agents that build agents

**Goal:** have an AI design, create, run, reuse and improve other AI agents.

## The big idea: an agent is data
```
AgentSpec = name + role + instructions (system prompt) + tools + limits
```
Once an agent is written down as data (a JSON file), **another agent can write it**. Then:

1. The **Architect** turns one sentence into a full AgentSpec (`a_architect.py`).
2. The **Meta-agent** (orchestrator) gets 4 special tools: `list_agents`, `create_agent`, `run_agent`, `retire_agent`. It decides on its own which specialists to hire, writes their instructions, gives them tasks, and checks their work (`b_meta_agent.py`).
3. Created agents are saved in `agent_registry/`. They are **assets** you can reuse, improve and retire (`c_reuse_agents.py`).

```
   You: "goal"
      │
      ▼
 [orchestrator] ──create_agent──> Governor ✔ ──> registry: researcher.json
      │         ──create_agent──> Governor ✔ ──> registry: writer.json
      │         ──run_agent(researcher, task)──> result
      │         ──run_agent(writer, task + result)──> draft
      ▼
  final answer + reusable agents + audit log
```

## The rules that make this safe (enforced in code, see lesson 07)
- New agents only get tools from the **toolbox**, and only tools their **creator holds** (no privilege escalation).
- Max number of agents per run; max **depth** (agents creating agents creating agents...).
- Budget cap, kill switch, audit log. All automatic.

## Say this to Claude Code
> Run lesson 6a with the goal "Turn customer complaint emails into a categorised summary with suggested replies". Show me the agent spec it designed and explain each part.

> Open agent_registry/ and explain the JSON file of the agent that was just created.

> Run lesson 6b with the goal "Create a one-page onboarding guide for new staff about using AI tools safely, plus a 5-question quiz". Then tell me: which agents did the orchestrator hire, and why?

> Open the latest file in logs/ and walk me through what the orchestrator did, step by step.

> Use lesson 6c to improve the agent <name> so that it always ends with a list of open questions.

> Read prompts/system/orchestrator.md and suggest 2 improvements. Apply the better one and rerun 6b.

## Run it
```
python run.py 6a "what the new agent should do"
python run.py 6b "a goal for the meta-agent"
python run.py 6c                      # list saved agents
python run.py 6c run NAME "task"      # reuse one
python run.py 6c improve NAME "what to improve"
```
Works offline (`LLM_PROVIDER=mock`) to watch the mechanics; use a Gemini key for real results.

## Key files
- `common/spec.py`: the AgentSpec (the "job description" format)
- `common/foundry.py`: `design_agent`, `register`, `run`, `meta_tools` (read this one!)
- `prompts/system/agent_architect.md` and `orchestrator.md`: change behaviour by editing text

## Takeaways
1. Agents building agents = an agent writing **AgentSpecs** + code that turns specs into running agents.
2. The creating agent decides *what* to build; your code decides *whether it's allowed*.
3. Saved agents become a reusable workforce, versioned and auditable.

**Exercises:** E6.1-E6.10
