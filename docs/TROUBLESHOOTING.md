# Troubleshooting

**First move for any error:** paste it into Claude Code with this prompt:

> *"I got this error. Explain in plain English what it means, what probably caused it, and fix it step by step. Show me each command before you run it. Don't open my .env file.*
> *[paste the full error here, including the lines above it]"*

Or type `/check-setup` to re-check everything.

---

| # | Problem (what you see) | Likely cause | Fix |
|---|---|---|---|
| 1 | `claude : The term 'claude' is not recognized` | CLI not installed, or terminal opened before installing | Install: `irm https://claude.ai/install.ps1 \| iex`, then **open a new terminal**. The VS Code extension alone does not add `claude` to PATH. |
| 2 | `python is not recognized` / Microsoft Store opens | Python not installed or not on PATH | Reinstall Python 3.12 and tick **Add python.exe to PATH**; or use `.venv\Scripts\python.exe` directly. |
| 3 | `uv is not recognized` | uv not installed / new terminal needed | `winget install astral-sh.uv`, open a new terminal. Or use `python -m pip install -r requirements.txt`. |
| 4 | `ModuleNotFoundError: No module named 'google'` (or `anthropic`, `rich`…) | Packages not installed, or wrong Python used | `uv pip install -r requirements.txt`, and run with `.venv\Scripts\python.exe`. In VS Code pick the `.venv` interpreter (bottom right). |
| 5 | "Hook error" messages in Claude Code after every action | `python` not on PATH for hooks, or Git Bash missing | Install Git for Windows and make sure `python --version` works in a new terminal. If needed ask Claude Code: *"Temporarily disable the hooks in .claude/settings.json"*. |
| 6 | Everything says "BLOCKED… kill switch is ON" | A file named `STOP` exists in the repo root | Delete `STOP` yourself in the VS Code Explorer (only a human should). |
| 7 | `Offline practice mode (mock model): answers are fake` | No API key found, so the course uses the free mock | Add `GOOGLE_API_KEY=` to `.env` (Setup step 8), or set `LLM_PROVIDER=gemini`. |
| 8 | Gemini: `API key not valid` / `PERMISSION_DENIED` | Key typo, extra spaces/quotes, or key deleted | Re-copy the key from https://aistudio.google.com/apikey; in `.env` write `GOOGLE_API_KEY=AIza...` (no quotes, no spaces). |
| 9 | Gemini: `404 … model not found` | Model name retired or misspelled | In `.env` set `GEMINI_MODEL=gemini-flash-latest` (and `GEMINI_WORKER_MODEL`). |
| 10 | `429` / `RESOURCE_EXHAUSTED` / "rate limit" | Free-tier requests-per-minute or per-day limit reached | Wait a minute; use fewer agents/turns; run mock mode for practice; try again tomorrow for daily limits. |
| 11 | Anthropic: `401 authentication_error` | Missing/wrong `ANTHROPIC_API_KEY` | Check the key in `.env`; or leave it empty and use Gemini/mock. A Claude subscription is not an API key. |
| 12 | Anthropic: "credit balance is too low" | No prepaid credit on the API account | Add credit in the Anthropic Console, or leave the key empty (lessons fall back to Gemini). |
| 13 | Unexpected API charges from `claude -p` | `ANTHROPIC_API_KEY` was set in the environment, so headless mode billed the API | The course helper removes the key automatically; for manual runs in PowerShell: `Remove-Item Env:ANTHROPIC_API_KEY`. Avoid `--bare` with a subscription. |
| 14 | `claude -p` asks to log in / returns an auth error | CLI never logged in on this computer | Run `claude` once in a terminal and complete login. |
| 15 | Script seems frozen | It is waiting for your **yes/no** approval (Governor or a human-review step) | Look at the terminal and answer. Add `--yes` where a lesson supports it. |
| 16 | `PermissionError: Agents may only use files inside the workspace/ folder` | An agent tried a path outside `workspace/` | Working as designed. Put files the agent needs into `workspace/`. |
| 17 | `ERROR: 'site.com' is not on the allowlist` | `fetch_webpage` only opens allow-listed sites | Add the domain to `WEB_ALLOWLIST` in `.env` (comma separated), only if you trust it. |
| 18 | `REFUSED by the Governor: …` | A limit or rule was hit (headcount, depth, tools, escalation) | Working as designed. Read the reason; loosen the `Policy` in that lesson only if it makes sense. |
| 19 | `stopped: budget` | The run reached `MAX_USD_PER_RUN` | Raise `MAX_USD_PER_RUN` in `.env` carefully, or use cheaper worker models / mock mode. |
| 20 | `adk web` shows no agents / "no root_agent" | Started from the wrong folder | `cd lessons/09_google_adk` first, then `adk web`; pick **adk_team** top-left. |
| 21 | `adk` is not recognized | ADK not installed in the active environment | `uv pip install google-adk`; run `.venv\Scripts\adk.exe web` or activate the venv. |
| 22 | `/mcp` shows **agent-registry** failed/disconnected | Wrong Python path, or the server crashed | Re-add: `claude mcp add agent-registry -- .venv\Scripts\python.exe lessons\10_mcp\agent_registry_server.py` from the repo folder; test it alone with `python lessons/10_mcp/agent_registry_server.py` (it should wait silently; Ctrl+C to exit). |
| 23 | MCP server worked, then broke after an edit | Something `print()`s to stdout | MCP servers must never print to stdout; log to stderr or a file instead. |
| 24 | `UnicodeEncodeError` / strange symbols in the console | Old Windows console encoding | Use Windows Terminal or VS Code's terminal; or run `chcp 65001` first. |
| 25 | Agent SDK (lesson 08b): "ANTHROPIC_API_KEY is not set" | The SDK requires an API key | Add a key, or use `cli_agent_factory.py` (subscription) instead. |
| 26 | `python -m pytest` fails | A change broke something, or packages missing | Ask: *"Run the tests and explain the failures simply, then fix them."* (the `test-runner` subagent). |
| 27 | New subagent isn't used | Vague `description`, or file not in `.claude/agents/` | Name it explicitly: *"Use the X agent to…"*; improve its description with trigger words. Files are reloaded within seconds. |
| 28 | Claude Code "usage limit reached" | Plan usage window used up (big multi-agent runs use more) | Check `/usage`; wait for the window to reset; run smaller teams. |
| 29 | `git clone` asks for a password | Private repo or no GitHub login | The course repo is public; check the URL. For your own private repos sign in with GitHub Desktop or `gh auth login`. |
| 30 | VS Code doesn't find the `.venv` interpreter | Interpreter not selected | Command Palette → **Python: Select Interpreter** → `.venv\Scripts\python.exe`. |

---

## Still stuck?
1. Run `python scripts/check_setup.py --live` (makes tiny test calls) and share the output with Claude Code.
2. Ask the `code-explainer` subagent: *"Use code-explainer to explain this error: …"*
3. Rewind: hover over an earlier message in Claude Code and rewind the code to before the problem started.
