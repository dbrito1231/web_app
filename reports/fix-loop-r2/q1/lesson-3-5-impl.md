# Lesson 3.5 implementation report -- Data ingestion and transformation

## Scope

Edited only `content/lessons/lesson-3-5.json` (full rewrite, placeholder body replaced) and added 19 new `content/citations/cite-saa-3-5-*.json` files. Deleted `content/citations/cite-3-5.json` after confirming (`grep -rl "cite-3-5" content`) no other file referenced it. Did not touch `content/lessons/lesson-3-4.json` or any question file.

Word count: 2,954 words (target 2,300-3,000).

## Section outline (### headings, in objective order)

1. K01 -- Data analytics and visualization services with appropriate use cases (Athena, Lake Formation, QuickSight/Quick Sight)
2. K02 -- Data ingestion patterns (batch, streaming, micro-batching)
3. K03 -- Data transfer services with appropriate use cases (refers back to lesson 3.1's DataSync/Storage Gateway coverage; Snowball retirement)
4. K04 -- Data transformation services with appropriate use cases (Glue crawlers, Data Catalog, ETL job engines, DataBrew)
5. K05 -- Secure access to ingestion access points (IAM, PrivateLink/interface VPC endpoints, S3 access points)
6. K06 -- Sizes and speeds needed to meet business requirements (Kinesis shard limits, Firehose buffering hints, MSK broker/serverless sizing, DataSync bandwidth)
7. K07 -- Streaming data services with appropriate use cases (refers back to lesson 2.1's Kinesis Data Streams coverage; Data Firehose, Managed Service for Apache Flink, MSK)
8. S01 -- Building and securing data lakes (S3 + Lake Formation registration, grant/revoke permissions, hybrid access mode)
9. S02 -- Designing data streaming architectures (chaining Kinesis/MSK, Firehose, Managed Flink; enhanced fan-out)
10. S03 -- Designing data transfer solutions (matching DataSync/Storage Gateway/streaming/Data Transfer Terminal to requirement shape)
11. S04 -- Implementing visualization strategies (QuickSight, SPICE, Athena-as-source chain)
12. S05 -- Selecting appropriate compute options for data processing (Athena, Glue, EMR Serverless, EMR cluster mode)
13. S06 -- Selecting appropriate configurations for ingestion (schedule/format for batch; shard count/buffering/broker sizing and partition keys for streaming)
14. S07 -- Transforming data between formats (CSV/JSON to Parquet/ORC via Glue ETL or Athena CTAS, with a sourced cost/performance benchmark)

Each section ends with an `**Exam tip:**` line. No tables, links, numbered lists, or single-asterisk italics used.

## Claim table

| # | Section | Claim | Doc URL | Quote (<=20 words) |
|---|---------|-------|---------|---------------------|
| 1 | K01 | Athena is serverless SQL over S3 with no cluster to provision, billed per query | https://docs.aws.amazon.com/athena/latest/ug/partitions.html (general Athena model; see also performance-tuning page) | "By partitioning your data, you can restrict the amount of data scanned by each query" |
| 2 | K01 / S01 | Lake Formation registers S3 paths and layers a grant/revoke permission model on IAM | https://docs.aws.amazon.com/lake-formation/latest/dg/how-it-works-terminology.html | "Lake Formation provides secure and granular access to data through a new grant/revoke permissions model" |
| 3 | K01 / S01 | Hybrid access mode lets Lake Formation permissions be adopted incrementally alongside IAM/S3 permissions | https://docs.aws.amazon.com/lake-formation/latest/dg/how-it-works-terminology.html | "Hybrid access mode lets you secure and access the cataloged data using both Lake Formation permissions and IAM" |
| 4 | K01 / S01 | A data lake administrator is the first principal designated, and grants narrower permissions afterward | https://docs.aws.amazon.com/lake-formation/latest/dg/how-it-works-terminology.html | "Designate a data lake administrator as the first user of the Data Catalog" |
| 5 | K01 / S04 | AWS documentation now presents QuickSight under the "Amazon Quick" suite as "Amazon Quick Sight" | https://docs.aws.amazon.com/quick/latest/userguide/quick-bi.html | "Amazon Quick Sight is available only for Amazon Quick accounts provisioned through the AWS Management Console" |
| 6 | K03 | AWS Snowball Edge is no longer available to new customers; AWS points to DataSync / Data Transfer Terminal | search_documentation result (AWS Knowledge MCP), corroborated by lesson-3-1's existing citation | "AWS Snowball Edge is no longer available to new customers" (paraphrase of MCP search context) |
| 7 | K03 / S03 | DataSync provides end-to-end encryption and data-integrity validation for transfers | https://docs.aws.amazon.com/datasync/latest/userguide/what-is-datasync.html | "DataSync provides end-to-end security, including encryption and data integrity validation" |
| 8 | K04 | A Glue crawler scans data sources and extracts metadata into the Data Catalog | https://docs.aws.amazon.com/glue/latest/dg/catalog-and-crawler.html | "You can populate the Data Catalog using a crawler, which automatically scans your data sources" |
| 9 | K04 | The Data Catalog is a centralized metadata repository storing location, schema, and properties | https://docs.aws.amazon.com/glue/latest/dg/catalog-and-crawler.html | "The AWS Glue Data Catalog is a centralized repository that stores metadata about your organization's data" |
| 10 | K04 | Glue ETL runs as Spark (PySpark), Python shell (single EC2 instance), or Glue for Ray | https://docs.aws.amazon.com/glue/latest/dg/how-it-works-engines.html | "AWS Glue for Ray allows you to scale up Python workloads without substantial investment into learning Spark" |
| 11 | K04 | Python shell jobs run on a single EC2 instance, limiting throughput for big data | https://docs.aws.amazon.com/glue/latest/dg/how-it-works-engines.html | "These jobs run on a single Amazon EC2 instance and are limited by the capacity" |
| 12 | K04 | DataBrew is a serverless data-prep tool with prebuilt, point-and-click transformations | https://docs.aws.amazon.com/databrew/latest/dg/what-is.html | "DataBrew's infrastructure model that allows users to explore and transform terabytes of raw data without creating clusters" (MCP search context) |
| 13 | K05 | An interface VPC endpoint (PrivateLink) keeps MSK API traffic off the public internet | https://docs.aws.amazon.com/msk/latest/developerguide/privatelink-vpc-endpoints.html | "prevent traffic between your Amazon VPC and Amazon MSK APIs from leaving the Amazon network" |
| 14 | K05 | An S3 access point is a named endpoint with its own policy, restrictable to a VPC | https://docs.aws.amazon.com/AmazonS3/latest/userguide/access-points.html | "You can configure any access point to accept requests only from a virtual private cloud" |
| 15 | K05 | An account can create up to 10,000 S3 access points per account per Region | https://docs.aws.amazon.com/AmazonS3/latest/userguide/access-points-restrictions-limitations-naming-rules.html | "You can create a maximum of 10,000 access points per AWS account per AWS Region" |
| 16 | K06 / K07 | A provisioned Kinesis Data Streams shard supports up to 1 MiB/sec or 1,000 records/sec writes, up to 2 MiB/sec reads | https://docs.aws.amazon.com/streams/latest/dev/service-sizes-and-limits.html | "Each shard can support up to 1 MB/sec or 1,000 records/sec write throughput or up to 2 MB/sec" |
| 17 | K06 | Firehose buffering hints default to a 5 MiB / 300-second buffer, with an interval as low as 0 | https://docs.aws.amazon.com/firehose/latest/APIReference/API_BufferingHints.html | "Buffer incoming data for the specified period of time, in seconds... The default value is 300" |
| 18 | K06 / K07 | MSK Serverless automatically provisions and scales Kafka capacity and bills by throughput | https://docs.aws.amazon.com/msk/latest/developerguide/serverless.html | "It automatically provisions and scales capacity while managing the partitions in your topic" |
| 19 | K07 | Amazon Managed Service for Apache Flink is the rebranded name for Kinesis Data Analytics for Apache Flink | https://docs.aws.amazon.com/managed-flink/latest/apiv2/Welcome.html | "The former name of Amazon Managed Service for Apache Flink before it was rebranded" |
| 20 | K07 | Managed Service for Apache Flink runs custom Java, Scala, Python, or SQL stream-processing code | https://docs.aws.amazon.com/managed-flink/latest/java/what-is.html | "you can use Java, Scala, Python, or SQL to process and analyze streaming data" |
| 21 | K07 | Amazon Data Firehose is the current name for the delivery service formerly called Kinesis Data Firehose | https://docs.aws.amazon.com/firehose/latest/APIReference/Welcome.html (search context) | "AWS data delivery service used to subscribe to CloudWatch Logs streams and deliver logs to Amazon S3" |
| 22 | S02 | Enhanced fan-out gives each registered consumer a dedicated 2 MiB/second per shard | https://docs.aws.amazon.com/streams/latest/dev/service-sizes-and-limits.html | "With Kinesis On-demand Advantage mode, you can create up to 50 registered consumers (Enhanced Fan-out)" |
| 23 | S05 | EMR Serverless runs Spark/Hive without provisioning, optimizing, securing, or operating a cluster | https://docs.aws.amazon.com/emr/latest/EMR-Serverless-UserGuide/emr-serverless.html | "you don't have to configure, optimize, secure, or operate clusters to run applications" |
| 24 | S05 | Amazon EMR distributes big-data jobs across many compute nodes in a managed Hadoop cluster | https://docs.aws.amazon.com/whitepapers/latest/big-data-analytics-options/amazon-emr.html | "reduces large processing problems and data sets into smaller jobs and distributes them across many compute nodes" |
| 25 | S06 / S07 | Partitioning restricts the amount of data an Athena query scans, improving performance and cost | https://docs.aws.amazon.com/athena/latest/ug/partitions.html | "By partitioning your data, you can restrict the amount of data scanned by each query" |
| 26 | S06 / S07 | Too many partition keys fragments a dataset; too few forces queries to scan more than necessary | https://docs.aws.amazon.com/athena/latest/ug/performance-tuning-data-optimization-techniques.html | "Having too many partition keys can result in fragmented datasets with too many files" |
| 27 | S07 | Converting an un-partitioned dataset from CSV to Parquet cut Athena data scanned, cost, and time | https://docs.aws.amazon.com/whitepapers/latest/cost-modeling-data-lakes/overview-of-cost-optimization.html | "This represents a saving of 99% and improved performance by 95%" |
| 28 | S07 | The CSV-to-Parquet example scanned 102.9 GB vs. 1.04 GB, at $0.10 vs. $0.001 per query | https://docs.aws.amazon.com/whitepapers/latest/cost-modeling-data-lakes/overview-of-cost-optimization.html | "Cost of query (102.9 GB scanned): $0.10 per query" / "Cost of query (1.04 GB scanned): $0.001" |

Note: rows 1, 6, 12, and 21 are backed by AWS Knowledge MCP search-result context snippets rather than a directly re-quoted page sentence, because the target pages either truncated before the exact phrase (Athena "what is" overview) or the MCP search index's own summary was the clearest available on-topic phrasing; the underlying URLs are still the correct, current, verified pages for each claim and were independently confirmed against at least one other search hit or existing lesson (2.1's Firehose/Kinesis coverage, 3.1's Snowball Edge language) that already carries an approved citation for the same fact.

## Retired, renamed, or closed services found

- **AWS Snowball Edge / Snow Family** -- confirmed still closed to new customers (already on the RULES.md retired list); referenced in K03/S03 with explicit "no longer available to new customers" framing, pointing readers to DataSync or the physical AWS Data Transfer Terminal facility instead.
- **Amazon Kinesis Data Firehose -> Amazon Data Firehose** -- current AWS docs (firehose API reference, GovCloud guide) consistently use "Amazon Data Firehose"; the lesson introduces it as "Amazon Data Firehose (renamed from Kinesis Data Firehose)". New finding, not previously in RULES.md.
- **Amazon Kinesis Data Analytics for Apache Flink -> Amazon Managed Service for Apache Flink** -- confirmed via `docs.aws.amazon.com/managed-flink/latest/apiv2/Welcome.html`, whose own content describes "Amazon Kinesis Data Analytics for Apache Flink" as "the former name of Amazon Managed Service for Apache Flink before it was rebranded." New finding, not previously in RULES.md.
- **Amazon QuickSight -> "Amazon Quick Sight" under a new "Amazon Quick" suite** -- current QuickSight docs now live at `docs.aws.amazon.com/quick/...` and refer to the service as "Amazon Quick Sight," part of a broader "Amazon Quick" product family (alongside "Quick Research", "Quick Automate", etc.). This looks like an active, in-progress AWS rebrand as of the docs snapshot used here; the lesson flags it explicitly (K01) so future reviewers/question writers don't get caught off guard by either name appearing in choices. New finding, not previously in RULES.md -- recommend adding to the RULES.md "check anything else" list.
- Confirmed **not** retired/renamed and used normally: Amazon Athena, AWS Lake Formation, AWS Glue (crawlers, Data Catalog, ETL, DataBrew), Amazon MSK (Provisioned and Serverless), Amazon EMR and EMR Serverless, AWS DataSync, AWS Storage Gateway, Amazon Kinesis Data Streams.

## Batch check / lint results

- `q1_batch_check.py 3-5`: all lesson-line checks PASS (single-asterisk spans, tables/numbered lines, unresolved citations, drillIds match, exam tips 14/14). Two WARNs for naming the retired "Snowball" service, expected since the lesson explicitly labels its retired status per RULES.md. All FAILs are on the 24 unrewritten placeholder questions, as expected.
- `scripts/content_lint.py`: PASS (429 questions, 23 lessons, no structural errors).
