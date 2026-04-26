#  Copyright 2026 Collate Inc.
#  Licensed under the Apache License, Version 2.0 (the "License"); you may
#  not use this file except in compliance with the License. You may obtain
#  a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
"""Check OpenMetadata MCP auth using repo-root ``.env`` (no secrets printed).

Usage (from repo root)::

    python scripts/diagnose_om_mcp_auth.py

Exit code 0 if ``list_tools`` and a drift-style ``search_metadata`` call succeed;
1 otherwise. Prints only lengths and status.
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parent.parent
load_dotenv(ROOT / ".env")

# Ensure pytest-only guards do not skip validation when run manually.
os.environ.pop("PYTEST_VERSION", None)


def main() -> int:
    from copilot.clients import om_mcp
    from copilot.config.settings import get_settings

    get_settings.cache_clear()
    om_mcp._get_sdk_client.cache_clear()

    s = get_settings()
    tok = s.ai_sdk_token.get_secret_value()
    print(f"AI_SDK_HOST={s.ai_sdk_host!r}")
    print(f"OM_MCP_HTTP_PATH={s.om_mcp_http_path!r}")
    print(f"AI_SDK_TOKEN length after normalization={len(tok)}")
    if not tok:
        print("ERROR: AI_SDK_TOKEN is empty after load.", file=sys.stderr)
        return 1
    kind = "fernet" if tok.startswith("fernet:") else ("jwt" if tok.startswith("eyJ") else "other")
    print(f"AI_SDK_TOKEN shape={kind!r}")

    # Bot JWT is validated by OM on MCP and many REST routes; ``/users/loggedIn`` may
    # return 404 for bot tokens and is not used as a signal here.

    try:
        names = om_mcp.list_tools()
    except Exception as exc:
        print(f"MCP list_tools FAILED: {type(exc).__name__}: {exc}", file=sys.stderr)
        return 1

    print(f"MCP list_tools OK: {len(names)} tool(s)")

    try:
        raw = om_mcp.call_tool("search_metadata", {"query": "*", "limit": 100})
    except Exception as exc:
        print(f"MCP search_metadata FAILED: {type(exc).__name__}: {exc}", file=sys.stderr)
        return 1

    hits = raw.get("hits", raw.get("data", raw.get("results", [])))
    if isinstance(hits, dict):
        hits = hits.get("hits", [])
    n = len(hits) if isinstance(hits, list) else 0
    print(f"MCP search_metadata OK: {n} hit(s) in normalised response")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
