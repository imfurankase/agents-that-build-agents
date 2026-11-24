# Lesson 02: Prompting, the master skill

**Goal:** write prompts that get excellent, reliable results from models, agents and Claude Code.

## The big idea
An agent *is* a prompt plus tools plus a loop. When an agent builds another agent, what it really writes is **a prompt**. So prompting is the skill everything else rests on, and it is the skill you will use most, because you build by prompting Claude Code.

## The 6-part prompt (memorise this)
1. **Role:** who the AI should be. *"You are a chief-of-staff briefing a director."*
2. **Context:** who it's for, why it matters, the material (inside `<document>` tags).
3. **Task:** one clear verb. *"Write a decision brief."*
4. **Format:** structure, length, tone. *"3 bullets, under 150 words."*
5. **Rules:** boundaries and what to do when unsure. *"Don't invent numbers; write 'unknown'."*
6. **Done when:** how to tell it's finished. *"…and it names the 3 decisions needed."*

The full guide is in [prompts/PROMPTING_GUIDE.md](../../prompts/PROMPTING_GUIDE.md), with 100+ ready prompts in [prompts/PROMPT_LIBRARY.md](../../prompts/PROMPT_LIBRARY.md).

## Say this to Claude Code
> Run lesson 2a. Then explain, part by part, why the strong prompt produced a better answer.

> Rewrite the STRONG_PROMPT in prompt_lab.py for a different audience: the IT security team. Run it again.

> Run lesson 2b with this rough prompt: "write something about our new AI policy for staff". Explain each change it made.

> Look at prompts/system/orchestrator.md. Which of the 6 parts does it contain? What is missing?

## Run it
```
python run.py 2a
python run.py 2b "your rough prompt"
```

## Prompting Claude Code (how you'll work every day)
Good requests to Claude Code have the same six parts:
> **Role/context:** "I'm new to Python; this repo is a course on agents."
> **Task:** "Add a new tool to common/toolbox.py that counts words in a workspace file."
> **Format/rules:** "Keep it under 20 lines, follow the style of the other tools, add a test."
> **Done when:** "The tests pass. Then explain what you changed in 3 bullets."

Use **Plan mode** (`/plan` or the mode switch) for anything bigger than a small change: Claude Code proposes a plan you approve before it edits anything.

## Takeaways
1. Specific beats long. Context beats commands. Examples beat adjectives.
2. Explain *why* behind a rule. Models follow reasons better than orders.
3. Structured output (JSON with a schema) turns an answer into something code can act on.
4. AI can improve prompts for AI (2b), the first step toward agents that build agents.

**Exercises:** E2.1-E2.10
