# Template: a brief for a team of agents

Use with `/build-team <brief>` in Claude Code, or `python run.py 12 "<brief>"` (the capstone). A good brief makes the planner hire the right team. A vague one wastes money.

---

**Goal:** [The deliverable in one sentence, e.g. "A one-page briefing for department heads on risks of letting AI agents act on team data."]

**Audience:** [Who reads it and what they need, e.g. "Busy senior managers, non-technical; they must decide whether to approve a pilot."]

**Must include:** [Content requirements, e.g. "top 5 risks, each with one mitigation; a 3-line summary at the top; a recommendation."]

**Sources:** [What the team may use, e.g. "Only the files in workspace/inputs/, plus allow-listed websites. No invented statistics."]

**Format:** [e.g. "Markdown, under 600 words, saved to workspace/reports/final_report.md"]

**Team limits:** [e.g. "At most 3 agents. No run_python. Budget $0.50."]

**Success criteria (how a strict reviewer will judge it):**
1. [Specific and checkable, e.g. "Names at least 5 distinct risks"]
2. [e.g. "Every risk has a concrete mitigation"]
3. [e.g. "No claim without a source or the word 'estimate'"]
4. [e.g. "Readable by a non-technical manager in 3 minutes"]

---

### Filled-in example
> Goal: a 1-page "AI agents readiness checklist" for department heads. Audience: non-technical managers deciding whether to start a pilot. Must include: 10-12 checklist items grouped under Purpose, Data, Tools, Oversight, Measurement; one-line rationale each. Sources: general best practice; no statistics. Format: Markdown under 500 words to reports/final_report.md. Team limits: max 3 agents, no web access. Success criteria: covers all 5 groups; every item is a yes/no question; includes a kill-switch item; plain English.
