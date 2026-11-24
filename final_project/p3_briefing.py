"""Final project · Milestone 3 - The morning briefing.

Run it:  python final_project/p3_briefing.py

This is a WORKFLOW, not an agent (lesson 04): plain code gathers today's
calendar, emails, reminders, weather and holidays; ONE model call turns it into
a structured briefing (JSON schema); code renders it for a phone screen.
Predictable, cheap, easy to test - the right tool for a fixed daily job.

Look for the "Watch out" section: the sample inbox contains a phishing email
and an email that tries to give orders to AI assistants.
Saved to: workspace/assistant/briefings/<date>.md
"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

import pa_core  # noqa: E402

from common import show  # noqa: E402

show.title("Morning briefing")
show.info(f"sources: {pa_core.source_status()}")
brief, markdown = pa_core.make_briefing()
show.panel(markdown, "Your briefing (as it will look on your phone)", "cyan")
show.info("Saved in workspace/assistant/briefings/")
