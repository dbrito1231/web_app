# Fix-loop gate — PYTHON (round-final)

Role: Python  
Workspace: `C:\Users\dbadmin\Desktop\GitServ\ccna\web_app`  
Date: 2026-09-25  
App code: not modified

## Command

From `backend/` with `.venv` activated:

```powershell
python manage.py test workbook
```

## Suite result

```
Found 11 test(s).
System check identified no issues (0 silenced).
...........
Ran 11 tests in 0.108s

OK
```

Exit code: **0**

## Issue verdicts

| ISS | Claim | Verdict | Evidence |
|-----|--------|---------|----------|
| ISS-001 | `test_post_with_vite_origin_and_csrf` | **Gone** | Test present and **PASS**. `CSRF_TRUSTED_ORIGINS = list(CORS_ALLOWED_ORIGINS)` in `backend/config/settings.py`. Client POSTs `/api/attempts` and `/api/labs/gl-01/checkpoints` with `HTTP_ORIGIN=http://127.0.0.1:5173` and CSRF token → 200 / 200–204. |
| ISS-003 | `public_question` pops rationale; `test_question_hides_answer_key` | **Gone** | `public_question` pops `correctAnswerIds` and `rationale`. `test_question_hides_answer_key` asserts both absent on GET → **PASS**. Attempt POST still returns `rationale` (`test_attempt_returns_rationale` **PASS**). |
| ISS-060 | `selectedIds` unknown choice returns 400 | **Gone** | `views.py` rejects ids not in question choice set with 400. `test_attempt_rejects_unknown_choice` posts `["not-a-choice"]` → **400 PASS**. |
| ISS-061 | DEBUG / SECRET_KEY local-only | **By-design** | Unchanged: `DEBUG = True`, `SECRET_KEY = "django-insecure-local-workbook-dev-only"`, hosts limited to localhost / 127.0.0.1 / testserver. Acceptable for local-only workbook scope; not treated as a defect. |

## New issues (Low+)

No new issues
