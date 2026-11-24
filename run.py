"""Course launcher: run any lesson by number.

    python run.py            -> show the menu
    python run.py 6b         -> run lesson 06b (the meta-agent)
    python run.py 6b "goal"  -> run it with your own goal
    python run.py check      -> check your setup

Tip: in Claude Code you can simply type  /run-lesson 6b
"""
import pathlib
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parent
L = "lessons/"

MENU = {
    "check": ("scripts/check_setup.py", "Check your setup (keys, packages, tools)"),
    "1a": (L + "01_first_call/hello_gemini.py", "First call to Gemini (free key)"),
    "1b": (L + "01_first_call/hello_claude_api.py", "First call to the Claude API (API key)"),
    "1c": (L + "01_first_call/hello_claude_code.py", "Claude Code from a script (subscription)"),
    "2a": (L + "02_prompting/prompt_lab.py", "Weak vs strong prompt, side by side"),
    "2b": (L + "02_prompting/prompt_improver.py", "AI that improves your prompts"),
    "3a": (L + "03_tools/gemini_tools.py", "Gemini with tools"),
    "3b": (L + "03_tools/claude_tools.py", "Claude with tools (API key)"),
    "4a": (L + "04_agent_loop/mini_agent_gemini.py", "Agent loop from scratch (Gemini)"),
    "4b": (L + "04_agent_loop/mini_agent_claude.py", "Agent loop from scratch (Claude API)"),
    "4c": (L + "04_agent_loop/watch_the_loop.py", "Watch the loop step by step (any provider)"),
    "5a": (L + "05_multi_agent_patterns/p1_chain.py", "Pattern: chain"),
    "5b": (L + "05_multi_agent_patterns/p2_router.py", "Pattern: router"),
    "5c": (L + "05_multi_agent_patterns/p3_parallel.py", "Pattern: parallel"),
    "5d": (L + "05_multi_agent_patterns/p4_orchestrator_workers.py", "Pattern: orchestrator-workers"),
    "5e": (L + "05_multi_agent_patterns/p5_evaluator_optimizer.py", "Pattern: evaluator-optimizer"),
    "6a": (L + "06_agents_that_build_agents/a_architect.py", "Architect designs a new agent"),
    "6b": (L + "06_agents_that_build_agents/b_meta_agent.py", "Meta-agent hires its own team"),
    "6c": (L + "06_agents_that_build_agents/c_reuse_agents.py", "List / reuse / improve saved agents"),
    "7a": (L + "07_controlling_agents/governor_demos.py", "Every control, demonstrated"),
    "7b": (L + "07_controlling_agents/strict_meta_agent.py", "Meta-agent under a strict policy"),
    "7c": (L + "07_controlling_agents/audit_report.py", "Readable report of the last run"),
    "8a": (L + "08_claude_code_agents/cli_agent_factory.py", "Script designs + runs Claude Code subagents"),
    "8b": (L + "08_claude_code_agents/sdk_subagents.py", "Claude Agent SDK team (API key)"),
    "9b": (L + "09_google_adk/dynamic_team.py", "ADK team built at run time"),
    "10": (L + "10_mcp/agent_registry_server.py", "MCP server (normally started by Claude Code)"),
    "11a": (L + "11_evals_and_safety/eval_harness.py", "Test an agent with an eval suite"),
    "11b": (L + "11_evals_and_safety/injection_demo.py", "Prompt-injection drill"),
    "12": (L + "12_capstone_agent_foundry/mission.py", "CAPSTONE: full governed mission"),
}

if len(sys.argv) < 2 or sys.argv[1] not in MENU:
    print(__doc__)
    for key, (_, description) in MENU.items():
        print(f"  {key:<6} {description}")
    print("\n  9a     ADK web UI: cd lessons/09_google_adk  then  adk web")
    sys.exit(0)

script, _ = MENU[sys.argv[1]]
sys.exit(subprocess.call([sys.executable, str(ROOT / script), *sys.argv[2:]], cwd=ROOT))
