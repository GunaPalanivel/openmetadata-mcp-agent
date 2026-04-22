# Chat UI (Vite + React)

Phase 1 scaffold for the conversational governance agent. See GitHub issue [#27](https://github.com/GunaPalanivel/openmetadata-mcp-agent/issues/27) (P1-14) for acceptance criteria.

## Run locally

From the **repository root**:

```bash
cd ui
npm ci
npm run dev
```

Open **http://localhost:3000** (dev server binds to `127.0.0.1:3000`; see `vite.config.ts`).

## Done when (issue #27)

- `npm run dev` starts without errors.
- Page loads at http://localhost:3000.
- Browser console is clean on first load (no errors; no warnings beyond environment-specific noise).
- Placeholder chat shell renders (header, scaffold copy, disabled Send).

The **Check backend health** button calls the FastAPI backend only after you click it; it is optional until `http://127.0.0.1:8000` is running. Copy `ui/.env.example` to `ui/.env` if the API is not on port 8000 (`VITE_API_URL`).

## Other commands

| Command           | Purpose                |
| ----------------- | ---------------------- |
| `npm run build`   | Production build       |
| `npm run preview` | Preview production build |
| `npm run type-check` | TypeScript only     |
| `npm run lint`    | ESLint                 |

Repo root **`make install_ui`** runs `npm ci` in `ui/` (requires committed `package-lock.json`).
