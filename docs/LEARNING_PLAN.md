# 6-week learning plan

**Time:** 3-4 hours per week, in two or three sessions of 60-90 minutes.
**Style:** you prompt, Claude Code does the typing. Every session ends with one exercise done and one thing you can explain to someone else.
**Exercises:** in [exercises/EXERCISES.md](../exercises/EXERCISES.md), with hints in [exercises/HINTS.md](../exercises/HINTS.md). Levels: 🟢 prompt-only · 🟡 run & tweak · 🔴 stretch.

| Week | Theme | Lessons | Exercises |
|---|---|---|---|
| 1 | Foundations: setup, model calls, prompting | 00-02 | E0.1-E0.4, E1.1-E1.6, E2.1-E2.10 |
| 2 | From talking to doing: tools, the loop, patterns | 03-05 | E3.1-E3.6, E4.1-E4.6, E5.1-E5.8 |
| 3 | **Agents that build agents** | 06 | E6.1-E6.10 |
| 4 | **Control**, and Claude Code as an agent factory | 07-08 | E7.1-E7.10, E8.1-E8.12 |
| 5 | Google ADK, MCP, evals & safety | 09-11 | E9.1-E9.7, E10.1-E10.6, E11.1-E11.8 |
| 6 | Capstone: a real mission | 12 | E12.1-E12.6 |

---

## Week 1: Foundations
**Goals:** a working setup; understand what a model call is; write a strong 6-part prompt.

**Session 1: Setup (60-90 min)**
- Follow [SETUP_WINDOWS.md](SETUP_WINDOWS.md), then in Claude Code: `/check-setup`
- `/run-lesson 4c`: see an agent run (mock mode is fine).
- Prompt: *"Give me a 5-minute tour of this repository: what is in each top-level folder?"*
- Exercises: E0.1-E0.4

**Session 2: First calls (60 min)**
- `/run-lesson 1a`, then `/run-lesson 1c`
- Prompt: *"Explain hello_gemini.py line by line in plain English. What is a token?"*
- Try the same prompt in Google AI Studio (see [AI_STUDIO_GUIDE.md](AI_STUDIO_GUIDE.md), walkthrough 1).
- Exercises: E1.1-E1.6

**Session 3: Prompting (90 min)**
- Read [prompts/PROMPTING_GUIDE.md](../prompts/PROMPTING_GUIDE.md) (20 min).
- `/run-lesson 2a`, then `/run-lesson 2b "write something about our AI policy for staff"`
- Prompt: *"Which of the 6 prompt parts are in prompts/system/orchestrator.md? What is missing?"*
- Exercises: E2.1-E2.10

**Self-check: can you explain…**
- the difference between a system prompt and a user message?
- why the model "forgets" between calls?
- the 6 parts of a strong prompt, from memory?

---

## Week 2: From talking to doing
**Goals:** understand tools, the agent loop, and the five multi-agent patterns.

**Session 1: Tools (60 min)**
- `/run-lesson 3a`
- Prompt: *"Add a fake get_team_budget tool to gemini_tools.py and ask which team has the biggest budget per person."*
- AI Studio walkthrough 3 (you play the tool).
- Exercises: E3.1-E3.6

**Session 2: The loop (60 min)**
- `/run-lesson 4c`, then `/run-lesson 4a`
- Prompt: *"Open common/llm.py, find run_agent, and explain its 5 numbered steps."*
- Exercises: E4.1-E4.6

**Session 3: Patterns (90 min)**
- `/run-lesson 5a` … `/run-lesson 5e`
- Prompt: *"For each pattern, give me an example from managing a real team."*
- Exercises: E5.1-E5.8

**Self-check: can you explain…**
- why the model never runs a tool itself, and why that matters for control?
- the difference between a workflow and an agent?
- which pattern fits "review a policy from 4 angles"? And "answer IT questions"?

---

## Week 3: Agents that build agents
**Goals:** create agents from a sentence; watch a meta-agent hire its own team; reuse and improve agents.

**Session 1: The architect (60 min)**
- `/run-lesson 6a "Turn long meeting notes into decisions, owners and deadlines"`
- `python run.py 6c examples`: install 3 example agents into the registry.
- Prompt: *"Explain the AgentSpec JSON that was just created, field by field."*

**Session 2: The meta-agent (90 min)**
- `/run-lesson 6b "Create a one-page onboarding guide on using AI tools safely, plus a 5-question quiz"`
- Prompt: *"Walk me through the latest audit log: which agents were hired, by whom, and why?"*
- Prompt: *"Improve prompts/system/orchestrator.md so it always uses a reviewer agent. Rerun and compare."*

**Session 3: Agents as assets (60 min)**
- `python run.py 6c`, then `python run.py 6c improve <name> "…"`
- Exercises: E6.1-E6.10

**Self-check: can you explain…**
- why writing an agent down as data is what makes agents-building-agents possible?
- the four meta-tools and what each does?
- who decides *what* to build and who decides *whether it's allowed*?

---

## Week 4: Control, and Claude Code as an agent factory
**Goals:** master the 8 controls; build agents in Claude Code with no code.

**Session 1: The Governor (90 min)**
- `/run-lesson 7a`, then `python run.py 7a approval` (answer yourself)
- `/run-lesson 7b "Write a short FAQ about our AI pilot"`: say **no** to one hire.
- `/run-lesson 7c`, then `/audit`
- Exercises: E7.1-E7.10

**Session 2: Subagents and skills (90 min)**
- Read [CLAUDE_CODE_GUIDE.md](CLAUDE_CODE_GUIDE.md) sections 2-5.
- `/new-agent an agent that reviews draft emails for tone and clarity`
- `/review-agent <that agent>`
- `/build-team Produce a one-page briefing on AI agent risks for our leadership team`

**Session 3: Hooks and headless (60 min)**
- `/stop-all`, try anything, then delete `STOP` yourself.
- `/run-lesson 8a "Write a 1-page explainer on AI agents to explainer.md" --save`
- Exercises: E8.1-E8.12

**Self-check: can you explain…**
- why a budget in code beats "please don't overspend" in a prompt?
- description vs. tools vs. body in a subagent file?
- what the guard hook blocks, and how the kill switch works?

---

## Week 5: Google ADK, MCP, evals & safety
**Goals:** see agents visually in ADK; connect Claude Code to your agents via MCP; test agents properly.

**Session 1: ADK (60-90 min)**
- AI Studio walkthroughs 2, 4 and 6.
- Prompt: *"Start adk web for lesson 9 and tell me what to click to see each agent's trace."*
- `/run-lesson 9b "Create a checklist for a safe AI pilot"`
- Exercises: E9.1-E9.7

**Session 2: MCP (60 min)**
- Prompt: *"Register the MCP server in lessons/10_mcp for this project."*, then `/mcp`
- Prompt: *"Using the agent-registry tools, list my agents and run meeting-scribe on these notes: …"*
- Exercises: E10.1-E10.6

**Session 3: Evals & safety (90 min)**
- `/run-lesson 11a`, then add 3 new cases and rerun.
- `/run-lesson 11b` and discuss each set-up.
- Exercises: E11.1-E11.8

**Self-check: can you explain…**
- AgentTool vs. sub_agents in ADK?
- why controls must live in the MCP server, not in the client?
- why prompts alone don't stop prompt injection, and what does?

---

## Week 6: Capstone
**Goals:** run a real, governed mission end to end and present it.

- Session 1: `/run-lesson 12 "<a real task from your work>"`. Review the plan before approving.
- Session 2: `/review-agent` on each hired agent; build a 5-case eval for the best one (lesson 11).
- Session 3: Prepare a 10-minute presentation: result, the team that made it, cost, audit trail, what's needed before production.
- Exercises: E12.1-E12.6

**Final self-check: can you…**
- design an agent from a sentence, review it, and explain its risk?
- set a policy (budget, headcount, depth, tool ceiling, approvals) for a given situation?
- tell a colleague how to stop every agent in this project immediately?

---

## For the teacher: running a 60-90 minute session
| Time | Activity |
|---|---|
| 0-5 min | **Recap:** learner explains last session's key idea in their own words |
| 5-15 min | **Concept:** one big idea from the slides (one diagram, one analogy) |
| 15-25 min | **Demo:** you drive Claude Code with the lesson's prompts; narrate what happens |
| 25-60 min | **Hands-on:** the learner drives; you only give hints (use `/quiz-me` or the `lesson-tutor` subagent for prompts) |
| 60-75 min | **Exercise:** one 🟢 and one 🟡 exercise from the week's range |
| 75-85 min | **Debrief:** what surprised you? Where would this help in your work? What's the risk? |
| 85-90 min | **Homework:** one exercise plus the self-check questions |

Tips: let the learner make (safe) mistakes and use **rewind**; keep `LLM_PROVIDER=mock` for the first run of anything new; always finish with `/audit` so reviewing logs becomes a habit.

---

## Weeks 7-9: Final project, your personal assistant
Follow [final_project/README.md](../final_project/README.md). Suggested pace:

| Week | Milestones | Sessions | Exercises |
|---|---|---|---|
| 7 | 1-3: free APIs, your data, morning briefing | `/run-lesson p1`, `p2`, `p3` | EP.1-EP.5 |
| 8 | 4-5: chat + reminders, then on your phone | `/run-lesson p4`, then set up Telegram and `p5` | EP.6-EP.9 |
| 9 | 6 + extend: real calendar/email, one new feature | `/run-lesson p6` | EP.10-EP.12 |

**Self-check:** Why is the briefing a workflow but the chat an agent? Which of the "dangerous trio" did we remove, and how? Where does your data go, and what does your organisation's policy say about that?
