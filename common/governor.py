"""The Governor: the supervisor that keeps every agent under control.

When agents can create other agents, you need rules that NO agent can
change. The Governor enforces them from outside the model:

    1. BUDGET      - stop when the run has spent more than $X
    2. TURN LIMIT  - stop after N model calls in total
    3. HEADCOUNT   - at most N agents may be created in one run
    4. DEPTH LIMIT - agents may create agents only N levels deep
    5. TOOL CEILING- a new agent can never get a tool outside the allowed list,
                     and never more power than its parent
    6. APPROVALS   - a human says yes/no before risky tools or new agents
    7. KILL SWITCH - create a file called STOP in the repo root -> everything halts
    8. AUDIT LOG   - every action is written to logs/run-<id>.jsonl

The model cannot talk its way past these rules, because they are plain
Python code, not instructions in a prompt.
"""
from __future__ import annotations

import datetime as _dt
import json
import uuid
from dataclasses import dataclass, field

from common import config, show
from common.llm import Hooks, StopAgent, Tool
from common.spec import SPAWN_PERMISSION, AgentSpec
from common.toolbox import TOOLBOX


@dataclass
class Policy:
    max_usd: float = config.MAX_USD_PER_RUN
    max_total_turns: int = 80
    max_agents: int = config.MAX_AGENTS_PER_RUN
    max_depth: int = config.MAX_SPAWN_DEPTH
    # Tools any agent in this run may ever hold (the "ceiling").
    allowed_tools: set[str] = field(default_factory=lambda: set(TOOLBOX) | {SPAWN_PERMISSION})
    # Tool risk levels that need a human "yes" before running.
    approval_for_risk: set[str] = field(default_factory=lambda: {"high"})
    # Ask a human before any new agent is created?
    approve_new_agents: bool = False
    # For automated tests: answer every approval question with this ("yes"/"no").
    auto_answer: str | None = None


class AuditLog:
    """Writes one JSON line per event. Open logs/ to read it after a run."""

    def __init__(self, run_id: str):
        self.path = config.LOGS / f"run-{run_id}.jsonl"

    def write(self, event: str, agent: str = "-", **details) -> None:
        record = {"time": _dt.datetime.now().isoformat(timespec="seconds"),
                  "event": event, "agent": agent, **details}
        with self.path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(record, default=str, ensure_ascii=False) + "\n")


class Governor(Hooks):
    def __init__(self, policy: Policy | None = None, run_id: str | None = None,
                 verbose: bool = True):
        self.policy = policy or Policy()
        self.run_id = run_id or _dt.datetime.now().strftime("%Y%m%d-%H%M%S-") + uuid.uuid4().hex[:4]
        self.log = AuditLog(self.run_id)
        self.verbose = verbose
        self.spent_usd = 0.0
        self.total_turns = 0
        self.agents_created = 0
        self.log.write("run_started", policy={
            "max_usd": self.policy.max_usd, "max_agents": self.policy.max_agents,
            "max_depth": self.policy.max_depth, "max_total_turns": self.policy.max_total_turns,
            "approval_for_risk": sorted(self.policy.approval_for_risk),
        })

    # ----- helpers --------------------------------------------------------
    def _say(self, who: str, what: str, style: str = "yellow") -> None:
        if self.verbose:
            show.event(f"[governor] {who}", what, style)

    def check_kill_switch(self) -> None:
        if config.KILL_SWITCH_FILE.exists():
            self.log.write("killed", reason="STOP file found")
            raise StopAgent("killed (STOP file found - delete it to allow runs again)")

    def ask_human(self, question: str) -> bool:
        if self.policy.auto_answer is not None:
            answer = self.policy.auto_answer
        else:
            try:
                answer = input(f"\n🛑 APPROVAL NEEDED: {question}\n   Type yes or no: ")
            except EOFError:  # no keyboard available (e.g. running in the background)
                answer = "no"
        approved = answer.strip().lower() in ("y", "yes")
        self.log.write("human_decision", question=question, approved=approved)
        return approved

    # ----- hooks called by the agent loop ---------------------------------
    def before_turn(self, agent_name: str, turn: int) -> None:
        self.check_kill_switch()
        self.total_turns += 1
        if self.total_turns > self.policy.max_total_turns:
            self.log.write("stopped", agent_name, reason="turn limit")
            raise StopAgent("turn limit reached")

    def on_usage(self, agent_name: str, model: str, input_tokens: int, output_tokens: int) -> None:
        cost = config.cost_usd(model, input_tokens, output_tokens)
        self.spent_usd += cost
        self.log.write("model_call", agent_name, model=model, input_tokens=input_tokens,
                       output_tokens=output_tokens, cost_usd=round(cost, 5),
                       total_usd=round(self.spent_usd, 5))
        if self.spent_usd > self.policy.max_usd:
            self._say(agent_name, f"budget exceeded (${self.spent_usd:.3f} > "
                                  f"${self.policy.max_usd:.2f}) - stopping", "red")
            self.log.write("stopped", agent_name, reason="budget")
            raise StopAgent("budget")

    def before_tool(self, agent_name: str, tool: Tool, args: dict) -> str | None:
        self.check_kill_switch()
        self.log.write("tool_requested", agent_name, tool=tool.name, risk=tool.risk, args=args)
        if tool.risk in self.policy.approval_for_risk:
            preview = json.dumps(args, ensure_ascii=False)[:400]
            if not self.ask_human(f"Agent '{agent_name}' wants to run {tool.name} "
                                  f"(risk: {tool.risk}) with {preview}"):
                self.log.write("tool_blocked", agent_name, tool=tool.name, reason="human said no")
                return "A human reviewer declined this action. Try another way or explain."
        self._say(agent_name, f"uses {tool.name} {json.dumps(args, ensure_ascii=False)[:120]}",
                  "cyan")
        return None

    def after_tool(self, agent_name: str, tool: Tool, args: dict, result: str) -> None:
        self.log.write("tool_result", agent_name, tool=tool.name, result=result[:500])

    # ----- rules for creating agents --------------------------------------
    def approve_new_agent(self, spec: AgentSpec, depth: int,
                          parent_tools: set[str] | None) -> tuple[bool, str]:
        """Decide whether a proposed agent may be created. Returns (ok, reason)."""
        self.check_kill_switch()
        if self.agents_created >= self.policy.max_agents:
            return False, f"headcount limit: max {self.policy.max_agents} new agents per run"
        if depth > self.policy.max_depth:
            return False, f"depth limit: agents may only be created {self.policy.max_depth} levels deep"
        outside_ceiling = set(spec.tools) - self.policy.allowed_tools
        if outside_ceiling:
            return False, f"tools not allowed in this run: {sorted(outside_ceiling)}"
        if parent_tools is not None:
            # No privilege escalation: a child can't have tools its parent lacks
            # (except basic low-risk tools, which are always fine).
            low_risk = {n for n, t in TOOLBOX.items() if t.risk == "low"}
            escalation = set(spec.tools) - parent_tools - low_risk
            if escalation:
                return False, f"a new agent cannot have more power than its creator: {sorted(escalation)}"
        if self.policy.approve_new_agents:
            question = (f"Create agent '{spec.name}' ({spec.role}) with tools "
                        f"{spec.tools or 'none'}?\n   Instructions: {spec.instructions[:300]}")
            if not self.ask_human(question):
                return False, "a human reviewer declined this new agent"
        self.agents_created += 1
        self.log.write("agent_created", spec.name, depth=depth, tools=spec.tools,
                       created_by=spec.created_by, role=spec.role)
        return True, "ok"

    def summary(self) -> str:
        return (f"Run {self.run_id}: spent ~${self.spent_usd:.4f} of ${self.policy.max_usd:.2f}, "
                f"{self.total_turns} model calls, {self.agents_created} agents created. "
                f"Audit log: {config.rel(self.log.path)}")
