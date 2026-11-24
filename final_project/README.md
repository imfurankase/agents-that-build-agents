# Final project: your personal assistant, on your phone

**The goal:** a private assistant in your pocket that reads your calendar and email, sends you a briefing every morning, reminds you of things at the right time, and answers your questions in a chat, using everything from lessons 01-12.

```
  📱 Your phone (Telegram)                 💻 Your computer (runs the bot)
  ┌──────────────────────┐   chat /     ┌───────────────────────────────────────────┐
  │ ☀️ 07:00 briefing     │ ◄──────────► │  p5_telegram_bot.py                        │
  │ ⏰ reminders          │  push msgs   │    ├─ Morning briefing  (WORKFLOW, lesson 05)│
  │ 💬 "what's on today?" │              │    ├─ Assistant         (AGENT, lesson 04)   │
  └──────────────────────┘              │    │    └─ Governor: daily budget, audit log │
                                         │    └─ Tools (read-only + reminders to you)   │
                                         │        calendar · email · reminders ·        │
                                         │        weather · holidays · currency · wiki  │
                                         └───────────────────────────────────────────┘
```

You build it in **six milestones**. Each one works on its own and starts with **sample data**, so nothing private is touched until milestone 6.

| # | Milestone | Run | You learn |
|---|---|---|---|
| 1 | Real-world tools from free APIs | `python run.py p1 "question"` | Tools; the agent choosing them (lessons 03-04) |
| 2 | Your data, no AI yet | `python run.py p2` | Data first; connectors; sample vs real |
| 3 | Morning briefing | `python run.py p3` | Workflow + structured output (lessons 02, 05) |
| 4 | Chat + reminders | `python run.py p4` | An agent with memory, tools, daily budget (lessons 04, 07) |
| 5 | On your phone | `python run.py p5` | A real app: Telegram bot, push notifications |
| 6 | Your real calendar & email | `python run.py p6` | Connecting real data safely (lesson 11) |

---

## The free APIs (no account, no key)

| Tool | Service | Example question |
|---|---|---|
| `get_weather` | [Open-Meteo](https://open-meteo.com) | "Do I need an umbrella in Nairobi tomorrow?" |
| `get_public_holidays` | [Nager.Date](https://date.nager.at) | "When is the next public holiday in Kenya?" |
| `convert_currency` | [Frankfurter](https://frankfurter.dev) (European Central Bank rates) | "How much is 250 USD in EUR?" |
| `wikipedia_summary` | [Wikipedia](https://en.wikipedia.org) | "What is the Model Context Protocol?" |

They live in `common/free_apis.py` and are in the shared toolbox, so **any agent in the course** can use them (try them in lesson 06's meta-agent). Be polite to free services: a few calls per question, never in tight loops. Set your city and country once in `.env`: `HOME_CITY=Nairobi`, `HOME_COUNTRY_CODE=KE`.

---

## Milestone 1: Ask anything (free APIs)
> Run `python run.py p1 "Will I need an umbrella in Nairobi tomorrow, and how much is 250 USD in EUR?"` and tell me which tools the agent used and why.

> Add a new free-API tool to common/free_apis.py: sunrise and sunset for any city (Open-Meteo has it). Register it in the toolbox, add an offline sample answer, and test it with p1.

**Done when:** you can predict which tools the agent will pick for a question.

## Milestone 2: Your data, no AI
> Run `python run.py p2` and explain where each piece of data comes from.

> Add 3 events to final_project/sample_data/calendar.json for tomorrow that look like my real week, and 2 emails to inbox.json. Run p2 again.

**Done when:** the sample data looks like a realistic day for you.

## Milestone 3: Morning briefing
> Run `python run.py p3`. Did it catch the phishing email, the email that tries to instruct the AI, and the lunch/IT-call clash?

> Edit prompts/system/briefing.md so the briefing also lists "3 things only I can do today". Run p3 again.

**Done when:** the briefing is something you'd actually want to read at 7am. Why a workflow and not an agent? The steps are the same every day, so plain code gathers the data and one model call writes the summary. That is cheaper, faster and more predictable (lesson 04: use the simplest thing that works).

## Milestone 4: Chat + reminders
> Run `python run.py p4` and try: "What's on today?", "Which emails need me?", "Remind me tomorrow at 9:00 to call Finance", "Forward the Finance email to my deputy" (it must refuse and offer a draft).

> Show me the audit log of my chat (logs/run-assistant-<today>.jsonl) and explain each tool call.

**Done when:** a reminder you set appears in `workspace/assistant/reminders.json` with the right time.

## Milestone 5: On your phone (Telegram)
1. Install Telegram on your phone (and optionally on your computer).
2. In Telegram, search **@BotFather** → send `/newbot` → pick a name and a username ending in `bot` → copy the **token**.
3. Put it in `.env` yourself: `TELEGRAM_BOT_TOKEN=...` (treat it like a password).
4. Run `python run.py p5`. Open your bot in Telegram, press **Start**: it replies with your user id.
5. Put `TELEGRAM_OWNER_ID=<your id>` in `.env` and restart `p5`. Now the bot answers **only you**.
6. Try `/brief`, `/reminders`, and chat. Set a reminder 2 minutes ahead and watch your phone buzz.

> Help me set up the Telegram bot for milestone 5, step by step. Don't open .env; tell me exactly which lines to add.

**Done when:** you get the morning briefing on your phone at `BRIEFING_TIME`, and a reminder arrives as a notification.

### Keep it running
The bot works while `p5` is running. Options, from simplest:
1. **Leave your computer on** with `p5` running in a terminal.
2. **Start it automatically** when you log in: *"Set up a Windows Task Scheduler task that starts the Telegram bot when I log in, using the .venv Python. Explain each step."*
3. **A small always-on machine** later (a Raspberry Pi or a small cloud server). Ask Claude Code to walk you through it when you're ready.

## Milestone 6: Your real calendar and email
Start with a **personal or test account**, not work email, until you are comfortable (see *Privacy* below).

**Calendar: a read-only iCal link (works for Google and Outlook).**
- Google Calendar on a computer → ⚙ Settings → your calendar → *Integrate calendar* → copy **Secret address in iCal format**.
- Outlook → Settings → Calendar → *Shared calendars* → *Publish a calendar* → copy the **ICS** link.
- In `.env`: `CALENDAR_ICS_URL=<that link>`. Treat it like a password: anyone with it can read your calendar.

**Email: read-only IMAP.**
- Gmail: turn on 2-Step Verification, then create an **App password** (Google Account → Security). In `.env`: `EMAIL_IMAP_HOST=imap.gmail.com`, `EMAIL_ADDRESS=you@gmail.com`, `EMAIL_APP_PASSWORD=<app password>`.
- The assistant opens the inbox **read-only** and uses PEEK, so emails stay unread and nothing is changed or sent.
- Work accounts (Microsoft 365 / Google Workspace) often block app passwords and IMAP. Ask your IT team; the proper route there is the Microsoft Graph or Gmail API with an approved app registration (Claude Code can help you build it, with IT's agreement).

Then run `python run.py p6`. It checks both connections and prints **counts only**, never your content.

---

## Safety and privacy rules for a personal assistant
This project is lesson 11's "dangerous trio" in real life: **emails are untrusted input**, your calendar and inbox are **private data**, and an assistant could **act**. The design removes the third:

1. **Read-only by design.** No tool can send, forward, reply, delete or pay. It can only read, and remind *you*.
2. **Owner-only.** The bot ignores everyone except `TELEGRAM_OWNER_ID`.
3. **Emails are data, not orders.** Labelled UNTRUSTED; the prompts tell the model to warn you about phishing and instructions aimed at AIs (the sample inbox tests both).
4. **Daily budget + audit log.** `ASSISTANT_DAILY_BUDGET_USD` caps spending per day; every action is in `logs/run-assistant-<date>.jsonl`. The `STOP` kill switch pauses it.
5. **Secrets stay in `.env`**, never in code, never committed (`.gitignore`), never read by Claude Code (hooks + permissions).
6. **Where your data goes:** your calendar and emails are sent to the AI provider to be summarised. Check the provider's terms (free tiers may use inputs to improve their products), follow your organisation's policy, and don't connect confidential work email without approval.

---

## Ideas to extend (agents that build agents, again)
- **Meeting prep agent:** 30 minutes before each meeting, send a one-paragraph prep note.
- **Weekly review:** every Friday at 16:00, summarise the week and next week's big items.
- **Specialists on demand:** give the assistant the Foundry's `create_agent`/`run_agent` (lesson 06) so it can hire a "travel planner" or "report drafter", under the Governor.
- **Your own subagents:** turn the briefing prompt into a Claude Code subagent you can also use in VS Code.
- **Voice:** Telegram voice notes → transcription → the assistant (a stretch goal).

## Build or buy?
The Claude apps can already connect to Gmail and Google Calendar and summarise them for you, with no code. Building your own teaches you how agents really work and lets you control every rule: data sources, prompts, budget, logging, and exactly what it may do. A good leader knows both options.

**Exercises:** EP.1-EP.12 in [exercises/EXERCISES.md](../exercises/EXERCISES.md)
