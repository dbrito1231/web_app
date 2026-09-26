# Task 3.5 questions implementation report

## Scope

Wrote all 24 `content/questions/q-saa-3-5-*.json` files (14 MC + 10 MR), keeping `id`, `type`, `module`, `objectiveIds`, and `selectCount` unchanged from the existing placeholders. Added 4 new question-only citations (`cite-saa-3-5-q-athena-serverless`, `cite-saa-3-5-q-firehose-what-is`, `cite-saa-3-5-q-kinesis-consumers`, `cite-saa-3-5-q-msk-kafka-compat`); everything else reuses the 19 lesson citations from round 1 plus `cite-saa-3-1-datasync-what-is`, `cite-saa-3-1-storage-gateway-types`, `cite-saa-3-1-snowball-edge-eol`, and `cite-saa-3-1-s3-transfer-acceleration` for the DataSync/Storage Gateway/Snowball-adjacent questions, per the watch item. No other files touched, no git commands run.

## Batch-check result

`q1_batch_check.py 3-5` (final run):

```
task 3-5: 24 questions
PASS: lesson single-asterisk spans: 0
PASS: lesson tables/numbered lines: 0
PASS: lesson citations unresolved: []
PASS: drillIds match questions (missing [], extra [])
PASS: exam tips 14 for 14 objectives
WARN: lesson names retired/closed service 'Snowball' (x2, lesson body -- pre-existing from round 1, the retired status is explicitly labeled both times)
PASS: duplicate 6-word openings: []
PASS: longest-is-key 4/14 = 29%
PASS: MC key positions {'a': 3, 'b': 4, 'c': 4, 'd': 3}
PASS: MR key slots {'a': 4, 'b': 4, 'c': 4, 'd': 4, 'e': 4}
RESULT: WARN
```

No FAILs. The only WARNs are the two pre-existing lesson-body mentions of "Snowball" from round 1 (both already reviewed and approved with the retired status clearly labeled); there are zero tell-word or retired-service WARNs on any question choice. `scripts/content_lint.py` passes (429 questions, 23 lessons).

First fix applied during iteration: `q-saa-3-5-k07-mc` and `q-saa-3-5-s01-mc` originally had the correct choice as the longest text (6/14 = 43%, over the 35% cap). Lengthened the three distractors in k07-mc (still accurate, just fuller phrasing: "Amazon Data Firehose delivering to Amazon S3", "Amazon MSK broker cluster running alone", "AWS Glue DataBrew for visual data cleaning") and shortened the s01-mc key text ("...and grant permissions there" instead of spelling out "through its database and table model"). Brought the rate to 4/14 = 29%, under the cap.

## Per-question table

| id | objective | tests | key | key basis (lesson quote) | distractor basis (lesson quotes) |
|---|---|---|---|---|---|
| k01-mc | K01 | Athena vs EMR/Presto vs QuickSight vs Lake Formation for ad hoc SQL, no infra | Athena | "Amazon Athena is a serverless, interactive SQL query service that runs directly against data sitting in Amazon S3" | EMR: "a persistent, tunable, multi-node Hadoop/Spark cluster" (provisioning required); QuickSight: "AWS's business-intelligence service for dashboards and visuals"; Lake Formation: "registers S3 paths...and layers a grant/revoke permissions model" |
| k01-mr | K01 | Lake Formation (permissions) vs QuickSight (dashboards), Athena/DataBrew/EMR as foils | Lake Formation, QuickSight | same as above | Athena: query engine, no permission model; DataBrew: "visual data-preparation tool"; EMR: compute cluster |
| k02-mc | K02 | Batch/micro-batch vs streaming for a seconds-level latency requirement | Streaming | "Streaming ingestion delivers records continuously, often within seconds" | Batch: "collects data over a window...simpler...appropriate when the business doesn't need the data until the next report"; micro-batch: "buffers a stream for a short, configurable interval" |
| k03-mc | K03 | DataSync (one-time bulk) vs S3 File Gateway (persistent) vs Kinesis vs Glue crawler | DataSync | "DataSync is an online transfer service...able to saturate a 10 Gbps link" (lesson 3.5 K03 + 3.1) | File Gateway: "keep serving an NFS share on an ongoing basis" (3.1); Kinesis: 1 MB/record cap; Glue crawler: catalogs, doesn't transfer |
| k04-mc | K04 | Glue ETL/Spark (scheduled join) vs DataBrew vs crawler vs Athena ad hoc | Glue ETL (Spark) | "Glue for Apache Spark (distributed, for large datasets)" | DataBrew: "visual, point-and-click interface"; crawler: "infers its schema, and writes table definitions"; Athena: ad hoc query, not a maintained pipeline |
| k04-mr | K04 | DataBrew (visual cleaning) vs Glue crawler (schema discovery), CTAS/EMR Serverless/Ray as foils | DataBrew, crawler | same K04 quotes | CTAS: builds from an existing table, doesn't discover new schema; EMR Serverless / Glue for Ray: run code, no visual interface |
| k05-mc | K05 | S3 access points (scoped, VPC-restricted) vs bucket policy vs IAM+naming vs Lake Formation admin | S3 access point | "each access point is a named network endpoint attached to a bucket...can be restricted to accept requests only from a specific VPC" | bucket policy: the "large, hard-to-audit" approach the requirement rejects; IAM+naming: no enforced boundary; LF administrator: broad governance role, not per-team scoping |
| k06-mc | K06 | Shard-count math from a stated records/sec requirement | 9 shards | "Each shard can support up to 1 MiB/second or 1,000 records/second of writes" | 4/6 shards: under capacity; 17 shards: double the needed minimum |
| k07-mc | K07 | Managed Flink (custom windowed compute) vs Firehose vs MSK vs DataBrew | Managed Service for Apache Flink | "a managed runtime for building custom stream-processing applications in SQL, Java, Python, or Scala" | Firehose: "buffers and loads streaming data into a destination...with little to no code"; MSK: Kafka-compatible transport, not compute; DataBrew: batch, not streaming |
| k07-mr | K07 | Firehose (delivery, no code) vs Kinesis Data Streams (independent replay), Glue for Ray/Managed Flink/DataBrew as foils | Firehose, Kinesis Data Streams | K07 Firehose/Kinesis quotes above | Glue for Ray: compute job, not delivery; Managed Flink: a stream consumer itself, not a multi-consumer replay source; DataBrew: no stream concept |
| s01-mc | S01 | Lake Formation database/table grants vs per-analyst IAM vs Intelligent-Tiering vs Glue for Ray filter | Lake Formation | "grants access through Lake Formation's grant/revoke permissions model rather than individual S3 bucket policies" | per-analyst IAM: permission-by-permission, not by database/table; Intelligent-Tiering: storage cost feature; Glue for Ray filter: a transform, not a permission system |
| s01-mr | S01 | Hybrid access mode (incremental migration) vs data lake administrator (grants permissions), crawler/storage-class-analysis/EMR Serverless as foils | Hybrid access mode, data lake administrator | "Hybrid access mode lets you secure and access the cataloged data using both Lake Formation permissions and IAM"; "Designate a data lake administrator as the first user of the Data Catalog" | crawler: schema only; storage class analysis: cost optimization; EMR Serverless: compute runtime |
| s02-mc | S02 | Kinesis Data Streams (multi-consumer durable layer) vs Firehose vs DataBrew vs QuickSight | Kinesis Data Streams | "Kinesis Data Streams retains an ordered, replayable stream that multiple independent consumers can read at their own pace" | Firehose: single destination, no replay; DataBrew: no ingestion role; QuickSight: visualization only |
| s02-mr | S02 | Enhanced fan-out (dedicated throughput) vs Firehose buffer size/interval (fewer, larger files), retention/on-demand/smaller-buffer as foils | Enhanced fan-out, larger Firehose buffer | "a consumer that registers for enhanced fan-out instead gets its own dedicated 2 MiB/second per shard"; Firehose buffering hints trade latency for larger, cheaper delivery files | retention period: replay window, not throughput; on-demand mode: total capacity, not per-consumer guarantee; smaller buffer: more small files |
| s03-mc | S03 | S3 File Gateway (persistent hybrid share) vs nightly DataSync vs Kinesis vs Lake Formation mount | S3 File Gateway | lesson 3.1 K01 (via 3.5 S03 reference): "presents an NFS or SMB file share backed by an S3 bucket, with a local cache" | nightly DataSync: task-based, not continuously mounted; Kinesis: event records, not files; Lake Formation: no mount/file-share capability |
| s03-mr | S03 | AWS Data Transfer Terminal (no-network offline) vs Kinesis (continuous telemetry), DataBrew/File Gateway/EMR as foils | Data Transfer Terminal, Kinesis Data Streams | "a very large, offline transfer with no viable network path now points to the physical AWS Data Transfer Terminal facility, since Snowball Edge no longer accepts new customers" | DataBrew: no transfer mechanism; File Gateway: persistent share, not event stream; EMR: processes landed data, not a live ingestion path |
| s04-mc | S04 | QuickSight + SPICE (fast, periodically refreshed) vs direct query vs repeated Athena query vs static Ray report | QuickSight + SPICE | "importing them into SPICE...avoids re-querying the source on every interaction...materially faster, more scalable dashboards" | direct query: fresher but not the cached performance wanted; repeated Athena query: same cost, no dashboard; Glue for Ray report: static, not interactive |
| s04-mr | S04 | Glue crawler (schema) vs Athena (QuickSight's data source), DataBrew/EMR Serverless/Lake Formation as foils | Glue crawler, Athena | "Glue crawler catalogs it, Athena...exposes it as queryable tables, and QuickSight connects to Athena as its data source" | DataBrew: cleans, doesn't catalog; EMR Serverless: compute, not a QuickSight source; Lake Formation: permissions, not a queryable source |
| s05-mc | S05 | EMR cluster mode (persistent, tunable, custom software) vs Athena vs Glue ETL vs EMR Serverless | EMR (cluster mode) | "EMR (cluster mode) is the choice when a workload needs a long-lived, tunable, multi-node cluster...custom cluster software, or fine-grained control" | Athena: no cluster concept; Glue ETL: serverless, no fine-grained tuning; EMR Serverless: removes the cluster (and the tuning) the requirement needs |
| s05-mr | S05 | Athena (occasional SQL) vs EMR Serverless (existing Spark, no cluster), EMR cluster/DataBrew/Lake Formation as foils | Athena, EMR Serverless | "EMR Serverless runs the same open-source big-data frameworks...as classic EMR without provisioning or sizing a cluster" | EMR cluster mode: too much infrastructure for an occasional query; DataBrew: can't run existing Spark code; Lake Formation: no execution role |
| s06-mc | S06 | Partition-key redesign (hot shard) vs retention vs Firehose interval vs "MSK broker" foil (concept confusion) | Better partition key | "a Kinesis Data Streams partition key that is too uniform overloads a single shard" | retention: replay window, unrelated; Firehose interval: downstream batching, not shard routing; "MSK broker" on a Kinesis stream: category confusion (Kinesis has shards, not brokers) |
| s06-mr | S06 | S3 date partitioning + matching Hive-style Athena partition keys, shard-count/buffer-size/Intelligent-Tiering as foils | Partition scheme + matching table keys | "an S3 landing-zone partition scheme...determines how efficiently Athena and Glue can later prune data" | shard count: ingest throughput, not file layout; buffer size: file cadence, not partitioning; Intelligent-Tiering: storage cost, not query pruning |
| s07-mc | S07 | CSV-to-Parquet conversion (Glue ETL or Athena CTAS) vs shard count vs DataBrew storage vs enhanced fan-out | Convert to Parquet | "converting from row-based CSV...into a columnar format such as Parquet...lets a query read only the columns it needs" | shard count: Kinesis concept, unrelated to a landed S3 dataset; DataBrew "storage": not a storage location and doesn't change format; enhanced fan-out: a Kinesis consumer feature, not an Athena setting |
| s07-mr | S07 | Parquet conversion (storage) + date partitioning (query pruning), retention/Transfer Acceleration/MSK storage as foils | Convert to Parquet, partition by date | benchmark: "a saving of 99% and improved performance by 95%"; partitioning restricts data scanned | Kinesis retention: unrelated to a CSV file's size; S3 Transfer Acceleration: speeds transfer, not query scan; MSK broker storage: a Kafka-cluster setting, unrelated to Athena/Parquet |

## Distractor-type table

**Update (post round-1 review):** the Teacher/AWS review flagged that DataBrew appeared as a choice in 10 of 24 questions, breaking the 15% (3-question) cap. Fixed by replacing the DataBrew distractor in 7 questions (`k01-mr`, `k07-mc`, `k07-mr`, `s02-mc`, `s03-mr`, `s04-mr`, `s05-mr`) with a different real, lesson-taught option that fails the same stated requirement for its own distinct reason, and updating each rationale accordingly:

- `k01-mr` choice c: DataBrew &rarr; **a Glue ETL job** ("for the interactive dashboards") -- a scheduled transform job, no dashboard capability.
- `k07-mc` choice d: DataBrew &rarr; **a scheduled AWS Glue ETL job** -- batch-scheduled, not continuous low-latency stream computation.
- `k07-mr` choice e: DataBrew &rarr; **an Amazon S3 access point** ("for the independent replay") -- a network/permission scope, no stream or replay concept.
- `s02-mc` choice c: DataBrew &rarr; **an AWS Glue ETL job** ("as the shared ingestion layer") -- transforms already-landed data, not itself an ingestion layer.
- `s03-mr` choice b: DataBrew &rarr; **an AWS DataSync task** ("for the offline archive") -- an online transfer service that still needs network bandwidth the scenario says isn't available, which is exactly why AWS points to the physical Data Transfer Terminal instead.
- `s04-mr` choice a: DataBrew &rarr; **an Amazon S3 access point** ("for the schema cataloging") -- scopes access, doesn't scan files or discover schema.
- `s05-mr` choice d: DataBrew &rarr; **an Amazon S3 access point** ("for the existing Spark job") -- scopes access, has no compute capability at all.

DataBrew now appears in only 3 files: `k04-mc` and `s07-mc` as a distractor (2 instances, each testing a distinct reason -- no scheduled/scripted execution, and not a storage/format-conversion tool), and `k04-mr` as the correct answer (visual, no-code cleaning is genuinely DataBrew's job there, so it isn't a "distractor type" instance at all). Both remaining distractor uses sit in the K04/S07 Glue-and-format neighborhood where the contrast is most natural, and 2 &le; 3 satisfies the cap.

Replacement services were chosen to avoid pushing any other type over the cap: **Glue ETL job** and **Amazon S3 access point** were essentially unused as distractors before this fix, so each absorbed exactly 3 of the 7 replacements (Glue ETL job: `k01-mr`, `k07-mc`, `s02-mc`; S3 access point: `k07-mr`, `s04-mr`, `s05-mr`) and DataSync absorbed 1 (`s03-mr`, bringing its distractor-instance count to 2). No previously-used type increased beyond 3 as a result of this fix.

| Type | Description | Questions using it (count) |
|---|---|---|
| Data-prep tool confused with pipeline/schema/storage role | DataBrew offered as a scheduled ETL or format-conversion role | k04-mc, s07-mc (2) |
| ETL/transform job confused with dashboard/ingestion/compute role | A Glue ETL job offered where a dashboard, a durable ingestion layer, or continuous stream computation is needed | k01-mr, k07-mc, s02-mc (3) |
| Access/network scoping mechanism confused with compute or discovery role | An S3 access point offered for stream replay, schema discovery, or running compute -- it only scopes network/permission access | k07-mr, s04-mr, s05-mr (3) |
| Governance/execution confusion | Lake Formation (or its admin role) offered as a query, dashboard-source, mount, or execution mechanism | k01-mc, k05-mc, s03-mc, s04-mr, s05-mr (5 -- pre-existing, not touched this round; flagged below) |
| Visualization tool misapplied | QuickSight/SPICE offered as an ingestion, cataloging, or query-execution role instead of a dashboard layer | k01-mc, s02-mc, s04-mc (3) |
| Compute cluster/serverless mismatch | EMR cluster vs. EMR Serverless vs. Athena vs. Glue mismatched to the stated management-overhead or tuning requirement | k01-mc, k04-mr, s01-mr, s03-mr, s04-mr, s05-mc, s05-mr (7 combined across the EMR/EMR-Serverless family -- pre-existing, flagged below) |
| Athena misapplied | Athena (ad hoc query or CTAS) offered for a dashboard, schema-discovery, or persistent-job role | k01-mr, k04-mc, k04-mr, s04-mc, s05-mc (5 -- pre-existing, flagged below) |
| Wrong ingestion timing/frequency | Batch, micro-batch, or streaming mismatched to a stated latency requirement | k02-mc (1) |
| Transfer service mismatched to persistence/connectivity shape | DataSync / Storage Gateway / Data Transfer Terminal mismatched to one-time vs. persistent vs. no-network needs | k03-mc, s03-mc, s03-mr (3) |
| Access-control mechanism mismatched to scope | Bucket policy / broad IAM+naming / Lake Formation admin offered instead of a scoped S3 access point | k05-mc (1) |
| Streaming-service lever misapplied to the wrong problem | Kinesis retention/on-demand/shard-count, Firehose buffer settings, or an invented "MSK broker" concept applied to solve an unrelated problem | k03-mc, k06-mc, s02-mr, s06-mc, s06-mr, s07-mc, s07-mr (7 combined across every Kinesis/Firehose/MSK lever -- pre-existing, flagged below) |
| Partition/format mismatch | A configuration change targets the wrong layer (ingest throughput, storage tier) instead of partitioning or columnar format | s01-mc, s01-mr, s06-mr, s07-mr (4 -- pre-existing, flagged below) |

**Known follow-up (out of scope for this round's DataBrew fix):** four rows above still read over the literal 3-question cap when every occurrence of a broad service family (EMR/EMR Serverless, Athena, Lake Formation, the Kinesis/Firehose/MSK lever family) is lumped into one row. This is a structural tension rather than something introduced by the DataBrew fix: with only about a dozen services taught in this lesson and 24 questions each needing 3-4 real, on-topic distractors, some service inevitably recurs more than 3 times if "type" is read as "named service" rather than "specific error pattern" (sub-splitting by exact lever -- e.g. "Kinesis retention period misapplied" vs. "Firehose buffer size misapplied" vs. "an invented MSK-on-Kinesis concept" -- brings each sub-type to 2-3). Flagging this explicitly rather than silently re-bucketing it as compliant; if the reviewer wants these families thinned further, the same swap-in-a-different-real-option technique used for DataBrew applies (e.g., replacing 2-3 of the Lake Formation or EMR instances with Glue crawler, S3 access point, or DataSync/Storage Gateway alternatives).

## Watch items addressed

1. **DataSync/Storage Gateway distractor reasoning**: k03-mc and s03-mc both frame the DataSync-vs-File-Gateway distinction exactly as lessons 3.1 and 3.5 teach it (one-time/high-speed transfer vs. persistent, cached, continuously mounted share), and both cite `cite-saa-3-1-datasync-what-is` / `cite-saa-3-1-storage-gateway-types` alongside the 3.5 citations. s03-mr's Data Transfer Terminal / Snowball-retirement reasoning cites `cite-saa-3-1-snowball-edge-eol`.
2. **S05 compute options**: s05-mc and s05-mr only use Athena, Glue (ETL job or DataBrew as a clearly-wrong foil), EMR Serverless, and EMR cluster mode as choices -- no Lambda, no Redshift, and no "manage your own EC2 instance" strawman anywhere in either question.
3. **Renamed services**: all questions use "Amazon Data Firehose" and "Amazon Managed Service for Apache Flink" throughout; no question uses a "(formerly ...)" parenthetical on any choice, so there is no length-tell risk from partial parenthetical use.

## Remaining FAILs/WARNs

None from `q1_batch_check.py 3-5` at the question level. `content_lint.py` is a clean PASS.
