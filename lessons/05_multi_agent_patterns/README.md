# Lesson 05: Multi-agent patterns

**Goal:** know the five proven ways to combine several AI calls/agents, and when to use each.

## The five patterns
| Pattern | Picture | Use when | File |
|---|---|---|---|
| **Chain** | A → B → C | Fixed steps in a fixed order | `p1_chain.py` |
| **Router** | classify → one specialist | Different request types need different experts | `p2_router.py` |
| **Parallel** | A, B, C at once → combine | Independent views or many independent items | `p3_parallel.py` |
| **Orchestrator-workers** | manager splits → workers → combine | Sub-tasks can't be known in advance | `p4_orchestrator_workers.py` |
| **Evaluator-optimizer** | writer ⇄ judge loop | Clear quality criteria; revision helps | `p5_evaluator_optimizer.py` |

**Rule of thumb: use the simplest pattern that works.** A single good prompt beats a clumsy multi-agent system. Add agents only when it measurably helps: quality, speed (parallel), or separation of concerns.

## Why multiple agents at all?
- **Focus:** each agent has one job and a short, precise prompt.
- **Context:** each agent sees only what it needs (less confusion, lower cost).
- **Checks:** one agent reviews another (the judge pattern catches mistakes).
- **Speed:** independent work runs in parallel.

Costs: more model calls, more to debug, errors can compound. Measure!

## Say this to Claude Code
> Run lessons 5a to 5e one by one. After each, explain the pattern with a real-life analogy from managing a team.

> Which pattern would you use for: (a) answering staff IT questions, (b) reviewing a policy from 4 angles, (c) writing a report until it meets a checklist? Explain.

> In p3_parallel.py add a fourth reviewer for "staff wellbeing" and run it.

> In p5_evaluator_optimizer.py, add a criterion "includes a contact email" and see how many rounds it now takes.

> Draw me an ASCII diagram of p4_orchestrator_workers.py, then explain what the orchestrator decides at run time.

## Run it
```
python run.py 5a   (chain)      python run.py 5d   (orchestrator-workers)
python run.py 5b   (router)     python run.py 5e   (evaluator-optimizer)
python run.py 5c   (parallel)
```

## Takeaways
1. Five patterns cover most real systems. Learn to recognise them.
2. Structured outputs (JSON) are the glue between agents.
3. Code-enforced limits (max workers, max rounds) keep patterns safe and affordable.
4. Orchestrator-workers is one step away from agents that **create** agents (next lesson).

**Exercises:** E5.1-E5.8
