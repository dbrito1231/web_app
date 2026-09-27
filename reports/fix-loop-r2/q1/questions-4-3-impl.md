# Questions 4.3 implementation report

## Per-question key and one-line justification

- `q-saa-4-3-k01-mc` -> d: Use consolidated billing and activate cost allocation tags for chargeback reporting.
- `q-saa-4-3-k02-mc` -> b: Use Cost Explorer for trends and forecasts, then Budgets alerts for the monthly threshold.
- `q-saa-4-3-k02-mr` -> b, e: Publish AWS Cost and Usage Report data for detailed line-item analysis.
- `q-saa-4-3-k03-mc` -> c: Add a DynamoDB Accelerator cluster in front of the table.
- `q-saa-4-3-k04-mc` -> a: Keep automated backup retention at 30 days and create monthly cluster snapshots.
- `q-saa-4-3-k05-mc` -> d: Use on-demand mode and remember provisioned-to-on-demand switching is limited to four times per 24 hours.
- `q-saa-4-3-k05-mr` -> a, d: One RCU supports one strongly consistent read per second for an item up to 4 KB.
- `q-saa-4-3-k06-mc` -> b: Place Amazon RDS Proxy in front of the database to pool connections and improve failover behavior.
- `q-saa-4-3-k07-mc` -> c: Select PostgreSQL as the engine baseline for advanced JSON and complex query support.
- `q-saa-4-3-k08-mc` -> a: Create read replicas and route reporting traffic to replica endpoints.
- `q-saa-4-3-k08-mr` -> c, e: Use Multi-AZ for synchronous standby failover protection.
- `q-saa-4-3-k09-mc` -> d: Use Amazon DynamoDB as the primary data store.
- `q-saa-4-3-s01-mc` -> b: Use tighter restore-point intervals and isolate failures so unaffected components stay outside the impact scope.
- `q-saa-4-3-s01-mr` -> b, d: Keep automated backups for day-to-day operational restore windows.
- `q-saa-4-3-s02-mc` -> c: Use PostgreSQL on Amazon RDS.
- `q-saa-4-3-s02-mr` -> a, c: Prioritize MySQL when framework compatibility and simpler transactional behavior are the top needs.
- `q-saa-4-3-s03-mc` -> a: Use Aurora Serverless v2 with a bounded ACU range for burst elasticity.
- `q-saa-4-3-s03-mr` -> d, e: Use on-demand mode for the unpredictable workload to avoid idle capacity planning.
- `q-saa-4-3-s04-mc` -> d: Use Amazon Redshift with columnar storage for analytical workloads.
- `q-saa-4-3-s04-mr` -> a, b: Treat Timestream for LiveAnalytics as closed to new customers during service selection.
- `q-saa-4-3-s05-mc` -> b: No; with AWS DMS at least one endpoint needs to be on an AWS service.
- `q-saa-4-3-s05-mr` -> c, d: Classify the move as heterogeneous and budget time for schema and query conversion.

## Distractor type table

Method: counted each non-key choice by first matching AWS service/token in the choice text; if none matched, counted as `Other-real-option`.

- Other-real-option: 23
- Aurora: 3
- DynamoDB: 3
- AWS Backup: 2
- Amazon RDS: 2
- CloudWatch: 2
- Neptune: 2
- API Gateway: 1
- AWS Batch: 1
- AWS Budgets: 1
- AWS Config: 1
- AWS Glue DataBrew: 1
- Athena: 1
- CloudTrail Lake: 1
- DataSync: 1
- DocumentDB: 1
- EMR: 1
- ElastiCache: 1
- EventBridge: 1
- IAM Access Analyzer: 1
- Inspector: 1
- Kendra: 1
- Keyspaces: 1
- Kinesis: 1
- Lex: 1
- NAT gateway: 1
- OpenSearch: 1
- Redshift: 1
- Route 53: 1
- SES: 1
- Secrets Manager: 1
- Shield Advanced: 1
- Step Functions: 1
- Storage Gateway: 1
- Systems Manager Parameter Store: 1
- Transfer Family: 1

## Balance stats

- MC longest-is-key: 2/14 = 14%
- MC key positions: {'d': 4, 'b': 4, 'c': 3, 'a': 3}
- MR key slots: {'b': 3, 'e': 3, 'a': 3, 'd': 4, 'c': 3}

## Lesson sentences added

- Added MySQL vs PostgreSQL discriminator sentence in S02 with concrete selection criteria.
- Added AWS DMS endpoint constraint sentence in S05 that one endpoint must be on AWS.
- Added plain-language definition of blast radius at first use in S01.
- Added plain-language ACID definition at first use in K09.
