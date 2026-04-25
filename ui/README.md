# Chat UI (Vite + React)

Phase 2 chat wiring for the conversational governance agent. Implements GitHub issue [#83](https://github.com/GunaPalanivel/openmetadata-mcp-agent/issues/83).

## Run locally

From the **repository root**:

```bash
cd ui
npm ci
npm run dev
```

Open **http://localhost:3000** (dev server binds to `127.0.0.1:3000`; see `vite.config.ts`).

## Verification (issue #83)

- `npm run dev` starts without errors.
- Page loads at http://localhost:3000.
- Send button enables for non-empty input.
- First message posts to `POST /api/v1/chat` without `session_id`.
- UI stores returned `session_id` and sends it on the next message.
- Agent response text renders in the chat transcript.
- If backend returns non-2xx error envelope, UI shows `<code>: <message>` and never raw stack traces.

The **Check backend health** button calls the FastAPI backend only after you click it.

Set `VITE_API_URL` in `ui/.env` if backend is not `http://localhost:8000`:

```env
VITE_API_URL=http://127.0.0.1:8000
```

## Playwright E2E Tests

```bash
npx playwright install chromium
npx playwright test
```

Three E2E scenarios cover:

1. Chat round-trip (send message → receive agent response)
2. HITL confirmation modal (write-tool proposals require explicit user approval)
3. Moment 3 injection neutralization (malicious catalog content is escaped)

## Other commands

| Command              | Purpose                  |
| -------------------- | ------------------------ |
| `npm run build`      | Production build         |
| `npm run preview`    | Preview production build |
| `npm run type-check` | TypeScript only          |
| `npm run lint`       | ESLint                   |
| `npm run test:e2e`   | Playwright browser E2E   |

Repo root **`make install_ui`** runs `npm ci` in `ui/` (requires committed `package-lock.json`).
