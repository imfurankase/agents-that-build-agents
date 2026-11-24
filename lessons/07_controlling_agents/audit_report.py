"""Lesson 07c - Turn an audit log into a readable report.

Run it:  python lessons/07_controlling_agents/audit_report.py              (latest run)
         python lessons/07_controlling_agents/audit_report.py logs/run-XXXX.jsonl

Answers the questions a manager asks after an autonomous run:
  Who was created, by whom?  What tools were used?  What was blocked?
  What did humans decide?    How much did it cost?
"""
import collections
import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))

from common import config, show


def section(heading: str, lines: list[str]) -> list[str]:
    return [heading, *(lines or ["  (none)"]), ""]


path = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else None
if path is None:
    logs = sorted(config.LOGS.glob("run-*.jsonl"))
    if not logs:
        sys.exit("No audit logs yet. Run a lesson 06 or 07 script first.")
    path = logs[-1]

records = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line]
by_event = collections.defaultdict(list)
for r in records:
    by_event[r["event"]].append(r)

cost = max((r.get("total_usd", 0) for r in by_event["model_call"]), default=0)
tools_used = collections.Counter(r["tool"] for r in by_event["tool_requested"])

report = [f"Run log: {path.name}",
          f"Model calls: {len(by_event['model_call'])}   Estimated cost: ${cost:.4f}", ""]
report += section("AGENTS CREATED:", [
    f"  - {r['agent']} (by {r.get('created_by')}, depth {r.get('depth')}, tools {r.get('tools')})"
    for r in by_event["agent_created"]])
report += section("TOOLS USED:", [f"  - {name}: {count}x"
                                  for name, count in tools_used.most_common()])
report += section("BLOCKED / STOPPED:", [
    f"  - {r['agent']}: {r.get('tool', '')} {r.get('reason', '')}"
    for r in by_event["tool_blocked"] + by_event["stopped"] + by_event["killed"]])
report += section("HUMAN DECISIONS:", [
    f"  - {'YES' if r['approved'] else 'NO '}: {r['question'][:110]}"
    for r in by_event["human_decision"]])
show.panel("\n".join(report), "Audit report", "cyan")
