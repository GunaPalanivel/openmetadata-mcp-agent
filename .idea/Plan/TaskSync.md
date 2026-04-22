# TaskSync — Master Task Tracker

> **Last updated**: April 22, 2026 (Day 6)
> **LLM Provider**: ✅ OpenAI GPT-4o-mini (free Codex credits)
> **Repo Strategy**: ✅ NEW standalone repo (`openmetadata-mcp-agent`) + fork for GFI only
> **Plan/ location**: ✅ `.idea/Plan/` stays local (agent command center)
> **All tasks ordered by priority. Check off as you complete them.**

---

## Phase 0 — Claim & Setup (COMPLETE ✅)

> All Phase 0 tasks completed April 19, 2026.

### OMH-GSA (@GunaPalanivel) — CRITICAL

- [x] `P0-01` 🔴 Post intent comment on [#26645](https://github.com/open-metadata/OpenMetadata/issues/26645)
- [x] `P0-02` 🔴 Post intent comment on [#26608](https://github.com/open-metadata/OpenMetadata/issues/26608)
- [x] `P0-03` Create NEW repo: `GunaPalanivel/openmetadata-mcp-agent` on GitHub (public, Apache 2.0)
- [!] `P0-04` Redeem OpenAI API credits at platform.openai.com/promotions (deferred)
- [!] `P0-05` Generate OpenAI API key, save in `.env` (deferred with P0-04)
- [x] `P0-06` Add all team as collaborators
- [x] `P0-07` Drop the `CLAUDE.md` template into the new repo root
- [x] `P0-08` Star [open-metadata/OpenMetadata](https://github.com/open-metadata/OpenMetadata)
- [x] `P0-09` Read Discovery + NFRs + CodingStandards + PromptInjection docs
- [x] `P0-10` Pre-commit hooks installed and running

---

## Phase 1 — Foundation (COMPLETE ✅)

> All Phase 1 tasks completed. Merged PRs: #46, #47, #51, #52, #53, #54, #55, #56, #57, #58.

### OMH-GSA (@GunaPalanivel) — Architect

- [x] `P1-01` Init `openmetadata-mcp-agent` repo with `pyproject.toml` (#14 → PR #46)
- [x] `P1-02` Create project structure (#15 → PR #54)
- [x] `P1-03` Implement MCP client: `search_metadata` + `call_tool` + `list_tools` (#16 → PR #55)
- [x] `P1-04` LangGraph 6-node agent skeleton (#17 → PR #55)
- [x] `P1-05` Verify smoke: search returns data from local OM (#18 → PR #58)
- [x] `P1-06` Review all Phase 1 PRs (#19)

### OMH-PSTL (@PriyankaSen0902) — Senior Builder

- [x] `P1-07` Study `data-ai-sdk` + `langchain-openai` docs — document tool schemas (#20 → PR #52)
- [x] `P1-08` Map all 12 MCP tools to governance use cases (#21 → PR #53)
- [x] `P1-09` Typed wrapper for top 6 tools (Pydantic params + responses) (#22 → PR #57)
- [x] `P1-10` 10+ unit tests for MCP client wrapper (#23 → PR #57)

### OMH-ATL (@aravindsai003) — Builder

- [x] `P1-11` Docker: local OM running at `:8585` (#24 → PR #51)
- [x] `P1-12` Generate Bot JWT (#25)
- [x] `P1-13` Pre-seed OM with 52 realistic tables (#26 → PR #56)
- [x] `P1-14` Confirm UI scaffold runs on `:3000` (#27)
- [x] `P1-15` Document setup in `README.md` (#28)

### OMH-BSE (@5009226-bhawikakumari) — Delivery

- [x] `P1-16` Polish public README (#29)
- [x] `P1-17` Daily monitor: unassigned hackathon GFIs (#30)
- [x] `P1-18` Add AI disclosure to README (#31)
- [x] `P1-19` Draft demo narrative outline (#32)
- [x] `P1-20` Daily refresh `Demo/CompetitiveMatrix.md` (#33)

### Phase 1 Exit Gate ✅

- [x] MCP client connects and returns search results
- [x] Chat UI scaffold renders on localhost
- [x] README + CLAUDE.md present in new repo
- [x] `POST /chat` wired to `run_chat_turn()` (PR #58)
- [x] Typed Pydantic wrappers for top 6 MCP tools (PR #57)
- [x] 52 seed tables in `seed/customer_db.json` (PR #56)

---

## Phase 2 — Core Features + Governance Engine (Day 6–7: April 22–23)

> **Strategy**: Lead with GOVERNANCE, not search. The governance engine is the biggest differentiator.
>
> **Phase 2 is split into two tracks:**
> - **Track A**: Original P2 tasks (auto-classify, lineage impact, UI wiring, NL query)
> - **Track B**: Governance engine upgrades (GOV-01 through GOV-07) — see [FeatureDev/GovernanceEngine.md](./FeatureDev/GovernanceEngine.md)

### Track A — Original Core Features

#### OMH-GSA (@GunaPalanivel)

- [x] `P2-04` FastAPI `POST /chat` wired to LangGraph agent ← **DONE in PR #58**
- [ ] `P2-01` **Auto-classification flow**: scan → GPT classify → suggest PII tags → user confirms → `patch_entity`
- [ ] `P2-02` **Lineage impact analysis**: NL query → `get_entity_lineage` → human-readable report
- [ ] `P2-03` Multi-step agent: chain 3+ tool calls per turn
- [ ] `P2-05` Review all Phase 2 PRs

#### OMH-PSTL (@PriyankaSen0902)

- [ ] `P2-06` **NL query engine**: text → intent → tool → Markdown response
- [ ] `P2-07` **Governance summary**: tag coverage %, PII exposure %, unclassified count
- [x] `P2-08` Retry + circuit breaker + structured error envelope on MCP calls ← **DONE in PR #55**
- [ ] `P2-09` Integration tests including circuit-breaker-open paths
- [x] `P2-10b` `services/prompt_safety.neutralize()` + 5-pattern tests ← **DONE in Phase 1 scaffold**
- [x] `P2-11b` `observability/redact.py` + `middleware/error_envelope.py` ← **DONE in Phase 1 scaffold**

#### OMH-ATL (@aravindsai003)

- [ ] `P2-10` Connect React UI to FastAPI (real chat responses)
- [ ] `P2-11` Render structured responses (markdown + sanitize)
- [ ] `P2-12` HITL confirmation modal
- [ ] `P2-13` E2E test including prompt-injection demo
- [x] `P2-13b` `seed/customer_db.json` (52 tables) + `scripts/load_seed.py` ← **DONE in PR #56**

#### OMH-BSE (@5009226-bhawikakumari)

- [ ] `P2-14` Claim + fix a GFI issue
- [ ] `P2-15` README Mermaid architecture diagram
- [ ] `P2-16` Refresh demo narrative
- [ ] `P2-17` Document all 12 MCP tools in README
- [ ] `P2-18` Daily refresh `Demo/CompetitiveMatrix.md`

### Track B — Governance Engine Upgrades 🔴

> **These are the upgrades that take the score from 42 → 58–60/60.**
> Full spec: [FeatureDev/GovernanceEngine.md](./FeatureDev/GovernanceEngine.md)

#### OMH-GSA (@GunaPalanivel) — GOV-01 + GOV-02

- [ ] `GOV-01` 🔴 **Governance lifecycle state machine** — FSM with 7 states, EntityGovernanceRecord, in-memory store ([#60](https://github.com/GunaPalanivel/openmetadata-mcp-agent/issues/60))
- [ ] `GOV-02` 🔴 **Session manager + wire /chat/confirm** — proposal store, confirm/cancel endpoints ([#61](https://github.com/GunaPalanivel/openmetadata-mcp-agent/issues/61))

#### OMH-PSTL (@PriyankaSen0902) — GOV-03 + GOV-04

- [ ] `GOV-03` **Drift detection service** — lineage hashing, tag verification, background task ([#62](https://github.com/GunaPalanivel/openmetadata-mcp-agent/issues/62))
- [ ] `GOV-04` **Similarity scoring** — learning from approvals, auto-approve at 0.85 ([#63](https://github.com/GunaPalanivel/openmetadata-mcp-agent/issues/63))

#### OMH-ATL (@aravindsai003) — GOV-05 + GOV-06

- [ ] `GOV-05` **Causal impact in format_response** — downstream asset counting, Tier-1 awareness ([#64](https://github.com/GunaPalanivel/openmetadata-mcp-agent/issues/64))
- [ ] `GOV-06` **Epistemic humility** — evidence gap detection, suggest glossary creation ([#65](https://github.com/GunaPalanivel/openmetadata-mcp-agent/issues/65))

#### OMH-BSE (@5009226-bhawikakumari) — GOV-07

- [ ] `GOV-07` **Docs update** — README governance diagram, API docs, CHANGELOG, plan updates ([#66](https://github.com/GunaPalanivel/openmetadata-mcp-agent/issues/66))

### Phase 2 Exit Gate

- [ ] `POST /chat` returns real agent responses ✅ (already done)
- [ ] `POST /chat/confirm` executes tools and transitions governance state
- [ ] Governance FSM rejects invalid transitions
- [ ] Drift detection identifies tag removal and lineage changes
- [ ] 3 governance workflows working: NL query + auto-classify + lineage impact
- [ ] Chat UI shows real responses from agent
- [ ] Human-in-the-loop confirmation working
- [ ] 30+ tests passing including governance + security tests
- [ ] [Validation/QualityGates.md](./Validation/QualityGates.md) Gates 0, 1, 2, 3 green

---

## Phase 3 — Polish + Multi-MCP (Day 8–9: April 24–25)

> **Strategy**: Multi-MCP is our INNOVATION differentiator. Polish UI to OM-native quality.

### OMH-GSA (@GunaPalanivel)

- [ ] `P3-01` **Multi-MCP**: connect GitHub MCP server via `langchain-mcp-adapters`
- [ ] `P3-02` Cross-MCP workflow: "find PII tables → create GitHub issue for each"
- [ ] `P3-03` Governance summary with aggregation: tag coverage %, tier distribution
- [ ] `P3-04` Security audit: no secrets in code, no debug logs, input validation
- [ ] `P3-05` Review all Phase 3 PRs

### OMH-PSTL (@PriyankaSen0902)

- [ ] `P3-06` Edge cases: empty results, auth failure, timeout — all structured error envelope
- [ ] `P3-07` `structlog` + redaction + `request_id`; zero `print()` calls
- [ ] `P3-08` Coverage report: target >70% on `src/copilot/`
- [ ] `P3-09` Full hardened CI per [Security/CIHardening.md](./Security/CIHardening.md)
- [ ] `P3-09b` `/metrics` endpoint with 4 Golden Signals

### OMH-ATL (@aravindsai003)

- [ ] `P3-10` **OM-native UI**: #7147E8 purple, Inter font, dark mode default
- [ ] `P3-11` Governance dashboard view: tag coverage chart, PII summary cards
- [ ] `P3-12` Responsive layout
- [ ] `P3-13` Loading animation + error states polished

### OMH-BSE (@5009226-bhawikakumari)

- [ ] `P3-14` Run 3-rehearsal protocol
- [ ] `P3-15` Record final demo video (2–3 min)
- [ ] `P3-16` Record + verify backup recording
- [ ] `P3-17` README finalized: GIF, 3-cmd setup, features, AI disclosure
- [ ] `P3-18` Verify clone → run on clean machine
- [ ] `P3-19` Architecture + trust-boundary Mermaid in README

### Phase 3 Exit Gate

- [ ] Multi-MCP workflow demonstrated
- [ ] UI is OM-native quality
- [ ] Final + backup demo videos recorded
- [ ] README clone → run < 5 min
- [ ] All tests green, >70% coverage
- [ ] Quality Gates 0–5 green

---

## Phase 4 — Submit (Day 10: April 26)

### All Team

- [ ] `P4-00` 🔴 Run PRR checklist end-to-end (OMH-GSA)
- [ ] `P4-01` Final README review (OMH-BSE)
- [ ] `P4-02` Repo hygiene + `gitleaks detect` returns 0 (OMH-GSA)
- [ ] `P4-03` AI disclosure confirmed (OMH-BSE)
- [ ] `P4-03b` Security audit report (OMH-GSA)
- [ ] `P4-03c` Demo machine pre-conditions (OMH-ATL)
- [ ] `P4-04` Submit hackathon form on WeMakeDevs (OMH-GSA)
- [ ] `P4-05` Link demo video + repo (OMH-GSA)
- [ ] `P4-06` Verify GFI PR status (OMH-BSE)
- [ ] `P4-07` Comment submission link on #26645 + #26608 (OMH-GSA)
- [ ] `P4-08` Team retrospective within 48h (all)

---

## ⚖️ Scoring Checklist (Run Before P4-04)

| Criterion                | Check                                                                                         | Target | Governance Engine Δ |
| ------------------------ | --------------------------------------------------------------------------------------------- | ------ | -------------------- |
| Potential Impact         | Demo shows governance automation with FSM lifecycle, drift detection, causal impact            | 10/10  | +1 (from 9) |
| Creativity & Innovation  | Multi-MCP + LLM classification + similarity scoring + epistemic humility                      | 10/10  | +1 (from 9) |
| Technical Excellence     | Tests pass, FSM-enforced transitions, circuit breakers, structured logging                    | 9/10   | +1 (from 8) |
| Best Use of OpenMetadata | All 12 MCP tools + governance state stored IN OM via `patch_entity` custom properties         | 10/10  | +0 (already 10) |
| User Experience          | OM-native UI, HITL with governance states, drift alerts, similarity-based reasoning           | 9/10   | +1 (from 8) |
| Presentation Quality     | README with governance FSM diagram, Mermaid trust boundary, <3 min demo                      | 9/10   | +1 (from 8) |
| **Total**                |                                                                                               | **57/60** | **+5 (from 52)** |

---

## Task Status Legend

| Symbol | Meaning             |
| ------ | ------------------- |
| `[ ]`  | Not started         |
| `[/]`  | In progress         |
| `[x]`  | Completed           |
| `[!]`  | Blocked             |
| 🔴     | Critical — do TODAY |
