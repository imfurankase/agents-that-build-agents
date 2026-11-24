"""Settings for the whole course, read from the `.env` file in the repo root.

You normally never edit this file. Change values in `.env` instead
(copy `.env.example` to `.env` first).
"""
from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv

# The repo root folder (the folder that contains README.md).
ROOT = Path(__file__).resolve().parents[1]

# Load .env into the environment so every SDK can find its API key.
load_dotenv(ROOT / ".env")


def _setting(name: str, default: str) -> str:
    value = os.getenv(name)
    return value.strip() if value and value.strip() else default


# Which company's model the Python lessons use:
#   "auto"   - Claude if ANTHROPIC_API_KEY is set, else Gemini if a Google key
#              is set, else the free offline mock (the default)
#   "claude" - Anthropic API (needs an API key from platform.claude.com;
#              a Claude Pro/Max subscription is NOT an API key)
#   "gemini" - Google AI Studio API key (has a free tier)
#   "mock"   - a fake, offline model: free, no key needed, good for practice
def _resolve_provider(choice: str) -> str:
    if choice != "auto":
        return choice
    if os.getenv("ANTHROPIC_API_KEY"):
        return "claude"
    if os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY"):
        return "gemini"
    return "mock"


PROVIDER = _resolve_provider(_setting("LLM_PROVIDER", "auto").lower())

# Claude models (Anthropic). Main = smartest; worker = used by sub-agents.
# To spend less, you may set CLAUDE_WORKER_MODEL to claude-sonnet-5-5 or
# claude-haiku-5-5 in your .env. That is your call, not the code's.
CLAUDE_MODEL = _setting("CLAUDE_MODEL", "claude-opus-5-5")
CLAUDE_WORKER_MODEL = _setting("CLAUDE_WORKER_MODEL", "claude-opus-5-5")

# Gemini models (Google AI Studio). "gemini-flash-latest" always points to
# Google's newest Flash model, so this keeps working as versions change.
GEMINI_MODEL = _setting("GEMINI_MODEL", "gemini-flash-latest")
GEMINI_WORKER_MODEL = _setting("GEMINI_WORKER_MODEL", "gemini-flash-latest")

# Your home city / country, used by the weather and holiday tools when no place is given.
HOME_CITY = _setting("HOME_CITY", "London")
HOME_COUNTRY_CODE = _setting("HOME_COUNTRY_CODE", "GB")

# Safety limits used by the Governor (lesson 07) unless a script overrides them.
MAX_USD_PER_RUN = float(_setting("MAX_USD_PER_RUN", "1.00"))
MAX_AGENTS_PER_RUN = int(_setting("MAX_AGENTS_PER_RUN", "6"))
MAX_SPAWN_DEPTH = int(_setting("MAX_SPAWN_DEPTH", "2"))

# Websites the fetch_webpage tool may open (comma separated). Least privilege!
WEB_ALLOWLIST = [
    d.strip().lower()
    for d in _setting(
        "WEB_ALLOWLIST",
        "en.wikipedia.org,docs.python.org,ai.google.dev,docs.claude.com,code.claude.com",
    ).split(",")
    if d.strip()
]

# Folders the course uses. (Tests set COURSE_DATA_DIR to keep your real
# folders clean; you never need to set it yourself.)
DATA = Path(os.environ["COURSE_DATA_DIR"]) if os.getenv("COURSE_DATA_DIR") else ROOT
WORKSPACE = DATA / "workspace"          # the only folder agents may read/write
LOGS = DATA / "logs"                    # audit logs (one file per run)
REGISTRY_DIR = DATA / "agent_registry"  # saved agent specs (JSON files)
KILL_SWITCH_FILE = ROOT / "STOP"        # create this file to stop all agents

for _folder in (WORKSPACE, LOGS, REGISTRY_DIR):
    _folder.mkdir(parents=True, exist_ok=True)


def rel(path: Path) -> str:
    """Show a path relative to the repo folder when possible (shorter to read)."""
    try:
        return Path(path).resolve().relative_to(ROOT).as_posix()
    except ValueError:
        return str(path)

# Rough prices in US dollars per 1 million tokens: (input, output).
# Claude prices are Anthropic's list prices. Gemini numbers are a cautious
# placeholder; check https://ai.google.dev/pricing for the real figure.
# The free tier of Google AI Studio costs $0 within its rate limits.
PRICES_PER_MILLION = {
    "claude-opus-5-5": (4.00, 20.00),
    "claude-sonnet-5-5": (2.00, 10.00),
    "claude-haiku-5-5": (0.10, 0.50),
    "claude-fable-5-2": (8.00, 40.00),
    "gemini": (0.50, 3.00),   # placeholder for any gemini-* model
    "mock": (0.0, 0.0),
}


def price_for(model: str) -> tuple[float, float]:
    """Return (input, output) price per million tokens for a model name."""
    if model in PRICES_PER_MILLION:
        return PRICES_PER_MILLION[model]
    if model.startswith("gemini"):
        return PRICES_PER_MILLION["gemini"]
    if model.startswith("mock"):
        return PRICES_PER_MILLION["mock"]
    return PRICES_PER_MILLION["claude-opus-5-5"]  # unknown: assume the pricier side


def cost_usd(model: str, input_tokens: int, output_tokens: int) -> float:
    price_in, price_out = price_for(model)
    return (input_tokens * price_in + output_tokens * price_out) / 1_000_000
