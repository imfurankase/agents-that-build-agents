"""One simple way to talk to Claude, Gemini, or a fake offline model.

Lessons 05-12 use this file, so the same agent code works with either
company's models. Lessons 01-04 show the raw SDK code instead, so you can
see what this file hides.

The most important function is `run_agent()` in `BaseProvider`. It is the
AGENT LOOP that every agent in this course runs:

    1. send the conversation to the model
    2. if the model asks to use tools, run them and send back the results
    3. repeat until the model answers without asking for a tool

Before every step the loop asks the `Hooks` object (the Governor in lesson 07)
for permission. That is how we keep agents under control.
"""
from __future__ import annotations

import json
from dataclasses import dataclass, field
from typing import Any, Callable

from common import config


# --------------------------------------------------------------------------
# Shared building blocks
# --------------------------------------------------------------------------

class StopAgent(Exception):
    """Raised by a supervisor to stop an agent immediately (budget, kill switch...)."""

    def __init__(self, reason: str):
        super().__init__(reason)
        self.reason = reason


@dataclass
class Tool:
    """A Python function an agent is allowed to call."""

    name: str
    description: str
    parameters: dict              # JSON Schema of the arguments ({"type": "object", ...})
    fn: Callable[..., Any]
    risk: str = "low"             # "low" | "medium" | "high" - the Governor uses this

    def run(self, args: dict) -> str:
        """Run the tool. Errors are returned as text so the agent can recover."""
        try:
            result = self.fn(**args)
        except StopAgent:
            raise
        except Exception as exc:  # a broken tool must never crash the whole agent
            return f"ERROR: {type(exc).__name__}: {exc}"
        if isinstance(result, str):
            return result
        return json.dumps(result, default=str, ensure_ascii=False)


@dataclass
class Usage:
    input_tokens: int = 0
    output_tokens: int = 0

    def add(self, input_tokens: int, output_tokens: int) -> None:
        self.input_tokens += input_tokens or 0
        self.output_tokens += output_tokens or 0


@dataclass
class AgentResult:
    """What an agent hands back when it finishes."""

    text: str
    turns: int
    usage: Usage
    tool_calls: list[dict] = field(default_factory=list)
    stopped_reason: str = "done"  # done | max_turns | budget | killed | refused | ...


@dataclass
class ToolCall:
    id: str
    name: str
    args: dict


@dataclass
class Step:
    """One reply from the model, translated into a provider-neutral shape."""

    text: str
    calls: list[ToolCall]
    input_tokens: int
    output_tokens: int
    refused: bool = False
    paused: bool = False


class Hooks:
    """Callbacks that let a supervisor watch and control an agent.

    The default does nothing. The Governor (common/governor.py) overrides them.
    """

    def before_turn(self, agent_name: str, turn: int) -> None:
        """Raise StopAgent to stop the agent before it calls the model again."""

    def on_usage(self, agent_name: str, model: str, input_tokens: int, output_tokens: int) -> None:
        """Called after every model call. Raise StopAgent to stop (e.g. over budget)."""

    def before_tool(self, agent_name: str, tool: Tool, args: dict) -> str | None:
        """Return a message to BLOCK the tool call, or None to allow it."""
        return None

    def after_tool(self, agent_name: str, tool: Tool, args: dict, result: str) -> None:
        """Called after a tool ran."""


# --------------------------------------------------------------------------
# The agent loop (shared by every provider)
# --------------------------------------------------------------------------

class BaseProvider:
    name = "base"
    model = "unknown"

    # Each provider fills in these three methods in its own SDK's format.
    def _start(self, system: str, task: str, tools: list[Tool], effort: str) -> Any:
        raise NotImplementedError

    def _step(self, state: Any) -> Step:
        raise NotImplementedError

    def _add_results(self, state: Any, results: list[tuple[ToolCall, str, bool]]) -> None:
        raise NotImplementedError

    def complete(self, system: str, prompt: str, *, json_schema: dict | None = None,
                 effort: str = "medium") -> tuple[str, Usage]:
        """One question, one answer (no tools). With json_schema the answer is JSON."""
        raise NotImplementedError

    def run_agent(self, *, name: str, system: str, task: str, tools: list[Tool],
                  max_turns: int = 10, hooks: Hooks | None = None,
                  effort: str = "medium") -> AgentResult:
        """THE AGENT LOOP. Read this function - it is the heart of every agent."""
        hooks = hooks or Hooks()
        tool_map = {t.name: t for t in tools}
        usage = Usage()
        calls_made: list[dict] = []
        state = self._start(system, task, tools, effort)
        last_text = ""

        for turn in range(1, max_turns + 1):
            # 1. Ask the supervisor if we may continue (kill switch, turn limits...).
            try:
                hooks.before_turn(name, turn)
            except StopAgent as stop:
                return AgentResult(last_text or f"(stopped: {stop.reason})", turn - 1,
                                   usage, calls_made, stop.reason)

            # 2. Call the model.
            step = self._step(state)
            usage.add(step.input_tokens, step.output_tokens)
            last_text = step.text or last_text
            try:
                hooks.on_usage(name, self.model, step.input_tokens, step.output_tokens)
            except StopAgent as stop:
                return AgentResult(last_text or f"(stopped: {stop.reason})", turn,
                                   usage, calls_made, stop.reason)

            if step.refused:
                return AgentResult("(the model declined this request)", turn, usage,
                                   calls_made, "refused")
            if step.paused:      # long server-side work; just continue the loop
                continue

            # 3. No tool requests? Then the agent is finished.
            if not step.calls:
                return AgentResult(step.text, turn, usage, calls_made, "done")

            # 4. Run each requested tool (if the supervisor allows it).
            results: list[tuple[ToolCall, str, bool]] = []
            for call in step.calls:
                tool = tool_map.get(call.name)
                if tool is None:
                    output, is_error = f"ERROR: there is no tool named '{call.name}'.", True
                else:
                    blocked = hooks.before_tool(name, tool, call.args)
                    if blocked:
                        output, is_error = f"BLOCKED by supervisor: {blocked}", True
                    else:
                        output = tool.run(call.args)
                        is_error = output.startswith("ERROR")
                        hooks.after_tool(name, tool, call.args, output)
                calls_made.append({"tool": call.name, "args": call.args, "result": output[:300]})
                results.append((call, output, is_error))

            # 5. Send the results back and go around again.
            self._add_results(state, results)

        return AgentResult(last_text or "(stopped: reached max_turns)", max_turns, usage,
                           calls_made, "max_turns")


# --------------------------------------------------------------------------
# Claude (Anthropic)
# --------------------------------------------------------------------------

class ClaudeProvider(BaseProvider):
    name = "claude"

    def __init__(self, model: str | None = None):
        import anthropic

        self.client = anthropic.Anthropic()  # reads ANTHROPIC_API_KEY from .env
        self.model = model or config.CLAUDE_MODEL

    def _create(self, **kwargs):
        # Server-side fallbacks: if a safety check declines a request, the API
        # automatically retries it on a suitable fallback model in the same call.
        return self.client.beta.messages.create(
            model=self.model,
            betas=["server-side-fallback-2026-07-01"],
            fallbacks="default",
            **kwargs,
        )

    def complete(self, system, prompt, *, json_schema=None, effort="medium"):
        output_config: dict = {"effort": effort}
        if json_schema:
            output_config["format"] = {"type": "json_schema", "schema": json_schema}
        response = self._create(
            max_tokens=16000,
            system=system,
            messages=[{"role": "user", "content": prompt}],
            output_config=output_config,
        )
        if response.stop_reason == "refusal":
            raise RuntimeError("Claude declined this request (stop_reason=refusal).")
        text = "".join(b.text for b in response.content if b.type == "text")
        return text, Usage(response.usage.input_tokens, response.usage.output_tokens)

    def _start(self, system, task, tools, effort):
        return {
            "system": system,
            "effort": effort,
            "tools": [
                {"name": t.name, "description": t.description, "input_schema": t.parameters}
                for t in tools
            ],
            "messages": [{"role": "user", "content": task}],
        }

    def _step(self, state) -> Step:
        kwargs = dict(
            max_tokens=16000,
            system=state["system"],
            messages=state["messages"],
            output_config={"effort": state["effort"]},
        )
        if state["tools"]:
            kwargs["tools"] = state["tools"]
        response = self._create(**kwargs)
        # Keep the FULL reply (including thinking and tool_use blocks) in the history.
        state["messages"].append({"role": "assistant", "content": response.content})
        text = "".join(b.text for b in response.content if b.type == "text")
        calls = [
            ToolCall(b.id, b.name, dict(b.input) if isinstance(b.input, dict) else {})
            for b in response.content
            if b.type == "tool_use"
        ]
        return Step(
            text=text,
            calls=calls,
            input_tokens=response.usage.input_tokens,
            output_tokens=response.usage.output_tokens,
            refused=response.stop_reason == "refusal",
            paused=response.stop_reason == "pause_turn",
        )

    def _add_results(self, state, results):
        # All tool results go back together in ONE user message.
        state["messages"].append({
            "role": "user",
            "content": [
                {"type": "tool_result", "tool_use_id": call.id, "content": output,
                 "is_error": is_error}
                for call, output, is_error in results
            ],
        })


# --------------------------------------------------------------------------
# Gemini (Google AI Studio)
# --------------------------------------------------------------------------

class GeminiProvider(BaseProvider):
    name = "gemini"

    def __init__(self, model: str | None = None):
        from google import genai

        self.client = genai.Client()  # reads GOOGLE_API_KEY (or GEMINI_API_KEY) from .env
        self.model = model or config.GEMINI_MODEL

    @staticmethod
    def _usage(response) -> tuple[int, int]:
        meta = response.usage_metadata
        if not meta:
            return 0, 0
        output = (meta.candidates_token_count or 0) + (meta.thoughts_token_count or 0)
        return meta.prompt_token_count or 0, output

    def complete(self, system, prompt, *, json_schema=None, effort="medium"):
        from google.genai import types

        cfg = types.GenerateContentConfig(system_instruction=system)
        if json_schema:
            cfg.response_mime_type = "application/json"
            cfg.response_json_schema = json_schema
        response = self.client.models.generate_content(model=self.model, contents=prompt,
                                                       config=cfg)
        return response.text or "", Usage(*self._usage(response))

    def _start(self, system, task, tools, effort):
        from google.genai import types

        declarations = [
            types.FunctionDeclaration(name=t.name, description=t.description,
                                      parameters_json_schema=t.parameters)
            for t in tools
        ]
        config_ = types.GenerateContentConfig(
            system_instruction=system,
            tools=[types.Tool(function_declarations=declarations)] if declarations else None,
            # We run the tools ourselves so the Governor can check every call.
            automatic_function_calling=types.AutomaticFunctionCallingConfig(disable=True),
        )
        contents = [types.Content(role="user", parts=[types.Part.from_text(text=task)])]
        return {"config": config_, "contents": contents}

    def _step(self, state) -> Step:
        response = self.client.models.generate_content(
            model=self.model, contents=state["contents"], config=state["config"])
        input_tokens, output_tokens = self._usage(response)
        candidate = response.candidates[0] if response.candidates else None
        if candidate is None or candidate.content is None:
            return Step("", [], input_tokens, output_tokens, refused=True)
        # Keep the model's full reply (it may carry "thought signatures" Gemini needs).
        state["contents"].append(candidate.content)
        calls = [
            ToolCall(fc.id or fc.name, fc.name, dict(fc.args or {}))
            for fc in (response.function_calls or [])
        ]
        text = "".join(p.text for p in (candidate.content.parts or [])
                       if getattr(p, "text", None) and not getattr(p, "thought", False))
        return Step(text, calls, input_tokens, output_tokens)

    def _add_results(self, state, results):
        from google.genai import types

        parts = [
            types.Part(function_response=types.FunctionResponse(
                id=call.id if call.id != call.name else None,
                name=call.name,
                response={"error": output} if is_error else {"result": output},
            ))
            for call, output, is_error in results
        ]
        state["contents"].append(types.Content(role="user", parts=parts))


# --------------------------------------------------------------------------
# Mock (offline, free) - for practice and automated tests
# --------------------------------------------------------------------------

def fake_from_schema(schema: dict, prop_name: str = "") -> Any:
    """Invent a value that fits a JSON schema. Used by the offline mock model."""
    if "enum" in schema:
        return schema["enum"][0]
    kind = schema.get("type", "string")
    if isinstance(kind, list):
        kind = kind[0]
    if kind == "object":
        props = schema.get("properties", {})
        return {key: fake_from_schema(sub, key) for key, sub in props.items()}
    if kind == "array":
        items = schema.get("items", {})
        if "enum" in items:
            return []  # e.g. a list of tool names: grant nothing by default
        return [fake_from_schema(items, prop_name)]
    if kind == "integer":
        return max(1, int(schema.get("minimum", 3)))
    if kind == "number":
        return 1.0
    if kind == "boolean":
        return True
    canned = {
        "expression": "2 + 2",
        "path": "mock_output.txt",
        "folder": ".",
        "url": "https://example.com",          # not on the allowlist -> no real download
        "code": "print('hello from the mock agent')",
    }
    if "name" in prop_name:
        return "example-agent"
    if prop_name in canned:
        return canned[prop_name]
    if prop_name == "instructions":
        return "You are an example agent created by the offline mock model. Do the task briefly."
    return f"example {prop_name or 'text'}"


class MockProvider(BaseProvider):
    """A fake model. No internet, no key, no cost.

    It is not smart: it calls each tool it is given once (with made-up
    arguments) and then says it is done. That is enough to watch the agent
    loop, the Governor and the logs work - without spending money.
    """

    name = "mock"

    def __init__(self, model: str | None = None):
        self.model = model or "mock-model"

    def complete(self, system, prompt, *, json_schema=None, effort="medium"):
        tokens_in = (len(system) + len(prompt)) // 4
        if json_schema:
            return json.dumps(fake_from_schema(json_schema)), Usage(tokens_in, 60)
        return f"[mock answer] Here is my reply to: {prompt[:100]}", Usage(tokens_in, 40)

    def _start(self, system, task, tools, effort):
        return {"task": task, "pending": list(tools), "results": [], "chars": len(system + task)}

    def _step(self, state) -> Step:
        tokens_in = state["chars"] // 4 + 50 * len(state["results"])
        if state["pending"]:
            tool = state["pending"].pop(0)
            args = fake_from_schema(tool.parameters)
            return Step(f"I will use {tool.name}.",
                        [ToolCall(f"call_{tool.name}", tool.name, args)], tokens_in, 30)
        summary = "; ".join(f"{c.name} -> {out[:60]}" for c, out, _ in state["results"])
        text = f"[mock agent] Finished the task: {state['task'][:80]}"
        if summary:
            text += f"\nTools used: {summary}"
        return Step(text, [], tokens_in, 40)

    def _add_results(self, state, results):
        state["results"].extend(results)


# --------------------------------------------------------------------------
# Pick a provider
# --------------------------------------------------------------------------

_MOCK_NOTICE_SHOWN = False


def get_llm(provider: str | None = None, *, worker: bool = False) -> BaseProvider:
    """Return a ready-to-use model client.

    provider: "claude", "gemini" or "mock" (default: LLM_PROVIDER from .env)
    worker:   True = use the worker model (for sub-agents)
    """
    provider = (provider or config.PROVIDER).lower()
    if provider == "claude":
        return ClaudeProvider(config.CLAUDE_WORKER_MODEL if worker else config.CLAUDE_MODEL)
    if provider == "gemini":
        return GeminiProvider(config.GEMINI_WORKER_MODEL if worker else config.GEMINI_MODEL)
    if provider == "mock":
        global _MOCK_NOTICE_SHOWN
        if not _MOCK_NOTICE_SHOWN:
            import sys
            print("ℹ️  Offline practice mode (mock model): answers are fake and free. "
                  "Add GOOGLE_API_KEY to .env for real answers.", file=sys.stderr)
            _MOCK_NOTICE_SHOWN = True
        return MockProvider()
    raise ValueError(f"Unknown LLM_PROVIDER '{provider}'. Use claude, gemini or mock.")
