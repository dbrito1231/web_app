# Student Agent UI Re-Review (Phase 3 redo)

**Status:** Executed 2026-09-25 — UI tab `b56e36`; all four routes visited; **≥15** exam cards clicked with **Check answers**. **Gap:** MCP evaluator browser POST **Forbidden** → 0 SQLite attempts; see `reports/evidence/STUDENT/ui-journey/exam.md`. **Follow-up:** 30 persisted attempts in standard Chrome at `127.0.0.1:5173` if required for acceptance.

## Goal

Re-run Agent 1 (College IT Student) strictly through the learner UI, matching `.cursor/plans/c-users-dbadmin-downloads-claude-web-ap-imperative-boot.md` §7 Agent 1 and §6 Phase 2 UI evidence rules.

## Hard rules

- **Browser-only** learner actions: built-in browser MCP, dedicated tab (`newTab: true` at start), desktop viewport only.
- **Forbidden:** direct `curl`/PowerShell `POST` to `/api/attempts`, reading `frontend/` or `backend/` before UI exploration (JSON lesson/lab reads allowed only for Confirmed teach-before-test findings after UI observation).
- **DB:** Restore from `eval-baseline/db.sqlite3.bak` before first UI click; log every attempt/checkpoint in `reports/evidence/STUDENT/db-actions.md`; restore DB again after session (Phase 14).
- **Writes:** Only `reports/**` and this plan file.

## UI checklist (must complete)

| Step | Route | Required actions | Evidence output |
|------|--------|------------------|-----------------|
| 1 | `/start` | Cold load; read onboarding; open **A0** lesson from sidebar; note readiness/progress copy | `reports/evidence/STUDENT/ui-journey/start.md` + screenshot ref |
| 2 | `/labs` | Find **GL-01** without source; expand card; read before-you-start + first 3 steps; open **UL-01** criteria (no reveal) | `ui-journey/labs.md` |
| 3 | `/coverage` | Open tab; scan registry presentation; one drill-down if available | `ui-journey/coverage.md` |
| 4 | `/exam` | Filter **A0** → answer all A0 drills via **Check answers**; repeat for **A1** sample (~25–30 total MC/MR) using only clicks/keyboard | `ui-journey/exam.md` + `db-actions.md` rows tagged `(UI)` |
| 5 | Unknown route | Visit `/not-a-tab` or invalid slug; note behavior | sentence in `ui-journey/start.md` or exam |
| 6 | Paper labs | GL-01, GL-02, GL-06, GL-10, GL-20, UL-01 from JSON **after** UI lab card review | retain in `01-college-it-student.md` |

## Deliverables

- Rewrite **`reports/01-college-it-student.md`**: Evaluation Scope must cite UI journey files; findings updated only where UI adds evidence; mark **Supersedes** prior API-only attempt batch.
- **`reports/evidence/STUDENT/evidence-log.md`**: EV rows with type `UI` and quoted on-screen text (≤30 words).
- **`reports/evidence/STUDENT/db-actions.md`**: one row per UI attempt with question id + choice + outcome if visible.
- Append **Evaluation Integrity** note to `reports/00-evaluation-summary.md` (Student redo + DB restore).
- Amend parent plan §18 checklist: Student UI re-review item checked when done.

## Acceptance

- ≥30 exam attempts logged with `(UI)` and browser snapshot or `ui-journey/exam.md` timestamps.
- All four primary tabs visited in the student tab in order: start → labs → coverage → exam (order may interleave after first pass).
- No `POST /api/attempts` except via UI button (network may be spot-checked in exam journey notes).
- DB fingerprint equals baseline after final restore.

## Risks

- Exam sidebar has 429 cards: use module filters to limit scope while hitting 30 attempts.
- Session time: batch clicks per module (A0=2, then A1 module filter + sequential cards).
