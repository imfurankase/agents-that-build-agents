"""Lesson 01a - Your first call to Gemini (Google AI Studio). FREE tier works.

Run it:     python lessons/01_first_call/hello_gemini.py
Needs:      GOOGLE_API_KEY in your .env file
            (get one free at https://aistudio.google.com/apikey)

What to notice:
- A "system instruction" sets WHO the model is. The "contents" is the request.
- The model has no memory between runs: every call starts fresh.
- Tokens are how usage is measured (roughly 1 token = 3/4 of a word).
"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))  # find the "common" folder

from google import genai
from google.genai import types

from common import config  # loads .env

client = genai.Client()  # finds GOOGLE_API_KEY automatically

response = client.models.generate_content(
    model=config.GEMINI_MODEL,
    contents="In 3 bullet points, explain what an AI agent is to a busy executive.",
    config=types.GenerateContentConfig(
        system_instruction="You are a clear, friendly teacher. Plain English, no jargon.",
    ),
)

print(response.text)
usage = response.usage_metadata
print(f"\n[model: {config.GEMINI_MODEL} | tokens in: {usage.prompt_token_count} "
      f"| tokens out: {usage.candidates_token_count}]")
