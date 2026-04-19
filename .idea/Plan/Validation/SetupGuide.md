# Local Setup Guide

## Prerequisites

| Tool | Version | Install |
|------|---------|---------|
| Python | 3.11+ | [python.org](https://python.org) |
| Node.js | 18+ | [nodejs.org](https://nodejs.org) |
| Docker | 24+ | [docker.com](https://docker.com) |
| Git | 2.30+ | System default |

## Step 1: Clone the Repository

```bash
git clone https://github.com/GunaPalanivel/OpenMetadata.git
cd OpenMetadata
```

## Step 2: Start OpenMetadata (Docker)

```bash
# From the project root
docker compose -f docker/development/docker-compose.yml up -d

# Wait for OM to be ready (check health)
curl http://localhost:8585/api/v1/health

# Expected: {"status":"healthy"}
```

## Step 3: Generate Bot JWT Token

1. Open OpenMetadata UI: `http://localhost:8585`
2. Login with default creds: `admin` / `admin`
3. Go to **Settings → Bots → ingestion-bot**
4. Copy the JWT token
5. Save to `.env` file:

```bash
AI_SDK_HOST=http://localhost:8585
AI_SDK_TOKEN=<paste-jwt-here>
```

## Step 4: Install Python Dependencies

```bash
cd openmetadata-mcp-agent/
pip install -e ".[dev]"
```

## Step 5: Verify MCP Connection

```bash
python -c "
from ai_sdk import AISdk, AISdkConfig
config = AISdkConfig.from_env()
client = AISdk.from_config(config)
result = client.mcp.call_tool('search_metadata', {'query': '*', 'size': 1})
print('✅ MCP Connected:', result)
"
```

## Step 6: Start the Chat UI

```bash
cd ui/
npm install
npm run dev
# → http://localhost:3000
```

## Step 7: Start the Agent Backend

```bash
cd openmetadata-mcp-agent/
uvicorn copilot.api:app --reload --port 8000
# → http://localhost:8000/docs
```

## Troubleshooting

| Issue | Fix |
|-------|-----|
| OM Docker fails to start | Check Docker Desktop is running, increase RAM to 8GB |
| JWT token expired | Re-generate from Settings → Bots |
| MCP connection refused | Verify OM is healthy: `curl localhost:8585/api/v1/health` |
| UI can't connect | Check API URL in `.env` matches backend port |
