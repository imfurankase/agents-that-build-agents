"""Lesson 01c - Ask Claude Code a question FROM A SCRIPT (uses your subscription).

Run it:     python lessons/01_first_call/hello_claude_code.py
Needs:      The Claude Code CLI installed and logged in (docs/SETUP_WINDOWS.md).
            No API key needed: this uses your Claude Pro/Max plan.

What to notice:
- This is the same Claude Code you use in VS Code, but driven by a program.
  Later (lesson 08) a script uses this to CREATE agents and run them.
- "headless mode" = `claude -p "your prompt"`. You can type that in a terminal too.
- Each call loads Claude Code's full toolkit (~45K tokens of context), so
  calls are heavy. Do not run this in a loop hundreds of times.
"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))

from common.claude_cli import ClaudeCLIError, run_claude

try:
    result = run_claude(
        "In 3 bullet points, explain what an AI agent is to a busy executive. "
        "Plain English, no jargon.",
        allowed_tools=[],          # no tools needed: just answer
        max_turns=2,
    )
except ClaudeCLIError as problem:
    print(problem)
    sys.exit(1)

print(result.get("result", "(no text returned)"))
print(f"\n[turns: {result.get('num_turns')} | finished: {result.get('subtype')} "
      f"| API-equivalent cost estimate: ${result.get('total_cost_usd', 0):.3f} "
      f"(on a subscription this counts toward your plan limits instead)]")
