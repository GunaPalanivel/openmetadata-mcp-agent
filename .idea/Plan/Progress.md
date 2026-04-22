# Progress Tracker

Per-person, per-phase progress on every task in [TaskSync.md](./TaskSync.md). One row per task. Use this file to coordinate day to day.

## How to use this file

1. Pick the next task in the "Order of execution" list for your phase.
2. Open a GitHub issue for that task in `GunaPalanivel/openmetadata-mcp-agent` using the right template (`task`, `feature`, or `bug`). Title format: `[<TASK-ID>] <short description>` (for example, `[P1-03] MCP client: search_metadata happy path`).
3. Assign the issue to yourself. Paste the issue number into the `Issue` column below.
4. Create a branch: `<type>/<task-id>-<short-slug>` (for example, `feat/p1-03-mcp-client-search`).
5. Walk the lifecycle and tick the boxes as you go. Do not check `Merged` until the PR is squashed and merged into `main`.

## Reviewer routing (automatic)

PRs get a reviewer requested for you by `.github/workflows/auto-assign-reviewer.yml`:

| Author                                                   | Reviewer requested |
| -------------------------------------------------------- | ------------------ |
| @PriyankaSen0902, @aravindsai003, @5009226-bhawikakumari | @GunaPalanivel     |
| @GunaPalanivel                                           | @PriyankaSen0902   |
| Outside contributor (forks, community)                   | @PriyankaSen0902   |

Backup: `.github/CODEOWNERS` requests @GunaPalanivel by default if the workflow is disabled.

## Lifecycle checklist (one row per task)

Each row uses the same 8-step lifecycle. Check the boxes inline:

```
[P] Plan  [B] Build  [V1] Validate  [F] Fix  [V2] Validate  [PR] PR opened  [R] Reviewed  [M] Merged
```

## Status legend

| Symbol | Meaning                              |
| ------ | ------------------------------------ |
| `[ ]`  | Not started                          |
| `[/]`  | In progress                          |
| `[x]`  | Done                                 |
| `[!]`  | Blocked (add a note next to the row) |

---

## Phase 0 — Claim and Setup (Day 3, April 19) ✅ COMPLETE

### @GunaPalanivel

| Task ID | Description                                                         | Issue                                                                                                | PR    | P   | B   | V1  | F   | V2  | PR opened | R   | M   |
| ------- | ------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------- | ----- | --- | --- | --- | --- | --- | --------- | --- | --- |
| P0-01   | Post intent comment on upstream #26645                              | [#26645 comment](https://github.com/open-metadata/OpenMetadata/issues/26645#issuecomment-4275961194) | n/a   | [x] | [x] | [x] | [x] | [x] | [x]       | [x] | [x] |
| P0-02   | Post intent comment on upstream #26608                              | [#26608 comment](https://github.com/open-metadata/OpenMetadata/issues/26608#issuecomment-4275961984) | n/a   | [x] | [x] | [x] | [x] | [x] | [x]       | [x] | [x] |
| P0-03   | Create repo `GunaPalanivel/openmetadata-mcp-agent`                  | done                                                                                                 | n/a   | [x] | [x] | [x] | [x] | [x] | [x]       | [x] | [x] |
| P0-04   | Redeem OpenAI API credits (deferred until P2-01)                    | n/a                                                                                                  | n/a   | [!] | [!] | [!] | [!] | [!] | [!]       | [!] | [!] |
| P0-05   | Generate OpenAI API key, save in `.env` (deferred with P0-04)       | n/a                                                                                                  | n/a   | [!] | [!] | [!] | [!] | [!] | [!]       | [!] | [!] |
| P0-06   | Add team as collaborators (3 invites)                               | done                                                                                                 | n/a   | [x] | [x] | [x] | [x] | [x] | [x]       | [x] | [x] |
| P0-07   | Drop `CLAUDE.md` template into repo root                            | done                                                                                                 | done  | [x] | [x] | [x] | [x] | [x] | [x]       | [x] | [x] |
| P0-08   | Star `open-metadata/OpenMetadata` (all 4)                           | done                                                                                                 | n/a   | [x] | [x] | [x] | [x] | [x] | [x]       | [x] | [x] |
| P0-09   | Read Discovery + NFRs + CodingStandards + PromptInjection           | done                                                                                                 | n/a   | [x] | [x] | [x] | [x] | [x] | [x]       | [x] | [x] |
| P0-10   | Install pre-commit hooks (`pre-commit install` + `run --all-files`) | n/a                                                                                                  | n/a   | [x] | [x] | [x] | [x] | [x] | [x]       | [x] | [x] |

### Per-person setup (every contributor)

| Owner                  | P0-10 Install pre-commit hooks |
| ---------------------- | ------------------------------ |
| @GunaPalanivel         | [x]                            |
| @PriyankaSen0902       | [x]                            |
| @aravindsai003         | [x]                            |
| @5009226-bhawikakumari | [x]                            |

---

## Phase 1 — Foundation (Day 3 to 4, April 19 to 20) ✅ COMPLETE

> All Phase 1 PRs merged. Upstream merge on April 22 brought #56, #57, #58.

### @GunaPalanivel

| Task ID | Description                                                   | Issue                                                                       | PR                                                                          | P   | B   | V1  | F   | V2  | PR opened | R   | M   |
| ------- | ------------------------------------------------------------- | --------------------------------------------------------------------------- | --------------------------------------------------------------------------- | --- | --- | --- | --- | --- | --------- | --- | --- |
| P1-01   | Init repo with `pyproject.toml` and Phase 1 deps              | [#14](https://github.com/GunaPalanivel/openmetadata-mcp-agent/issues/14)    | [#46](https://github.com/GunaPalanivel/openmetadata-mcp-agent/pull/46)      | [x] | [x] | [x] | [x] | [x] | [x]       | [x] | [x] |
| P1-02   | Create project structure (`src/copilot/...`, `ui/`, `tests/`) | [#15](https://github.com/GunaPalanivel/openmetadata-mcp-agent/issues/15)    | [#54](https://github.com/GunaPalanivel/openmetadata-mcp-agent/pull/54)      | [x] | [x] | [x] | [x] | [x] | [x]       | [x] | [x] |
| P1-03   | Implement MCP client `search_metadata` happy path             | [#16](https://github.com/GunaPalanivel/openmetadata-mcp-agent/issues/16)    | [#55](https://github.com/GunaPalanivel/openmetadata-mcp-agent/pull/55)      | [x] | [x] | [x] | [x] | [x] | [x]       | [x] | [x] |
| P1-04   | LangGraph agent skeleton (NL → intent → tool → respond)      | [#17](https://github.com/GunaPalanivel/openmetadata-mcp-agent/issues/17)    | [#55](https://github.com/GunaPalanivel/openmetadata-mcp-agent/pull/55)      | [x] | [x] | [x] | [x] | [x] | [x]       | [x] | [x] |
| P1-05   | Verify smoke: search returns data                             | [#18](https://github.com/GunaPalanivel/openmetadata-mcp-agent/issues/18)    | [#58](https://github.com/GunaPalanivel/openmetadata-mcp-agent/pull/58)      | [x] | [x] | [x] | [x] | [x] | [x]       | [x] | [x] |
| P1-06   | Review all Phase 1 PRs                                        | [#19](https://github.com/GunaPalanivel/openmetadata-mcp-agent/issues/19)    | n/a                                                                         | [x] | [x] | [x] | [x] | [x] | [x]       | [x] | [x] |

### @PriyankaSen0902

| Task ID | Description                                                     | Issue                                                                       | PR                                                                          | P   | B   | V1  | F   | V2  | PR opened | R   | M   |
| ------- | --------------------------------------------------------------- | --------------------------------------------------------------------------- | --------------------------------------------------------------------------- | --- | --- | --- | --- | --- | --------- | --- | --- |
| P1-07   | Study `data-ai-sdk` + `langchain-openai`, document tool schemas | [#20](https://github.com/GunaPalanivel/openmetadata-mcp-agent/issues/20)    | [#52](https://github.com/GunaPalanivel/openmetadata-mcp-agent/pull/52)      | [x] | [x] | [x] | [x] | [x] | [x]       | [x] | [x] |
| P1-08   | Map all 12 MCP tools to governance use cases (update audit doc) | [#21](https://github.com/GunaPalanivel/openmetadata-mcp-agent/issues/21)    | [#53](https://github.com/GunaPalanivel/openmetadata-mcp-agent/pull/53)      | [x] | [x] | [x] | [x] | [x] | [x]       | [x] | [x] |
| P1-09   | Typed wrapper for top 6 tools (Pydantic params + responses)     | [#22](https://github.com/GunaPalanivel/openmetadata-mcp-agent/issues/22)    | [#57](https://github.com/GunaPalanivel/openmetadata-mcp-agent/pull/57)      | [x] | [x] | [x] | [x] | [x] | [x]       | [x] | [x] |
| P1-10   | 10+ unit tests for MCP client wrapper (mock responses)          | [#23](https://github.com/GunaPalanivel/openmetadata-mcp-agent/issues/23)    | [#57](https://github.com/GunaPalanivel/openmetadata-mcp-agent/pull/57)      | [x] | [x] | [x] | [x] | [x] | [x]       | [x] | [x] |

### @aravindsai003

| Task ID | Description                                           | Issue                                                                       | PR                                                                          | P   | B   | V1  | F   | V2  | PR opened | R   | M   |
| ------- | ----------------------------------------------------- | --------------------------------------------------------------------------- | --------------------------------------------------------------------------- | --- | --- | --- | --- | --- | --------- | --- | --- |
| P1-11   | Local OM at `:8585` via Docker                        | [#24](https://github.com/GunaPalanivel/openmetadata-mcp-agent/issues/24)    | [#51](https://github.com/GunaPalanivel/openmetadata-mcp-agent/pull/51)      | [x] | [x] | [x] | [x] | [x] | [x]       | [x] | [x] |
| P1-12   | Generate Bot JWT, share privately                     | [#25](https://github.com/GunaPalanivel/openmetadata-mcp-agent/issues/25)    | n/a                                                                         | [x] | [x] | [x] | [x] | [x] | [x]       | [x] | [x] |
| P1-13   | Pre-seed OM with 52 realistic tables                  | [#26](https://github.com/GunaPalanivel/openmetadata-mcp-agent/issues/26)    | [#56](https://github.com/GunaPalanivel/openmetadata-mcp-agent/pull/56)      | [x] | [x] | [x] | [x] | [x] | [x]       | [x] | [x] |
| P1-14   | Confirm UI scaffold runs on `:3000`                   | [#27](https://github.com/GunaPalanivel/openmetadata-mcp-agent/issues/27)    | n/a                                                                         | [x] | [x] | [x] | [x] | [x] | [x]       | [x] | [x] |
| P1-15   | Document setup in `README.md` (clone to run in 5 min) | [#28](https://github.com/GunaPalanivel/openmetadata-mcp-agent/issues/28)    | n/a                                                                         | [x] | [x] | [x] | [x] | [x] | [x]       | [x] | [x] |

### @5009226-bhawikakumari

| Task ID | Description                                                | Issue                                                                       | PR                                                                          | P   | B   | V1  | F   | V2  | PR opened | R   | M   |
| ------- | ---------------------------------------------------------- | --------------------------------------------------------------------------- | --------------------------------------------------------------------------- | --- | --- | --- | --- | --- | --------- | --- | --- |
| P1-16   | Polish public README (1-liner, features, setup)            | [#29](https://github.com/GunaPalanivel/openmetadata-mcp-agent/issues/29)    | n/a                                                                         | [x] | [x] | [x] | [x] | [x] | [x]       | [x] | [x] |
| P1-17   | Daily monitor unassigned hackathon GFIs                    | [#30](https://github.com/GunaPalanivel/openmetadata-mcp-agent/issues/30)    | n/a                                                                         | [x] | [x] | [x] | [x] | [x] | [x]       | [x] | [x] |
| P1-18   | Add AI disclosure to `README.md`                           | [#31](https://github.com/GunaPalanivel/openmetadata-mcp-agent/issues/31)    | n/a                                                                         | [x] | [x] | [x] | [x] | [x] | [x]       | [x] | [x] |
| P1-19   | Draft demo narrative outline (refresh `Demo/Narrative.md`) | [#32](https://github.com/GunaPalanivel/openmetadata-mcp-agent/issues/32)    | n/a                                                                         | [x] | [x] | [x] | [x] | [x] | [x]       | [x] | [x] |
| P1-20   | Daily refresh `Demo/CompetitiveMatrix.md`                  | [#33](https://github.com/GunaPalanivel/openmetadata-mcp-agent/issues/33)    | n/a                                                                         | [x] | [x] | [x] | [x] | [x] | [x]       | [x] | [x] |

### Phase 1 Exit Gate ✅

- [x] MCP client connects and returns search results
- [x] Chat UI scaffold renders on localhost
- [x] `README.md` and `CLAUDE.md` present in repo
- [x] `POST /chat` wired to `run_chat_turn()` (PR #58)
- [x] Typed Pydantic wrappers for top 6 MCP tools (PR #57)
- [x] 52 seed tables loaded (PR #56)

---

## Phase 2 — Core Features + Governance Engine (Day 5 to 7, April 21 to 23)

**Order of execution (governance engine track):**

1. GOV-01 (GSA: governance state machine — foundation for everything) ← **START HERE**
2. GOV-02 (GSA: session manager + confirm wiring — HITL end-to-end)
3. GOV-03 (PSTL: drift detection — the "wow" demo moment)
4. GOV-04 (PSTL: similarity scoring — learning governance)
5. GOV-05 (ATL: causal impact — consequence-driven responses)
6. GOV-06 (ATL: epistemic humility — knowing when NOT to act)
7. GOV-07 (BSE: docs update — architecture diagrams, API docs, CHANGELOG)

**Original P2 tasks run in parallel** — see TaskSync.md for ordering.

### @GunaPalanivel — Governance Engine Core

| Task ID | Description                                                      | Issue                                                                       | PR    | P   | B   | V1  | F   | V2  | PR opened | R   | M   |
| ------- | ---------------------------------------------------------------- | --------------------------------------------------------------------------- | ----- | --- | --- | --- | --- | --- | --------- | --- | --- |
| P2-04   | FastAPI `POST /chat` wired to LangGraph agent                    | done (PR #58)                                                               | #58   | [x] | [x] | [x] | [x] | [x] | [x]       | [x] | [x] |
| GOV-01  | 🔴 Governance lifecycle state machine (FSM + records + store)    | [#60](https://github.com/GunaPalanivel/openmetadata-mcp-agent/issues/60)    |       | [ ] | [ ] | [ ] | [ ] | [ ] | [ ]       | [ ] | [ ] |
| GOV-02  | 🔴 Session manager + wire /chat/confirm + /chat/cancel           | [#61](https://github.com/GunaPalanivel/openmetadata-mcp-agent/issues/61)    |       | [ ] | [ ] | [ ] | [ ] | [ ] | [ ]       | [ ] | [ ] |
| P2-01   | Auto-classification flow (scan → classify → suggest → apply)    |                                                                             |       | [ ] | [ ] | [ ] | [ ] | [ ] | [ ]       | [ ] | [ ] |
| P2-02   | Lineage impact analysis report with Tier warnings                |                                                                             |       | [ ] | [ ] | [ ] | [ ] | [ ] | [ ]       | [ ] | [ ] |
| P2-03   | Multi-step agent: chain 3+ tool calls per turn                   |                                                                             |       | [ ] | [ ] | [ ] | [ ] | [ ] | [ ]       | [ ] | [ ] |
| P2-05   | Review all Phase 2 PRs (full PR-Review checklist)                |                                                                             | n/a   | [ ] | [ ] | [ ] | [ ] | [ ] | [ ]       | [ ] | [ ] |

### @PriyankaSen0902 — Drift + Similarity

| Task ID | Description                                                      | Issue                                                                       | PR    | P   | B   | V1  | F   | V2  | PR opened | R   | M   |
| ------- | ---------------------------------------------------------------- | --------------------------------------------------------------------------- | ----- | --- | --- | --- | --- | --- | --------- | --- | --- |
| P2-08   | Retry + circuit breaker + structured error envelope on MCP calls | done (Phase 1)                                                              | #55   | [x] | [x] | [x] | [x] | [x] | [x]       | [x] | [x] |
| P2-10b  | `services/prompt_safety.neutralize` + 5-pattern tests            | done (Phase 1)                                                              | #55   | [x] | [x] | [x] | [x] | [x] | [x]       | [x] | [x] |
| P2-11b  | `observability/redact.py` + `middleware/error_envelope.py`       | done (Phase 1)                                                              | #55   | [x] | [x] | [x] | [x] | [x] | [x]       | [x] | [x] |
| GOV-03  | Drift detection service + background scan                        | [#62](https://github.com/GunaPalanivel/openmetadata-mcp-agent/issues/62)    |       | [ ] | [ ] | [ ] | [ ] | [ ] | [ ]       | [ ] | [ ] |
| GOV-04  | Similarity scoring — learning from past approvals                | [#63](https://github.com/GunaPalanivel/openmetadata-mcp-agent/issues/63)    |       | [ ] | [ ] | [ ] | [ ] | [ ] | [ ]       | [ ] | [ ] |
| P2-06   | NL query engine: text → intent → tool → Markdown                 |                                                                             |       | [ ] | [ ] | [ ] | [ ] | [ ] | [ ]       | [ ] | [ ] |
| P2-07   | Governance summary: tag coverage %, PII %, unclassified count    |                                                                             |       | [ ] | [ ] | [ ] | [ ] | [ ] | [ ]       | [ ] | [ ] |
| P2-09   | Integration tests including circuit-breaker-open paths           |                                                                             |       | [ ] | [ ] | [ ] | [ ] | [ ] | [ ]       | [ ] | [ ] |

### @aravindsai003 — Impact + Humility + UI

| Task ID | Description                                                         | Issue                                                                       | PR    | P   | B   | V1  | F   | V2  | PR opened | R   | M   |
| ------- | ------------------------------------------------------------------- | --------------------------------------------------------------------------- | ----- | --- | --- | --- | --- | --- | --------- | --- | --- |
| P2-13b  | `seed/customer_db.json` (52 tables) + `scripts/load_seed.py`       | done (PR #56)                                                               | #56   | [x] | [x] | [x] | [x] | [x] | [x]       | [x] | [x] |
| GOV-05  | Causal impact analysis in format_response                           | [#64](https://github.com/GunaPalanivel/openmetadata-mcp-agent/issues/64)    |       | [ ] | [ ] | [ ] | [ ] | [ ] | [ ]       | [ ] | [ ] |
| GOV-06  | Epistemic humility — evidence gap handling                          | [#65](https://github.com/GunaPalanivel/openmetadata-mcp-agent/issues/65)    |       | [ ] | [ ] | [ ] | [ ] | [ ] | [ ]       | [ ] | [ ] |
| P2-10   | Connect React UI to FastAPI (real chat responses)                   |                                                                             |       | [ ] | [ ] | [ ] | [ ] | [ ] | [ ]       | [ ] | [ ] |
| P2-11   | Render structured responses (markdown + sanitize, no innerHTML)     |                                                                             |       | [ ] | [ ] | [ ] | [ ] | [ ] | [ ]       | [ ] | [ ] |
| P2-12   | HITL confirmation modal (tool name, risk, FQN list, Confirm/Cancel) |                                                                             |       | [ ] | [ ] | [ ] | [ ] | [ ] | [ ]       | [ ] | [ ] |
| P2-13   | E2E test including the prompt-injection demo flow                   |                                                                             |       | [ ] | [ ] | [ ] | [ ] | [ ] | [ ]       | [ ] | [ ] |

### @5009226-bhawikakumari — Docs + Governance Docs

| Task ID | Description                                                    | Issue                                                                       | PR       | P   | B   | V1  | F   | V2  | PR opened | R   | M   |
| ------- | -------------------------------------------------------------- | --------------------------------------------------------------------------- | -------- | --- | --- | --- | --- | --- | --------- | --- | --- |
| GOV-07  | Docs update: governance architecture + API + README + CHANGELOG | [#66](https://github.com/GunaPalanivel/openmetadata-mcp-agent/issues/66)    |          | [ ] | [ ] | [ ] | [ ] | [ ] | [ ]       | [ ] | [ ] |
| P2-14   | Claim + fix a GFI issue if an unassigned one appears           | upstream                                                                    | upstream | [ ] | [ ] | [ ] | [ ] | [ ] | [ ]       | [ ] | [ ] |
| P2-15   | README Mermaid architecture + trust-boundary diagram           |                                                                             |          | [ ] | [ ] | [ ] | [ ] | [ ] | [ ]       | [ ] | [ ] |
| P2-16   | Refresh `Demo/Narrative.md` with measurable outcomes           |                                                                             |          | [ ] | [ ] | [ ] | [ ] | [ ] | [ ]       | [ ] | [ ] |
| P2-17   | Document all 12 MCP tools used in README (cite audit)          |                                                                             |          | [ ] | [ ] | [ ] | [ ] | [ ] | [ ]       | [ ] | [ ] |
| P2-18   | Daily refresh `Demo/CompetitiveMatrix.md`                      |                                                                             | n/a      | [ ] | [ ] | [ ] | [ ] | [ ] | [ ]       | [ ] | [ ] |

### Phase 2 Exit Gate

- [x] `POST /chat` wired to `run_chat_turn()` (PR #58)
- [ ] `POST /chat/confirm` executes tools and transitions governance state (GOV-02)
- [ ] Governance FSM rejects invalid transitions (GOV-01)
- [ ] Drift detection identifies changes (GOV-03)
- [ ] 3 governance workflows working: NL query + auto-classify + lineage impact
- [ ] Chat UI shows real responses from agent
- [ ] HITL confirmation working
- [ ] 30+ tests passing including governance + security tests

---

## Phase 3 — Polish + Multi-MCP (Day 8 to 9, April 24 to 25)

> See TaskSync.md for full Phase 3 task list. Progress rows will be added when Phase 2 exits.

### Phase 3 Exit Gate

- [ ] Multi-MCP workflow demonstrated
- [ ] UI is OM-native quality (`#7147E8`, Inter, dark mode default)
- [ ] Final + backup demo videos recorded; both play cleanly
- [ ] README clone-to-run < 5 min on the backup machine
- [ ] All tests green, >70% coverage on `src/copilot/`
- [ ] `Validation/QualityGates.md` Gates 0, 1, 2, 3, 4, 5 green

---

## Phase 4 — Submit (Day 10, April 26)

> See TaskSync.md for full Phase 4 task list. Progress rows will be added when Phase 3 exits.

---

## Snapshot per person (counts — updated April 22)

| Owner                  | Phase 0 | Phase 1 | Phase 2 (Track A) | Phase 2 (GOV) | Phase 3 | Phase 4 | Total |
| ---------------------- | ------- | ------- | ------------------ | -------------- | ------- | ------- | ----- |
| @GunaPalanivel         | 9 ✅    | 6 ✅    | 4                  | 2              | 5       | 6       | 32    |
| @PriyankaSen0902       | 0       | 4 ✅    | 3                  | 2              | 5       | 0       | 14    |
| @aravindsai003         | 0       | 5 ✅    | 4                  | 2              | 4       | 1       | 16    |
| @5009226-bhawikakumari | 0       | 5 ✅    | 4                  | 1              | 6       | 3       | 19    |

---

## Upstream Sync Log

| Date | Commits Pulled | Key Changes |
|------|----------------|-------------|
| April 22, 2026 | 3 (dbd81e3, acca5f4, aa5325e) | PR #56: 52 seed tables + load_seed.py, PR #57: Typed Pydantic wrappers for 6 MCP tools, PR #58: Smoke test + `POST /chat` wired to `run_chat_turn()` |
