# Fix-loop gate — IT Manager (round-final)

Workspace: `C:\Users\dbadmin\Desktop\GitServ\ccna\web_app`  
Role: IT Manager (read-only attestation). No app code edited.  
Evidence date: 2026-09-25. Cross-check: `reports/fix-loop/round-final/automated.md` (11 Django tests OK; CSRF origins set).

---

## Gate checklist

### ISS-001 — Progress can be saved (`CSRF_TRUSTED_ORIGINS` present) — **Gone**

`backend/config/settings.py` sets:

> `CSRF_TRUSTED_ORIGINS = list(CORS_ALLOWED_ORIGINS)`

Live settings load shows Vite origins trusted: `http://127.0.0.1:5173`, `http://localhost:5173`, and `:5174` variants. Regression: `test_post_with_vite_origin_and_csrf` POSTs `/api/attempts` and a GL-01 checkpoint with `HTTP_ORIGIN` + CSRF token. CR-0006 / WP1 closed for this defect.

### ISS-003 — Rationales not on question GET — **Gone**

`public_question` strips `rationale` (and answer keys). `GET /api/questions/<id>` returns via `public_question`. Sample `q-a0-mc-001` public payload has no `rationale`. Attempt POST still returns rationale after score. Tests: `test_question_hides_answer_key`, `test_attempt_returns_rationale`. CR-0007 / WP2.

### ISS-040 — Lessons listed on Start here — **Gone**

`StartHereTab.tsx` loads `summary.lessons` into a lesson `<select>` (not A0-only). Content summary reports **23** lesson ids (`a0-lab-safety`, `lesson-1-1`, …). CR-0012 / WP7 done; Teacher approved Start here lesson picker.

### ISS-080 — Sandbox note in `docs/labs-and-safety.md` — **Gone**

Section **Company sandbox (if you run labs at work)** present:

> Use a sandbox account or OU, not a production account. Budget alerts warn only; they do not stop spend. Tear down the same day. Do not treat this workbook's progress file as an audit record of who completed training.

CR-0016 / WP11 (docs portion); Teacher approved the sandbox note.

### ISS-081 — Audit-grade metrics — **By-design** (not a regression)

Multi-user / audit-grade completion metrics remain **out of scope** under KISS and intended local workbook design (single SQLite progress; export is personal backup, not attestation). CR-0016 Teacher note: audit-grade multi-user metrics stay out of scope. Readiness remains self-study signal only. Rationale-leak half of original ITMGR-201 is addressed under ISS-003; the audit-platform ask was never in product scope and was not reintroduced as a bug.

---

## Summary

| Item | Verdict |
|------|---------|
| ISS-001 CSRF / progress save | Gone |
| ISS-003 rationale off question GET | Gone |
| ISS-040 lessons on Start here | Gone |
| ISS-080 sandbox note in labs-and-safety | Gone |
| ISS-081 audit-grade metrics | By-design (out of scope; not regression) |

---

## Go / no-go

**Go** for this IT Manager gate: Critical save-path and answer-prefetch defects that blocked workforce progress and exam integrity are remediated; learners can reach the lesson catalog from Start here; corporate sandbox / non-audit wording is on the labs safety doc; and audit-grade L&D metrics correctly remain a deliberate non-goal rather than an unfinished regression. This attestation covers only the five items above—not every remaining curriculum or UX open item outside this checklist.

No new issues
