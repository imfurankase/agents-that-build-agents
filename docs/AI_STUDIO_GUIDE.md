# Google AI Studio: six no-code walkthroughs

[Google AI Studio](https://aistudio.google.com) is Google's free web playground for Gemini models. It is the fastest way to **try an idea before building it**: a system prompt, a JSON output format, a tool, a model comparison. When it works, one click gives you the code to hand to Claude Code.

> Google changes AI Studio's layout often. If a button below has moved or been renamed, look for the same idea nearby (settings usually sit in a panel on the right of the chat).

---

## Before you start: your free API key
1. Go to https://aistudio.google.com/apikey and create a key.
2. Paste it into the course's `.env` file after `GOOGLE_API_KEY=` (open `.env` yourself; never paste keys into a chat).
3. Check: `python run.py check` shows "Google AI Studio key is set".

**Free tier, two cautions:**
- **Rate limits:** the free tier allows a limited number of requests per minute and per day. If you see `429` / "resource exhausted", wait a minute or slow down (fewer agents, fewer turns).
- **Your data:** free-tier prompts may be used by Google to improve its products. **Do not paste confidential, personal or classified information** into AI Studio or free-tier API calls. Check Google's current terms before using real organisational data; paid tiers have different data terms.

---

## Walkthrough 1: System instructions (an agent's personality)
1. Create a new prompt (chat).
2. Find **System instructions** and paste:
   *"You are a chief-of-staff. Answer in 3 bullets, plain English, max 60 words. If you don't know, say 'unknown'."*
3. Ask: *"What should a manager check before letting an AI assistant read team emails?"*
4. Change one line of the system instruction (e.g. "for a board audience") and ask again.

**Learn:** the system instruction is the agent's job description. Small changes there change everything downstream.

## Walkthrough 2: Structured output (JSON with a schema)
1. In the settings panel, turn on **Structured output** (JSON mode) and open the schema editor.
2. Paste:
   ```json
   {"type": "object",
    "properties": {
      "category": {"type": "string", "enum": ["it", "hr", "finance"]},
      "urgency": {"type": "string", "enum": ["low", "medium", "high"]},
      "summary": {"type": "string"}},
    "required": ["category", "urgency", "summary"]}
   ```
3. Send: *"My laptop won't connect to the VPN and I have a board presentation in 20 minutes."*

**Learn:** the answer is now *data* a program can act on, the glue between agents (the router pattern in lesson 05 and the AgentSpec in lesson 06 work this way).

## Walkthrough 3: Function calling (you play the tool)
1. In the tools section, enable **Function calling** and edit the declarations. Paste:
   ```json
   [{"name": "lookup_team",
     "description": "Look up a team in the staff directory. Returns its lead and headcount.",
     "parameters": {"type": "object",
                    "properties": {"team_name": {"type": "string"}},
                    "required": ["team_name"]}}]
   ```
2. Ask: *"How many people work in Finance and IT combined?"*
3. The model doesn't answer. It **asks you** to call `lookup_team`. Type a result yourself, e.g. `{"lead": "A. Mugisha", "headcount": 18}`, and continue.

**Learn:** the model never runs tools; *the code in the middle* does. In this walkthrough, you are that code. The Governor in lesson 07 sits exactly where you are sitting now.

## Walkthrough 4: Grounding with Google Search
1. Turn on **Grounding with Google Search** in the tools section.
2. Ask: *"What are two recent public examples of governments piloting AI agents? Give sources."*
3. Open the source links it shows.

**Learn:** grounding gives the model fresh facts plus citations. Always click through to check important claims. The ADK `researcher` agent in lesson 09 uses the same Google Search tool.

## Walkthrough 5: Compare models
1. Keep the same system instruction and question.
2. Switch the model in the model picker (e.g. a Flash model vs a Pro model) and compare quality, speed and length.
3. Note: `gemini-flash-latest` (the course default) always points to Google's newest Flash model.

**Learn:** bigger isn't always better. Use the smallest model that passes your quality bar for worker agents, and the strongest for planning and judging.

## Walkthrough 6: Get code → hand it to Claude Code
1. When a prompt works, click **Get code** and choose **Python**.
2. Copy the code. In VS Code, tell Claude Code:
   > *"Here is code from Google AI Studio: [paste]. Turn it into a new lesson script in lessons/09_google_adk/ that loads the key from .env using common/config.py, and run it."*
   or:
   > *"Turn this AI Studio prompt into an ADK agent and add it to the adk_team as a new teammate."*

**Learn:** prototype in AI Studio (minutes), productionise with Claude Code (minutes more), govern with the course's Foundry.

---

## Bonus: Build mode
AI Studio can also generate small apps from a description. Try: *"A one-page app where I paste meeting notes and get decisions and action items."* Use it for prototypes and demos; keep real data out of it.

## Exercises
E9.1-E9.3 in [exercises/EXERCISES.md](../exercises/EXERCISES.md) use these walkthroughs.
