"""Lesson 07a - See each control in action, one at a time.

Run it:  python lessons/07_controlling_agents/governor_demos.py            (all demos)
         python lessons/07_controlling_agents/governor_demos.py budget     (one demo)

Demos: ceiling, escalation, headcount, depth, approval, budget, killswitch, audit

Most demos call the Governor directly, so they cost nothing and work offline.
The "budget" and "killswitch" demos run a real agent loop (use LLM_PROVIDER=mock
to keep them free).
"""
import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))

from common import config, show
from common.foundry import AgentFoundry
from common.governor import Governor, Policy
from common.llm import get_llm
from common.spec import AgentSpec
from common.toolbox import tools_by_name


def make_spec(name, tools, instructions="You are a helpful test agent. Do the task briefly."):
    return AgentSpec(name=name, role="demo agent", instructions=instructions, tools=tools)


def demo_ceiling():
    show.title("1. TOOL CEILING - some tools are simply not allowed in this run")
    gov = Governor(Policy(allowed_tools={"calculator", "read_notes", "save_note"}), verbose=False)
    ok, why = gov.approve_new_agent(make_spec("web-researcher", ["fetch_webpage"]), 1, None)
    show.event("Create an agent with fetch_webpage ->", f"{'ALLOWED' if ok else 'REFUSED'}: {why}",
               "red" if not ok else "green")


def demo_escalation():
    show.title("2. NO ESCALATION - an agent cannot give more power than it has")
    gov = Governor(Policy(), verbose=False)
    parent_tools = {"save_note", "read_notes", "calculator"}
    ok, why = gov.approve_new_agent(make_spec("code-runner", ["run_python"]), 1, parent_tools)
    show.event(f"Parent holds {sorted(parent_tools)}; child asks for run_python ->",
               f"{'ALLOWED' if ok else 'REFUSED'}: {why}", "red" if not ok else "green")


def demo_headcount():
    show.title("3. HEADCOUNT - at most N new agents per run")
    gov = Governor(Policy(max_agents=2), verbose=False)
    for i in range(1, 4):
        ok, why = gov.approve_new_agent(make_spec(f"helper-{i}", []), 1, None)
        show.event(f"Hire helper-{i} ->", "ALLOWED" if ok else f"REFUSED: {why}",
                   "green" if ok else "red")


def demo_depth():
    show.title("4. DEPTH LIMIT - agents creating agents creating agents...")
    gov = Governor(Policy(max_depth=2), verbose=False)
    for depth in (1, 2, 3):
        ok, why = gov.approve_new_agent(make_spec(f"level-{depth}-agent", []), depth, None)
        show.event(f"Create an agent at depth {depth} ->", "ALLOWED" if ok else f"REFUSED: {why}",
                   "green" if ok else "red")


def demo_approval():
    show.title("5. HUMAN APPROVAL - risky actions wait for a person")
    show.info("A high-risk tool (run_python) needs your yes/no. Try answering 'no'.")
    gov = Governor(Policy(approval_for_risk={"high"}))
    tool = tools_by_name(["run_python"])[0]
    blocked = gov.before_tool("demo-agent", tool, {"code": "print('hello')"})
    if blocked:
        show.event("Result ->", f"BLOCKED: {blocked}", "red")
    else:
        show.event("Result ->", tool.run({"code": "print('hello')"}), "green")


def demo_budget():
    show.title("6. BUDGET - the run stops when the money limit is reached")
    llm = get_llm()
    if llm.name == "mock":
        show.info("(mock model: pretending each token is very expensive so the limit trips)")
        config.PRICES_PER_MILLION["mock"] = (50_000.0, 50_000.0)
    gov = Governor(Policy(max_usd=0.01))
    result = llm.run_agent(name="spender", system="You are a test agent.",
                           task="Use each of your tools once, then summarise.",
                           tools=tools_by_name(["calculator", "get_current_datetime", "read_notes"]),
                           max_turns=10, hooks=gov)
    config.PRICES_PER_MILLION["mock"] = (0.0, 0.0)
    show.event("Agent stopped because ->", result.stopped_reason, "red")
    show.info(gov.summary())


def demo_killswitch():
    show.title("7. KILL SWITCH - a file named STOP freezes every agent")
    config.KILL_SWITCH_FILE.write_text("stop all agents", encoding="utf-8")
    try:
        foundry = AgentFoundry(governor=Governor(Policy()), verbose=False)
        result = foundry.run(make_spec("any-agent", ["calculator"]), "What is 2+2?")
        show.event("Agent stopped because ->", result.stopped_reason, "red")
    finally:
        config.KILL_SWITCH_FILE.unlink(missing_ok=True)
        show.info("(STOP file removed again so you can keep working)")


def demo_audit():
    show.title("8. AUDIT LOG - every decision is written down")
    logs = sorted(config.LOGS.glob("run-*.jsonl"))
    if not logs:
        show.info("No logs yet - run another demo first.")
        return
    lines = logs[-1].read_text(encoding="utf-8").splitlines()[-8:]
    for line in lines:
        record = json.loads(line)
        show.event(record["time"], f"{record['event']:<16} {record['agent']}", "cyan")
    show.info(f"Full log: {config.rel(logs[-1])} "
              f"(or run lessons/07_controlling_agents/audit_report.py)")


DEMOS = {"ceiling": demo_ceiling, "escalation": demo_escalation, "headcount": demo_headcount,
         "depth": demo_depth, "approval": demo_approval, "budget": demo_budget,
         "killswitch": demo_killswitch, "audit": demo_audit}

chosen = sys.argv[1:] or list(DEMOS)
for name in chosen:
    if name not in DEMOS:
        sys.exit(f"Unknown demo '{name}'. Choose from: {', '.join(DEMOS)}")
    DEMOS[name]()
