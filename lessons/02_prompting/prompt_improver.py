"""Lesson 02b - The Prompt Improver: an AI that improves prompts for AIs.

Run it:     python lessons/02_prompting/prompt_improver.py "your rough prompt here"
   or just: python lessons/02_prompting/prompt_improver.py      (it will ask you)

What to notice:
- This is the first step toward "agents that build agents": an AI writing
  instructions for another AI. In lesson 06 the same idea designs whole agents.
- The improved prompt and the list of changes are saved in workspace/prompts/.
- The answer is STRUCTURED (JSON that follows a schema), so a program can use it.
"""
import datetime
import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))

from common import config, show
from common.foundry import load_prompt
from common.llm import get_llm

SCHEMA = {
    "type": "object",
    "properties": {
        "improved_prompt": {"type": "string"},
        "changes": {"type": "array", "items": {"type": "string"},
                    "description": "what you changed and why, one line each"},
        "questions_for_the_author": {"type": "array", "items": {"type": "string"},
                                     "description": "missing facts that would improve it"},
    },
    "required": ["improved_prompt", "changes", "questions_for_the_author"],
    "additionalProperties": False,
}

rough = " ".join(sys.argv[1:]) or input("Paste a rough prompt to improve:\n> ")

llm = get_llm()
text, usage = llm.complete(load_prompt("prompt_improver"), f"<rough_prompt>\n{rough}\n</rough_prompt>",
                           json_schema=SCHEMA, effort="high")
result = json.loads(text)

show.panel(result["improved_prompt"], "Improved prompt")
show.panel("\n".join(f"- {c}" for c in result["changes"]), "What changed", "cyan")
if result["questions_for_the_author"]:
    show.panel("\n".join(f"? {q}" for q in result["questions_for_the_author"]),
               "Questions that would make it even better", "yellow")

out = config.WORKSPACE / "prompts"
out.mkdir(exist_ok=True)
path = out / f"improved-{datetime.datetime.now():%Y%m%d-%H%M%S}.md"
path.write_text(f"# Original\n\n{rough}\n\n# Improved\n\n{result['improved_prompt']}\n\n"
                f"# Changes\n\n" + "\n".join(f"- {c}" for c in result["changes"]) + "\n",
                encoding="utf-8")
show.info(f"Saved to {config.rel(path)}")
