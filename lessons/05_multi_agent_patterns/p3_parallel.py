"""Pattern 3 - PARALLEL (panel of experts): several agents work at the same time.

Run it:  python lessons/05_multi_agent_patterns/p3_parallel.py "proposal to review"

   ┌-> [legal reviewer]   ┐
   ├-> [finance reviewer] ├-> [chair: combines the views]
   └-> [risk reviewer]    ┘

When to use: independent views of the same thing, or many independent items.
Why it works: it is faster (they run at once) and you get diverse perspectives.
"""
import pathlib
import sys
from concurrent.futures import ThreadPoolExecutor

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))

from common import show
from common.llm import get_llm

proposal = " ".join(sys.argv[1:]) or (
    "Proposal: give every employee an AI assistant with access to their email and "
    "shared drives, starting next month, at $30 per user per month.")

REVIEWERS = {
    "legal": "You are a legal and compliance reviewer. List the top 3 legal/privacy concerns.",
    "finance": "You are a finance reviewer. Assess cost, value and hidden costs in 3 bullets.",
    "risk": "You are a security risk reviewer. List the top 3 security risks and a mitigation each.",
}

llm = get_llm(worker=True)
show.title(f"PARALLEL pattern - {llm.name}/{llm.model}")


def review(item):
    role, system = item
    text, _ = llm.complete(system, f"Review this proposal:\n{proposal}", effort="low")
    return role, text


with ThreadPoolExecutor(max_workers=3) as pool:          # all three run at the same time
    reviews = dict(pool.map(review, REVIEWERS.items()))

for role, text in reviews.items():
    show.panel(text, f"{role} reviewer")

combined = "\n\n".join(f"## {role}\n{text}" for role, text in reviews.items())
verdict, _ = llm.complete(
    "You chair a review board. Combine the reviews into: Decision (go / no-go / go with "
    "conditions), top 3 conditions, and one sentence on the biggest disagreement.",
    combined, effort="medium")
show.panel(verdict, "Chair's combined verdict", "cyan")
