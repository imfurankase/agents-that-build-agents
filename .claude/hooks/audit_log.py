"""Claude Code PreToolUse hook: write every tool call to logs/claude_code_audit.jsonl.

This gives you an audit trail of what Claude Code (and its subagents) did,
just like the Python Governor's logs. Read it with the /audit skill.
Never blocks anything (always exits 0).
"""
import datetime
import json
import os
import pathlib
import sys


def main() -> None:
    data = json.load(sys.stdin)
    project = pathlib.Path(os.environ.get("CLAUDE_PROJECT_DIR") or data.get("cwd") or ".")
    tool_input = data.get("tool_input") or {}
    summary = {k: (str(v)[:200]) for k, v in tool_input.items()
               if k in ("command", "file_path", "path", "pattern", "url", "query",
                        "description", "subagent_type", "prompt")}
    record = {
        "time": datetime.datetime.now().isoformat(timespec="seconds"),
        "session": data.get("session_id", "")[:8],
        "tool": data.get("tool_name"),
        "input": summary,
    }
    logs = project / "logs"
    logs.mkdir(exist_ok=True)
    with (logs / "claude_code_audit.jsonl").open("a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")


if __name__ == "__main__":
    try:
        main()
    except Exception:
        pass
    sys.exit(0)
