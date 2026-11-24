"""Pattern 5 - EVALUATOR-OPTIMIZER (writer and critic loop).

Run it:  python lessons/05_multi_agent_patterns/p5_evaluator_optimizer.py "what to write"

   [writer] -> draft -> [judge] -> pass? -> done
       ^                   |
       └---- feedback -----┘   (at most MAX_ROUNDS times)

When to use: there are clear quality criteria and revising actually helps.
Why it works: a separate judge with a strict rubric catches what the writer missed.
Control: MAX_ROUNDS stops endless polishing (and endless spending).
"""
import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))

from common import show
from common.foundry import load_prompt
from common.llm import get_llm

request = " ".join(sys.argv[1:]) or (
    "A 120-word announcement telling staff that a new AI assistant pilot starts Monday.")
CRITERIA = [
    "Under 130 words",
    "Says who can join and how to sign up",
    "Mentions one data-safety rule staff must follow",
    "Friendly, plain-English tone with no jargon",
]
JUDGE_SCHEMA = {
    "type": "object",
    "properties": {"score": {"type": "integer"}, "passed": {"type": "boolean"},
                   "feedback": {"type": "array", "items": {"type": "string"}}},
    "required": ["score", "passed", "feedback"],
    "additionalProperties": False,
}
MAX_ROUNDS = 3

writer, judge = get_llm(worker=True), get_llm()
show.title(f"EVALUATOR-OPTIMIZER - writer {writer.model}, judge {judge.model}")

draft, _ = writer.complete("You write internal announcements.", request, effort="low")
for round_number in range(1, MAX_ROUNDS + 1):
    show.panel(draft, f"Draft, round {round_number}")
    verdict_text, _ = judge.complete(
        load_prompt("judge"),
        "<criteria>\n" + "\n".join(f"- {c}" for c in CRITERIA) + f"\n</criteria>\n<work>\n{draft}\n</work>",
        json_schema=JUDGE_SCHEMA, effort="medium")
    verdict = json.loads(verdict_text)
    show.event("[judge]", f"score {verdict['score']}/10, passed={verdict['passed']}",
               "green" if verdict["passed"] else "red")
    if verdict["passed"]:
        break
    feedback = "\n".join(f"- {f}" for f in verdict["feedback"])
    show.info(f"feedback:\n{feedback}")
    draft, _ = writer.complete("You write internal announcements. Apply ALL feedback.",
                               f"Request: {request}\n\nYour draft:\n{draft}\n\nFeedback:\n{feedback}",
                               effort="low")
else:
    show.info("Reached MAX_ROUNDS - a human should review the last draft.")
