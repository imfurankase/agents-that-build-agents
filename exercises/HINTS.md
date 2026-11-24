# Hints & answers

Try first, then peek. Or ask the tutor: *"Use the lesson-tutor to give me the smallest hint for E6.8."*

## Module 0-1
- **E0.1:** Most ❌ are fixed by: creating the venv (`uv venv`), installing packages (`uv pip install -r requirements.txt`), copying `.env.example` to `.env`. For `claude` not found: install the CLI, then open a **new** terminal.
- **E0.4:** Subscription → Claude Code track (VS Code, skills, subagents, `claude -p`). AI Studio key → all Python lessons with real answers + ADK. API key → `*_claude_api` lessons + Agent SDK.
- **E1.5:** Each call is independent. Chat apps look like they remember because they re-send the whole conversation every time. Agents do the same (the `messages`/`contents` list in lesson 04).
- **E1.6:** Rule of thumb: 1 page ≈ 500 words ≈ 650-700 tokens. 10 pages ≈ 7K tokens. On Claude Opus 5.5 ($4 per million input tokens) that's about $0.03 to read, plus the output.

## Module 2
- **E2.1:** Role (chief-of-staff), context (director, 2 minutes), material (`<document>`), task (decision brief), format (4 numbered parts, <150 words), rules (no invented numbers).
- **E2.6:** Without permission to say "unknown", models tend to fill gaps plausibly. Giving an explicit fallback answer removes the pressure to invent.
- **E2.7:** Schema example: `{"type":"object","properties":{"name":{"type":"string"},"date":{"type":"string"},"amount":{"type":"number"}},"required":["name","date","amount"]}`.
- **E2.9:** It has role, method, rules and output guidance. A possible improvement: a concrete example of a good delegation brief, or an explicit "done when".

## Module 3-4
- **E3.2:** The model needs headcount (lookup_team) and budget (get_team_budget), then division (calculator). If it skips the calculator, tighten the system instruction: "Use the calculator for all math."
- **E3.4:** `run_python` can do *anything* the computer can (read files, use the network) within its 30-second limit. Hence high risk and human approval.
- **E4.3:** With 1 turn, the model asks for a tool, but the loop ends before it can see the result and answer.
- **E4.5:** Same: the loop (ask → run tools → send results → repeat). Different: message formats (`messages` + `tool_result` vs `contents` + `function_response`) and how tools are declared.
- **E4.6:** In the `Narrator.on_usage` hook, accumulate `config.cost_usd(model, input_tokens, output_tokens)` and print the total.

## Module 5
- **E5.2:** IT requests → router. Policy from 4 angles → parallel. Draft until checklist met → evaluator-optimizer.
- **E5.4:** If it passes in round 1 anyway, the writer may already satisfy it. Make the criterion more demanding.
- **E5.6:** Use `ThreadPoolExecutor` like `p3_parallel.py`: `pool.map(run_worker, subtasks)`.

## Module 6
- **E6.2:** The architect's prompt says "fewest tools"; a pure text job (summarising pasted notes) needs no tools at all. That is least privilege in action.
- **E6.5:** `python run.py 6c run meeting-scribe "Notes: ..."`.
- **E6.8:** Add to the method in `orchestrator.md`: "Step 0: ALWAYS call list_agents first; reuse an agent if its role fits." Then check the audit log order.
- **E6.10:** Use `Policy(max_depth=2)` in `b_meta_agent.py` and a goal with clearly separable sub-projects, e.g. "Create a training pack: a guide (with its own research) and a quiz (with its own answer key)". Risk: costs and complexity grow fast with depth, and errors compound. That's why the default is 1-2.

## Module 7
- **E7.3:** The tool returns "REFUSED by the Governor: a human reviewer declined this new agent". The orchestrator's prompt tells it to adapt and mention refusals.
- **E7.5:** Typical PRODUCTION: low `max_usd`, `max_agents` 3, `max_depth` 1, `approve_new_agents=True`, `approval_for_risk={"medium","high"}`, restricted `allowed_tools`. SANDBOX: higher limits, approvals only for high risk.
- **E7.6:** The risk is exfiltration: read untrusted content → write it (or secrets) somewhere. Check in `approve_new_agent`: `if {"fetch_webpage","write_file"} <= set(spec.tools): return False, "..."`.
- **E7.7:** Track spending per agent name in `on_usage`; raise `StopAgent("agent budget")` when one exceeds `max_usd_per_agent`.

## Module 8
- **E8.3:** You can also force it: "Use the <name> subagent". The panel shows subagent activity.
- **E8.5:** No restart needed: Claude Code reloads agent files within seconds.
- **E8.9:** Test pattern: `echo '{"tool_name":"Bash","tool_input":{"command":"curl http://unknown.example"}}' | python .claude/hooks/guard.py` → exit code 2 means blocked.
- **E8.10:** If `claude` isn't found, install the CLI (docs/SETUP_WINDOWS.md step 3) and use a new terminal.

## Module 9-10
- **E9.2:** Run `adk web` from inside `lessons/09_google_adk` (the folder that *contains* `adk_team`).
- **E9.3:** AgentTool: the lead calls the agent like a function and gets the result back, so the lead stays in control. sub_agents: the conversation is handed over (transfer).
- **E10.1:** If it won't connect: check the Python path in the `claude mcp add` command points to your `.venv`, and that the packages are installed in that venv.
- **E10.4:** MCP over stdio uses stdout for protocol messages; any extra print corrupts them. Use stderr or logging.

## Module 11-12
- **E11.4:** Typical fixes come straight from the judge's feedback: add the missing rule ("mark UNASSIGNED"), add an example, or tighten the output format.
- **E11.5:** B relies on the model choosing to obey the house rules; C makes the attack impossible (no write tool); D puts a human in the way. Structure beats persuasion.
- **E12.3:** Compare `verdict.score` and the governor summary (cost) in the two mission records in `workspace/missions/`.
- **E12.5:** Start with `MAX_USD_PER_RUN=0.50` and `max_agents` 3. Review every proposed agent before approving.
