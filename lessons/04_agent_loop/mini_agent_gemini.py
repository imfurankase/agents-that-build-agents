"""Lesson 04a - An AI agent from scratch, in about 60 lines (Gemini, free tier).

Run it:     python lessons/04_agent_loop/mini_agent_gemini.py
Needs:      GOOGLE_API_KEY in .env

THE AGENT LOOP - the one idea behind every AI agent:

    while not finished:
        1. send the conversation + the list of tools to the model
        2. if the model asks for tools -> run them, add results to the conversation
        3. if the model just answers  -> finished

What to notice:
- MAX_TURNS is a safety limit. Without it, a confused agent could loop forever.
- The agent decides the ORDER of tool calls itself. We only give it a goal.
"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))

from google import genai
from google.genai import types

from common import config
from common.toolbox import calculator, read_notes, save_note

TOOLS = {"calculator": calculator, "save_note": save_note, "read_notes": read_notes}
MAX_TURNS = 8

GOAL = ("Our team of 12 is going to a 3-day training. Hotel: $95 per person per night "
        "for 2 nights. Meals: $40 per person per day. Venue: $1,200 in total. "
        "Calculate the total budget, save it as a note titled 'workshop budget' with a "
        "one-line breakdown, then tell me the total.")

client = genai.Client()
settings = types.GenerateContentConfig(
    system_instruction="You are a careful budget assistant. Use the calculator for all math.",
    tools=list(TOOLS.values()),
    # Turn OFF automatic tool running: we run the loop ourselves to see it.
    automatic_function_calling=types.AutomaticFunctionCallingConfig(disable=True),
)
conversation = [types.Content(role="user", parts=[types.Part.from_text(text=GOAL)])]

for turn in range(1, MAX_TURNS + 1):
    response = client.models.generate_content(model=config.GEMINI_MODEL,
                                              contents=conversation, config=settings)
    conversation.append(response.candidates[0].content)     # remember what the model said

    if not response.function_calls:                          # no tool requests -> done
        print(f"\n✅ FINAL ANSWER (turn {turn}):\n{response.text}")
        break

    results = []
    for call in response.function_calls:                     # run each requested tool
        output = TOOLS[call.name](**dict(call.args or {}))
        print(f"turn {turn}: 🔧 {call.name}({dict(call.args or {})}) -> {output}")
        results.append(types.Part(function_response=types.FunctionResponse(
            id=call.id, name=call.name, response={"result": output})))
    conversation.append(types.Content(role="user", parts=results))  # give results back
else:
    print("⛔ Stopped: reached MAX_TURNS.")
