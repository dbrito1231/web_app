# Teacher review — Lesson 3.5 "High-performing data ingestion and transformation"

Saved by Lead Dev from the Teacher's reply (AGENTS.md: the Teacher does not write files).

**1. Claim table spot-check (7 rows, none AWS listed):** rows 2, 3, 4 (Lake Formation grant/revoke, hybrid access mode, data-lake-admin-first — all exact matches vs. `lake-formation/latest/dg/how-it-works-terminology.html`), 7 (DataSync end-to-end security/encryption/integrity — exact match), 9 (Data Catalog centralized metadata repo — exact match), 11 (Python shell single-EC2-instance limit — exact match), 17 (Firehose buffering hints default 5 MiB/300s, min interval 0 — exact match), 26 (too-many-partition-keys fragmentation — exact match, Athena performance-tuning page). All 7 verified verbatim or in substance. No claim-table failures.

**2. Coverage:** all 14 `SAA-3.5-*` objectives (`content/objectives/saa_c03.json`) have a matching `###` section in order (K01–K07, S01–S07). Confirmed independently — matches the AWS review.

**3. Teaching quality:** clear for a college IT student; the four confusable clusters are all explicitly contrasted (Data Streams vs. Firehose vs. Managed Service for Apache Flink vs. MSK in K07/S02; Glue ETL vs. EMR vs. Athena in S05; crawler/Data Catalog in K04; Lake Formation grant/revoke vs. IAM in S01; columnar formats + partitioning in S07/S06). Both renamed services are introduced with old and new names (Data Firehose, Managed Service for Apache Flink) and the in-progress QuickSight/"Quick Sight" rebrand is well-hedged. All 14 exam tips read correct and on-topic. No filler spotted — each paragraph carries distinct facts. No contradiction with lessons 2.1 or 3.1 (Kinesis shard figure and DataSync/Storage Gateway/Snowball status match exactly).

**4. Length:** 2,954 words for 14 objectives (≈211 words/objective) is acceptable — in line with other approved 3.x lessons and within the stated 2,300–3,000 target. No filler to cut.

**5. Format (`q1_batch_check.py 3-5`, lesson lines only):**
```
PASS: lesson single-asterisk spans: 0
PASS: lesson tables/numbered lines: 0
PASS: lesson citations unresolved: []
PASS: drillIds match questions (missing [], extra [])
PASS: exam tips 14 for 14 objectives
WARN: lesson names retired/closed service 'Snowball' (x2) — expected, explicitly labeled retired per RULES.md
```

**6. Teach-before-test gaps:**
- No hard gaps. All facts needed for MC/MR distractors on K01–K07 and S01–S07 are present with enough distinct detail (e.g., S01 has 5 distinguishable facts for its 5-choice MR: register S3, run crawler, designate admin first, grant/revoke model, hybrid access mode; S06 similarly has 5: schedule, file format, shard count, buffering hints, broker/serverless, partition scheme).
- Watch item (not a defect): K03/S03 lean on lesson 3.1 for DataSync/Storage Gateway mechanics rather than re-teaching them. This mirrors 3.1's own approved pattern and AWS found no issue, so it's acceptable — but the question writer should pull DataSync/Storage Gateway distractor-wrongness reasoning from 3.1's lesson body, not assume it here.
- Watch item: S05's compute-option coverage is limited to Athena/Glue/EMR Serverless/EMR (4 named options). If an S05 MR question uses a 5th distractor like AWS Lambda or Amazon Redshift as a "wrong" choice, the reason it's wrong for this specific data-processing context isn't taught in this lesson (Redshift Spectrum is mentioned once, in K04, as a Data-Catalog consumer, which is thin). Recommend the question writer either stick to the 4 taught compute options plus a taught non-compute distractor (e.g., "an EC2 instance you manage yourself"), or flag a lesson addition if a 5th real compute service is needed.

No issues rose to `TEACHER-L35-###` severity — nothing wrong, stale, or inconsistent was found.

Lesson 3.5: approve for question writing

Overall: approve
