"""Lesson 04c - Watch the agent loop step by step (works with ANY provider, even offline).

Run it:     python lessons/04_agent_loop/watch_the_loop.py
Offline:    set LLM_PROVIDER=mock in .env to practice for free

This uses the shared agent loop in common/llm.py (BaseProvider.run_agent).
A small "Hooks" object prints every turn and every tool call, so you can see
exactly what happens inside an agent. In lesson 07 the same hooks become the
Governor that can say NO.
"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))

from common import show
from common.llm import Hooks, get_llm
from common.toolbox import tools_by_name


class Narrator(Hooks):
    """Prints what the agent is doing. Changes nothing."""

    def before_turn(self, agent_name, turn):
        show.event(f"[turn {turn}]", f"{agent_name} is thinking...", "blue")

    def on_usage(self, agent_name, model, input_tokens, output_tokens):
        show.info(f"          model={model} read {input_tokens} tokens, wrote {output_tokens}")

    def before_tool(self, agent_name, tool, args):
        show.event("          🔧", f"{tool.name}({args})", "cyan")
        return None  # None = allowed

    def after_tool(self, agent_name, tool, args, result):
        show.info(f"          -> {result[:200]}")


llm = get_llm()
show.title(f"Watching an agent - provider: {llm.name}, model: {llm.model}")
result = llm.run_agent(
    name="budget-assistant",
    system="You are a careful budget assistant. Use the calculator for all math.",
    task=("Our team of 12 is going to a 3-day training. Hotel: $95 per person per night for "
          "2 nights. Meals: $40 per person per day. Venue: $1,200. Calculate the total, save "
          "it as a note titled 'workshop budget', then tell me the total."),
    tools=tools_by_name(["calculator", "save_note"]),
    max_turns=8,
    hooks=Narrator(),
)
show.panel(result.text, f"Final answer ({result.stopped_reason} after {result.turns} turns)")
