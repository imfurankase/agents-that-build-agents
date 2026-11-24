"""Lesson 10 - An MCP server that lets Claude Code manage YOUR Python agents.

MCP (Model Context Protocol) is the standard plug that connects AI apps to
tools and data. This server exposes the course's agent registry as tools, so
from VS Code you can say things like:

    "List my registered agents"
    "Create an agent called meeting-scribe that turns notes into action items"
    "Run the meeting-scribe agent on workspace/notes.txt"

Register it with Claude Code ONCE (run in the repo folder, in a terminal):
    claude mcp add agent-registry -- .venv\\Scripts\\python.exe lessons\\10_mcp\\agent_registry_server.py
Then in the Claude Code panel type /mcp to check it is connected.

Or just ask Claude Code: "Register the MCP server in lessons/10_mcp for this project."

Rules this server enforces (Claude Code cannot override them):
  - new agents are validated and checked by a strict Governor
  - no agent created here may hold run_python (high risk)
  - running an agent has a small budget, and risky tools are auto-declined
    (there is no human at a keyboard inside an MCP server)

IMPORTANT for MCP servers: never print() to stdout - it would corrupt the
protocol messages. That is why everything here runs with verbose=False.
"""
import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))

from mcp.server.mcpserver import MCPServer
from pydantic import ValidationError

from common.foundry import AgentFoundry
from common.governor import Governor, Policy
from common.registry import AgentRegistry
from common.spec import AgentSpec
from common.toolbox import TOOLBOX, read_notes

MCP_TOOL_CEILING = {name for name, tool in TOOLBOX.items() if tool.risk != "high"}

mcp = MCPServer(
    "agent-registry",
    instructions=("Manage the AI agents saved in this course's agent_registry/ folder: list, "
                  "inspect, create, run and retire them. Agents are JSON specs with a name, "
                  "role, instructions, tools and max_turns."),
)
registry = AgentRegistry()


def _strict_governor() -> Governor:
    return Governor(Policy(max_usd=0.25, max_agents=1, max_depth=0,
                           allowed_tools=set(MCP_TOOL_CEILING),
                           approval_for_risk={"high"}, auto_answer="no"), verbose=False)


@mcp.tool()
def list_agents() -> str:
    """List all registered agents with their role and tools."""
    return registry.summary()


@mcp.tool()
def get_agent(name: str) -> str:
    """Show the full spec (including instructions) of one registered agent."""
    spec = registry.get(name)
    return json.dumps(spec.model_dump(), indent=2) if spec else f"No agent named '{name}'."


@mcp.tool()
def available_tools() -> str:
    """List the tools a new agent may be given through this server."""
    return "\n".join(f"- {n} (risk: {TOOLBOX[n].risk}): {TOOLBOX[n].description}"
                     for n in sorted(MCP_TOOL_CEILING))


@mcp.tool()
def create_agent(name: str, role: str, instructions: str, tools: list[str],
                 max_turns: int = 6) -> str:
    """Create and save a new agent. Give it the fewest tools it needs.

    Args:
        name: lowercase-with-dashes, e.g. "meeting-scribe"
        role: one sentence describing what it is for
        instructions: its full system prompt, written to the agent ("You are...")
        tools: tool names from available_tools
        max_turns: how many steps it may take (1-25, usually 3-8)
    """
    try:
        spec = AgentSpec(name=name, role=role, instructions=instructions, tools=tools,
                         max_turns=max_turns, created_by="claude-code (mcp)")
    except ValidationError as exc:
        return f"Invalid agent: {exc.errors()[0]['msg']}"
    ok, reason = _strict_governor().approve_new_agent(spec, depth=0, parent_tools=None)
    if not ok:
        return f"Refused by the Governor: {reason}"
    path = registry.save(spec)
    return f"Saved agent '{spec.name}' to {path.name}."


@mcp.tool()
def run_agent(name: str, task: str) -> str:
    """Run a registered agent on a task (small budget; risky tools auto-declined)."""
    foundry = AgentFoundry(governor=_strict_governor(), registry=registry, verbose=False)
    try:
        result = foundry.run(name, task, depth=0)
    except (ValueError, PermissionError) as exc:
        return f"Could not run: {exc}"
    return (f"[{name}: {result.stopped_reason} after {result.turns} turns; "
            f"{foundry.governor.summary()}]\n\n{result.text}")


@mcp.tool()
def retire_agent(name: str) -> str:
    """Retire an agent (moved to agent_registry/retired/, not deleted)."""
    return f"Retired '{name}'." if registry.retire(name) else f"No agent named '{name}'."


@mcp.tool()
def read_team_notebook() -> str:
    """Read the shared notebook that agents write to (workspace/team_notes.md)."""
    return read_notes()


if __name__ == "__main__":
    mcp.run()  # stdio transport: Claude Code starts this process and talks to it
