"""Lesson 03a - Giving Gemini "hands": tools (also called function calling).

Run it:     python lessons/03_tools/gemini_tools.py
Needs:      GOOGLE_API_KEY in .env (free tier works)

What to notice:
- A tool is just a normal Python function with a good docstring.
  The docstring is what the model reads to decide WHEN to use the tool.
- We never tell the model which tool to call. It decides by itself.
- The SDK runs the tools for us here ("automatic function calling").
  In lesson 04 you will see the loop that hides behind this.
"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))

from google import genai
from google.genai import types

from common import config

# A tiny fictional staff directory (fake data for practice).
DIRECTORY = {
    "finance": {"lead": "A. Mugisha", "headcount": 18},
    "it": {"lead": "C. Uwase", "headcount": 26},
    "operations": {"lead": "J. Habimana", "headcount": 41},
}


def lookup_team(team_name: str) -> dict:
    """Look up a team in the staff directory. Returns its lead and headcount.

    Args:
        team_name: The team, e.g. "Finance", "IT" or "Operations".
    """
    print(f"   [tool called] lookup_team({team_name!r})")
    return DIRECTORY.get(team_name.strip().lower(), {"error": f"no team called {team_name}"})


def calculator(expression: str) -> str:
    """Calculate a simple math expression such as '18 + 26'.

    Args:
        expression: The math to calculate.
    """
    from common.toolbox import calculator as safe_calculator
    print(f"   [tool called] calculator({expression!r})")
    return safe_calculator(expression)


client = genai.Client()
question = ("How many people work in Finance and IT combined, "
            "and who leads the larger of the two teams?")
print(f"QUESTION: {question}\n")

response = client.models.generate_content(
    model=config.GEMINI_MODEL,
    contents=question,
    config=types.GenerateContentConfig(tools=[lookup_team, calculator]),
)
print(f"\nANSWER: {response.text}")
