"""Final project · Milestone 2 - Your data, with NO AI involved yet.

Run it:  python final_project/p2_my_day.py

Shows what the assistant can see: today's calendar, recent emails, reminders,
weather. It starts with SAMPLE data (in final_project/sample_data/), so you can
build everything safely before connecting your real calendar and inbox (milestone 6).

Lesson: get the data right first. An AI can only be as good as what it can see.
"""
import datetime as dt
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

import pa_core  # noqa: E402  (lives next to this file)

from common import config, show  # noqa: E402
from common.free_apis import get_weather  # noqa: E402

status = pa_core.source_status()
show.title("My day - raw data (no AI)")
show.info(f"calendar source: {status['calendar']} | email source: {status['email']}")

today = dt.datetime.combine(dt.date.today(), dt.time())
events = pa_core.load_events(today, today + dt.timedelta(days=1))
show.panel("\n".join(pa_core._format_event(e) for e in events) or "(no events)", "Calendar today")

emails = pa_core.load_emails()
show.panel("\n".join(f"{'●' if e['unread'] else ' '} {e['from']}: {e['subject']}" for e in emails)
           or "(no emails)", "Inbox (● = unread)")

reminders = pa_core.Reminders().upcoming()
show.panel("\n".join(f"{r['due']} {r['text']}" for r in reminders) or "(no reminders yet)",
           "Reminders")
show.panel(get_weather(config.HOME_CITY, 1), f"Weather ({config.HOME_CITY} - change HOME_CITY in .env)")
