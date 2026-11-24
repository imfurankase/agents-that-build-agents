"""Lesson 04b - An AI agent from scratch, in about 70 lines (Claude API).

Run it:     python lessons/04_agent_loop/mini_agent_claude.py
Needs:      ANTHROPIC_API_KEY in .env

Same loop as mini_agent_gemini.py, written for Claude. Compare the two files
side by side: the shapes differ, the idea is identical.
"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))

import anthropic

from common import config
from common.toolbox import TOOLBOX

TOOL_NAMES = ["calculator", "save_note", "read_notes"]
MAX_TURNS = 8

GOAL = ("Our team of 12 is going to a 3-day training. Hotel: $95 per person per night "
        "for 2 nights. Meals: $40 per person per day. Venue: $1,200 in total. "
        "Calculate the total budget, save it as a note titled 'workshop budget' with a "
        "one-line breakdown, then tell me the total.")

client = anthropic.Anthropic()
tools = [{"name": n, "description": TOOLBOX[n].description,
          "input_schema": TOOLBOX[n].parameters} for n in TOOL_NAMES]
messages = [{"role": "user", "content": GOAL}]

for turn in range(1, MAX_TURNS + 1):
    response = client.beta.messages.create(
        model=config.CLAUDE_MODEL, max_tokens=16000,
        system="You are a careful budget assistant. Use the calculator for all math.",
        tools=tools, messages=messages, output_config={"effort": "medium"},
        betas=["server-side-fallback-2026-07-01"], fallbacks="default",
    )
    messages.append({"role": "assistant", "content": response.content})  # remember it all

    if response.stop_reason == "refusal":
        print("Claude declined the request.")
        break
    tool_requests = [b for b in response.content if b.type == "tool_use"]
    if not tool_requests:                                    # no tool requests -> done
        answer = "".join(b.text for b in response.content if b.type == "text")
        print(f"\n✅ FINAL ANSWER (turn {turn}):\n{answer}")
        break

    results = []
    for request in tool_requests:                            # run each requested tool
        output = TOOLBOX[request.name].run(request.input)
        print(f"turn {turn}: 🔧 {request.name}({request.input}) -> {output}")
        results.append({"type": "tool_result", "tool_use_id": request.id, "content": output})
    messages.append({"role": "user", "content": results})    # all results in ONE message
else:
    print("⛔ Stopped: reached MAX_TURNS.")
