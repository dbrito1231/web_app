# Implementer log: Batch F4 (Amendment 2, round-3 Python fixes)

Scope: `scripts/scan_lab_placeholders.py`, `scripts/content_lint.py`, `backend/workbook/**` only.
Source: `reports/fix-loop-r2/round-3/PYTHON.md`.

## PY-R3-002 — scanner guard check was text-only

Replaced the greedy regex guard check with:

- `_parse_guard(line)`: parses `if (COND) { BODY }` using bracket-depth counting
  (`_match_balanced`), not a greedy regex, so a delete outside the guard's braces
  no longer matches, and nested `foreach`/`if`/`do...while` blocks inside a valid
  guard body no longer break the parse.
- `GUARD_TERM`: a guard term must be a bare `$Name` (optionally `${Name}`),
  optionally compared with `-eq`/`-ne` to a quoted string, `$true`, or `$false`.
  Anything else (`-not`, `!`, `-or`, a bare `$true`) fails to match, invalidating
  the whole guard. `-eq $null` is rejected explicitly, since it guards the delete
  on the value being *absent* (an inverted guard) — `-ne $null`/other `-eq`
  comparisons (e.g. `-eq 'False'`, used by real content in `ul-16`) are fine.
- Guard variable names are matched as a full `\$\{?Name\}?` token via `GUARD_TERM`,
  not `in`/substring, so `$VpcIdOld` no longer satisfies a `$VpcId` guard requirement.
- Terms are joined only by `-and` (case-insensitive); condition must consist
  entirely of such terms or the whole guard is rejected.

## PY-R3-003 — `$null`-reset bypasses

- `_is_reset_rhs`: also rejects `''`, `""`, and a self-assignment (`$X = $X`,
  case-insensitive), in addition to `$null`/`$NULL`/any-case `$null`.
- `_assignments_in`/`_assigned_in`: an assignment now only counts if its
  `$Name =` target is **outside** any single/double-quoted string span
  (`_string_spans`/`_inside_a_string`), computed on the raw line — so
  `Write-Host "$VpcId = gone"` no longer registers as an assignment. The
  right-hand side is still read from the unmodified text so a real
  `$X = ''`/`$X = $null` reset is still detected correctly (stripping the
  quotes first, as an earlier draft did, destroyed the very text needed to
  tell a reset from a real assignment — fixed by span-checking the match
  position instead of blanking string contents).
- New check: a teardown with no non-comment, non-empty line now fails
  (`... teardown has no delete commands (empty or comments only)`), for both
  guided and unguided labs.

## PY-R3-004 — `-ErrorAction` false positives/negatives

- Guided-lab step bullets are now checked **individually**
  (`_iter_bullets`/`_check_error_action` called per bullet), not on
  `json.dumps(steps)` as one blob, so two unrelated bullets (one mentioning
  "aws" in prose, another using `-ErrorAction` on an unrelated cmdlet) no
  longer produce a false positive.
- `ERROR_ACTION` now matches `-ErrorAction`/`-EA` case-insensitively
  (`(?i)-(?:ErrorAction|EA)\b`), and `AWS_CMD` matches `aws` or `aws.exe`
  case-insensitively.

## PY-R3-005 — prose-assignment regex too loose

`PROSE_ASSIGN` narrowed to two literal phrasings: `Copy ... into `$X`` and
`Set `$X` to ...`. "Look into `$X` later" and "Set `$X` later" no longer count
as a stand-in assignment. Re-derived which labs actually *depend* on this
fallback (none currently do — even GL-01's `$AccountId`/`$BoundaryArn` are also
self-assigned in the teardown itself — but GL-01's steps do use the "Copy ...
into" phrasing, which the narrowed regex still recognizes for defense in depth).

## PY-R3-006 — case sensitivity

- All variable-name comparisons (`used`, `assigned`, `declared`, `AUTOMATIC`,
  guard vars) are done via `.lower()`; display text keeps the original casing
  from the line so existing error-message assertions (`$VpcId but nothing
  sets...`) still read naturally.
- `VAR_REF`/`GUARD_TERM` accept `${Name}` as well as `$Name`.
- `IF_OPEN`/guard parsing matches `if (` case-insensitively (`If (` works).
- `AUTOMATIC` is now all-lowercase and compared case-insensitively, so
  `$PWD`/`$Null`/`$True` match the automatic-variable exemption regardless of case.

## PY-R3-001 — bad shapes inside otherwise-valid files crashed with an HTML 500

`backend/workbook/content_loader.py`:

- `load_question` now validates (raising `ContentParseError`, not letting the
  caller crash later) that `choices` is a list of objects, and that
  `objectiveIds`/`correctAnswerIds`, if present, are lists — this is what fixes
  the `"choices": "ab"` → `AttributeError` in `create_attempt`, and the
  `objectiveIds` "string iterated character by character" silent-wrong-answer
  case.
- `saa_objective_domain_map`/`terraform_objective_group_map` now validate each
  row is a dict with the required key(s) (`id`+`domain_id`, `id`+`group`) and
  raise `ContentParseError` instead of `KeyError`/`TypeError`; a non-numeric
  `group` also raises `ContentParseError` instead of an uncaught `ValueError`.
  Both are `@lru_cache`d functions — `functools.lru_cache` does not cache
  raised exceptions, so a later call still re-validates and returns fresh
  results once content is fixed.
- `views.readiness_metrics` already caught `ContentParseError` around both
  `_question_objectives_map()` and `compute_readiness_metrics(...)`, so no view
  change was needed there — the fix was making the loaders raise the right
  exception type instead of an unhandled one.

`backend/workbook/tests/test_scoring_and_api.py` (`ContentParseTests`):
extended `test_corrupt_files_return_json_500_through_real_views` to also hit
`GET /api/metrics/readiness` and `POST /api/attempts` for all three corrupt-file
shapes (syntax error, UTF-16, wrong top-level type), and added two new direct
unit tests: `test_question_with_bad_choices_shape_raises` and
`test_objective_row_missing_fields_raises`.

## TEACHER-R3-001 — duplicate-criterion lint rule

`scripts/content_lint.py`: added `find_duplicate_criteria(criteria)` (using
`_normalize_criterion`: collapse whitespace, lowercase) and wired it into the
unguided-lab loop, so a lab with two acceptance criteria that are identical
once normalized fails lint.

While making this testable without side effects, refactored `content_lint.py`
so the whole analysis runs inside `main() -> int` (returns 0/1) behind
`if __name__ == "__main__": sys.exit(main())`. `find_duplicate_criteria` and
`_normalize_criterion` stay at module level, outside `main()`, so importing the
module for a unit test defines them without re-running the full lint against
the real `content/` tree. Command-line behavior (`python scripts\content_lint.py`,
exit code, stdout) is unchanged.

## Fixture tests added

`backend/workbook/tests/test_lab_scan.py` — one passing and one failing case
per new rule (24 new tests total, plus 2 for the lint duplicate rule):

- Guard quality: `test_always_true_guard_fails`, `test_inverted_guard_fails`,
  `test_delete_outside_guard_block_fails`,
  `test_second_statement_after_guard_fails`,
  `test_guard_name_must_match_whole_variable`,
  `test_guard_eq_null_is_inverted_and_fails` (fail cases);
  `test_nested_blocks_inside_a_valid_guard_pass`,
  `test_guard_with_value_comparison_passes` (pass cases).
- Null/empty resets and empty teardown:
  `test_empty_string_reset_is_not_an_assignment`,
  `test_self_assignment_is_not_an_assignment`,
  `test_assignment_text_inside_a_string_does_not_count`,
  `test_empty_teardown_fails`, `test_comment_only_teardown_fails`.
- `-ErrorAction`: `test_lowercase_erroraction_on_aws_fails`,
  `test_ea_alias_on_aws_fails`, `test_aws_exe_with_erroraction_fails` (fail
  cases); `test_error_action_checked_per_bullet_not_whole_step` (pass case).
- Prose regex: `test_prose_copy_into_and_set_to_still_satisfy_the_rule` (pass),
  `test_prose_that_only_mentions_the_variable_does_not_satisfy_the_rule` (fail,
  i.e. correctly still reports "nothing sets").
- Case-insensitivity: `test_variable_case_mismatch_is_not_flagged`,
  `test_braced_variable_is_recognized`, `test_pwd_automatic_variable_is_not_flagged`,
  `test_uppercase_if_guard_is_recognized` (all pass cases; there is no
  meaningful "fail" counterpart for a case-normalization fix).
- `ContentLintDuplicateCriterionTests`: `test_duplicate_criteria_detected`,
  `test_distinct_criteria_pass`.

`backend/workbook/tests/test_scoring_and_api.py`:
`test_question_with_bad_choices_shape_raises`,
`test_objective_row_missing_fields_raises`, and the extended
`test_corrupt_files_return_json_500_through_real_views`.

## Command output

`cd backend; PYTHONDONTWRITEBYTECODE=1 .venv\Scripts\python.exe manage.py test workbook`
```
Ran 46 tests in 0.162s

OK
```

`backend\.venv\Scripts\python.exe scripts\scan_lab_placeholders.py`
```
PASS 42 labs scanned
```

`backend\.venv\Scripts\python.exe scripts\content_lint.py`
```
questions 429 aws 310 tf 119
labs 21 + 21
lessons 23
PASS
```

## Real content vs. the new rules

All 42 labs pass the rewritten scanner and content_lint as they stand today —
**no lab needed to be flagged for a maintainer to fix.** Two real labs came
close during development and are recorded here for transparency:

- `ul-07`'s nested `if ($FileSystemId) { $MtIds = ...; foreach ($MtId in $MtIds)
  { if ($MtId) { ... } } }` and a `do { ... } while (...)` guard initially
  failed under a naive greedy-regex guard parser (a bug in an intermediate
  version of this fix, not a real content problem) — fixed by switching to
  bracket-depth parsing (`_parse_guard`/`_match_balanced`). Now passes cleanly.
- `ul-16`'s `if ($VpcId -and $IsDefault -eq 'False') { aws ec2 delete-vpc
  --vpc-id $VpcId }` initially failed because an intermediate version of
  `GUARD_TERM` only accepted `-ne` comparisons (per the report's literal
  wording). Real content legitimately uses `-eq` against a non-null string, so
  `GUARD_TERM` was generalized to accept `-eq`/`-ne` against any quoted
  string/`$true`/`$false`, while still specifically rejecting `-eq $null` (the
  actual inverted-guard bypass the report was concerned about). Now passes
  cleanly, no content edit needed.

No other batch's in-flight content changes were touched by this batch.
