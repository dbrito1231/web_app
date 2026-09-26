# Task 3.3 question rewrite -- implementation report

Scope: rewrote all 21 files `content/questions/q-saa-3-3-*.json` (real scenario stems,
4/5 real choices, exactly-one/`selectCount` keys, content-based rationale, `citationIds`
pointing at existing `cite-saa-3-3-*` files, `mcpStatus: "verified"`,
`reviewedOn: "2026-09-26"`). `id`, `type`, `module`, `objectiveIds`, and `selectCount` for
each question were kept from the placeholder files except where `selectCount` needed to
equal the number of keys chosen (all MR questions already had `selectCount: 2`, unchanged).
No lesson, citation, or other task's files were touched in this step.

## Batch-check result

```
task 3-3: 21 questions
PASS: lesson single-asterisk spans: 0
PASS: lesson tables/numbered lines: 0
PASS: lesson citations unresolved: []
PASS: drillIds match questions (missing [], extra [])
PASS: exam tips 13 for 13 objectives
PASS: duplicate 6-word openings: []
PASS: longest-is-key 3/13 = 23%
PASS: MC key positions {'a': 4, 'b': 3, 'c': 3, 'd': 3}
PASS: MR key slots {'a': 6, 'b': 6, 'c': 1, 'd': 2, 'e': 1}
RESULT: PASS
```

`scripts/content_lint.py` also PASSes after the rewrite (429 questions, 21+21 labs, 23
lessons). No FAIL or WARN lines were produced (no tell-word or retired-name hits on any
choice; a self-written pre-check for the same regexes the checker uses found zero hits
before the official run confirmed it).

## Per-question table

Objective text is paraphrased, not quoted, per the no-paste rule. "Lesson quote" cells are
short, exact substrings from `lesson-3-3.json`'s `bodyMarkdown` (double-asterisk markers
stripped for readability).

| Question | Tests | Key | Lesson quote for key | Lesson quote for each distractor |
| --- | --- | --- | --- | --- |
| k01-mc | Cross-Region read replica shortens a distant reader's path | a: cross-Region replica near Sydney | "placing read replicas in AZs or Regions near the readers who use them shortens the read path further" | b (bigger instance), c (io2 storage): both raise compute/IOPS, not geography, per K04's "guaranteed, consistent IOPS rate" framing being a different lever than K01's Region/AZ framing; d (RDS Proxy): "pooling and multiplexing many client-side connections", a connection-count fix, not a distance fix |
| k01-mr | Same-Region deployment + cross-Region replica both cut cross-Region latency | a, c | same K01 quote as above, plus "A cross-Region call to a database adds tens of milliseconds that a same-Region call does not" | b, d (IOPS/auto scaling): storage-side fixes unrelated to Region placement; e (replica back in the source Region): same K01 quote shows proximity to the *reader* is what matters, and a source-Region replica is not closer to a us-east-1 reader |
| k02-mc | Write-through vs lazy loading/TTL for "must be current on next read" | b: write-through | "Write-through updates the cache every time the application writes to the database, so cached data is always current" | a (shorter TTL): "lazy loading ... only loads an item into the cache after the application asks for it and misses ... can hold stale data until it expires" -- still stale until expiry; c (DAX in front of ElastiCache): DAX is described only as "DynamoDB's own purpose-built ... cache and is a separate service from ElastiCache"; d (longer TTL): opposite of the K02 TTL guidance |
| k03-mc | Write-intensive workload needs compute/IOPS, not read fixes | c: bigger instance + IOPS | "write-intensive ... does not benefit from read replicas at all ... and instead needs a larger instance class, provisioned IOPS storage" | a, d (replica/reader endpoint), b (ElastiCache): all read-side fixes the same K03 sentence rules out for a write-heavy pipeline |
| k04-mc | io2 for a guaranteed IOPS floor above gp3's baseline | d: io2 | "Provisioned IOPS SSD (io2) ... is for I/O-intensive, latency-sensitive transactional workloads that need a guaranteed, consistent IOPS rate higher than gp3 can provide" | a (gp3 + auto scaling): auto scaling grows size, not the IOPS ceiling; b (burstable class): "burstable classes earn CPU credits during idle periods and can be throttled ... under sustained load"; c (replica on gp3): replicas add read capacity, not the primary's own IOPS guarantee |
| k04-mr | gp3-IOPS-bump and io2 both relieve a confirmed storage I/O bottleneck | b, d | K04's gp3 baseline/threshold text and the io2 quote above | a, c (instance-class changes): K04 frames instance class as compute, separate from "Storage is chosen and sized separately from compute"; e (replica for reads): does not touch the primary's write-side storage I/O |
| k05-mc | RDS Proxy pooling fixes connection exhaustion, not compute/storage | a: RDS Proxy | "pooling and multiplexing many client-side connections onto a much smaller number of actual database connections, which both prevents connection exhaustion and reduces the CPU and memory overhead of opening new database connections repeatedly" | b, c (bigger instance/io2): K05's own exam tip says "add RDS Proxy rather than resizing the instance"; d (split across replica): each instance still receives full unpooled connections |
| k06-mc | Heterogeneous migration needs SCT (schema) then DMS (data) | b: SCT then DMS | "a heterogeneous migration ... is a two-step process: the AWS Schema Conversion Tool (AWS SCT) first converts the source schema ... and only then does AWS DMS migrate" | a (DMS alone): "DMS moves data, it does not rewrite schemas or stored procedures"; c (SCT alone moves data too): SCT is described only as converting schema/code, not migrating data; d (DMS replication converts procedures): DMS's role in the lesson is limited to moving/replicating data |
| k07-mc | Aurora Replicas + reader endpoint auto-route new readers | c: Aurora Replicas + reader endpoint | "a cluster can run up to 15 of them behind a single reader endpoint that load-balances connections across whichever replicas are currently healthy" | a (standalone RDS replicas): K07 distinguishes Aurora Replicas (shared storage, ms lag) from ordinary RDS read replicas (separate copies, asynchronous); b (Multi-AZ cluster): task 2.2 concept, capped at two standbys, a different deployment type; d (promote a replica): removes it from the reader pool |
| k07-mr | True vs false facts about Aurora Replica limits/mechanics | a, b | "up to 15" and reader-endpoint quotes above | c, d, e are constructed negations of the same taught facts (Region restriction, separate storage copies, no-downtime add/remove) that the lesson's K07/K08 text establishes as false (shared storage, in-Region by default, dynamic add/remove via the reader endpoint) |
| k08-mc | Current vs retired time-series service, plus wrong category | d: Timestream for InfluxDB | "closed to new customers on 6/20/25 ... AWS now points new customers to Amazon Timestream for InfluxDB instead" | c (Timestream for LiveAnalytics): the same quote shows it is closed to new customers; a (Neptune), b (Keyspaces): K08's own service list ties Neptune to graph and Keyspaces to wide-column, not time series |
| s01-mc | Read replica removes a reporting bottleneck from the primary | a: read replica | S01: "add same-Region read replicas to offload reporting or analytics queries from the primary" | b (more storage): unrelated to query compute load; c (RDS Proxy): pools connections, does not reduce query work; d (DAX in front of RDS): DAX is DynamoDB-only per K02 |
| s01-mr | Reader-endpoint routing + lag monitoring are the safe operational steps after adding replicas | b, e | S01: "route the application's read traffic ... to the single reader endpoint for Aurora so new replicas join the pool transparently; and monitor replica lag, since a replica that falls too far behind can return noticeably stale data" | a (promote immediately): "Promoting a replica breaks replication permanently and should be reserved for failover"; c (write to a replica): replicas are read-only per K07; d (grow primary storage): Aurora Replicas share the primary's storage automatically |
| s02-mc | Hot partition needs a higher-cardinality key, not more capacity | b: redesign the key | "a key with too few distinct values, or one where most traffic lands on a small number of values, creates a hot partition that throttles requests well before the table's total capacity is exhausted" | a (switch billing mode): same S02 text frames capacity mode and partition key design as separate levers; c (raise capacity): the quote explicitly says throttling happens "well before ... total capacity is exhausted"; d (GSI on the same attribute): a new index on the same low-cardinality attribute inherits the same key |
| s02-mr | GSI can be added later with a different key; LSI cannot | a, d | "global secondary index (GSI) has its own partition key ... different from the base table's ... can be added or removed at any time" | b, c (LSI addable anytime / both need up-front definition): the lesson states the opposite -- "local secondary index (LSI) shares the base table's partition key ... must be created when the table is created"; e (LSI fits any pattern): LSI is scoped to the base table's own partition key |
| s03-mc | Aurora PostgreSQL keeps extensions and adds throughput/replica scaling | c: Aurora PostgreSQL | "PostgreSQL adds richer data types, extensions ... is the engine of choice when an application needs those extensions" plus "Amazon Aurora ... is the default recommendation when an application is compatible with either open-source engine and wants Aurora's higher throughput ... and up to 15 low-lag replicas" | a (Aurora MySQL): a different SQL dialect, breaking Postgres-only extensions; b (Redshift): K08/S03 ties Redshift to OLAP, not this OLTP workload; d (RDS PostgreSQL, replicas only): keeps the engine but not Aurora's replica count/lag |
| s03-mr | SCT+DMS for the SQL Server move; Aurora for the new, dependency-free workload | a, b | K06 SCT/DMS quote above; S03 Aurora "default recommendation" quote above | c (DMS alone): skips the schema-conversion step K06 requires; d (RDS for SQL Server): keeps a dependency the stem says does not exist for the new workload; e (SCT alone moves data): SCT only converts schema/code per K06 |
| s04-mc | Unpredictable key-value scale needs DynamoDB on-demand | d: DynamoDB on-demand | "on-demand ... bills per request and scales instantly with no capacity planning ... the default, recommended starting point for most workloads and well suited to unpredictable or spiky traffic" | a (fixed RDS instance): relational, must be pre-sized, the opposite of unpredictable-scale fit; b (Redshift): built for analytics, not single-item lookups; c (DynamoDB provisioned, fixed throughput): right service, "costs less for steady, predictable traffic you can forecast" -- the opposite of this scenario |
| s04-mr | Neptune for graph traversal; ElastiCache for a low-latency leaderboard | a, b | K08: "Graph -- traversing many-to-many relationships ... Amazon Neptune stores nodes and edges"; K02: ElastiCache "cutting both latency (microseconds instead of milliseconds)" | c (Keyspaces for traversal): K08 ties Keyspaces to wide-column, not graph; d (Redshift for the leaderboard): K08/S03 ties Redshift to OLAP, not low-latency lookups; e (DocumentDB for traversal): K08 ties DocumentDB to documents, not graph edges |
| s05-mc | DAX caches DynamoDB with zero call changes; ElastiCache needs a code change | a: DAX | "DAX ... sitting transparently in front of the table and answering GetItem, BatchGetItem, Query, and Scan calls from its own in-memory cache without any application changes to those calls" | b (ElastiCache + rewritten calls): S05 exam tip contrasts DAX's no-code-change fit against a relational-database cache that does need call changes; c (more provisioned read capacity): still sends every hot-key read to DynamoDB; d (GSI on product ID): changes query shape, not re-read frequency |
| s05-mr | DAX pairs with DynamoDB; ElastiCache pairs with the RDS workload | a, b | S05: "choose DAX when the database being cached is DynamoDB ... choose ElastiCache when the database being cached is relational" | c (DAX for RDS): DAX is DynamoDB-only per K02/S05; d (ElastiCache replacing DAX for DynamoDB): S05 gives DAX the edge for DynamoDB's transparent fit; e (Redshift as a cache): never described as a caching service anywhere in the lesson |

## Distractor-type table

Each question is tagged with the single dominant distractor pattern its wrong choices
share; no type exceeds 3 of the 21 questions (14.3%), at or under the 15% cap.

| Type | Questions | Count |
| --- | --- | --- |
| Wrong location/scope (right fix, wrong Region/AZ) | k01-mc, k01-mr | 2 |
| Wrong caching strategy or direction (TTL/write-through/DAX mix-up) | k02-mc | 1 |
| Read-side fix offered for a write-side bottleneck | k03-mc | 1 |
| Wrong storage tier (gp3 vs io2, or compute mistaken for storage) | k04-mc, k04-mr | 2 |
| Missing connection pooling (resize/storage/replica instead of RDS Proxy) | k05-mc | 1 |
| Wrong migration-tool order or scope (SCT/DMS misapplied) | k06-mc, s03-mr | 2 |
| Wrong replication mechanism (RDS replica vs Aurora Replica vs Multi-AZ cluster) | k07-mc | 1 |
| False mechanics of a named feature (Aurora Replica / GSI / LSI facts) | k07-mr, s02-mr | 2 |
| Retired or wrong-category service | k08-mc, s04-mr | 2 |
| Orthogonal or insufficient fix ignoring the stated bottleneck | s01-mc, s02-mc | 2 |
| Breaks the intended mechanism (promote/write to a read-only replica) | s01-mr | 1 |
| Wrong engine for an extension/compatibility requirement | s03-mc | 1 |
| Unpredictable-vs-forecastable capacity mode mismatch | s04-mc | 1 |
| Wrong cache-service pairing (DAX/ElastiCache cross-wired or code-change tradeoff) | s05-mc, s05-mr | 2 |

Total: 2+1+1+2+1+2+1+2+2+2+1+1+1+2 = 21, matching the 21 questions (each counted once
under its dominant type).

## Retired/closed services in the question set

Only `q-saa-3-3-k08-mc` names a retired/closed service (**Amazon Timestream for
LiveAnalytics**, closed to new customers 6/20/25), used strictly as a labeled-wrong
distractor per `RULES.md`, never as the key. No other retired name from `RULES.md`'s list
(Copilot CLI, Snow Family, FSx File Gateway, CodeCommit, Cloud9, CodeStar, QLDB) appears
anywhere in the question set; confirmed with the same `RETIRED` regex the batch checker
uses (see self-check script output -- zero hits).
