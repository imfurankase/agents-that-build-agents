"""Check that everything needed for the course is installed and configured.

Run it:  python scripts/check_setup.py
         python scripts/check_setup.py --live     (also makes one tiny test call per provider)

It never prints your API keys - only whether they are set.
"""
import importlib
import os
import pathlib
import shutil
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

for stream in (sys.stdout, sys.stderr):
    try:
        stream.reconfigure(encoding="utf-8")
    except Exception:
        pass

OK, WARN, BAD = "✅", "⚠️ ", "❌"
problems = 0


def report(status: str, what: str, fix: str = "") -> None:
    global problems
    print(f"{status} {what}")
    if fix:
        print(f"     -> {fix}")
    if status == BAD:
        problems += 1


print("\n=== Agents That Build Agents - setup check ===\n")

# 1. Python
version = sys.version_info
if version >= (3, 10):
    report(OK, f"Python {version.major}.{version.minor}")
else:
    report(BAD, f"Python {version.major}.{version.minor} is too old", "Install Python 3.12 (docs/SETUP_WINDOWS.md)")

in_venv = sys.prefix != getattr(sys, "base_prefix", sys.prefix)
report(OK if in_venv else WARN, "Running inside a virtual environment" if in_venv
       else "Not inside the course's virtual environment",
       "" if in_venv else "Use .venv\\Scripts\\python.exe (or ask Claude Code: 'activate the venv')")

# 2. Packages
for package, module in [("anthropic", "anthropic"), ("google-genai", "google.genai"),
                        ("google-adk", "google.adk"), ("claude-agent-sdk", "claude_agent_sdk"),
                        ("mcp", "mcp"), ("pydantic", "pydantic"), ("python-dotenv", "dotenv"),
                        ("rich", "rich"), ("python-telegram-bot", "telegram"),
                        ("icalendar", "icalendar"), ("recurring-ical-events", "recurring_ical_events")]:
    try:
        importlib.import_module(module)
        report(OK, f"package {package}")
    except Exception:
        report(BAD, f"package {package} is missing", "Run: uv pip install -r requirements.txt")

# 3. .env and keys
env_file = ROOT / ".env"
if env_file.exists():
    report(OK, ".env file exists")
else:
    report(BAD, ".env file is missing", "Copy .env.example to .env, then add your key(s)")

try:
    from common import config
    has_claude = bool(os.getenv("ANTHROPIC_API_KEY"))
    has_gemini = bool(os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY"))
    report(OK if has_gemini else WARN, "Google AI Studio key " + ("is set" if has_gemini else "is NOT set"),
           "" if has_gemini else "Free key: https://aistudio.google.com/apikey -> GOOGLE_API_KEY= in .env")
    report(OK if has_claude else WARN, "Anthropic API key " + ("is set" if has_claude else "is NOT set (optional)"),
           "" if has_claude else "Optional. Only needed for *_claude_api / SDK lessons. A Claude subscription is not an API key.")
    report(OK, f"Python lessons will use provider: {config.PROVIDER}"
               + ("  (offline practice mode - free)" if config.PROVIDER == "mock" else ""))
except Exception as exc:
    report(BAD, f"Could not load settings: {exc}")

# 4. Command-line tools (install tips differ on Windows and Mac)
ON_MAC = sys.platform == "darwin"
VENV_BIN = pathlib.Path(sys.executable).parent  # tools installed into .venv live here
for command, why, win_fix, mac_fix in [
    ("claude", "Claude Code CLI (for lesson 01c, 08, 10)",
     "PowerShell: irm https://claude.ai/install.ps1 | iex   then open a NEW terminal",
     "Terminal: curl -fsSL https://claude.ai/install.sh | bash   then open a NEW terminal"),
    ("git", "Git (version history, GitHub)", "Install Git for Windows: https://git-scm.com",
     "Terminal: xcode-select --install"),
    ("uv", "uv (fast Python package manager)", "PowerShell: winget install astral-sh.uv",
     "Optional: brew install uv   (python3 -m venv works too)"),
    ("adk", "Google ADK command (lesson 09)", "Run: uv pip install google-adk",
     "Run: .venv/bin/python -m pip install google-adk"),
    ("node", "Node.js (optional: MCP Inspector)", "Optional: winget install OpenJS.NodeJS.LTS",
     "Optional: brew install node"),
]:
    fix = mac_fix if ON_MAC else win_fix
    path = shutil.which(command) or shutil.which(command, path=str(VENV_BIN))
    report(OK if path else (WARN if command in ("node", "uv") else BAD),
           f"{why}" + ("" if path else " - not found"), "" if path else fix)

# 5. Optional live test
if "--live" in sys.argv:
    print("\n--- live test (tiny calls) ---")
    from common.llm import get_llm
    for provider in ("gemini", "claude"):
        try:
            text, usage = get_llm(provider).complete("Reply with one word.", "Say OK", effort="low")
            report(OK, f"{provider} answered: {text.strip()[:40]}")
        except Exception as exc:
            report(WARN, f"{provider} test skipped/failed: {type(exc).__name__}: {str(exc)[:120]}")
    if shutil.which("claude"):
        try:
            from common.claude_cli import run_claude
            result = run_claude("Reply with the single word OK.", allowed_tools=[], max_turns=2,
                                timeout=180)
            report(OK, f"Claude Code CLI answered: {str(result.get('result'))[:40]}")
        except Exception as exc:
            report(WARN, f"Claude Code CLI test failed: {str(exc)[:160]}",
                   "Open a terminal, type `claude`, and log in once.")

print(f"\n{'All good! 🎉' if problems == 0 else f'{problems} problem(s) to fix above.'}\n")
