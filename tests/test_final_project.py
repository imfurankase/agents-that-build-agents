"""Offline tests for the final project (personal assistant). No keys, no internet."""
import datetime as dt
import os
import pathlib
import subprocess
import sys
import tempfile

import pytest

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "final_project"))
os.environ["LLM_PROVIDER"] = "mock"
os.environ.setdefault("COURSE_DATA_DIR", tempfile.mkdtemp(prefix="course-test-"))
for key in ("CALENDAR_ICS_URL", "CALENDAR_ICS_FILE", "EMAIL_IMAP_HOST", "EMAIL_ADDRESS"):
    os.environ.pop(key, None)

import pa_core  # noqa: E402

from common import free_apis  # noqa: E402
from common.toolbox import TOOLBOX  # noqa: E402

TODAY = dt.datetime.combine(dt.date.today(), dt.time())


def test_free_api_tools_are_in_the_toolbox_and_offline():
    for name in ("get_weather", "get_public_holidays", "convert_currency", "wikipedia_summary"):
        assert TOOLBOX[name].risk == "low"
    assert free_apis.OFFLINE
    assert "sample data" in free_apis.get_weather("Paris", 2)


def test_reminders_lifecycle(tmp_path):
    reminders = pa_core.Reminders(tmp_path / "r.json")
    soon = (dt.datetime.now() + dt.timedelta(minutes=5)).strftime("%Y-%m-%d %H:%M")
    item = reminders.add("call Finance", soon)
    assert reminders.upcoming()[0]["text"] == "call Finance"
    assert reminders.due_now() == []
    with pytest.raises(ValueError):
        reminders.add("too late", "2000-01-01 09:00")
    reminders.mark_sent(item["id"])
    assert reminders.upcoming() == []
    other = reminders.add("x", soon)
    assert reminders.cancel(other["id"]) and not reminders.cancel("nope")


def test_sample_calendar_has_events_today():
    events = pa_core.load_events(TODAY, TODAY + dt.timedelta(days=1))
    assert len(events) >= 3 and all(e["start"].startswith(TODAY.date().isoformat()) for e in events)


def test_ics_parser_expands_repeating_events():
    data = (ROOT / "final_project/sample_data/calendar.ics").read_bytes()
    events = pa_core.parse_ics(data, TODAY, TODAY + dt.timedelta(days=7))
    assert sum("stand-up" in e["title"] for e in events) == 7
    assert any(e["all_day"] for e in events)


def test_sample_inbox_contains_the_safety_test_emails():
    subjects = " ".join(e["subject"] + e["body"] for e in pa_core.load_emails())
    assert "AI ASSISTANTS" in subjects and "Verify your password" in subjects


def test_assistant_has_no_tool_that_can_send_or_delete():
    names = {t.name for t in pa_core.assistant_tools(pa_core.Reminders())}
    assert not any(word in n for n in names for word in ("send", "forward", "delete", "reply"))


def test_briefing_and_chat_in_mock_mode():
    brief, markdown = pa_core.make_briefing()
    assert "Good morning" in markdown and set(pa_core.BRIEFING_SCHEMA["required"]) <= set(brief)
    assert pa_core.Assistant().ask("What's on today?")


def test_telegram_bot_builds_without_network(monkeypatch):
    monkeypatch.setenv("TELEGRAM_BOT_TOKEN", "123456:TEST")
    monkeypatch.setenv("TELEGRAM_OWNER_ID", "42")
    import importlib
    import p5_telegram_bot
    bot = importlib.reload(p5_telegram_bot)
    app = bot.build_app()
    assert len(app.handlers[0]) == 4 and len(app.job_queue.jobs()) == 2


@pytest.mark.parametrize("script", ["p1_ask_anything.py", "p2_my_day.py", "p3_briefing.py",
                                    "p4_chat.py", "p6_check_connections.py"])
def test_milestone_scripts_run_offline(script, tmp_path_factory):
    env = {**os.environ, "LLM_PROVIDER": "mock", "PYTHONIOENCODING": "utf-8",
           "COURSE_DATA_DIR": str(tmp_path_factory.getbasetemp() / "course-data")}
    completed = subprocess.run([sys.executable, str(ROOT / "final_project" / script)], cwd=ROOT,
                               env=env, capture_output=True, text=True, encoding="utf-8",
                               input="What's on today?\nquit\n", timeout=120)
    assert completed.returncode == 0, completed.stdout[-1500:] + completed.stderr[-1500:]
