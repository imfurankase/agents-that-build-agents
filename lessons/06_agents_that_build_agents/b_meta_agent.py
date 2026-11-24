"""Lesson 06b - The Meta-Agent: a manager agent that hires and directs its own team.

Run it:  python lessons/06_agents_that_build_agents/b_meta_agent.py "your goal"
Example: python lessons/06_agents_that_build_agents/b_meta_agent.py "Write a one-page guide for staff on spotting phishing emails, then a 5-question quiz on it"

What happens (nobody scripts the team in advance):
  - The orchestrator gets the goal and 4 special tools:
        list_agents, create_agent, run_agent, retire_agent
  - It DECIDES which specialists it needs, WRITES their instructions,
    HIRES them (create_agent), GIVES them tasks (run_agent), checks their
    work, and writes the final answer.
  - Every hire goes through the Governor (limits on number, depth, tools, cost).

Watch the console, then open:
  agent_registry/      -> the agents it created (reusable!)
  workspace/           -> files and team notes they wrote
  logs/run-*.jsonl     -> the full audit trail
"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))

from common import show
from common.foundry import AgentFoundry
from common.governor import Governor, Policy

goal = " ".join(sys.argv[1:]) or (
    "Write a one-page guide for staff on spotting phishing emails, "
    "then a 5-question multiple-choice quiz based on the guide.")

# A friendly policy for learning. Lesson 07 shows a strict one.
policy = Policy(max_usd=1.00, max_agents=4, max_depth=1)
foundry = AgentFoundry(governor=Governor(policy))

show.title("The Meta-Agent at work")
show.panel(goal, "Goal")
result = foundry.run_orchestrator(goal)

show.panel(result.text, f"Final answer ({result.stopped_reason}, {result.turns} turns)", "cyan")
show.panel(foundry.registry.summary(), "Agents in the registry now")
show.info(foundry.governor.summary())
