# Demo Narrative — Three Scenes

> **Owner**: OMH-BSE (refresh with measurable outcomes from [Project/PRD.md](../Project/PRD.md)).
> **Runtime**: ~2–3 minutes live; align with [FeatureDev/GovernanceEngine.md](../FeatureDev/GovernanceEngine.md) once HITL + drift ship.

## Preconditions

- OpenMetadata 1.6.x running (local Docker per [Validation/SetupGuide.md](../Validation/SetupGuide.md)).
- Seed loaded: [`seed/customer_db.json`](../../seed/customer_db.json) + search reindex per [Demo/FailureRecovery.md](./FailureRecovery.md).
- Agent: `uvicorn copilot.api.main:app` on `127.0.0.1`; UI on `http://127.0.0.1:3000` when wired (P2-10).

## Scene 1 — Governance opener (auto-classify + HITL)

**Goal (judge-visible):** NL request → agent proposes **real** `patch_entity` writes → UI shows **pending_confirmation** with FQNs and risk badge.

| Step | Action                                                          | Success signal                                                              |
| ---- | --------------------------------------------------------------- | --------------------------------------------------------------------------- |
| 1    | In chat: “Scan `customer_db` for PII columns and suggest tags.” | Response lists tables/columns with suggested tags (Markdown table OK).      |
| 2    | If write flow: open confirmation modal (P2-12).                 | `proposal_id`, `risk_level: hard_write`, entity FQNs visible.               |
| 3    | Click **Confirm**.                                              | `200` from `POST /api/v1/chat/confirm`; audit shows `patch_entity` success. |

**Measurable:** proposal (and post-confirm write-back) includes all 3 seed spot-check columns on `sample_mysql.default.customer_db.customers`:
- `sample_mysql.default.customer_db.customers.email`
- `sample_mysql.default.customer_db.customers.phone`
- `sample_mysql.default.customer_db.customers.ssn`

## Scene 2 — Lineage impact (Tier story)

**Goal:** Prove **downstream / Tier-1** language, not generic lineage dump.

| Step | Action                                                          | Success signal                                                    |
| ---- | --------------------------------------------------------------- | ----------------------------------------------------------------- |
| 1    | Ask: “What depends on `<Tier1 table FQN>` if we drop PII tags?” | Response cites upstream/downstream counts or named Tier-1 assets. |
| 2    | (Optional) Open OM lineage graph for same FQN.                  | Narration matches OM graph within one hop tolerance.              |

**Measurable:** Response mentions **at least two** downstream FQNs or a clear “none in N hops” with method stated.

## Scene 3 — Trust + injection resistance

**Goal:** [Project/JudgePersona.md §Moment 3](../Project/JudgePersona.md) — planted prompt-injection in seed metadata does **not** become tool args or unsanitized HTML.

| Step | Action                                                                | Success signal                                                    |
| ---- | --------------------------------------------------------------------- | ----------------------------------------------------------------- |
| 1    | Query the table/column documented in seed as carrying injection bait. | UI renders plain text / sanitized Markdown only.                  |
| 2    | Inspect network or logs (redacted).                                   | No raw exfil string in LLM-bound tool args (see `prompt_safety`). |

**Measurable:** `tests/security/test_prompt_injection.py` green in CI (P2-10b).

## Timing budget

| Scene | Target duration |
| ----- | --------------- |
| 1     | 60–90 s         |
| 2     | 45–60 s         |
| 3     | 30–45 s         |

## Post-demo (catalog write-back — when P2-22 lands)

Add **15 s**: Open OM entity page → show custom property **`governance_state`** (or agreed key) set by agent after approve/drift.
