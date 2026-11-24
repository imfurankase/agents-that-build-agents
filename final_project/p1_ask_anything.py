"""Final project · Milestone 1 - Real-world tools from FREE public APIs.

Run it:  python final_project/p1_ask_anything.py "your question"
Example: python final_project/p1_ask_anything.py "Will I need an umbrella in Nairobi tomorrow, and how much is 250 USD in EUR?"

The agent gets 5 tools: get_weather, get_public_holidays, convert_currency,
wikipedia_summary and calculator. None of them needs an account or a key.
Watch which tools it chooses for your question - and in what order.
"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

from common import show
from common.governor import Governor, Policy
from common.llm import get_llm
from common.toolbox import tools_by_name

question = " ".join(sys.argv[1:]) or (
    "What's the weather in Paris for the next 3 days, when is the next public holiday in "
    "France, and how much is 100 USD in EUR?")

llm = get_llm()
show.title(f"Ask anything - {llm.name}/{llm.model}")
show.panel(question, "Question")
result = llm.run_agent(
    name="ask-anything",
    system=("You answer practical questions using your tools for any facts (weather, holidays, "
            "money, encyclopedia). Answer in at most 8 short lines, and say which tool each fact "
            "came from."),
    task=question,
    tools=tools_by_name(["get_weather", "get_public_holidays", "convert_currency",
                         "wikipedia_summary", "calculator"]),
    max_turns=8,
    hooks=Governor(Policy(max_usd=0.30)),
)
show.panel(result.text, f"Answer ({result.stopped_reason}, {result.turns} turns)", "cyan")
