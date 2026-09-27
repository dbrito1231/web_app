# Questions 4.3 implementation report

## Per-question key and one-line justification

- `q-saa-4-3-k01-mc` -> d: Use consolidated billing and activate cost allocation tags for chargeback.
- `q-saa-4-3-k02-mc` -> b: Use Cost Explorer for trend and forecast analysis, then configure AWS Budgets for threshold alerts.
- `q-saa-4-3-k02-mr` -> b, e: Publish Cost and Usage Report data for line-item chargeback analysis.
- `q-saa-4-3-k03-mc` -> c: Add DynamoDB Accelerator in front of the table.
- `q-saa-4-3-k04-mc` -> a: Set 30-day automated retention and create monthly manual cluster snapshots.
- `q-saa-4-3-k05-mc` -> d: Use on-demand capacity mode for launch traffic.
- `q-saa-4-3-k05-mr` -> a, d: One RCU supports one strongly consistent read per second for an item up to 4 KB.
- `q-saa-4-3-k06-mc` -> b: Place Amazon RDS Proxy in front of the database for connection pooling.
- `q-saa-4-3-k07-mc` -> c: Choose PostgreSQL for advanced JSON handling, complex queries, and extension support.
- `q-saa-4-3-k08-mc` -> a: Create read replicas and route reporting queries to replica endpoints.
- `q-saa-4-3-k08-mr` -> a, b: Use Multi-AZ DB instance deployment for synchronous standby failover.
- `q-saa-4-3-k09-mc` -> d: Use DynamoDB as the primary key-value datastore.
- `q-saa-4-3-s01-mc` -> b: Use tighter recovery coverage for critical components and isolate boundaries to reduce impact scope.
- `q-saa-4-3-s01-mr` -> a, b: Keep automated backups for day-to-day operational restore needs.
- `q-saa-4-3-s02-mc` -> b: Use PostgreSQL on Amazon RDS.
- `q-saa-4-3-s02-mr` -> a, b: Choose MySQL when broad framework compatibility and simpler transactional patterns are priority.
- `q-saa-4-3-s03-mc` -> a: Use Aurora Serverless v2 with a bounded ACU range for elasticity.
- `q-saa-4-3-s03-mr` -> a, b: Use on-demand mode for the unpredictable workload.
- `q-saa-4-3-s04-mc` -> a: Use Amazon Redshift with columnar storage for analytical scan workloads.
- `q-saa-4-3-s04-mr` -> a, b: Treat Timestream for LiveAnalytics as closed to new customers during solution selection.
- `q-saa-4-3-s05-mc` -> b: No; AWS DMS requires at least one endpoint, source or target, on an AWS service.
- `q-saa-4-3-s05-mr` -> a, b: Classify the migration as heterogeneous and plan schema and query conversion work.

## Distractor type table

Method: counted each non-key choice by first matching AWS service/token in the choice text; if none matched, counted as `Other-real-option`.

- Other-real-option: 36
- read replica: 5
- snapshot: 4
- AWS DMS: 3
- Multi-AZ: 3
- Amazon RDS: 2
- Aurora: 2
- Cost Explorer: 2
- ElastiCache: 2
- AWS Backup: 1
- AWS Budgets: 1
- Athena: 1
- Database Migration Service: 1
- DynamoDB: 1
- Standard-IA: 1
- Timestream: 1

## Balance stats

- MC longest-is-key: 3/14 = 21%
- MC key positions: {'d': 3, 'b': 5, 'c': 2, 'a': 4}
- MR key slots: {'b': 7, 'e': 1, 'a': 7, 'd': 1}

## Lesson sentences added

- Added MySQL vs PostgreSQL discriminator sentence in S02 with concrete selection criteria.
- Added AWS DMS endpoint constraint sentence in S05 that one endpoint must be on AWS.
- Added plain-language definition of blast radius at first use in S01.
- Added plain-language ACID definition at first use in K09.

## Round 2 rework summary

- Replaced category-error distractors with plausible database architecture alternatives that miss exactly one stated requirement.
- Removed giveaway and self-justifying phrasing from options and refreshed rationales to explain each distractor by content.
- Rebalanced wording and option lengths to keep longest-is-key within policy while preserving key-slot distribution.
- Reordered MR choices to remove key-pattern bias while keeping option text and correctness unchanged.
- MR key-set distribution: ad:1, ae:1, bc:1, bd:1, be:1, cd:1, ce:1, de:1.
