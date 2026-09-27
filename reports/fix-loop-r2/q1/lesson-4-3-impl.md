# Lesson 4.3 rewrite - implementation report

## Outline

- Replaced placeholder text in `content/lessons/lesson-4-3.json` with a full lesson covering all 14 objectives in order (K01-K09, S01-S05).
- Used one `###` section per objective and ended every section with an `**Exam tip:**` line.
- Preserved the `### Warnings` block content and removed the trailing placeholder citation line.
- Added explicit confusion contrasts required by scope: RDS vs Aurora vs Aurora Serverless v2; Aurora Standard vs Aurora I/O-Optimized; provisioned vs serverless; RDS Reserved Instances vs Savings Plans scope; Multi-AZ instance vs Multi-AZ DB cluster; read replicas vs standby; DynamoDB on-demand vs provisioned plus auto scaling and reserved capacity; DynamoDB Standard vs Standard-IA; ElastiCache and DAX; storage/backup/snapshot/PITR cost controls.
- Updated `drillIds` to all 22 task question IDs in objective order (including `-mc` and `-mr`).
- Replaced `cite-4-3` with new `cite-saa-4-3-*` citation files and deleted `content/citations/cite-4-3.json` after confirming it was only used by lesson 4.3.

## CLAIM TABLE

| # | Section | Claim | Doc URL | Quote (<=20 words) |
|---|---|---|---|---|
| 1 | K01 | RDS Reserved DB instances are one- or three-year commitments | https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_WorkingWithReservedDBInstances.html | "reserve a DB instance for a one- or three-year term" |
| 2 | K01 | Reserved DB instance discounts are billing discounts, not physical instances | https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_WorkingWithReservedDBInstances.html | "are not physical instances, but rather a billing discount" |
| 3 | K01 | Compute Savings Plans apply to EC2, Lambda, and Fargate | https://docs.aws.amazon.com/savingsplans/latest/userguide/sp-services.html | "Compute Savings Plans apply to usage across Amazon EC2, AWS Lambda, and AWS Fargate." |
| 4 | K03 | DAX can reduce latency from milliseconds to microseconds | https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/DAX.html | "from single-digit milliseconds to microseconds." |
| 5 | K03 | DAX can reduce overprovisioned read capacity cost | https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/DAX.html | "potential operational cost savings by reducing the need to overprovision read capacity units." |
| 6 | K04/S01 | RDS DB instance automated retention is 0-35 days | https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_WorkingWithAutomatedBackups.BackupRetention.html | "set the backup retention period of a DB instance to between 0 and 35 days." |
| 7 | K04/S01 | Multi-AZ DB cluster retention is 1-35 days | https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_WorkingWithAutomatedBackups.BackupRetention.html | "For a Multi-AZ DB cluster, you can set the backup retention period to between 1 and 35 days." |
| 8 | K04 | Manual snapshots do not expire | https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_CreateSnapshot.html | "manual snapshots aren't subject to the backup retention period. Snapshots don't expire." |
| 9 | K04/S01 | Aurora automated backup retention is 1-35 days | https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/Aurora.Managing.Backups.html | "You can specify a backup retention period from 1-35 days" |
| 10 | K04/S01 | Aurora latest restorable time is typically within 5 minutes | https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/Aurora.Managing.Backups.html | "typically within 5 minutes of the current time" |
| 11 | K04/S01 | DynamoDB PITR recovery period is 1-35 days | https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/PointInTimeRecovery_Howitworks.html | "Choose a value between 1 and 35 for your backup recovery period." |
| 12 | K04/S01 | DynamoDB PITR pricing is table-size based, not window-length based | https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/PointInTimeRecovery_Howitworks.html | "Changing the recovery window ... doesn't reduce the price." |
| 13 | K05 | One RCU is one strongly consistent read/sec up to 4 KB | https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/provisioned-capacity-mode.html | "one read capacity unit (RCU) represents one strongly consistent read operation per second" |
| 14 | K05 | One WCU is one write/sec up to 1 KB | https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/provisioned-capacity-mode.html | "A write capacity unit (WCU) represents one write per second for an item up to 1 KB." |
| 15 | K05 | New on-demand tables start at 4,000 writes and 12,000 reads/sec | https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/on-demand-capacity-mode.html | "up to 4,000 writes per second and 12,000 reads per second." |
| 16 | K05 | On-demand instantly supports up to double previous peak | https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/on-demand-capacity-mode.html | "instantly accommodates up to double the previous peak traffic on a table." |
| 17 | K05/K09 | Provisioned->on-demand switch limit is four times per 24 hours | https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/on-demand-capacity-mode.html | "up to four times in a 24-hour rolling window." |
| 18 | K05/S03 | Aurora Serverless ACU combines about 2 GiB memory plus CPU/network | https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/aurora-serverless-v2.how-it-works.html | "Each ACU is a combination of approximately 2 gibibytes (GiB) of memory" |
| 19 | K05/S03 | Aurora Serverless supports up to 0-256 ACUs | https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/aurora-serverless-v2.how-it-works.html | "Aurora serverless offers capacity from 0 ACUs to 256 ACUs." |
| 20 | K05/S03 | Aurora Serverless scaling increments can be as small as 0.5 ACU | https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/aurora-serverless-v2.how-it-works.html | "Scaling happens in increments as small as 0.5 ACUs." |
| 21 | K06 | RDS Proxy enables many client connections over smaller DB connections | https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/rds-proxy-planning.html | "open many client connections, while the proxy manages a smaller number of long-lived connections" |
| 22 | K06/K08 | RDS Proxy can reduce Multi-AZ failover times up to 66% | https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/rds-proxy-planning.html | "reduce failover times by up to 66%" |
| 23 | K07/S05 | DMS supports same-engine and cross-engine migration | https://docs.aws.amazon.com/dms/latest/userguide/CHAP_Introduction.html | "same database engine ... different database engines" |
| 24 | K07/S05 | DMS requires at least one endpoint on AWS | https://docs.aws.amazon.com/dms/latest/userguide/CHAP_Introduction.html | "one of your endpoints must be on an AWS service." |
| 25 | K08 | Read replicas are read-only copies of a DB instance | https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_ReadRepl.html | "A read replica is a read-only copy of a DB instance." |
| 26 | K08 | Primary-to-read-replica updates are asynchronous | https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_ReadRepl.html | "Amazon RDS copies them asynchronously to the read replica." |
| 27 | K08 | Multi-AZ standby replication is synchronous and standby cannot read | https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_ReadRepl.html | "Replication with the standby replica is synchronous. Unlike a read replica, a standby replica can't serve read traffic." |
| 28 | K08 | Multi-AZ DB instance failover is typically 60-120 seconds | https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/Concepts.MultiAZ.Failover.html | "Failover times are typically 60-120 seconds." |
| 29 | K08 | Multi-AZ DB cluster failover is typically under 35 seconds | https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/multi-az-db-clusters-concepts-failover.html | "Failover times are typically under 35 seconds." |
| 30 | K09/S03 | RDS is billed in 1-second increments with 10-minute minimum | https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/User_DBInstanceBilling.html | "RDS usage is billed in 1-second increments, with a minimum of 10 minutes." |
| 31 | K09/S03 | Aurora Standard bills I/O requests separately | https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/User_DBInstanceBilling.html | "for the Aurora Standard DB cluster configuration only." |
| 32 | K09/S03 | Aurora I/O-Optimized includes read/write I/O at no extra charge | https://docs.aws.amazon.com/rds/latest/auroraextendedcontent/aurora-faq-billing.html | "read and write I/O operations are included at no additional charge." |
| 33 | K09/S03 | Aurora I/O-Optimized can save up to 40% when I/O exceeds 25% | https://docs.aws.amazon.com/rds/latest/auroraextendedcontent/aurora-faq-billing.html | "I/O spend exceeding 25% ... save up to 40% on costs." |
| 34 | K09/S03 | DynamoDB reserved capacity one-year discount up to 54% | https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/reserved-capacity.html | "save up to 54% off standard rates for a one-year term" |
| 35 | K09/S03 | DynamoDB reserved capacity three-year discount up to 77% | https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/reserved-capacity.html | "77% off standard rates for a three-year term." |
| 36 | K09/S03 | DynamoDB reserved capacity sold in 100 RCU/WCU blocks | https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/reserved-capacity.html | "Reserved capacity is purchased in allocations of 100 WCUs or 100 RCUs." |
| 37 | K09/S03 | Standard-IA is storage-optimized and Standard is throughput-optimized | https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/WorkingWithTables.tableclasses.html | "Standard-Infrequent Access ... optimized for tables where storage is the dominant cost." |
| 38 | K09/S03 | 50% storage-to-throughput threshold for Standard-IA cost benefit | https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/WorkingWithTables.tableclasses.html | "When storage exceeds 50% of the throughput (reads and writes) cost" |
| 39 | S04 | Redshift columnar storage reduces disk I/O for analytics | https://docs.aws.amazon.com/redshift/latest/dg/c_challenges_achieving_high_performance_queries.html | "Columnar storage for database tables drastically reduces the overall disk I/O requirements" |
| 40 | S04 | Timestream for LiveAnalytics is closed to new customers (2025-06-20) | https://docs.aws.amazon.com/timestream/latest/developerguide/AmazonTimestreamForLiveAnalytics-availability-change.html | "close new customer access ... effective 6/20/25." |
| 41 | S02 | MySQL vs PostgreSQL selection discriminator for compatibility vs advanced features | https://docs.aws.amazon.com/AmazonRDS/latest/gettingstartedguide/choosing-engine.html | "Choose MySQL ... broad compatibility ... Choose PostgreSQL ... advanced features" |
| 42 | S05/K07 | DMS requires one endpoint on AWS and cannot do direct on-prem to on-prem | https://docs.aws.amazon.com/dms/latest/userguide/CHAP_Introduction.html | "one of your endpoints must be on an AWS service." |
| 43 | S01 | Fault-isolated boundaries limit failure impact to part of workload | https://docs.aws.amazon.com/wellarchitected/2023-10-03/framework/rel-10.html | "Components outside of the boundary are unaffected by the failure." |
| 44 | K09 | ACID in DynamoDB transactions means all-or-nothing correctness-preserving writes | https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/transactions.html | "Transactions provide atomicity, consistency, isolation, and durability (ACID)" |

## New citation files

- `content/citations/cite-saa-4-3-rds-billing.json`
- `content/citations/cite-saa-4-3-aurora-billing.json`
- `content/citations/cite-saa-4-3-aurora-faq-billing.json`
- `content/citations/cite-saa-4-3-savingsplans-services.json`
- `content/citations/cite-saa-4-3-rds-reserved.json`
- `content/citations/cite-saa-4-3-multiaz-concepts.json`
- `content/citations/cite-saa-4-3-multiaz-failover-instance.json`
- `content/citations/cite-saa-4-3-multiaz-failover-cluster.json`
- `content/citations/cite-saa-4-3-rds-read-replicas.json`
- `content/citations/cite-saa-4-3-rds-proxy-planning.json`
- `content/citations/cite-saa-4-3-dynamodb-ondemand.json`
- `content/citations/cite-saa-4-3-dynamodb-provisioned.json`
- `content/citations/cite-saa-4-3-dynamodb-reserved-capacity.json`
- `content/citations/cite-saa-4-3-dynamodb-table-classes.json`
- `content/citations/cite-saa-4-3-dynamodb-pitr.json`
- `content/citations/cite-saa-4-3-dax.json`
- `content/citations/cite-saa-4-3-elasticache-what-is.json`
- `content/citations/cite-saa-4-3-rds-backup-retention.json`
- `content/citations/cite-saa-4-3-rds-snapshots.json`
- `content/citations/cite-saa-4-3-aurora-backups.json`
- `content/citations/cite-saa-4-3-aurora-serverless-v2.json`
- `content/citations/cite-saa-4-3-dms-introduction.json`
- `content/citations/cite-saa-4-3-redshift-columnar.json`
- `content/citations/cite-saa-4-3-timestream-liveanalytics-change.json`

- `content/citations/cite-saa-4-3-rds-choosing-engine.json`

- `content/citations/cite-saa-4-3-waf-rel-10.json`

- `content/citations/cite-saa-4-3-dynamodb-transactions.json`

## Retired / renamed / closed-service finds

- Confirmed and used in-lesson status: **Amazon Timestream for LiveAnalytics is closed to new customers effective 2025-06-20**.
- Additional check for QLDB status in AWS documentation search did not return a current availability-change page; no new QLDB status entry added.
