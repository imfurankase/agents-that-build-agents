---
name: stop-all
description: KILL SWITCH - freeze every agent in this project (Python agents and Claude Code tool use) by creating the STOP file.
disable-model-invocation: true
---

Create a file named `STOP` in the repository root containing the current date and time and the words "kill switch engaged".

Then tell the user:
- All Python agents will stop at their next step (the Governor checks for this file).
- The project's guard hook will block Claude Code from running commands, editing files or starting subagents while the file exists.
- To resume: delete the `STOP` file themselves in the VS Code file explorer. Claude Code cannot delete it while it exists - that is the point of a kill switch: only a human can turn it off.
