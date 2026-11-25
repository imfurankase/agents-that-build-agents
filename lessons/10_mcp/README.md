# Lesson 10: MCP, plugging agents into tools and data

**Goal:** connect Claude Code to your own tools with the Model Context Protocol, and let it manage your Python agents.

## The big idea
**MCP is the "USB port" for AI.** One standard way for an AI app (Claude Code, Claude Desktop, ADK, many others) to discover and call tools from a *server*. Write a tool once as an MCP server, and any MCP-capable agent can use it.

```
Claude Code ──MCP──> agent-registry server ──> agent_registry/*.json
                                           └─> Foundry + Governor (runs agents safely)
```

`agent_registry_server.py` exposes: `list_agents`, `get_agent`, `available_tools`, `create_agent`, `run_agent`, `retire_agent`, `read_team_notebook`. Now **Claude Code can create and run your Python agents**, still under a strict Governor (small budget, no high-risk tools, risky actions auto-declined).

## Connect it (once)
In a terminal in the repo folder:
```
# Windows
claude mcp add agent-registry -- .venv\Scripts\python.exe lessons\10_mcp\agent_registry_server.py
# Mac
claude mcp add agent-registry -- .venv/bin/python lessons/10_mcp/agent_registry_server.py
```
(or ask Claude Code: *"Register the MCP server in lessons/10_mcp for this project"*). Then type `/mcp` in the Claude Code panel. You should see **agent-registry: connected**.

## Say this to Claude Code
> Using the agent-registry MCP tools, list my agents and describe each one in one line.

> Using the agent-registry tools, create an agent "policy-qa" that answers questions about a policy document in workspace/policy.md using read_file only. Then run it with the question "Who approves new AI tools?"

> Try to create an agent with run_python through the MCP server. What does the Governor say, and why?

> Explain agent_registry_server.py in plain English. Why must an MCP server never use print()?

> Add a new MCP tool "agent_stats" that returns how many agents exist and how many were created by each creator.

## Good to know
- Popular ready-made MCP servers exist for GitHub, databases, browsers, Google Drive, Slack and more. Add them with `claude mcp add`, and give them the **least access** possible.
- **MCP Inspector** (`npx @modelcontextprotocol/inspector`) lets you click through a server's tools without any AI, which is handy for testing.
- Every MCP server you add is code that runs on your machine and tools your agent can call. Treat it like installing software: trusted sources only.

## Takeaways
1. MCP = a standard plug between agents and tools/data.
2. Your Python foundry is now a tool Claude Code can use: agents building agents across systems.
3. Controls stay in the server: the client (Claude Code) cannot override the Governor.

**Exercises:** E10.1-E10.6
