"""Drive Claude Code (the CLI) from Python, using your Claude subscription.

This is how a Python script can create Claude Code agents on the fly:
it writes agent definitions to a JSON file and passes them with --agents.

Requirements:
- The Claude Code CLI is installed (docs/SETUP_WINDOWS.md, step 3) and you have
  logged in once by typing `claude` in a terminal.
- Your plan's usage limits apply, exactly as when you chat in VS Code.

Billing note: if ANTHROPIC_API_KEY is set, `claude -p` bills that API key
instead of your subscription. This helper REMOVES the key for the CLI call
unless you pass use_api_key=True.
"""
from __future__ import annotations

import json
import os
import shutil
import subprocess
import tempfile
from pathlib import Path


class ClaudeCLIError(RuntimeError):
    pass


def find_claude() -> str:
    exe = shutil.which("claude")
    if not exe:
        raise ClaudeCLIError(
            "The `claude` command was not found.\n"
            "Install the Claude Code CLI (PowerShell):  irm https://claude.ai/install.ps1 | iex\n"
            "then open a NEW terminal, type `claude`, and log in once."
        )
    return exe


def run_claude(prompt: str, *, cwd: str | Path | None = None,
               allowed_tools: list[str] | None = None,
               permission_mode: str = "dontAsk",
               max_turns: int | None = None,
               max_budget_usd: float | None = None,
               agents: dict | None = None,
               json_schema: dict | None = None,
               append_system_prompt: str | None = None,
               model: str | None = None,
               use_api_key: bool = False,
               timeout: int = 1800) -> dict:
    """Run `claude -p` once and return its JSON result as a dict.

    Useful keys in the result: "result" (the final text), "num_turns",
    "total_cost_usd" (an estimate), "is_error", "structured_output" (with json_schema).

    permission_mode="dontAsk" means: tools in allowed_tools run, everything
    else is refused automatically. Nothing can wait for a human click.
    """
    cmd = [find_claude(), "-p", "--output-format", "json", "--permission-mode", permission_mode]
    if allowed_tools:
        cmd += ["--allowedTools", ",".join(allowed_tools)]
    if max_turns:
        cmd += ["--max-turns", str(max_turns)]
    if max_budget_usd:
        cmd += ["--max-budget-usd", str(max_budget_usd)]
    if model:
        cmd += ["--model", model]
    if append_system_prompt:
        cmd += ["--append-system-prompt", append_system_prompt]
    if json_schema:
        cmd += ["--json-schema", json.dumps(json_schema)]

    agents_file = None
    if agents:
        # Pass the agent definitions as a file: safer than quoting JSON on Windows.
        agents_file = tempfile.NamedTemporaryFile("w", suffix=".json", delete=False,
                                                  encoding="utf-8")
        json.dump(agents, agents_file, indent=2)
        agents_file.close()
        cmd += ["--agents", agents_file.name]

    env = dict(os.environ)
    if not use_api_key:
        env.pop("ANTHROPIC_API_KEY", None)   # use the subscription login instead

    try:
        completed = subprocess.run(cmd, input=prompt, cwd=cwd, env=env, capture_output=True,
                                   text=True, encoding="utf-8", timeout=timeout)
    finally:
        if agents_file:
            Path(agents_file.name).unlink(missing_ok=True)

    raw = completed.stdout.strip()
    if not raw:
        raise ClaudeCLIError(f"claude returned no output. stderr:\n{completed.stderr[-2000:]}")
    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        # Some versions print one JSON object per line: keep the final "result" one.
        lines = [json.loads(line) for line in raw.splitlines() if line.strip().startswith("{")]
        data = next((d for d in reversed(lines) if d.get("type") == "result"), lines[-1])
    if isinstance(data, list):
        data = next((d for d in reversed(data) if d.get("type") == "result"), data[-1])
    return data
