---
name: run-lesson
description: Run one lesson of the course by its number (e.g. 4c, 6b, 12) and explain what happened.
argument-hint: "<lesson id, e.g. 6b> [optional goal text]"
disable-model-invocation: true
---

# Run lesson $ARGUMENTS

1. Run `python run.py` with no arguments first if you need the menu of lesson ids.
2. Read the README of that lesson folder (`lessons/NN_*/README.md`) so you can explain it.
3. Tell the user in one line what the lesson will do and whether it calls a paid model (check `python scripts/check_setup.py` output if unsure which provider is active).
4. Run: `python run.py $ARGUMENTS` (use `.venv\Scripts\python.exe` on Windows, `.venv/bin/python` on Mac if a .venv folder exists). If the script asks a yes/no question, tell the user and let them decide - do not answer for them.
5. Explain the output in plain English: what the agents did, any Governor decisions, cost, and where files/logs were saved.
6. Suggest the matching exercise from `exercises/EXERCISES.md`.
