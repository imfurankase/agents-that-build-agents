---
name: review-agent
description: Safety-review an agent definition (Claude Code subagent or Python agent spec) and suggest fixes.
argument-hint: "<agent name or file path>"
disable-model-invocation: true
---

Find the agent **$ARGUMENTS** in `.claude/agents/` or `agent_registry/`. Use the `safety-reviewer` subagent to review it. Show the rating and findings, then ask whether to apply the suggested fixes.
