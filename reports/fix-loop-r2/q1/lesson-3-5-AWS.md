# Lesson 3.5 AWS review -- "High-performing data ingestion and transformation"

Reviewer: Senior AWS Solutions Architect (read-only). Source: `content/lessons/lesson-3-5.json` (commit `b51fe35`), claim table and notes in `reports/fix-loop-r2/q1/lesson-3-5-impl.md`.

## Per-section verdicts

- K01 (analytics/viz services): accurate. Athena/Lake Formation/QuickSight roles correctly distinguished. OK.
- K02 (ingestion patterns): accurate, clear batch/streaming/micro-batch contrast. OK.
- K03 (data transfer): accurate, correctly defers to 3.1, correct Snowball Edge status. OK.
- K04 (transformation services): accurate on crawler, Data Catalog, three Glue ETL engines, DataBrew. OK.
- K05 (secure ingestion access): accurate on IAM, PrivateLink, S3 access points incl. 10,000/account/Region limit (doc-verified). OK.
- K06 (sizing): accurate on Kinesis shard limits, Firehose buffering hints, MSK Serverless, DataSync (matches 3.1). OK.
- K07 (streaming services): accurate rebrands (Data Firehose, Managed Service for Apache Flink) and correct MSK/Kinesis Data Streams contrast; consistent with lesson 2.1. OK.
- S01 (data lake build/secure): accurate on registration, hybrid access mode, admin-first pattern. OK.
- S02 (streaming architecture): accurate; enhanced fan-out figure (2 MiB/s per shard per consumer) doc-verified. OK.
- S03 (transfer design): accurate, correctly routes bulk-offline to Data Transfer Terminal since Snowball Edge is closed to new customers. OK.
- S04 (visualization): accurate SPICE vs. direct-query tradeoff and Athena-as-source chain. OK.
- S05 (compute options): accurate Athena/Glue/EMR Serverless/EMR contrast. OK.
- S06 (ingestion configuration): accurate, ties back to K02/K06 correctly. OK.
- S07 (format transforms): accurate; CSV-vs-Parquet benchmark (102.9 GB/$0.10 vs. 1.04 GB/$0.001, "99% saving / 95% faster") verified verbatim against the "Choose a columnar format" section of the cited whitepaper -- correctly NOT conflated with that paper's separate "Partition data" example (94%/6.49 GB), which the lesson does not cite for this claim. OK.

## Claim table check (8+ rows spot-checked, all numbers verified)

Verified against live docs: rows 1 (Athena partitioning), 5 (QuickSight/Quick Sight rename -- see below), 15 (S3 access points, 10,000/account/Region -- exact match), 16 (Kinesis shard: 1 MiB or 1,000 records/sec write, 2 MiB/sec read -- exact match, also consistent with lesson 2.1's own figure), 19 (Managed Service for Apache Flink rename -- exact match: "The former name of Amazon Managed Service for Apache Flink before it was rebranded"), 21 (Data Firehose rename -- exact match: current Firehose API Welcome page states "Amazon Data Firehose was previously known as Amazon Kinesis Data Firehose"), 22 (enhanced fan-out 2 MB/sec per shard per consumer -- exact match), 27/28 (CSV vs. Parquet cost/scan/time figures -- exact match, see S07 above). No row fails. Table has 28 rows, exceeding the 8-row minimum.

## Service name and status check

- **Amazon Data Firehose**: confirmed current name; lesson correctly notes "(renamed from Kinesis Data Firehose)." Doc-verified via `firehose/latest/APIReference/Welcome.html`.
- **Amazon Managed Service for Apache Flink**: confirmed current name for the former "Kinesis Data Analytics for Apache Flink"; lesson correctly notes the old name and does not imply the older Kinesis Data Analytics **SQL** applications (a separate, now-legacy offering) are the same product. No misstatement found.
- **"Quick Sight" rebrand**: the writer's claim held up under direct verification, contrary to the reviewer's initial suspicion. Current AWS docs (`docs.aws.amazon.com/quick/latest/userguide/quick-bi.html` and `.../quicksight/latest/user/welcome.html`, the latter now retitled "What is Amazon Quick?") state verbatim: "Amazon Quick evolved from Amazon QuickSight. QuickSight continues as Amazon Quick Sight, a feature within Quick. All existing QuickSight APIs, SDKs, and integrations continue to work without changes." The lesson's hedge -- current docs increasingly use "Amazon Quick Sight," but the exam guide and most material still say "Amazon QuickSight," and it is functionally the same service -- is the correct, well-calibrated way to present an in-progress rebrand. No fix needed. This is a genuine new finding worth keeping on RULES.md's "check anything else" watchlist, as the impl report already recommends.

## Contrasts, exam tips, coverage, citations, prior-lesson consistency

- Contrasts (Streams vs. Firehose vs. Flink vs. MSK; Glue ETL vs. EMR vs. Athena; crawlers/Data Catalog; Lake Formation; columnar format + partitioning benefit) are all present and accurate.
- All 14 exam tips read correctly and match the section content.
- Coverage: all 14 `SAA-3.5-*` objective ids in `content/objectives/saa_c03.json` have a matching `###` section, in id order.
- Citations: 19 citation files back specific sentences; spot-checked citations align with their claims (see claim-table check above).
- No contradiction found with lesson 2.1 (Kinesis Data Streams description and shard limit match exactly) or lesson 3.1 (DataSync/Storage Gateway/Snowball Edge status and 10 Gbps figure match exactly).

## Lint

`content_lint.py`: PASS (429 questions, 23 lessons, no structural errors).

## Issues

None found at AWS-review severity. No `AWS-L35-###` items opened.

Lesson 3.5: approve for question writing

Overall: approve
