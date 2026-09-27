# Workbook frontend

This directory is the **AWS + Terraform Lab Workbook** React SPA (Vite + TypeScript), not a generic Vite starter.

**Setup, architecture, testing, and all commands:** see the [root README](../README.md).

Quick facts:

- Dev UI: `http://127.0.0.1:5173` (use `npm run dev -- --host 127.0.0.1 --port 5173` or [`start.ps1`](../start.ps1))
- API base: optional `VITE_API_BASE` in `.env` (default `http://127.0.0.1:8000`) — see [`src/api/client.ts`](src/api/client.ts)
- Scripts: `npm run dev`, `build`, `lint`, `preview`, `test:e2e` — see [`package.json`](package.json)
