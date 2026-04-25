# Changelog

All notable changes to this project are documented here. Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), version numbers follow [SemVer](https://semver.org/).

## [0.3.0] - 2026-04-25

Hackathon final submission — WeMakeDevs × OpenMetadata "Back to the Metadata" (Track T-01).

### Added

#### Phase 2 — Core Features

- LangGraph 6-node agent orchestrator (`classify_intent` → `select_tools` → `validate_proposal` → `hitl_gate` → `execute_tool` → `format_response`)
- HITL confirmation gate for all write operations (`POST /api/v1/chat/confirm`)
- Governance state machine (`GovernanceRecord` FSM with scan → suggest → approve/reject → enforce transitions)
- Session store with TTL-based expiry for pending confirmations
- Drift detection background polling loop (60 s interval)
- Governance API (`GET /api/v1/governance/drift`)
- Auto-classification pipeline (PII detection via `search` + `get_entity_details` + `patch_entity`)
- Lineage impact analysis (3-hop upstream/downstream via `get_entity_lineage`)
- Multi-MCP orchestration (OM MCP + GitHub MCP in a single conversation)
- NL router with deterministic + LLM fallback intent classification
- Similarity scoring for search result relevance
- Prompt safety module (5-layer Module G defense: regex, HTML escape, truncation, allowlist, HITL)

#### Phase 2 — Frontend

- Full chat UI with message history, `session_id` tracking, error envelopes
- HITL confirmation modal (`proposal_id`, `tool_name`, `risk_level`, arguments, expiry)
- Drift dashboard sidebar (drift count, entity count, last scan timestamp)
- Health check button with backend status display

#### Phase 2 — Infrastructure

- `docker-compose.om.yml` for local OpenMetadata (MySQL 8 + ES 7.16 + OM server + migrate)
- `scripts/generate_bot_jwt.py` for automated Bot JWT generation
- `scripts/load_seed.py` for frozen demo dataset (52 tables)
- `scripts/trigger_om_search_reindex.py` for ES index refresh
- `scripts/smoke_test.py` for demo-day morning validation
- `scripts/multi_mcp_demo.py` for Phase 3 cross-platform workflow

#### Phase 3 — E2E & Polish

- Playwright E2E test suite (`ui/e2e/chat-hitl-moment3.spec.ts`) with 3 scenarios
- Playwright config (`ui/playwright.config.ts`) with Chromium project + Vite webServer
- Integration test suite (`tests/integration/`) with mock MCP + full agent pipeline

### Security

- 5-layer prompt-injection defense (Module G) with 5 canonical pattern tests
- Tool allowlist (13 tools: 12 OM + 1 GitHub) enforced server-side
- Secret redaction processor in structlog (strips `AI_SDK_TOKEN`, `OPENAI_API_KEY` from all log lines)
- Bandit AST scanning + pip-audit CVE scanning in CI
- Gitleaks secret scanning on every commit

### Test & Quality

- 333 tests passing (unit + security + architecture)
- 87 % code coverage on `src/copilot/` (70 % CI gate)
- 3 Playwright E2E scenarios
- Architecture layer import enforcement tests
- Pre-commit hooks: ruff + gitleaks + license headers

### Hackathon

- Submitted to WeMakeDevs × OpenMetadata "Back to the Metadata" hackathon (Apr 17–26, 2026)
- Track T-01: MCP Ecosystem & AI Agents
- Targets issues [#26645](https://github.com/open-metadata/OpenMetadata/issues/26645) and [#26608](https://github.com/open-metadata/OpenMetadata/issues/26608)
- Team: The Mavericks (Guna Palanivel, Priyanka Sen, Aravind Sai, Bhawika Kumari)

## [0.1.0] - 2026-04-19

### Added

- Initial scaffold for `openmetadata-mcp-agent` (BUILD Phase 1 of [`.idea/Plan/TaskSync.md`](.idea/Plan/TaskSync.md))
- Repository structure mirroring OpenMetadata's layered conventions (api / services / clients / models / middleware / config / observability)
- FastAPI app factory with `/api/v1/healthz` (functional), `/api/v1/metrics` (Prometheus), `/api/v1/chat` (stub returning structured `not_implemented` envelope)
- Full Pydantic v2 models: `ChatSession`, `ToolCallProposal`, `ToolCallRecord`, `ClassificationJob`, `TagSuggestion`, `LineageImpactReport`, `LineageNode`, `ErrorEnvelope`
- `services/prompt_safety.neutralize()` — Module G Layer-1 input neutralization (escape + truncate + instruction-pattern flagging) covering 5 canonical injection patterns
- `middleware/request_id.py` — UUID propagation through `structlog.contextvars`
- `middleware/error_envelope.py` — typed exception → structured error envelope (`code`, `message`, `request_id`, `ts`)
- `middleware/rate_limit.py` — slowapi gates per [`.idea/Plan/Project/NFRs.md`](.idea/Plan/Project/NFRs.md)
- `config/settings.py` — Pydantic Settings with `SecretStr` for the 3 secrets, `host=127.0.0.1` (SC-1), all NFR resilience knobs
- `observability/redact.py` — structlog processor that strips known secret values from log lines
- `observability/metrics.py` — Prometheus counters/histograms for the 4 Golden Signals + token usage + circuit-breaker state
- `tests/unit/test_smoke.py` — imports every module + asserts `/healthz` returns 200
- `tests/security/test_prompt_injection.py` — 5 canonical patterns from [`.idea/Plan/Security/PromptInjectionMitigation.md`](.idea/Plan/Security/PromptInjectionMitigation.md)
- `tests/architecture/test_layer_imports.py` — enforces Three Laws of Implementation Law 1 (layer separation)
- `ui/` — Vite + React 18 + TypeScript 5 chat shell with OM brand styling (`#7147E8`, Inter, dark mode)
- `seed/` — frozen demo dataset placeholder (will hold 50+ tables in Phase 2)
- `scripts/` — `load_seed.py`, `smoke_test.py`, `check_openai_quota.py`
- `infrastructure/docker-compose.yml` — agent backend service (OM is assumed running externally)
- `docs/` — public documentation (getting-started, architecture, api, runbook, contributing)
- `.github/workflows/ci.yml` — full hardened pipeline: lint + typecheck + unit tests + security scan + secret scan + UI build + path-guard (per [`.idea/Plan/Security/CIHardening.md`](.idea/Plan/Security/CIHardening.md))
- `.github/dependabot.yml` — pip + actions + npm weekly
- `.github/PULL_REQUEST_TEMPLATE.md` — adapted from [`.idea/Plan/PR-Review/PRTemplate.md`](.idea/Plan/PR-Review/PRTemplate.md) with all four review gates (Architecture / Resilience / Observability / AI-ML Security)
- `.github/ISSUE_TEMPLATE/` — task / feature / bug templates referencing TaskSync IDs
- `CLAUDE.md` — top-level architecture contract for AI agents
- `CodePatterns.md` — code conventions mirroring OpenMetadata (Python pytest/Pydantic, TypeScript no-`any`/no-`console.log`, comments policy, git, license headers)
- `LICENSE_HEADER.txt` — Apache 2.0 source-file header
- Pre-commit hooks: ruff + gitleaks (SHA-pinned)
- `.gitignore` — curated to publish ~38 of 48 internal planning docs (strong engineering-process signal) while keeping 8 tactical/sensitive files private

### Defense-in-depth highlights

- **Five trust zones** documented (browser → agent backend → LLM provider → OpenMetadata MCP → GitHub MCP)
- **Three independent gates** between LLM output and any write: Pydantic schema validation → tool allowlist → HITL confirmation
- **No `pickle` / `joblib` / `eval` / `exec` / `os.system`** anywhere — bandit + ruff enforce
- **Secret redaction** in every log line (defense against accidental f-string interpolation)
- **Circuit breakers** on every external call (OM MCP, OpenAI, GitHub MCP)

### Hackathon

Submitted to WeMakeDevs × OpenMetadata "Back to the Metadata" hackathon (Apr 17–26, 2026), Track T-01: MCP Ecosystem & AI Agents. Targets issues [#26645](https://github.com/open-metadata/OpenMetadata/issues/26645) and [#26608](https://github.com/open-metadata/OpenMetadata/issues/26608). Team: The Mavericks (Guna Palanivel, Priyanka Sen, Aravind Sai, Bhawika Kumari).
