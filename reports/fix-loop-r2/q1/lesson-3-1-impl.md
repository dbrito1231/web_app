# Lesson 3.1 rewrite — implementation notes

**Scope:** `content/lessons/lesson-3-1.json` body rewrite (K01–K03, S01–S02), 17 new citation files (`content/citations/cite-saa-3-1-*.json`), placeholder `content/citations/cite-3-1.json` removed (only lesson-3-1.json referenced it). No question files touched.

## Section outline (objective id order)

- **K01 — Hybrid storage solutions to meet business requirements.** Storage Gateway's three current types (S3 File Gateway, Volume Gateway cached/stored, Tape Gateway); FSx File Gateway flagged as no longer available to new customers. DataSync (online, NFS/SMB/HDFS/object → S3/EFS/FSx) vs. the Snow Family, which is also no longer available to new customers — new customers are pointed to DataSync (online) or AWS Data Transfer Terminal (offline, physical facility).
- **K02 — Storage services with appropriate use cases (S3, EFS, EBS).** Builds on 2.1/2.2 basics; adds the FSx family: Lustre (HPC/ML, Scratch vs Persistent, S3 data-repository linking), Windows File Server (SMB/AD), NetApp ONTAP (multi-protocol, snapshots/dedup), OpenZFS (ZFS features, in-memory cache, 1M+ IOPS).
- **K03 — Storage types with associated characteristics (object, file, block).** Block: gp3 vs gp2 vs io2 Block Express vs st1 vs sc1 with baseline/max IOPS and throughput numbers; instance store (ephemeral). File: EFS performance modes (General Purpose vs Max I/O) and throughput modes (Bursting/Provisioned/Elastic) with the documented figures. Object: S3 Express One Zone (single-digit-ms latency, directory-bucket request-rate ceilings) vs S3 Standard.
- **S01 — Determining storage services and configurations that meet performance demands.** S3 techniques (byte-range fetches, multipart upload, Transfer Acceleration, prefix scaling) plus matching a stated IOPS/throughput/latency number to the right EBS type, EFS mode, or FSx variant.
- **S02 — Determining storage services that can scale to accommodate future needs.** S3 (no capacity planning), EBS Elastic Volumes (resize/retype live, 64 TiB single-volume ceiling), EFS (auto-grows, Elastic throughput auto-scales), FSx (post-creation capacity/throughput increases), DataSync scaling via parallel tasks/agents now that Snowball Edge is closed to new customers.

## Concepts per current (placeholder) question

- `q-saa-3-1-k01-mc/mr` → objective text "Hybrid storage solutions" → now taught under K01 (Storage Gateway types, DataSync vs Snow Family).
- `q-saa-3-1-k02-mc` → "Storage services with appropriate use cases (S3, EFS, EBS)" → K02 (FSx variants added as the performance-oriented extension of S3/EFS/EBS).
- `q-saa-3-1-k03-mc` → "Storage types with associated characteristics (object, file, block)" → K03 (EBS volume types, instance store, EFS modes, S3 Express One Zone).
- `q-saa-3-1-s01-mc/mr` → "Determining storage services and configurations that meet performance demands" → S01 (S3 performance techniques, matching numeric requirements to service/config).
- `q-saa-3-1-s02-mc/mr` → "Determining storage services that can scale to accommodate future needs" → S02 (scaling paths per service).

These placeholder questions still use "Apply the objective directly" filler; per the task instructions no question files were edited — that rewrite is a separate Q1 pass.

## Doc URLs used (all accessed 2026-09-26)

- https://docs.aws.amazon.com/ebs/latest/userguide/general-purpose.html (gp3/gp2)
- https://docs.aws.amazon.com/ebs/latest/userguide/provisioned-iops.html (io2 Block Express)
- https://docs.aws.amazon.com/ebs/latest/userguide/hdd-vols.html (st1/sc1)
- https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/InstanceStorage.html (instance store)
- https://docs.aws.amazon.com/efs/latest/ug/performance.html (EFS performance/throughput modes)
- https://docs.aws.amazon.com/fsx/latest/LustreGuide/what-is.html (FSx for Lustre)
- https://docs.aws.amazon.com/fsx/latest/WindowsGuide/what-is.html (FSx for Windows File Server)
- https://docs.aws.amazon.com/fsx/latest/ONTAPGuide/what-is-fsx-ontap.html (FSx for NetApp ONTAP)
- https://docs.aws.amazon.com/fsx/latest/OpenZFSGuide/what-is-fsx.html (FSx for OpenZFS)
- https://docs.aws.amazon.com/AmazonS3/latest/userguide/optimizing-performance-guidelines.html (byte-range fetches)
- https://docs.aws.amazon.com/AmazonS3/latest/userguide/optimizing-performance-design-patterns.html (prefix request-rate scaling)
- https://docs.aws.amazon.com/AmazonS3/latest/userguide/transfer-acceleration.html (Transfer Acceleration)
- https://docs.aws.amazon.com/AmazonS3/latest/userguide/s3-express-performance.html (S3 Express One Zone)
- https://docs.aws.amazon.com/storagegateway/latest/userguide/WhatIsStorageGateway.html (Storage Gateway types)
- https://docs.aws.amazon.com/filegateway/latest/filefsxw/what-is-file-fsxw.html (FSx File Gateway EOL notice)
- https://docs.aws.amazon.com/datasync/latest/userguide/what-is-datasync.html (DataSync)
- https://docs.aws.amazon.com/snowball/latest/developer-guide/snowball-edge-availability-change.html (Snowball Edge EOL notice)

## Notable fact-check finding

Both **Amazon FSx File Gateway** and the entire **AWS Snow Family** (Snowball Edge, and by extension Snowcone/Snowmobile) are now documented as "no longer available to new customers." The lesson reflects this instead of presenting them as live options: hybrid file access now routes through S3 File Gateway or a direct FSx connection, and physical migration now routes through AWS Data Transfer Terminal, with DataSync as the online-transfer default.

## Verification performed

- `content_lint.py`: PASS (429 questions, 21+21 labs, 23 lessons).
- Word count: 1,868 (within the 1,800–2,500 target).
- 0 single-asterisk spans; only `###`/`####` section headings (plus the lesson's top-level `##` title, matching the established lesson-2-1/2-2 convention), `- ` bullets, `**bold**`, and backticks used; no tables, links, or numbered lists.
- All 17 `citationIds` resolve to files in `content/citations/`; all 8 `drillIds` resolve to existing `q-saa-3-1-*` question files (k01-mc, k01-mr, k02-mc, k03-mc, s01-mc, s01-mr, s02-mc, s02-mr), in objective order.
- Placeholder citation `cite-3-1.json` deleted after confirming (via grep) that only `lesson-3-1.json` referenced it.
- `git status` confirms only `content/lessons/lesson-3-1.json` and `content/citations/cite-saa-3-1-*.json` (plus the deleted placeholder) changed — no question files touched.
