"""Pattern 2 - ROUTER (receptionist): classify the request, send it to the right specialist.

Run it:  python lessons/05_multi_agent_patterns/p2_router.py "your request"

              ┌-> [IT helpdesk specialist]
   [router] --+-> [HR policy specialist]
              └-> [Finance specialist]

When to use: requests come in different kinds that need different expertise.
Why it works: each specialist has a focused prompt; the router's answer is
STRUCTURED (JSON with a fixed list of choices), so code can act on it safely.
"""
import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))

from common import show
from common.llm import get_llm

SPECIALISTS = {
    "it": "You are an IT helpdesk specialist. Give numbered troubleshooting steps.",
    "hr": "You are an HR policy advisor. Be accurate, kind, and suggest who to contact.",
    "finance": "You are a finance officer. Be precise with numbers and approval rules.",
}
ROUTE_SCHEMA = {
    "type": "object",
    "properties": {
        "category": {"type": "string", "enum": list(SPECIALISTS)},
        "reason": {"type": "string"},
    },
    "required": ["category", "reason"],
    "additionalProperties": False,
}

request = " ".join(sys.argv[1:]) or "My laptop won't connect to the office VPN since this morning."
llm = get_llm(worker=True)
show.title(f"ROUTER pattern - {llm.name}/{llm.model}")
show.panel(request, "Incoming request")

decision_text, _ = llm.complete("Classify the request into exactly one category.", request,
                                json_schema=ROUTE_SCHEMA, effort="low")
decision = json.loads(decision_text)
show.event("[router]", f"-> {decision['category']} ({decision['reason']})", "yellow")

answer, _ = llm.complete(SPECIALISTS[decision["category"]], request, effort="low")
show.panel(answer, f"Answer from the {decision['category']} specialist", "cyan")
