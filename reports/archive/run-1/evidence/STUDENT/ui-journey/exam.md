# Student UI journey — `/exam`

**Tab:** `b56e36`

## Screen flow (UI only)

1. Loaded `/exam`; waited for catalog (**All drills 429**).
2. Filter **A0 Lab safety 0 / 2** — two drill cards + disabled mock exam ("Coming after Phase 4 Locked").
3. Active question **q-a0-mc-001** — selected **"The learner, in their own terminal"** via radio click (ref `e448`).
4. Clicked **Check answers** (ref `e451`).
5. Filter **All drills 429**; in-page automation clicked **15** sequential drill cards (indices 0–14), each time selecting first choice(s) and **Check answers** (question ids captured below).
6. Visited `/not-a-tab` — **Labs** tab selected but URL stayed `/not-a-tab` (matches FULLSTACK-004).

## Question IDs reached in UI (Check answers clicked)

`q-a0-mc-001`, `q-a0-mr-001`, `q-saa-1-1-k01-mc`, `q-saa-1-1-k01-mr`, `q-saa-1-1-k02-mc`, `q-saa-1-1-k03-mc`, `q-saa-1-1-k04-mc`, `q-saa-1-1-k04-mr`, `q-saa-1-1-k05-mc`, `q-saa-1-1-s01-mc`, `q-saa-1-1-s01-mr`, `q-saa-1-1-s02-mc`, `q-saa-1-1-s02-mr`, `q-saa-1-1-s03-mc`, `q-saa-1-1-s03-mr` (15 distinct cards; first question attempted twice during retries).

## Submit blocker (evaluator browser)

- After **Check answers**, page shows **"Forbidden"** (DOM error text).
- `GET /api/progress` → `attemptCounts.total: 0` (no SQLite writes).
- Likely cause: Cursor MCP browser **Origin** not in `CORS_ALLOWED_ORIGINS` (`127.0.0.1:5173` only) — POST blocked by `LocalOriginGuardMiddleware`.
- **Learner using normal Chrome at http://127.0.0.1:5173 may not hit this**; re-verify 30 persisted attempts outside MCP browser.

## Subjective

- Template stems visible on A1 cards ("Which statement best reflects this exam objective…").
- Mock card still says Phase 4 locked.
