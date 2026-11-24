"""Lesson 12 - CAPSTONE: the Agent Foundry runs a whole mission.

Run it:  python lessons/12_capstone_agent_foundry/mission.py "your goal"
         add --yes to skip the approval question

Everything from the course, in one flow:

  1. PLAN     - a planner agent designs a team (agents + steps + success criteria)
  2. APPROVE  - you review the team before anyone is hired
  3. HIRE     - every agent passes the Governor and is saved to agent_registry/
  4. EXECUTE  - agents work step by step, sharing a team notebook
  5. JUDGE    - an independent judge grades the result against the criteria
  6. IMPROVE  - if it fails, the last agent revises once with the judge's feedback
  7. REPORT   - mission record saved to workspace/missions/, audit log in logs/
"""
import datetime
import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))

from pydantic import ValidationError

from common import config, show
from common.foundry import AgentFoundry
from common.governor import Governor, Policy
from common.spec import AgentSpec

args = [a for a in sys.argv[1:] if not a.startswith("--")]
goal = " ".join(args) or (
    "Produce a 1-page 'AI agents readiness checklist' for department heads: what to check "
    "before letting AI agents act on their team's data, with a short rationale per item.")
auto_yes = "--yes" in sys.argv

policy = Policy(max_usd=2.00, max_agents=5, max_depth=1, approval_for_risk={"high"})
foundry = AgentFoundry(governor=Governor(policy))
stamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")

# Fresh notebook for this mission (the old one is archived, not deleted).
notebook = config.WORKSPACE / "team_notes.md"
if notebook.exists():
    notebook.replace(config.WORKSPACE / f"team_notes-before-{stamp}.md")

# 1. PLAN -----------------------------------------------------------------
show.title("1. PLAN - designing the team")
plan = foundry.plan_team(goal)
show.panel(plan["summary"], "Plan")
for a in plan["agents"]:
    show.event(f"  agent {a['name']}", f"- {a['role']} | tools: {a['tools']}", "cyan")
for i, s in enumerate(plan["steps"], 1):
    show.event(f"  step {i}", f"{s['agent']}: {s['task'][:110]}", "white")
show.panel("\n".join(f"- {c}" for c in plan["success_criteria"]), "Success criteria", "yellow")

# 2. APPROVE --------------------------------------------------------------
if not auto_yes and input("\nApprove this team and start? (yes/no): ").strip().lower() not in ("y", "yes"):
    sys.exit("Mission cancelled before any agent was hired.")

# 3. HIRE -----------------------------------------------------------------
show.title("3. HIRE")
hired = set()
for data in plan["agents"]:
    try:
        spec = AgentSpec(**data, created_by="team-planner")
    except ValidationError as exc:
        show.event("  skipped", f"{data.get('name')}: {exc.errors()[0]['msg']}", "red")
        continue
    ok, _ = foundry.register(spec)
    if ok:
        hired.add(spec.name)

# 4. EXECUTE --------------------------------------------------------------
show.title("4. EXECUTE")
outputs = []
steps = plan["steps"]
for i, step in enumerate(steps, 1):
    if step["agent"] not in hired:
        show.event(f"  step {i}", f"skipped - '{step['agent']}' was not hired", "red")
        continue
    task = (f"OVERALL GOAL: {goal}\n\nYOUR STEP ({i} of {len(steps)}): {step['task']}\n\n"
            f"If you have read_notes, read the team notebook first for earlier results. "
            f"If you have save_note, save your result as a note titled 'step {i}: {step['agent']}'.")
    result = foundry.run(step["agent"], task)
    outputs.append({"step": i, "agent": step["agent"], "stopped": result.stopped_reason,
                    "text": result.text})
    if result.stopped_reason in ("budget", "turn limit reached") or result.stopped_reason.startswith("killed"):
        show.event("  mission", f"halted by the Governor: {result.stopped_reason}", "red")
        break

report_file = config.WORKSPACE / "reports" / "final_report.md"
final = (report_file.read_text(encoding="utf-8") if report_file.exists()
         else (outputs[-1]["text"] if outputs else "(no output)"))

# 5. JUDGE & 6. IMPROVE ----------------------------------------------------
show.title("5. JUDGE")
verdict = foundry.judge(final, plan["success_criteria"])
show.event("  judge", f"score {verdict['score']}/10 - {'PASS' if verdict['passed'] else 'FAIL'}",
           "green" if verdict["passed"] else "red")
if not verdict["passed"] and outputs:
    show.title("6. IMPROVE - one revision with the judge's feedback")
    last_agent = outputs[-1]["agent"]
    feedback = "\n".join(f"- {f}" for f in verdict["feedback"])
    revised = foundry.run(last_agent, f"OVERALL GOAL: {goal}\n\nRevise this work using the "
                                      f"reviewer's feedback.\n\nWORK:\n{final}\n\nFEEDBACK:\n{feedback}")
    final = (report_file.read_text(encoding="utf-8") if report_file.exists() else revised.text)
    verdict = foundry.judge(final, plan["success_criteria"])
    show.event("  judge", f"after revision: {verdict['score']}/10 - "
                          f"{'PASS' if verdict['passed'] else 'FAIL'}", "green" if verdict["passed"] else "red")

# 7. REPORT ---------------------------------------------------------------
show.title("7. REPORT")
show.panel(final[:3000], "Final deliverable", "cyan")
missions = config.WORKSPACE / "missions"
missions.mkdir(exist_ok=True)
record = missions / f"mission-{stamp}.json"
record.write_text(json.dumps({"goal": goal, "plan": plan, "outputs": outputs, "verdict": verdict,
                              "final": final, "governor": foundry.governor.summary()},
                             indent=2, ensure_ascii=False), encoding="utf-8")
show.info(foundry.governor.summary())
show.info(f"Mission record: {config.rel(record)}")
