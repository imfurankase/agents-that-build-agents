# Lesson 03: Tools, giving an AI "hands"

**Goal:** understand how a model *uses* things in the world (calculators, files, websites, other agents).

## The big idea
A model can only produce text. **Tool use** (also called *function calling*) is a deal:
1. You describe tools to the model: name, what it does, what inputs it needs.
2. The model replies *"please call `lookup_team` with `{"team_name": "IT"}`"* instead of an answer.
3. **Your code** runs the tool and sends back the result.
4. The model continues, now knowing the result.

The model **never runs anything itself**. Your code is always in the middle, and that is where control lives (lesson 07).

## The most important part of a tool: its description
The model decides *when* to use a tool purely from its name and description. A vague description means the tool is used wrongly or never. Compare:
- ❌ `lookup(x)`: "Looks things up."
- ✅ `lookup_team(team_name)`: "Look up a team in the staff directory. Returns its lead and headcount. team_name: e.g. 'Finance', 'IT'."

## Say this to Claude Code
> Run lesson 3a and show me which tools Gemini decided to call, in which order, and why.

> Add a new fake tool to gemini_tools.py called get_team_budget(team_name) with made-up budgets, then ask "Which team has the biggest budget per person?"

> Open common/toolbox.py and explain the risk levels. Why is write_file "medium" and run_python "high"?

> What would go wrong if the description of lookup_team was just "does stuff"? Try it and show me.

## Run it
```
python run.py 3a        # Gemini (free key)
python run.py 3b        # Claude API (API key)
```

## No-code version (Google AI Studio)
In AI Studio, open the **Tools** panel → **Function calling** → **Edit**, and paste a function declaration (JSON). Ask a question that needs it. AI Studio shows you the function call the model wants; you type the result yourself. You are playing "the code in the middle".

## Takeaways
1. Tools turn a talker into a doer. The model asks; your code acts.
2. Tool descriptions are prompts. Write them as carefully as system prompts.
3. Give the fewest, safest tools that do the job (**least privilege**).

**Exercises:** E3.1-E3.6
