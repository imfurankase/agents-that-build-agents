# Lesson 12: Capstone, the Agent Foundry

**Goal:** run a complete, governed, self-organising mission: from one sentence to a judged deliverable, with every agent created on the fly.

## The flow
```
 goal
  │
  ▼
 1 PLAN     planner designs team: agents + steps + success criteria (structured JSON)
 2 APPROVE  you review the team before anyone is hired           ← human in the loop
 3 HIRE     each agent passes the Governor → saved to agent_registry/
 4 EXECUTE  agents work in order, sharing workspace/team_notes.md
 5 JUDGE    independent judge grades the result against the criteria
 6 IMPROVE  if it fails: one revision with the judge's feedback
 7 REPORT   workspace/missions/mission-*.json + logs/run-*.jsonl
```
Everything from lessons 02-11 in one place: prompting (planner/judge prompts), tools, the loop, patterns (orchestrator + evaluator), agents creating agents, governance, evals.

## Run it
```
python run.py 12 "your goal"
python run.py 12 "your goal" --yes     # skip the approval question
```
Good first goals:
- *"Produce a 1-page AI agents readiness checklist for department heads."*
- *"Create a staff guide to spotting phishing, plus a 5-question quiz and answer key."*
- *"Draft a 6-week rollout plan for AI assistants in a 50-person department, with risks and owners."*

## Say this to Claude Code
> Run the capstone with the goal "...". When it asks for approval, show me the plan as a table first and tell me if anything looks risky.

> After the mission, summarise the mission record in workspace/missions/ and the audit report (lesson 7c) for my leadership team in 10 lines.

> Improve prompts/system/team_planner.md so plans always include a fact-checking step. Run the same goal again and compare scores.

> Make the capstone run each mission twice with different planners (one "cautious", one "fast") and compare cost and score.

## Your capstone challenge
Pick a **real task from your own work** (a briefing, a policy draft, a training pack, an analysis). Then:
1. Run it through `mission.py` with a tight budget.
2. Review the hired agents with `/review-agent`. Keep the good ones.
3. Build an eval (lesson 11) for the best agent with 5 realistic cases.
4. Present: the result, the team that made it, cost, audit trail, and what you would need before trusting it in production.

**Exercises:** E12.1-E12.6
