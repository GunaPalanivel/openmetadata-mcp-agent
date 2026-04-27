# Getting Started

Get the agent running on your laptop in under 5 minutes. **Status: Hackathon Complete.**

## Prerequisites

| Tool    | Version | Notes                                                |
| ------- | ------- | ---------------------------------------------------- |
| Python  | 3.11+   | 3.12 also OK; older versions not supported           |
| Node.js | 20+     | LTS 20 or 22 recommended; required for the React UI  |
| Docker  | Recent  | Docker Desktop or Docker Engine (see WSL note below) |
| Git     | Recent  |                                                      |

> **WSL Docker alternative**: If you don't have Docker Desktop, you can run Docker Engine inside WSL. Use the WSL wrapper shown in Step 2 to start the stack.

## Step 1: Clone

```bash
git clone https://github.com/GunaPalanivel/openmetadata-mcp-agent.git
cd openmetadata-mcp-agent
```

## Step 2: Bring up OpenMetadata

You need a running OpenMetadata instance for the agent to call. This repo ships a self-contained Docker Compose stack:

```bash
# One command — starts MySQL, Elasticsearch, and OpenMetadata server
make om-start
# Waits for health automatically; prints next steps when ready.

# Verify manually (optional):
curl -s http://localhost:8585/api/v1/system/version
# Expected JSON includes "version"; admin liveness: curl -sf http://localhost:8586/healthcheck
```

This uses [`infrastructure/docker-compose.om.yml`](../infrastructure/docker-compose.om.yml) (OpenMetadata server image pinned there—currently `docker.getcollate.io/openmetadata/server:latest`; MySQL 8; Elasticsearch). Total stack stays under 8 GB. Make sure Docker Desktop has at least 8 GB allocated (Settings → Resources).

**WSL Docker users** (no Docker Desktop):

```bash
wsl.exe -d Ubuntu-22.04 -- bash -lc "docker compose -f infrastructure/docker-compose.om.yml up -d"
```

To stop: `make om-stop`. To check health: `make om-health`. To tail logs: `make om-logs`.

If you already have OpenMetadata running somewhere else, skip this step and set `AI_SDK_HOST` in your `.env` to point to it.

## Step 3: Generate a Bot JWT

The agent authenticates to OpenMetadata's MCP server using a Bot JWT.

### Option A: Automated (recommended)

```bash
# Generates a 30-day JWT and prints it for you to paste into .env
# Tries admin/admin first, then admin@open-metadata.org/admin on basic-auth installs.
make om-gen-token

# Custom expiry (supports 7/30/60/90 days or Unlimited)
python scripts/generate_bot_jwt.py --expiry-days 60

# Custom OM host
python scripts/generate_bot_jwt.py --host http://remote-om:8585

# Custom login identifier for installs with a different principal domain
python scripts/generate_bot_jwt.py --username admin@example.com
```

### Option B: Manual (via OM UI)

1. Open OpenMetadata UI: http://localhost:8585
2. Login with default creds: `admin` / `admin`
3. Go to **Settings -> Bots -> ingestion-bot**
4. Click **Generate New Token**, set expiry to 30 days, copy the token

> **Security**: Do NOT paste the token in any GitHub comment, issue, or PR.

## Step 4: Configure secrets

```bash
make setup
# Edit .env with your editor; paste:
#   AI_SDK_TOKEN=<the JWT from step 3>
#   OPENAI_API_KEY=<your OpenAI key from platform.openai.com/api-keys>
```

## Step 5: Install + run

```bash
# Install Python deps + UI deps
make install_dev_env

# One-time: install pre-commit hooks (lint, format, gitleaks, license headers).
# These run on every `git commit` and are required for PRs to merge.
pip install pre-commit
pre-commit install
pre-commit run --all-files   # initial bulk run

# Start backend + UI
make demo
# Backend: http://127.0.0.1:8000  (FastAPI docs at /api/v1/docs)
# UI:      http://localhost:3000
```

UI-only checks (port `:3000`, console clean): [`ui/README.md`](../ui/README.md). `make install_dev_env` runs `npm ci` under `ui/` using the committed lockfile.

### Step 5b: Load seed data

After OpenMetadata is healthy and the agent is running, load the sample catalog data:

```bash
python scripts/load_seed.py --drop-existing && python scripts/trigger_om_search_reindex.py
```

This populates tables, topics, and dashboards so the agent has metadata to work with.

## Step 6: Verify

In a new terminal:

```bash
python scripts/smoke_test.py --include-om
```

Should print `smoke: all green`. If it doesn't, check [Troubleshooting](#troubleshooting) below.

In the UI, click **Check backend health** — should show `status: ok`.

### Step 6b: Run Playwright E2E tests

```bash
cd ui && npx playwright install chromium && npx playwright test
```

---

## Troubleshooting

### `OPENAI_API_KEY not set`

You forgot to copy `.env.example` to `.env` or didn't paste a real key. Fix:

```bash
make setup
# edit .env
```

### OpenMetadata returns 401

Bot JWT is expired or wrong. Regenerate it (Step 3) and update `.env`.

### Docker container won't start (OOM)

OpenMetadata needs ~8 GB RAM. In Docker Desktop -> Settings -> Resources, increase memory to 8 GB and restart Docker.

### Docker Desktop is manually paused

**Symptom**: `Error response from daemon: Docker Desktop is manually paused`

**Fix**:

```bash
docker desktop restart
```

Then re-run `make om-start`.

### Docker credential helper not found (WSL)

**Symptom**: `error getting credentials - docker-credential-desktop.exe not found`

**Fix**: Bypass the credential helper by passing a temporary config directory:

```bash
docker --config /tmp/docker-nocreds compose -f infrastructure/docker-compose.om.yml up -d
```

### Port 8585 / 8000 / 3000 already in use

Another process is bound. Either kill it (`lsof -i :8000`) or override the port in `.env` (backend) / `vite.config.ts` (UI).

### CI fails on first push

This is expected for the first push because some dependencies need to actually install in CI. Re-run the failed workflow once and it usually goes green. If it persists, check the workflow logs and file an issue with the failed job name.

---

## Next

- Read [`CLAUDE.md`](../CLAUDE.md) for the architectural contract.
- Read [`CodePatterns.md`](../CodePatterns.md) before writing code.
- See [`docs/architecture.md`](architecture.md) for the system context diagram.
- See [`docs/api.md`](api.md) for the FastAPI surface.
- See [`docs/runbook.md`](runbook.md) for operations.

Deeper design notes: [`docs/architecture.md`](architecture.md), [`SECURITY.md`](../SECURITY.md), [`CONTRIBUTING.md`](../CONTRIBUTING.md).

Hackathon submitters: [Track T-01 submission checklist](hackathon-submission.md).
