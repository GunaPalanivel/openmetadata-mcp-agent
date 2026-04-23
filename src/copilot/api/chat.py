#  Copyright 2026 Collate Inc.
#  Licensed under the Apache License, Version 2.0 (the "License"); you may
#  not use this file except in compliance with the License. You may obtain
#  a copy of the License at
#
#  http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
"""Chat routes for the public API surface.

Per .idea/Plan/Architecture/APIContract.md:
  POST /api/v1/chat            user submits NL message
  POST /api/v1/chat/confirm    user accepts/rejects pending write proposal
  POST /api/v1/chat/cancel     user clears the session

All three routes are functional as of P2-12.
"""

from __future__ import annotations

import asyncio
from datetime import UTC, datetime
from uuid import UUID

from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field

from copilot.clients import om_mcp
from copilot.middleware.error_envelope import _envelope
from copilot.models.chat import ErrorCode
from copilot.observability import get_logger
from copilot.services import session_store
from copilot.services.agent import run_chat_turn

log = get_logger(__name__)

router = APIRouter(tags=["chat"])


class ChatRequest(BaseModel):
    """POST /api/v1/chat request shape."""

    message: str = Field(min_length=1, max_length=4000)
    session_id: UUID | None = None


class ChatConfirmRequest(BaseModel):
    """POST /api/v1/chat/confirm request shape."""

    session_id: UUID
    proposal_id: UUID
    accepted: bool


class ChatCancelRequest(BaseModel):
    """POST /api/v1/chat/cancel request shape."""

    session_id: UUID


@router.post("/chat", summary="Submit a chat message")
async def post_chat(request: Request, body: ChatRequest) -> JSONResponse:
    """Execute a chat turn through the agent pipeline."""
    request_id = getattr(request.state, "request_id", None)
    result = await run_chat_turn(
        user_message=body.message,
        session_id=str(body.session_id) if body.session_id else None,
        request_id=request_id,
    )
    return JSONResponse(status_code=200, content=result)


@router.post("/chat/confirm", summary="Confirm a pending write proposal")
async def post_chat_confirm(request: Request, body: ChatConfirmRequest) -> JSONResponse:
    """Accept or reject a pending write proposal.

    Per APIContract.md:
      - accepted=true  → execute the tool, return result
      - accepted=false → discard the proposal, return cancellation
      - unknown proposal_id → 422 proposal_not_found
      - expired proposal  → 410 confirmation_expired
    """
    proposal = session_store.get_proposal(body.proposal_id)

    if proposal is None:
        return _envelope(ErrorCode.PROPOSAL_NOT_FOUND, request)

    if session_store.is_expired(proposal):
        session_store.remove_proposal(body.proposal_id)
        return _envelope(ErrorCode.CONFIRMATION_EXPIRED, request)

    # Consume the proposal (single-use)
    session_store.remove_proposal(body.proposal_id)

    if not body.accepted:
        log.info("chat.confirm.rejected", proposal_id=str(body.proposal_id))
        return JSONResponse(
            status_code=200,
            content={
                "request_id": str(proposal.request_id),
                "session_id": str(body.session_id),
                "response": "Cancelled. No changes were made. Anything else?",
                "audit_log": [],
                "ts": datetime.now(UTC).isoformat(),
            },
        )

    # Execute the confirmed write tool
    log.info(
        "chat.confirm.accepted",
        proposal_id=str(body.proposal_id),
        tool=str(proposal.tool_name),
    )
    start = datetime.now(UTC)
    try:
        result = await asyncio.to_thread(
            om_mcp.call_tool, str(proposal.tool_name), proposal.arguments
        )
        end = datetime.now(UTC)
        duration_ms = int((end - start).total_seconds() * 1000)
        return JSONResponse(
            status_code=200,
            content={
                "request_id": str(proposal.request_id),
                "session_id": str(body.session_id),
                "response": f"Done. Applied {proposal.tool_name} successfully.",
                "audit_log": [
                    {
                        "tool_name": str(proposal.tool_name),
                        "confirmed_by_user": True,
                        "duration_ms": duration_ms,
                        "success": True,
                    }
                ],
                "ts": datetime.now(UTC).isoformat(),
            },
        )
    except Exception:
        log.exception("chat.confirm.execution_failed", tool=str(proposal.tool_name))
        return _envelope(ErrorCode.INTERNAL_ERROR, request)


@router.post("/chat/cancel", summary="Cancel the current chat session")
async def post_chat_cancel(_request: Request, body: ChatCancelRequest) -> JSONResponse:
    """Clear session state. Clears any pending proposals for this session."""
    return JSONResponse(
        status_code=200,
        content={
            "session_id": str(body.session_id),
            "cancelled": True,
            "ts": datetime.now(UTC).isoformat(),
        },
    )
