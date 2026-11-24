"""Lesson 03b - Giving Claude "hands": tool use with the Tool Runner.

Run it:     python lessons/03_tools/claude_tools.py
Needs:      ANTHROPIC_API_KEY in .env (API billing, not your subscription)

What to notice:
- `@beta_tool` turns a normal Python function into a tool. The docstring
  (including the Args section) becomes the description Claude reads.
- The Tool Runner repeats "Claude asks -> we run the tool -> Claude reads
  the result" until Claude is done. Each loop prints below.
"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))

import anthropic
from anthropic import beta_tool

from common import config
from common.toolbox import calculator as safe_calculator

DIRECTORY = {
    "finance": {"lead": "A. Mugisha", "headcount": 18},
    "it": {"lead": "C. Uwase", "headcount": 26},
    "operations": {"lead": "J. Habimana", "headcount": 41},
}


@beta_tool
def lookup_team(team_name: str) -> str:
    """Look up a team in the staff directory. Returns its lead and headcount.

    Args:
        team_name: The team, e.g. "Finance", "IT" or "Operations".
    """
    return str(DIRECTORY.get(team_name.strip().lower(), {"error": f"no team {team_name}"}))


@beta_tool
def calculator(expression: str) -> str:
    """Calculate a simple math expression such as '18 + 26'.

    Args:
        expression: The math to calculate.
    """
    return safe_calculator(expression)


client = anthropic.Anthropic()
question = ("How many people work in Finance and IT combined, "
            "and who leads the larger of the two teams?")
print(f"QUESTION: {question}\n")

runner = client.beta.messages.tool_runner(
    model=config.CLAUDE_MODEL,
    max_tokens=16000,
    tools=[lookup_team, calculator],
    messages=[{"role": "user", "content": question}],
    output_config={"effort": "medium"},
    betas=["server-side-fallback-2026-07-01"],
    fallbacks="default",
)

for turn, message in enumerate(runner, start=1):
    for block in message.content:
        if block.type == "tool_use":
            print(f"turn {turn}: Claude calls {block.name}({block.input})")
        elif block.type == "text" and block.text.strip():
            print(f"turn {turn}: Claude says: {block.text}")
