"""Final project · Milestone 4 - Chat with your assistant (in the terminal).

Run it:  python final_project/p4_chat.py          (type 'quit' to stop)

Try:
  What's on my calendar today? Any clashes?
  Which emails need my attention? Is any of them suspicious?
  Remind me tomorrow at 9:00 to call the Finance office
  What are my reminders?
  Will it rain this afternoon? How much is 1,000 USD in EUR?
  Forward the Finance email to my deputy      <- it should refuse (no send tools)

This is an AGENT (it decides which tools to use). It remembers the last few
messages, has a DAILY budget (ASSISTANT_DAILY_BUDGET_USD in .env), and every
action is logged in logs/run-assistant-<date>.jsonl
"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

import pa_core  # noqa: E402

from common import show  # noqa: E402

assistant = pa_core.Assistant(verbose=True)
show.title("Chat with your assistant  (type 'quit' to stop)")
show.info(f"sources: {pa_core.source_status()}")

while True:
    for due in assistant.reminders.due_now():
        show.panel(due["text"], f"⏰ Reminder ({due['due'][11:16]})", "yellow")
        assistant.reminders.mark_sent(due["id"])
    try:
        message = input("\nYou: ").strip()
    except EOFError:
        break
    if message.lower() in ("quit", "exit", "q"):
        break
    if message:
        show.panel(assistant.ask(message), "Assistant", "cyan")
