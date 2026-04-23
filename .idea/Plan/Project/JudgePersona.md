# Judge Personas — Demo Moments

> **Public figures named in [README.md](../README.md) vision section** (Suresh Srinivas, Sriharsha Chintalapani): treat as **distributed-systems + metadata-native** judges — they reward **contracts**, **failure behavior**, and **real OM depth**, not slideware.

## Three judge archetypes

| Archetype                | What they care about                               | What they click                                                         |
| ------------------------ | -------------------------------------------------- | ----------------------------------------------------------------------- |
| **Platform engineer**    | APIs, errors, logs, idempotency, HITL              | Swagger `/api/v1/docs`, `POST /chat`, `POST /chat/confirm`, network tab |
| **Data governance lead** | Tagging, lineage, policy, catalog truth            | OM UI: table metadata, lineage tab, classification/tags                 |
| **AI skeptic**           | Prompt injection, hallucinated tools, data leakage | Malicious-ish queries from seed, inspect redaction / allowlist          |

## Moment 1 — “This is not a wrapper”

**Audience:** All three.
**Action:** Open Swagger or README Mermaid — show **LangGraph** boundary + **MCP** allowlist + **structured error envelope**.
**Pass:** One sentence naming **two** concrete OM MCP tools used in the last request.

## Moment 2 — “OpenMetadata is the source of truth”

**Audience:** Governance lead + platform.
**Action:** Same entity in **chat** and **OM UI** — FQN matches; tags or summary align after refresh.
**Pass:** Judge copies FQN from UI into a second chat query and gets a consistent answer.

## Moment 3 — “Adversarial default”

**Audience:** AI skeptic (+ primary hackathon security story).
**Action:** Drive the **planted prompt-injection** path from [`seed/customer_db.json`](../../seed/customer_db.json) per [Demo/Narrative.md §Scene 3](../Demo/Narrative.md).
**Pass:** E2E or live demo shows **sanitized** rendering + **no** execution of hidden instructions; CI **`tests/security/test_prompt_injection.py`** referenced as backstop.

## Anti-patterns (do not do these on camera)

- Reading API keys or JWTs from screen.
- `dangerouslySetInnerHTML` or raw HTML from model output.
- Claiming “we use all 12 tools” without a **named** list or audit reference ([DataFindings/ExistingMCPAudit.md](../DataFindings/ExistingMCPAudit.md)).
- Apologizing for local-only demo without showing **why** (ThreatModel v1 loopback binding).

## Post–governance engine (P2-19+)

Add **Moment 4** (optional, 20 s): open OM entity **custom properties** — show `governance_state` (or agreed key) written by the agent after approval or drift ([GovernanceEngine.md](../FeatureDev/GovernanceEngine.md)).
