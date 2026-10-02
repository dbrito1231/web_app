# Plan P2: Scope the distractor audit terms

Author: Lead Developer. Status: **draft, awaiting user approval.** Phase 1 of `master_open_items_20261002.plan.md`.

## Problem (facts checked 2026-10-02)

- `scripts/distractor_type_audit.py` has one global `TERMS` list shared by both exams.
- It FAILs on 9 closed SAA tasks: 1-2, 2-1, 2-2, 3-1, 3-2, 3-3, 3-4, 3-5 and 4-1. The flagged terms are mostly the task's own subject (for example RDS, Aurora and DynamoDB in 3-3 Databases, and Glue, EMR and Athena in 3-5 Analytics). These FAILs predate the Q1 rewrite of those tasks.
- The Terraform tasks already follow a rule written in the script's comments: "bare subject vocabulary is deliberately excluded", because a term the lesson is *about* is not a reused distractor type.
- A FAIL that everyone ignores trains people to ignore the script, and that is how the tf-g7 `identity` term silently broke task 1-1.

## Options (KISS)

1. **Per-task subject exclusions (recommended).** Add a small `SUBJECT` map, task to terms that are that task's own subject. The Teacher writes it from each lesson's objectives. Those terms are skipped for that task only. This applies the existing Terraform rule to the SAA tasks.
2. **Split by exam only.** Have separate `SAA_TERMS` and `TF_TERMS` lists, chosen by task prefix. This stops cross-exam false hits like `identity`, but the 9 SAA FAILs remain, because they are SAA terms in SAA tasks.
3. **Record and downgrade.** Keep the script, but report closed SAA tasks as WARN instead of FAIL, and list them in the register. This is cheap, but it hides any real reuse.

## Recommended approach (option 1, plus option 2's split, which is one extra line)

1. Run the audit on all 22 tasks and save the output (the baseline).
2. The Teacher proposes the `SUBJECT` exclusions per SAA task, from each task's objective bullets. It also says which flagged terms are a **real** reused distractor type rather than subject vocabulary. Those stay counted.
3. The Lead Dev adds the map, plus the exam split, to the script, with a comment citing this plan.
4. Re-run all 22 tasks.
   - Any task still FAILing after exclusions has real distractor reuse. **It is reported, not fixed here.** Fixing questions in closed tasks would be a separate content plan.
   - The Teacher confirms that no exclusion hides a real reuse.

## Files

`scripts/distractor_type_audit.py`; `HANDOFF.md` (the check-suite table); the register.

## Risks

- Over-excluding hides genuine reuse. The mitigation is that the Teacher rules term by term and the before and after outputs are both kept in `reports/`.
- Tasks tf-g5 to tf-g8 must still PASS with identical counts.

## Tests

The audit on all 22 tasks, before and after (both saved); `content_lint.py`; `test_q1_letter.py`.

## Learning content affected

No content changes. Only a check script changes. The Teacher rules on the exclusions, because they decide what counts as reuse.
