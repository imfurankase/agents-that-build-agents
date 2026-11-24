# Lesson 07: Controlling agents (governance)

**Goal:** stay firmly in control when agents act, and especially when they create other agents.

## The big idea: control lives OUTSIDE the model
A prompt that says "don't overspend" is a *request*. A line of code that stops the loop at $1.00 is a *guarantee*. Every agent in this course runs through the **Governor** (`common/governor.py`), plain code the model cannot talk its way past.

## The 8 controls
| # | Control | What it prevents | Where |
|---|---|---|---|
| 1 | **Budget** (`max_usd`) | Runaway spending | `on_usage` |
| 2 | **Turn limit** | Infinite loops | `before_turn` |
| 3 | **Headcount** (`max_agents`) | Agent explosions | `approve_new_agent` |
| 4 | **Depth limit** (`max_depth`) | Agents → agents → agents... | `approve_new_agent` |
| 5 | **Tool ceiling** (`allowed_tools`) | Risky capabilities in a run | `approve_new_agent`, `run` |
| 6 | **No escalation** | A child getting more power than its parent | `approve_new_agent` |
| 7 | **Human approval** | Risky actions without a person's OK | `before_tool`, `approve_new_agent` |
| 8 | **Kill switch** (`STOP` file) | Everything, instantly | checked before every step |
| + | **Audit log** (`logs/run-*.jsonl`) | "What happened?" with no answer | every event |

The same ideas exist in Claude Code: **permissions** (allow/ask/deny), **hooks** (code that runs before every tool call, like `.claude/hooks/guard.py`), `--max-turns`, `--max-budget-usd`, and subagent `tools:` lists.

## Say this to Claude Code
> Run lesson 7a and explain each of the 8 demos in one sentence each, like a briefing for a board.

> Run the approval demo (python run.py 7a approval) and let me answer. Explain what happened.

> Run lesson 7b with the goal "Write a short FAQ about our AI pilot". I'll answer the approval questions myself. Afterwards, run 7c and explain the audit report.

> Make me a strict policy for a "production" setting and a relaxed one for "sandbox" experiments, as two Policy objects, and explain the differences.

> Type /stop-all, then try to run lesson 4c. What happens? (Then I'll delete the STOP file myself.)

> Show me logs/claude_code_audit.jsonl: what did you (Claude Code) do in this session?

## Run it
```
python run.py 7a                 # all demos (budget & killswitch run an agent: use mock to keep free)
python run.py 7a depth           # one demo
python run.py 7b "your goal"     # the strict meta-agent: you approve every hire
python run.py 7c                 # audit report of the last run
```

## Design principles for controlling agents that create agents
1. **Deny by default:** new agents start with no tools; add only what's justified.
2. **Inherit, never escalate:** you can't give what you don't have.
3. **Bound everything:** money, turns, headcount, depth, time.
4. **Humans approve the irreversible:** spending, sending, deleting, publishing, hiring.
5. **Log everything, review regularly:** autonomy without audit is a liability.
6. **One big red button:** a kill switch any human can press.

**Exercises:** E7.1-E7.10
