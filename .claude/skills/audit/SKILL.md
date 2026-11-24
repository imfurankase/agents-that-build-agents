---
name: audit
description: Summarise what agents did - from the Python audit logs (logs/run-*.jsonl) and the Claude Code audit log (logs/claude_code_audit.jsonl).
disable-model-invocation: true
---

1. Run `python lessons/07_controlling_agents/audit_report.py` for the latest Python run.
2. Read the last ~50 lines of `logs/claude_code_audit.jsonl` (if it exists) to see recent Claude Code tool use.
3. Report in plain English: agents created and by whom, tools used, anything blocked or stopped, human decisions, estimated cost. Flag anything unusual (many failed calls, blocked actions, unexpected file writes).
