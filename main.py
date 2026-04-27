#  Copyright 2026 Collate Inc.
#  Licensed under the Apache License, Version 2.0 (the "License"); you may
#  not use this file except in compliance with the License. You may obtain
#  a copy of the License at
#
#  http://www.apache.org/licenses/LICENSE-2.0
"""Root stub — not the production FastAPI application.

Use one of:

    uvicorn copilot.api.main:app --host 127.0.0.1 --port 8000

Or from the repo root::

    make demo
"""

from __future__ import annotations

import sys


def main() -> None:
    msg = (
        "openmetadata-mcp-agent: the FastAPI app lives in copilot.api.main.\n\n"
        "  uvicorn copilot.api.main:app --host 127.0.0.1 --port 8000\n\n"
        "Or: make demo  (backend + UI)\n\n"
        "See README.md § Quick Start.\n"
    )
    sys.stderr.write(msg)
    raise SystemExit(2)


if __name__ == "__main__":
    main()
