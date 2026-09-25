# PYTHON.md — Senior Python Developer, fix-loop round 2 (team review)

> Intended path: `reports/fix-loop-r2/round-2/PYTHON.md`. Plan mode was active for this reviewer, so the
> report could not be written there; this is the full text for Lead Dev to record verbatim.

Scope: `git diff 925b619 8789bf5 -- backend scripts` (content_loader.py, views.py, test_scoring_and_api.py,
scan_lab_placeholders.py). Read-only. Only GET requests were made to the running backend.

## Verdicts

| Item | Verdict | Evidence |
|---|---|---|
| O10 — corrupt content JSON gives clear JSON 500 | **Partially fixed** (Probable concern, Medium) | `_read_json` (content_loader.py:20-29) converts only `json.JSONDecodeError`. Every content route now catches `ContentParseError`: catalog (views.py:71-75), summary (78-85), lesson (88-95), question (98-106), attempts POST (130-135), lab (169-178), readiness (247-253), coverage (256-268, own inline handler). Still unguarded (HTML Django debug 500, DEBUG=True): (a) non-UTF-8 file → `UnicodeDecodeError` from `json.load` is a ValueError but not JSONDecodeError, so it escapes `_read_json` and `coverage_registry`; (b) valid JSON of the wrong shape (`[]`, `null`, `"x"`) → `AttributeError` in `lesson_index`/`lab_index`/`exercise_index`/`question_catalog` (`.get`), `create_attempt` (views.py:137), or `ValueError/TypeError` in `public_question`/`public_lab` (`dict(list)`), which run **outside** the try in `question_detail` (106) and `lab_detail` (178); (c) `saa_objective_domain_map` (content_loader.py:169) `row["id"]` KeyError on a malformed objective row → readiness HTML 500. Routes that load no content (checkpoints, progress, export, import, reset, health) are N/A. |
| ISS-060 — unknown choice → 400; corrupt JSON → bare 500 | **Unknown-choice part: Gone** (views.py:137-139, covered by `test_attempt_rejects_unknown_choice`). **Corrupt-JSON part: same as O10 — Gone for JSON syntax errors, open for encoding / wrong-shape files.** Recommend keep ISS-060 open (or close with PY-R2-2-001 as follow-up). | |

## New issues (Low+)

| ID | Tag | Sev | Evidence | Detail / recommendation |
|---|---|---|---|---|
| PY-R2-2-001 | Confirmed defect | Medium | content_loader.py:`_read_json`:23-29; views.py:`coverage_registry`:261-268 | Only `JSONDecodeError` is converted. A file saved as UTF-16/cp1252 (plausible on Windows: PowerShell 5.1 `Set-Content` default is ANSI) raises `UnicodeDecodeError` → HTML traceback 500. Fix: `except (json.JSONDecodeError, UnicodeDecodeError)` in both places; better, make `coverage_registry` call `_read_json` instead of duplicating it. |
| PY-R2-2-002 | Probable concern | Medium | views.py:`question_detail`:106, `lab_detail`:178, `create_attempt`:137; content_loader.py:`lesson_index`:88, `lab_index`:102, `exercise_index`:130, `question_catalog`:71 | Valid-JSON-wrong-type files crash with non-JSON 500. `_read_json` claims `-> dict` but never checks. Fix: in `_read_json`, `if not isinstance(data, (dict, list))` / per-loader `isinstance(data, dict)` → raise `ContentParseError("… top-level must be an object")`. (Objectives files are lists, so the check must be per-loader.) |
| PY-R2-2-003 | Confirmed defect (scanner) | **High** (it masked a cost-risk content bug) | scan_lab_placeholders.py:`scan_file`:53 | `assigned` is computed by regex `\$X\s*=` over the **whole file blob, teardown included**. So `$X = $null` in the teardown satisfies the check. Measured: GL-01 (`$BoundaryArn`), GL-06 (10 vars), GL-08 (11 vars) pass only via teardown `$null` lines; UL-05/06/07/08/09/10/11/12/14/16 null every resource var. In UL-05 the deletes are **unguarded** (`aws ec2 delete-vpc --vpc-id $VpcId` after `$VpcId = $null`), so they run with empty IDs and fail; nothing is deleted. This matches uncommitted plan Amendment 1 N2a/N2b — confirmed independently. Fix as planned: count assignments only from `steps`, fail on any teardown `= $null`. |
| PY-R2-2-004 | Confirmed defect (scanner) | Medium | scan_lab_placeholders.py:`scan_file`:75 (`if steps:`) | The unset-variable rule is skipped for every lab with no steps, i.e. all 20 `ul-*` labs. Combined with 003, UL teardowns are effectively unchecked for variables. UL-20 uses `$Bucket`/`$Suffix` with no assignment anywhere (whitelisted at 62-73). Fix: run the rule for UL labs against the planned `# Uses …` header instead of `steps`. |
| PY-R2-2-005 | Probable concern | Low | scan_lab_placeholders.py:62-73 | Global whitelist (`Bucket`, `Suffix`, `AccountId`, …) exempts those names in every lab, so an unassigned `$Bucket` in a teardown never fails. Scope the whitelist per lab or require an explicit prompt/assignment. GL-01 teardown uses `$AccountId` (budgets delete) with no assignment — passes only via whitelist. |
| PY-R2-2-006 | Probable concern | Low | content_loader.py:`lab_index`:103-112 vs frontend/src/utils/progress.ts:`labChecklist`:11-17 | Backend drops non-dict / id-less steps and does **not** fall back to acceptanceCriteria when `steps` is non-empty but yields no ids; frontend uses `lab.steps` as-is. Header stats (backend `stepIds`) and the lab card (frontend) can disagree. Non-list truthy `steps` (string/dict) iterates chars/keys → `[]`; string `acceptanceCriteria` → one `cNN` per character. Current content: 0 labs hit these shapes (script over 42 labs). Recommend a content_lint rule (steps is list of dicts with unique `id`; criteria is list of str) rather than more loader code. |
| PY-R2-2-007 | Recommendation | Low | test_scoring_and_api.py:`test_question_get_returns_json_500_for_corrupt_file` | Route test patches `workbook.views.load_question`; it never goes through the real loader + view. Use `override_settings(CONTENT_ROOT=tmpdir)` with a real `questions/q-bad.json` containing `{`, and parametrize over all 8 content routes (summary, catalog, lesson, question, lab, attempts POST, readiness, coverage). Add cases for UTF-16 bytes and top-level `[]`. Also wrap in `assertLogs("workbook.views", "ERROR")` — the log line currently leaks to test stderr (see output). |
| PY-R2-2-008 | Recommendation | Low | tests (none) | Untested: `lab_index` / `exercise_index` / enriched `lesson_index` fields and the criteria fallback (`c01`…); `coverage_registry` corrupt path; readiness corrupt path; `scan_lab_placeholders.py` (no test at all — a fixture test would have caught 003). |
| PY-R2-2-009 | Probable concern | Low | content_loader.py:`content_summary`:142-159 | No caching: each call reads and parses 23 lessons + 42 labs + 60 exercises + 2 objective files (≈127 files). Measured GET /api/content/summary: 200, 84,311 B, ~30 ms (3 runs). Called twice on the Start here path (useWorkbookBootstrap.ts:87 and StartHereTab.tsx:78). Acceptable for a local app; if it grows, cache on a dir-mtime key. Do **not** use a bare `lru_cache` (see 010). |
| PY-R2-2-010 | Probable concern | Low | content_loader.py:162-179 (`@lru_cache`) | Pre-existing, relevant to O10: objective maps are cached for the process lifetime. A corrupt objectives file introduced after the first success is not detected; a fixed file after a failure is fine (exceptions are not cached). Content edits need a server restart for readiness. Informational for the fix loop. |
| PY-R2-2-011 | Recommendation | Informational | views.py:`_content_error`:48-50; content_loader.py:12 | `logger.error` without `exc_info` loses the cause; use `logger.exception` or `exc_info=exc.__cause__`. `ContentParseError(ValueError)` would be swallowed as a 400 by any broad `except ValueError` (e.g. the pattern in `import_view`:230) if content loading is ever added there — keep in mind. `content_summary_view` (82-83) still returns `str(FileNotFoundError)`, i.e. an absolute path, in the 500 body (pre-existing, local-only). |

## Checked and fine

- All 8 content-loading routes have an `except ContentParseError` clause; handler returns `JsonResponse` 500 with `path.name` only (no absolute path).
- `exercise_index` handles a missing directory (redundant `is_dir` check, harmless).
- `lab_index` criteria IDs (`c{index+1:02d}`) match frontend `labChecklist` (`c` + padStart 2).
- Scanner now includes GL-01 (`paths` computed once; count message fixed). `python scripts/scan_lab_placeholders.py` → `PASS 42 labs scanned` — but see 003/004: PASS is not meaningful for teardown variables yet.

## Test output

`cd backend; $env:PYTHONDONTWRITEBYTECODE=1; .\.venv\Scripts\python.exe manage.py test workbook -v 2`

```
test_attempt_rejects_unknown_choice ... ok
test_attempt_returns_rationale ... ok
test_catalog_omits_rationale ... ok
test_lab_hides_solution_until_reveal ... ok
test_post_with_vite_origin_and_csrf ... ok
test_question_hides_answer_key ... ok
test_loader_rejects_corrupt_json ... ok
test_question_get_returns_json_500_for_corrupt_file ... Corrupt content file: Content file q-bad.json is not valid JSON: Expecting value (line 1)
ok
test_import_rejects_future_schema ... ok
test_reset_requires_confirm_token ... ok
test_insufficient_evidence_by_default ... ok
test_mc_all_or_nothing_correct ... ok
test_mr_all_or_nothing_partial_wrong ... ok
----------------------------------------------------------------------
Ran 13 tests in 0.100s
OK
System check identified no issues (0 silenced).
```
