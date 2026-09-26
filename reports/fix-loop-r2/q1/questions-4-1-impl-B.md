# Task 4.1 — Writer B (skill questions s01–s10) implementation report

Scope: `content/questions/q-saa-4-1-s01..s10-mc.json` and `-mr.json` (20 files), plus 3 new citation
files reused across these questions. `k*` files (Writer A) were not touched.

New citations added (existing lesson citations did not cover S3 multipart/batch pricing or EBS
Elastic Volumes resizing):
- `cite-saa-4-1-s-multipart-upload` — AWS "Uploading and copying objects using multipart upload"
- `cite-saa-4-1-s-batch-operations` — AWS "Performing large-scale batch operations on Amazon S3 objects"
- `cite-saa-4-1-s-ebs-elastic-volumes` — AWS "Amazon EBS Elastic Volumes"

All other citations reuse the lesson's own citation set or existing DataSync/Transfer
Family/Storage Gateway citations from lessons 2.1 and 3.1 (`cite-saa-2-1-transfer-family-what-is`,
`cite-saa-3-1-datasync-what-is`, `cite-saa-3-1-storage-gateway-types`).

## Per-question table

| Question | Objective | What it tests | Key | Lesson quote (key) | Lesson quote (distractors) |
|---|---|---|---|---|---|
| s01-mc | S01 | Many small S3 uploads → batch/Batch Operations cuts per-request cost | a | "a workload that uploads one object at a time... pays far more in request charges than the same data grouped into fewer, larger objects" | Lifecycle/Intelligent-Tiering/Transfer Acceleration each address a different cost lever (class, monitoring, latency), not request count |
| s01-mr | S01 | Multipart upload for reliability + lifecycle rule to expire incomplete uploads | a, b | "split the upload into parts... a failed part only needs to be retried" / "incomplete multipart uploads still bill for the storage they hold until an S3 Lifecycle rule expires them" | Object Lock, Requester Pays, CRR are real but unrelated features |
| s02-mc | S02 | Size EBS realistically, use Elastic Volumes to grow later | b | "the safer strategy is to start at a realistic size and scale up when metrics justify it rather than over-provisioning up front" | io2 max IOPS = performance not capacity; EFS drops the block-storage requirement; upfront max sizing = the named bad practice |
| s02-mr | S02 | EFS elastic throughput and FSx billing models | c, d | "S3, EFS, and FSx with elastic throughput remove this decision for storage capacity entirely, since they bill actual usage" / "FSx requires provisioning storage... similarly to EBS" | False statements about EFS needing fixed size, FSx billing like S3, gp3 billing actual usage |
| s03-mc | S03 | Lowest ongoing fee for a recurring bulk transfer over an existing link | c | "AWS DataSync is normally the lowest-cost method: it is billed per GB transferred with no appliance to provision" | Storage Gateway (hybrid, not migration), Transfer Family (partner protocol), Data Transfer Terminal (for network-infeasible transfers) |
| s03-mr | S03 | Matching Transfer Family (partner SFTP) and DataSync (finite HDFS migration) | a, e | "AWS Transfer Family... exchanging files with external partners who require one of those legacy protocols" / "recurring, over the network, verified transfer is DataSync" | Storage Gateway/Transfer Family swapped onto the wrong requirement |
| s04-mc | S04 | Identify which layer needs a built capacity-expansion process | d | "EBS volumes do not auto-scale: a volume stays at its provisioned size... until you resize it" | S3/EFS auto-scale; Intelligent-Tiering only changes storage class, not capacity behavior |
| s04-mr | S04 | Same fact, EBS + FSx both need explicit capacity requests | b, c | "FSx file systems similarly need capacity increases requested explicitly on most deployment types" | S3 and EFS (plain or with a Lifecycle policy) never raise this problem |
| s05-mc | S05 | 128 KB default minimum object size blocks small-object transitions | a | "by default only objects of at least 128 KB transition, though a rule can add an object-size filter" | Versioning, filter type, and duration timing are unrelated to the size floor |
| s05-mr | S05 | Expiration actions for incomplete multipart uploads and noncurrent versions | d, e | "expiration actions (delete the current version, noncurrent versions, delete markers, or incomplete multipart uploads after N days)" | Transition action, Object Lock, replication don't delete/expire anything |
| s06-mc | S06 | EBS-only long-term retention → EBS Snapshot Archive tier | b | "archiving offers up to about 75% lower storage cost for snapshots kept 90 days or longer" | AWS Backup is over-scoped (cross-service, not needed); manual Glacier copy misapplies object storage to snapshots; Vault Lock is immutability not cost |
| s06-mr | S06 | AWS Backup spans multiple resource types, incremental after first backup | a, b | "AWS Backup centralizes policy-driven backup across many AWS resource types... incrementally, so ongoing storage cost reflects only the changed data" | EBS Snapshot Archive and Glacier Deep Archive are wrong-scoped; "full backup every time" is false |
| s07-mc | S07 | Ongoing hybrid access (not a finished migration) → Storage Gateway | c | "A requirement to keep serving on-premises applications from AWS storage indefinitely... calls for Storage Gateway instead — that is hybrid access, not a migration you finish and turn off" | One-time/recurring DataSync jobs finish and disconnect; Transfer Family is for partner protocols |
| s07-mr | S07 | Feature-level facts about Transfer Family and DataSync billing/protocols | d, e | "AWS Transfer Family... managed SFTP, FTPS, AS2... backed by S3 or EFS" / "AWS DataSync's job... billed per GB transferred with no appliance to run" | Storage Gateway billed like DataSync is false; Transfer Family needing an EC2 FTP server is the opposite of what it avoids; DataSync doesn't provide SFTP endpoints |
| s08-mc | S08 | Annual-or-rarer access + 12hr retrieval + 180-day retention → Deep Archive is cheapest | d | "for annual-or-rarer access, Glacier Deep Archive" | Flexible Retrieval meets time/duration but costs more; Standard-IA and Intelligent-Tiering fit different access patterns |
| s08-mr | S08 | Intelligent-Tiering: no retrieval fee, but a monitoring fee | a, e | "S3 Intelligent-Tiering, which carries no retrieval fee in exchange for a small monitoring fee" | False claims about Standard-IA, One Zone-IA, and Glacier Instant Retrieval |
| s09-mc | S09 | Early-transition charge from violating a class's minimum storage duration | a | "scheduling one earlier than the minimum still bills for the shortfall" | A true-but-irrelevant duration fact, and unrelated filter/size facts |
| s09-mr | S09 | Correct minimum-duration numbers for Flexible Retrieval (90d) and Deep Archive (180d) | b, c | "90 days for Glacier Instant and Flexible Retrieval, 180 days for Deep Archive" | Numbers swapped onto the wrong class (30d, 90d, 90d) |
| s10-mc | S10 | No POSIX need, static content → S3 is the cheapest baseline | b | "a data lake or static content workload with no need for a POSIX file interface belongs on S3... the cheapest baseline" | FSx premium, EFS higher per-GB rate, EBS provisioned-capacity billing don't fit |
| s10-mr | S10 | Match EBS (low-latency block DB) and EFS (POSIX, no capacity planning) | d, e | "A single-instance database... needing guaranteed low-latency block access is EBS" / "Shared, POSIX-compliant file access with unpredictable growth belongs on EFS... needs no capacity planning" | S3 has no block interface; FSx needs provisioning; EFS doesn't fit a low-latency block DB |

## Distractor-type table (max any type: 2 of 20; cap was 3)

| Type | Count | Questions |
|---|---|---|
| Wrong cost lever (different dimension than requested) | 1 | s01-mc |
| Unrelated real AWS feature | 1 | s01-mr |
| Over-provisioning practice (real, costly) | 1 | s02-mc |
| False billing/feature statement | 2 | s02-mr, s07-mr |
| Wrong service for transfer scenario | 2 | s03-mc, s07-mc |
| Wrong service/requirement pairing | 2 | s03-mr, s10-mr |
| Wrong layer (auto-scaling confusion) | 2 | s04-mc, s04-mr |
| Wrong-cause misattribution | 2 | s05-mc, s09-mc |
| Wrong action type (transition vs. expiration vs. lock/replication) | 1 | s05-mr |
| Wrong-scope service (over/under-scoped) | 1 | s06-mc |
| Wrong service for resource type | 1 | s06-mr |
| Wrong tier (meets time/duration, fails cost) | 1 | s08-mc |
| False statement about tier behavior | 1 | s08-mr |
| Wrong numeric threshold | 1 | s09-mr |
| Wrong service for workload (POSIX/engine mismatch) | 1 | s10-mc |

## Checks

- `q1_batch_check.py 4-1`: RESULT WARN — the only WARN is a pre-existing lesson mention of the
  retired Snowball Edge, already correctly labeled ("never the retired Snowball Edge"); not part of
  writer B's files. All other checks PASS, including duplicate-opening (0), longest-is-key (6/21 =
  29%, under 35%), MC key spread (a6/b6/c5/d4), MR key slot spread (a6/b5/c5/d6/e6) — these totals
  are task-wide (k + s combined).
- `content_lint.py`: PASS (429 questions, 23 lessons).

No lesson additions requested — every key and distractor traces to lesson 4.1's existing text.

## AWS round-2 fix

AWS-Q41-001: Amazon EFS was a wrong answer in 7 of 35 task questions (cap 5). Fixed by swapping
the EFS distractor in the two Writer B questions named in the report (ignored the report's muddled
"S3 Storage Lens" idea for s04-mr and chose a cleaner replacement instead):

- **s04-mr, choice d**: "Amazon EFS file systems" → "An AWS Backup vault storing recovery points".
  Still fails the stem's "capacity has to be requested or automated explicitly" test — AWS Backup
  manages its own recovery-point storage with nothing for the team to provision or resize — and is
  not a duplicate of any other choice's fact in this question. Added citation
  `cite-saa-4-1-backup-plans` alongside the existing `cite-saa-4-1-ebs-general-purpose`; rationale
  updated to explain the new choice by content.
- **s10-mr, choice c**: "Amazon EFS for the single-instance database" → "Amazon FSx for Windows
  File Server for the single-instance database" (the report's suggestion, confirmed lesson-taught:
  K04/S10 name FSx for Windows File Server as one of FSx's purpose-built engines). Still fails the
  stem's "guaranteed low-latency block storage" requirement — FSx for Windows File Server is a
  managed file storage engine, not block storage — and fails a different fact than choice b's FSx
  distractor (capacity planning), so it is not a duplicate within the question. Citations unchanged
  (`cite-saa-4-1-ebs-general-purpose`, `cite-saa-4-1-efs-lifecycle`); rationale updated.

Re-ran `q1_batch_check.py 4-1` (RESULT WARN, same pre-existing labeled Snowball mention only; all
structural checks still PASS) and `content_lint.py` (PASS, 429 questions).
