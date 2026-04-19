# PR Review Checklist

Walk this checklist on every PR before approving. Skip sections that don't apply (e.g., skip "AI/ML Security" if the PR only touches docs).

## Basics

- [ ] `pre-commit run --all-files` is clean (author confirms, no `--no-verify`)
- [ ] Code builds without errors
- [ ] No unused imports or dead code
- [ ] Type hints on all Python signatures; no `any` / `as any` in TypeScript
- [ ] Names are descriptive (`classify_columns` not `process`, `is_active` not `flag`)
- [ ] No hardcoded secrets, tokens, or URLs
- [ ] No `console.log` / `print()` in production paths
- [ ] Functions have docstrings

## Architecture

Code lives in the right layer. Quick grep to verify:

- [ ] No business logic in `src/copilot/api/` (no `if confidence`, no `openai.`, no `client.mcp`)
- [ ] No HTTP types in `src/copilot/services/` (no `HTTPException`, `Request`, `Response`)
- [ ] No business rules in `src/copilot/clients/` (clients: build request, call SDK, map response, raise typed error)
- [ ] `tests/architecture/test_layer_imports.py` passes

## Resilience

Every external call (MCP, LLM, GitHub) needs three things:

- [ ] Explicit `timeout=` (connect + read)
- [ ] `@retry` with exponential backoff + jitter (`tenacity`)
- [ ] `pybreaker.CircuitBreaker` wrapping the call
- [ ] Circuit-breaker-open path returns structured error envelope (`om_unavailable`, `llm_unavailable`, etc.)
- [ ] No `requests.*` anywhere (use `httpx`); no bare `openai.chat.completions.create()`

## Observability

- [ ] No `print()` (ruff rule T201)
- [ ] No bare `logging.*` (only `structlog` with redaction processor)
- [ ] Service entry/exit has a structlog line with `request_id`
- [ ] Sensitive data (secrets, prompts, user content) never logged
- [ ] New metrics exposed on `GET /api/v1/metrics` if applicable

## AI/ML Security

Only applies to PRs that touch LLM prompts, tool registration, or catalog content flowing into prompts.

- [ ] Catalog content flowing into prompts goes through `services.prompt_safety.neutralize()`
- [ ] New tools added to `ALLOWED_TOOLS` in `services/agent.py`
- [ ] Write tools have `risk_level` set (`soft_write` / `hard_write`) and go through HITL confirmation
- [ ] LLM output parsed via `ToolCallProposal.model_validate()` before execution
- [ ] No `pickle`, `joblib`, `yaml.load(unsafe)`, `eval`, `exec`, or `os.system`
- [ ] `tests/security/test_prompt_injection.py` still covers all 5 patterns

## Tests

- [ ] New code has tests (happy path + at least one failure case)
- [ ] All existing tests pass (`make test`)
- [ ] Integration test added if touching MCP client or agent
- [ ] Coverage stays above 70% on `src/copilot/`

## Merge

- [ ] CI is green (lint, types, tests, security scan, secret scan)
- [ ] At least 1 approving review
- [ ] No merge conflicts, branch rebased on `main`
- [ ] If last PR in a phase: [QualityGates.md](../Validation/QualityGates.md) gates are green
