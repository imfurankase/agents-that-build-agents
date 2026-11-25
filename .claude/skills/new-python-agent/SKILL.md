---
name: new-python-agent
description: Create a new Python agent spec in agent_registry/ (for the Gemini/Claude API foundry in lessons 06-12), then test-run it.
argument-hint: "<what the agent should do>"
disable-model-invocation: true
---

# Create a Python agent for the Foundry

**Job:** $ARGUMENTS

1. Run the Architect lesson, which designs, validates and saves the spec:
   `python lessons/06_agents_that_build_agents/a_architect.py "$ARGUMENTS" --yes`
   (use `.venv\Scripts\python.exe` on Windows, `.venv/bin/python` on Mac if a .venv folder exists)
2. Open the new file in `agent_registry/` and explain it to the user in plain English: role, tools (and why), max_turns.
3. Ask the `safety-reviewer` subagent to review the JSON file. Report the rating.
4. Suggest one test command, e.g.
   `python lessons/06_agents_that_build_agents/c_reuse_agents.py run <name> "<a realistic task>"`
   and ask whether to run it now (it calls the model, so it may cost a little).
