"""AgentSpec: the "job description" of an agent, written as data.

This is the key idea of the whole course:

    An agent = instructions + tools + model + limits.

If we write that down as data (JSON), then ANOTHER agent can write it too.
That is how agents build agents: one agent writes an AgentSpec, our code
checks it, saves it, and turns it into a running agent.

Example AgentSpec (JSON):
{
  "name": "budget-analyst",
  "role": "Checks numbers in budget documents",
  "instructions": "You are a careful budget analyst. ...",
  "tools": ["read_file", "calculator"],
  "max_turns": 6
}
"""
from __future__ import annotations

import re

from pydantic import BaseModel, Field, field_validator

from common.toolbox import TOOLBOX

NAME_PATTERN = re.compile(r"^[a-z][a-z0-9-]{2,40}$")

# A special "tool" that lets an agent create and run other agents.
# Only granted when the Governor's depth limit allows it.
SPAWN_PERMISSION = "spawn_agents"


class AgentSpec(BaseModel):
    name: str = Field(description="lowercase-with-dashes, e.g. 'budget-analyst'")
    role: str = Field(description="One sentence: what this agent is for")
    instructions: str = Field(description="The agent's system prompt")
    tools: list[str] = Field(default_factory=list, description="Tool names from the toolbox")
    max_turns: int = Field(default=8, ge=1, le=25)
    model_tier: str = Field(default="worker", description="'main' or 'worker'")
    created_by: str = "human"
    parent: str | None = None
    version: int = 1

    @field_validator("name")
    @classmethod
    def _check_name(cls, value: str) -> str:
        value = value.strip().lower().replace(" ", "-").replace("_", "-")
        if not NAME_PATTERN.match(value):
            raise ValueError("name must be 3-41 chars: lowercase letters, digits, dashes")
        return value

    @field_validator("tools")
    @classmethod
    def _check_tools(cls, value: list[str]) -> list[str]:
        allowed = set(TOOLBOX) | {SPAWN_PERMISSION}
        unknown = [t for t in value if t not in allowed]
        if unknown:
            raise ValueError(f"unknown tools {unknown}; choose from {sorted(allowed)}")
        return sorted(set(value))

    @field_validator("instructions")
    @classmethod
    def _check_instructions(cls, value: str) -> str:
        if len(value.strip()) < 20:
            raise ValueError("instructions are too short to be useful (min 20 characters)")
        return value.strip()


def agent_spec_schema(allowed_tools: list[str] | None = None) -> dict:
    """JSON Schema the model must follow when it designs a new agent.

    We write it by hand (simple, no $refs) so both Claude and Gemini accept it.
    """
    tool_names = sorted(allowed_tools if allowed_tools is not None else TOOLBOX)
    return {
        "type": "object",
        "properties": {
            "name": {"type": "string", "description": "lowercase-with-dashes, 3-41 chars"},
            "role": {"type": "string", "description": "one sentence"},
            "instructions": {"type": "string",
                             "description": "the full system prompt for the new agent"},
            "tools": {"type": "array", "items": {"type": "string", "enum": tool_names}},
            "max_turns": {"type": "integer", "description": "between 1 and 25"},
        },
        "required": ["name", "role", "instructions", "tools", "max_turns"],
        "additionalProperties": False,
    }


def team_plan_schema(allowed_tools: list[str] | None = None) -> dict:
    """JSON Schema for a whole team: several agents plus the order to run them."""
    return {
        "type": "object",
        "properties": {
            "summary": {"type": "string", "description": "the plan in two sentences"},
            "agents": {"type": "array", "items": agent_spec_schema(allowed_tools)},
            "steps": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "agent": {"type": "string", "description": "name of an agent above"},
                        "task": {"type": "string", "description": "what this agent must do"},
                    },
                    "required": ["agent", "task"],
                    "additionalProperties": False,
                },
            },
            "success_criteria": {"type": "array", "items": {"type": "string"}},
        },
        "required": ["summary", "agents", "steps", "success_criteria"],
        "additionalProperties": False,
    }
