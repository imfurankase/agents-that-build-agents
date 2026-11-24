---
name: build-team
description: Design a small team of specialist subagents for a goal, run them, and report. The "agents that build agents" workflow inside Claude Code.
argument-hint: "<goal in plain English>"
disable-model-invocation: true
---

# Build a team of agents for this goal

**Goal:** $ARGUMENTS

Follow these steps exactly. Keep the user informed with one short line per step.

1. **Design.** Use the `agent-architect` subagent to design 2-3 specialist subagents for the goal (least privilege; clear descriptions). Name them `team-<short-goal>-<role>` and save them in `.claude/agents/`.
2. **Review.** Use the `safety-reviewer` subagent on each new file. Apply any HIGH-risk fixes before continuing.
3. **Approve.** Show the user a table: agent | what it does | tools | risk rating. Ask: "Run the team now? (yes/no)". Stop and wait for the answer.
4. **Run.** If yes: delegate the work to the new subagents (in parallel where the tasks are independent). Save deliverables under `workspace/teams/<short-goal>/`.
5. **Check.** Review the combined result against the goal. If something important is missing, send ONE round of specific feedback to the relevant subagent.
6. **Report.** Give: a 3-line summary, the deliverable's location, what each agent did, and anything that went wrong.
7. **Tidy up.** Ask whether to KEEP the new agents (they stay in `.claude/agents/` for reuse) or DELETE them.

Limits: at most 3 new agents, at most one feedback round, no `Bash` tool for the new agents unless the user explicitly asks.
