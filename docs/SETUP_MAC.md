# Setup on a Mac (step by step)

Allow about **30 minutes** the first time. Tick each box as you go. (On Windows? See [SETUP_WINDOWS.md](SETUP_WINDOWS.md).)

> **The 5-minute version:** if VS Code with the Claude Code extension is already installed, open this course folder in VS Code, open the Claude Code panel and type **`/check-setup`**. Claude Code will check everything below and walk you through whatever is missing.

To open **Terminal**: press **Cmd + Space**, type `Terminal`, press Enter. VS Code also has one built in: **Terminal → New Terminal**.

---

## What each thing is for

| Tool | What it does for you | Needed for |
|---|---|---|
| **VS Code + Claude Code extension** | Where you work: you chat with Claude Code and it reads, runs and edits the course for you | Everything |
| **Git** (Apple's Command Line Tools) | Version history and downloading the course | Everything |
| **Claude Code CLI** | Claude Code in a terminal. Lets scripts drive Claude Code (`claude -p`) | Lessons 01c, 08a, 10 |
| **Python 3.12 or newer** | Runs the course's Python agents | Lessons 01-12 |
| **Homebrew** *(recommended)* | The usual way to install developer tools on a Mac | Installing Python, uv, Node |
| **uv** *(optional)* | Fast Python package installer. Not required on a Mac | Faster installs |
| **Google AI Studio key** | Free key for Gemini models | Real answers in the Python lessons, ADK (lesson 09) |
| **Anthropic API key** *(optional)* | Pay-per-token access to Claude from Python | `*_claude_api` lessons, Agent SDK (08b) |
| **PyCharm** *(optional)* | A second editor if you prefer it | Nothing extra |
| **Node.js LTS** *(optional)* | Runs the MCP Inspector tool | Lesson 10 extras |

---

## Step 1: VS Code and the Claude Code extension
- [ ] Download **VS Code** for Mac from https://code.visualstudio.com and drag it into **Applications**.
- [ ] In VS Code, open **Extensions** (the four-squares icon on the left), search **"Claude Code"** and install the extension published by **Anthropic** (ID: `anthropic.claude-code`).
- [ ] Open the Claude Code panel (Claude icon in the side bar) and **sign in** with your Claude account (Pro or Max plan).

> The extension does **not** add the `claude` command to your terminal. That is what Step 3 is for.

## Step 2: Git
- [ ] In Terminal run:
  ```bash
  xcode-select --install
  ```
  and click **Install** in the window that appears (a few minutes). If it says the tools are already installed, you're done.
- [ ] Check: `git --version` prints a version number.

## Step 3: Claude Code CLI (the terminal version)
- [ ] In Terminal, run the official installer:
  ```bash
  curl -fsSL https://claude.ai/install.sh | bash
  ```
  Alternative with Homebrew: `brew install --cask claude-code` (this version doesn't update itself; run `brew upgrade claude-code` now and then).
- [ ] **Close and reopen** Terminal so it sees the new command.
- [ ] Type `claude` and follow the login steps once. Then exit with `/exit`.
- [ ] Check: `claude --version` prints a version number.

> **Billing note:** the CLI uses your Claude subscription. If an `ANTHROPIC_API_KEY` environment variable is set, `claude -p` (headless mode) bills that API key instead. The course's helper removes the key for these calls so you don't pay twice by accident.

## Step 4: Python 3.12 or newer
- [ ] Install **Homebrew** from https://brew.sh: copy the one-line command on its home page into Terminal and follow the prompts.
- [ ] Then:
  ```bash
  brew install python
  ```
  (Or use the macOS installer from https://www.python.org/downloads/.)
- [ ] Check: `python3 --version` shows 3.12 or newer.

> **On a Mac the command is `python3`, not `python`.** Inside the course's environment (Step 7), `python` works too. Commands in this course that start with `python` work once the environment is active, or you can write `.venv/bin/python` instead.

## Step 5 (optional): uv
- [ ] `brew install uv`. You can skip this: Step 7 shows a route without it.

## Step 6: Get the course
- [ ] In Terminal, go to where you keep projects and download the course:
  ```bash
  mkdir -p ~/Documents/GitHub && cd ~/Documents/GitHub
  git clone https://github.com/imfurankase/agents-that-build-agents.git
  ```
- [ ] In VS Code: **File → Open Folder…** → choose `agents-that-build-agents`. If VS Code asks whether you trust the authors, choose **Yes, I trust**.
- [ ] Accept the prompt to install the **recommended extensions** (Claude Code, Python).

## Step 7: Install the course packages
Easiest: in the Claude Code panel type **`/check-setup`** and say yes when it offers to create the environment.

Or yourself, in VS Code's terminal inside the course folder:
```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
```
(With uv instead: `uv venv` then `uv pip install -r requirements.txt`.)
- [ ] A `.venv` folder now exists in the course folder.
- [ ] To use plain `python` in a terminal, activate the environment first: `source .venv/bin/activate`. VS Code does this for you in new terminals once you pick the `.venv` interpreter (bottom right of the window).

## Step 8: Your free Google AI Studio key
- [ ] Go to https://aistudio.google.com/apikey and click to create an API key. Copy it.
- [ ] In the course folder, create your settings file from the template:
  ```bash
  cp .env.example .env
  ```
- [ ] **Open `.env` yourself** in VS Code (it's in the file list on the left; Finder hides files whose names start with a dot) and paste the key after `GOOGLE_API_KEY=`. Save with **Cmd + S**.

> Claude Code is deliberately blocked from creating, reading or editing `.env` in this project, so your keys never enter a conversation. Always paste keys yourself.

## Step 9 (optional): Anthropic API key
- An API key is **separate** from your Claude Pro/Max subscription and is **billed per token**. You only need it for `hello_claude_api.py`, `claude_tools.py`, `mini_agent_claude.py` and the Agent SDK lesson (08b).
- [ ] Create one at https://platform.claude.com, **set a monthly spend limit** in the console first, then paste it after `ANTHROPIC_API_KEY=` in `.env`.
- With this key set, the Python lessons use Claude automatically (`LLM_PROVIDER=auto`).

## Step 10: Check everything
- [ ] In the terminal: `.venv/bin/python run.py check`. Everything important shows ✅.
- [ ] In the Claude Code panel: **`/run-lesson 4c`**. You should see an agent work turn by turn.

🎉 You are ready. Start with [lessons/01_first_call](../lessons/01_first_call/README.md) or follow [LEARNING_PLAN.md](LEARNING_PLAN.md).

---

## Optional extras

### PyCharm
- **File → Open** → the course folder.
- **Settings → Project → Python Interpreter → Add Interpreter → Existing** → choose `.venv/bin/python` inside the course folder.
- Claude Code works in PyCharm too: type `claude` in PyCharm's built-in terminal (needs Step 3), or install Anthropic's Claude Code plugin for JetBrains IDEs from the plugin marketplace.

### Node.js LTS (for the MCP Inspector, lesson 10)
```bash
brew install node
```
Then `npx @modelcontextprotocol/inspector` opens a web page where you can click through an MCP server's tools without any AI.

### Running the phone assistant on a Mac (final project)
The Telegram bot only works while your Mac is awake and the script is running. To start it automatically at log-in, ask Claude Code for a **launchd agent** (exercise EP.9). To stop the Mac sleeping while it's plugged in: **System Settings → Battery → Options → Prevent automatic sleeping when the display is off**.

---

## If something goes wrong
See [TROUBLESHOOTING.md](TROUBLESHOOTING.md), or paste the error into Claude Code with: *"I got this error during setup. Explain it simply and fix it step by step: …"*
