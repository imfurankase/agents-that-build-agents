# Template: a request to Claude Code (the 6 parts)

Fill in, paste into the Claude Code panel. For anything touching more than one file, switch to **Plan mode** first.

---

**Context:** [Who you are and what this is about, e.g. "I'm not a programmer. This repo is my agents course. I'm working on lesson 06."]

**Task:** [One clear goal with a verb, e.g. "Create a new Python agent that turns supplier emails into a table of dates and amounts."]

**Where:** [Files/folders to use or change, with @-mentions, e.g. "@common/toolbox.py and @lessons/06_agents_that_build_agents/"]

**Constraints:** [Scope and style, e.g. "Only change these files. Follow the style of the existing tools. Keep it under 30 lines. No new packages."]

**Done when:** [How we both know it worked, e.g. "You've run it on workspace/inbox/sample.txt, shown me the output, and the tests pass (python -m pytest -q)."]

**Then:** [What you want back, e.g. "Explain what you changed in 3 bullets, and suggest one exercise."]

---

### Filled-in example
> **Context:** I'm not a programmer; this is my agents course repo.
> **Task:** Add a tool called `word_count` that counts the words in a workspace file.
> **Where:** @common/toolbox.py
> **Constraints:** Low risk level; follow the style of `read_file`; must refuse paths outside workspace/.
> **Done when:** a test for it exists in tests/test_offline.py and all tests pass.
> **Then:** explain the change in 3 bullets, and show me how an agent would use the new tool.
