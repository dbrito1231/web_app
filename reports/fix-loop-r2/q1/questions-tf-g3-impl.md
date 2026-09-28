# Questions tf-g3 (Core Terraform workflow) — implementation report

## Outline

- Wrote 21 questions (3 per objective: mc, mc2, mr) replacing the 21 placeholder files, one set per objective tf.004.3a–3g in order.
- `id`, `type`, `module`, `objectiveIds`, `selectCount` kept unchanged from the placeholders. `citationIds` set to the single g3 citation for that question's own objective (e.g. `cite-tf-g3-init` for all 3b questions). `mcpStatus: "verified"`, `reviewedOn: "2026-09-26"` on every question.
- Every scenario uses a distinct fictional company and a distinct 6-word stem opener (`stem_echo_check.py` confirms no duplicate openings and no giveaway).
- Teach-before-test: every flag or command behavior a question turns on (`-upgrade`, `-auto-approve`, `-out`, `-target`, `-refresh-only`, `-destroy`, `-check`, `-recursive`, `-backend=false`, the dependency lock file) is present in the fixed lesson body — checked by substring search after the lesson fixes landed, not assumed.
- Every distractor is a real Terraform command or flag (verified against the seven doc pages fetched for the lesson) applied to a scenario that meets every stated requirement but one; no strawman actions (no "an engineer does it by hand," no manual non-tool steps).
- No banned giveaway words (`since`, `even though`, `which does not`, `despite`, `requiring`, `must`, `without changing`, `because`, `by default`) appear in any choice text (only in stems/rationale, where they are fine).
- Added a `curated TERMS` block to `scripts/distractor_type_audit.py` for the 6 Terraform commands and 9 flags this lesson introduces, since the existing list only covered tf-g1/g2 vocabulary.

## Distractor-type table (15% of 21 = 3 max)

| Type | Count | % | Questions |
|---|---|---|---|
| `terraform fmt` | 3 | 14% | 3b-mc, 3c-mc, 3f-mc |
| `terraform validate` | 3 | 14% | 3b-mc, 3g-mc, 3g-mc2 |
| `-upgrade` | 3 | 14% | 3b-mc2, 3b-mr, 3f-mc2 |
| `-recursive` | 3 | 14% | 3c-mc, 3f-mc, 3g-mc2 |
| `terraform init` | 3 | 14% | 3c-mc, 3f-mc, 3f-mc2 |
| `-destroy` | 3 | 14% | 3d-mc, 3d-mc2, 3e-mr |
| `-target` | 3 | 14% | 3d-mc, 3e-mc, 3f-mc2 |
| `-out` | 3 | 14% | 3d-mc, 3d-mc2, 3d-mr |
| `terraform destroy` | 2 | 10% | 3b-mc, 3c-mc |
| `dependency lock file` | 2 | 10% | 3b-mc2, 3b-mr |
| `-backend=false` | 2 | 10% | 3c-mc, 3f-mc |
| `-refresh-only` | 2 | 10% | 3d-mc2, 3e-mc |
| `-check` | 2 | 10% | 3e-mc, 3g-mc |
| `-auto-approve` | 2 | 10% | 3e-mc2, 3f-mc |
| `terraform apply` | 2 | 10% | 3f-mc, 3f-mc2 |
| `terraform plan` | 1 | 5% | 3f-mc2 |

No type exceeds the 3-question cap. `distractor_type_audit.py tf-g3`: PASS.

Getting under the cap took real rework: the first draft used full `terraform <command> <flag>` phrasing in nearly every choice (comparing sibling commands), which pushed `terraform apply` to 7/21 and `-target` to 6/21. Fixed by (a) writing same-command flag-differentiation questions (3d, 3e's internal comparisons, 3g) as bare flags since the base command is already fixed by the stem, eliminating repeated `terraform plan`/`terraform apply` mentions entirely from those questions, and (b) diversifying the remaining cross-command distractors (e.g. `terraform init -backend=false` in place of a second `terraform apply -auto-approve`) so no single command name is reused as a wrong answer more than 3 times across the task.

## Balance

- MC key letters: a=3, b=4, c=4, d=3 (14 MC questions).
- MR key slots: a=3, b=2, c=3, d=3, e=3 (7 MR questions, 14 correct slots).
- MR key sets: 7 distinct pairs, none repeated (`b,d` `a,c` `c,e` `a,d` `b,e` `a,e` `c,d`) — no set appears more than once, well under the "no more than 40% repeat" bar.
- Longest-choice-is-key: 4/14 MC = 29% (cap 35%). Two ties were found and fixed during balancing: `3a-mc`'s "Write"/"Apply" length tie (lengthened the `Init` distractor to "Initialize the working directory") and `3e-mc`'s `-refresh-only`/`-auto-approve` 13-character tie (lengthened the `-target` distractor to "-target <address>").

## Stem/key echo

`stem_echo_check.py tf-g3`: PASS, no giveaway or bulk echo. Two giveaways were found and fixed during drafting, both from a key literally repeating a stem word that no distractor shared: `3a-mr`'s "reviewing"/"change" (stem reworded to "looks at every infrastructure update... around plan review," and the key changed to start "Review the plan's..." so `review` also appears in a distractor) and `3f-mr`'s "approaches" (key rewritten from "Both approaches end with..." to "Both routes end with..." since no distractor used the plural "approaches").

## Retired / renamed / closed-to-new-customers findings

None (no AWS content in this lesson).

## Checks

- `content_lint.py`: PASS.
- `q1_batch_check.py tf-g3`: PASS — lesson lines PASS as before; question lines now PASS too (no objective-text paste, no placeholder stems, all `citationIds` set, `mcpStatus`/`reviewedOn` verified/2026-09-26, MR stems carry "(Select TWO.)", no duplicate 6-word openings, longest-is-key 4/14=29%, MC key positions balanced, MR key slots and sets balanced).
- `distractor_type_audit.py tf-g3`: PASS, table above, max 3/21 (14%) per type.
- `stem_echo_check.py tf-g3`: PASS, 0 unwaived giveaway, 0 waived, 0 bulk echo.
- `claim_prose_check.py tf-g3`: PASS (unchanged from the lesson-fix pass; questions do not add new lesson claims).
