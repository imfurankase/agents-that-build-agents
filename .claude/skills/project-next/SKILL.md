---
name: project-next
description: Final project coach - work out which personal-assistant milestone the learner has reached and guide the next step.
disable-model-invocation: true
---

Read `final_project/README.md`. Then work out progress WITHOUT opening `.env`:
- Run `python scripts/check_setup.py` and `python final_project/p6_check_connections.py` (they only report set/not set and counts).
- Look for evidence: files in `workspace/assistant/briefings/` (milestone 3 done), `workspace/assistant/reminders.json` (milestone 4), changes in `final_project/sample_data/` (EP.3).

Report in this format:
- **Milestones done:** ✅/⬜ for 1-6, one line each with the evidence.
- **Next step:** the single next milestone or exercise (EP.x), what it achieves, and the exact prompt or command to start it.
- **Heads-up:** one safety or privacy point relevant to that step (e.g. treat the bot token and iCal link like passwords; use a personal/test inbox first).

Keep it under 200 words. Ask before running anything that calls a paid model.
