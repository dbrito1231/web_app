# Gate 0 — save failure confirmation (run-2)

**Verdict: Result A — Confirmed.** Paper-feedback mode applies to all roles.

Recorded: 2026-09-25 after DB baseline match; browser tab viewId `72af38`.

## Exam drill — `q-a0-mc-001`

1. Opened `http://127.0.0.1:5173/exam` (question `q-a0-mc-001` visible).
2. Selected answer: "The learner, in their own terminal".
3. Clicked **Check answers** once.

| Field | Value |
|-------|--------|
| Request | `POST http://127.0.0.1:8000/api/attempts` |
| Request `Origin` | `http://127.0.0.1:5173` |
| HTTP status | **403 Forbidden** |
| UI `[role=alert]` | `Forbidden` |
| Response body (excerpt) | `CSRF verification failed. Request aborted.` |
| Django reason (excerpt) | `Origin checking failed - http://127.0.0.1:5173 does not match any trusted origins.` |

**Not** the custom guard text `Origin not allowed` from `LocalOriginGuardMiddleware` (that applies when Origin is outside `CORS_ALLOWED_ORIGINS`; here Origin is allowed for CORS but missing from `CSRF_TRUSTED_ORIGINS`).

Tool: built-in browser click + CDP `Runtime.evaluate` fetch hook (read-only instrumentation); excerpt ≤30 words in EV-GATE0-001.

## Lab checkpoint — GL-01

1. Opened `http://127.0.0.1:5173/labs` (GL-01 expanded).
2. Clicked checkpoint control **Set the profile and region** (first step).

| Field | Value |
|-------|--------|
| Request | `POST http://127.0.0.1:8000/api/labs/gl-01/checkpoints` |
| Request `Origin` | `http://127.0.0.1:5173` |
| HTTP status | **403 Forbidden** |
| UI `[role=alert]` | `Forbidden` |
| Response body (excerpt) | Same CSRF origin failure text as attempts |

## Configuration note (read-only)

`backend/config/settings.py` defines `CORS_ALLOWED_ORIGINS` for Vite but has **no** `CSRF_TRUSTED_ORIGINS` entry for `http://127.0.0.1:5173`.

## Mode switch

Because saves fail, all drill/lab scoring feedback in the UI is **Needs Verification** until a fix lands. Roles grade keys on paper per plan §4.
