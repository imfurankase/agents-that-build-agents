"""Lesson 02a - The Prompt Lab: the same task, a weak prompt vs a strong prompt.

Run it:     python lessons/02_prompting/prompt_lab.py
Works with: Claude API, Gemini, or the offline mock (see LLM_PROVIDER in .env)

What to notice:
- The model is the same. Only the prompt changes. Look at how different the
  answers are. Prompting is the #1 skill for building agents, because an
  agent's "personality and job" IS a prompt.
- The strong prompt has: role, context, task, output format, and rules.

Exercise: edit STRONG_PROMPT below (or ask Claude Code to) and run again.
"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))

from common import show
from common.llm import get_llm

DOCUMENT = """\
MEMO - Operations Team, internal
Subject: 90-day pilot of AI assistants

Over the last quarter, 14 staff used AI assistants for drafting reports, summarising
long documents and answering routine questions from other departments. Staff report
saving between 2 and 6 hours per week each. Two incidents occurred: one draft report
contained an invented statistic that was caught in review, and one staff member pasted
a document marked CONFIDENTIAL into a public chatbot. Licensing for the whole
department (120 staff) would cost about $45,000 per year. The IT team asks for a
decision on (a) expanding to the whole department, (b) a data-handling policy, and
(c) mandatory training before access is granted.
"""

WEAK_PROMPT = f"Summarize this.\n\n{DOCUMENT}"

STRONG_PROMPT = f"""\
<role>You are a chief-of-staff briefing a busy director.</role>

<context>The director must decide this week whether to expand an AI-assistant pilot.
They have 2 minutes to read your brief.</context>

<document>
{DOCUMENT}
</document>

<task>Write a decision brief based ONLY on the document.</task>

<format>
1. One-line recommendation (start with "Recommend:").
2. "Benefits" - 2 bullets with numbers from the memo.
3. "Risks" - 2 bullets, each with a concrete mitigation.
4. "Decisions needed" - the 3 decisions, each as a yes/no question.
Under 150 words. No preamble.
</format>

<rules>Do not invent numbers. If something is unknown, write "unknown".</rules>
"""

llm = get_llm()
show.title(f"Prompt Lab - provider: {llm.name}, model: {llm.model}")

for label, prompt in [("WEAK prompt: 'Summarize this.'", WEAK_PROMPT),
                      ("STRONG prompt: role + context + task + format + rules", STRONG_PROMPT)]:
    text, usage = llm.complete("You are a helpful assistant.", prompt, effort="low")
    show.panel(text, f"{label}  ({usage.output_tokens} output tokens)")
