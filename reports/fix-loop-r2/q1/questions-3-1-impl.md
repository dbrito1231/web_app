# Task 3.1 question rewrite — implementation report

## AWS review fixes

- **AWS-Q31-001** (`q-saa-3-1-s02-mr` choice b): "AWS Snowball Edge devices, ordered again each time the dataset grows" → "S3 Transfer Acceleration enabled for the pipeline's uploads to cut per-transfer latency". Rationale clause updated to match. `citationIds` swapped `cite-saa-3-1-snowball-edge-eol` → `cite-saa-3-1-s3-transfer-acceleration`. Re-run of `q1_batch_check.py 3-1`: RESULT WARN (no FAIL; only the two expected labelled-retired-service WARNs remain, down from three).

## Batch-check result

```
task 3-1: 8 questions
PASS: lesson single-asterisk spans: 0
PASS: lesson tables/numbered lines: 0
PASS: lesson citations unresolved: []
PASS: drillIds match questions (missing [], extra [])
PASS: exam tips 5 for 5 objectives
WARN: lesson names retired/closed service 'FSx File Gateway' (labelled EOL in lesson body — expected)
WARN: lesson names retired/closed service 'Snowball' x3 (labelled closed-to-new-customers in lesson body — expected)
WARN: q-saa-3-1-k01-mc choice d: retired/closed 'FSx File Gateway' (distractor, clearly labelled EOL in rationale)
WARN: q-saa-3-1-k01-mr choice b: retired/closed 'Snowball' (distractor, clearly labelled closed in rationale)
WARN: q-saa-3-1-s02-mr choice b: retired/closed 'Snowball' (distractor, clearly labelled closed in rationale)
PASS: duplicate 6-word openings: []
PASS: longest-is-key 1/5 = 20%
PASS: MC key positions {'a': 1, 'b': 2, 'c': 1, 'd': 1}
PASS: MR key slots {'a': 1, 'b': 1, 'c': 2, 'd': 1, 'e': 1}
RESULT: WARN (no FAIL)
```
`content_lint.py`: PASS.

All WARNs are the expected "tell words / retired names" flags on distractors that are explicitly labelled as end-of-support or closed-to-new-customers in the choice text and rationale (FSx File Gateway, Snowball Edge) — required by RULES.md ("lesson warnings about labelled retired services are expected").

## Per-question table

| ID | Objective | Tests | Key | Lesson sentence(s) teaching key / distractors |
|---|---|---|---|---|
| k01-mc | K01 | S3 File Gateway vs Volume Gateway vs Tape Gateway vs FSx File Gateway | b: S3 File Gateway (NFS) | "Amazon S3 File Gateway presents an NFS or SMB file share backed by an S3 bucket, with a local cache..." / "Volume Gateway presents block volumes over iSCSI..." / "Tape Gateway presents a virtual tape library..." / "Amazon FSx File Gateway...is no longer available to new customers" |
| k01-mr | K01 | DataSync + S3 File Gateway (SMB) vs Snowball (EOL) vs Volume Gateway stored vs DataSync-alone | a: DataSync, c: S3 File Gateway (SMB) | "DataSync is an online transfer service...with built-in encryption, integrity checks, and a purpose-built protocol that can saturate a 10 Gbps link" / "stored volumes keep the full dataset on-premises" / "AWS Snowball Edge is no longer available to new customers" |
| k02-mc | K02 | FSx for Lustre + data repo association vs Windows/ONTAP/OpenZFS | c: FSx for Lustre | "FSx for Lustre is built for high-performance computing...up to multiple terabytes per second of throughput...across thousands of concurrently mounted EC2 instances, and a data repository association can link it directly to an S3 bucket" / Windows File Server "native Windows file system over SMB" / ONTAP "multi-protocol access...existing NetApp shop" / OpenZFS "in-memory read cache...up to 2,000,000 IOPS" |
| k03-mc | K03 | io2 Block Express vs gp3 vs io1 vs st1 | a: io2 Block Express | "io2 Block Express is the highest-performance EBS type: up to 256,000 IOPS and 4,000 MiB/s...sub-millisecond average latency, and 99.999% durability" / gp3 "up to 80,000 IOPS" / io1 "up to 64,000 IOPS and 1,000 MiB/s" / st1 "price by throughput, not IOPS" |
| s01-mc | S01 | S3 Transfer Acceleration vs multipart vs byte-range vs prefixes | d: Transfer Acceleration | "S3 Transfer Acceleration routes the upload through the nearest CloudFront edge location and over AWS's backbone network...cutting the distance-driven latency" / multipart "splits the object into parts uploaded in parallel" / byte-range "concurrent Range GET requests" / prefixes "spread the load across multiple key prefixes" |
| s01-mr | S01 | EFS Max I/O + Elastic vs General Purpose+Provisioned vs sc1/gp3 vs st1 | b: EFS Max I/O+Elastic, d: st1 | "Max I/O trades higher per-operation latency for higher aggregate throughput and IOPS across a very large number of concurrently connected clients" / "st1...fits large sequential workloads accessed frequently" / "General Purpose has the lowest per-operation latency" / "sc1...infrequently accessed sequential data" |
| s02-mc | S02 | S3 (no provisioning) vs EBS Elastic Volumes vs EFS Provisioned vs FSx Scratch | b: S3 | "Amazon S3 has effectively unlimited object storage capacity with no capacity to plan ahead of time" / EBS "still lives in one Availability Zone and tops out at 64 TiB" / "Provisioned throughput lets you set a fixed MiB/s" / "Scratch deployment for short-lived, non-replicated processing" |
| s02-mr | S02 | EBS Elastic Volumes + DataSync vs instance store vs Snowball vs single prefix | c: EBS Elastic Volumes, e: DataSync | "Elastic Volumes: you can increase size, change volume type...or raise provisioned IOPS and throughput while the volume stays attached...with no downtime" / "DataSync scales by running more tasks in parallel or adding agents" / "Snowball Edge is closed to new customers" / "a single prefix supports at least 3,500...requests per second" |

## Distractor-type table (cap: 1 per type in 8 questions)

| Type | Used in |
|---|---|
| Volume Gateway (cached) vs file-gateway need | k01-mc |
| Tape Gateway vs file-gateway need | k01-mc |
| FSx File Gateway EOL | k01-mc |
| Snowball Edge closed-to-new-customers (migration) | k01-mr |
| Volume Gateway (stored) vs SMB need | k01-mr |
| DataSync-alone, no local share configured | k01-mr |
| FSx Windows vs Lustre need | k02-mc |
| FSx ONTAP vs Lustre need | k02-mc |
| FSx OpenZFS vs Lustre need | k02-mc |
| gp3 vs io2 IOPS ceiling | k03-mc |
| io1 vs io2 ceiling/durability | k03-mc |
| st1 (throughput-priced) vs IOPS need | k03-mc |
| Multipart vs distance-latency need | s01-mc |
| Byte-range (download) vs upload need | s01-mc |
| Prefix scaling vs distance-latency need | s01-mc |
| EFS General Purpose+Provisioned vs many-client need | s01-mr |
| sc1 vs frequently-accessed sequential need | s01-mr |
| gp3 (IOPS-priced) vs sequential-throughput need | s01-mr |
| EBS Elastic Volumes vs no-provisioning need | s02-mc |
| EFS Provisioned throughput vs no-planning need | s02-mc |
| FSx Lustre Scratch vs durable-growth need | s02-mc |
| Instance store fixed/ephemeral vs growth need | s02-mr |
| Snowball Edge closed (repeat-order) | s02-mr |
| Single S3 prefix vs growing-request-volume need | s02-mr |

All 24 distractor types are distinct; no type repeats within the 8-question task.

## Lesson additions requested

None. Every key and distractor is fully taught by the existing lesson-3-1 body.
