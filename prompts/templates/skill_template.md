---
name: [command-name, e.g. weekly-brief]
description: [What this playbook does, in one sentence. Claude may use it automatically when this matches, unless disable-model-invocation is true.]
argument-hint: "[what to type after the command, e.g. <notes or file path>]"
disable-model-invocation: true   # true = only runs when YOU type /command-name
---

<!--
HOW TO USE THIS TEMPLATE
1. Save as .claude/skills/<command-name>/SKILL.md
2. $ARGUMENTS below is replaced by whatever you type after the command.
3. Run it in Claude Code: /<command-name> your text here
-->

# [Title of the playbook]

**Input:** $ARGUMENTS

1. [Step 1, e.g. "If no input was given, ask me for it and stop."]
2. [Step 2, e.g. "Use the researcher subagent to check any facts or numbers."]
3. [Step 3, e.g. "Write the result to workspace/briefs/<date>.md"]
4. [Ask for approval before anything irreversible: "Show me the draft and ask: save it? (yes/no)"]
5. [Report: "Tell me in 3 bullets what you did and where the file is."]

Limits: [e.g. at most 2 subagents, no Bash, under 400 words.]
