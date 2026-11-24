"""Lesson 07b - The same meta-agent as lesson 06, now under a STRICT policy.

Run it:  python lessons/07_controlling_agents/strict_meta_agent.py "your goal"

Compare with lesson 06b. The differences are ONLY in the Policy below:
  - a human approves every new agent before it exists
  - medium AND high risk tools need a human yes
  - small budget, small team, no grandchildren
  - the orchestrator can only hand out a short list of tools

Try saying "no" to one of the agents it proposes and watch how it adapts.
Then open the audit log it prints at the end.
"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))

from common import show
from common.foundry import AgentFoundry
from common.governor import Governor, Policy

goal = " ".join(sys.argv[1:]) or (
    "Draft a short internal FAQ (5 questions) about our new AI assistant pilot "
    "and save it to reports/ai_pilot_faq.md")

policy = Policy(
    max_usd=0.50,
    max_agents=3,
    max_depth=1,
    approve_new_agents=True,
    approval_for_risk={"medium", "high"},
    allowed_tools={"save_note", "read_notes", "write_file", "calculator", "spawn_agents"},
)
foundry = AgentFoundry(governor=Governor(policy))

show.title("Strictly governed meta-agent")
result = foundry.run_orchestrator(goal, delegable_tools=["save_note", "read_notes", "write_file"])
show.panel(result.text, f"Final answer ({result.stopped_reason})", "cyan")
show.info(foundry.governor.summary())
