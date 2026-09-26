# Task 4.1 — Senior AWS Solutions Architect review (Round 2)

## (a) AWS's own round-1 lesson findings

AWS raised no `AWS-L41-###` findings in round 1. Nothing to mark Gone.

## (b) Second-role check of Teacher's round-1 lesson findings

Verified commit `a2ac449` against `content/lessons/lesson-4-1.json` and AWS docs directly.

- **TEACHER-L41-001** (K09, vague "tiered manually"): **Gone.** K09 now reads "...tiered with a scheduled S3 Lifecycle rule instead of S3 Intelligent-Tiering, saving the per-object monitoring fee that Intelligent-Tiering charges for handling unknown or changing access." Matches the requested fix.
- **TEACHER-L41-002** (K10, missing Glacier retrieval tiers): **Gone.** New K10 sentence states Expedited 1–5 min, Standard 3–5 hrs, Bulk (free) 5–12 hrs for Flexible Retrieval, and Deep Archive Standard within 12 hrs / Bulk within 48 hrs. Re-verified against `glacier-storage-classes.html`: Expedited "Typically restores the object in 1–5 minutes"; Standard "3–5 hours"; Bulk "5–12 hours. Bulk retrievals are free"; Deep Archive Standard "within 12 hours"; Bulk "within 48 hours at a fraction of the cost." Exact match.
- **TEACHER-L41-003** (K10, missing EFS lifecycle day thresholds): **Gone.** New K10 sentence: "By default, EFS Lifecycle Management moves files not accessed in 30 days into the IA storage class and not accessed in 90 days into the Archive storage class, though both thresholds are configurable..." Re-verified against `lifecycle-management-efs.html`: "files that are not accessed in Standard storage class for 30 days are transitioned into IA"; Archive "for 90 days." Exact match.

All three Teacher round-1 findings: **Gone** (second role confirms).

## (c) Question-by-question review (35 of 35)

| Question | Key correct/best | Distractors real, current, single-fail, non-strawman | Rationale accurate | Stem unambiguous | Citations support |
|---|---|---|---|---|---|
| k01-mc | Yes (Requester Pays) | Yes | Yes | Yes | Yes |
| k02-mc | Yes (Consolidated billing) | Yes | Yes | Yes | Yes |
| k02-mr | Yes (tags + consolidated billing) | Yes | Yes | Yes | Yes |
| k03-mc | Yes (Budgets) | Yes | Yes | Yes | Yes |
| k04-mc | Yes (S3) | Yes | Yes | Yes | Yes |
| k05-mc | Yes (AWS Backup) | Yes | Yes | Yes | Yes |
| k05-mr | Yes (plan + cold-storage lifecycle) | Yes | Yes | Yes | Yes |
| k06-mc | Yes (gp2→gp3) | Yes | Yes | Yes | Yes |
| k07-mc | Yes (S3 Lifecycle) | Yes | Yes | Yes | Yes |
| k08-mc | Yes (Transfer Family) | Yes | Yes | Yes | Yes |
| k08-mr | Yes (DataSync + Storage Gateway) | Yes | Yes | Yes | Yes |
| k09-mc | Yes (Intelligent-Tiering) | Yes | Yes | Yes | Yes |
| k10-mc | Yes (Glacier Flexible Retrieval, 3-5 hr tier) | Yes | Yes, numbers match docs | Yes | Yes |
| k11-mc | Yes (S3) | Yes | Yes | Yes | Yes |
| k11-mr | Yes (EBS + S3) | Yes | Yes | Yes | Yes |
| s01-mc | Yes (batch/Batch Operations) | Yes | Yes | Yes | Yes |
| s01-mr | Yes (multipart + expiry rule) | Yes | Yes | Yes | Yes |
| s02-mc | Yes (right-size + Elastic Volumes) | Yes | Yes | Yes | Yes |
| s02-mr | Yes (EFS elastic / FSx provisioned) | Yes | Yes | Yes | Yes |
| s03-mc | Yes (DataSync) | Yes | Yes | Yes | Yes |
| s03-mr | Yes (Transfer Family + DataSync) | Yes | Yes | Yes | Yes |
| s04-mc | Yes (EBS) | Yes, but see AWS-Q41-001 | Yes | Yes | Yes |
| s04-mr | Yes (EBS + FSx) | Yes, but see AWS-Q41-001 | Yes | Yes | Yes |
| s05-mc | Yes (128 KB floor) | Yes | Yes | Yes | Yes |
| s05-mr | Yes (two expiration actions) | Yes | Yes | Yes | Yes |
| s06-mc | Yes (EBS Snapshot Archive) | Yes | Yes | Yes | Yes |
| s06-mr | Yes (AWS Backup facts) | Yes | Yes | Yes | Yes |
| s07-mc | Yes (Storage Gateway) | Yes | Yes | Yes | Yes |
| s07-mr | Yes (Transfer Family + DataSync facts) | Yes | Yes | Yes | Yes |
| s08-mc | Yes (Glacier Deep Archive, cheapest at 180d/12hr) | Yes | Yes | Yes | Yes |
| s08-mr | Yes (Intelligent-Tiering: no retrieval fee, has monitoring fee) | Yes | Yes | Yes | Yes |
| s09-mc | Yes (early-transition cause) | Yes | Yes | Yes | Yes |
| s09-mr | Yes (90d/180d correctly matched) | Yes, numbers verified against docs | Yes | Yes | Yes |
| s10-mc | Yes (S3, cheapest baseline) | Yes, but see AWS-Q41-001 | Yes | Yes | Yes |
| s10-mr | Yes (EBS + EFS) | Yes, but see AWS-Q41-001 | Yes | Yes | Yes |

Every key traces to a sentence in the round-1-fixed lesson body; every distractor fails exactly one stated stem requirement; no strawmen (no manual/anti-pattern options); no letter references in rationale; no choice refers to another choice; no giveaway words (`since`, `even though`, `which does not`, `despite`, `requiring`, `must`, `without changing`) found in any choice text.

## (d) Numbers verified in keys/rationale

All re-checked directly against AWS docs this round: 20% (gp3 vs gp2, k06-mc), 75%/90 days (EBS Snapshot Archive, s06-mc), 90 days (Backup cold storage, k05-mr), 128 KB (IA/Glacier IR/Lifecycle floor, k04-mc/k11-mc/s05-mc/s09-mc), 30/90/180-day minimum durations (k10-mc/s08-mc/s09-mr), Glacier Flexible Retrieval's 3–5 hr Standard tier and 5–12 hr Bulk tier (k10-mc), Glacier Deep Archive's 12 hr Standard / 48 hr Bulk (s08-mc). No invented prices found; no dollar figures appear in any question.

## Issues

**AWS-Q41-001** (moderate, distractor diversity, task-wide): **Amazon EFS used as a wrong answer in 7 of 35 questions** (k11-mc, k11-mr, s02-mc, s04-mc, s04-mr, s10-mc, s10-mr) — 20%, above the "no more than 5 of 35" cap in the round-2 brief. Each individual use is a legitimate, single-fact-failing distractor (not a strawman), but the type as a whole is over-represented.
- Fix: reduce to 5 by swapping EFS out of two of the least-essential occurrences. Recommended: in **s04-mr**, replace choice `d` ("Amazon EFS file systems") with a fresh real distractor not otherwise used for this fact, e.g. "Amazon S3 buckets with a Lifecycle policy" is already choice `e` — instead use "Amazon FSx for Lustre" (real service, still fails the "needs explicit capacity increases on most deployment types" test only insofar as it's already-FSx-family, so prefer instead a service outside the FSx/S3/EFS family that clearly does not need explicit capacity management, e.g. drop to 4 choices is not allowed by format rules, so substitute "Amazon S3 Intelligent-Tiering" reworded as "An S3 bucket using S3 Storage Lens" — a real, current, S3-family feature that also never raises a capacity problem, testing the same fact from a still-valid but distinct angle). In **s10-mr**, replace the EFS-for-database distractor (`c`) with "Amazon FSx for Windows File Server for the single-instance database" (real service, still fails the "guaranteed low-latency block access" requirement, and not yet used as a distractor in this specific S10 pair-matching question).
- This is a diversity/format issue, not a factual error — no doc re-verification needed for the fix itself, only for whichever replacement service and claim the Lead Dev finally writes in.

No other issues found. No invented prices, no strawmen, no citation mismatches, no contradicted numbers.

## Checks run

- `backend\.venv\Scripts\python.exe scripts\q1_batch_check.py 4-1`: RESULT WARN (only the expected, correctly-labeled Snowball retired-service mention). All structural checks PASS: drillIds match, exam tips 21/21, duplicate 6-word openings 0, longest-is-key 6/21 = 29%, MC key spread a6/b6/c5/d4, MR key slot spread a6/b5/c5/d6/e6.
- `backend\.venv\Scripts\python.exe scripts\content_lint.py`: PASS (questions 429, lessons 23).
- All 3 of Writer B's new citation files (`cite-saa-4-1-s-multipart-upload`, `cite-saa-4-1-s-batch-operations`, `cite-saa-4-1-s-ebs-elastic-volumes`) exist, and their claims (multipart parallel upload + incomplete-upload billing; Batch Operations for large-scale jobs; Elastic Volumes resize/retype/re-tune live with no downtime) are already taught in lesson 4.1's S01/S02 sections — re-verified the Elastic Volumes claim directly against `ebs-modify-volume.html` ("you can increase the volume size, change the volume type, or adjust the performance... without detaching the volume or restarting the instance").

## Round 2 follow-up

Reviewed commit `4603939` (Writer B's AWS-Q41-001 fix) against `content/questions/q-saa-4-1-s04-mr.json` and `q-saa-4-1-s10-mr.json`.

- **s10-mr, choice c** ("Amazon FSx for Windows File Server for the single-instance database"): correct, real, current service; fails the stated "guaranteed low-latency block access" requirement only (not a duplicate of choice `b`'s FSx-capacity-planning fact); fully taught — K04 names FSx for Windows File Server as one of FSx's engines, K11/S10 establish FSx as file storage requiring provisioning "similarly to EBS," and S10 explicitly separates FSx's SMB/engine use case from "a single-instance database or boot volume needing guaranteed low-latency block access is EBS." No issue.
- **s04-mr, choice d** ("An AWS Backup vault storing recovery points"): the underlying claim is factually true (a backup vault is a managed logical container for recovery points, not a volume a team sizes or resizes) and it is a real, current AWS resource. However, this specific reasoning — that AWS Backup vault storage needs no capacity request or resize — is **not taught anywhere in lesson 4.1**. K05 covers AWS Backup's incremental-backup model and cold-storage lifecycle, but never states that vault storage is unprovisioned/auto-managed the way K04/K11/S04 state it for S3 and EFS. AWS Backup is also outside objective S04's own example list (S3, EFS, EBS, FSx). This is a teach-before-test gap, not a factual error.
  - **AWS-Q41-002** (low-moderate, s04-mr choice d / lesson K05): distractor relies on an untaught fact. Fix: add one clause to lesson 4.1's K05 paragraph, doc-supportable as written — "AWS Backup vaults are managed containers for recovery points, with no storage capacity for you to provision or resize" — placed after the existing cold-storage-tier sentence. Once added, this distractor is teach-before-test clean with no change to the question itself.

AWS-Q41-001 (EFS over-represented as a wrong answer): **Gone.** Lead Dev's count of 5/35 (k11-mc, k11-mr, s02-mc, s04-mc, s10-mc) is confirmed correct and at the cap, not over it; k05-mc/k05-mr (EFS Lifecycle Management, a different fact/type) and s02-mr (a false statement tested about EFS itself, not EFS-as-wrong-answer-for-another-service) are correctly excluded from the count.

Reviewed commit `0856d7c`: `s04-mr` choice d is now "Amazon EBS snapshots moved to the snapshot archive tier," rationale "snapshots are stored and billed by the data they hold, with no capacity to request or resize," citation `cite-saa-4-1-ebs-snapshot-archive`. Doc-verified: EBS snapshot billing "is determined by the size of the snapshot data rather than the size of the source volume" (`docs.aws.amazon.com/ebs/latest/userguide/how_snapshots_work.html`) — matches the rationale exactly, including for archived snapshots. This fact is taught in lesson 4.1: K05 establishes that AWS Backup/snapshot-style backups bill incrementally by changed data (not a provisioned capacity), and K07/K10/S06 name the EBS Snapshot Archive tier as a lifecycle/cold-tier mechanism, so a student can correctly place snapshots on the "billed by data held, nothing to provision" side of the S04 framework. It fails the stem's "capacity has to be requested or automated explicitly" test on its own distinct fact (snapshots aren't a capacity concept at all), and does not duplicate choices b (EBS volumes), c (FSx), or e (S3 with Lifecycle).

AWS-Q41-002: Gone.

Task 4.1: close

## Verdict

Task 4.1: close

Overall: approve

## Lead Dev closure note

- s04-mr and s10-mr were changed after the Student text-packet run: the AWS-Q41-001 and AWS-Q41-002 distractor swaps. Both keys are unchanged.
- AWS (the reporter) confirmed both fixes. Lead Dev checked the EFS count with a script (5 of 35).
