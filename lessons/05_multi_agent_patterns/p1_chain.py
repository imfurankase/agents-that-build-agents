"""Pattern 1 - CHAIN (assembly line): each step's output is the next step's input.

Run it:  python lessons/05_multi_agent_patterns/p1_chain.py "topic of your choice"

   [outline writer] -> [draft writer] -> [editor]

When to use: the task splits into fixed steps that always happen in the same order.
Why it works: each step is simple, so each prompt can be short and precise,
and you can check the work between steps (a "gate").
"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))

from common import show
from common.llm import get_llm

topic = " ".join(sys.argv[1:]) or "Why every team should keep a shared prompt library"
llm = get_llm(worker=True)
show.title(f"CHAIN pattern - {llm.name}/{llm.model}")

outline, _ = llm.complete("You write crisp outlines.",
                          f"Write a 4-point outline for a one-page memo on: {topic}", effort="low")
show.panel(outline, "Step 1: outline")

# A GATE: a simple code check between steps. Stop early if step 1 failed.
if len(outline.strip()) < 20:
    sys.exit("The outline looks empty - stopping the chain.")

draft, _ = llm.complete("You write clear memos for executives.",
                        f"Write the memo (max 250 words) from this outline:\n{outline}",
                        effort="low")
show.panel(draft, "Step 2: draft")

final, _ = llm.complete("You are a strict editor. Cut 20% of the words, keep every fact.",
                        f"Edit this memo:\n{draft}", effort="low")
show.panel(final, "Step 3: edited final", "cyan")
