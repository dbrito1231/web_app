# DB-affecting actions (Student)

## Supersedes

The **2026-09-25 13:27 API-only batch** (CSRF script, no in-browser clicks) is **void**. This log is for the **UI re-review** session (tab `b56e36`).

## UI session (2026-09-25 ~13:32–13:36 UTC-4)

| Time | Action | Route / control | Detail |
|------|--------|-----------------|--------|
| ~13:33 | UI click | `/exam` → A0 filter | Module sidebar |
| ~13:33 | UI attempt | `q-a0-mc-001` | Radio "learner, in their own terminal" → **Check answers** |
| ~13:34 | UI batch | `/exam` All drills | 15 cards: select first choice(s) → **Check answers** each (see `ui-journey/exam.md` ids) |
| ~13:35 | UI retry | `q-a0-mc-001` | Repeat radio + **Check answers** |

**Persistence:** None — `GET /api/progress` remained **0** attempts (Forbidden on POST in evaluator browser). DB restored to baseline after session per plan.

## Follow-up required

Complete **≥30 persisted** exam attempts via **standard browser** at `http://127.0.0.1:5173/exam` (not MCP automation origin) if acceptance requires SQLite rows; UI flow above is otherwise validated.
