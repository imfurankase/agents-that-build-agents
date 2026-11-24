"""Final project · Milestone 6 - Check your REAL calendar and email connections.

Run it:  python final_project/p6_check_connections.py

Tests the settings in .env (see README, "Connect your real data") WITHOUT
showing any private content: it only prints counts and whether each source works.
Nothing is changed: the inbox is opened read-only and emails stay unread.
"""
import datetime as dt
import os
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

import pa_core  # noqa: E402

from common import show  # noqa: E402

status = pa_core.source_status()
show.title("Checking your data connections")

today = dt.datetime.combine(dt.date.today(), dt.time())
try:
    events = pa_core.load_events(today, today + dt.timedelta(days=7))
    show.event("✅ calendar", f"{status['calendar']}: {len(events)} events in the next 7 days", "green")
except Exception as exc:
    show.event("❌ calendar", f"{status['calendar']}: {type(exc).__name__}: {str(exc)[:150]}", "red")

try:
    emails = pa_core.load_emails()
    unread = sum(e["unread"] for e in emails)
    show.event("✅ email", f"{status['email']}: {len(emails)} recent emails ({unread} unread)", "green")
except Exception as exc:
    show.event("❌ email", f"{status['email']}: {type(exc).__name__}: {str(exc)[:150]}", "red")

for name in ("TELEGRAM_BOT_TOKEN", "TELEGRAM_OWNER_ID"):
    ok = bool(os.getenv(name))
    show.event("✅" if ok else "⚠️ ", f"{name} {'is set' if ok else 'is not set (needed for milestone 5)'}",
               "green" if ok else "yellow")
