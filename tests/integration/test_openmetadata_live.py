#  Copyright 2026 Collate Inc.
#  Licensed under the Apache License, Version 2.0 (the "License"); you may
#  not use this file except in compliance with the License. You may obtain
#  a copy of the License at
#
#  http://www.apache.org/licenses/LICENSE-2.0
"""Live-stack probes. Run via ``make test-integration`` with OM up, or CI on main."""

from __future__ import annotations

import os

import httpx
import pytest

pytestmark = pytest.mark.integration


def _sdk_host() -> str:
    return os.environ.get("AI_SDK_HOST", "http://localhost:8585").rstrip("/")


@pytest.mark.integration
def test_openmetadata_api_version_reachable() -> None:
    """OM HTTP API must answer at ``/api/v1/system/version`` (auth not required)."""
    url = f"{_sdk_host()}/api/v1/system/version"
    try:
        response = httpx.get(url, timeout=15.0)
    except httpx.RequestError as exc:
        pytest.skip(f"OpenMetadata not reachable at {_sdk_host()}: {exc}")

    assert response.status_code == 200, f"GET {url} → {response.status_code}"
    body = response.json()
    assert "version" in body or "Version" in str(body)
