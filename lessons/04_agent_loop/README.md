# Lesson 04: The agent loop

**Goal:** see the single loop that turns a model + tools into an **agent**.

## The big idea
```
goal ──> [ model ] ──wants a tool?──yes──> run tool ──> add result ──┐
             ^                                                       │
             └───────────────────────────────────────────────────────┘
                         no ──> final answer (done)
```
That's it. An **agent** is a model running in this loop, choosing its own next step, until it decides it is done, or until **you** stop it (max turns, budget, kill switch).

Workflow vs agent:
- **Workflow:** *you* decide the steps in code (lesson 05).
- **Agent:** *the model* decides the steps at run time (this lesson and beyond).

## Three versions of the same agent
| File | What it shows |
|---|---|
| `mini_agent_gemini.py` | The raw loop, ~60 lines, Gemini |
| `mini_agent_claude.py` | The same loop for Claude. Compare side by side! |
| `watch_the_loop.py` | The shared loop in `common/llm.py`, narrated turn by turn. Works offline. |

## Say this to Claude Code
> Run lesson 4c and narrate each turn of the loop to me like a sports commentator.

> Open common/llm.py, find run_agent, and explain the 5 numbered steps in plain English.

> In mini_agent_gemini.py, set MAX_TURNS to 1 and run it. What happens and why? Then put it back to 8.

> Compare mini_agent_gemini.py and mini_agent_claude.py and make me a table of the differences.

> Change the goal in watch_the_loop.py to plan a 2-day offsite for 8 people, and run it.

## Run it
```
python run.py 4c        # any provider, including free offline mock
python run.py 4a        # Gemini
python run.py 4b        # Claude API
```

## What to look for
- The **turn numbers**: one model call per turn.
- The model choosing tools in a sensible order *by itself*.
- `stopped_reason`: `done` (it finished) vs `max_turns` (we stopped it).

## Takeaways
1. Agent = model + tools + loop + a stopping rule.
2. The loop is where control lives: every turn and every tool call passes through *your* code.
3. Always cap the loop (`max_turns`). An uncapped agent is a runaway cost.

**Exercises:** E4.1-E4.6
