"""Lesson 09b - ADK agents built AT RUN TIME: from saved specs, and by a hiring tool.

Run it:  python lessons/09_google_adk/dynamic_team.py "your goal"
         python lessons/09_google_adk/dynamic_team.py --dry-run     (build only, no model calls)
Needs:   GOOGLE_API_KEY in .env (free tier works)

Two ways agents appear here, and neither is written in this file in advance:
  1. FROM DATA: every agent saved in agent_registry/ (lesson 06) is turned into
     an ADK agent. The same JSON spec now runs on Google's framework.
     -> agent specs are portable assets, not locked into one tool.
  2. BY AN AGENT: the lead agent has a hire_specialist tool. When it decides it
     needs a new expert, it writes the instructions and the tool creates that
     ADK agent on the spot and runs it. Hiring is capped by MAX_HIRES.
"""
import asyncio
import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))

from google.adk import Agent
from google.adk.runners import InMemoryRunner
from google.adk.tools.agent_tool import AgentTool

from common import config, show
from common.foundry import load_prompt
from common.registry import AgentRegistry
from common.spec import AgentSpec
from common.toolbox import TOOLBOX

MAX_SPECIALISTS_FROM_REGISTRY = 4
MAX_HIRES = 2
HOUSE_RULES = load_prompt("common_rules")


def adk_name(name: str) -> str:
    """ADK agent names must be Python identifiers: 'budget-analyst' -> 'budget_analyst'."""
    return re.sub(r"\W", "_", name).strip("_") or "agent"


def from_spec(spec: AgentSpec) -> Agent:
    """Turn one of OUR AgentSpecs into a Google ADK Agent."""
    return Agent(
        name=adk_name(spec.name),
        model=config.GEMINI_WORKER_MODEL,
        description=spec.role,
        instruction=spec.instructions + "\n\n" + HOUSE_RULES,
        tools=[TOOLBOX[t].fn for t in spec.tools if t in TOOLBOX and TOOLBOX[t].risk != "high"],
    )


def final_text(events) -> str:
    texts = []
    for event in events:
        if event.is_final_response() and event.content and event.content.parts:
            texts += [p.text for p in event.content.parts if getattr(p, "text", None)]
    return "\n".join(texts) or "(no text)"


hired: dict[str, str] = {}


async def hire_specialist(name: str, instructions: str, task: str) -> str:
    """Create a brand-new specialist agent on the spot and give it one task.

    Use this only when none of your existing specialists fits.

    Args:
        name: Short name for the specialist, e.g. "policy_checker".
        instructions: The specialist's full instructions (its system prompt).
        task: The complete, self-contained task for the specialist.
    """
    if len(hired) >= MAX_HIRES:
        return f"REFUSED: hiring limit reached ({MAX_HIRES}). Use existing specialists."
    specialist = Agent(name=adk_name(name), model=config.GEMINI_WORKER_MODEL,
                       instruction=instructions + "\n\n" + HOUSE_RULES)
    hired[name] = instructions
    show.event("[hire]", f"created specialist '{name}'", "green")
    runner = InMemoryRunner(agent=specialist, app_name="hired_specialist")
    events = await runner.run_debug(task, quiet=True)
    return final_text(events)


def build_lead() -> Agent:
    specs = AgentRegistry().list()[:MAX_SPECIALISTS_FROM_REGISTRY]
    specialists = [from_spec(s) for s in specs]
    show.panel("\n".join(f"- {a.name}: {a.description}" for a in specialists) or
               "(registry is empty - run lesson 06 first, or rely on hiring)",
               "Specialists loaded from agent_registry/")
    return Agent(
        name="lead",
        model=config.GEMINI_MODEL,
        instruction=(
            "You lead a team of specialists (available to you as tools). Break the goal into "
            "steps, use the best specialist for each step, and if no specialist fits, use "
            f"hire_specialist (at most {MAX_HIRES} hires). Finish with the final answer and a "
            "list of which specialists you used or hired."),
        tools=[AgentTool(agent=a) for a in specialists] + [hire_specialist],
    )


async def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    goal = " ".join(args) or ("Create a short checklist for a manager who wants to start "
                              "a safe pilot of AI assistants in their team.")
    lead = build_lead()
    if "--dry-run" in sys.argv:
        show.info(f"Dry run: built lead agent with {len(lead.tools)} tools. No model calls made.")
        return
    runner = InMemoryRunner(agent=lead, app_name="dynamic_team")
    events = await runner.run_debug(goal, quiet=True)
    show.panel(final_text(events), "Final answer", "cyan")
    if hired:
        show.panel("\n\n".join(f"{n}:\n{i[:400]}" for n, i in hired.items()),
                   "Specialists hired during this run", "yellow")


asyncio.run(main())
