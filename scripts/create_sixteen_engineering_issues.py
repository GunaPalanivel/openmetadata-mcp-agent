#  Copyright 2026 Collate Inc.
#  Licensed under the Apache License, Version 2.0 (the "License"); you may
#  not use this file except in compliance with the License. You may obtain
#  a copy of the License at
#
#  http://www.apache.org/licenses/LICENSE-2.0
"""Create the 16 engineering GitHub issues for the sprint program.

Requires: gh CLI, logged in, repo GunaPalanivel/openmetadata-mcp-agent.

Run from repository root:
  python scripts/create_sixteen_engineering_issues.py

Idempotent-ish: always creates NEW issues. Close old duplicates separately.
"""

from __future__ import annotations

import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

REPO = "GunaPalanivel/openmetadata-mcp-agent"
ROOT = Path(__file__).resolve().parents[1]
_GH = shutil.which("gh")
if not _GH:
    raise SystemExit("gh CLI not found in PATH")


def gh(*args: str) -> str:
    argv = [_GH, *args, "--repo", REPO]
    r = subprocess.run(  # noqa: S603
        argv,
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=True,
    )
    return r.stdout.strip()


def make_issue(
    title: str,
    assignee: str,
    body: str,
) -> str:
    tmp = ROOT / ".issue_body_tmp.md"
    tmp.write_text(body, encoding="utf-8")
    try:
        url = gh(
            "issue", "create", "--title", title, "--body-file", str(tmp), "--assignee", assignee
        )
        return url
    finally:
        tmp.unlink(missing_ok=True)


def eng_tokens(s: str) -> str:
    """Replace ENG-03/16 style refs with <<N03>> placeholders (filled after issue creation)."""
    if s == "None":
        return s
    return re.sub(r"ENG-(\d+)/16", lambda m: f"<<N{int(m.group(1)):02d}>>", s)


def section_docs(files: list[str]) -> str:
    lines = "\n".join(f"- [ ] `{f}`" for f in files)
    return f"""## Plan docs to update (same PR as code - keep plan == reality)

{lines}

> Docs-only follow-ups (README GIF, submission form) stay in TaskSync Phase 3-4 and **do not** count toward the 16 engineering issues.
"""


def main() -> int:
    plan = ".idea/Plan"
    specs: list[tuple[str, str, str]] = []

    def T(
        title: str,
        assignee: str,
        context: str,
        steps: list[str],
        done: list[str],
        depends: str,
        unblocks: str,
        ac: list[str],
        docs: list[str],
        refs: list[str],
    ) -> tuple[str, str, str]:
        steps_b = "\n".join(f"{i}. {s}" for i, s in enumerate(steps, 1))
        done_b = "\n".join(f"- [ ] {d}" for d in done)
        ac_b = "\n".join(f"- [ ] {a}" for a in ac)
        refs_b = "\n".join(f"- `{r}`" for r in refs)
        body = f"""## Context

{context}

## What to do

{steps_b}

## Done when

{done_b}

## Depends on

{eng_tokens(depends)}

## Unblocks

{eng_tokens(unblocks)}

## Acceptance criteria

{ac_b}

{section_docs(docs)}

## References

{refs_b}
"""
        return title, assignee, body

    specs.append(
        T(
            "[ENG-01/16] Session store + wire /chat/confirm and /chat/cancel (P2-19)",
            "GunaPalanivel",
            "`POST /api/v1/chat/confirm` returns 501 today. Judges cannot approve writes. Implements in-memory pending proposals keyed by `session_id` per GovernanceEngine.",
            [
                "Add `src/copilot/services/sessions.py` (or equivalent) storing `ToolCallProposal` + TTL.",
                "Wire `post_chat_confirm` / `post_chat_cancel` in `src/copilot/api/chat.py` through services only (CLAUDE layer rules).",
                "On accept: execute allowlisted write via `om_mcp`; on reject: clear pending; match APIContract envelopes (410/422).",
                "Add `tests/unit/test_sessions.py` (or under `tests/unit/`) covering happy path + expiry + not found.",
            ],
            [
                "`POST /chat/confirm` returns 200 with audit when accepted; no `not_implemented` envelope.",
                "`POST /chat/cancel` clears pending session state.",
                "CI unit tests green.",
            ],
            "None",
            "ENG-02/16, ENG-03/16, ENG-06/16",
            [
                "**PRD**: HITL gate for writes / conversational governance loop.",
                "**APIContract**: `POST /chat/confirm` and `POST /chat/cancel` response shapes and error codes.",
                "**Tests**: new unit tests for session + confirm path (mock MCP).",
            ],
            [
                f"{plan}/Architecture/DataModel.md",
                f"{plan}/Architecture/APIContract.md",
                f"{plan}/FeatureDev/GovernanceEngine.md",
                f"{plan}/Progress.md",
            ],
            [
                f"{plan}/Project/PRD.md",
                f"{plan}/PR-Review/EngineeringIssueTemplate.md",
            ],
        )
    )

    specs.append(
        T(
            "[ENG-02/16] GovernanceState FSM + governance_store (P2-20)",
            "GunaPalanivel",
            "Per-entity governance lifecycle is the differentiator vs read-only chatbots.",
            [
                "Add `src/copilot/models/governance_state.py` with `GovernanceState` + `ALLOWED_TRANSITIONS`.",
                "Add `src/copilot/services/governance_store.py` with `get_or_create`, `transition` (raises on illegal).",
                "Unit tests for every illegal transition and happy paths.",
            ],
            [
                "FSM matches `.idea/Plan/FeatureDev/GovernanceEngine.md`.",
                "`pytest` tests for store pass.",
            ],
            "ENG-01/16",
            "ENG-03/16",
            [
                "**PRD**: governance automation / catalog-backed story.",
                "**DataModel**: `GovernanceState`, `EntityGovernanceRecord` sections match implementation.",
                "**Tests**: `tests/unit/test_governance_store.py` (or equivalent).",
            ],
            [
                f"{plan}/Architecture/DataModel.md",
                f"{plan}/Architecture/AgentPipeline.md",
                f"{plan}/FeatureDev/GovernanceEngine.md",
            ],
            [f"{plan}/Project/PRD.md", f"{plan}/Project/NFRs.md"],
        )
    )

    specs.append(
        T(
            "[ENG-03/16] Agent hooks + OM write-back (P2-21, P2-22)",
            "PriyankaSen0902",
            "Connect LangGraph nodes + confirm path to governance_store; persist key states to OM via `patch_entity`.",
            [
                "In `validate_proposal` / `hitl_gate` / confirm handler: call `governance_store` transitions (SCANNED, SUGGESTED, APPROVED).",
                "Async write-back on APPROVED / DRIFT_DETECTED using validated `patch_entity` args; extension property keys per GovernanceEngine.",
                "Integration-style tests with mocked MCP for write-back enqueue path.",
            ],
            [
                "OM UI or API shows custom governance properties after approve (manual verify checklist in PR).",
                "No direct `om_mcp` calls from `api/`.",
            ],
            "ENG-01/16, ENG-02/16",
            "ENG-04/16, ENG-06/16",
            [
                "**PRD**: Best Use of OpenMetadata - catalog reflects agent decisions.",
                "**APIContract**: write responses + audit fields consistent.",
                "**Tests**: mocked `patch_entity` invoked once per approved batch.",
            ],
            [
                f"{plan}/Architecture/DataFlow.md",
                f"{plan}/Architecture/Overview.md",
                f"{plan}/FeatureDev/GovernanceEngine.md",
            ],
            [f"{plan}/Project/PRD.md", f"{plan}/Architecture/APIContract.md"],
        )
    )

    specs.append(
        T(
            "[ENG-04/16] Drift service + lifespan poll + GET /governance/drift (P2-23, P2-24)",
            "GunaPalanivel",
            "Detect when live OM diverges from approved baseline; expose drift list for demo Moment.",
            [
                "Implement `src/copilot/services/drift.py` (hash + tag signals).",
                "FastAPI lifespan task + `GET /api/v1/governance/drift` route (move from planned to implemented in APIContract when shipped).",
                "Unit tests for drift pure logic; integration test with mocked MCP.",
            ],
            [
                "Drift worker runs without crashing when OM down (structured 503 on drift GET per contract).",
                "`GET /api/v1/governance/drift` returns JSON per APIContract.",
            ],
            "ENG-03/16",
            "ENG-16/16",
            [
                "**APIContract**: planned drift section matches implementation.",
                "**NFRs**: timeouts + breaker on MCP calls in drift loop.",
            ],
            [
                f"{plan}/Architecture/APIContract.md",
                f"{plan}/Architecture/DataFlow.md",
                f"{plan}/FeatureDev/GovernanceEngine.md",
            ],
            [f"{plan}/Project/NFRs.md", f"{plan}/Validation/TestStrategy.md"],
        )
    )

    specs.append(
        T(
            "[ENG-05/16] Agent UX hardening — similarity + causal + evidence_gap (P2-25, P2-26)",
            "PriyankaSen0902",
            "Opinionated governance assistant + causal impact + humility when evidence is missing.",
            [
                "Add `src/copilot/services/similarity.py` with weighted score; inject context in `format_response` when > threshold.",
                "Extend `format_response` for classify intent with causal downstream block (lineage read, redacted).",
                "Add `evidence_gap` to `AgentState` + `validate_proposal` path; format_response handles it.",
            ],
            [
                "Unit tests for similarity scoring and evidence_gap formatting branches.",
                "No extra OM calls without timeouts.",
            ],
            "ENG-03/16",
            "ENG-06/16",
            [
                "**PRD**: Creativity / impact story for judges.",
                "**Tests**: `tests/unit/` coverage for new pure functions.",
            ],
            [
                f"{plan}/Architecture/DataModel.md",
                f"{plan}/Architecture/AgentPipeline.md",
                f"{plan}/Validation/TestStrategy.md",
            ],
            [f"{plan}/Project/PRD.md", f"{plan}/Security/PromptInjectionMitigation.md"],
        )
    )

    specs.append(
        T(
            "[ENG-06/16] Auto-classification flow end-to-end (P2-01)",
            "GunaPalanivel",
            "Hackathon demo opener: scan → classify → HITL → patch.",
            [
                "Ensure classify intent chains search + details + proposals with Module G allowlist.",
                "Wire to sessions + governance transitions from prior issues.",
                "Document demo FQNs in Demo/Narrative if changed.",
            ],
            [
                "Happy path produces `pending_confirmation` for batch tag writes.",
                "Spot-check 3 PII columns against seed expectations.",
            ],
            "ENG-01/16, ENG-02/16, ENG-03/16",
            "ENG-16/16",
            [
                "**PRD**: auto-classify measurable outcomes.",
                "**Demo**: Narrative Scene 1 passes on local OM.",
            ],
            [
                f"{plan}/Demo/Narrative.md",
                f"{plan}/FeatureDev/AutoClassification.md",
                f"{plan}/TaskSync.md",
            ],
            [f"{plan}/Project/PRD.md", f"{plan}/Demo/FailureRecovery.md"],
        )
    )

    specs.append(
        T(
            "[ENG-07/16] Lineage impact analysis (P2-02)",
            "PriyankaSen0902",
            "Plain-English downstream / Tier-1 risk from `get_entity_lineage`.",
            [
                "Implement lineage summarization path in agent services.",
                "Tests with fixture lineage JSON (mock MCP).",
            ],
            [
                "Lineage intent returns human-readable report with Tier warnings.",
            ],
            "ENG-05/16",
            "ENG-16/16",
            [
                "**PRD**: Criterion Potential Impact / lineage story.",
            ],
            [
                f"{plan}/FeatureDev/LineageImpact.md",
                f"{plan}/Architecture/DataFlow.md",
            ],
            [f"{plan}/Project/PRD.md"],
        )
    )

    specs.append(
        T(
            "[ENG-08/16] NL query engine (P2-06)",
            "PriyankaSen0902",
            "NL → intent → single best tool → structured Markdown.",
            [
                "Harden intent routing and tool selection for search/details/lineage queries.",
                "Add/extend unit tests for routing matrix.",
            ],
            [
                "Representative NL queries hit correct MCP tool in tests.",
            ],
            "ENG-05/16",
            "ENG-09/16",
            [
                "**PRD**: conversational discovery.",
            ],
            [
                f"{plan}/FeatureDev/NLQueryEngine.md",
                f"{plan}/TaskSync.md",
            ],
            [f"{plan}/Project/PRD.md", f"{plan}/DataFindings/ExistingMCPAudit.md"],
        )
    )

    specs.append(
        T(
            "[ENG-09/16] React UI wired to FastAPI (P2-10)",
            "aravindsai003",
            "UI must show real agent responses for judges.",
            [
                "Wire `ui/` chat to `POST /api/v1/chat` with session_id handling.",
                "Error envelope surfaced in UI (no raw stack).",
            ],
            [
                "Manual: message → streamed or full JSON response rendered.",
            ],
            "ENG-01/16",
            "ENG-10/16, ENG-16/16",
            [
                "**PRD**: UX criterion.",
                "**ui/README.md**: verification steps updated.",
            ],
            [
                "ui/README.md",
                f"{plan}/FeatureDev/ChatUI.md",
                f"{plan}/Architecture/APIContract.md",
            ],
            [f"{plan}/Project/PRD.md", f"{plan}/Architecture/CodingStandards.md"],
        )
    )

    specs.append(
        T(
            "[ENG-10/16] HITL confirmation modal (P2-12)",
            "aravindsai003",
            "Judges must see proposal_id, risk badge, FQN list, confirm/cancel.",
            [
                "UI modal driven by `pending_confirmation` envelope.",
                "Calls `POST /chat/confirm` and `POST /chat/cancel`.",
            ],
            [
                "Approve + reject paths verified manually against APIContract.",
            ],
            "ENG-01/16, ENG-09/16",
            "ENG-16/16",
            [
                "**APIContract**: field parity with `pending_confirmation`.",
            ],
            [
                f"{plan}/Demo/Narrative.md",
                f"{plan}/Project/JudgePersona.md",
            ],
            [f"{plan}/Architecture/APIContract.md"],
        )
    )

    specs.append(
        T(
            "[ENG-11/16] OM-native UI + governance dashboard (P3-10, P3-11)",
            "aravindsai003",
            "OM purple, Inter, dark mode; optional dashboard cards for tag coverage.",
            [
                "Apply design tokens per Plan; governance summary widgets if time.",
            ],
            [
                "Visual pass matches Milestones / PRD UX targets (screenshot in PR).",
            ],
            "ENG-09/16",
            "ENG-16/16",
            [
                "**PRD**: UX score target.",
            ],
            [
                f"{plan}/FeatureDev/ChatUI.md",
                f"{plan}/Project/Milestones.md",
            ],
            [f"{plan}/Project/PRD.md"],
        )
    )

    specs.append(
        T(
            "[ENG-12/16] Multi-MCP - GitHub workflow (P3-01, P3-02)",
            "5009226-bhawikakumari",
            "Innovation differentiator: OM → GitHub issue per steward/table.",
            [
                "Phase 3 adapter wiring per CLAUDE.md; cross-MCP allowlist.",
                "Minimal happy-path demo with mocked or sandbox GitHub.",
            ],
            [
                "One scripted flow creates an issue from OM-derived PII list (documented in PR).",
            ],
            "ENG-06/16",
            "ENG-16/16",
            [
                "**PRD**: Multi-MCP criterion.",
            ],
            [
                f"{plan}/FeatureDev/MultiMCPOrchestrator.md",
                f"{plan}/Architecture/Overview.md",
            ],
            [f"{plan}/Project/PRD.md", f"{plan}/Security/ThreatModel.md"],
        )
    )

    specs.append(
        T(
            "[ENG-13/16] Integration tests + security gates + coverage baseline (P2-09, P2-10b, P3-08)",
            "5009226-bhawikakumari",
            "Prove resilience + injection + coverage trajectory toward ≥70%.",
            [
                "Expand `tests/integration/` for agent+MCP mocks including breaker-open.",
                "Ensure `tests/security/test_prompt_injection.py` complete for Layer 1 if missing.",
                "Document coverage % and gap list in PR.",
            ],
            [
                "`pytest tests/integration` and security tests green in CI.",
            ],
            "ENG-03/16",
            "ENG-14/16",
            [
                "**QualityGates**: Gate 0-2 satisfied where applicable.",
            ],
            [
                f"{plan}/Validation/TestStrategy.md",
                f"{plan}/Validation/QualityGates.md",
            ],
            [f"{plan}/Project/NFRs.md", f"{plan}/Security/PromptInjectionMitigation.md"],
        )
    )

    specs.append(
        T(
            "[ENG-14/16] CI - close gaps vs CIHardening (P3-09)",
            "5009226-bhawikakumari",
            "Align `.github/workflows/ci.yml` with Security/CIHardening.md (permissions, jobs, optional gates).",
            [
                "Diff checklist vs CIHardening; implement missing steps or documented waivers in PR body.",
            ],
            [
                "CI green on branch; waivers explicitly listed if any.",
            ],
            "None",
            "ENG-13/16",
            [
                "**Security/CIHardening.md**: explicit mapping table in PR description.",
            ],
            [
                f"{plan}/Security/CIHardening.md",
                ".github/workflows/ci.yml",
            ],
            [f"{plan}/Validation/QualityGates.md"],
        )
    )

    specs.append(
        T(
            "[ENG-15/16] Demo automation - seed + rehearsal scripts (P2-13b, P3-14-P3-16 code)",
            "5009226-bhawikakumari",
            "Reproducible demo: load seed, reindex hints, optional video script hooks.",
            [
                "Ensure `scripts/load_seed.py` + docs for `make demo-fresh` stay accurate.",
                "Add or refine checklist scripts if needed (no large binaries in git).",
            ],
            [
                "Another teammate can run demo from FailureRecovery pre-flight alone.",
            ],
            "ENG-14/16",
            "ENG-16/16",
            [
                "**Demo/FailureRecovery.md**: steps match scripts.",
            ],
            [
                f"{plan}/Demo/FailureRecovery.md",
                "seed/README.md",
            ],
            [f"{plan}/Demo/Narrative.md", f"{plan}/Validation/SetupGuide.md"],
        )
    )

    specs.append(
        T(
            "[ENG-16/16] E2E - Playwright chat + HITL + Judge Moment 3 (P2-13)",
            "aravindsai003",
            "Capstone: browser proves UI + API + injection path for judges.",
            [
                "Add Playwright tests under `tests/e2e/` (or `ui/e2e/` per repo convention).",
                "Cover chat round-trip, HITL modal, planted injection row from seed.",
            ],
            [
                "`pytest tests/e2e` or `npx playwright test` green in CI or documented nightly profile.",
            ],
            "ENG-09/16, ENG-10/16, ENG-13/16",
            "None",
            [
                "**JudgePersona**: Moment 3 evidence.",
                "**PRD**: Presentation + UX.",
            ],
            [
                f"{plan}/Project/JudgePersona.md",
                f"{plan}/Validation/TestStrategy.md",
                f"{plan}/Validation/SetupGuide.md",
            ],
            [f"{plan}/Demo/Narrative.md", f"{plan}/Security/PromptInjectionMitigation.md"],
        )
    )

    out: list[dict[str, str]] = []
    for title, assignee, body in specs:
        url = make_issue(title, assignee, body)
        num = url.rstrip("/").split("/")[-1]
        out.append({"title": title, "assignee": assignee, "url": url, "number": num})
        print(url, flush=True)

    nums = [int(x["number"]) for x in out]
    repl = {f"<<N{i:02d}>>": f"#{nums[i - 1]}" for i in range(1, len(nums) + 1)}
    tmp_edit = ROOT / ".issue_body_tmp.md"
    for idx, num in enumerate(nums):
        b = specs[idx][2]
        for k, v in repl.items():
            b = b.replace(k, v)
        tmp_edit.write_text(b, encoding="utf-8")
        try:
            gh("issue", "edit", str(num), "--body-file", str(tmp_edit))
        finally:
            tmp_edit.unlink(missing_ok=True)

    outp = ROOT / ".idea" / "Plan" / "SPRINT16_GITHUB_ISSUES.json"
    outp.parent.mkdir(parents=True, exist_ok=True)
    outp.write_text(json.dumps(out, indent=2), encoding="utf-8")
    print(f"\nWrote {outp.relative_to(ROOT)}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
