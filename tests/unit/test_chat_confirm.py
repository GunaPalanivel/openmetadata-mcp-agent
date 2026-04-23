#  Copyright 2026 Collate Inc.
#  Licensed under the Apache License, Version 2.0 (the "License"); you may
#  not use this file except in compliance with the License. You may obtain
#  a copy of the License at
#
#  http://www.apache.org/licenses/LICENSE-2.0
"""Tests for POST /api/v1/chat/confirm (P2-12 HITL confirmation flow).

Covers:
  - Confirm with valid proposal_id → 200, tool executed
  - Reject with valid proposal_id → 200, no changes
  - Unknown proposal_id → 422 proposal_not_found
  - Expired proposal → 410 confirmation_expired
  - Double-confirm → first wins, second gets proposal_not_found
"""

from __future__ import annotations

from datetime import UTC, datetime, timedelta
from uuid import uuid4

import pytest
from unittest.mock import patch
from fastapi.testclient import TestClient

from copilot.models.chat import RiskLevel, ToolCallProposal, ToolName
from copilot.services import session_store


@pytest.fixture(autouse=True)
def _clear_store() -> None:
    """Ensure a clean store for every test."""
    session_store.clear_all()


def _make_proposal(
    *,
    tool: ToolName = ToolName.PATCH_ENTITY,
    risk: RiskLevel = RiskLevel.HARD_WRITE,
    expired: bool = False,
) -> ToolCallProposal:
    """Build a ToolCallProposal, optionally already expired."""
    now = datetime.now(UTC)
    return ToolCallProposal(
        request_id=uuid4(),
        tool_name=tool,
        arguments={"entityFQN": "customer_db.public.users", "op": "add_tag", "tag": "PII.Sensitive"},
        risk_level=risk,
        rationale="Apply PII tag to users table",
        expires_at=now - timedelta(minutes=1) if expired else now + timedelta(minutes=5),
    )


class TestConfirmAccepted:
    """Confirm with accepted=true → execute the tool, return 200."""

    @patch("copilot.api.chat.om_mcp.call_tool", return_value={"status": "ok"})
    def test_confirm_executes_tool(self, mock_call_tool, client: TestClient) -> None:
        proposal = _make_proposal()
        session_store.store_proposal(proposal)
        session_id = str(uuid4())

        response = client.post(
            "/api/v1/chat/confirm",
            json={
                "session_id": session_id,
                "proposal_id": str(proposal.proposal_id),
                "accepted": True,
            },
        )

        assert response.status_code == 200
        body = response.json()
        assert body["session_id"] == session_id
        assert "Done." in body["response"]
        assert body["audit_log"][0]["confirmed_by_user"] is True
        assert body["audit_log"][0]["success"] is True
        assert body["audit_log"][0]["tool_name"] == "patch_entity"

        mock_call_tool.assert_called_once_with(
            "patch_entity",
            {"entityFQN": "customer_db.public.users", "op": "add_tag", "tag": "PII.Sensitive"},
        )

    @patch("copilot.api.chat.om_mcp.call_tool", return_value={"status": "ok"})
    def test_confirm_consumes_proposal(self, mock_call_tool, client: TestClient) -> None:
        """After confirmation, the proposal is consumed (single-use)."""
        proposal = _make_proposal()
        session_store.store_proposal(proposal)

        client.post(
            "/api/v1/chat/confirm",
            json={
                "session_id": str(uuid4()),
                "proposal_id": str(proposal.proposal_id),
                "accepted": True,
            },
        )

        assert session_store.get_proposal(proposal.proposal_id) is None


class TestConfirmRejected:
    """Confirm with accepted=false → 200, no changes made."""

    def test_reject_returns_cancellation(self, client: TestClient) -> None:
        proposal = _make_proposal()
        session_store.store_proposal(proposal)
        session_id = str(uuid4())

        response = client.post(
            "/api/v1/chat/confirm",
            json={
                "session_id": session_id,
                "proposal_id": str(proposal.proposal_id),
                "accepted": False,
            },
        )

        assert response.status_code == 200
        body = response.json()
        assert "Cancelled" in body["response"]
        assert body["audit_log"] == []

    def test_reject_consumes_proposal(self, client: TestClient) -> None:
        proposal = _make_proposal()
        session_store.store_proposal(proposal)

        client.post(
            "/api/v1/chat/confirm",
            json={
                "session_id": str(uuid4()),
                "proposal_id": str(proposal.proposal_id),
                "accepted": False,
            },
        )

        assert session_store.get_proposal(proposal.proposal_id) is None


class TestConfirmNotFound:
    """Unknown proposal_id → 422 proposal_not_found."""

    def test_unknown_proposal_returns_422(self, client: TestClient) -> None:
        response = client.post(
            "/api/v1/chat/confirm",
            json={
                "session_id": str(uuid4()),
                "proposal_id": str(uuid4()),
                "accepted": True,
            },
        )

        assert response.status_code == 422
        body = response.json()
        assert body["code"] == "proposal_not_found"


class TestConfirmExpired:
    """Expired proposal → 410 confirmation_expired."""

    def test_expired_proposal_returns_410(self, client: TestClient) -> None:
        proposal = _make_proposal(expired=True)
        session_store.store_proposal(proposal)

        response = client.post(
            "/api/v1/chat/confirm",
            json={
                "session_id": str(uuid4()),
                "proposal_id": str(proposal.proposal_id),
                "accepted": True,
            },
        )

        assert response.status_code == 410
        body = response.json()
        assert body["code"] == "confirmation_expired"

    def test_expired_proposal_is_cleaned_up(self, client: TestClient) -> None:
        proposal = _make_proposal(expired=True)
        session_store.store_proposal(proposal)

        client.post(
            "/api/v1/chat/confirm",
            json={
                "session_id": str(uuid4()),
                "proposal_id": str(proposal.proposal_id),
                "accepted": True,
            },
        )

        assert session_store.get_proposal(proposal.proposal_id) is None


class TestDoubleConfirm:
    """Double-confirm: first wins, second gets proposal_not_found."""

    @patch("copilot.api.chat.om_mcp.call_tool", return_value={"status": "ok"})
    def test_second_confirm_returns_not_found(self, mock_call_tool, client: TestClient) -> None:
        proposal = _make_proposal()
        session_store.store_proposal(proposal)
        body = {
            "session_id": str(uuid4()),
            "proposal_id": str(proposal.proposal_id),
            "accepted": True,
        }

        first = client.post("/api/v1/chat/confirm", json=body)
        assert first.status_code == 200

        second = client.post("/api/v1/chat/confirm", json=body)
        assert second.status_code == 422
        assert second.json()["code"] == "proposal_not_found"


class TestSessionStore:
    """Unit tests for the session_store module itself."""

    def test_store_and_get(self) -> None:
        proposal = _make_proposal()
        session_store.store_proposal(proposal)
        assert session_store.get_proposal(proposal.proposal_id) is proposal

    def test_remove(self) -> None:
        proposal = _make_proposal()
        session_store.store_proposal(proposal)
        removed = session_store.remove_proposal(proposal.proposal_id)
        assert removed is proposal
        assert session_store.get_proposal(proposal.proposal_id) is None

    def test_remove_missing_returns_none(self) -> None:
        assert session_store.remove_proposal(uuid4()) is None

    def test_is_expired_false(self) -> None:
        proposal = _make_proposal(expired=False)
        assert not session_store.is_expired(proposal)

    def test_is_expired_true(self) -> None:
        proposal = _make_proposal(expired=True)
        assert session_store.is_expired(proposal)

    def test_is_expired_no_ttl(self) -> None:
        proposal = _make_proposal()
        proposal.expires_at = None
        assert not session_store.is_expired(proposal)

    def test_clear_all(self) -> None:
        for _ in range(5):
            session_store.store_proposal(_make_proposal())
        session_store.clear_all()
        assert session_store.get_proposal(uuid4()) is None
