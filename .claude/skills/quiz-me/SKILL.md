---
name: quiz-me
description: Quiz the user on a lesson or topic of this course, one question at a time.
argument-hint: "<lesson number or topic, e.g. 07 or 'prompt injection'>"
disable-model-invocation: true
---

Use the `lesson-tutor` subagent's approach to quiz me on: **$ARGUMENTS**

- Read the relevant lesson README first.
- Ask 5 questions, ONE at a time, mixing: one definition, two "what would happen if...", one "which pattern fits this scenario", one "spot the risk in this agent".
- After each answer: say what was right, add what was missing, then ask the next question.
- At the end: a score out of 5 and the one idea to review.
