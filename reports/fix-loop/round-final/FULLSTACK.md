# Fix-loop gate — FULLSTACK (round-final)

Role: Full-Stack  
Workspace: `C:\Users\dbadmin\Desktop\GitServ\ccna\web_app`  
Date: 2026-09-25  
App code: not modified

## Command

From `frontend/`:

```powershell
npx eslint src
```

Exit code: **0** (clean).

## Issue verdicts

| ISS | Claim | Verdict | Evidence |
|-----|--------|---------|----------|
| ISS-001 | `client.ts` plain 403 text + CSRF setting | **Gone** | `backend/config/settings.py:26` — `CSRF_TRUSTED_ORIGINS = list(CORS_ALLOWED_ORIGINS)`. `frontend/src/api/client.ts:17-22` attaches `X-CSRFToken` on non-GET/HEAD; `:37-40` maps non-JSON **403** to `"Your answer couldn't be saved — the app's server refused the request"`. |
| ISS-003 | Exam drills show `result.rationale`, not `question.rationale` | **Gone** | `ExamDrillsTab.tsx:320` renders `{result.rationale}` inside the post-submit block (`:311-326`). No `question.rationale` read in the UI. Backend `public_question` also pops rationale (`content_loader.py:48`). |
| ISS-050 | Catalog (not N+1), unknown slug redirect, MR `selectCount` gate, mock copy, `aria-live`, lab load error, `bestByQuestion` | **Gone** | See checklist below. |

### ISS-050 checklist

| Criterion | Verdict | File:line |
|-----------|---------|-----------|
| Catalog endpoint instead of N+1 question GETs | **Gone** | `ExamDrillsTab.tsx:38-39` → `api.questionCatalog()`; `client.ts:58-59` → `/api/content/catalog`. Active question still one `api.question(id)` (`:84`). |
| Unknown slug redirects | **Gone** | `App.tsx:31-35` — `navigate('/labs', { replace: true })` when `tabSlug` not in `PATH_TO_TAB`. |
| MR `selectCount` disables submit | **Gone** | `ExamDrillsTab.tsx:143-144`, `:290` — `disabled={selected.size !== Number(selectCount) \|\| loading}`. |
| Mock card copy | **Gone** | `ExamDrillsTab.tsx:222-234` — disabled card; title/copy say set shipped / timed runner not in build (no “Phase 4 Locked”). |
| `aria-live` on feedback | **Gone** | `ExamDrillsTab.tsx:312-315` — `role="status"` + `aria-live="polite"`. |
| Lab load error surfaced | **Gone** | `useWorkbookBootstrap.ts:22,55-59` sets `labLoadError`; `App.tsx:82-86` renders it with `role="alert"`. |
| `bestByQuestion` from progress | **Gone** | `ExamDrillsTab.tsx:40,51` — `api.progress()` then `setBestScores(progress.bestByQuestion)`. |

## New issues (Low+)

| ID | Severity | Location | Note |
|----|----------|----------|------|
| FS-FINAL-001 | Medium | `useWorkbookBootstrap.ts:76` (`reloadLabs(sum.labs)`), `:41-60` | WP8 also called for **lazy** lab load. Failures are no longer silent, but bootstrap still parallel-GETs every lab id on every cold start. |
| FS-FINAL-002 | Low | `LabCard.tsx:123-134` | Disclosure `role="button"` / `aria-expanded` still has no concise `aria-label` (residual FULLSTACK-210). |

No other Low+ findings from this pass (`eslint` clean; gate checklist items Gone).

**Lead Dev follow-up:** FS-FINAL-001 labs load only when the Labs tab is open (`App.tsx` `ensureLabs`). FS-FINAL-002 lab card header has `aria-label`. Exam-first load issued 0 `/api/labs/` requests; opening Labs then issued 42, and the first card name was `GL-01. GL-01 — Identity, budget, and preflight`.
