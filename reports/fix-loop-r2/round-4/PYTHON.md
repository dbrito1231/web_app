# PYTHON.md: Senior Python Developer, fix-loop round 4

Scope: `f93c3f1` (scanner rewrite, loader shape validation, lint duplicate-criterion rule, `main()` refactor, 27 new tests). Change log: `reports/fix-loop-r2/amendment-2/impl-F4.md`.

This was a read-only review. I did not start a server, send a POST, run a migration or install, or edit any repo file other than this report.

I wrote two scratchpad scripts:
- `adv_r4.py` runs 50 adversarial probes against `scan_lab()` and re-scans all 42 real labs.
- `loader_r4.py` probes loader shapes in-process against a temporary `CONTENT_ROOT`.

Both scripts are in the session scratchpad, outside the repo.

Note: `git status` shows two uncommitted frontend edits (`frontend/src/components/ExamDrillsTab.tsx`, `frontend/src/styles/app.css`). They are not mine and are out of scope for this review.

## Verdicts (round-3 items)

| Item | Verdict | Evidence |
|---|---|---|
| PY-R3-001 shapes inside files cause an HTML 500 | **Gone (for the reported cases)**, with a residual | content_loader.py:56-77 checks that `choices` is a list of objects and that `objectiveIds`/`correctAnswerIds` are lists. content_loader.py:203-209 and :220-231 check each objective row and raise `ContentParseError`. Tests: test_scoring_and_api.py `test_question_with_bad_choices_shape_raises` and `test_objective_row_missing_fields_raises`. **Residual:** element types are not checked. See PY-R4-010. |
| PY-R3-002 text-only guard check | **Gone (for all round-3 probes)**, but a new bypass exists | `_parse_guard` (scan_lab_placeholders.py:69-94) and `_guard_covers` (:183-204) are bracket-aware. They reject `-or`, `-not`, `$true`, statements after `}`, and prefix names. The same round-3 probes now FAIL, as they should (A01-A03, A05). **New bypass:** a value comparison is accepted as a presence check. See PY-R4-001. |
| PY-R3-003 `$null`-reset bypasses | **Gone (for the listed forms)**; other forms remain | `_is_reset_rhs` (:132-140) handles `''`, `""`, `$NULL`, the trailing `;` and self-assignment. The string-span check is at :143-156. The empty or comment-only teardown check is at :241-245. Remaining bypasses: `${X} = $null`, `[void]($X = $null)`, chained assignment, `Set-/Clear-Variable`, and fake assignments in trailing comments or here-strings. See PY-R4-004, -005 and -006. |
| PY-R3-004 `-ErrorAction` false positives/negatives | **Gone (for the listed cases)** | Checks now run per bullet (:228-233) and per line (:238-239). `(?i)-(?:ErrorAction\|EA)\b` and `aws(\.exe)?` match case-insensitively (:36-37). `-EA:SilentlyContinue` and `& aws` are caught (A39, A40, A42). New gaps: splits inside strings, `&aws`, a quoted or full-path `aws.exe`, `-ErrorAct`. See PY-R4-007. |
| PY-R3-005 loose prose regex | **Gone** | `PROSE_ASSIGN` is narrowed to "Copy ... into `$X`" and "Set `$X` to" (:26-29). Tests cover both directions. |
| PY-R3-006 case-sensitivity / `${}` | **Still present (partly)** | `VAR_REF` handles `${}` (:18), `IF_OPEN` has `re.I` (:39), and `AUTOMATIC` is lowercase (:100). The missing-variable check lowercases names (:278-281). **But** the guard requirement at :286, `learner_vars = used & declared - assigned`, uses sets with the original case, so `$vpcid` skips the guard rule entirely (A11). See PY-R4-002. |
| PY-R3-007 route test gaps | **Gone** | test_scoring_and_api.py:192 adds `/api/metrics/readiness`, and :206-227 adds a CSRF-checked `POST /api/attempts` for all three corrupt-file shapes. Round-2 items 009, 010 and 011 are unchanged and remain Informational (PY-R4-012). |
| TEACHER-R3-001 duplicate criteria (lint) | **Done** | content_lint.py:21-35 and :106-107. Tests: `ContentLintDuplicateCriterionTests`. Scope limits are listed in PY-R4-011. |

## Adversarial results (`scan_lab()`, 50 probes)

"Result" is what the scanner does. PASS means it reported no problem.

**Wrong: 36 of 50.** Of these, 25 PASS when they should fail, and 11 FAIL when they should pass.

| # | Probe | Result | Should | Verdict |
|---|---|---|---|---|
| A01 | UL guard on an unrelated declared var `if ($SubnetId) { ...$VpcId }` | FAIL | fail | ok |
| A02 | UL `if ($VpcId -or $SubnetId)` | FAIL | fail | ok |
| A03 | UL `if ($VpcId) { } elseif ($true) { delete }` | FAIL | fail | ok |
| A04 | UL `if ($VpcId) { delete } else { Write-Host 'skip' }` (legit) | FAIL | pass | **false positive** |
| A05 | UL `switch ($VpcId) { default { delete } }` | FAIL | fail | ok |
| A06 | UL `if ($VpcId -eq '') { delete }` (inverted) | PASS | fail | **bypass** |
| A07 | UL `if ($VpcId -eq "$null") { delete }` | PASS | fail | **bypass** |
| A08 | UL `if ($VpcId -ne 'x') { delete }` (true when `$VpcId` is `$null`) | PASS | fail | **bypass** |
| A09 | UL `if ($VpcId -ne $false) { delete }` (true when `$null`) | PASS | fail | **bypass** |
| A10 | UL `if ($VpcId -ne $null) { delete }` | PASS | pass | ok |
| A11 | UL header `$VpcId`, line `aws ec2 delete-vpc --vpc-id $vpcid` unguarded | PASS | fail | **bypass** |
| A12 | UL header `${VpcId}`, unguarded delete | FAIL | fail | ok |
| A13 | UL `$VpcId = "$VpcId"`, then an unguarded delete | PASS | fail | **bypass** |
| A14 | UL `$VpcId = $VpcId.Trim()`, then an unguarded delete | PASS | fail | **bypass** |
| A15 | UL `foreach ($VpcId in @()) { }`, then an unguarded delete | PASS | fail | **bypass** |
| A16 | UL `$VpcId = [string]$VpcId; delete` on one line | PASS | fail | **bypass** |
| A17 | GL `Set-Variable -Name VpcId -Value $null`, then delete | PASS | fail | **bypass** |
| A18 | GL `Clear-Variable VpcId`, then delete | PASS | fail | **bypass** |
| A19 | GL delete, then `Remove-Variable VpcId` (benign cleanup) | PASS | pass | ok |
| A20 | GL `${VpcId} = $null` | PASS | fail | **bypass** |
| A21 | GL `[void]($VpcId = $null)` | PASS | fail | **bypass** |
| A22 | GL `$VpcId = $X = $null` | PASS | fail | **bypass** |
| A23 | GL `$VpcId = ' '` | PASS | fail | **bypass** (debatable) |
| A24 | UL here-string body line `$VpcId = 'vpc-0abc'`, then an unguarded delete | PASS | fail | **bypass** |
| A25 | GL, no step assignment; a here-string body fakes one | PASS | fail | **bypass** |
| A26 | GL `aws ... \``, next line `-ErrorAction SilentlyContinue` | PASS | fail | **bypass** |
| A27 | UL guard split over 3 lines (`if ($VpcId) {` / delete / `}`) | FAIL | pass | **false positive** |
| A28 | UL guard with a backtick continuation | FAIL | pass | **false positive** |
| A29 | GL `aws ... --query "a;b" -EA 0` | PASS | fail | **bypass** (`;` in a string splits the segment) |
| A30 | GL `aws ... --query 'x\|y' -ErrorAction Ignore` | PASS | fail | **bypass** |
| A31 | GL `Write-Output "done with aws cleanup" -EA 0` | FAIL | pass | **false positive** |
| A32 | UL `if ($VpcId) { Write-Host '}'; delete }` | FAIL | pass | **false positive** |
| A33 | UL `if ($VpcId -ne ')') { delete }` | FAIL | fail | ok |
| A34 | UL `if ($VpcId) { Write-Host '{' }; delete; '}'` (smuggle) | FAIL | fail | ok |
| A35 | GL `delete # $VpcId = 'vpc-0abc'` with nothing set in steps | PASS | fail | **bypass** |
| A36 | UL `delete # $VpcId = 'vpc-0abc'` unguarded | PASS | fail | **bypass** |
| A37 | UL `if ($VpcId) { delete } # VPC last` | FAIL | pass | **false positive** |
| A38 | GL `delete # never add -ErrorAction to aws` | FAIL | pass | **false positive** |
| A39 | GL `-EA:SilentlyContinue` | FAIL | fail | ok |
| A40 | GL `-ErrorAction:Ignore` | FAIL | fail | ok |
| A41 | GL `-ErrorAct SilentlyContinue` (PS prefix abbreviation) | PASS | fail | **bypass** |
| A42 | GL `& aws ... -EA 0` | FAIL | fail | ok |
| A43 | GL `&aws ... -EA 0` | PASS | fail | **bypass** |
| A44 | GL `& 'aws' ... -EA 0` | PASS | fail | **bypass** |
| A45 | GL `& "C:\Program Files\Amazon\AWSCLIV2\aws.exe" ... -ErrorAction 0` | PASS | fail | **bypass** |
| A46 | GL step "Don't skip: `$VpcId = aws ec2 create-vpc --query 'Vpc.VpcId'`" | FAIL | pass | **false positive** (the apostrophe opens a fake string span) |
| A47 | GL step `Set-Variable -Name VpcId -Value (aws ...)` | FAIL | pass | **false positive** (debatable) |
| A48 | GL duplicate line that differs only in whitespace | PASS | fail | bypass (low value) |
| A49 | UL `if ($VpcId -and $VpcId -eq '')` | PASS | pass | ok (never runs) |
| A50 | UL `If(${VpcId}){ delete }` | PASS | pass | ok |

**Real content:** `scan_lab()` returns no errors for any of the 42 labs, and `main()` prints `PASS 42 labs scanned`.

I also grepped every real teardown for the risky shapes:
- Every `-ne 'None'` guard in UL-03/04/09/10/11/12/15/17/18/19 is paired with a bare `$X -and` term, so the fix proposed in PY-R4-001 keeps them passing.
- No teardown uses here-strings, backtick continuations, `else`, trailing `#` comments after code, `Set-/Clear-Variable`, or `&`/quoted `aws`.

The bypasses are therefore **latent**. Today's PASS is honest.

Only one UL teardown assigns a variable it also declares. UL-02 has `if (-not $Bucket) { $Bucket = "workbook-ul02-$(...)" }`, and its right-hand side does not reference `$Bucket`, so the fix proposed in PY-R4-003 keeps it passing.

## Loader and lint review

**`content_loader.py` shape validation.**
- **Correctness:** the checks are correct for what they cover.
- **Over-strictness:** none. All 429 questions pass: `choices` is a list of dicts, and `objectiveIds`/`correctAnswerIds` are lists of strings. All 189 SAA rows and all 37 TF rows have `id` plus `domain_id`/`group`, and every `group` is an int.
- **Caching:** `lru_cache` does not cache exceptions (correct), and the test clears the cache on both sides.
- **Gaps** (`loader_r4.py`):
  - The element types inside the lists are not checked.
  - Unhashable ids in the SAA map are not caught.
  - `load_lab`/`lab_index` do no shape checks, so `/api/content/summary` still returns an HTML 500 when `steps` or `acceptanceCriteria` is not a list.

  All of these are listed in PY-R4-010.
- **Route coverage:**
  - Covered: questions, catalog, attempts and readiness (through `load_question` and the objective maps).
  - Not covered: lessons, labs, exercises and coverage get top-level checks only. Lesson, lab and coverage detail pass the JSON through unchanged, so they do not crash. The summary route (`lab_index`) can crash.

**`content_lint.py`.**
- The `main() -> int` refactor is behavior-preserving. Module-level state is gone, `sys.exit(main())` keeps the exit code, and stdout is unchanged. The module can now be imported for tests without running the lint.
- `find_duplicate_criteria` is correct for exact duplicates once whitespace and case are normalized.
- Limitations (PY-R4-011):
  - It checks only unguided `acceptanceCriteria`.
  - "X." and "X" count as distinct.
  - Guided step bullets and step ids are not checked for duplicates.
  - Lint does not mirror the loader's new shape rules, so lint can PASS while the API returns a 500.

## New issues

| ID | Tag | Sev | File:line | Detail |
|---|---|---|---|---|
| PY-R4-001 | Confirmed (scanner) | Medium | scan_lab_placeholders.py:45-49, 193-204 | **A value comparison counts as a presence guard.** `GUARD_TERM` accepts `$X -ne <anything>` and `$X -eq '<string>'`, and only `-eq $null` is rejected. In PowerShell, `$null -ne 'x'` and `$null -ne $false` are `$True`, so `if ($VpcId -ne 'x')` runs the delete when the ID is unset (A08, A09). `-eq ''` and `-eq "$null"` are inverted guards (A06, A07). **Fix:** every learner var must appear as a bare `$X` term or as `$X -ne $null`. Allow value comparisons only as *extra* `-and` terms. Every real guard (`$X -and $X -ne 'None'`, UL-16 `$VpcId -and $IsDefault -eq 'False'`) already has this shape. |
| PY-R4-002 | Confirmed (scanner) | Medium | scan_lab_placeholders.py:286 (and :261, :275-279) | **Case-sensitive set algebra skips the guard rule.** `declared`, `used` and `assigned` keep their original case, and `used & declared - assigned` compares them raw. A header `# Uses: $VpcId` with the line `aws ec2 delete-vpc --vpc-id $vpcid` gives an empty `learner_vars`, so no guard is required and the lab PASSES (A11). The missing-variable check at :281 lowercases names, so nothing else catches it. **Fix:** compute `learner_vars` on lowercased names, e.g. `{v for v in used if v.lower() in _lower(declared) - _lower(assigned)}`. Add a test. |
| PY-R4-003 | Confirmed (scanner) | Medium | scan_lab_placeholders.py:159-165, 274-278, 290 | **A no-op teardown "lookup" releases a declared var from the guard rule.** Any assignment that is not a reset counts as a lookup: `$VpcId = "$VpcId"`, `$VpcId = $VpcId.Trim()`, `$VpcId = [string]$VpcId`, or `foreach ($VpcId in @()) {}`. After that, later lines (or the same line) may use `$VpcId` unguarded (A13-A16). **Fix (UL only):** do not count an assignment whose right-hand side references the target var. Do not carry `foreach` loop vars past their own line. UL-02's defaulting line still passes under this rule. |
| PY-R4-004 | Confirmed (scanner) | Medium | scan_lab_placeholders.py:143-165, 175-180, 69-94 | **Trailing `#` comments are analysed as code.** `aws ec2 delete-vpc --vpc-id $VpcId # $VpcId = 'vpc-0abc'` counts as an assignment. That satisfies the "nothing sets" rule in GL (A35) and removes the guard requirement in UL (A36). The same comment text also causes false positives: `} # note` breaks the guard parse (A37), and a comment that mentions `-ErrorAction` trips the aws rule (A38). **Fix:** strip a `#` comment that lies outside a string (and is not in `<#...#>`) before any per-line analysis. |
| PY-R4-005 | Confirmed (scanner) | Low | scan_lab_placeholders.py:19, 132-140, 143-156 | **Reset forms that are still missed:** `${X} = $null` (`ASSIGN` has no braced form, so a braced *real* assignment is also invisible), `[void]($X = $null)` (the rhs is `$null)`), chained `$X = $Y = $null` (non-overlapping `finditer`), `$X = ' '`, and `Set-Variable -Value $null`/`Clear-Variable X` (A17, A18, A20-A23). **Fix:** make `ASSIGN` accept `\$\{?Name\}?`, strip `)` from the rhs, treat `Set-Variable ... $null` and `Clear-Variable Name` as resets, and blank-trim quoted strings before comparing. |
| PY-R4-006 | Confirmed (scanner) | Low | scan_lab_placeholders.py:238-290 | **Every teardown entry is analysed on its own.** This causes three problems: here-string bodies are treated as code, so a fake `$X = ...` line inside `@"..."@` satisfies the rules (A24, A25); a backtick continuation hides `-ErrorAction` on the next line (A26); and legitimate multi-line guards fail (A27, A28). **Fix (KISS):** add a lint/scanner rule that rejects `@'`/`@"` and a trailing backtick in `orderedDeletesPowerShell`, so every entry must be one self-contained statement. That is already true of all 42 labs. |
| PY-R4-007 | Confirmed (scanner) | Low | scan_lab_placeholders.py:32, 36-37, 175-180 | **The `-ErrorAction` rule does not understand strings.** `SEGMENT_SPLIT` splits on `;` or `\|` inside quotes (A29, A30, false negatives), and "aws " inside a string literal counts as a command (A31, false positive). `AWS_CMD` misses `&aws`, `& 'aws'` and a full-path `...\aws.exe"` (A43-A45). `ERROR_ACTION` misses PowerShell prefix abbreviations such as `-ErrorAct`/`-ErrorA` (A41). **Fix:** blank string contents (keeping the quote characters) before splitting. Widen the `AWS_CMD` prefix to `[\s\`(&'"\\]` and allow an optional closing quote. Use `-(?:EA\|ErrorA[a-z]*)\b`. |
| PY-R4-008 | Probable (scanner) | Low | scan_lab_placeholders.py:96, 107-112, 53-66 | **String spans are naive.** `'[^']*'` pairs apostrophes in prose ("Don't", "VPC's"), so a real step assignment that sits between two apostrophes is ignored. The result is a false "nothing sets" (A46). `_match_balanced` counts braces inside strings (A32). This is latent: all current labs pass. **Fix:** for bullets, look for assignments only inside backtick code spans. Make `_match_balanced` skip quoted text. |
| PY-R4-009 | Recommendation | Low | scan_lab_placeholders.py:91-93, 19 | **Legitimate shapes that are rejected:** `if (...) { ... } else { ... }` (A04), and `Set-Variable -Name X -Value (...)` as a step assignment (A47). The whitespace-only duplicate-line check is also still missing (A48). None of these occur in current content, so either document them as unsupported or handle them. |
| PY-R4-010 | Confirmed (loader) | Low | content_loader.py:74-76, 209, 226-231, 137-146; readiness.py:29; views.py:137; scoring.py:5 | **The shape validation does not check element types.** Several shapes still crash as an uncaught exception, which gives an HTML 500 rather than JSON (see `loader_r4.py`):<br>• `objectiveIds: [1]` → `AttributeError` in `_attempt_track`/`question_track` (readiness once attempts exist).<br>• A choice whose `id` is a list, or a list inside `correctAnswerIds` → `TypeError: unhashable` in `create_attempt`/`score_question`.<br>• An SAA row with a list `id` → uncaught `TypeError` at :209. The TF map catches the same case at :228 but reports it wrongly as "non-numeric group", and silently coerces `1.9` or `True` to `1`.<br>• A lab where `steps` or `acceptanceCriteria` is not a list → `TypeError` in `lab_index`, so `/api/content/summary` returns an HTML 500 (the view catches only `FileNotFoundError`/`ContentParseError`).<br>**Fix:** pass `item_type=str` for `objectiveIds`/`correctAnswerIds`, check that each choice `id` is a str, check `isinstance(row["id"], str)` and `type(group) is int` in the maps, and validate `steps`/`acceptanceCriteria` as lists in `load_lab`. |
| PY-R4-011 | Recommendation | Low | scripts/content_lint.py:21-35, 102-107, 70-81 | **Duplicate-criterion rule scope:**<br>• It applies only to unguided `acceptanceCriteria`.<br>• Normalization keeps trailing punctuation, so "X." and "X" count as distinct.<br>• Guided bullets and step ids are not checked.<br>• Lint does not mirror the loader shape rules from PY-R4-010, so lint can PASS on content the API rejects.<br>Other points: `ACCOUNT` (line 14) is unused, and `errors[:40]` truncates the list (the count is still printed). The `main()` refactor itself is fine. |
| PY-R4-012 | Informational | Info | views.py:48-50, 82-83; content_loader.py:196, 213 | Round-2 items 009, 010 and 011 are unchanged:<br>• No summary cache.<br>• The objective maps are `lru_cache`d for the life of the process, so they go stale after a content edit until a restart.<br>• `logger.error` is called without `exc_info`.<br>• `str(FileNotFoundError)` leaks the absolute path in the summary 500. |

**Priority for Lead Dev:** PY-R4-001, -002, -003 and -004 are cheap regex and set fixes. Each one closes a guard or assignment bypass that a future content edit could slip through. Every fix keeps all 42 real labs passing. PY-R4-006's single-statement rule is the KISS way to close A24-A28 together.

## Command output

`cd backend; $env:PYTHONDONTWRITEBYTECODE=1; .\.venv\Scripts\python.exe manage.py test workbook`
```
Found 46 test(s).
System check identified no issues (0 silenced).
Creating test database for alias 'default'...
..............................................
----------------------------------------------------------------------
Ran 46 tests in 0.152s

OK
Destroying test database for alias 'default'...
exit=0
```

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

Scratchpad `adv_r4.py` summary:
```
50 probes, 36 wrong
real labs: 42 scanned, 0 with errors
```

Scratchpad `loader_r4.py`:
```
objectiveIds=[1] load: OK -> loaded
objectiveIds=[1] _attempt_track: UNCAUGHT AttributeError: 'int' object has no attribute 'startswith'
objectiveIds=[1] question_track: UNCAUGHT AttributeError: 'int' object has no attribute 'startswith'
choice id is a list -> create_attempt set(): UNCAUGHT TypeError: unhashable type: 'list'
correctAnswerIds [[a]] -> score_question: UNCAUGHT TypeError: unhashable type: 'list'
choices as dict: ContentParseError (Content file q-choices-dict.json field 'choices' must be a list of objects)
saa row id unhashable: UNCAUGHT TypeError: unhashable type: 'list'
tf row id unhashable (message?): ContentParseError (Content file terraform_004.json has a non-numeric 'group' for ['x'])
tf group 1.9 / True silently coerced: OK -> {'tf.1': 1, 'tf.2': 1}
lab acceptanceCriteria=5 -> content_summary: UNCAUGHT TypeError: 'int' object is not iterable
lab steps=7 -> content_summary: UNCAUGHT TypeError: 'int' object is not iterable
lesson drillIds string -> content_summary: OK -> [{'id': 'l-1', 'title': 'l-1', 'drillIds': 'q-1', 'objectiveIds': []}]
```
