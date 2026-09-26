# Lesson 3.3 AWS review -- Round 1

Reviewer: Senior AWS Solutions Architect (read-only). Commit reviewed: `8a1c7a9`.
10 claim-table rows fetched and spot-checked directly against the cited AWS doc pages
(gp3/io2 storage, RDS instance classes, Aurora scalability, Aurora Serverless v2,
DynamoDB capacity modes, partition keys, secondary indexes, DAX, ElastiCache engines
and strategies, DMS/SCT, Timestream EOL).

## Per-section verdict

- K01 (global infra): correct, no citation needed, consistent with 2.2 K01. OK.
- K02 (caching strategies): lazy loading / write-through / TTL quotes verified verbatim except one paraphrase (AWS-L33-002). OK with fix.
- K03 (access patterns): correct, conceptual, no numbers to check. OK.
- K04 (capacity planning): gp3/io2 IOPS numbers verified, but "independent of volume size" is inaccurate for gp3 (AWS-L33-001). Instance-class family list is incomplete (AWS-L33-003, minor).
- K05 (connections/proxy): RDS Proxy claim consistent with lesson 2.2 K09 (already AWS-approved there). OK.
- K06 (engines/migration): homogeneous/heterogeneous DMS+SCT quotes verified verbatim. OK.
- K07 (replication): Aurora 15-replica cap, single-digit-ms lag, reader endpoint all verified verbatim against the Aurora scalability page. Consistent with lesson 2.2 K06. OK.
- K08 (database types): ElastiCache engine list, Aurora storage 10 GB/256 TiB increment, Timestream EOL date and InfluxDB pointer all verified verbatim. Aurora Serverless "scale to zero" claim has a citation/quote mismatch (AWS-L33-004). OK with fix.
- S01 (read replica config): correct, builds on K07/S01, no new numbers. OK.
- S02 (database architecture / DynamoDB capacity): on-demand default/recommended wording, hot-partition quote, GSI/LSI comparison all verified verbatim. OK.
- S03 (engine selection): correct, conceptual, consistent with K06/K07. OK.
- S04 (database type selection): correct, conceptual, consistent with K08. OK.
- S05 (caching integration): DAX cache-hit and write-through quotes verified verbatim. OK.
- Retired/closed services: Timestream for LiveAnalytics closed-to-new-customers 6/20/25 confirmed and correctly labeled; InfluxDB alternative correctly named. QLDB correctly omitted rather than named as current. ElastiCache engine naming (Valkey, Redis OSS, Memcached) confirmed current, no stale "Redis" naming used. OK.
- Objective coverage: all 13 `SAA-3.3-*` ids from `content/objectives/saa_c03.json` have a `###` section, in id order. OK.
- Cross-lesson consistency (2.2): Multi-AZ instance vs cluster, read replicas, Aurora Replicas/Global Database, RDS Proxy failover role -- no contradictions found; 3.3 explicitly defers to 2.2 for the HA angle and stays in the performance lane. OK.
- Lint: `content_lint.py` -> PASS (429 questions, 21+21 labs, 23 lessons).

## Issues

- **AWS-L33-001** (moderate, K04, "General Purpose SSD (gp3) is the default, cost-effective choice with a baseline of 3,000 IOPS and 125 MiB/s independent of volume size"): Not accurate. Per `AmazonRDS/latest/UserGuide/CHAP_Storage.html`, the 3,000 IOPS/125 MiB/s baseline only holds up to a per-engine size threshold (e.g., 20-399 GiB for MariaDB/MySQL/PostgreSQL/Db2); above that threshold RDS stripes across four volumes and the baseline jumps to 12,000 IOPS/500 MiB/s. Fix: change "independent of volume size" to "up to a per-engine storage-size threshold, above which RDS stripes the volume and the baseline rises to 12,000 IOPS/500 MiB/s" (or simply drop the "independent of volume size" clause).
- **AWS-L33-002** (low, K02, TTL claim): The claim-table quote "Add a time to live value to each cache write to combine the benefits of lazy loading and write-through" is a paraphrase, not verbatim (rule requires a verbatim quote, <=20 words). Actual page (`AmazonElastiCache/latest/dg/Strategies.html`) says: "By adding a time to live (TTL) value to each write, you can have the advantages of each strategy." Fix: replace the claim-table quote with the exact sentence above; lesson body wording itself is fine and needs no change.
- **AWS-L33-003** (low, K04, instance-class families): `AmazonRDS/latest/UserGuide/Concepts.DBInstanceClass.Types.html` lists five use-case categories (general-purpose, memory-optimized, compute-optimized, burstable-performance, **and Optimized Reads**); the lesson names only the first four. Not wrong, just incomplete. Optional fix: add ", and Optimized Reads instance classes for workloads needing high-speed local NVMe storage" to the K04 sentence.
- **AWS-L33-004** (low, K08, Aurora Serverless "scale to zero" citation): The claim-table row cites `AmazonRDS/latest/AuroraUserGuide/aurora-serverless-v2.how-it-works.html` with the quote "When your database is idle, Aurora will automatically scale down to zero" -- that exact sentence is not on the how-it-works page; it is on `rds/latest/auroraextendedcontent/aurora-features-scalability.html` (already cited elsewhere in this lesson as `cite-saa-3-3-aurora-scalability`). The how-it-works page does support the underlying claim via its "Scaling to Zero" (auto-pause) section, so the fact is correct, only the quote-to-URL pairing is wrong. Fix: either move this quote to the `cite-saa-3-3-aurora-scalability` citation, or replace it with a verbatim quote from the how-it-works page, e.g. "Aurora serverless writers and readers can scale all the way down to zero ACUs."
- **AWS-L33-005** (informational, K06 citation scope): `cite-saa-3-3-dms-heterogeneous` points at a SQL-Server-source migration guide (`prescriptive-guidance/latest/migration-sql-server/heterogeneous-migration-tools.html`) to support a general homogeneous-vs-heterogeneous DMS/SCT claim. The quoted sentences are accurate and generic, but the source page is scoped to SQL Server migrations specifically. No fix required unless a more general DMS/SCT overview page is preferred later.
- **New retired/closed-service find for the RULES.md list:** RDS magnetic storage is deprecated (not just legacy) -- as of 2026-09-26, `CHAP_Storage.html` states new DB instances can no longer use it, and starting **July 1, 2026** you can no longer even restore a snapshot to magnetic storage. Worth adding "RDS magnetic storage: deprecated, cannot create new instances; snapshot restores to it end 7/1/26" to the RULES.md retired-services list for future lessons that might mention legacy storage.

Lesson 3.3: approve for question writing

Overall: approve
