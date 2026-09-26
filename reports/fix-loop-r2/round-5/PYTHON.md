# PYTHON.md: Senior Python Developer, fix-loop round 5

Scope: commit `9fdd1d2` ("Scanner: presence guards, case-insensitive, no
self-referencing lookups, comments stripped, hard constructs banned; loader
and lint validate list item types"), change log
`reports/fix-loop-r2/amendment-2/impl-F11.md`. Prior review:
`reports/fix-loop-r2/round-4/PYTHON.md`.

This was a read-only review. I did not start a server, send a POST, run a
migration or install, or edit any repo file other than this report.

Scratchpad script (outside the repo): `adv_r5.py` — imports
`scan_lab_placeholders.scan_lab` directly and runs 32 new adversarial
teardown probes in-process, plus a full re-scan of all 42 real labs. It does
not repeat any of `adv_r4.py`'s or `impl-F11.md`'s `adv_r5.py`'s 50 probes.

## 1. Verdicts on round-4 items

| Item | Verdict | Evidence |
|---|---|---|
| PY-R4-001 value comparison alone accepted as presence guard | **Gone** | `_guard_covers` (scan_lab_placeholders.py:339-373) tracks `presence_vars` separately; a bare `$X` or `$X -ne $null` term is required, a value comparison is only an allowed *extra* `-and` term. `-eq $null` still rejected. Matches `impl-F11.md`'s described fix exactly. |
| PY-R4-002 case-sensitive set algebra skipped the guard rule | **Gone** | scan_lab_placeholders.py:461: `learner_vars = {v for v in used if v.lower() in _lower(declared) - _lower(assigned)}` — case-insensitive on both sides now. |
| PY-R4-003 no-op "lookup" released a var from the guard rule | **Gone** | `_is_noop_rhs` (scan_lab_placeholders.py:151-163) plus `_references_var` (:136-137) exclude self-interpolation/`.Trim()`/`[string]$X` from counting as a real assignment; `_foreach_assigned_in` (:269-293) requires a non-empty, non-`@()`, non-self-referencing collection. |
| PY-R4-004 trailing `#` comments analysed as code | **Gone** | `_strip_comment` (scan_lab_placeholders.py:122-133) truncates at the first `#` outside a string span; wired into every per-line check in `scan_lab` (:407-465). |
| PY-R4-005 remaining reset forms (`${X}=$null`, `[void](...)`, chained, whitespace, `Set-/Clear-Variable`) | **Still present for the parsing gaps, but the exploit surface was closed a different way** | `_is_reset_rhs` (scan_lab_placeholders.py:140-148) is unchanged (no braced-target, no `[void]` unwrap, no chained-assignment handling, no blank-trim). But `Set-Variable`/`Clear-Variable`/`Remove-Variable` and any `${` are now separately **banned outright** in a teardown line (`_banned_construct`, :220-245), so `Set-Variable -Value $null` and `${X} = $null` no longer need `_is_reset_rhs` to catch them — they FAIL as banned constructs before reaching the reset check. `[void]($X = $null)` and `$X = $Y = $null` are NOT banned and remain live gaps (confirmed: `[void]($VpcId = $null)` still scans clean when it should be flagged as a reset-to-null). Recommend re-filing the `[void]`/chained-assignment residual as its own low-severity item since the original PY-R4-005 is now split between "closed via a ban" and "still open." |
| PY-R4-006 every teardown entry analysed on its own (here-strings, backtick continuation, multi-line guards) | **Gone (via an outright ban, not parsing)** | `HERE_STRING_OPEN`/`BACKTICK_CONT_TAIL` bans (scan_lab_placeholders.py:230-233); `_parse_guard` now also accepts a trailing `else {...}` (:206-217) so a legitimate one-line `if/else` no longer false-positives. A guard split across separate array entries is now a deliberate FAIL (documented behavior change in `impl-F11.md`), not a bug. |
| PY-R4-007 `-ErrorAction` string/case/prefix/aws-invocation gaps | **Gone for every originally cited form** | Whole-line masking (`_mask_strings`) replaces segment-splitting, so a `;`/`\|` inside a string no longer produces false segments (closes A29/A30/A31 from round 4). `AWS_CMD` is case-insensitive and `ERROR_ACTION` now matches any `-EA`/`-ErrorAction` prefix ≥3 chars (closes A41). `&aws`, `& 'aws'`, and a full/quoted `aws.exe` path are now banned outright (closes A43-A45). **New residual, found this round:** `aws` reached through a *variable* (`$cli='aws'; & $cli ...`) or through `iex`/`Invoke-Expression` on a quoted command string is neither banned nor detected — see PY-R5-001 and PY-R5-002 below. These are new attack surfaces exposed by the F11 rewrite (the ban is keyed to the literal token `aws`/`aws.exe`, which a variable or a quoted iex argument never presents on the unmasked/relevant span), not a re-opening of the originally reported items. |
| PY-R4-008 naive string spans (`_match_balanced` not string-aware, apostrophe swallowing a bullet assignment) | **Still present (partly)**, as `impl-F11.md` itself documents | Rule 6 (`BACKTICK_CODE`/`_code_spans_in`) fixes the bullet-apostrophe case (A46-type). `_match_balanced` (scan_lab_placeholders.py:166-179) is unchanged — still not string-aware, so a `'}'` inside a string can still break brace matching (A32, explicitly listed as unfixed in `impl-F11.md`'s adversarial re-run table). Confirmed unfixed in this round's probes only indirectly (not independently re-tested since `impl-F11.md` already reproduces it and nothing in the diff touches `_match_balanced`). |
| PY-R4-009 legitimate shapes rejected (`else`, `Set-Variable` step assignment, whitespace-only duplicate) | **Partially addressed, partially superseded by a deliberate design choice** | A plain `if (...) { ... } else { ... }` is now correctly recognized (closes the `else` half). The `Set-Variable` step-assignment shape and the whitespace-only duplicate-line check were **not** implemented; instead, `impl-F11.md`'s "Deliberate behavior changes" section explicitly re-scopes A19/A27/A28/A50 to now FAIL by design (ban supersedes "safe form" recognition). This is a reasonable KISS call — none of the 42 real labs need the safe forms — but it is a conscious rejection of part of the original recommendation, not a fix. |
| PY-R4-010 loader didn't check element types | **Gone** | `content_loader.py`: `load_question` passes `item_type=str` for `objectiveIds`/`correctAnswerIds` (:97-98); `_require_choice_ids` (:79-89) checks each choice `id` is `str`; `load_lab` validates `steps`/`acceptanceCriteria` shapes (:105-106); `saa_objective_domain_map`/`terraform_objective_group_map` check `id` is `str` and `group` is a real `int` (not `bool`, not `float`) (:235-238, :256-266). All of `loader_r4.py`'s uncaught-exception probes from round 4 are covered by new tests in `test_scoring_and_api.py`. |
| PY-R4-011 lint duplicate-rule scope / no shape mirror | **Gone** | `_normalize_criterion` strips a trailing `.` (content_lint.py:23); duplicate check now runs over all `labs`, not just `unguided` (:137-141); `check_question_shape`/`check_lab_shape` (:51-81) mirror the loader's checks and are wired into `main()` (:117, :138). Guided step-bullet duplicates and step-id duplicates are still not checked — not part of PY-R4-011's original ask, so not a regression. |
| PY-R4-012 (informational: no summary cache, `lru_cache` staleness, `logger.error` no `exc_info`, path leak in 500) | **Still present, unchanged** | Not in scope for F11 (`impl-F11.md` scope line explicitly limits itself to the round-4 Python items list, and 012 was Informational/no fix requested). `views.py`/`content_loader.py` lines are unchanged from round 4. |

## 2. Adversarial results (fresh probes, `adv_r5.py`, 32 probes)

None of these repeat `adv_r4.py`'s 50 probes or `impl-F11.md`'s `adv_r5.py`
(the F11 implementer's own re-run of an adapted `adv_r4.py`). "Result" is
what the scanner does; PASS means it reported no problem. GL probes that
test `-ErrorAction`/`aws`-detection isolate that check with a real preceding
lookup line for `$VpcId`, so a result is never confounded by the unrelated
"nothing sets or declares it" rule (GL labs have no `# Uses:` header).

**24 of 32 correct. 8 wrong — all 8 are new bypasses, not previously
reported.**

| # | Probe | Result | Should | Verdict |
|---|---|---|---|---|
| B01 | UL `if (-not -not $VpcId) { delete }` (double negation) | FAIL | fail | ok (unrecognized shape, forced rework — not a bypass) |
| B02 | UL `if (-not [string]::IsNullOrEmpty($VpcId)) { delete }` | FAIL | fail | ok (unrecognized shape) |
| B03 | UL `if ($null -ne $VpcId) { delete }` (operands reversed) | FAIL | fail | ok (unrecognized shape) |
| B04 | UL `if ($SkipCleanup) { } else { delete-on-$VpcId }` | FAIL | fail | ok (cond doesn't cover $VpcId) |
| B05 | UL `if ($SkipCleanup -eq $false) { delete-on-$VpcId }` | FAIL | fail | ok |
| B06 | UL `$VpcIds \| ForEach-Object { delete $_ }`, unguarded | FAIL | fail | ok (no ForEach-Object bypass) |
| B07 | UL real lookup, then `$VpcIds \| % { delete $_ }` | PASS | pass | ok (legitimate) |
| B08 | GL `Invoke-Expression "aws ... -ErrorAction SilentlyContinue"` | PASS | fail | **bypass** |
| B09 | GL `iex "aws ... -ErrorAction SilentlyContinue"` | PASS | fail | **bypass** |
| B10 | GL `$cli='aws'; & $cli ... -ErrorAction SilentlyContinue` | PASS | fail | **bypass** |
| B11 | GL two-line: `$cli='aws'` / `& $cli ... -ErrorAction SilentlyContinue` | PASS | fail | **bypass** |
| B12 | GL uppercase `AWS ec2 delete-vpc ... -ErrorAction ...` | FAIL | fail | ok (case-insensitive, sanity) |
| B13 | GL en-dash `aws ec2 ... –ErrorAction SilentlyContinue` | PASS | fail | **bypass** |
| B14 | GL em-dash `aws ec2 ... —ErrorAction SilentlyContinue` | PASS | fail | **bypass** |
| B15 | GL tab before `-ErrorAction` | FAIL | fail | ok (sanity) |
| B16 | UL tab-indented guard, otherwise legitimate | PASS | pass | ok (sanity) |
| B17 | UL `%`-alias unguarded delete (VpcId not looked up) | FAIL | fail | ok |
| B18 | UL `if (-not $VpcId) { } else { delete }` (correct semantics) | FAIL | fail | ok (unrecognized shape) |
| B19 | GL `$c='aws'; iex "& $c ... -EA 0"` (compound) | PASS | fail | **bypass** |
| B20 | GL unquoted full-path `aws.exe` | FAIL | fail | ok (sanity) |
| B21 | GL `$exe='...\aws.exe'; & $exe ... -ErrorAction ...` | FAIL | fail | ok (caught, but see note below) |
| B22 | UL `if ($VpcId -and -not -not $Extra) { delete }` | FAIL | fail | ok (one bad term voids whole guard, fails safe) |
| B23 | UL `if (-not [string]::IsNullOrWhiteSpace($VpcId)) { delete }` | FAIL | fail | ok |
| B24 | UL `$_.VpcId` property access, undeclared, via `%` | PASS | pass | ok (VAR_REF never captures `$_.Prop`) |
| B25 | GL uppercase `AWS` + en-dash `-EA` | PASS | fail | **bypass** |
| B26 | UL chained `Where-Object`/`%` pipeline, unguarded head var | FAIL | fail | ok |
| B27 | GL `Set-Variable @VarParams` (splatted) | FAIL | fail | ok (cmdlet name still literal) |
| B28 | UL legitimate `-and`-guarded `%`-alias pipeline | PASS | pass | ok (legitimate) |
| B29 | UL `if ($VpcId -ne ${Null}) { delete }` | FAIL | fail | ok (double-banned: `${` + unrecognized guard) |
| B30 | GL benign `iex "Write-Host ..."` elsewhere, unrelated normal delete | PASS | pass | ok (no cross-line interaction) |
| B31 | GL `$cli='aws'; & $cli ...` with **no** `-ErrorAction` | PASS | pass | ok (nothing to flag; isolates B10's failure to the `-ErrorAction` leak specifically) |
| B32 | GL `- ErrorAction` (space after dash, invalid PS syntax anyway) | PASS | pass | ok (not exploitable at runtime, so a scanner PASS is correct here) |

**B21 correction:** I initially expected this to be a bypass symmetric to
B10, but it is correctly caught — for an unrelated reason. `FULLPATH_AWS_EXE`
runs on the *raw* (unmasked) line by design (per `impl-F11.md`'s rule-5
notes), and its regex matches the `\aws.exe` text sitting inside the quoted
`$exe = '...'` string too, so the banned-construct rule fires regardless of
the variable indirection. This is a **fragility**, not a live gap: if
`FULLPATH_AWS_EXE`'s raw-line check is ever changed to run on a masked line
(e.g., to fix some future false positive), this exact case would silently
flip into a real bypass. Documented as PY-R5-004 (low severity, watch item).

**Real content:** re-scanning all 42 real labs in-process returns zero
errors, matching `scan_lab_placeholders.py`'s own `PASS 42 labs scanned`.

## 3. Loader and lint shape-validation review

**`content_loader.py`.**
- Correctness: `_require_optional_list`, `_require_choice_ids`, and the two
  objective-map checks are all correct for what they check. `bool`/`float`
  are explicitly excluded from the `int` group check (right call, since
  `bool` is an `int` subclass in Python and `1.9` must not silently
  truncate).
- Over-strictness: **none found.** `content_lint.py` (which now mirrors
  these exact checks via `check_question_shape`/`check_lab_shape`) passes
  clean on all current content (`questions 429 aws 310 tf 119`, `labs 21 +
  21`), and `manage.py test workbook` passes all 90 tests, including the new
  shape tests added in this commit. I did not find any real content file
  whose `choices`, `objectiveIds`, `correctAnswerIds`, `steps`, or
  `acceptanceCriteria` would trip a false failure under the new rules.
- Residual gaps (informational, not blocking): `load_lesson`,
  `exercise_index`, and `lesson_index`/`lab_index`'s own dict-shaped fields
  (`title`, `objectiveIds` when present but not validated at the *lesson* or
  *exercise* level) still pass JSON through with only a top-level
  `dict`/`list` check — same gap noted as out-of-scope in round 4
  (`content_loader.py` route-coverage note), unchanged and not part of this
  commit's stated scope.

**`content_lint.py`.**
- `_is_list_of` correctly treats `None`/missing as fine (mirrors the
  loader's "absent field = empty list" convention) — no over-strictness.
- `check_question_shape`/`check_lab_shape` are a faithful mirror of the
  loader; I did not find a case where lint would fail content the loader
  accepts, or vice versa, for the fields both now check.
- `_normalize_criterion`'s new trailing-`.`-stripping is correct and matches
  its own new test (`test_trailing_period_difference_is_still_a_duplicate`).
- Confirmed no false failures against current content: `python
  scripts\content_lint.py` returns `PASS` (see §5).

## 4. New issues

| ID | Tag | Sev | File:line | Detail |
|---|---|---|---|---|
| PY-R5-001 | Confirmed (scanner) | Low | scan_lab_placeholders.py:331-336 (`_check_error_action`), :39 (`AWS_CMD`) | **`iex`/`Invoke-Expression` on a quoted command string hides `-ErrorAction` from detection.** `_check_error_action` masks quoted-string contents before matching `AWS_CMD`+`ERROR_ACTION`. When the whole `aws ... -ErrorAction SilentlyContinue` invocation is itself a string argument to `iex`/`Invoke-Expression`, masking blanks out both the literal `aws` token and `-ErrorAction`, so the combined check never fires (B08, B09, B19). The line still IS a delete (VAR_REF still sees `$VpcId` inside the string, so the existing missing-var/guard checks are unaffected) — only the `-ErrorAction`-swallowing signal is lost. **Fix:** ban `iex`/`Invoke-Expression` outright in a teardown line, consistent with the KISS "ban the hard-to-parse construct" pattern already used for here-strings/backtick-continuation/`&`-invocation/full-path `aws.exe` (rule 5). None of the 42 real labs use it. |
| PY-R5-002 | Confirmed (scanner) | Low | scan_lab_placeholders.py:39 (`AWS_CMD`), :68 (`AMP_AWS_INVOKE`) | **`aws` invoked through a variable bypasses both the `&`-invocation ban and `-ErrorAction` detection.** `AMP_AWS_INVOKE` only matches `&` followed (after an optional quote) by the *literal* token `aws`/`aws.exe`; `AWS_CMD` likewise requires the literal token on the line. `$cli = 'aws'; & $cli ec2 delete-vpc --vpc-id $VpcId -ErrorAction SilentlyContinue` never presents that literal token outside a masked string, so neither the ban nor the `-ErrorAction` check fires (B10, B11, B19), whether the assignment and invocation are on the same teardown line or split across two. **Fix:** ban any `&`-invocation whose callee is a bare variable (`&\s*\$[A-Za-z_]`) in a teardown line — same KISS ban pattern as rule 5, since safely resolving what a variable holds is exactly the kind of parsing this rule set has already chosen not to attempt. |
| PY-R5-003 | Confirmed (scanner) | Low | scan_lab_placeholders.py:43-45 (`ERROR_ACTION`) | **`ERROR_ACTION` is ASCII-hyphen-only; a Unicode dash (en dash U+2013, em dash U+2014) before `ErrorAction`/`EA` is not matched.** PowerShell 7.2+ accepts several Unicode dash characters as parameter-prefix equivalents to `-`, so `aws ec2 delete-vpc --vpc-id $VpcId –ErrorAction SilentlyContinue` would still silence the real AWS CLI error at runtime, but the scanner reports no problem (B13, B14, B25). Latent: no real lab uses a Unicode dash. **Fix:** widen the dash character in `ERROR_ACTION` (and ideally `AWS_CMD`'s own `-` mentions, though none exist there) to a small class of ASCII hyphen plus the PowerShell-recognized dash code points (U+2013, U+2014, U+2212), e.g. `[-–—−]`. |
| PY-R5-004 | Recommendation (fragility) | Info | scan_lab_placeholders.py:236-239 (`_banned_construct`) | **`FULLPATH_AWS_EXE`/`AMP_AWS_INVOKE` run on the raw (unmasked) line by design, which happens to also catch a variable-indirected full path (B21) as a side effect of matching text inside a quoted string.** This is not a live gap today, but it means the ban's effectiveness against that specific shape is incidental, not intentional — a future edit to mask these two checks (e.g. to fix an unrelated false positive on a string that merely *mentions* a path) would silently reopen it. No content or code change needed now; flagging so a future edit to `_banned_construct` re-checks this case. |
| PY-R5-005 | Recommendation | Info | scan_lab_placeholders.py:140-148 (`_is_reset_rhs`) | **Residual from PY-R4-005, now split:** `${X} = $null` and `Set-/Clear-Variable ... $null` are closed (banned outright by rule 5, independent of `_is_reset_rhs`). `[void]($X = $null)` and chained `$X = $Y = $null` are **not** banned and `_is_reset_rhs` still can't parse them, so a teardown could still "reset" a variable to `$null` through either form without being flagged as `teardown resets a variable to $null`. Confirmed live: `[void]($VpcId = $null)` scans clean. Low value (no real lab needs this), carried forward from round 4 rather than a new finding. |

## 5. Judgment: is the scanner good enough to close?

All newly confirmed gaps (PY-R5-001/002/003) require a content author to
deliberately reach for an obfuscation idiom — `iex`/`Invoke-Expression` on a
quoted command string, `aws` called through an intermediate variable, or a
Unicode dash typed in place of `-` — none of which appears by accident, and
none of which any of the 42 real labs uses today (confirmed by the in-process
re-scan). Real labs also go through direct AWS and Student review per
`AGENTS.md`, so this scanner is a regression guard, not the sole line of
defence. I rate all three **Low**: exploiting them requires intent to hide a
teardown mistake, not an ordinary typo, and a human reviewer reading the
PowerShell would still see the plaintext `-ErrorAction SilentlyContinue` (or
the dash-oddity) in the diff. PY-R5-004 and -005 are Info/carry-forward, not
new exposure.

Every PY-R4 item the task said was fixed (001-004, 010, 011, plus the
banned-construct and prose rules) verified **Gone** against its originally
reported forms. PY-R4-005, -008, -009 remain partially open exactly as
`impl-F11.md` itself documents (either explicitly out of scope for F11, or a
deliberate design trade-off), not silently regressed.

**Scanner/loader work: close.**

The remaining items (PY-R5-001/002/003/004/005, plus the carried-forward
PY-R4-005/008/009/012) are all Low or Info. None of the round-4 Medium items
survive this commit under their originally reported forms, and the three new
Low findings this round are all deliberate-obfuscation shapes with no
foothold in real content, backstopped by direct human review. If Lead Dev
wants a cheap follow-up, PY-R5-001/002 (ban `iex`/`Invoke-Expression` and
`&`-through-a-bare-variable) are one-line regex bans consistent with the
existing rule-5 pattern and would close the two live gaps outright; PY-R5-003
(Unicode dash) is optional given how implausible accidental use is.

## 6. Command output

`cd backend; $env:PYTHONDONTWRITEBYTECODE=1; .\.venv\Scripts\python.exe manage.py test workbook`
```
Found 90 test(s).
System check identified no issues (0 silenced).
Creating test database for alias 'default'...
..........................................................................................
----------------------------------------------------------------------
Ran 90 tests in 0.194s

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

Scratchpad `adv_r5.py` summary:
```
32 probes, 8 wrong (all 8 are new confirmed bypasses: iex/Invoke-Expression
string-masking, aws-via-variable indirection, Unicode dash)
Full real-content re-scan: 42 labs scanned, 0 with errors
```

No repo file other than this report was created or edited.
