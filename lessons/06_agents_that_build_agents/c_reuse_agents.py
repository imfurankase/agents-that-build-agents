"""Lesson 06c - Agents are assets: list, reuse, improve and retire saved agents.

Run it:  python lessons/06_agents_that_build_agents/c_reuse_agents.py            (list them)
         python lessons/06_agents_that_build_agents/c_reuse_agents.py run NAME "task"
         python lessons/06_agents_that_build_agents/c_reuse_agents.py improve NAME "what to improve"
         python lessons/06_agents_that_build_agents/c_reuse_agents.py retire NAME
         python lessons/06_agents_that_build_agents/c_reuse_agents.py examples

"improve" asks the Architect to write a better version of an existing agent
(version number goes up). That is an agent improving another agent.

"examples" installs the 3 ready-made example agents from agent_registry/examples/
(meeting-scribe, policy-qa, briefing-writer) into your registry. Agents you
already have with the same name are left untouched.
"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))

from common import config, show
from common.foundry import AgentFoundry
from common.spec import AgentSpec

foundry = AgentFoundry()
args = sys.argv[1:]
command = args[0] if args else "list"

if command == "list":
    show.panel(foundry.registry.summary(), "Saved agents (agent_registry/)")

elif command == "examples":
    examples_dir = config.ROOT / "agent_registry" / "examples"
    installed, skipped = [], []
    for path in sorted(examples_dir.glob("*.json")):
        spec = AgentSpec.model_validate_json(path.read_text(encoding="utf-8"))
        if foundry.registry.get(spec.name):
            skipped.append(spec.name)
            continue
        foundry.registry.save(spec)
        installed.append(spec.name)
    show.panel(f"Installed: {', '.join(installed) or 'none'}\n"
               f"Already present (skipped): {', '.join(skipped) or 'none'}\n\n"
               f"{foundry.registry.summary()}", "Example agents")

elif command == "run" and len(args) >= 3:
    result = foundry.run(args[1], " ".join(args[2:]))
    show.panel(result.text, f"{args[1]} ({result.stopped_reason})")
    show.info(foundry.governor.summary())

elif command == "improve" and len(args) >= 3:
    old = foundry.registry.get(args[1])
    if old is None:
        sys.exit(f"No agent named {args[1]}")
    request = (f"Improve this existing agent. Keep the name '{old.name}'.\n"
               f"Current role: {old.role}\nCurrent tools: {old.tools}\n"
               f"Current instructions:\n{old.instructions}\n\n"
               f"Requested improvement: {' '.join(args[2:])}")
    new = foundry.design_agent(request, created_by="architect (improvement)")
    new = new.model_copy(update={"name": old.name})
    ok, reason = foundry.register(new)
    show.panel(new.instructions, f"New instructions for {new.name}" if ok else reason, "cyan")

elif command == "retire" and len(args) >= 2:
    done = foundry.registry.retire(args[1])
    print(f"Retired {args[1]}" if done else f"No agent named {args[1]}")

else:
    print(__doc__)
