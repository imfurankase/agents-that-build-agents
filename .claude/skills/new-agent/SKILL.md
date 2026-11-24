---
name: new-agent
description: Create a new Claude Code subagent from a plain-English description, safety-review it, and show how to use it.
argument-hint: "<what the agent should do>"
disable-model-invocation: true
---

# Create a new agent

**The user wants an agent that:** $ARGUMENTS

1. Use the `agent-architect` subagent to design and write it to `.claude/agents/<name>.md`.
2. Use the `safety-reviewer` subagent to review the new file. If the rating is MEDIUM or HIGH, apply the suggested fixes and say what changed.
3. Show the user:
   - the file path (as a clickable link),
   - a plain-English summary of what the agent does and which tools it has (and why),
   - two example prompts to use it, e.g. "Use the <name> agent to ...".
4. Remind them they can change the agent by editing the Markdown file in plain English, or by asking: "Improve the <name> agent so that ...".
