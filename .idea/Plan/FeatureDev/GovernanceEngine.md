# Governance Engine — Technical Specification

> **Status**: Plan-only contract. Implementation follows [CLAUDE.md](../../../CLAUDE.md) layer rules (API → services → clients).
> **Replaces for execution**: Informal `P0`–`P6` labels in [Task.md](../../../Task.md) — use **TaskSync `P2-19`…`P2-26`** below.
> **GitHub issues**: Every engineering issue body **must** follow [PR-Review/EngineeringIssueTemplate.md](../PR-Review/EngineeringIssueTemplate.md) (Context → What to do → Done when → Depends on → Unblocks → Acceptance criteria → References).

## Why this exists

Differentiates the project from a “search chatbot”: **per-entity governance lifecycle**, **human-in-the-loop writes**, **catalog write-back** via OpenMetadata APIs, and **drift** when reality diverges from an approved baseline. Aligns with hackathon criteria **Best Use of OpenMetadata** and **Potential Impact**.

## Canonical task ID map (Task.md → TaskSync)

| Legacy (Task.md)    | TaskSync ID | One-line scope                                                                                                                                                |
| ------------------- | ----------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| P0                  | **P2-19**   | In-memory pending proposals by `session_id`; wire `POST /chat/confirm` and `POST /chat/cancel` through **services** (not direct `om_mcp` from `api/`).        |
| P1                  | **P2-20**   | `GovernanceState` enum + `ALLOWED_TRANSITIONS` + `governance_store` (`EntityGovernanceRecord` keyed by entity FQN).                                           |
| —                   | **P2-21**   | Integrate store into LangGraph nodes: `validate_proposal`, `hitl_gate`, and confirm path (transitions: scanned, suggested, approved).                         |
| P2                  | **P2-22**   | Persist selected states to OM via `patch_entity` / extension properties (async fire-and-forget with structured logging).                                      |
| P3 (service)        | **P2-23**   | `drift.py`: compare lineage hash + approved tags vs live `get_entity_lineage` / `get_entity_details`.                                                         |
| P3 (API + lifespan) | **P2-24**   | Background drift poll in FastAPI lifespan; **`GET /api/v1/governance/drift`** per [APIContract.md §Planned endpoints](../Architecture/APIContract.md).        |
| P4                  | **P2-25**   | `similarity.py`: weighted signals; optional “opinionated” line in `format_response` context when score > threshold.                                           |
| P5 + P6             | **P2-26**   | Causal / downstream impact in `format_response` for classify; `evidence_gap` on `AgentState` when no proposals — single PR acceptable, timebox humility copy. |

## Merge order (dependencies)

1. **P2-19** before **P2-01** (auto-classify): writes must not execute without working confirm/cancel + pending store.
2. **P2-20** before **P2-21** (store before agent hooks).
3. **P2-21** before **P2-22** (valid transitions before OM persistence).
4. **P2-22** optional but recommended before **P2-23** (persist baseline hash/tags for drift).
5. **P2-23** before **P2-24** (signals before exposing HTTP).
6. **P2-25** / **P2-26** can follow core HITL; timebox **P2-26** humility path if schedule slips.

## `GovernanceState` (contract)

```python
from enum import StrEnum

class GovernanceState(StrEnum):
    UNKNOWN = "unknown"
    SCANNED = "scanned"
    SUGGESTED = "suggested"
    APPROVED = "approved"
    ENFORCED = "enforced"
    DRIFT_DETECTED = "drift_detected"
    REMEDIATED = "remediated"

ALLOWED_TRANSITIONS: dict[GovernanceState, frozenset[GovernanceState]] = {
    GovernanceState.UNKNOWN: frozenset({GovernanceState.SCANNED}),
    GovernanceState.SCANNED: frozenset({GovernanceState.SUGGESTED, GovernanceState.UNKNOWN}),
    GovernanceState.SUGGESTED: frozenset({GovernanceState.APPROVED, GovernanceState.SCANNED}),
    GovernanceState.APPROVED: frozenset({GovernanceState.ENFORCED, GovernanceState.DRIFT_DETECTED}),
    GovernanceState.ENFORCED: frozenset({GovernanceState.DRIFT_DETECTED}),
    GovernanceState.DRIFT_DETECTED: frozenset({GovernanceState.REMEDIATED, GovernanceState.SUGGESTED}),
    GovernanceState.REMEDIATED: frozenset({GovernanceState.ENFORCED}),
}
```

`governance_store.transition(fqn, new_state, evidence)` raises on illegal transitions; `get_or_create(fqn)` seeds `UNKNOWN`.

## Session proposals (P2-19)

- **Store**: `Dict[str, PendingSession]` or `Dict[UUID, ...]` keyed by `session_id` string; value holds `pending: ToolCallProposal | None`, `expires_at`.
- **`POST /chat/confirm`**: Service loads proposal by `(session_id, proposal_id)`; if `accepted`, call `om_mcp` / tool executor with allowlist + breaker; update governance store → `APPROVED`; clear pending. If rejected, clear pending and return cancellation copy per [APIContract.md](../Architecture/APIContract.md).
- **`POST /chat/cancel`**: Clear session pending + any ephemeral LangGraph checkpoint if introduced later.
- **Errors**: `proposal_not_found`, `confirmation_expired` — already in contract.

## OM write-back (P2-22)

- On transition to **`APPROVED`** or **`DRIFT_DETECTED`**, enqueue async task to patch entity custom/extension fields (exact OM JSON Patch shape TBD against server version; use MCP `patch_entity` with validated args).
- Suggested property keys (string values): `governance_state`, `governance_lineage_snapshot_hash`, `governance_approved_tags_json` (or equivalent).
- **References**: [OpenMetadata REST / metadata APIs](https://docs.open-metadata.org/) — verify field names against deployed OM 1.6.x.

## Drift (P2-23 / P2-24)

- **Signals** (non-exhaustive): lineage structure/hash change vs stored snapshot; approved tags missing from live entity.
- **Poll interval**: configurable (e.g. 10 minutes), NFR-aligned timeouts on each MCP call.
- **Endpoint**: `GET /api/v1/governance/drift` returns list of FQNs (and optional signal detail) for entities in `DRIFT_DETECTED`.

## Similarity (P2-25)

- **Inputs**: candidate table FQN; corpus of prior approved entities from `governance_store`.
- **Signals** (example weights, tune in implementation): column name overlap **0.5**; lineage Jaccard upstream overlap **0.3**; glossary term co-occurrence **0.2**.
- **Output**: score in `[0,1]`; if **> 0.85**, add short “opinionated” clause to LLM context in `format_response` (still subject to HITL for writes).

## Causal impact + epistemic humility (P2-26)

**Causal:** When `intent == "classify"` (or lineage-heavy flows), compute downstream counts / Tier-1 exposure from `get_entity_lineage` (truncated, redacted per `prompt_safety`). Append structured bullet block to model context so the assistant explains **what breaks if untagged**.

**Humility:** Add optional `evidence_gap: bool` on `AgentState` (see [DataModel.md](../Architecture/DataModel.md)). Set when `intent == "classify"` and `tool_proposals` is empty after validation. `format_response` instructs the model to state missing glossary/terms or insufficient catalog signal — no fabricated tags.

## Sixteen-issue GitHub budget (repo work)

| #   | Title                                       | Scope                                                                                                                                                  | Primary owner |
| --- | ------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------ | ------------- |
| 1   | [BE] Session store + confirm/cancel         | P2-19                                                                                                                                                  | GSA           |
| 2   | [BE] GovernanceState FSM + governance_store | P2-20                                                                                                                                                  | GSA           |
| 3   | [BE] Agent hooks + OM write-back            | P2-21, P2-22                                                                                                                                           | GSA / PSTL    |
| 4   | [BE] Drift service + poll + GET drift       | P2-23, P2-24                                                                                                                                           | GSA           |
| 5   | [BE] Agent UX hardening                     | P2-25, P2-26                                                                                                                                           | PSTL          |
| 6   | [BE] Auto-classification flow               | P2-01                                                                                                                                                  | GSA           |
| 7   | [BE] Lineage impact analysis                | P2-02                                                                                                                                                  | PSTL          |
| 8   | [BE] NL query engine                        | P2-06                                                                                                                                                  | PSTL          |
| 9   | [FE] React UI → FastAPI                     | P2-10                                                                                                                                                  | ATL           |
| 10  | [FE] HITL confirmation modal                | P2-12                                                                                                                                                  | ATL           |
| 11  | [FE] OM-native UI + governance dashboard    | P3-10, P3-11                                                                                                                                           | ATL           |
| 12  | [Multi-MCP] GitHub MCP + cross workflow     | P3-01, P3-02                                                                                                                                           | GSA           |
| 13  | [Test] Integration + security gates         | P2-09, P2-10b, P3-08                                                                                                                                   | PSTL          |
| 14  | [CI] Close gaps vs CIHardening              | P3-09 (repo already has [.github/workflows/ci.yml](../../../.github/workflows/ci.yml) — diff vs [Security/CIHardening.md](../Security/CIHardening.md)) | BSE           |
| 15  | [Demo] Seed + rehearsal + video             | P2-13b, P3-14–P3-16 (automation/scripts only — not prose)                                                                                              | BSE           |
| 16  | [E2E] Playwright — chat + HITL + Moment 3   | P2-13 + [JudgePersona.md §Moment 3](../Project/JudgePersona.md); UI + API against local stack                                                          | ATL / PSTL    |

**Docs / README / submission** (P3-17, P3-19, P4-04, P4-05) are **outside** the 16-issue engineering count — track in [TaskSync.md](../TaskSync.md) Phase 3–4.

## Upstream contribution track (parallel, not counted in 16)

- **Hackathon repo** (`openmetadata-mcp-agent`): full agent, judges run here.
- **Upstream-ready**: at least one **small, reviewable** PR to `open-metadata/OpenMetadata` (GFI or docs) from the team fork per [DataFindings/GoodFirstIssues.md](../DataFindings/GoodFirstIssues.md) — see [Project/PRD.md §Upstream contribution vs hackathon deliverable](../Project/PRD.md). The agent codebase does **not** merge wholesale into OM core.

## Judge validation script (post-implementation)

1. Load seed OM; open UI; run classify intent; receive `pending_confirmation`.
2. **Approve** → verify `patch_entity` success in audit log **and** custom property visible on entity in OM UI.
3. Manually remove a tag or alter lineage in OM; wait for drift poll **or** trigger manual drift check if exposed for demo.
4. Call **`GET /api/v1/governance/drift`** → entity listed with `DRIFT_DETECTED`.
5. Reject path: new proposal → reject → no write; session clear on cancel.

## Related documents

- [Architecture/APIContract.md](../Architecture/APIContract.md) — chat + planned drift route
- [Architecture/DataModel.md](../Architecture/DataModel.md) — `EntityGovernanceRecord`, `AgentState` extensions
- [Architecture/AgentPipeline.md](../Architecture/AgentPipeline.md) — node + FSM diagram
- [Demo/Narrative.md](../Demo/Narrative.md) — scripted demo
- [Project/JudgePersona.md](../Project/JudgePersona.md) — judge moments
