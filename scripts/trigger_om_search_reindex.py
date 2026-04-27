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
"""Trigger OpenMetadata Elasticsearch search reindex (after API-only seed loads).

Tables created via ``load_seed.py`` exist in the catalog but may not appear in
``GET /api/v1/search/query`` until search indices are rebuilt. Use this script
(or ``make demo-fresh`` which invokes it) so ``search_metadata`` MCP has data.

Usage:
    python scripts/trigger_om_search_reindex.py
    python scripts/trigger_om_search_reindex.py --om-url http://host:8585

    # If ingestion-bot gets HTTP 403 on Trigger (common): re-run as admin:
    python scripts/trigger_om_search_reindex.py --as-admin

Requires ``AI_SDK_TOKEN`` (Bot JWT) for the default path, or ``--as-admin``
which logs in using ``OM_ADMIN_USERNAME`` and ``OM_ADMIN_PASSWORD`` from
``.env`` (both must be set; do not hardcode production credentials in source)
to obtain a JWT with Trigger rights. Typical local OM quickstart uses the
same values as the OM UI login; set them in ``.env`` (see ``.env.example``).

The repo root ``.env`` is loaded automatically via ``python-dotenv``.
"""

from __future__ import annotations

import argparse
import base64
import json
import os
import sys
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any

from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parent.parent
load_dotenv(ROOT / ".env")

API_PREFIX = "/api/v1"


def _admin_login_jwt(om_url: str, username: str, password: str) -> str | None:
    """Return access token from ``/users/login`` (OM 1.6.x password is Base64)."""
    candidates = [username]
    if username == "admin":
        candidates.extend(["admin@open-metadata.org"])

    url = f"{om_url}{API_PREFIX}/users/login"
    pwd_b64 = base64.b64encode(password.encode("utf-8")).decode("ascii")
    headers = {"Content-Type": "application/json"}

    for email in candidates:
        body = json.dumps({"email": email, "password": pwd_b64}).encode("utf-8")
        req = urllib.request.Request(  # noqa: S310 - OM URL is user-supplied host
            url, data=body, headers=headers, method="POST"
        )
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:  # noqa: S310
                data: dict[str, Any] = json.loads(resp.read().decode("utf-8"))
        except urllib.error.HTTPError as exc:
            _ = exc.read()
            continue
        except (urllib.error.URLError, TimeoutError, json.JSONDecodeError):
            continue

        tok = data.get("accessToken")
        if isinstance(tok, str) and tok:
            return tok
        nested = data.get("data", {})
        if isinstance(nested, dict):
            tok2 = nested.get("accessToken")
            if isinstance(tok2, str) and tok2:
                return tok2
    return None


def main() -> int:
    parser = argparse.ArgumentParser(description="POST OpenMetadata search reindex.")
    parser.add_argument(
        "--om-url",
        default=os.environ.get("AI_SDK_HOST", "http://localhost:8585").rstrip("/"),
        help="OpenMetadata base URL (default: AI_SDK_HOST or http://localhost:8585)",
    )
    parser.add_argument(
        "--as-admin",
        action="store_true",
        help="Log in as admin (Trigger permission) instead of using AI_SDK_TOKEN only",
    )
    args = parser.parse_args()

    token = ""
    if args.as_admin:
        u = os.environ.get("OM_ADMIN_USERNAME", "").strip()
        p = os.environ.get("OM_ADMIN_PASSWORD", "").strip()
        if not u or not p:
            print(
                "ERROR: --as-admin requires OM_ADMIN_USERNAME and OM_ADMIN_PASSWORD "
                "in .env (same credentials as OM UI admin login). See .env.example.",
                file=sys.stderr,
            )
            return 1
        print("reindex: logging in as admin for SearchIndexingApplication trigger …")
        token = _admin_login_jwt(args.om_url, u, p) or ""
        if not token:
            print(
                "ERROR: admin login failed; check OM_ADMIN_USERNAME / OM_ADMIN_PASSWORD "
                "or run OM UI: Settings → Search → reindex.",
                file=sys.stderr,
            )
            return 1
    else:
        token = os.environ.get("AI_SDK_TOKEN", "")
        if not token:
            print("ERROR: AI_SDK_TOKEN is not set (or pass --as-admin)", file=sys.stderr)
            return 1

    # OM 1.6.x: search indexing is the "SearchIndexingApplication" app, not /search/reindex.
    primary = f"{args.om_url}{API_PREFIX}/apps/trigger/SearchIndexingApplication"
    fallback = f"{args.om_url}{API_PREFIX}/search/reindex"
    body = json.dumps({"recreateIndex": False, "batchSize": 100}).encode("utf-8")
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }

    def _post(url: str) -> tuple[int, str]:
        req = urllib.request.Request(url, data=body, headers=headers, method="POST")  # noqa: S310
        try:
            with urllib.request.urlopen(req, timeout=120) as resp:  # noqa: S310
                return resp.status, resp.read().decode("utf-8", errors="replace")
        except urllib.error.HTTPError as exc:
            return exc.code, exc.read().decode("utf-8", errors="replace")
        except (urllib.error.URLError, TimeoutError) as exc:
            return -1, str(exc)

    status, raw = _post(primary)
    url_used = primary

    if status == 404:
        status, raw = _post(fallback)
        url_used = fallback

    if status == -1:
        print(f"FAIL: POST {url_used} -> {raw}", file=sys.stderr)
        return 1

    if status >= 400:
        if status == 400 and "already running" in raw.lower():
            print(f"OK: search indexing job already running ({url_used})")
            return 0
        if status == 403 and not args.as_admin:
            print(
                f"FAIL: POST {url_used} -> HTTP {status}: {raw[:800]}",
                file=sys.stderr,
            )
            print(
                "Hint: ingestion-bot often cannot Trigger SearchIndexingApplication. "
                "Re-run:  python scripts/trigger_om_search_reindex.py --as-admin",
                file=sys.stderr,
            )
            return 1
        print(f"FAIL: POST {url_used} -> HTTP {status}: {raw[:800]}", file=sys.stderr)
        return 1

    print(f"OK: search indexing triggered ({url_used})")
    if raw.strip():
        print(raw[:500])
    return 0


if __name__ == "__main__":
    sys.exit(main())
