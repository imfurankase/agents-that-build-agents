"""Claude Code PreToolUse hook: the project's guard rails.

Claude Code runs this BEFORE every Bash / Write / Edit / Agent tool call and
sends the details as JSON on stdin. If this script exits with code 2, the call
is BLOCKED and the message printed to stderr is shown to Claude.

Rules:
  1. Kill switch: if a file named STOP exists in the project root, block everything
     that changes things (commands, edits, starting subagents).
  2. Never let commands read or print the .env file (where API keys live).
  3. Block a short list of clearly destructive commands.

Fails OPEN: if anything goes wrong inside this script, it allows the action
(exit 0) so a bug here can never lock you out of your own project.
"""
import json
import os
import pathlib
import re
import sys

DANGEROUS = [
    (r"\brm\s+-[a-z]*r[a-z]*f?\s+(/|~|\*|\.\s*$)", "recursive delete of a top-level folder"),
    (r"Remove-Item\b.*-Recurse.*\s([A-Za-z]:\\?|~|\\)\s*$", "recursive delete of a drive or home folder"),
    (r"\bformat\s+[a-z]:", "formatting a drive"),
    (r"\bgit\s+push\b.*--force", "force-pushing over shared history"),
    (r"\bgit\s+reset\s+--hard\b", "discarding all uncommitted work"),
    (r"(cat|type|more|less|head|tail|Get-Content|gc|notepad|code)\s+[^|;&]*\.env\b(?!\.example)",
     "reading the .env file (API keys)"),
]


def block(reason: str) -> None:
    print(f"BLOCKED by project guard: {reason}", file=sys.stderr)
    sys.exit(2)


def main() -> None:
    data = json.load(sys.stdin)
    tool = data.get("tool_name", "")
    tool_input = data.get("tool_input") or {}
    project = pathlib.Path(os.environ.get("CLAUDE_PROJECT_DIR") or data.get("cwd") or ".")

    if (project / "STOP").exists():
        block("the kill switch is ON (a file named STOP exists in the project root). "
              "Tell the human; only they should delete STOP to resume.")

    if tool == "Bash" or tool == "PowerShell":
        command = str(tool_input.get("command", ""))
        for pattern, why in DANGEROUS:
            if re.search(pattern, command, flags=re.IGNORECASE):
                block(f"{why}. Ask the human to run this themselves if it is really intended.")


if __name__ == "__main__":
    try:
        main()
    except SystemExit:
        raise
    except Exception:
        sys.exit(0)  # fail open
