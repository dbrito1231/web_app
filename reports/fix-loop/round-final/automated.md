# Final gate — automated checks (2026-09-25)

| Check | Result |
|---|---|
| `python manage.py test workbook` | **11 OK** (includes Origin CSRF POST and rationale-absent GET) |
| `python scripts\content_lint.py` | **PASS** (drillIds, template-stem ban, MC key share ≤45%) |
| `python scripts\scan_lab_placeholders.py` | **PASS** (41 labs; unset teardown vars are errors) |
| `npx eslint src` | **exit 0** |
| `npm run build` | **OK** |
| `terraform fmt -check` and `terraform validate` in `lab-fixtures/gl-20` | **valid** |
| Dotted `q-saa-N.N-` drillIds | **none** |
| `CSRF_TRUSTED_ORIGINS` | set from `CORS_ALLOWED_ORIGINS` |

Six role reports for this round are written beside this file as they finish.
