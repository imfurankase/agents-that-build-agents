# Setup on Windows (step by step)

On a Mac? Follow [SETUP_MAC.md](SETUP_MAC.md) instead.

Allow about **45 minutes** the first time. Tick each box as you go.

> **The 5-minute version:** if VS Code with the Claude Code extension is already installed, open this course folder in VS Code, open the Claude Code panel and type **`/check-setup`**. Claude Code will check everything below and walk you through whatever is missing.

---

## What each thing is for

| Tool | What it does for you | Needed for |
|---|---|---|
| **VS Code + Claude Code extension** | Where you work: you chat with Claude Code and it reads, runs and edits the course for you | Everything |
| **Git for Windows** | Version history and downloading the course. It also provides "Git Bash", which Claude Code uses to run commands and hooks | Everything |
| **Claude Code CLI** | Claude Code in a terminal. Lets scripts drive Claude Code (`claude -p`) | Lessons 01c, 08a, 10 |
| **Python 3.12** | Runs the course's Python agents | Lessons 01-12 |
| **uv** | Fast, simple Python package installer | Installing the course packages |
| **Google AI Studio key** | Free key for Gemini models | Real answers in the Python lessons, ADK (lesson 09) |
| **Anthropic API key** *(optional)* | Pay-per-token access to Claude from Python | `*_claude_api` lessons, Agent SDK (08b) |
| **PyCharm** *(optional)* | A second editor if you prefer it | Nothing extra |
| **Node.js LTS** *(optional)* | Runs the MCP Inspector tool | Lesson 10 extras |

---

## Step 1: VS Code and the Claude Code extension
- [ ] Install **VS Code** (version 1.94 or newer) from https://code.visualstudio.com
- [ ] In VS Code, open **Extensions** (the four-squares icon on the left), search **"Claude Code"** and install the extension published by **Anthropic** (ID: `anthropic.claude-code`).
- [ ] Open the Claude Code panel (Claude icon in the side bar) and **sign in** with your Claude account (Pro or Max plan).

> The extension does **not** add the `claude` command to your terminal. That is what Step 3 is for.

## Step 2: Git for Windows
- [ ] Install from https://git-scm.com/download/win (accept the defaults), **or** in PowerShell:
  ```powershell
  winget install Git.Git
  ```
- [ ] Why: Claude Code uses Git Bash to run commands and the course's safety hooks. Without it, Claude Code falls back to PowerShell and some hooks may show errors.

## Step 3: Claude Code CLI (the terminal version)
- [ ] Open **PowerShell** and run the official installer:
  ```powershell
  irm https://claude.ai/install.ps1 | iex
  ```
  Alternative: `winget install Anthropic.ClaudeCode` (note: the winget version does not update itself; run `winget upgrade Anthropic.ClaudeCode` now and then).
- [ ] **Close and reopen** the terminal (so Windows sees the new command).
- [ ] Type `claude` and follow the login steps once. Then exit with `/exit`.
- [ ] Check: `claude --version` prints a version number.

> **Billing note:** the CLI uses your Claude subscription. If an `ANTHROPIC_API_KEY` environment variable is set, `claude -p` (headless mode) bills that API key instead. The course's helper removes the key for these calls so you don't pay twice by accident.

## Step 4: Python 3.12
- [ ] Download Python 3.12 from https://www.python.org/downloads/ and, on the first installer screen, **tick "Add python.exe to PATH"**. Or in PowerShell:
  ```powershell
  winget install Python.Python.3.12
  ```
- [ ] Open a new terminal and check: `python --version` shows 3.12.x.

## Step 5: uv (package installer)
- [ ] In PowerShell:
  ```powershell
  winget install astral-sh.uv
  ```
  or
  ```powershell
  powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
  ```
- [ ] New terminal, check: `uv --version`.

## Step 6: Get the course
- [ ] In a terminal, go to where you keep projects (e.g. `cd $HOME\Documents`) and run:
  ```powershell
  git clone https://github.com/imfurankase/agents-that-build-agents.git
  ```
- [ ] In VS Code: **File → Open Folder…** → choose `agents-that-build-agents`. If VS Code asks whether you trust the authors, choose **Yes, I trust**.
- [ ] Accept the prompt to install the **recommended extensions** (Claude Code, Python).

## Step 7: Install the course packages
Easiest: in the Claude Code panel type **`/check-setup`** and say yes when it offers to create the environment.

Or yourself, in VS Code's terminal (**Terminal → New Terminal**) inside the course folder:
```powershell
uv venv
uv pip install -r requirements.txt
```
- [ ] A `.venv` folder now exists in the course folder.

## Step 8: Your free Google AI Studio key
- [ ] Go to https://aistudio.google.com/apikey and click to create an API key. Copy it.
- [ ] In the course folder, copy `.env.example` to a new file named `.env` (or ask Claude Code: *"Create my .env file from .env.example"*).
- [ ] **Open `.env` yourself** in VS Code and paste the key after `GOOGLE_API_KEY=`. Save.

> Claude Code is deliberately blocked from reading `.env` in this project, so your keys never enter a conversation. Always paste keys yourself.

## Step 9 (optional): Anthropic API key
- An API key is **separate** from your Claude Pro/Max subscription and is **billed per token**. You only need it for `hello_claude_api.py`, `claude_tools.py`, `mini_agent_claude.py` and the Agent SDK lesson (08b).
- [ ] Create one at https://platform.claude.com, **set a monthly spend limit** in the console first, then paste it after `ANTHROPIC_API_KEY=` in `.env`.
- With this key set, the Python lessons use Claude automatically (`LLM_PROVIDER=auto`).

## Step 10: Check everything
- [ ] In the terminal: `python run.py check` (or `.venv\Scripts\python.exe run.py check`). Everything important shows ✅.
- [ ] In the Claude Code panel: **`/run-lesson 4c`**. You should see an agent work turn by turn.

🎉 You are ready. Start with [lessons/01_first_call](../lessons/01_first_call/README.md) or follow [LEARNING_PLAN.md](LEARNING_PLAN.md).

---

## Optional extras

### PyCharm
- **File → Open** → the course folder.
- **Settings → Project → Python Interpreter → Add Interpreter → Existing** → choose `.venv\Scripts\python.exe` inside the course folder.
- Claude Code works in PyCharm too: type `claude` in PyCharm's built-in terminal (needs Step 3), or install Anthropic's Claude Code plugin for JetBrains IDEs from the plugin marketplace.

### Node.js LTS (for the MCP Inspector, lesson 10)
```powershell
winget install OpenJS.NodeJS.LTS
```
Then `npx @modelcontextprotocol/inspector` opens a web page where you can click through an MCP server's tools without any AI.

### Windows Terminal
Usually pre-installed on Windows 11. Nicer tabs and colours than the old console: `winget install Microsoft.WindowsTerminal`.

---

## If something goes wrong
See [TROUBLESHOOTING.md](TROUBLESHOOTING.md), or paste the error into Claude Code with: *"I got this error during setup. Explain it simply and fix it step by step: …"*
