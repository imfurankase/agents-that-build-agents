# Lesson 01: Your first call to an AI model

**Goal:** see what "calling a model" really is: text in, text out, measured in tokens.

## The big idea
A large language model (LLM) is a function: you send it **instructions + a request**, it sends back **text**. It has **no memory** between calls; anything it should know must be in the request. Usage is counted in **tokens** (about ¾ of a word each), and tokens are what you pay for.

- **System prompt / system instruction:** *who* the model should be and how it should behave.
- **User message / contents:** *what* you want right now.
- **Context window:** how much text fits in one call (Claude: up to 1M tokens).

## Three ways to make the same call

| File | Uses | Needs |
|---|---|---|
| `hello_gemini.py` | Google's Gemini API | Free Google AI Studio key |
| `hello_claude_api.py` | Anthropic's Claude API | Anthropic API key (billed separately from Claude Pro/Max) |
| `hello_claude_code.py` | Claude Code CLI, from a script | Claude Code CLI + your subscription |

## Say this to Claude Code
> Run lesson 1a and explain each line of hello_gemini.py in plain English.

> Change the system instruction in hello_gemini.py so the answer is written for a 12-year-old, then run it again and compare.

> What is a token? Count roughly how many tokens the question in hello_gemini.py uses.

> Run lesson 1c and explain what "headless mode" means and why it is useful for agents.

## Run it
```
python run.py 1a     # Gemini
python run.py 1c     # Claude Code CLI (subscription)
python run.py 1b     # Claude API (only with an API key)
```

## What to look for
- The token counts printed at the end: input vs output.
- How changing only the **system instruction** changes the style of the answer.
- 1c reports an "API-equivalent cost". On a subscription you are not billed this, but it counts toward your plan's usage limits.

## No-code version (Google AI Studio)
Open [aistudio.google.com](https://aistudio.google.com) → **Create prompt**. Paste the system instruction into *System instructions* and the question into the chat box. Click **Get code** to see the same Python you have here.

## Takeaways
1. A model call = instructions + request → text. Nothing more.
2. The model forgets everything between calls. Agents add memory by re-sending the conversation.
3. Tokens = cost and limits. Long prompts cost more; caching and smaller models cost less.

**Exercises:** E1.1-E1.6 in [exercises/EXERCISES.md](../../exercises/EXERCISES.md)
