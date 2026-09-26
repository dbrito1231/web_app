# Task 3.5 questions AWS review -- round 2

Reviewer: Senior AWS Solutions Architect. Source: `content/questions/q-saa-3-5-*.json` (commit `e632950`), `reports/fix-loop-r2/q1/questions-3-5-impl.md`. Round 1 lesson findings: none were opened, so item (a)/(b) of round 2 (marking prior findings Gone) is not applicable.

`q1_batch_check.py 3-5`: RESULT WARN, but the only WARNs are the two pre-existing, already-approved "Snowball" mentions in the lesson body (labeled retired, from round 1). No question-level FAIL or WARN. `content_lint.py`: PASS.

## Per-question table

| id | key correct/best | distractors real, one-reason-wrong, not strawmen | renamed services correct | rationale accurate | stem unambiguous | citations support | verdict |
|---|---|---|---|---|---|---|---|
| k01-mc | yes (Athena) | yes | n/a | yes | yes | yes | OK |
| k01-mr | yes (Lake Formation, QuickSight) | yes | n/a | yes | yes | yes | OK |
| k02-mc | yes (streaming) | yes (timing-tolerance distractors, not services) | n/a | yes | yes | yes | OK |
| k03-mc | yes (DataSync) | yes | n/a | yes | yes | yes | OK |
| k04-mc | yes (Glue ETL/Spark) | yes | n/a | yes | yes | yes | OK |
| k04-mr | yes (DataBrew, crawler) | yes | n/a | yes | yes | yes | OK |
| k05-mc | yes (S3 access point) | yes | n/a | yes | yes | yes | OK |
| k06-mc | yes, math verified: 8,500/1,000=8.5 -> 9 shards minimum | yes (4, 6 under; 17 double) | n/a | yes | yes | yes | OK |
| k07-mc | yes (Managed Service for Apache Flink) | yes | correct current name used | yes | yes | yes | OK |
| k07-mr | yes (Data Firehose, Kinesis Data Streams) | yes | correct current names used | yes | yes | yes | OK |
| s01-mc | yes (Lake Formation) | yes | n/a | yes | yes | yes | OK |
| s01-mr | yes (hybrid access mode, data lake administrator) | yes | n/a | yes | yes | yes | OK |
| s02-mc | yes (Kinesis Data Streams) | yes | correct Data Firehose name | yes | yes | yes | OK |
| s02-mr | yes, math verified: enhanced fan-out = 2 MiB/s per shard per consumer, doc-confirmed | yes | n/a | yes | yes | yes | OK |
| s03-mc | yes (S3 File Gateway) | yes | n/a | yes | yes | yes | OK |
| s03-mr | yes (Data Transfer Terminal, Kinesis Data Streams); "Data Transfer Terminal" confirmed as a real, current AWS offering (`docs.aws.amazon.com/datatransferterminal/...`) | yes | Snowball Edge status correct | yes | yes | yes | OK |
| s04-mc | yes (QuickSight + SPICE) | yes | n/a | yes | yes | yes | OK |
| s04-mr | yes (Glue crawler, Athena) | yes | n/a | yes | yes | yes | OK |
| s05-mc | yes (EMR cluster mode) | yes | n/a | yes | yes | yes | OK |
| s05-mr | yes (Athena, EMR Serverless) | yes | n/a | yes | yes | yes | OK |
| s06-mc | yes (better partition key) | yes; "add broker nodes to Kinesis" is a real MSK term deliberately misapplied to Kinesis, not a strawman | n/a | yes | yes | yes | OK |
| s06-mr | yes (S3 date partitioning + matching Hive-style Athena keys) | yes | n/a | yes | yes | yes | OK |
| s07-mc | yes (convert to Parquet via Glue ETL/CTAS) | yes | n/a | yes | yes | yes | OK |
| s07-mr | yes (convert to Parquet + partition by date); benchmark numbers verified against the cited whitepaper's "Choose a columnar format" section | yes | n/a | yes | yes | yes | OK |

No `AWS-Q35-###` blocking issues. One non-blocking observation below.

## Distractor-type clustering (the writer's flagged item)

Judged: **no distractor type exceeds the 3-of-24 cap under the rule's intent**, but by raw service name a few services are reused as a wrong-role distractor more than 3 times: Lake Formation (5x: k01-mc, k05-mc, s03-mc, s04-mr, s05-mr), the EMR/EMR Serverless family (7x combined), Athena (5x), and the Kinesis/Firehose/MSK "wrong lever" family (7x combined across distinct levers: retention, on-demand mode, buffer size, shard count, "broker nodes"). This is a byproduct of the lesson teaching only ~13 named services across 14 objectives and 24 questions each needing 3-4 real, same-area, single-reason-wrong distractors -- not a repeated lazy crutch. Verified each individual occurrence gives a distinct, specific, doc-accurate reason for failing (e.g., Lake Formation is rejected once for having no query engine, once for being a bucket-wide governance role rather than a per-team boundary, once for lacking a mount capability, twice for not being a QuickSight source/compute engine -- five different facts, not one repeated joke). This is unlike the round-1 DataBrew problem, which was the same "obviously non-technical" gag reused as a crutch. Recommend, as optional round-3 polish and not a blocker: swap one or two of the Lake Formation instances (e.g., in `s04-mr` or `s05-mr`) for an underused real option (S3 access point already used there; a Glue Data Catalog or AWS DataSync substitution would work) if the team wants the raw-service-count table under 3 everywhere. Not required for closure.

## Other checks

- No two questions test the identical fact; overlapping-topic pairs (e.g., k03-mc/s03-mc on DataSync-vs-File-Gateway, s07-mc/s07-mr on Parquet conversion) test complementary halves of the same distinction from different angles, consistent with how lessons 2.1/3.1 already pair such contrasts.
- All numbers used in a key verified against docs: shard write limit (1,000 records/sec or 1 MiB/sec), enhanced fan-out (2 MiB/sec/shard/consumer), and the CSV-vs-Parquet cost/scan benchmark (102.9 GB/$0.10 vs 1.04 GB/$0.001, 99%/95%).
- Renamed services (Amazon Data Firehose, Amazon Managed Service for Apache Flink) are named correctly and consistently in every question that uses them; no stale name appears anywhere in choices or rationale.
- Citations spot-checked (Athena serverless whitepaper, Data Firehose "what is" page, QuickSight/Quick rename page, Data Transfer Terminal facility page) all support the specific claim they're attached to.
- No banned giveaway words found in any choice text; no choice references another choice; no strawman/anti-pattern choices found.

Task 3.5: close

Overall: approve
