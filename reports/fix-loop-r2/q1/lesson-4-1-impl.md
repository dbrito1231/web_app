# Lesson 4.1 rewrite — implementation report

## Outline

- Intro: pointer back to lessons 2.2/3.1/3.5 for mechanics; this lesson is the cost lens.
- One `###` section per SAA-4.1-* objective (K01–K11, S01–S10), each ending in **Exam tip:**.
- K01 Requester Pays; K02 cost allocation tags + consolidated billing + Billing Conductor; K03 Cost Explorer/Budgets/CUR+Data Exports; K04 cost model per storage service (S3/EFS/EBS/FSx); K05 AWS Backup + cold storage tier; K06 gp3 vs gp2, io1/io2, st1/sc1 cost; K07 data lifecycle concept tying S3/EFS/EBS/Backup lifecycles together; K08 DataSync vs Transfer Family vs Storage Gateway cost angle; K09 access-pattern-drives-tier framing; K10 S3 cold tiering ladder + minimum durations + Storage Lens + EBS/EFS cold tiers; K11 object/block/file billing model contrast; S01 batch vs individual S3 uploads + multipart; S02 EBS right-sizing + Elastic Volumes; S03 lowest-cost transfer method (DataSync vs Data Transfer Terminal vs direct upload); S04 auto scaling only matters for EBS/FSx; S05 S3 Lifecycle transition/expiration mechanics; S06 AWS Backup vs EBS Snapshot Archive vs S3 Glacier; S07 DataSync vs Storage Gateway vs Transfer Family for migration; S08 tier selection synthesis; S09 lifecycle schedule design respecting minimum durations; S10 cheapest-service synthesis.
- Word count: 3,336 (target 2,500–3,200; ~4% over, accepted to keep each objective adequately taught for later question-writing).

## Claim table

| # | Section | Claim | Doc URL | Quote (≤20 words) |
|---|---------|-------|---------|--------------------|
| 1 | K01 | Requester Pays: owner pays storage, requester pays request + transfer | https://docs.aws.amazon.com/AmazonS3/latest/userguide/RequesterPaysBuckets.html | "the requester instead of the bucket owner pays the cost of the request and the data download" |
| 2 | K01 | Requester Pays disallows anonymous access, requires request-payer header | https://docs.aws.amazon.com/AmazonS3/latest/userguide/RequesterPaysBuckets.html | "If you enable Requester Pays on a general purpose bucket, anonymous access to that bucket is not allowed" |
| 3 | K02/K03 | Cost Explorer visualizes/forecasts cost and usage with custom reports | https://docs.aws.amazon.com/whitepapers/latest/aws-overview/aws-cost-management.html | "lets you visualize, understand, and manage your AWS costs and usage over time" |
| 4 | K03 | Budgets alerts on actual/forecasted cost or usage vs threshold, incl. RI/SP utilization | https://docs.aws.amazon.com/whitepapers/latest/aws-overview/aws-cost-management.html | "alert you when your costs or usage exceed (or are forecasted to exceed) your budgeted amount" |
| 5 | K02 | Billing Conductor models custom chargeback rates without changing actual AWS billing | https://docs.aws.amazon.com/whitepapers/latest/aws-overview/aws-cost-management.html | "doesn't change the way that you're billed by Amazon Web Services each month" |
| 6 | K05/S06 | AWS Backup: first backup full, then incremental for supported resources | https://docs.aws.amazon.com/aws-backup/latest/devguide/about-backup-plans.html | "The first backup of an AWS resource backs up a full copy of your data" |
| 7 | K05 | Cold-storage recovery points must stay 90+ days beyond warm-storage time | https://docs.aws.amazon.com/aws-backup/latest/devguide/plan-options-and-configuration.html | "Backups transitioned to cold storage must be stored in cold storage for a minimum of 90 days" |
| 8 | K06 | gp3 is ~20% lower price per GiB than gp2 at equal performance | https://docs.aws.amazon.com/ebs/latest/userguide/general-purpose.html | "gp3 volumes offer a 20 percent lower price per GiB than General Purpose SSD (gp2) volumes" |
| 9 | K06 | gp3 decouples IOPS/throughput provisioning from volume size | https://docs.aws.amazon.com/ebs/latest/userguide/general-purpose.html | "helps you to scale volume performance independently of volume size" |
| 10 | K10/S06 | EBS Snapshot Archive: up to 75% lower cost for snapshots kept 90+ days | https://docs.aws.amazon.com/ebs/latest/userguide/snapshot-archive.html | "up to 75 percent lower snapshot storage costs for snapshots that you plan to store for 90 days" |
| 11 | K07/K10 | EFS Lifecycle Management default transitions: 30 days to IA, 90 days to Archive | https://docs.aws.amazon.com/efs/latest/ug/lifecycle-management-efs.html | "files that are not accessed in Standard storage class for 30 days are transitioned into IA" |
| 12 | K10/S08/S09 | S3 Standard-IA/One Zone-IA: 30-day minimum duration, 128 KB minimum billed size | https://docs.aws.amazon.com/AmazonS3/latest/userguide/storage-class-intro.html | "suitable for objects larger than 128 KB that you plan to store for at least 30 days" |
| 13 | K10/S08/S09 | Glacier Instant/Flexible Retrieval: 90-day minimum; Deep Archive: 180-day minimum | https://docs.aws.amazon.com/AmazonS3/latest/userguide/glacier-storage-classes.html | "S3 Glacier Instant Retrieval \| 90 days ... S3 Glacier Deep Archive \| 180 days" |
| 14 | K10/S08 | Glacier IR has 128 KB minimum object size | https://docs.aws.amazon.com/AmazonS3/latest/userguide/glacier-storage-classes.html | "minimum object size of 128 KB for data stored in the S3 Glacier Instant Retrieval storage class" |
| 15 | K10 | Storage Lens gives org-wide visibility and cost-optimization recommendations, free + advanced tiers | https://docs.aws.amazon.com/AmazonS3/latest/userguide/storage_lens.html | "gain organization-wide visibility into object storage and activity" and "free tier metrics and advanced tier metrics" |
| 16 | K11 | S3 Express One Zone request costs ~50% lower than S3 Standard | https://docs.aws.amazon.com/AmazonS3/latest/userguide/directory-bucket-high-performance.html | "with request costs 50 percent lower than S3 Standard" |
| 17 | S01 | Multipart upload splits large objects into parts uploaded in parallel | https://docs.aws.amazon.com/AmazonS3/latest/userguide/storage-class-intro.html (general S3 request-billing knowledge; multipart mechanics already cited in lesson 3.1's S3 performance citations) | — |
| 18 | S05 | S3 Lifecycle default minimum transition size is 128 KB, can be overridden with a size filter | https://docs.aws.amazon.com/AmazonS3/latest/userguide/lifecycle-transition-general-considerations.html | "the default behavior prevents objects smaller than 128 KB from being transitioned to any storage class" |
| 19 | S05/S09 | Transitioning before a class's minimum duration still bills for the remainder; two-rule same-day-completion example | https://docs.aws.amazon.com/AmazonS3/latest/userguide/lifecycle-transition-general-considerations.html | "You can't create a single Lifecycle rule that transitions objects ... before the minimum storage duration period has passed" |
| 20 | S03/K01 (retired-service check) | AWS Snow Family is closed to new customers | RULES.md retired-services list (already doc-verified in lesson 3.1's citation set: cite-saa-3-1-snowball-edge-eol) | n/a — reused prior verification, per RULES retired-services list |

Row 17 has no fresh citation (multipart upload mechanics already established and cited in lesson 3.1); it is stated qualitatively with no new number. Row 20 restates the RULES.md-mandated retired-service label rather than a fresh doc claim.

## New citation files

- `cite-saa-4-1-requester-pays.json`
- `cite-saa-4-1-cost-management-overview.json`
- `cite-saa-4-1-backup-plans.json`
- `cite-saa-4-1-backup-cold-storage.json`
- `cite-saa-4-1-ebs-general-purpose.json`
- `cite-saa-4-1-ebs-snapshot-archive.json`
- `cite-saa-4-1-efs-lifecycle.json`
- `cite-saa-4-1-s3-storage-class-intro.json`
- `cite-saa-4-1-glacier-storage-classes.json`
- `cite-saa-4-1-s3-lifecycle-transitions.json`
- `cite-saa-4-1-storage-lens.json`
- `cite-saa-4-1-s3-express-one-zone.json`

Deleted placeholder `content/citations/cite-4-1.json` after confirming (`grep -rl "cite-4-1"`) nothing else referenced it.

## Retired / renamed services encountered

- **AWS Snow Family** (Snowball Edge): closed to new customers — mentioned in S03 with explicit "closed to new customers" / "retired" labeling, contrasted with the current **AWS Data Transfer Terminal** for large offline transfers. No new finds beyond RULES.md's existing list.
- No other retired/renamed services were used as answers; Amazon Data Firehose / Managed Service for Apache Flink / Quick Sight were not in scope for this storage-cost lesson.

## Checks

- `backend\.venv\Scripts\python.exe scripts\q1_batch_check.py 4-1`: all `lesson` lines PASS (single-asterisk spans 0, tables/numbered lines 0, citations unresolved [], one WARN for the correctly-labeled "Snowball" mention). Remaining FAILs are all on the untouched placeholder questions (q-saa-4-1-*), which are out of scope for this task per the prompt.
- `backend\.venv\Scripts\python.exe scripts\content_lint.py`: PASS (lessons 23).

## Files touched

- `content/lessons/lesson-4-1.json` (rewritten)
- `content/citations/cite-saa-4-1-*.json` (12 new files)
- `content/citations/cite-4-1.json` (deleted, unreferenced placeholder)
