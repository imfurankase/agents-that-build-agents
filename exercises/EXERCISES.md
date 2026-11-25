# Exercises: 99 hands-on tasks

**Levels**
- 🟢 **Explore:** prompting, reading, no-code (Claude Code chat or AI Studio). 10-15 min.
- 🟡 **Build:** run and change things *through Claude Code*. 15-30 min.
- 🔴 **Challenge:** design something new and test it. 30-60+ min.

Each exercise has a **Done when** line: that is your success test. Hints: [HINTS.md](HINTS.md). Tip: after each exercise, ask Claude Code *"What did I just learn? Give me 3 bullets."*

---

## Module 0: Setup & orientation
**E0.1 🟢 Check your setup.** Type `/check-setup` and fix every ❌ with Claude Code's help. *Done when:* `python run.py check` shows no ❌.
**E0.2 🟢 Tour the repo.** Ask: *"Give me a 5-minute tour of this repository."* Then open `README.md` and `CLAUDE.md`. *Done when:* you can name what `common/`, `lessons/`, `.claude/` and `workspace/` are for.
**E0.3 🟢 Free practice mode.** Set `LLM_PROVIDER=mock` in `.env` (edit it yourself), run `/run-lesson 4c`, then switch back to `auto`. *Done when:* you've seen the "Offline practice mode" notice and know how to turn it off.
**E0.4 🟢 Your three accounts.** Ask Claude Code to explain subscription vs API key vs AI Studio key. Write down which you have. *Done when:* you know which lessons each one unlocks.

## Module 1: First call
**E1.1 🟢 Hello Gemini.** `/run-lesson 1a`. *Done when:* you can point to the tokens-in and tokens-out numbers.
**E1.2 🟡 Change the persona.** Ask Claude Code to change the system instruction in `hello_gemini.py` to "a sceptical CFO". Run again. *Done when:* you can describe how tone and content changed.
**E1.3 🟢 Same prompt in AI Studio.** Recreate lesson 1a in AI Studio (system instructions + question), then click **Get code**. *Done when:* you can match the AI Studio code to `hello_gemini.py`.
**E1.4 🟡 Headless Claude Code.** `/run-lesson 1c`. Then type in a terminal: `claude -p "In one sentence, what is an AI agent?"`. *Done when:* both work and you know which plan the usage counts against.
**E1.5 🟢 No memory.** In AI Studio, start a new chat and ask "what did I just ask you?" Explain the answer. *Done when:* you can explain why agents must re-send the conversation.
**E1.6 🟢 Token sense.** Ask Claude Code to estimate the tokens (and Claude API cost) of a 10-page report. *Done when:* you have a rough "words → tokens → $" rule of thumb.

## Module 2: Prompting
**E2.1 🟢 Weak vs strong.** `/run-lesson 2a`. *Done when:* you can name the 6 parts in the strong prompt.
**E2.2 🟡 New audience.** Ask Claude Code to rewrite STRONG_PROMPT in `prompt_lab.py` for the IT security team. *Done when:* the output focuses on security decisions.
**E2.3 🟡 Prompt improver.** `/run-lesson 2b` with a rough prompt you really use at work. *Done when:* the improved version is saved in `workspace/prompts/` and you agree with the changes.
**E2.4 🟢 Score a prompt.** Paste one of your prompts and ask Claude Code to score it against the checklist in `PROMPTING_GUIDE.md` §11. *Done when:* you've fixed its 2 weakest parts.
**E2.5 🟢 Few-shot.** In AI Studio, ask for 5 meeting-note action items; then add 2 examples of the exact format you want. *Done when:* the format matches your examples.
**E2.6 🟢 Make it say "unknown".** Ask a question whose answer isn't in a pasted document, first without and then with "if it isn't in the document, say UNKNOWN". *Done when:* you've seen the hallucination disappear.
**E2.7 🟡 Structured output.** In AI Studio, extract {name, date, amount} from 3 pasted invoices using a JSON schema. *Done when:* all 3 come back as valid JSON.
**E2.8 🟢 Ask-first prompt.** Write a prompt that makes the AI ask you 3 questions before drafting a policy. *Done when:* it asks good questions instead of guessing.
**E2.9 🟡 Audit a system prompt.** Ask Claude Code which of the 6 parts `prompts/system/orchestrator.md` contains. *Done when:* you can name one improvement.
**E2.10 🔴 Your prompt pack.** Create `workspace/my_prompts.md` with your 5 most useful work prompts rewritten with the 6-part structure. *Done when:* each has role, context, task, format, rules, done-when.

## Module 3: Tools
**E3.1 🟢 Watch tool choice.** `/run-lesson 3a`. *Done when:* you can say which tool was called first and why.
**E3.2 🟡 Add a tool.** Ask Claude Code to add `get_team_budget(team_name)` with fake data to `gemini_tools.py` and ask "Which team has the biggest budget per person?" *Done when:* the model uses all three tools.
**E3.3 🟢 Bad description.** Ask Claude Code to temporarily change lookup_team's docstring to "does stuff" and run again. *Done when:* you've seen the behaviour get worse, and it's restored.
**E3.4 🟢 Risk levels.** Ask for a table of every toolbox tool with a scenario where it would be dangerous. *Done when:* you can justify why `run_python` is high risk.
**E3.5 🟡 Word-count tool.** Prompt Claude Code to add a low-risk `word_count(path)` tool to `common/toolbox.py` with a test (prompt #31). *Done when:* `python -m pytest -q` passes.
**E3.6 🟢 Be the tool (AI Studio).** Declare a function in AI Studio's function calling panel and answer the model's call yourself. *Done when:* the model uses your "result" in its answer.

## Module 4: The agent loop
**E4.1 🟢 Narrated loop.** `/run-lesson 4c`. *Done when:* you can explain each turn.
**E4.2 🟢 Read the loop.** `/explain` the `run_agent` function in `common/llm.py`. *Done when:* you can draw the loop from memory.
**E4.3 🟡 Starve the loop.** Set `MAX_TURNS = 1` in `mini_agent_gemini.py`, run, restore. *Done when:* you've seen "Stopped: reached MAX_TURNS".
**E4.4 🟡 New goal.** Change the goal in `watch_the_loop.py` to plan a 2-day offsite for 8 people with a budget. *Done when:* the agent uses the calculator and saves a note.
**E4.5 🟢 Compare providers.** Ask for a table comparing `mini_agent_gemini.py` and `mini_agent_claude.py`. *Done when:* you can name 2 differences and the 1 thing that's identical.
**E4.6 🔴 Add a narrator feature.** Ask Claude Code to make `watch_the_loop.py` also print the running estimated cost after each turn. *Done when:* the cost appears per turn.

## Module 5: Multi-agent patterns
**E5.1 🟢 Five patterns.** Run 5a-5e. *Done when:* you can give a work example for each pattern.
**E5.2 🟢 Pick the pattern.** Ask: *"Which pattern fits: IT help requests; reviewing a policy from 4 angles; drafting until it meets a checklist?"* *Done when:* you agree with the reasoning.
**E5.3 🟡 Fourth reviewer.** Add a "staff wellbeing" reviewer to `p3_parallel.py`. *Done when:* the chair's verdict mentions wellbeing.
**E5.4 🟡 Harder judge.** Add a criterion to `p5_evaluator_optimizer.py`. *Done when:* you've seen it take more rounds (or explain why not).
**E5.5 🟡 New route.** Add a "legal" specialist to `p2_router.py` and send a contract question. *Done when:* it routes to legal.
**E5.6 🟡 Parallel workers.** Ask Claude Code to make `p4_orchestrator_workers.py` run workers in parallel. *Done when:* it's noticeably faster and the output is the same shape.
**E5.7 🔴 Router + chain.** Build `p6_router_chain.py` (prompt #43). *Done when:* it routes, drafts, then edits.
**E5.8 🔴 Design for your work.** In Plan mode, design (don't build) a multi-agent system for a real process in your team. *Done when:* you have a diagram, the pattern(s) named, and the risks listed.

## Module 6: Agents that build agents
**E6.1 🟡 First architect.** `/run-lesson 6a` with a goal from your work. *Done when:* a new JSON file appears in `agent_registry/` and you can explain each field.
**E6.2 🟢 Read a spec.** `/explain` the new JSON file. *Done when:* you can say why it got each tool (or none).
**E6.3 🟡 Meta-agent.** `/run-lesson 6b` with the default goal. *Done when:* you can list which agents it hired and why.
**E6.4 🟢 Read the story.** Ask Claude Code to tell the story of the run from the latest `logs/run-*.jsonl`. *Done when:* you can follow create → run → result for each agent.
**E6.5 🟡 Reuse.** `python run.py 6c examples`, then run `meeting-scribe` on your own notes with 6c. *Done when:* a saved agent did real work without being redesigned.
**E6.6 🟡 Improve an agent.** Use `6c improve` to make an agent end with "open questions". *Done when:* its version number went up and the new behaviour shows.
**E6.7 🟡 Tune the architect.** Make `prompts/system/agent_architect.md` always add a "Questions to ask the human" section. *Done when:* the next designed agent has it.
**E6.8 🟡 Reuse first.** Edit the orchestrator prompt so it checks `list_agents` before creating anything. *Done when:* the audit log shows `list_agents` first and an existing agent reused.
**E6.9 🔴 The librarian.** Create a "librarian" agent that recommends which registered agent fits a task (prompt #58). *Done when:* it recommends correctly for 3 test tasks.
**E6.10 🔴 Grandchildren.** Ask Claude Code to run the meta-agent with `max_depth=2` and a goal big enough that a child hires its own helper. *Done when:* the audit log shows an agent created at depth 2, and you can explain the risk.

## Module 7: Controlling agents
**E7.1 🟢 All demos.** `/run-lesson 7a` (with mock mode for zero cost). *Done when:* you can explain each control in one sentence.
**E7.2 🟡 Approval.** `python run.py 7a approval`, and answer "no". *Done when:* you see BLOCKED and understand where that came from.
**E7.3 🟡 Strict meta-agent.** `/run-lesson 7b` and decline one proposed agent. *Done when:* the orchestrator adapted and the final answer mentions the refusal.
**E7.4 🟢 Audit report.** `/run-lesson 7c`. *Done when:* you can answer "who created what, what was blocked, what did it cost".
**E7.5 🟡 Presets.** Create SANDBOX and PRODUCTION Policy presets (prompt #62). *Done when:* both exist, tests pass, and you can justify each value.
**E7.6 🟡 Toxic combination.** Add a rule: no agent may hold `fetch_webpage` + `write_file` together, with a test (prompt #63). *Done when:* the test passes and you can explain the risk.
**E7.7 🟡 Per-agent budget.** Prompt #64. *Done when:* one greedy agent stops while the run continues.
**E7.8 🟢 Kill switch.** `/stop-all`, try any lesson, then delete `STOP` yourself. *Done when:* you've seen both Python and Claude Code blocked, then resumed.
**E7.9 🟢 Claude Code audit.** `/audit`. *Done when:* you can see the tools Claude Code used today.
**E7.10 🔴 Governance policy.** Ask Claude Code for a one-page Agent Governance Policy for your organisation (prompt #68), then edit it yourself. *Done when:* it states who may create agents, approval levels by risk, limits, logging and review cadence.

## Module 8: Claude Code as an agent factory
**E8.1 🟢 Inventory.** Ask for a table of this project's subagents (prompt #69). *Done when:* you know which has the most power.
**E8.2 🟡 First subagent.** `/new-agent` an email tone checker. *Done when:* the file exists, the safety review is LOW risk, and you've used it once.
**E8.3 🟡 Use it.** Ask: *"Use the <name> agent to check this draft: ..."* *Done when:* the main session delegated (you'll see the subagent working).
**E8.4 🟢 Read a subagent.** Open `.claude/agents/agent-architect.md`. Identify description/tools/body. *Done when:* you can explain "description = when, tools = what, body = how".
**E8.5 🟡 Edit by hand.** Change one line in your subagent's body yourself (plain English), then use it again. *Done when:* the behaviour changed with no restart.
**E8.6 🟡 Build a team.** `/build-team Produce a one-page briefing on AI agent risks for leadership`. *Done when:* the deliverable is in `workspace/teams/` and you chose keep/delete.
**E8.7 🟡 New skill.** Create `/weekly-brief` (prompt #75). *Done when:* typing `/weekly-brief` runs your playbook.
**E8.8 🟢 Settings tour.** Ask Claude Code to explain `.claude/settings.json` (prompt #76). *Done when:* you can say what is allowed, asked and denied.
**E8.9 🟡 Guard rule.** Add a guard rule and test it with sample JSON (prompt #77). *Done when:* the new rule blocks the test command and normal commands still pass.
**E8.10 🟡 Script-made agents.** `/run-lesson 8a` with `--save`. *Done when:* new agents appear in `.claude/agents/` and you used one in VS Code.
**E8.11 🟢 Plan mode.** In Plan mode, ask for 4 subagents for your department (prompt #82); review the plan, approve only some. *Done when:* only approved agents were created.
**E8.12 🔴 Your personal staff.** Build 3 subagents you'll really use weekly (e.g. brief writer, email checker, research assistant), each reviewed LOW risk. *Done when:* you've used each on real work.

## Module 9: Google AI Studio & ADK
**E9.1 🟢 AI Studio tour.** Follow walkthroughs 1-3 in `docs/AI_STUDIO_GUIDE.md`. *Done when:* you've used system instructions, a JSON schema and function calling.
**E9.2 🟡 adk web.** Start `adk web` for lesson 9 and ask for a briefing. *Done when:* you've clicked through the events and seen each agent's work.
**E9.3 🟢 AgentTool vs sub_agents.** Ask Claude Code to explain the difference. *Done when:* you can say which keeps the lead in control.
**E9.4 🟡 Fact checker.** Add a `fact_checker` to the ADK team (prompt #85). *Done when:* the trace shows it being called.
**E9.5 🟡 Dynamic team.** `/run-lesson 9b`. *Done when:* you can say which specialists came from your registry and which were hired.
**E9.6 🟡 Studio to repo.** Build a prompt in AI Studio, click Get code, and ask Claude Code to turn it into an agent in the repo (prompt #87). *Done when:* it runs under the Governor.
**E9.7 🔴 Cross-framework agent.** Take one registry agent and run it three ways: Python foundry (6c), ADK (9b), Claude Code subagent (prompt #80). *Done when:* you can compare the results and say which you prefer and why.

## Module 10: MCP
**E10.1 🟡 Connect.** Register the agent-registry MCP server (prompt #91). *Done when:* `/mcp` shows it connected.
**E10.2 🟡 Manage via MCP.** List, create and run an agent through MCP (prompts #92-93). *Done when:* a new agent with `created_by: claude-code (mcp)` exists.
**E10.3 🟢 Hit the ceiling.** Try to create an agent with `run_python` via MCP. *Done when:* you've seen the Governor refuse it and know why.
**E10.4 🟢 No print().** Ask why MCP servers must not print to stdout. *Done when:* you can explain it in one sentence.
**E10.5 🟡 New MCP tool.** Add `agent_stats` (prompt #95). *Done when:* Claude Code can call it after reconnecting.
**E10.6 🔴 MCP shopping list.** Research ready-made MCP servers useful for your team and the least access each needs (prompt #96, use the researcher). *Done when:* you have a table with name, use, access, risk.

## Module 11: Evals & safety
**E11.1 🟡 Run the eval.** `/run-lesson 11a`. *Done when:* you can explain each case's result.
**E11.2 🟡 More cases.** Add 3 cases (French notes; shared task; "next Tuesday") and rerun. *Done when:* the scorecard includes them.
**E11.3 🟡 Eval your agent.** Build 5 cases for an agent you created and run `--agent <name>` (prompt #99). *Done when:* you have a pass rate.
**E11.4 🟡 Fix and re-test.** Improve the agent from E11.3 based on its failures (6c improve), rerun the eval. *Done when:* the pass rate went up.
**E11.5 🟢 Injection drill.** `/run-lesson 11b`. *Done when:* you can explain why C and D are stronger than B.
**E11.6 🟡 Red team.** Add a case that tries to extract the agent's instructions (prompt #101). *Done when:* it's in the suite and you know if the agent resisted.
**E11.7 🟢 Risk table.** Use the safety-reviewer on all agents (prompt #102). *Done when:* every HIGH has a fix planned.
**E11.8 🔴 Launch checklist.** Create your organisation's pre-launch checklist for agents (prompt #106). *Done when:* it covers purpose, tools, data, untrusted input, limits, approvals, audit, evals, kill switch.

## Module 12: Capstone
**E12.1 🟡 First mission.** `/run-lesson 12` with a default goal. *Done when:* you approved the plan and got a judged deliverable.
**E12.2 🟢 Leadership summary.** Summarise the mission record and audit report in 10 lines (prompt #108). *Done when:* a non-technical colleague could understand it.
**E12.3 🟡 Better planner.** Add a fact-checking step to the team planner prompt; rerun; compare (prompt #109). *Done when:* you can say whether the score improved and at what cost.
**E12.4 🟡 Budget experiment.** Run the same goal with two budgets (prompt #110). *Done when:* you have a cost vs quality comparison.
**E12.5 🔴 Real task.** Run a real task from your work through the Foundry with a tight budget (prompt #111). *Done when:* you have the result, team, cost, audit trail and a "ready for production?" verdict.
**E12.6 🔴 Present it.** Prepare a 5-minute presentation of E12.5: what the agents built, how they were controlled, what it cost, and what you'd need to scale it. *Done when:* you've delivered it to a colleague and answered their questions.

## Final project: your personal assistant (EP)
Follow [final_project/README.md](../final_project/README.md). Work in order; each milestone builds on the last.

**EP.1 🟢 Free-API questions.** `/run-lesson p1` with three questions of your own (weather where you'll travel, the next holiday, a currency conversion). *Done when:* you can predict which tools it uses before you press Enter.
**EP.2 🟡 New free tool.** Ask Claude Code to add a sunrise/sunset tool (Open-Meteo) to `common/free_apis.py`, register it in the toolbox, with an offline sample answer and a test. *Done when:* p1 uses it and `python -m pytest -q` passes.
**EP.3 🟡 Your sample week.** Make `final_project/sample_data/` look like your real week (fictional but realistic events and emails). *Done when:* `python run.py p2` shows a day that feels like yours.
**EP.4 🟡 Briefing that fits you.** Run p3, then edit `prompts/system/briefing.md` (e.g. add "3 things only I can do today"). *Done when:* you'd happily read it every morning.
**EP.5 🟢 Did it catch the traps?** In p3's output, check: the phishing email, the email instructing AI assistants, and the lunch/IT-call clash. *Done when:* all three appear under "Watch out", or you've improved the prompt until they do.
**EP.6 🟡 Chat and reminders.** In p4, set three reminders in natural language ("in 10 minutes", "tomorrow at 9", "Friday 4pm"). *Done when:* `workspace/assistant/reminders.json` has the right three times.
**EP.7 🟢 Refusal test.** In p4, ask it to forward, delete or reply to an email. *Done when:* it refuses and offers a draft, and you can explain why it *can't* (no such tools).
**EP.8 🟡 On your phone.** Complete milestone 5 (BotFather, token, owner id). *Done when:* `/brief` works on your phone and a 2-minute reminder buzzes.
**EP.9 🟡 Keep it running.** Ask Claude Code to set up a Windows Task Scheduler task (on a Mac: a launchd agent) that starts the bot at log-in. *Done when:* the bot works after a restart without you starting it.
**EP.10 🟡 Real calendar.** Add your calendar's secret iCal link to `.env`; run p6, then p2. *Done when:* p6 shows ✅ for the calendar and the briefing uses your real events.
**EP.11 🔴 Real email (personal account).** Set up read-only IMAP with an app password for a personal or test account; run p6. *Done when:* p6 shows ✅ for email and the inbox stays unread.
**EP.12 🔴 Extend it.** Add one feature from "Ideas to extend" (e.g. a Friday weekly review, or meeting-prep messages 30 minutes before each meeting), with a test and a safety review (`/review-agent`). *Done when:* it runs on your phone and you can explain its controls.
