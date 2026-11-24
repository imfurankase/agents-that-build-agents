# Costs, data and safety

## 1. Money: three different meters

| What you use | How it is paid | Where to watch it |
|---|---|---|
| **Claude Code** (VS Code panel, CLI, `claude -p`) | Your Claude **subscription**, within plan usage limits | `/usage` in Claude Code |
| **Claude API** (`ANTHROPIC_API_KEY`, Agent SDK) | **Per token**, separate from the subscription | Anthropic Console: usage and **spend limits** |
| **Gemini API** (`GOOGLE_API_KEY`) | **Free tier** within rate limits; paid tier per token | Google AI Studio / Google Cloud billing |
| **Mock mode** | Free | — |

> **Trap:** if `ANTHROPIC_API_KEY` is set, `claude -p` bills the API instead of your subscription. The course helper removes it for its own calls.

### How the Governor estimates cost
Every model call reports tokens in/out. `common/config.py` multiplies them by a price table (Claude list prices; a cautious placeholder for Gemini) and the Governor adds them up. When the total passes `MAX_USD_PER_RUN`, the run stops. It's an **estimate**: the provider's bill is the truth. On the Gemini free tier the real cost is $0.

### Set limits at the source too
- **Anthropic Console:** set a monthly spend limit before adding credit.
- **Google:** use the free tier while learning; if you enable billing, set budget alerts in Google Cloud.
- **Claude Code:** headless runs accept `--max-budget-usd` and `--max-turns`.

### Cost-saving habits
1. **Practise in mock mode** (`LLM_PROVIDER=mock`): mechanics are identical, cost is zero.
2. **Use cheaper worker models** for sub-agents (`CLAUDE_WORKER_MODEL` / `GEMINI_WORKER_MODEL`), and keep the strongest model for planning and judging. Your call, not the code's.
3. **Lower effort** for simple tasks (`effort="low"`).
4. **Small `max_turns`** (3-8) and **small teams** (2-3 agents).
5. **Reuse saved agents** instead of designing new ones every run.
6. **Keep prompts stable** so caching can work; put changing details at the end.
7. Don't loop `claude -p`: each call loads a large toolkit context.

---

## 2. Data: what goes where

| Never | Why |
|---|---|
| Paste API keys, passwords or tokens into any chat | Chats are stored; keys must stay in `.env` (which Claude Code is blocked from reading here) |
| Paste confidential, classified or personal data into free-tier tools | Free tiers may use data to improve products; check the provider's current terms |
| Commit `.env` to git | It's in `.gitignore`; keep it that way |
| Give agents access to real systems while learning | Use `workspace/` sample files instead |

Built-in protections in this repo:
- Python agents can only read and write inside `workspace/`.
- `fetch_webpage` only opens allow-listed sites (`WEB_ALLOWLIST`).
- Web content is labelled *untrusted* before an agent sees it.
- Claude Code's guard hook blocks reading `.env` and destructive commands.

---

## 3. Safety: the agent checklist (from lesson 11)
1. **Purpose:** one clear job, written down.
2. **Tools:** least privilege; justify each one.
3. **Data:** what can it read? Could it see secrets or personal data?
4. **Untrusted input:** does it read web/email/files from outside? Then no unsupervised "act" tools.
5. **Limits:** max turns, budget, headcount, depth.
6. **Humans:** approval for irreversible or external actions.
7. **Audit:** logs reviewed regularly.
8. **Evals:** passes its test suite, including injection cases.
9. **Kill switch:** you know how to stop it now.

## 4. Design principles for agents that create agents (from lesson 07)
1. **Deny by default:** new agents start with no tools.
2. **Inherit, never escalate:** a creator can only grant tools it holds.
3. **Bound everything:** money, turns, headcount, depth, time.
4. **Humans approve the irreversible:** spending, sending, deleting, publishing, hiring.
5. **Log everything, review regularly.**
6. **One big red button:** a kill switch any human can press.

---

## 5. Organisational policy starter (adapt before use)

> A starting point for a team or department policy on AI agents. Review with your legal, security and data-protection colleagues.

**Scope.** Applies to any AI system that takes actions (calls tools, edits files, sends messages, creates other agents) on behalf of staff.

**Roles.**
| Role | May do |
|---|---|
| Agent user | Use approved agents for approved tasks |
| Agent builder | Create/modify agents in sandbox environments |
| Agent owner | Accountable for one production agent: purpose, access, evals, logs |
| Reviewer (security/data) | Approves agents rated Medium/High risk before production |

**Risk levels and approvals.**
| Risk | Examples | Approval before production |
|---|---|---|
| Low | Read-only, public or sample data, no external actions | Agent owner |
| Medium | Writes files, reads internal documents, uses the web | Owner + reviewer |
| High | Sends messages, changes systems, runs code, handles personal/classified data, **creates other agents** | Owner + reviewer + senior sign-off; human approval gate on every high-risk action |

**Mandatory controls (all production agents).** Written purpose; least-privilege tools; budget and turn limits; audit logging; a named owner; an eval suite with a minimum pass rate; a documented kill switch.

**Agents that create agents.** Allowed only with: a headcount and depth limit, a tool ceiling, no privilege escalation, human approval of new agents in production, and the created agents saved to a registry for review.

**Logging and retention.** Keep agent audit logs for a defined period (set by your records policy); review a sample monthly; review all blocked/stopped events.

**Review cadence.** Re-run evals on every change and at least quarterly; re-approve agents when their tools, data access or model changes.

**Incidents.** Any unexpected action, data exposure or prompt-injection event: press the kill switch, preserve logs, report to security.
