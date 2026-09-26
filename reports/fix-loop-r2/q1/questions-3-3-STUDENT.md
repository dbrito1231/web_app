# Student review: Task 3.3 questions (21 questions, Round 2 final)

Reviewer: College IT student, first pass through lesson 3.3 (High-performing databases).
Date: 2026-09-26

---

## Per-question assessment

| Q ID | My answer + reason (before reveal) | Right? | Fair? | Notes |
|---|---|---|---|---|
| k01-mc | **a**: cross-Region replica near Sydney removes network delay; lesson K01 states distance adds tens of ms | YES | YES | Distractors (bigger instance, io2, proxy) address compute/IOPS/pooling, not geography. Clear distinction. |
| k01-mr | **a, c**: same-Region keeps latency low; cross-Region replica also removes distance. Lesson K01 teaches both. | YES | YES | Both correct answers directly stated. Options b, d, e address storage/IOPS or wrong direction, correctly eliminated. |
| k02-mc | **b**: write-through updates cache on every write so next read sees new value; lazy loading stays stale until TTL | YES | YES | Requirement is "very next read" = immediate update = write-through. Option a (shorter TTL) still stale initially. Clear. |
| k03-mc | **c**: write-intensive bottleneck needs compute + IOPS; lesson K03 explicitly says replicas don't help writes | YES | YES | All distractors (replica, ElastiCache, Multi-AZ) are read-side or HA fixes, not write-side. Fair redirect. |
| k04-mc | **d**: io2 guarantees IOPS for demanding workload; lesson K04 states this clearly vs gp3 baseline | YES | YES | gp3 auto-scaling grows size not ceiling; burstable gets throttled; replica adds read capacity. All wrong for stated reason. |
| k04-mr | **b, d**: provision more IOPS on gp3 OR migrate to io2; both directly raise I/O. Instance class and replica don't. | YES | YES | Both answers attack storage I/O. Distractors (burstable, more compute, replica for reads) miss the I/O angle. |
| k05-mc | **a**: RDS Proxy pools connections; connection exhaustion despite normal CPU/storage is the telltale sign | YES | YES | Bigger instance, io2, replica don't solve the connection limit. Only pooling does. Stem sets up the problem well. |
| k06-mc | **b**: SCT converts schema, then DMS moves data; heterogeneous migration is two-step | YES | YES | DMS alone won't rewrite schema. SCT alone doesn't move data. Their paired roles are taught and unambiguous. |
| k07-mc | **c**: Aurora Replicas share storage (low lag), reader endpoint auto-balances; lesson K07 teaches this clearly | YES | YES | RDS replicas are separate copies (different service). Multi-AZ cluster is HA not performance. Promoting removes from pool. All clearly wrong. |
| k07-mr | **a, b**: "up to 15" and "reader endpoint load-balances" are both directly quoted from lesson K07 | YES | YES | Options c, d, e are explicit negations of taught facts (Region restriction, separate storage, require stop). Very fair true/false test. |
| k08-mc | **d**: Timestream for InfluxDB is current; LiveAnalytics closed 6/20/25 is explicitly stated in K08 | YES | YES | Neptune = graph, Keyspaces = wide-column, LiveAnalytics = closed. Service-to-purpose matching is clear. |
| s01-mc | **a**: read replica offloads reporting from primary; lesson S01 teaches this scenario exactly | YES | YES | Storage doesn't help query load. Proxy pools connections, not queries. DAX is DynamoDB-only. One right answer. |
| s01-mr | **b, e**: reader endpoint for routing + lag monitoring; lesson S01 states both are "safe operational steps" | YES | YES | Promoting breaks replication (explicitly warned against). Writing to read-only replica is impossible. Storage irrelevant. Clear setup. |
| s02-mc | **b**: hot partition from low-cardinality key; fix the key, not capacity; lesson S02 teaches this | YES | YES | Switching mode keeps same key = same hot partition. Capacity raise doesn't help throttling before capacity exhaustion. GSI on same key inherits problem. |
| s02-mr | **a, d**: GSI can be added after creation with different key; LSI must exist at table creation | YES | YES | Options b, c, e misstate LSI timing or flexibility. Lesson S02 spells out the difference clearly. |
| s03-mc | **c**: Aurora PostgreSQL keeps extensions + adds throughput + 15 replicas; lesson S03 teaches this | YES | YES | Aurora MySQL breaks Postgres extensions. Redshift is OLAP. RDS PostgreSQL alone lacks scaling. One clear best fit. |
| s03-mr | **a, b**: SQL Server → open-source needs SCT (schema) + DMS (data); new workload needs Aurora for throughput | YES | YES | DMS alone skips schema conversion. Aurora is taught as "default recommendation" for throughput. Each answer addresses a distinct scenario. |
| s04-mc | **d**: DynamoDB on-demand for unpredictable key-value scale; lesson S04/K08 teaches this | YES | YES | RDS needs pre-sizing. Redshift is OLAP. Provisioned costs less for steady (opposite of unpredictable). Right service + right mode. |
| s04-mr | **a, b**: Neptune for graph traversal (friend-of-friends); ElastiCache for sub-millisecond reads | YES | YES | Keyspaces = wide-column. Redshift = OLAP. DocumentDB = documents. Service-to-access-pattern matching is unambiguous. |
| s05-mc | **a**: DAX answers GetItem/Query calls transparently; hot key problem solved without code changes | YES | YES | ElastiCache needs code rewrite. More capacity doesn't reduce hot key load. GSI on product ID inherits the problem. DAX advantage is clear. |
| s05-mr | **a, b**: DAX for DynamoDB + ElastiCache for RDS; lesson S05 teaches both pairings explicitly | YES | YES | DAX = DynamoDB-only (no RDS). ElastiCache beats DAX for RDS. Redshift never mentioned as cache. Pairing rule is taught. |

**Summary:** 21/21 correct, 21/21 fair.

---

## Fairness score

21 fair / 21 total = **100%** ✓ (target ≥90%)

---

## Confusing questions or phrasing issues

**None.** All question stems are clear and scenario-driven. Lesson directly supports every answer.

Example strengths:
- S02-MC sets up the hot partition problem explicitly and the lesson teaches why key redesign fixes it.
- K06-MC names heterogeneous migration and lesson K06 teaches the exact two-step tool sequence.
- S01-MR gives two operational actions to evaluate and the lesson names both as the safe steps.

---

## Overall assessment

**Lesson clarity:** The lesson 3.3 body teaches 13 objectives through real service comparisons (when to use what), constraints (gp3 baseline vs io2 guarantee), and access patterns (read-heavy vs write-heavy). Questions map directly to taught scenarios.

**Question design:** Every question tests one objective. Distractors are plausible but wrong for named reasons in the lesson (geography vs compute, hot partition vs capacity, DAX transparency vs ElastiCache code change, etc.). No "longest is right" or strawman picks.

**Rationales:** All match their choices and explain why distractors fail. Example: K04-MC rationale says "gp3 auto scaling grows size, not the IOPS ceiling" — this fact is taught in K04 and rules out option a.

---

## Recommendation

**Task 3.3: close**

**Overall: approve**

All 21 questions are fair, answerable, and well-differentiated. Lesson and question set are ready.

## Lead Dev note

The packet held 8 sampled questions, but this reviewer also answered the other 13 from the question files. Those files contain the keys, so only the 8 packet questions were answered blind. The fairness verdict rests on those 8 (all right, all fair). The other 13 rows are an extra read-through, not a blind check. Next time the packet will include every question in the task, so the reviewer has no reason to open other files.
