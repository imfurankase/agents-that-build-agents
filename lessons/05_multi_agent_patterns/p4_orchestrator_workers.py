"""Pattern 4 - ORCHESTRATOR + WORKERS (manager and team).

Run it:  python lessons/05_multi_agent_patterns/p4_orchestrator_workers.py "a goal"

   [orchestrator] decides the sub-tasks AT RUN TIME
        ├-> [worker 1]
        ├-> [worker 2]     (as many as the goal needs)
        └-> [worker N]
   [synthesizer] combines the results

When to use: you cannot know the sub-tasks in advance.
This is the bridge to lesson 06: here the workers are generic. In lesson 06
the orchestrator also WRITES each worker's job description (creates agents).
"""
import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))

from common import show
from common.llm import get_llm

goal = " ".join(sys.argv[1:]) or (
    "Prepare a one-page briefing on how a government agency could start using AI agents safely.")

PLAN_SCHEMA = {
    "type": "object",
    "properties": {
        "subtasks": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {"title": {"type": "string"}, "instructions": {"type": "string"}},
                "required": ["title", "instructions"],
                "additionalProperties": False,
            },
        }
    },
    "required": ["subtasks"],
    "additionalProperties": False,
}

boss = get_llm()                 # main model plans and synthesizes
worker = get_llm(worker=True)    # worker model does the pieces
show.title(f"ORCHESTRATOR-WORKERS - {boss.name}/{boss.model}")

plan_text, _ = boss.complete(
    "You are a project lead. Split the goal into 2-4 independent sub-tasks. Each "
    "sub-task's instructions must be self-contained and say what to return.",
    goal, json_schema=PLAN_SCHEMA, effort="medium")
subtasks = json.loads(plan_text)["subtasks"][:4]   # code-enforced limit: max 4 workers
for i, task in enumerate(subtasks, 1):
    show.event(f"[orchestrator] task {i}:", task["title"], "yellow")

results = []
for task in subtasks:
    text, _ = worker.complete("You are a diligent analyst. Be concise and concrete.",
                              task["instructions"], effort="low")
    results.append(f"## {task['title']}\n{text}")
    show.panel(text, f"worker: {task['title']}")

final, _ = boss.complete("Combine the sections into one coherent one-page briefing with a "
                         "3-line executive summary at the top.",
                         f"Goal: {goal}\n\n" + "\n\n".join(results), effort="medium")
show.panel(final, "Final briefing", "cyan")
