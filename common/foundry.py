"""The Agent Foundry: where agents are designed, built, run - and build each other.

Three ways an agent gets made in this course:

  1. A HUMAN writes an AgentSpec (a JSON file in agent_registry/).
  2. The ARCHITECT designs one from a plain-English goal  -> design_agent()
  3. A RUNNING AGENT creates one with its create_agent tool -> meta_tools()

Every new agent passes through the Governor first. No exceptions.

Prompts live in prompts/system/*.md so you can change how agents behave by
editing text, not code.
"""
from __future__ import annotations

import json

from pydantic import ValidationError

from common import config, show
from common.governor import Governor
from common.llm import AgentResult, BaseProvider, Tool, get_llm
from common.registry import AgentRegistry
from common.spec import SPAWN_PERMISSION, AgentSpec, agent_spec_schema, team_plan_schema
from common.toolbox import TOOLBOX, describe_toolbox, tools_by_name

PROMPTS = config.ROOT / "prompts" / "system"


def load_prompt(name: str, **values) -> str:
    """Read prompts/system/<name>.md and fill in {{PLACEHOLDERS}}."""
    text = (PROMPTS / f"{name}.md").read_text(encoding="utf-8")
    for key, value in values.items():
        text = text.replace("{{" + key + "}}", str(value))
    return text


def _schema_str(name: str) -> dict:
    return {"type": "string", "description": name}


class AgentFoundry:
    def __init__(self, governor: Governor | None = None, registry: AgentRegistry | None = None,
                 provider: str | None = None, verbose: bool = True):
        self.governor = governor or Governor(verbose=verbose)
        self.registry = registry or AgentRegistry()
        self.provider = provider          # None = use LLM_PROVIDER from .env
        self.verbose = verbose

    # ------------------------------------------------------------------
    # helpers
    # ------------------------------------------------------------------
    def _llm(self, main: bool) -> BaseProvider:
        return get_llm(self.provider, worker=not main)

    def _say(self, who: str, what: str, style: str = "green") -> None:
        if self.verbose:
            show.event(who, what, style)

    def _allowed_tool_names(self) -> list[str]:
        return sorted(t for t in TOOLBOX if t in self.governor.policy.allowed_tools)

    # ------------------------------------------------------------------
    # 1) The architect: an LLM designs an agent from a goal
    # ------------------------------------------------------------------
    def design_agent(self, goal: str, created_by: str = "architect") -> AgentSpec:
        """Ask the model to write an AgentSpec (JSON) for a plain-English goal."""
        llm = self._llm(main=True)
        system = load_prompt("agent_architect", TOOLBOX=describe_toolbox())
        text, usage = llm.complete(system, f"Design one agent for this goal:\n\n{goal}",
                                   json_schema=agent_spec_schema(self._allowed_tool_names()),
                                   effort="high")
        self.governor.on_usage("architect", llm.model, usage.input_tokens, usage.output_tokens)
        data = json.loads(text)
        data.update(created_by=created_by)
        data["max_turns"] = min(max(int(data.get("max_turns", 6)), 1), 25)
        return AgentSpec.model_validate(data)

    def plan_team(self, goal: str) -> dict:
        """Ask the model to design a whole team (agents + steps + success criteria)."""
        llm = self._llm(main=True)
        system = load_prompt("team_planner", TOOLBOX=describe_toolbox(),
                             MAX_AGENTS=self.governor.policy.max_agents)
        text, usage = llm.complete(system, f"Goal:\n{goal}",
                                   json_schema=team_plan_schema(self._allowed_tool_names()),
                                   effort="high")
        self.governor.on_usage("planner", llm.model, usage.input_tokens, usage.output_tokens)
        return json.loads(text)

    def judge(self, work: str, criteria: list[str]) -> dict:
        """An LLM judge grades work against success criteria.

        Returns {"score": 0-10, "passed": bool, "feedback": [...], "checks": [...]}.
        """
        schema = {
            "type": "object",
            "properties": {
                "checks": {"type": "array", "items": {
                    "type": "object",
                    "properties": {"criterion": {"type": "string"}, "met": {"type": "boolean"},
                                   "evidence": {"type": "string"}},
                    "required": ["criterion", "met", "evidence"],
                    "additionalProperties": False}},
                "score": {"type": "integer", "description": "0-10"},
                "passed": {"type": "boolean"},
                "feedback": {"type": "array", "items": {"type": "string"}},
            },
            "required": ["checks", "score", "passed", "feedback"],
            "additionalProperties": False,
        }
        llm = self._llm(main=True)
        prompt = ("<criteria>\n" + "\n".join(f"- {c}" for c in criteria) +
                  f"\n</criteria>\n\n<work>\n{work}\n</work>")
        text, usage = llm.complete(load_prompt("judge"), prompt, json_schema=schema,
                                   effort="medium")
        self.governor.on_usage("judge", llm.model, usage.input_tokens, usage.output_tokens)
        verdict = json.loads(text)
        self.governor.log.write("judged", "judge", score=verdict.get("score"),
                                passed=verdict.get("passed"))
        return verdict

    # ------------------------------------------------------------------
    # 2) Register: the Governor decides, the registry remembers
    # ------------------------------------------------------------------
    def register(self, spec: AgentSpec, depth: int = 1,
                 creator_tools: set[str] | None = None) -> tuple[bool, str]:
        ok, reason = self.governor.approve_new_agent(spec, depth, creator_tools)
        if ok:
            path = self.registry.save(spec)
            self._say("[foundry]", f"hired '{spec.name}' (tools: {spec.tools or 'none'}) "
                                   f"-> {config.rel(path)}", "green")
        else:
            self._say("[foundry]", f"REFUSED '{spec.name}': {reason}", "red")
        return ok, reason

    # ------------------------------------------------------------------
    # 3) Run an agent
    # ------------------------------------------------------------------
    def run(self, agent: str | AgentSpec, task: str, depth: int = 1) -> AgentResult:
        spec = agent if isinstance(agent, AgentSpec) else self.registry.get(agent)
        if spec is None:
            raise ValueError(f"No agent named '{agent}' in the registry.")
        outside = set(spec.tools) - self.governor.policy.allowed_tools
        if outside:
            raise PermissionError(f"'{spec.name}' holds tools not allowed in this run: {outside}")

        tools: list[Tool] = tools_by_name(spec.tools)
        if SPAWN_PERMISSION in spec.tools:
            if depth + 1 <= self.governor.policy.max_depth:
                tools += self.meta_tools(spec, child_depth=depth + 1)
            else:
                self._say("[foundry]", f"'{spec.name}' may not create agents at depth "
                                       f"{depth + 1} (limit {self.governor.policy.max_depth})",
                          "yellow")

        system = spec.instructions + "\n\n" + load_prompt("common_rules")
        llm = self._llm(main=spec.model_tier == "main")
        self._say(f"▶ {spec.name}", f"starts: {task[:150]}", "bold blue")
        self.governor.log.write("agent_started", spec.name, task=task, depth=depth)
        result = llm.run_agent(name=spec.name, system=system, task=task, tools=tools,
                               max_turns=spec.max_turns, hooks=self.governor,
                               effort="high" if spec.model_tier == "main" else "medium")
        self.governor.log.write("agent_finished", spec.name, stopped_reason=result.stopped_reason,
                                turns=result.turns, result=result.text[:1000])
        self._say(f"■ {spec.name}", f"finished ({result.stopped_reason}, {result.turns} turns)",
                  "bold blue")
        return result

    # ------------------------------------------------------------------
    # 4) Meta-tools: the tools that let an AGENT build and command agents
    # ------------------------------------------------------------------
    def meta_tools(self, creator: AgentSpec, child_depth: int) -> list[Tool]:
        creator_tools = set(creator.tools)

        def create_agent(name: str, role: str, instructions: str, tools: list[str],
                         max_turns: int = 6) -> str:
            try:
                spec = AgentSpec(name=name, role=role, instructions=instructions, tools=tools,
                                 max_turns=min(max(int(max_turns), 1), 25),
                                 created_by=creator.name, parent=creator.name)
            except ValidationError as exc:
                return f"ERROR: that agent spec is invalid: {exc.errors()[0]['msg']}"
            ok, reason = self.register(spec, depth=child_depth, creator_tools=creator_tools)
            return f"Created agent '{spec.name}'." if ok else f"REFUSED by the Governor: {reason}"

        def run_agent(agent_name: str, task: str) -> str:
            if self.registry.get(agent_name) is None:
                return f"ERROR: no agent named '{agent_name}'. Use list_agents or create_agent."
            try:
                result = self.run(agent_name, task, depth=child_depth)
            except PermissionError as exc:
                return f"REFUSED by the Governor: {exc}"
            return (f"[{agent_name} finished: {result.stopped_reason}, {result.turns} turns]\n"
                    f"{result.text}")

        def list_agents() -> str:
            return self.registry.summary()

        def retire_agent(agent_name: str) -> str:
            done = self.registry.retire(agent_name)
            self.governor.log.write("agent_retired", agent_name, by=creator.name, ok=done)
            return f"Retired '{agent_name}'." if done else f"No agent named '{agent_name}'."

        tool_names = sorted(t for t in TOOLBOX if t in self.governor.policy.allowed_tools)
        if child_depth < self.governor.policy.max_depth:
            tool_names.append(SPAWN_PERMISSION)  # children may hire too (one level deeper)
        create_schema = {
            "type": "object",
            "properties": {
                "name": _schema_str("lowercase-with-dashes, e.g. 'fact-checker'"),
                "role": _schema_str("one sentence: what the agent is for"),
                "instructions": _schema_str("the new agent's full system prompt"),
                "tools": {"type": "array", "items": {"type": "string", "enum": tool_names},
                          "description": "the fewest tools it needs"},
                "max_turns": {"type": "integer", "description": "1-25, usually 3-8"},
            },
            "required": ["name", "role", "instructions", "tools", "max_turns"],
            "additionalProperties": False,
        }
        name_only = {"type": "object", "properties": {"agent_name": _schema_str("agent name")},
                     "required": ["agent_name"], "additionalProperties": False}
        return [
            Tool("list_agents", "List the agents that already exist (reuse them when they fit).",
                 {"type": "object", "properties": {}, "required": [],
                  "additionalProperties": False}, list_agents),
            Tool("create_agent", "Create (hire) a new specialist agent. The Governor may refuse.",
                 create_schema, create_agent, "medium"),
            Tool("run_agent", "Give an agent a task and get back its result.",
                 {"type": "object",
                  "properties": {"agent_name": _schema_str("which agent"),
                                 "task": _schema_str("a complete, self-contained task")},
                  "required": ["agent_name", "task"], "additionalProperties": False},
                 run_agent),
            Tool("retire_agent", "Retire an agent that is no longer needed.", name_only,
                 retire_agent),
        ]

    # ------------------------------------------------------------------
    # 5) The orchestrator: a manager agent that hires its own team
    # ------------------------------------------------------------------
    def orchestrator_spec(self, delegable_tools: list[str] | None = None) -> AgentSpec:
        """The top-level manager. It can only hand out tools it holds itself."""
        delegable = delegable_tools if delegable_tools is not None else [
            "save_note", "read_notes", "calculator", "get_current_datetime",
            "write_file", "read_file", "list_files", "fetch_webpage",
        ]
        return AgentSpec(
            name="orchestrator",
            role="Manager that builds and directs a team of agents",
            instructions=load_prompt("orchestrator", MAX_AGENTS=self.governor.policy.max_agents),
            tools=sorted(set(delegable) | {SPAWN_PERMISSION}),
            max_turns=20,
            model_tier="main",
            created_by="human",
        )

    def run_orchestrator(self, goal: str, delegable_tools: list[str] | None = None) -> AgentResult:
        return self.run(self.orchestrator_spec(delegable_tools), goal, depth=0)
