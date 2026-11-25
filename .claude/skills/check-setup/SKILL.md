---
name: check-setup
description: Check that Python, packages, keys and tools for this course are ready, and fix what is missing step by step.
disable-model-invocation: true
---

1. If there is no `.venv` folder, offer to create it: `uv venv` then `uv pip install -r requirements.txt`, or on a Mac without uv: `python3 -m venv .venv` then `.venv/bin/python -m pip install -r requirements.txt` (ask before running).
2. Run `python scripts/check_setup.py` (prefer `.venv\Scripts\python.exe` on Windows, `.venv/bin/python` on Mac). Never open `.env` yourself.
3. For each ❌ or ⚠️ line, explain in one sentence what it means and the exact fix. Offer to do the fixes that do not involve secrets.
4. For missing API keys: tell the user where to get the key and to paste it into `.env` THEMSELVES (copy `.env.example` to `.env` for them if `.env` does not exist).
5. Finish with which lessons they can run right now with what they have (mock mode, Gemini key, Claude CLI, Anthropic API key).
