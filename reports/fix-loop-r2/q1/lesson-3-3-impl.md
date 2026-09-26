# Lesson 3.3 implementation report -- "Determine high-performing database solutions"

Scope: rewrote `content/lessons/lesson-3-3.json` (`bodyMarkdown`, `citationIds`, `drillIds`)
and added 16 new citation files `content/citations/cite-saa-3-3-*.json`. Deleted the
now-unreferenced placeholder citation `content/citations/cite-3-3.json` (grepped first;
only lesson-3-3.json referenced it). No question files or other lessons were touched.

Verification: `scripts/content_lint.py` → **PASS** (429 questions, 21+21 labs, 23 lessons).
Lesson body: 2,823 words, 14 `### ` sections (13 objective bullets + Warnings), 0
single-asterisk spans, 0 pipe-table characters, 0 markdown links. All 16 `citationIds`
resolve to files in `content/citations/`; all 21 `drillIds` resolve to files in
`content/questions/`.

## Section outline (bodyMarkdown)

| Order | Heading | Objective | Focus |
| --- | --- | --- | --- |
| 1 | K01 -- AWS global infrastructure | SAA-3.3-K01 | Region/AZ placement and its effect on database latency |
| 2 | K02 -- Caching strategies and services | SAA-3.3-K02 | ElastiCache, lazy loading vs write-through, TTL |
| 3 | K03 -- Data access patterns | SAA-3.3-K03 | read-intensive vs write-intensive design |
| 4 | K04 -- Database capacity planning | SAA-3.3-K04 | RDS instance classes, gp3 vs io2 |
| 5 | K05 -- Database connections and proxies | SAA-3.3-K05 | RDS Proxy connection pooling |
| 6 | K06 -- Database engines with appropriate use cases | SAA-3.3-K06 | homogeneous vs heterogeneous migration, AWS DMS + SCT |
| 7 | K07 -- Database replication | SAA-3.3-K07 | RDS read replicas vs Aurora Replicas/reader endpoint |
| 8 | K08 -- Database types and services | SAA-3.3-K08 | relational/key-value/document/in-memory/graph/time-series/wide-column mapped to AWS services, serverless pattern |
| 9 | S01 -- Configuring read replicas to meet business requirements | SAA-3.3-S01 | replica placement, routing, lag monitoring |
| 10 | S02 -- Designing database architectures | SAA-3.3-S02 | end-to-end design checklist; DynamoDB capacity modes, partition key/hot partitions, GSI vs LSI |
| 11 | S03 -- Determining an appropriate database engine | SAA-3.3-S03 | MySQL/MariaDB/PostgreSQL/Oracle/SQL Server/Aurora tradeoffs |
| 12 | S04 -- Determining an appropriate database type | SAA-3.3-S04 | scenario-to-service mapping, Aurora Serverless vs provisioned |
| 13 | S05 -- Integrating caching to meet business requirements | SAA-3.3-S05 | ElastiCache vs DAX selection |
| 14 | Warnings | -- | unchanged boilerplate (root user, teardown, budget alerts) |

Task 2.2 cross-references (not re-derived here): Multi-AZ instance vs cluster, read
replicas (HA angle), Aurora Replicas, Aurora Global Database, DynamoDB global tables,
RDS Proxy's failover role.

## Concepts per current question (placeholders, to be rewritten in Q1)

All 21 files under `content/questions/q-saa-3-3-*.json` are still the generic
"Apply the objective directly" / "Design against the stated requirement" placeholder
template (`mcpStatus: "pending_recheck"`, empty `citationIds`). Mapping objective → concept
the real question should test:

- `q-saa-3-3-k01-mc/mr` (K01): Region/AZ placement effect on database latency.
- `q-saa-3-3-k02-mc` (K02): lazy loading vs write-through vs TTL; ElastiCache vs DAX distinction.
- `q-saa-3-3-k03-mc` (K03): read-intensive vs write-intensive fix (replica vs bigger writer/sharding).
- `q-saa-3-3-k04-mc/mr` (K04): gp3 vs io2 selection; instance class families.
- `q-saa-3-3-k05-mc` (K05): RDS Proxy connection pooling vs resizing the instance.
- `q-saa-3-3-k06-mc` (K06): homogeneous (DMS only) vs heterogeneous (SCT + DMS) migration.
- `q-saa-3-3-k07-mc/mr` (K07): read replica (async, read scaling) vs Aurora Replica/reader endpoint (15 max, ms lag) vs Multi-AZ failover (task 2.2 boundary).
- `q-saa-3-3-k08-mc` (K08): matching an access pattern to relational/key-value/document/in-memory/graph/time-series/wide-column service; Aurora Serverless / DynamoDB on-demand as the serverless pattern; Timestream for LiveAnalytics retirement trap.
- `q-saa-3-3-s01-mc/mr` (S01): read replica routing/reader endpoint vs resizing the writer for a reporting-query bottleneck.
- `q-saa-3-3-s02-mc/mr` (S02): hot partition from poor key design vs insufficient capacity; GSI (new access pattern, added later) vs LSI (same partition key, sort key, created at table creation).
- `q-saa-3-3-s03-mc/mr` (S03): PostgreSQL-specific extensions / SQL Server stored procedures ruling out a same-family swap vs Aurora as the throughput/read-scaling default.
- `q-saa-3-3-s04-mc/mr` (S04): scenario → database type (cart/session = DynamoDB, catalog joins = relational, leaderboard = ElastiCache/MemoryDB, relationship walk = Neptune, unpredictable/bursty = serverless).
- `q-saa-3-3-s05-mc/mr` (S05): DAX for DynamoDB hot-key reads vs ElastiCache for a relational database's read-heavy queries.

## Retired / closed services found

- **Amazon Timestream for LiveAnalytics** closed new-customer access effective **6/20/25**
  (`https://docs.aws.amazon.com/timestream/latest/developerguide/AmazonTimestreamForLiveAnalytics-availability-change.html`).
  AWS now points new customers to **Amazon Timestream for InfluxDB**. The lesson (K08) names
  this explicitly and does not recommend LiveAnalytics for a new design; it is kept only as
  a legacy label a question might still use.
- Checked and **not** used in this lesson: **Amazon QLDB** (ledger database) -- objectives
  for task 3.3 do not ask for a ledger type, so it was left out entirely rather than cited as
  current; general knowledge (outside the docs I could re-confirm live in this pass) is that
  QLDB has also been wound down for new customers, so it should not be introduced later
  without a fresh docs check.
- Checked ElastiCache engines: **Valkey, Redis OSS, and Memcached** are all current
  (`AmazonElastiCache/latest/dg/SelectEngine.html`: "Amazon ElastiCache supports the Valkey,
  Memcached, and Redis OSS cache engines"). I initially drafted a citation note claiming
  Valkey is "the default engine for new clusters" -- that specific phrase came from a
  different, narrower e-commerce pattern page, not the general engine-selection page, so I
  removed the "default" claim from both the citation note and kept the lesson body's wording
  engine-neutral (it never asserted a default).
- No other end-of-support services (RDS magnetic storage is deprecated and is mentioned only
  implicitly by recommending gp3/io2; the lesson does not need to name magnetic storage).

## Corrections made after a first self-check

- Swapped the NoSQL-type-mapping citation from `choosing-an-aws-nosql-database` (a
  whitepaper explicitly marked *"for historical reference only"*) to the current, actively
  maintained `whitepapers/latest/aws-overview/database.html` comparison table.
- Swapped the Redshift citation from a whitepaper page that failed to render and from a
  second whitepaper also marked historical, to the current
  `redshift/latest/dg/c_redshift_system_overview.html` architecture page.
- Verified the gp3 baseline numbers (3,000 IOPS / 125 MiB/s) directly against
  `AmazonRDS/latest/UserGuide/CHAP_Storage.html` rather than leaving them unverified.
- Added the missing **compute-optimized** RDS instance-class family to K04 (the docs list
  general-purpose, memory-optimized, compute-optimized, burstable-performance, and Optimized
  Reads; the draft had omitted compute-optimized).
- Added that DynamoDB on-demand is "the default and recommended throughput option for most
  DynamoDB workloads" per `capacity-mode.html`, to match the doc's own framing in S02.

## Claim table

Every factual claim and number in `lesson-3-3.json`'s `bodyMarkdown`, one row per claim,
with the section, the claim, the doc URL, and a supporting quote (verbatim, <=20 words).

| Section | Claim | Doc URL | Verbatim quote |
| --- | --- | --- | --- |
| K02 | ElastiCache is an in-memory cache offering microsecond-scale latency | https://docs.aws.amazon.com/whitepapers/latest/aws-overview/database.html | "Unlock microsecond latency and scale with in-memory caching" |
| K02 | Lazy loading only loads data into the cache after a miss and can leave the cache stale | https://docs.aws.amazon.com/AmazonElastiCache/latest/dg/Strategies.html | "lazy loading is a caching strategy that loads data into the cache only when necessary" |
| K02 | Lazy loading's disadvantage is that data in the cache can become stale | https://docs.aws.amazon.com/AmazonElastiCache/latest/dg/Strategies.html | "data in the cache can become stale" |
| K02 | Write-through updates the cache on every database write | https://docs.aws.amazon.com/AmazonElastiCache/latest/dg/Strategies.html | "write-through strategy adds data or updates data in the cache whenever data is written to the database" |
| K02 | A TTL combines lazy loading and write-through while limiting staleness | https://docs.aws.amazon.com/AmazonElastiCache/latest/dg/Strategies.html | "Add a time to live value to each cache write to combine the benefits of lazy loading and write-through" |
| K04 | RDS storage choice is between gp3 (General Purpose SSD) and io2/io1 (Provisioned IOPS SSD) | https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/CHAP_Storage.html | "Amazon RDS provides two storage types: Provisioned IOPS SSD ... and General Purpose SSD" |
| K04 | gp3 baseline performance is 3,000 IOPS and 125 MiB/s | https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/CHAP_Storage.html | "Amazon RDS provides a baseline storage performance of 3000 IOPS and 125 MiB/s" |
| K04 | io2 Block Express is recommended for I/O-intensive, latency-sensitive workloads and scales to 256,000 IOPS | https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/CHAP_Storage.html | "we recommend that you use Provisioned IOPS SSD io2 Block Express storage to achieve up to 256,000" IOPS |
| K04 | RDS DB instance classes fall into general-purpose, memory-optimized, compute-optimized, and burstable-performance families | https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/Concepts.DBInstanceClass.Types.html | "Amazon RDS supports DB instance classes for the following use cases: General-purpose ... Memory-optimized ... Compute-optimized ... Burstable-performance" |
| K05 | RDS Proxy pools/multiplexes many client connections onto fewer database connections | https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/rds-proxy-best-practices.usage-scenarios.html | "multiplex many client connections onto fewer database connections, enabling applications to scale beyond the database instance's connection limit" |
| K06 | A homogeneous migration is between the same engine on source and target | https://docs.aws.amazon.com/prescriptive-guidance/latest/migration-sql-server/heterogeneous-migration-tools.html | "AWS DMS supports homogeneous migrations such as migrating data from one SQL Server database to another" |
| K06 | A heterogeneous migration needs AWS SCT to convert the schema before AWS DMS migrates data | https://docs.aws.amazon.com/prescriptive-guidance/latest/migration-sql-server/heterogeneous-migration-tools.html | "AWS SCT makes heterogeneous database migrations predictable by automatically converting the source database schema" |
| K07 | RDS read replicas are asynchronous, read-only copies used to offload reads | https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_ReadRepl.html | "Special RDS DB instance created from a source DB instance using built-in replication, receiving asynchronous updates" |
| K07 | An Aurora cluster supports up to 15 low-latency read replicas | https://docs.aws.amazon.com/rds/latest/auroraextendedcontent/aurora-features-scalability.html | "You can create up to 15 read replicas to increase read throughput without impacting performance on the primary instance" |
| K07 | Aurora Replicas share the primary's storage, giving single-digit-millisecond replica lag | https://docs.aws.amazon.com/rds/latest/auroraextendedcontent/aurora-features-scalability.html | "reduces the replica lag time -- often down to single-digit milliseconds" |
| K07 | Aurora provides a reader endpoint that load-balances across replicas automatically | https://docs.aws.amazon.com/rds/latest/auroraextendedcontent/aurora-features-scalability.html | "Aurora provides a reader endpoint for automatic connection routing and load balancing across read replicas" |
| K08 | Aurora storage auto-scales in 10 GB increments up to 256 TiB | https://docs.aws.amazon.com/rds/latest/auroraextendedcontent/aurora-features-scalability.html | "database volume expands in increments of 10 GB up to a maximum of 256 TiB" |
| K08 | Aurora Serverless scales compute automatically within a min/max ACU range, including to zero, with no connection-string change | https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/aurora-serverless-v2.how-it-works.html | "When your database is idle, Aurora will automatically scale down to zero" |
| K08 | ElastiCache currently supports Valkey, Memcached, and Redis OSS engines | https://docs.aws.amazon.com/AmazonElastiCache/latest/dg/SelectEngine.html | "Amazon ElastiCache supports the Valkey, Memcached, and Redis OSS cache engines" |
| K08 | DynamoDB is the AWS key-value database service | https://docs.aws.amazon.com/whitepapers/latest/aws-overview/database.html | "Amazon DynamoDB -- Fast, flexible NoSQL database service for single-digit millisecond performance at any scale" |
| K08 | Amazon DocumentDB is the AWS document database service | https://docs.aws.amazon.com/whitepapers/latest/aws-overview/database.html | "Amazon DocumentDB (with MongoDB compatibility) -- Scale JSON workloads with ease" |
| K08 | ElastiCache and MemoryDB are the AWS in-memory database/cache services | https://docs.aws.amazon.com/whitepapers/latest/aws-overview/database.html | "Amazon MemoryDB -- Redis-compatible, durable, in-memory database service for ultra-fast performance" |
| K08 | Amazon Neptune is the AWS graph database service | https://docs.aws.amazon.com/whitepapers/latest/aws-overview/database.html | "Amazon Neptune -- Build and run graph applications with highly connected datasets" |
| K08 | Amazon Keyspaces is the AWS wide-column (Cassandra-compatible) database service | https://docs.aws.amazon.com/whitepapers/latest/aws-overview/database.html | "Amazon Keyspaces -- A scalable, highly available, and managed Apache Cassandra-compatible database service" |
| K08 | Amazon Timestream is AWS's time-series database family | https://docs.aws.amazon.com/whitepapers/latest/aws-overview/database.html | "Amazon Timestream -- Fast, scalable, serverless time series database" |
| K08 | Amazon Timestream for LiveAnalytics closed to new customers effective 6/20/25 | https://docs.aws.amazon.com/timestream/latest/developerguide/AmazonTimestreamForLiveAnalytics-availability-change.html | "close new customer access to Amazon Timestream for LiveAnalytics, effective 6/20/25" |
| K08 | New Timestream customers are directed to Timestream for InfluxDB instead | https://docs.aws.amazon.com/timestream/latest/developerguide/AmazonTimestreamForLiveAnalytics-availability-change.html | "We recommend that new customers evaluate Amazon Timestream for InfluxDB as an alternative" |
| K08 / S03 | Amazon Redshift's performance comes from massively parallel processing, columnar storage, and compression | https://docs.aws.amazon.com/redshift/latest/dg/c_redshift_system_overview.html | "combination of massively parallel processing, columnar data storage, and very efficient, targeted data compression" |
| S02 | DynamoDB on-demand mode is pay-per-request with no capacity planning | https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/capacity-mode.html | "DynamoDB on-demand offers pay-per-request pricing for read and write requests so that you only pay for what you use" |
| S02 | On-demand is the default and recommended mode for most workloads | https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/capacity-mode.html | "On-demand mode is the default and recommended throughput option for most DynamoDB workloads" |
| S02 | Provisioned capacity mode fits steady, forecastable workloads for cost predictability | https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/capacity-mode.html | "choose to use provisioned capacity if you have steady workloads with predictable growth" |
| S02 | A poor partition key design creates hot partitions that throttle before total capacity is used | https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/bp-partition-key-uniform-load.html | "hot\" partitions that result in throttling and use your provisioned I/O capacity inefficiently" |
| S02 | A GSI can have a different partition/sort key than the base table and is created independently | https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/SecondaryIndexes.html | "index with a partition key and a sort key that can be different from those on the base table" |
| S02 | An LSI shares the base table's partition key but uses a different sort key | https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/SecondaryIndexes.html | "index that has the same partition key as the base table, but a different sort key" |
| S05 | DAX serves eventually-consistent reads from cache on a hit without touching DynamoDB | https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/DAX.concepts.html | "If DAX has the item available (a cache hit), DAX returns the item to the application without accessing DynamoDB" |
| S05 | DAX write operations are write-through: data is written to DynamoDB and DAX, succeeding only if both succeed | https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/DAX.concepts.html | "data is first written to the DynamoDB table, and then to the DAX cluster. The operation is successful only if" both succeed |

Conceptual sections without an independent number/citation (K01, K03, S01, S03, S04) build
directly on the specific claims above and on Multi-AZ/read-replica/Aurora facts already
established and cited in the approved lesson 2.2; they were not re-cited here to avoid
duplicate citation IDs across lessons.
