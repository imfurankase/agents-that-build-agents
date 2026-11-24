"""Lesson 08a - A script that DESIGNS Claude Code subagents, then RUNS them.
Uses your Claude subscription (no API key).

Run it:  python lessons/08_claude_code_agents/cli_agent_factory.py "your goal"
         add --yes  to skip the approval question
         add --save to also save the new agents into .claude/agents/ so you can
                    use them later in VS Code ("use the <name> agent to ...")

Example: python lessons/08_claude_code_agents/cli_agent_factory.py "Research 3 recent public examples of governments using AI agents and write a 1-page summary to summary.md" --save

How it works:
  Step 1  Claude Code is asked to act as an architect and return a JSON list of
          subagents (name, description, prompt, tools). --json-schema guarantees
          the shape of the answer.
  Step 2  You approve the team (the human stays in charge).
  Step 3  Claude Code runs the goal with those subagents loaded via --agents.
          It works inside its own folder: workspace/cli_runs/<time>/
          Permission mode "dontAsk" = only the listed tools can run.
"""
import datetime
import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))

from common import config, show
from common.claude_cli import ClaudeCLIError, run_claude

# The only Claude Code tools the generated agents may use (least privilege).
SAFE_TOOLS = ["Read", "Glob", "Grep", "Write", "Edit", "WebSearch", "WebFetch"]

DESIGN_SCHEMA = {
    "type": "object",
    "properties": {
        "plan": {"type": "string"},
        "agents": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "name": {"type": "string"},
                    "description": {"type": "string"},
                    "prompt": {"type": "string"},
                    "tools": {"type": "array", "items": {"type": "string", "enum": SAFE_TOOLS}},
                },
                "required": ["name", "description", "prompt", "tools"],
                "additionalProperties": False,
            },
        },
    },
    "required": ["plan", "agents"],
    "additionalProperties": False,
}

DESIGN_PROMPT = """You are an agent architect for Claude Code. Design the SMALLEST team of
specialist subagents (2 or 3) that would help achieve the goal below. Do not do the work.

For each subagent:
- name: lowercase-with-dashes
- description: one sentence saying WHEN to use it (Claude reads this to decide delegation)
- prompt: its full system prompt, written to the subagent ("You are..."), with a method,
  an output format, and boundaries
- tools: the fewest tools it needs from the allowed list

Goal: {goal}"""

args = [a for a in sys.argv[1:] if not a.startswith("--")]
goal = " ".join(args) or ("Write a one-page plain-English explainer called explainer.md on "
                          "what an 'AI agent' is, with one real-world example, then have it "
                          "fact-checked and improved.")
auto_yes, save = "--yes" in sys.argv, "--save" in sys.argv

try:
    # ---------- Step 1: design the team ----------
    show.title("Step 1 - Claude Code designs a team of subagents")
    design = run_claude(DESIGN_PROMPT.format(goal=goal), allowed_tools=[], max_turns=3,
                        json_schema=DESIGN_SCHEMA)
    team = design.get("structured_output") or json.loads(design.get("result", "{}"))
    agents = {a["name"]: {"description": a["description"], "prompt": a["prompt"],
                          "tools": a["tools"]} for a in team["agents"][:4]}
    show.panel(team["plan"], "Plan")
    for name, a in agents.items():
        show.panel(f"{a['description']}\n\ntools: {a['tools']}\n\n{a['prompt'][:700]}",
                   f"subagent: {name}", "cyan")

    # ---------- Step 2: human approval ----------
    if not auto_yes and input("Run the goal with this team? (yes/no): ").strip().lower() not in ("y", "yes"):
        sys.exit("Stopped before running. Nothing was executed.")

    # ---------- Step 3: run with the new agents ----------
    run_dir = config.WORKSPACE / "cli_runs" / datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    run_dir.mkdir(parents=True)
    (run_dir / "team.json").write_text(json.dumps(agents, indent=2), encoding="utf-8")
    show.title(f"Step 3 - running in {config.rel(run_dir)}")
    show.info("This can take a few minutes. Claude Code is delegating to the new subagents...")
    result = run_claude(
        f"{goal}\n\nDelegate the specialist work to your subagents "
        f"({', '.join(agents)}). Save any files in the current folder. "
        f"Finish with a short report of what each subagent did.",
        agents=agents,
        allowed_tools=["Agent", *SAFE_TOOLS],
        permission_mode="dontAsk",
        max_turns=40,
        cwd=run_dir,
    )
except ClaudeCLIError as problem:
    sys.exit(str(problem))

show.panel(result.get("result", "(no result)"), f"Result ({result.get('subtype')})", "green")
stats = result.get("subagent_stats") or {}
show.info(f"turns: {result.get('num_turns')} | subagents spawned: {stats.get('spawned', '?')} | "
          f"files: {[p.name for p in run_dir.iterdir()]}")

# ---------- Optional: keep the agents for VS Code ----------
if save:
    agent_dir = config.ROOT / ".claude" / "agents"
    for name, a in agents.items():
        path = agent_dir / f"{name}.md"
        path.write_text(
            f"---\nname: {name}\ndescription: {a['description']}\n"
            f"tools: {', '.join(a['tools'])}\n---\n\n{a['prompt']}\n", encoding="utf-8")
        show.info(f"saved {config.rel(path)} - use it in VS Code by name")
