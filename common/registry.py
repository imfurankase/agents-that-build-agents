"""The Agent Registry: a folder of saved agents (one JSON file per agent).

Why save agents? Because an agent that another agent designed is an ASSET.
Once it is saved you can read it, review it, improve it, reuse it in another
run, or retire it. Open the `agent_registry/` folder to see them.
"""
from __future__ import annotations

import json
from pathlib import Path

from common import config
from common.spec import AgentSpec


class AgentRegistry:
    def __init__(self, folder: Path | None = None):
        self.folder = folder or config.REGISTRY_DIR
        self.retired = self.folder / "retired"
        self.folder.mkdir(parents=True, exist_ok=True)

    def _path(self, name: str) -> Path:
        return self.folder / f"{name}.json"

    def save(self, spec: AgentSpec) -> Path:
        """Save (or update) an agent. Updating bumps its version number."""
        existing = self.get(spec.name)
        if existing:
            spec = spec.model_copy(update={"version": existing.version + 1})
        path = self._path(spec.name)
        path.write_text(json.dumps(spec.model_dump(), indent=2, ensure_ascii=False),
                        encoding="utf-8")
        return path

    def get(self, name: str) -> AgentSpec | None:
        path = self._path(name)
        if not path.exists():
            return None
        return AgentSpec.model_validate_json(path.read_text(encoding="utf-8"))

    def list(self) -> list[AgentSpec]:
        specs = []
        for path in sorted(self.folder.glob("*.json")):
            try:
                specs.append(AgentSpec.model_validate_json(path.read_text(encoding="utf-8")))
            except Exception:
                continue  # skip broken files instead of crashing
        return specs

    def retire(self, name: str) -> bool:
        """Move an agent to agent_registry/retired/ (kept for the record, not deleted)."""
        path = self._path(name)
        if not path.exists():
            return False
        self.retired.mkdir(exist_ok=True)
        path.replace(self.retired / path.name)
        return True

    def summary(self) -> str:
        specs = self.list()
        if not specs:
            return "(no agents saved yet)"
        return "\n".join(
            f"- {s.name} v{s.version}: {s.role} | tools: {', '.join(s.tools) or 'none'}"
            f" | created by: {s.created_by}"
            for s in specs
        )
