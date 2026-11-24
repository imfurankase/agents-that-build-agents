"""Offline tests: they use the free mock model, so no keys and no cost.

Run:  python -m pytest -q
Or ask Claude Code: "run the tests and explain the results simply".
"""
import json
import os
import pathlib
import subprocess
import sys
import tempfile

import pytest

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
os.environ["LLM_PROVIDER"] = "mock"
os.environ["COURSE_DATA_DIR"] = tempfile.mkdtemp(prefix="course-test-")  # don't touch real folders

from common import config  # noqa: E402
from common.foundry import AgentFoundry  # noqa: E402
from common.governor import Governor, Policy  # noqa: E402
from common.llm import fake_from_schema, get_llm  # noqa: E402
from common.registry import AgentRegistry  # noqa: E402
from common.spec import AgentSpec, agent_spec_schema, team_plan_schema  # noqa: E402
from common.toolbox import TOOLBOX, calculator, read_file  # noqa: E402


@pytest.fixture()
def foundry(tmp_path):
    return AgentFoundry(governor=Governor(Policy(auto_answer="no"), verbose=False),
                        registry=AgentRegistry(tmp_path / "registry"), provider="mock",
                        verbose=False)


def spec(name="test-agent", tools=()):
    return AgentSpec(name=name, role="test", instructions="You are a test agent. Be brief.",
                     tools=list(tools))


# ---- toolbox --------------------------------------------------------------
def test_calculator_is_safe():
    assert calculator("(2 + 3) * 4") == "20"
    with pytest.raises(ValueError):
        calculator("__import__('os').system('echo hi')")


def test_file_tools_stay_in_workspace():
    with pytest.raises(PermissionError):
        read_file("../.env")


def test_web_allowlist_blocks_unknown_sites():
    assert TOOLBOX["fetch_webpage"].run({"url": "https://example.com"}).startswith("ERROR")


# ---- specs ----------------------------------------------------------------
def test_spec_validation():
    assert spec("Budget Analyst").name == "budget-analyst"
    with pytest.raises(ValueError):
        AgentSpec(name="x", role="r", instructions="too short", tools=[])
    with pytest.raises(ValueError):
        spec(tools=["launch_missiles"])


def test_schemas_are_strict():
    for schema in (agent_spec_schema(), team_plan_schema()):
        assert schema["additionalProperties"] is False
        json.dumps(schema)
    AgentSpec(**fake_from_schema(agent_spec_schema()))  # mock output must be a valid spec


# ---- governor ---------------------------------------------------------------
def test_governor_limits():
    gov = Governor(Policy(max_agents=1, max_depth=1,
                          allowed_tools={"calculator", "save_note"}), verbose=False)
    assert gov.approve_new_agent(spec("too-deep"), depth=2, parent_tools=None)[0] is False
    assert gov.approve_new_agent(spec("web", ["fetch_webpage"]), 1, None)[0] is False
    assert gov.approve_new_agent(spec("ok-one", ["calculator"]), 1, None)[0] is True
    assert gov.approve_new_agent(spec("second"), 1, None)[0] is False  # headcount


def test_no_privilege_escalation():
    gov = Governor(Policy(), verbose=False)
    ok, why = gov.approve_new_agent(spec("runner", ["run_python"]), 1, {"save_note"})
    assert not ok and "more power" in why


def test_approval_gate_blocks_when_human_says_no():
    gov = Governor(Policy(auto_answer="no"), verbose=False)
    assert gov.before_tool("a", TOOLBOX["run_python"], {"code": "print(1)"})


def test_budget_stops_agent():
    gov = Governor(Policy(max_usd=0.0), verbose=False)
    config.PRICES_PER_MILLION["mock"] = (1000.0, 1000.0)
    try:
        result = get_llm("mock").run_agent(name="a", system="s", task="t",
                                           tools=[TOOLBOX["calculator"]], hooks=gov)
    finally:
        config.PRICES_PER_MILLION["mock"] = (0.0, 0.0)
    assert result.stopped_reason == "budget"


def test_kill_switch(foundry):
    config.KILL_SWITCH_FILE.write_text("stop")
    try:
        assert foundry.run(spec(tools=["calculator"]), "2+2?").stopped_reason.startswith("killed")
    finally:
        config.KILL_SWITCH_FILE.unlink(missing_ok=True)


# ---- foundry: agents building agents -----------------------------------------
def test_architect_designs_valid_agent(foundry):
    designed = foundry.design_agent("summarise meeting notes")
    assert isinstance(designed, AgentSpec)


def test_meta_agent_creates_runs_and_retires(foundry):
    result = foundry.run_orchestrator("Make a tiny plan.")
    assert result.stopped_reason == "done"
    names = [c["tool"] for c in result.tool_calls]
    assert {"create_agent", "run_agent", "retire_agent"} <= set(names)
    created = next(c for c in result.tool_calls if c["tool"] == "create_agent")
    assert created["result"].startswith("Created")


def test_registry_versions(foundry):
    foundry.registry.save(spec("versioned"))
    foundry.registry.save(spec("versioned"))
    assert foundry.registry.get("versioned").version == 2


def test_judge_returns_verdict(foundry):
    verdict = foundry.judge("some work", ["is good"])
    assert {"score", "passed", "feedback"} <= set(verdict)


# ---- every lesson script runs offline (no keys) ------------------------------
MOCK_SCRIPTS = [
    ["lessons/02_prompting/prompt_lab.py"],
    ["lessons/02_prompting/prompt_improver.py", "make me a summary"],
    ["lessons/04_agent_loop/watch_the_loop.py"],
    ["lessons/05_multi_agent_patterns/p1_chain.py"],
    ["lessons/05_multi_agent_patterns/p2_router.py"],
    ["lessons/05_multi_agent_patterns/p3_parallel.py"],
    ["lessons/05_multi_agent_patterns/p4_orchestrator_workers.py"],
    ["lessons/05_multi_agent_patterns/p5_evaluator_optimizer.py"],
    ["lessons/06_agents_that_build_agents/a_architect.py", "--yes"],
    ["lessons/06_agents_that_build_agents/b_meta_agent.py"],
    ["lessons/06_agents_that_build_agents/c_reuse_agents.py"],
    ["lessons/07_controlling_agents/governor_demos.py", "ceiling", "escalation", "headcount",
     "depth", "budget", "killswitch", "audit"],
    ["lessons/07_controlling_agents/audit_report.py"],
    ["lessons/11_evals_and_safety/eval_harness.py"],
    ["lessons/12_capstone_agent_foundry/mission.py", "--yes"],
    ["scripts/check_setup.py"],
]


@pytest.mark.parametrize("command", MOCK_SCRIPTS, ids=lambda c: pathlib.Path(c[0]).stem)
def test_lesson_runs_offline(command, tmp_path_factory):
    data_dir = tmp_path_factory.getbasetemp() / "course-data"  # keeps your real folders clean
    env = {**os.environ, "LLM_PROVIDER": "mock", "PYTHONIOENCODING": "utf-8",
           "COURSE_DATA_DIR": str(data_dir)}
    completed = subprocess.run([sys.executable, *command], cwd=ROOT, env=env,
                               capture_output=True, text=True, encoding="utf-8",
                               input="no\n", timeout=120)
    assert completed.returncode == 0, completed.stdout[-1500:] + completed.stderr[-1500:]
