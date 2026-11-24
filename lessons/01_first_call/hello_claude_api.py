"""Lesson 01b - Your first call to the Claude API (Anthropic).

Run it:     python lessons/01_first_call/hello_claude_api.py
Needs:      ANTHROPIC_API_KEY in your .env file (from https://platform.claude.com)
            NOTE: a Claude Pro/Max subscription is NOT an API key. The API is
            billed separately, per token. If you only have a subscription, use
            hello_claude_code.py instead - it uses your subscription.

What to notice:
- `system` sets who Claude is; `messages` is the conversation.
- `effort` controls how hard Claude thinks (low / medium / high / xhigh / max).
- Every response tells you how many tokens it used, so you can compute cost.
"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))

import anthropic

from common import config

client = anthropic.Anthropic()  # finds ANTHROPIC_API_KEY automatically

response = client.beta.messages.create(
    model=config.CLAUDE_MODEL,
    max_tokens=16000,
    system="You are a clear, friendly teacher. Plain English, no jargon.",
    messages=[{"role": "user",
               "content": "In 3 bullet points, explain what an AI agent is to a busy executive."}],
    output_config={"effort": "medium"},
    # If a safety check declines the request, retry automatically on a fallback model.
    betas=["server-side-fallback-2026-07-01"],
    fallbacks="default",
)

if response.stop_reason == "refusal":
    print("Claude declined this request.")
else:
    for block in response.content:
        if block.type == "text":
            print(block.text)

usage = response.usage
cost = config.cost_usd(config.CLAUDE_MODEL, usage.input_tokens, usage.output_tokens)
print(f"\n[model: {config.CLAUDE_MODEL} | tokens in: {usage.input_tokens} "
      f"| tokens out: {usage.output_tokens} | cost about ${cost:.4f}]")
