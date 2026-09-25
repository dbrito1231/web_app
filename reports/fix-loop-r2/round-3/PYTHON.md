# PYTHON.md: Senior Python Developer, fix-loop round 3

Scope: `1c68079` (loader/views), `bbb05de` (scanner rewrite and fixture tests), `git diff 925b619 HEAD -- backend`.
Read-only review. No servers were started, no POSTs were sent, and no repo files were edited except this report.
I ran the adversarial probes from a scratchpad script that imports `scan_lab()` directly. It did not touch repo content.

## Verdicts (round-2 items)

| Item | Verdict | Evidence |
|---|---|---|
| PY-R2-2-001 non-UTF-8 → HTML 500 | **Gone** | content_loader.py:30-33 catches `UnicodeDecodeError` and raises `ContentParseError`. `coverage_registry` now goes through `load_coverage_registry` (content_loader.py:64-65, views.py:256-264), so the duplicate reader is gone. Test: `utf16` subTest (test_scoring_and_api.py:166). |
| PY-R2-2-002 wrong-shape top level → HTML 500 | **Gone (top level)**, with a residual (see PY-R3-001) | `_read_json(path, expect)` (content_loader.py:20, 34-38). Lessons, questions, labs and coverage use `dict` (53-65), exercises use `dict` (144), objectives use `list` (166, 169, 182, 192). Test: `wrong-type` subTest (`[]`). Shapes **inside** a valid object can still crash. |
| PY-R2-2-003 `$X = $null` in teardown satisfied the check | **Gone** | scan_lab_placeholders.py:32 excludes `rhs == "$null"`, :70-71 fails any teardown `= $null`, and :88 counts assignments only from steps. Teardown lookups count only for later lines (:105). Test: `test_null_reset_is_not_an_assignment`. Bypass variants remain (PY-R3-003). |
| PY-R2-2-004 UL labs skipped the variable rule | **Gone** | The rule now runs for every lab (:88-105). UL labs need a `# Uses:` header (:77-82) and an `if (...)` guard for declared vars (:97-103). Test: `test_unguided_needs_header_guards_and_own_names`. Guard quality is covered in PY-R3-002. |
| PY-R2-2-005 global whitelist (`Bucket`, `Suffix`, `AccountId`) | **Gone** | The whitelist is replaced by `AUTOMATIC` (:24), which holds PowerShell automatics only. GL-01 `$AccountId` and `$BoundaryArn` are now satisfied only by step prose (`PROSE_ASSIGN`, :19; both bullets are genuine). UL-20 declares `$Suffix`/`$Bucket` in `# Uses:` and guards them. |
| PY-R2-2-007 route test mocked the loader | **Gone** (minor gap) | test_scoring_and_api.py:164-197 uses `override_settings(CONTENT_ROOT=tmp)` with real files (syntax, UTF-16, `[]`) on 6 GET routes, wrapped in `assertLogs`, so stderr is clean. It does not cover `POST /api/attempts` or `GET /api/readiness`. The code paths are guarded (views.py:130-135, 249-252) but untested (PY-R3-007). |
| N5 scanner fixture tests | **Done** | backend/workbook/tests/test_lab_scan.py (6 tests, all pass). Coverage gaps are listed in PY-R3-006. |

## Scanner rewrite review

The probe cases below were run against `scan_lab()`. PASS means the scanner reports no problem.

| Probe teardown / steps | Scanner | Should be |
|---|---|---|
| UL `if ($true -or $VpcId) { aws ec2 delete-vpc --vpc-id $VpcId }` | PASS | fail (always-true guard) |
| UL `if (-not $VpcId) { aws ec2 delete-vpc --vpc-id $VpcId }` | PASS | fail (inverted guard: runs only when the ID is empty) |
| UL `if ($VpcId) { } aws ec2 delete-vpc --vpc-id $VpcId` | PASS | fail (delete is outside the guard block) |
| UL `if ($VpcId -and $SubnetId) { ...$VpcId }; aws ec2 delete-subnet --subnet-id $SubnetId` | PASS | fail (second statement unguarded) |
| UL guard `if ($VpcIdOld) {...}` on a line that also uses `$VpcId` | PASS | fail (`"$VpcId" in "$VpcIdOld"` is a substring test, :101) |
| UL `$VpcId = $VpcId` or `$VpcId = ''`, then an unguarded delete | PASS | fail (the self or empty assignment counts as a lookup, :32/:105) |
| UL `aws ec2 delete-vpc --vpc-id ${VpcId}` (braced variable) | PASS | fail (`VAR_REF` at :15 does not see `${...}`) |
| UL teardown = `# Uses:` header plus only comment lines | PASS | fail (a teardown that deletes nothing) |
| GL empty teardown | PASS | fail |
| GL teardown `Write-Host "$VpcId = gone"` then a delete | PASS | fail (text inside a string counts as an assignment) |
| GL steps `$VpcId = $null;` | PASS (counts as set) | not set (`rhs` is `$null;`, :16/:32) |
| GL steps "Look into `$VpcId` later." or "Set `$VpcId` when you have it." | PASS | debatable (PY-R3-005) |
| `aws ... -erroraction SilentlyContinue`, `-EA`, `aws.exe ... -ErrorAction` | PASS | fail (false negatives, PY-R3-004) |
| Steps: bullet 1 `aws sts ...`, bullet 2 `Remove-Item Env:X -ErrorAction ...` (same step) | **FAIL** | pass (false positive, PY-R3-004) |
| Steps: "Configure the aws CLI, then `Remove-Item x -ErrorAction Stop`" | **FAIL** | pass (false positive) |
| Teardown `aws s3 rb ...; Remove-Item f -ErrorAction SilentlyContinue` | PASS | pass (correct: `;` splits the segments) |
| Teardown `$vpcid` when the steps set `$VpcId` | **FAIL** | pass (PowerShell names are case-insensitive) |
| Teardown `Remove-Item $PWD/out.json` | **FAIL** | pass (`AUTOMATIC` has `pwd`, not `PWD`) |
| UL `If ($VpcId) { ... }` | **FAIL** "not guarded" | pass (`if` is matched case-sensitively, :99) |
| UL `$VpcId = $NULL` | FAIL, but for the wrong reason ("uses $NULL but nothing sets") | fail as a `$null` reset (:70 is case-sensitive) |
| Duplicate line that differs only in whitespace | PASS | fail (low value) |

**Current content:** I checked all 42 labs for inverted or constant guards, `${}`, `-EA`, lowercase `-erroraction`, `If (`, empty-string resets, and statements after a guard's closing brace. **None were found.** The only teardowns with no `aws ... delete`-style call are GL-20 and UL-20. Both use `terraform destroy`, which is correct. UL-19 has statements after a `}`, but they are inside `foreach` or `if` blocks that name fixed `workbook-ul19` resources, so they are fine. The bypasses above are therefore **latent**. Today's PASS is honest, but the scanner can still be fooled by future edits.

**`-ErrorAction` segment rule:** it is correct for teardown lines. `Remove-Item` on the same line as `aws` is fine when the two are separated by `;`, `|`, `{` or `}`. For steps, the scanner splits `json.dumps(steps)` (:49, :63), and bullets inside one step are joined by `", "`, which has no split character. So any step where one bullet mentions `aws ` (even in prose) and another bullet uses `-ErrorAction` on a cmdlet is a false positive. No lab has any `-ErrorAction` today (grep of content/labs is empty after CR-0017 batch A), so the false positive is latent. It will, however, block legitimate cmdlet use in steps.

**Prose regex:** see PY-R3-005.

**Fixture tests:** they are meaningful for the round-2 regressions. `test_null_reset_is_not_an_assignment` would have caught PY-R2-2-003, and the UL test would have caught PY-R2-2-004. They do not exercise the guard's content, prose assignment, `foreach`, multi-bullet steps, or `main()`. Details are in PY-R3-006.

## New issues

| ID | Tag | Sev | File:line | Detail |
|---|---|---|---|---|
| PY-R3-001 | Probable | Low | views.py:137; content_loader.py:183, 193; readiness.py:47-60 | Crashes on the shape **inside** a file still give an HTML 500. `"choices": "ab"` (or a list of strings) leads to `choice.get` → `AttributeError` in `create_attempt`. An objectives row that is missing `id`/`domain_id`/`group`, or is not a dict, leads to `KeyError`/`TypeError` in `saa_objective_domain_map`/`terraform_objective_group_map`. `readiness_metrics` catches only `ContentParseError` (views.py:251). This only triggers once attempts exist, because the maps are built per attempt. Also, `objectiveIds` given as a string is iterated character by character, which gives silently wrong results rather than a crash. Fix: validate row shape in the map builders and raise `ContentParseError`, or add content_lint rules for choices and objective rows. |
| PY-R3-002 | Confirmed (scanner) | Medium | scan_lab_placeholders.py:99-103 | The UL guard check is textual only. It accepts always-true guards (`$true -or $X`), inverted guards (`-not $X`, `!$X`, `-eq $null`), statements after the guard block closes (`if ($X) { } aws ... $X`, `}; aws ... $Y`), and prefix-name matches (`$VpcIdOld` covers `$VpcId` via the substring test at :101). Fix: require the whole command after the guard to sit inside one balanced `{...}` that ends the line. Match guard vars with a `\$Name\b` regex, not `in`. Reject `-not`, `!`, `-or`, `$true` and `-eq $null` inside the guard. |
| PY-R3-003 | Confirmed (scanner) | Medium | scan_lab_placeholders.py:16, 32, 70, 105 | The `$null` rule can be bypassed. `$X = ''`, `$X = ""`, `$X = $X`, `$X = $NULL`, and `"$X = ..."` inside a string all count as assignments. Only the exact lowercase `$null` is rejected, and `$X = $null;` in steps counts as set because `rhs` includes the `;`. The scanner also does not fail a teardown that has no non-comment lines, or an empty teardown. Fix: strip trailing `;` from `rhs`, compare case-insensitively, and treat `''`, `""`, `$null` and a self-reference as resets. Ignore matches inside quotes. Require at least one non-comment teardown line. |
| PY-R3-004 | Confirmed (scanner) | Low | scan_lab_placeholders.py:21, 49, 63-66 | The `-ErrorAction` rule has false positives and false negatives. False positives: on steps, the whole `json.dumps(steps)` is split only on `;{}|`, so separate bullets join and prose "aws " matches. False negatives: `-erroraction` (case), the `-EA` alias, and `aws.exe`. Fix: scan each bullet (or each backtick code span) separately, and use `(?i)-(ErrorAction\|EA)\b` and `\baws(\.exe)?\s`. |
| PY-R3-005 | Probable (scanner) | Low | scan_lab_placeholders.py:19, 88 | `PROSE_ASSIGN` is too loose. Any "Set `$X`" or "... into `$X`" counts as an assignment, including "look into `$X`" or "Set `$X` later", even when no command produces the value. Today only GL-01 (`$AccountId`, `$BoundaryArn`) depends on it, and both of those bullets are genuine. Fix: narrow the pattern to the phrasings actually used (`Copy ... into `$X``, `Set `$X` to`), or require a code assignment in the same step. |
| PY-R3-006 | Recommendation | Low | scan_lab_placeholders.py:15, 24, 70, 99; test_lab_scan.py | The scanner is case-sensitive where PowerShell is not. `$vpcid` vs `$VpcId`, `$PWD`/`$Null` versus `AUTOMATIC`, and `If (` all produce false positives, and `${Var}` is not seen at all. Fix: use `re.I` for the guard and `$null` checks, compare names with `.lower()`, and add `\$\{(\w+)\}`. Tests to add: prose assignment, `foreach` vars, a multi-bullet `-ErrorAction` false positive, the ENI/VPC rules, `main()` exit code and a non-dict file, and the bypass probes above once 002-004 are fixed. |
| PY-R3-007 | Recommendation | Informational | test_scoring_and_api.py:164-197; views.py:48-50, 82-83; content_loader.py:176-193 | Add `POST /api/attempts` (CSRF client) and `GET /api/readiness` to the corrupt-file route test. Round-2 items 009, 010 and 011 are unchanged and still informational: no summary cache, `lru_cache` staleness, `logger.error` without `exc_info`, and the `str(FileNotFoundError)` absolute path in the summary 500. |

**`git diff 925b619 HEAD -- backend`:** no new bug found. The diff covers content_loader.py, views.py, test_scoring_and_api.py and test_lab_scan.py.
- `expect` defaults to `None`, and every caller passes a type.
- The `coverage_registry` 404 and 500 paths are both preserved.
- `lab_index` ids still match the frontend `c01` format.
- `ContentParseError` is still a `ValueError` subclass. No content loading happens inside `import_view`'s broad `except ValueError`, so this is still fine.

## Command output

`backend\.venv\Scripts\python.exe scripts\scan_lab_placeholders.py`
```
PASS 42 labs scanned
exit=0
```

`backend\.venv\Scripts\python.exe scripts\content_lint.py`
```
questions 429 aws 310 tf 119
labs 21 + 21
lessons 23
PASS
exit=0
```

`cd backend; $env:PYTHONDONTWRITEBYTECODE=1; .\.venv\Scripts\python.exe manage.py test workbook -v 2`
```
Found 19 test(s).
Creating test database for alias 'default' ('file:memorydb_default?mode=memory&cache=shared')...
Operations to perform:
  Synchronize unmigrated apps: messages, staticfiles
  Apply all migrations: admin, auth, contenttypes, sessions, workbook
Running migrations:
  Applying contenttypes.0001_initial... OK
  ... (auth 0001-0012, admin 0001-0003, sessions.0001) OK
  Applying workbook.0001_initial... OK
System check identified no issues (0 silenced).
test_attempt_rejects_unknown_choice (...AttemptApiTests) ... ok
test_attempt_returns_rationale (...AttemptApiTests) ... ok
test_catalog_omits_rationale (...AttemptApiTests) ... ok
test_lab_hides_solution_until_reveal (...AttemptApiTests) ... ok
test_post_with_vite_origin_and_csrf (...AttemptApiTests) ... ok
test_question_hides_answer_key (...AttemptApiTests) ... ok
test_corrupt_files_return_json_500_through_real_views (...ContentParseTests) ... ok
test_loader_rejects_corrupt_json (...ContentParseTests) ... ok
test_import_rejects_future_schema (...ImportResetTests) ... ok
test_reset_requires_confirm_token (...ImportResetTests) ... ok
test_insufficient_evidence_by_default (...ReadinessTests) ... ok
test_mc_all_or_nothing_correct (...ScoringTests) ... ok
test_mr_all_or_nothing_partial_wrong (...ScoringTests) ... ok
test_clean_guided_lab_passes (...LabScanTests) ... ok
test_duplicate_lines_fail (...LabScanTests) ... ok
test_error_action_on_aws_fails_but_cmdlet_is_fine (...LabScanTests) ... ok
test_null_reset_is_not_an_assignment (...LabScanTests) ... ok
test_teardown_lookup_counts_as_assignment (...LabScanTests) ... ok
test_unguided_needs_header_guards_and_own_names (...LabScanTests) ... ok
----------------------------------------------------------------------
Ran 19 tests in 0.135s

OK
Destroying test database for alias 'default' ('file:memorydb_default?mode=memory&cache=shared')...
exit=0
```
The "Corrupt content file" log line no longer leaks to stderr, because `assertLogs` captures it.
