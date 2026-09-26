# Lesson 4.1 — Senior AWS Solutions Architect review (Round 1)

Reviewed against `content/lessons/lesson-4-1.json` (commit `8f8a097`) and the writer's claim table in `reports/fix-loop-r2/q1/lesson-4-1-impl.md`.

## Per-section verdicts

- K01 Requester Pays — correct, matches doc (row 1–2 verified).
- K02 cost allocation tags / consolidated billing / Billing Conductor — correct as stated; not independently re-verified beyond the whitepaper cite (low risk, standard AWS overview language).
- K03 Cost Explorer / Budgets / CUR+Data Exports — correct contrast; matches shared rule of "visualize vs alert vs granular line items."
- K04 storage service cost model (S3/EFS/EBS/FSx) — correct, consistent with 3.1's service descriptions.
- K05 AWS Backup + cold storage — correct; 90-day minimum verified against docs (row 7).
- K06 gp3/gp2/io1/io2/st1/sc1 cost — correct; 20% gp3/gp2 differential verified (row 8); consistent with lesson 3.1's EBS section, no contradiction.
- K07 data lifecycle concept — correct, no numeric claims to check.
- K08 DataSync/Transfer Family/Storage Gateway — correct, consistent with 3.1.
- K09 access-pattern framing — correct, qualitative.
- K10 S3 cold tiering ladder — **verified exactly against docs**: 30d (Standard-IA/One Zone-IA), 90d (Glacier IR/Flexible), 180d (Deep Archive), 128 KB minimum billed size for IA classes and Glacier IR (rows 12–14). Storage Lens free/advanced tiers correct (row 15).
- K11 storage type billing contrast — correct; S3 Express One Zone "50% lower request cost" verified verbatim (row 16).
- S01 batch/multipart — correct; multipart mechanics reused from 3.1 per the report, acceptable since no new number is asserted.
- S02 EBS right-sizing / Elastic Volumes — correct, consistent with 3.1.
- S03 lowest-cost transfer — correct; Snow Family correctly labeled "closed to new customers," Data Transfer Terminal used as the current answer, no strawman.
- S04 auto scaling applicability — correct.
- S05 S3 Lifecycle mechanics — **verified**: 128 KB default transition floor and size-filter override match docs exactly (row 18); minimum-duration-before-transition constraint matches docs (row 19).
- S06 backup/archival selection — correct; EBS Snapshot Archive 75%/90-day claim verified verbatim (row 10).
- S07 migration service selection — correct, consistent with 3.1.
- S08 tier selection synthesis — correct, consistent with K09/K10.
- S09 lifecycle schedule design — correct; the example schedule (30d IA → 90d Glacier FR → 180d Deep Archive) is internally consistent with the verified minimum durations.
- S10 cheapest-service synthesis — correct, consistent with K04/K11.

## Issues

None found at severity requiring a fix. No AWS-L41-### issues raised in round 1.

## Verification notes

- Spot-checked 9 claim-table rows directly against AWS docs (rows 7, 8, 10, 11, 12, 13, 14, 18, 19) — all numbers match verbatim: S3 Standard-IA/One Zone-IA 30-day/128 KB, Glacier Instant/Flexible 90-day, Deep Archive 180-day, Glacier IR 128 KB minimum object size, EBS Snapshot Archive 75%/90-day, EFS Lifecycle 30-day IA / 90-day Archive, gp3 20% cheaper than gp2, S3 Lifecycle 128 KB default transition floor with size-filter override, minimum-duration-before-transition rule.
- No invented dollar figures: only percentages (20%, 50%, 75%), all doc-cited and verified above. The one `$` figure ("$10 budget alerts warn") is the standard cross-lesson safety-warning boilerplate used identically in all 14 lesson files, not a lesson-specific claim — no citation needed.
- Contrasts required by the task (storage-class-by-access-pattern, Cost Explorer vs Budgets vs CUR/Data Exports vs Storage Lens, Requester Pays) are all present and correctly framed.
- Coverage: all 21 `SAA-4.1-*` objective ids (K01–K11, S01–S10) from `content/objectives/saa_c03.json` have a matching `###` section, in order, each ending in an **Exam tip:**.
- Citations: all 12 new `cite-saa-4-1-*` files exist on disk and match `citationIds`; no unresolved citation ids (`q1_batch_check.py 4-1` reports zero on lesson lines).
- Retired-service handling: AWS Snow Family correctly labeled "closed to new customers" in S03; no other retired/renamed services used as a current answer.
- No contradiction found against lessons 2.2, 3.1, or 3.5: cross-checked EBS volume types (gp3/gp2/st1/sc1), EFS storage classes, S3 Glacier/One Zone terminology, and Storage Gateway/DataSync framing — all consistent.
- Lint: `python manage.py`-independent `scripts\content_lint.py` → **PASS** (23 lessons). `q1_batch_check.py 4-1` shows only FAILs on the untouched placeholder questions (out of scope for this lesson-only task, confirmed by inspection — they are all `q-saa-4-1-s04..s10` style stems that still paste objective text), not on the lesson itself.

## Verdict

Lesson 4.1: approve for question writing

Overall: approve
