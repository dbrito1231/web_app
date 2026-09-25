# Student re-check — fix-loop round-final

Role: College IT Student  
Workspace: `C:\Users\dbadmin\Desktop\GitServ\ccna\web_app`  
Checked: 2026-09-25  
UI method: Cursor browser MCP failed (no tab); used one-shot Playwright against `http://127.0.0.1:5173` (Start / Exam / Labs). One allowed POST: **Check answers** once on `q-a0-mc-001`. Did not click Reset or Import. Did not edit app code. Did not read `reports/archive`.

---

## ISS-001 — save CSRF

**Verdict: Gone**

- Settings quote: `backend/config/settings.py` has `CSRF_TRUSTED_ORIGINS = list(CORS_ALLOWED_ORIGINS)` (includes `http://127.0.0.1:5173`).
- UI: On `/exam`, selected a choice on `q-a0-mc-001`, clicked **Check answers** once → `POST http://127.0.0.1:8000/api/attempts -> 200`. No “couldn't be saved” / Forbidden. Score/explanation rendered (`Incorrect` + rationale + `Objectives: SAA-1.1-K05`).

---

## ISS-003 — rationale not on screen before submit

**Verdict: Gone**

- API quote: `GET /api/questions/q-a0-mc-001` returns stem/choices/module only — no `rationale` key (observed live JSON).
- UI: Before submit, article showed stem and choices only; no Correct/Incorrect and no Objectives block. After Check answers, rationale appeared (`REQ-P03 and REQ-L30: the learner runs CLI locally…`).

---

## ISS-004 — lesson drill links

**Verdict: Gone**

- File quote (`content/lessons/lesson-1-2.json`): `drillIds` are hyphenated (`q-saa-1-2-k01-mc`, …) — no dotted `q-saa-1.2-…`.
- Spot-check: all `lesson-*.json` drillIds resolve to existing `content/questions/*.json` files (0 missing; 0 dotted SAA ids). `content_lint.py` PASS.

---

## ISS-010 — template stems

**Verdict: Still present**

- Banned lint skeleton is gone (`Which statement best reflects this exam objective` count = 0; lint PASS).
- Student experience still templated. File quote (`content/questions/q-saa-1-1-k01-mc.json`):

  > `"stem": "A design review asks how you would handle this requirement: Access controls and management across multiple accounts Which action matches that requirement?"`

- ~226 stems share that “A design review asks…” opening; ~156 MR stems share “Select TWO actions that support this requirement: …”. Choices often mirror the objective text (“Apply the objective directly: …”). Not exam-realistic drill practice.

---

## ISS-020 — lab followability (GL-08 user-data; UL-01 / GL-03 text)

**Verdict: Still present** (UL-01 part fixed; GL-08 still awkward to follow from the Labs UI)

- **UL-01 / GL-03 — Gone.** UI on Labs after search `ul-01`: “Finish GL-01 first. GL-03 is optional for the bucket check.” Criteria includes optional path: “If you already completed GL-03, list that bucket read-only; otherwise…”
- **GL-08 user-data — Still present for followability.** JSON/API has a real newline inside `--user-data "#!/bin/bash\npython3 -m http.server 80"`. On `/labs` the step bullet collapses to a single line in the page text students copy:

  > `--user-data "#!/bin/bash python3 -m http.server 80"`

  That one-liner is not a valid two-line user-data script when pasted as shown. Hourly cost-risk gate on GL-08 is fine; the copy/paste of user-data is the blocker.

---

## ISS-040 — lessons reachable on Start here

**Verdict: Gone**

- UI: `/start` lesson `<select>` has **23** options including `a0-lab-safety`, `lesson-1-1`, `lesson-1-2`, … `lesson-tf-g8`.
- Matches `GET /api/content/summary` `lessons` list. Switching the picker loads lesson body (markdown).

---

## ISS-050 — exam UX

**Verdict: Gone** (for the WP8 UX defects I can see as a student)

- `/exam` loads catalog (~430 cards), module aside with `aria-label="Exam drill modules"`, stem + radio/checkbox choices, **Check answers** works (see ISS-001).
- Mock exam card is present, **disabled**, copy: “Set shipped; timed runner not in this build / Not runnable” — honest, not a fake runnable control.
- Bad-tab routing not re-broken in this pass (`/start` and `/exam` both render).

---

## New issues (Low+)

1. **Medium — drill bank still feels generated (same as ISS-010 residual).** Hundreds of stems share one scenario frame; keeping ISS-010 Still present rather than opening a duplicate ID.
2. **Low — Start here lesson picker shows raw ids** (`lesson-1-2`) instead of lesson titles, so browsing the catalog is harder than it needs to be.
3. **Low — lesson `drillIds` are API-only.** Start here shows lesson prose but does not list or deep-link the related drills (e.g. A0’s `q-a0-mc-001` / `q-a0-mr-001`), so “study then drill” is still a manual hop to Exam drills.

No other new Low+ findings beyond the above and the ISS-020 GL-08 copy issue.

**Lead Dev follow-up:** GL-08 user-data is now a here-string written to `user-data.sh`, then `--user-data file://user-data.sh`, so the Labs list does not collapse the script onto one line. The 226 “A design review asks…” stems were split across eight different openings. The Start here picker shows lesson titles, and each lesson lists drill links to `/exam?q=<id>`.
