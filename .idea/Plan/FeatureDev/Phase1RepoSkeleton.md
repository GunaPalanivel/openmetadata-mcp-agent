# Phase 1 Repo Skeleton (P1-02)

## Owner: OMH-GSA (Guna)

## Phase: 1 (Day 3-4)

## Issue: [#15](https://github.com/GunaPalanivel/openmetadata-mcp-agent/issues/15)

---

## Overview

Verify that the on-disk directory tree covers every location listed in
[TaskSync.md](../TaskSync.md) P1-02, document the single intentional drift
from the original flat layout to the layered-architecture layout already
spec'd in [Architecture/Overview.md](../Architecture/Overview.md) and
[Architecture/CodePatterns.md](../Architecture/CodePatterns.md), and make
that drift the *single source of truth* so future contributors do not
re-flatten the package.

This is a verification gate, not a code change. No new `.py` files are added
in this task.

---

## 1. Planned skeleton (TaskSync.md P1-02, original)

Quoted verbatim from the P1-02 entry in [TaskSync.md](../TaskSync.md) as
written on Day-1 planning:

```
openmetadata-mcp-agent/
├── pyproject.toml
├── README.md
├── .env.example
├── .gitignore
├── src/copilot/
│   ├── __init__.py
│   ├── agent.py          ← LangGraph agent
│   ├── mcp_client.py     ← data-ai-sdk wrapper
│   ├── governance.py     ← Classification logic
│   └── api.py            ← FastAPI endpoints
├── ui/                   ← React chat (Phase 2)
└── tests/
```

The [P1-02 issue](https://github.com/GunaPalanivel/openmetadata-mcp-agent/issues/15)
also names five additional top-level directories that must exist on disk:
`scripts/`, `infrastructure/`, `docs/`, `seed/` (and `src/copilot/`, `ui/`,
`tests/` above).

---

## 2. Actual skeleton (on main at cut point `5b7e462`)

Top-level:

```
openmetadata-mcp-agent/
├── pyproject.toml            [present]
├── README.md                 [present]
├── .env.example              [present]
├── .gitignore                [present]
├── CHANGELOG.md
├── CLAUDE.md
├── CodePatterns.md
├── CONTRIBUTING.md
├── LICENSE_HEADER.txt
├── Makefile
├── SECURITY.md
├── .gitattributes
├── .pre-commit-config.yaml
├── .github/                  (workflows, issue + PR templates, dependabot)
├── docs/                     [present]
├── infrastructure/           [present]
├── scripts/                  [present]
├── seed/                     [present]
├── src/copilot/              [present; layered - see §3]
├── tests/                    [present; layered - see §3]
└── ui/                       [present]
```

`src/copilot/` (depth 2, generated files stripped):

```
src/copilot/
├── __init__.py
├── api/
│   ├── __init__.py
│   ├── chat.py
│   └── main.py
├── clients/
│   ├── __init__.py
│   ├── om_mcp.py
│   └── openai_client.py
├── config/
│   ├── __init__.py
│   └── settings.py
├── middleware/
│   ├── __init__.py
│   ├── error_envelope.py
│   ├── rate_limit.py
│   └── request_id.py
├── models/
│   ├── __init__.py
│   └── chat.py
├── observability/
│   ├── __init__.py
│   ├── metrics.py
│   └── redact.py
└── services/
    ├── __init__.py
    ├── agent.py
    └── prompt_safety.py
```

`tests/`:

```
tests/
├── __init__.py
├── conftest.py
├── architecture/
│   ├── __init__.py
│   └── test_layer_imports.py
├── security/
│   ├── __init__.py
│   └── test_prompt_injection.py
└── unit/
    ├── __init__.py
    ├── test_settings.py
    └── test_smoke.py
```

---

## 3. Drift: flat layout -> layered layout

### 3.1 Why the repo diverged from TaskSync

The Day-1 flat layout in TaskSync predates the architecture decisions
captured in [Overview.md](../Architecture/Overview.md) and
[CodePatterns.md](../Architecture/CodePatterns.md). Those docs are the
authoritative architecture contract for this service:

- [Overview.md](../Architecture/Overview.md) L61 - "**Governance Engine** - Python services in `src/copilot/services/`".
- [CodePatterns.md](../Architecture/CodePatterns.md) L283 - "Routes (`api/`) are thin orchestrators. Business logic lives in `services/`. Data access lives in `clients/`."
- [CodePatterns.md](../Architecture/CodePatterns.md) L334 - `src/copilot/api/` + `src/copilot/services/` mirror OpenMetadata's `openmetadata-service/` layering.
- [CodePatterns.md](../Architecture/CodePatterns.md) L336 - `src/copilot/clients/` + `src/copilot/models/` mirror OpenMetadata's `ingestion/` data layer.

The layered layout is also **enforced in CI** by
[tests/architecture/test_layer_imports.py](../../../tests/architecture/test_layer_imports.py),
which asserts: `api/` does not import `clients/`, `services/` does not
import `api/` or `fastapi`, and `clients/` does not import `api/` or
`services/`. Reverting to the flat layout in TaskSync would break those
tests and violate the Three Laws of Implementation Law 1 (layer separation)
from [CodingStandards.md](../Architecture/CodingStandards.md).

### 3.2 Mapping table

| TaskSync flat path             | Actual layered path                                                      | Justification                                                                                  |
| ------------------------------ | ------------------------------------------------------------------------ | ---------------------------------------------------------------------------------------------- |
| `src/copilot/__init__.py`      | `src/copilot/__init__.py`                                                | unchanged                                                                                      |
| `src/copilot/agent.py`         | `src/copilot/services/agent.py`                                          | Business logic -> `services/` per CodePatterns L283                                            |
| `src/copilot/mcp_client.py`    | `src/copilot/clients/om_mcp.py`                                          | External I/O -> `clients/` per CodePatterns L283/L336; named `om_mcp` to leave room for `github_mcp` in Phase 3 |
| `src/copilot/api.py`           | `src/copilot/api/main.py` + `src/copilot/api/chat.py`                    | Thin HTTP orchestrators -> `api/` package; split per endpoint group                            |
| `src/copilot/governance.py`    | **deferred** -> will land as `src/copilot/services/governance.py` in P1-08 / [#21](https://github.com/GunaPalanivel/openmetadata-mcp-agent/issues/21) | No caller yet. Adding an empty module now would add dead code and fail arch tests' no-orphan-import posture. Classification primitives currently live in `services/prompt_safety.py` and are composable from the eventual `governance.py`. |

### 3.3 Net-new modules beyond the flat plan

These were added during Phase 1 scaffold because they are required by the
architecture contract but were not spelled out in the Day-1 TaskSync list:

| Module                                | Role                                                                     | Contract reference                                                             |
| ------------------------------------- | ------------------------------------------------------------------------ | ------------------------------------------------------------------------------ |
| `src/copilot/clients/openai_client.py` | LLM provider client with timeout / retry / circuit-breaker              | [NFRs.md](../Project/NFRs.md), [Architecture/Overview.md](../Architecture/Overview.md) L57 |
| `src/copilot/config/settings.py`      | Pydantic Settings with `SecretStr` for 3 secrets, `host=127.0.0.1` (SC-1) | [Security/SecretsHandling.md](../Security/SecretsHandling.md)                  |
| `src/copilot/middleware/*`            | `request_id` / `error_envelope` / `rate_limit`                           | [Architecture/APIContract.md](../Architecture/APIContract.md)                  |
| `src/copilot/models/chat.py`          | Pydantic v2 models: `ChatSession`, `ToolCallProposal`, `ToolCallRecord`, `ErrorEnvelope`, etc. | [Architecture/DataModel.md](../Architecture/DataModel.md)                      |
| `src/copilot/observability/*`         | structlog JSON + Prometheus metrics + PII redaction                      | [Security/CIHardening.md](../Security/CIHardening.md), [Architecture/Overview.md](../Architecture/Overview.md) §Observability Subsystem |
| `src/copilot/services/prompt_safety.py` | Module G Layer-1 input neutralization (5 canonical patterns)           | [Security/PromptInjectionMitigation.md](../Security/PromptInjectionMitigation.md) |

All of these follow the same layering rules as the core five and are
covered by the arch-import tests.

---

## 4. Verification commands

Run from the repo root in the `.venv`:

```bash
# Every top-level dir from the P1-02 issue body exists:
for d in src/copilot ui tests scripts infrastructure docs seed; do
    [ -d "$d" ] && echo "ok  $d" || echo "MISS $d"
done

# Every src/copilot/ layer from Architecture/Overview.md exists:
for d in api clients config middleware models observability services; do
    [ -d "src/copilot/$d" ] && echo "ok  src/copilot/$d" || echo "MISS src/copilot/$d"
done

# Layer boundaries hold:
pytest tests/architecture -v
```

Expected: every line `ok ...`, and `tests/architecture` green (7 passed).

---

## 5. Done when (from [#15](https://github.com/GunaPalanivel/openmetadata-mcp-agent/issues/15))

- [x] Every directory listed in the P1-02 issue body exists on disk (`src/copilot/`, `ui/`, `tests/`, `scripts/`, `infrastructure/`, `docs/`, `seed/`).
- [x] Every directory listed in the TaskSync.md P1-02 tree exists on disk (`src/copilot/`, `ui/`, `tests/`).
- [x] Drift from the original flat layout is documented (this file + TaskSync.md update).
- [x] Governance module deferral is traced to a live issue (P1-08 / [#21](https://github.com/GunaPalanivel/openmetadata-mcp-agent/issues/21)).

## 6. Cross-references

- [TaskSync.md](../TaskSync.md) P1-02 (updated in this PR to the layered tree)
- [Progress.md](../Progress.md) P1-02 row
- [Architecture/Overview.md](../Architecture/Overview.md)
- [Architecture/CodePatterns.md](../Architecture/CodePatterns.md)
- [Architecture/CodingStandards.md](../Architecture/CodingStandards.md)
- [tests/architecture/test_layer_imports.py](../../../tests/architecture/test_layer_imports.py)
- Phase 1 dep-pin spec: [Phase1Dependencies.md](./Phase1Dependencies.md)
