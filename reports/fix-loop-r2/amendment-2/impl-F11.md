# Implementer log: Batch F11 (Amendment 2, round-4 Python fixes)

Scope: `scripts/scan_lab_placeholders.py`, `scripts/content_lint.py`, `backend/workbook/**` only.
Source: `reports/fix-loop-r2/round-4/PYTHON.md`. Restart of a prior attempt that
stopped before editing anything — this run made all the edits below.

## PY-R4-001 — a value comparison alone was accepted as a presence guard

`_guard_covers` (`scan_lab_placeholders.py`) now tracks `presence_vars`
separately from "any recognized term". A guard term only adds its variable to
`presence_vars` if it is a bare `$X` or `$X -ne $null`. A value comparison
(`-eq`/`-ne` a quoted string, `$true`, or `$false`) is still accepted as a
syntactically valid *extra* `-and` term (so `$VpcId -and $VpcId -eq ''`
doesn't blow up the whole guard), but it never satisfies the presence
requirement on its own. `-eq $null` is still rejected outright (inverted
guard). Coverage now requires every learner var to be in `presence_vars`,
not just "mentioned somewhere in the condition".

Tests: `test_value_comparison_alone_is_not_a_presence_guard` (fail),
`test_inverted_value_comparison_fails` (fail),
`test_bare_presence_plus_value_comparison_passes` (pass),
`test_ne_null_is_a_presence_guard` (pass).

## PY-R4-002 — case-sensitive set algebra let a guard rule be skipped

The `learner_vars` computation at the old line 286 built `used & declared -
assigned` directly on original-case name sets, so a header declaring
`$VpcId` and a line using `$vpcid` produced an empty intersection — no guard
required. Rewrote it as `{v for v in used if v.lower() in _lower(declared) -
_lower(assigned)}`, matching the case-insensitive style already used by the
adjacent "missing" check.

Tests: `test_guard_var_case_mismatch_still_requires_a_guard` (fail),
`test_guard_var_case_mismatch_is_still_covered_by_a_guard` (pass).

## PY-R4-003 — a no-op "lookup" released a declared var from the guard rule

Added `_is_noop_rhs(name, rhs)`: true for a reset (delegates to
`_is_reset_rhs`), an empty right-hand side, or any right-hand side that still
mentions `name` (via the new `_references_var` helper — `"$X"` interpolation,
`$X.Trim()`, `[string]$X`, etc.). `_assigned_in`/`_assigned_in_bullet` now
exclude no-op assignments from the "set" set.

`_foreach_assigned_in` replaces the old unconditional `FOREACH` regex: it
parses the whole `foreach (Name in Collection)` header with bracket-depth
matching, and only counts `Name` as set if `Collection` is non-empty, isn't
the literal `@()`, and doesn't reference `Name` itself. This closes
`foreach ($VpcId in @()) { }` as a bypass while keeping a genuine loop var
bound over a real collection (`foreach ($MtId in $MtIds) { ... }`, used by
`ul-07`) working exactly as before.

Tests: `test_self_interpolated_assignment_does_not_unlock_an_unguarded_delete`
(fail), `test_trim_self_assignment_does_not_unlock_an_unguarded_delete`
(fail), `test_foreach_over_empty_literal_does_not_unlock_an_unguarded_delete`
(fail), `test_foreach_over_a_real_collection_still_sets_its_own_loop_var`
(pass, regression guard for the existing nested-guard test),
`test_real_lookup_still_sets_the_variable` (pass).

## PY-R4-004 — trailing `#` comments were analyzed as code

Added `_strip_comment(text)`: finds the first `#` outside any quoted string
(via `_string_spans`) and truncates there; a `#` inside a string (e.g. the
real `gl-08` shebang written into `WriteAllText`) is left alone. Every
per-line teardown check — guard parsing, `-ErrorAction`, banned-construct,
assignment/use extraction — now runs on the comment-stripped line; the raw
line is kept only for error messages and the literal `USES_HEADER`/duplicate
checks, which are deliberately comment-aware already.

Tests: `test_trailing_comment_fake_assignment_does_not_count` (fail),
`test_trailing_comment_does_not_break_a_valid_guard` (pass),
`test_trailing_comment_erroraction_is_not_flagged` (pass).

## Rule 5 — hard constructs are now banned outright in teardown lines

New `_banned_construct(line)` FAILs a teardown line containing:

- a here-string opener (`@'`/`@"`) — checked on the raw line;
- a trailing backtick line continuation — checked on the raw line;
- `Set-Variable`/`Clear-Variable`/`Remove-Variable` — checked with quoted
  string contents blanked out (`_mask_strings`), so a mention inside a
  string doesn't count;
- a literal `${` — also checked on the masked line, so `${Bucket}` used
  only for string-interpolation disambiguation (the real `ul-02` shape,
  `"Skipping ${Ul02Bucket}: ..."`) is not banned, but any other use —
  including a legitimate-looking braced guard variable — now is, per the
  rule as written;
- `&` invoking `aws`/`aws.exe`, or a full path to `aws.exe` — both checked
  on the **raw** line, deliberately not masked, since the realistic bypass
  (`& "C:\...\aws.exe"`) is itself inside quotes.

`ERROR_ACTION` is widened to match `-EA` or any case-insensitive prefix of
`-ErrorAction` whose flag text (dash included) is at least 3 characters
(`-Er` through `-ErrorAction`), built programmatically from
`"ErrorAction"[:n]` for `n` in `2..11`.

`_check_error_action` no longer splits on `;`/`{`/`}`/`|` before matching —
it masks string contents and checks the whole (comment-stripped) line at
once. This is what "match ... per line, before splitting" means in practice:
segment-splitting on a raw line was itself the bug (a `;` inside a `--query`
string produced two fake segments that separated `aws` from `-EA` and missed
a real violation), and masking-then-whole-line-check both catches that real
violation and stops "aws" appearing only inside a string from causing a
false positive.

`_parse_guard` now accepts an optional trailing `else { ... }` after a valid
`if (...) { ... }` (bracket-matched, its contents unexamined — it only runs
when the guard is false), so a harmless `else { Write-Host 'skip' }` no
longer breaks recognition of an otherwise-valid guard.

Tests: `test_here_string_in_teardown_is_banned`,
`test_backtick_line_continuation_in_teardown_is_banned`,
`test_set_variable_in_teardown_is_banned`,
`test_braced_var_construct_in_teardown_code_is_banned`,
`test_amp_aws_invoke_in_teardown_is_banned`,
`test_fullpath_aws_exe_in_teardown_is_banned`,
`test_amp_full_path_aws_exe_is_banned_as_amp_invoke` (all fail);
`test_braced_var_inside_a_string_is_not_banned`,
`test_legit_else_branch_after_a_valid_guard_passes` (both pass);
`test_abbreviated_erroraction_on_aws_fails` (fail). Also updated
`test_braced_variable_is_recognized` → renamed
`test_braced_variable_in_header_is_recognized` (moved the `${VpcId}` example
from a teardown command line, now banned, to the `# Uses:` header, where
`${Name}` is still recognized).

## Rule 6 — prose apostrophes are no longer string delimiters

Added `BACKTICK_CODE`/`_code_spans_in(bullet)`: for step bullets,
`_assigned_in_bullet` only runs assignment/foreach detection inside
backtick-delimited code spans (each span gets its own local
`_string_spans`), never over the raw prose. An apostrophe in "Don't skip:
`$VpcId = ...`." can no longer open a fake string span that swallows the
real, backtick-fenced assignment that follows it. `PROSE_ASSIGN` (the
"Copy ... into `$X`"/"Set `$X` to ..." phrasing) is unaffected — it
deliberately spans prose and a backtick-quoted variable reference, so it
still runs over the whole bullet. Confirmed against real content: all 93
`$Name =` assignments across the 42 labs' bullets already sit inside
backtick spans, so this is a pure bug fix, not a content-shape change.

Tests: `test_prose_apostrophe_does_not_mask_a_real_backtick_assignment`
(pass), `test_prose_apostrophe_alone_still_leaves_a_real_gap` (fail, sanity
check that a genuinely missing assignment is still reported).

## PY-R4-010 — loader didn't check element types inside lists

`backend/workbook/content_loader.py`:

- `_require_optional_list` already checked item types when given
  `item_type`; `load_question` now passes `item_type=str` for
  `objectiveIds` and `correctAnswerIds` (previously unchecked).
- New `_require_choice_ids`: each `choices[i]["id"]` must be a `str`
  (closes the `unhashable type: 'list'` crash in `create_attempt`'s
  `{choice.get("id") for choice in ...}` and in `score_question`'s set
  comparisons).
- `load_lab` now validates `steps` (list of dict) and `acceptanceCriteria`
  (list of str) the same way `load_question` validates its lists. This is
  what actually closes the `/api/content/summary` 500: `lab_index()` calls
  `load_lab()`, which now raises `ContentParseError` before `lab_index`'s
  own step/criteria iteration can hit a bad shape, and `content_summary_view`
  already caught `ContentParseError` → JSON 500 — no view-layer change
  needed.
- `saa_objective_domain_map`/`terraform_objective_group_map`: each row's
  `id` must now be `str` (closes an unhashable-`list`-id `TypeError`).
  `terraform_objective_group_map`'s `group` must be a real `int` — `bool`
  is explicitly rejected (Python's `bool` is an `int` subclass, so
  `True`/`False` would otherwise silently become `1`/`0`) and a float like
  `1.9` is rejected instead of truncating via the old `int(...)` call.

Tests (`backend/workbook/tests/test_scoring_and_api.py`):
`test_question_with_bad_choice_id_shape_raises`,
`test_question_with_non_string_objective_id_raises`,
`test_question_with_non_string_correct_answer_id_raises`,
`test_lab_with_non_list_steps_raises`,
`test_lab_with_non_list_acceptance_criteria_raises`,
`test_saa_objective_row_with_non_string_id_raises`,
`test_terraform_objective_row_with_bool_group_raises`,
`test_terraform_objective_row_with_float_group_raises` (all raise
`ContentParseError`); `test_question_with_good_choice_ids_loads`,
`test_lab_with_good_shape_loads`,
`test_terraform_objective_row_with_good_int_group_loads` (all load cleanly).
New real-route test `test_summary_route_500s_on_a_lab_with_bad_steps_shape`:
builds a temp `CONTENT_ROOT` with a lab whose `steps` is the string
`"not-a-list"` and asserts `GET /api/content/summary` now returns a JSON 500
containing `"Content file"` (previously an uncaught `TypeError`/HTML 500,
per `loader_r4.py`'s probe in the round-4 report).

## PY-R4-011 — lint didn't mirror the loader's shapes; duplicate rule scope

`scripts/content_lint.py`:

- `_normalize_criterion` now also strips a trailing `.`, so "The VPC no
  longer exists." and "The VPC no longer exists" are treated as the same
  criterion.
- New `check_question_shape`/`check_lab_shape`, mirroring
  `content_loader.py`'s checks (`choices` list-of-dict-with-str-id,
  `objectiveIds`/`correctAnswerIds` list-of-str, lab `steps`
  list-of-dict, `acceptanceCriteria` list-of-str), wired into the
  question and lab loops in `main()` so a shape lint can catch fails
  before the loader/API ever sees the file.
- The duplicate-criterion check moved out of the `unguided`-only loop into
  a loop over all `labs`, per the round-4 recommendation ("apply to all
  labs"). No guided lab currently has an `acceptanceCriteria` field, so
  this is a no-op for them today but no longer hard-codes the assumption
  that only unguided labs can have one.

Tests (`backend/workbook/tests/test_lab_scan.py`):
`test_trailing_period_difference_is_still_a_duplicate` (fail),
`test_different_sentences_are_not_duplicates` (pass),
`test_question_with_non_string_objective_id_fails` (fail),
`test_question_with_good_shape_passes` (pass),
`test_lab_with_non_list_acceptance_criteria_fails` (fail),
`test_lab_with_good_shape_passes` (pass).

## Deliberate behavior changes vs. round-4 (adapted adversarial expectations)

Three round-4 probes assumed a *safe* form of a construct that rule 5 now
bans unconditionally (KISS: ban the construct, don't try to tell a safe use
from an unsafe one — none of the 42 real labs need the safe form):

- **A19** (`Remove-Variable` after a delete, otherwise benign) now FAILs —
  `Set-/Clear-/Remove-Variable` are banned outright in any teardown line.
- **A27** (an `if (...) { ... }` guard split across separate
  `orderedDeletesPowerShell` array entries) now FAILs — every entry must be
  one self-contained statement (already true of all 42 real labs); this was
  never supported by design, just previously mis-scored as a false positive.
- **A28** (a guard with a backtick line continuation) now FAILs — via the
  backtick-continuation ban, which supersedes trying to join continued
  lines.
- **A50** (`If(${VpcId}){ ... }`, a braced guard variable) now FAILs — rule
  5 bans any `${` in a teardown line without a carve-out for a guard
  condition; no real lab's guard uses braced syntax.

## Adversarial re-run (adapted `adv_r4.py` → `adv_r5.py`, scratchpad-only)

50 probes, re-scored against the new scanner: **44 correct, 6 still wrong**
(down from 36 wrong in round 4). All 6 remaining mismatches are pre-existing,
explicitly out-of-scope items from the round-4 report, left as documented
limitations because F11's task list did not include them:

| # | Probe | Gap | Report ID |
|---|---|---|---|
| A21 | `[void]($VpcId = $null)` reset bypass | `_is_reset_rhs` doesn't parse a cast/void wrapper | PY-R4-005 |
| A22 | `$VpcId = $X = $null` chained reset | non-overlapping regex `finditer` | PY-R4-005 |
| A23 | `$VpcId = ' '` (whitespace) reset | not blank-trimmed before comparing | PY-R4-005 |
| A32 | `'}'` inside a string breaks guard brace-matching | `_match_balanced` isn't string-aware | PY-R4-008 |
| A47 | `Set-Variable -Value (aws ...)` as a step assignment | not a recognized bullet-assignment shape | PY-R4-009 (recommendation) |
| A48 | duplicate teardown line differing only by whitespace | not normalized before dup check | PY-R4-009 (recommendation, low value) |

Real content: **42 labs scanned, 0 with errors** (unchanged).

## Command output

`cd backend; PYTHONDONTWRITEBYTECODE=1; .venv/Scripts/python.exe manage.py test workbook`
```
Creating test database for alias 'default'...
..........................................................................................
----------------------------------------------------------------------
Ran 90 tests in 0.213s

OK
Destroying test database for alias 'default'...
```

`backend/.venv/Scripts/python.exe scripts/scan_lab_placeholders.py`
```
PASS 42 labs scanned
```

`backend/.venv/Scripts/python.exe scripts/content_lint.py`
```
questions 429 aws 310 tf 119
labs 21 + 21
lessons 23
PASS
```

No real lab failed any new or changed rule — no content file needed listing
or editing.

## Files changed

- `scripts/scan_lab_placeholders.py` — rewritten per items 1-6 above.
- `scripts/content_lint.py` — normalization + shape checks + duplicate-rule
  scope (item 8).
- `backend/workbook/content_loader.py` — element-type validation (item 7).
- `backend/workbook/tests/test_lab_scan.py` — new scanner/lint tests, one
  renamed test.
- `backend/workbook/tests/test_scoring_and_api.py` — new loader/route tests.

No file under `content/**` was touched.
