---
name: explain
description: Explain a file, folder, error or concept from this course in plain English for a non-programmer.
argument-hint: "<file, folder, error message or concept>"
---

Use the `code-explainer` subagent to explain: **$ARGUMENTS**

If no argument was given, explain the file currently open or selected in the editor.
Keep it under ~250 words. Finish with one "Try this" prompt the user can paste into Claude Code.
