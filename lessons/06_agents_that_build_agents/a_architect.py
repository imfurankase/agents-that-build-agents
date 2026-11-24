"""Lesson 06a - The Architect: an AI designs a brand-new agent from one sentence.

Run it:  python lessons/06_agents_that_build_agents/a_architect.py "what the agent should do"
Example: python lessons/06_agents_that_build_agents/a_architect.py "Turn long meeting notes into decisions, owners and deadlines"

What happens:
  1. The architect (an LLM) writes an AgentSpec: name, role, instructions, tools, limits.
  2. YOU review it (the human stays in charge).
  3. The Governor checks it; the registry saves it to agent_registry/<name>.json
  4. The new agent runs a first test task.

Open agent_registry/ afterwards: the new agent is a file you can read, edit and reuse.
"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))

from common import show
from common.foundry import AgentFoundry

goal = " ".join(a for a in sys.argv[1:] if a != "--yes") or (
    "Turn long meeting notes into a list of decisions, owners and deadlines")
auto_yes = "--yes" in sys.argv

foundry = AgentFoundry()
show.title("Step 1 - the Architect designs an agent")
spec = foundry.design_agent(goal)
show.panel(
    f"name:      {spec.name}\nrole:      {spec.role}\ntools:     {spec.tools or 'none'}\n"
    f"max_turns: {spec.max_turns}\n\ninstructions:\n{spec.instructions}",
    "Proposed agent spec", "cyan")

show.title("Step 2 - human review")
if not auto_yes and input("Hire this agent? (yes/no): ").strip().lower() not in ("y", "yes"):
    sys.exit("Not hired. Tip: rerun with a more specific goal.")

ok, reason = foundry.register(spec)
if not ok:
    sys.exit(f"The Governor refused: {reason}")

show.title("Step 3 - first test run")
test_task = (input("Give it a first task (or press Enter for a default):\n> ").strip()
             if not auto_yes else "")
test_task = test_task or (
    "Here are meeting notes: 'Ana will draft the AI policy by Friday. We agreed to pilot the "
    "assistant with 10 staff. Ben checks the licence cost before the 15th. Training is still "
    "undecided.' Do your job on these notes.")
result = foundry.run(spec.name, test_task)
show.panel(result.text, f"{spec.name} says ({result.stopped_reason})")
show.info(foundry.governor.summary())
