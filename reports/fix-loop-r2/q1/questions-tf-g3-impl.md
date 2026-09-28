# Questions tf-g3 (Core Terraform workflow) — implementation report

## Round 2 — Lead Dev pre-check fixes (commit 341afe7)

1. **Dependents/dependencies contradiction** (paired with the lesson fix above). `3f-mc2`'s stem and rationale said `destroy -target` removes the resource "and whatever depends on it" — backwards; per the destroy page it is "a particular resource and its dependencies" (what the resource depends on), confirmed by the plan page's `-target` mechanism description. Fixed `3f-mc2`'s wording to "anything that database resource itself depends on." Rewrote `3f-mr` entirely around the corrected, doc-accurate discriminator: an instance that references (depends on) a security group. `destroy -target` on the instance also destroys the security group (key a); deleting only the instance's block and applying leaves the security group untouched (key b) — the two routes now genuinely diverge in the question, matching the lesson's corrected "equivalent only when there are no dependencies" teaching. Key moved: `3f-mr` was `{a, e}`, now `{a, b}` (new content, not just a relettering — the old choice-a claim, "both routes end with everything else untouched," is now one of the *wrong* choices, `c`).
2. **Self-explaining choices, reworded.** `3g-mc` choice c ("leave off any flag, which only reaches the current directory") → "run the command with no additional flag" — states the action, not the reason it fails. `3g-mc2`'s equivalent choice was removed entirely by rewording the whole question (see next point).
3. **Repetitive option sets, reworked one question per pair.** `3d-mc2` no longer asks "which flag narrows a plan" (same 4-flag pool as `3d-mc`); it now asks what a `plan -target` run actually *covers* when the target has a dependency, testing the target-extends-to-dependencies consequence (mirroring `3e-mc2`'s model). `3g-mc2` no longer asks "which command formats vs. checks" (same pool as `3g-mc`); it now asks what actually happens when `fmt -check` runs against an unformatted file (file untouched, non-zero exit, name listed) — a consequence question, not a flag-naming one. `3d-mc` and `3g-mc` are unchanged (each pair now has one flag-identification question and one behavior/consequence question).

Verifying `-target`'s direction required a fresh WebFetch of both the destroy and plan pages this turn (not assumed from the earlier lesson pass), since the original wording in both the lesson and these two questions had been asserting the wrong direction consistently — a single error propagated, not two independent ones.

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
| `-upgrade` | 3 | 14% | 3b-mc2, 3b-mr, 3f-mc2 |
| `terraform init` | 3 | 14% | 3c-mc, 3f-mc, 3f-mc2 |
| `-target` | 3 | 14% | 3d-mc, 3e-mc, 3f-mc2 |
| `terraform validate` | 2 | 10% | 3b-mc, 3g-mc |
| `terraform destroy` | 2 | 10% | 3b-mc, 3c-mc |
| `dependency lock file` | 2 | 10% | 3b-mc2, 3b-mr |
| `-backend=false` | 2 | 10% | 3c-mc, 3f-mc |
| `-recursive` | 2 | 10% | 3c-mc, 3f-mc |
| `-out` | 2 | 10% | 3d-mc, 3d-mr |
| `-destroy` | 2 | 10% | 3d-mc, 3e-mr |
| `-check` | 2 | 10% | 3e-mc, 3g-mc |
| `-auto-approve` | 2 | 10% | 3e-mc2, 3f-mc |
| `terraform apply` | 2 | 10% | 3f-mc, 3f-mc2 |
| `-refresh-only` | 1 | 5% | 3e-mc |
| `terraform plan` | 1 | 5% | 3f-mc2 |

No type exceeds the 3-question cap. `distractor_type_audit.py tf-g3`: PASS. (Reworking `3d-mc2` and `3g-mc2` into consequence questions dropped `-recursive` and `terraform validate` out of `3g-mc2`'s choice set entirely, which is why their counts read lower than the first draft.)

Getting under the cap took real rework: the first draft used full `terraform <command> <flag>` phrasing in nearly every choice (comparing sibling commands), which pushed `terraform apply` to 7/21 and `-target` to 6/21. Fixed by (a) writing same-command flag-differentiation questions (3d, 3e's internal comparisons, 3g) as bare flags since the base command is already fixed by the stem, eliminating repeated `terraform plan`/`terraform apply` mentions entirely from those questions, and (b) diversifying the remaining cross-command distractors (e.g. `terraform init -backend=false` in place of a second `terraform apply -auto-approve`) so no single command name is reused as a wrong answer more than 3 times across the task.

## Balance

- MC key letters: a=3, b=4, c=4, d=3 (14 MC questions).
- MR key slots: a=3, b=3, c=3, d=3, e=2 (7 MR questions, 14 correct slots).
- MR key sets: 7 distinct pairs, none repeated (`b,d` `a,c` `c,e` `a,d` `b,e` `a,b` `c,d`) — no set appears more than once. (`3f-mr`'s set changed from `a,e` to `a,b` when it was rewritten around the dependents/dependencies fix; still distinct from every other set.)
- Longest-choice-is-key: 4/14 MC = 29% (cap 35%). Ties/overlengths were found and fixed at two points: initial balancing (`3a-mc`'s "Write"/"Apply" length tie, fixed by lengthening the `Init` distractor; `3e-mc`'s `-refresh-only`/`-auto-approve` 13-character tie, fixed by lengthening the `-target` distractor), and again after reworking `3d-mc2` into a consequence question, whose new key was briefly the longest choice by a wide margin — trimmed to a bare resource list once the reasoning clause was redundant with the rationale.

## Stem/key echo

`stem_echo_check.py tf-g3`: PASS, no unwaived giveaway, 1 advisory bulk echo (`3f-mr`, key shares more stem wording than the best distractor — read and judged not a defect, since the shared terms are the scenario's own resource names). Giveaways found and fixed during drafting and rework, each from a key literally repeating a stem word that no distractor shared: `3a-mr`'s "reviewing"/"change"; `3f-mr`'s "approaches" (both fixed during round 1); and, introduced by the round-2 rework and fixed in the same pass, `3d-mc2`'s and `3f-mr`'s "target" (added the word "target" to a non-key distractor in each so it no longer singled out the key).

## Retired / renamed / closed-to-new-customers findings

None (no AWS content in this lesson).

## Checks

- `content_lint.py`: PASS.
- `q1_batch_check.py tf-g3`: PASS — lesson lines PASS; question lines PASS (no objective-text paste, no placeholder stems, all `citationIds` set, `mcpStatus`/`reviewedOn` verified/2026-09-26, MR stems carry "(Select TWO.)", no duplicate 6-word openings, longest-is-key 4/14=29%, MC key positions balanced, MR key slots and sets balanced).
- `distractor_type_audit.py tf-g3`: PASS, table above, max 3/21 (14%) per type.
- `stem_echo_check.py tf-g3`: PASS, 0 unwaived giveaway, 0 waived, 1 advisory bulk echo (`3f-mr`, read and not a defect).
- `claim_prose_check.py tf-g3`: PASS (the `-target`/dependencies wording fix in the lesson didn't add new numeric claims).
- All four re-run against the full 21-question set after the round-2 rework, not just the touched files, per the "After applying a fix" rule.
