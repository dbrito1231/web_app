# Implementation report: Batch F6 (Amendment 2, item N8)

Interim fix for `rationale` fields in `content/questions/*.json` that referred to
choices by on-screen letter (A/B/C/...). Answer keys were rotated and the app
shuffles choices at render time, so any letter reference in a rationale is
stale or meaningless to the learner. `q-saa-1-1-*.json` (19 files, being
rewritten separately) were explicitly excluded and confirmed untouched.

## Scope

- 429 question files total in `content/questions/`.
- 410 candidate files after excluding `q-saa-1-1-*.json`.
- **185 files changed** (only the `rationale` field in each).

## Detection regex

A rationale was flagged as letter-referencing if it matched any of:

```
\bOptions?\s+[A-F]\b
\bChoices?\s+[A-F]\b
\([A-F]\)
\b[A-F]\s+and\s+[A-F]\b
\b[A-F]\s+or\s+[A-F]\b
\b[A-F](?:\s*,\s*[A-F])+\b
\b[A-F](?:/[A-F])+\b
\b[A-F]\s+is\b
\b[A-F]\s+are\b
\bletters?\s+[A-F]\b
\b[A-F]\s*[–-]\s*[A-F]\b        # en dash or hyphen, e.g. "A-C"
```

No bare `\b[A-F]\b` pattern was used, so ordinary words like "A design" or
abbreviations like "AWS" are never matched; every pattern requires a
letter-specific construction (a parenthesized letter, a letter list/range, a
letter directly followed by a linking verb, etc.).

Scanning all 429 files with this regex after the fix reports **0 remaining
letter references**.

## What was actually found

Every one of the 185 hits reduced to exactly two literal, reused rationale
strings (the content had been templated, and the answer-key rotation left the
templates stale relative to `correctAnswerIds`):

1. `"A and B are sound exam/lab practice. C/D/E violate credential, teardown, or root-user rules."` — 148 files, all `mr` (select-two) questions built from the same 5-choice pool (skip teardown / use root creds / design against requirement / validate with docs / store keys in git). Rewritten to name the two current `correctAnswerIds` choices by their actual text.
2. `"Option A aligns with the published objective wording. B violates root/MFA guidance. C ignores teardown. D misstates AWS Budgets behavior (alerts do not stop spend)."` — 37 files, `mc` "quick check" questions where the correct choice is always `"Apply the objective directly: <objective wording>"` and the three distractors are a fixed set (root/MFA violation, no-teardown, budget-alert misstatement). Rewritten to name the current correct choice by its actual (per-question) text.

A generic by-text fallback template exists in the script for any rationale
that matched the detection regex but not these two literal templates; it was
not exercised because no such case existed in this batch.

## Rewrite rules applied

- Rationale text was rebuilt from `choices` + `correctAnswerIds` at write time, so it is always consistent with the current answer key.
- All other fields (`stem`, `choices`, `correctAnswerIds`, `selectCount`, ids, objective/citation ids, module, difficulty, `reviewedOn`, `mcpStatus`) were left untouched.
- Original reasoning content (credential/teardown/root-user rule violations; root/MFA, teardown, and AWS Budgets distractor reasoning) was preserved, just attached to choice text instead of letters.

## 10 before → after examples

1. `q-saa-1-2-k02-mr.json`
   - Before: `A and B are sound exam/lab practice. C/D/E violate credential, teardown, or root-user rules.`
   - After: `Correct: 'Design against the stated requirement and document tradeoffs' and 'Validate with official documentation before applying'. The other choices break credential, teardown, or root-user rules.`
2. `q-saa-1-2-k05-mr.json` — same before/after pair as above (shared template, same choice pool).
3. `q-saa-1-2-s01-mr.json` — same before/after pair as above.
4. `q-saa-1-2-s02-mr.json` — same before/after pair as above.
5. `q-saa-1-2-s03-mr.json` — same before/after pair as above.
6. `q-tf-004-1a-mc2.json`
   - Before: `Option A aligns with the published objective wording. B violates root/MFA guidance. C ignores teardown. D misstates AWS Budgets behavior (alerts do not stop spend).`
   - After: `Correct: 'Apply the objective directly: Explain what IaC is'. The other choices break root/MFA guidance, skip teardown, or misstate AWS Budgets behavior (alerts do not stop spend).`
7. `q-tf-004-1b-mc2.json`
   - After: `Correct: 'Apply the objective directly: Describe the advantages of IaC patterns'. The other choices break root/MFA guidance, skip teardown, or misstate AWS Budgets behavior (alerts do not stop spend).`
8. `q-tf-004-1c-mc2.json`
   - After: `Correct: 'Apply the objective directly: Explain how Terraform manages multi-cloud, hybrid cloud, and service-agnostic workflows'. The other choices break root/MFA guidance, skip teardown, or misstate AWS Budgets behavior (alerts do not stop spend).`
9. `q-tf-004-2a-mc2.json`
   - After: `Correct: 'Apply the objective directly: Install and version Terraform providers'. The other choices break root/MFA guidance, skip teardown, or misstate AWS Budgets behavior (alerts do not stop spend).`
10. `q-tf-004-2b-mc2.json`
    - After: `Correct: 'Apply the objective directly: Describe how Terraform uses providers'. The other choices break root/MFA guidance, skip teardown, or misstate AWS Budgets behavior (alerts do not stop spend).`

(Items 2-5 illustrate that the 148-file group is a single literal template
reused verbatim across files that share the same 5-choice pool and the same
correct pair; each file's `choices`/`correctAnswerIds` were still read from
that file individually, not hardcoded, so any future file with a different
key would get a different rewritten rationale.)

## Verification

- **Letter-reference sweep** (script, all 429 files, same regex as above): `0` remaining matches.
- **Field-isolation check**: parsed JSON compared field-by-field, before vs. after, for all 429 files (185 changed + 244 untouched, including all 19 `q-saa-1-1-*.json`). Result: every changed file differs in `rationale` only; `q-saa-1-1-*.json` files show zero diffs (confirmed untouched).
- **Content lint**:
  ```
  > backend\.venv\Scripts\python.exe scripts\content_lint.py
  questions 429 aws 310 tf 119
  labs 21 + 21
  lessons 23
  PASS
  ```

## Files touched

185 files under `content/questions/` (rationale field only). No files outside
`content/questions/` were modified. No git commands were run.
