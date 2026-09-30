# D6 Part B batch 3b: exercises implementation (8 files)

Files: de-db-migration, de-saa-4.3-s02, de-saa-4.3-s04, de-saa-4.4-s03, de-saa-4.4-s05, de-saa-4.4-s07, de-tgw, de-throttling. All 8 still had a template opening at edit time (guard passed for all; none skipped). Kept: id, title, practiceMode, objectiveIds, constraint_reason, r1-r5, the 4 generic constraints. Old scenario for all 8 was the template ("You must design a solution addressing: <title>..." or "Design a solution that demonstrates skill: <objective text>"). requiredArtifact changed only for de-throttling (added "+ guidance for API callers on rejected requests"). No dollar prices anywhere. Budgets are caps or relative targets.

AWS facts checked with the AWS docs MCP: standard VPN tunnel up to 1.25 Gbps; Large Bandwidth Tunnel up to 5 Gbps, Transit Gateway or Cloud WAN only; ECMP across VPN connections via Transit Gateway; API Gateway 429 on exceeding rate/burst limits and usage plans enforce per-API-key throttles. All other facts are the lesson sentences quoted below.

## de-db-migration (SAA-4.3-S05, SAA-3.3-K06)
- New scenario: Lindqvist Parts Distribution, 1.8 TB Oracle order DB with ~350 stored procedures plus a 40 GB MySQL 8 web-store DB, lease ends in 7 months, order system to a PostgreSQL-compatible engine, web store stays on MySQL, 3-day copy, never offline for the copy.
- Added constraints: 30-minute cutover downtime; no hand-rewrite of the 350 procedures beyond what tooling cannot translate; parallel run capped at 2 weeks; one data-movement service for both DBs.
- r6: order DB arrives with schema and all 350 procedures working and offline no more than 30 min despite the 3-day copy. r7: MySQL DB prepared with no more work than needed, and the record justifies why the two are prepared differently.
- Decisive figures and one best design: Oracle to PostgreSQL-compatible is different engines (3.3-K06), so schema/procedure conversion comes first and only then data movement; 3-day copy vs 30-minute window forces ongoing replication of changes (4.3-S05 cutover window, replication lag); MySQL to MySQL needs no conversion. A dump-and-load is excluded by the 30 minutes; hand rewriting is excluded by constraint 2.
- Named or needed and taught: Oracle/MySQL/PostgreSQL (lesson 3.3 K06 "Oracle to Aurora PostgreSQL, SQL Server to MySQL"; 4.3 K07 "homogeneous migration (same engine ...)"). Needed: SCT + DMS, lesson 3.3 K06 "AWS Schema Conversion Tool (AWS SCT) first converts the source schema and application SQL ... and only then does AWS DMS migrate and, optionally, continuously replicate the data"; homogeneous "AWS DMS alone can migrate the data with minimal downtime"; lesson 4.3 S05 "cutover window, rollback design" and "at least one endpoint ... must be on an AWS service" (the target is in AWS).
- constraint_reason ("Service unavailable or not disposable in a personal same-day lab"): still makes sense (an on-premises source is not available in a personal account). No edit.
- Note: constraint 4 ("one data-movement service") mildly steers the web-store database to the same service; native tools would also work, so this constraint removes that ambiguity deliberately.

## de-saa-4.3-s02 (SAA-4.3-S02)
- New scenario: Tamarind Bay Bookkeeping, new build with no data migrated; 20-200 nested attributes filtered inside the stored document, join/subquery-heavy month-end reports, vendor add-on loaded in the database and supported on one engine only; developers know only MySQL; go-live in 6 months; fixed-size managed instance wanted.
- Added constraints: vendor add-on supported on one engine only and must run in-database; fixed-size instance not usage-metered; 6 months, no training budget beyond vendor docs.
- r6: engine supports all three stated behaviours and record explains why MySQL familiarity does not override. r7: record states ramp-up risk and a mitigation fitting 6 months.
- One best design: the add-on's single supported engine (PostgreSQL, taught as "custom extensions") plus nested-document filtering and complex queries decide it; no migration source removes the compatibility pull toward MySQL; the fixed-size instance sentence keeps the question to engine choice (RDS with instance classes), not Aurora serverless.
- Taught: lesson 4.3 S02 "Choose PostgreSQL when you need advanced JSON handling, complex queries, or custom extensions"; "prioritize engine compatibility with current schema and workload constraints before optimizing secondary preferences"; K07 "MySQL and PostgreSQL on RDS for managed operations with fixed instance classes". The scenario never names PostgreSQL.
- constraint_reason: generic ("Mapped as design_exercise to complete skill coverage ...") still true. No edit.

## de-saa-4.3-s04 (SAA-4.3-S04)
- New scenario: Brightwater Hydrology Board, one oversized relational DB with three workloads: 6,000 gauges at 15 s (400 writes/s, never edited, time-window averages); 3 billion rows x 60 columns scanned 4 columns at a time by five analysts; 900,000-row permit registry with multi-table transactional row updates.
- Added constraints: no self-managed database servers; total run-rate not above today's single database; no service closed to new customers.
- r6: each workload on a type chosen from its own pattern, none left on an unfit type because it exists. r7: names the largest saving and how to confirm it.
- One best design: append-only time-window reads to a time-series type; wide-table few-column scans to columnar; row transactions stay relational. The closed-service constraint removes the retired time-series offering as an answer and keeps the current alternative.
- Taught: lesson 4.3 S04 "For time-series data, design for append-heavy writes and range-based reads over time ... Timestream for LiveAnalytics is closed to new customers as of 2025-06-20 ... Amazon Timestream for InfluxDB"; "columnar ... Amazon Redshift"; "transactional row-oriented patterns with frequent point updates, relational OLTP services remain the fit". Scenario names no service.
- Residual (flag for Teacher): DynamoDB for the gauge data is a weaker alternative because the reads are time-window aggregates across groups of gauges, not key lookups; the wording was chosen to exclude it.
- constraint_reason: unchanged, still true.

## de-saa-4.4-s03 (SAA-4.4-S03)
- New scenario: Halloran Transcription Services; workers in 3 AZs behind one NAT gateway in the first zone; 60 TB/month through it = 55 TB S3 (same Region) + 3 TB DynamoDB + 2 TB partner API on the public internet; 9 TB/month copied to a second Region with no residency or latency need; two thirds of NAT traffic comes from the other two zones.
- Added constraints: cut bytes processed by NAT by at least 90 percent; an AZ outage must not cut partner access for the other two zones; reporting team accepts the primary Region.
- r6: NAT-processed bytes fall by at least 90 percent of 60 TB and the remainder is identified. r7: no cross-AZ hop to a NAT, AZ outage leaves the other two with access, 9 TB/month stops crossing Regions.
- Arithmetic: 55 + 3 = 58 of 60 TB = 96.7 percent removable, so a 90 percent target is met only by removing both S3 and DynamoDB traffic; the 2 TB partner API stays (public-only). One NAT per AZ is forced by constraint 2; single NAT plus endpoints would fail r7.
- Taught: lesson 4.4 S03 "use a gateway endpoint when the target is Amazon S3 or DynamoDB, because there is no additional charge"; "Data transfers between AWS Regions typically incur charges ... avoids a multi-Region path unless the workload specifically requires it"; S01 "NAT gateway in each Availability Zone ... keeps traffic in-AZ and keeps one AZ's failure from taking down egress". Global Accelerator deliberately not used (lesson: not primarily a cost tool).
- constraint_reason: unchanged, still true.

## de-saa-4.4-s05 (SAA-4.4-S05)
- New scenario: Ravenscar Map Publishing; transfer charges up 70 percent with flat users; only service-level totals exist; a week of VPC flow logs splits the extra bytes 58 percent repeat downloads of ~2,500 unchanging files from the servers, 27 percent cross-AZ via a single NAT in the third zone, 15 percent a nightly 3 TB unjustified cross-Region copy. Static files change at most weekly.
- Added constraints: 24-hour staleness accepted; servers stay in the current Region and 3 AZs; two engineers, AWS-native only.
- r6: each of the three drivers matched to a fix removing its charge, none proposed for traffic not shown. r7: names the measurement to repeat and the cost line that should show the rise reversing.
- Arithmetic: 58 + 27 + 15 = 100. One best design: cacheable static content to edge caching (freshness accepted); NAT per AZ; stop the copy (no reader, no rule). Keeping servers in place excludes moving workloads.
- Taught: lesson 4.4 S05 "Use Amazon CloudWatch and VPC flow logs to capture details about your data transfer ... AWS Cost Explorer"; "confirm NAT gateways sit in the same AZ as the resources that use them ... confirm cross-Region calls are actually required, and confirm cacheable content is in front of a CDN"; S04 CloudFront "static or infrequently changing assets". Scenario names VPC flow logs only (taught); no solution service named.
- constraint_reason: unchanged, still true.

## de-saa-4.4-s07 (SAA-4.4-S07)
- New scenario: Penhallow Survey Group; branch opens in 3 weeks; sustained 3 Gbps; encrypted; branch router supports tunnels of at most 1.25 Gbps; carrier needs at least 6 weeks for any dedicated circuit; a Transit Gateway already exists.
- Added constraints: nothing needing a new physical circuit; at least 2 Gbps after any one tunnel fails; no paying for capacity beyond what the figures require.
- r6: at least 3 Gbps at the documented ceiling, at least 2 Gbps with one tunnel down, at most one tunnel beyond the minimum. r7: record explains why a single tunnel, a dedicated circuit and a larger tunnel type are each unsuitable.
- Arithmetic: 3 x 1.25 = 3.75 (>= 3); minus one tunnel = 2.5 (>= 2); 2 tunnels give 2.5 (< 3) so 3 is the minimum. Direct Connect excluded by 3 weeks vs 6; single tunnel fails 3 Gbps; larger tunnel excluded by the router's 1.25 Gbps limit. "Up to" is preserved by sizing at the documented ceiling and r6 reads "at the documented per-tunnel ceiling".
- Taught: lesson 4.4 S07 "standard bandwidth is up to 1.25 Gbps per tunnel ... Large Bandwidth Tunnel raises that to up to 5 Gbps ... scaled with multiple VPN connections in parallel (using equal-cost multi-path routing through Transit Gateway)"; "match it to the smallest VPN tunnel count or Direct Connect port size that clears that number". The scenario avoids "ECMP" and "Large Bandwidth Tunnel" (only r7 names "a larger tunnel type" generically).
- Residual (flag for Teacher): tunnel count vs connection count (each connection has two tunnels, K05) could be argued; r6 is written in tunnels carrying traffic to tolerate 3 connections or 2 connections with both tunnels used by ECMP (one extra tunnel allowed).
- constraint_reason: unchanged, still true.

## de-tgw (SAA-4.4-K06)
- New scenario: Mossgiel Outfitters; 14 VPCs now, 30 within 12 months; all must reach each other and head office (VPN now, Direct Connect link next year); two of them exchange about 80 TB/month with each other; two-person network team.
- Added constraints: adding a VPC must not require editing or linking every existing VPC; the 80 TB/month kept off any per-GB processing charge the other VPCs' shared path incurs; head-office VPN and future Direct Connect reach all VPCs without per-VPC connections.
- r6: onboarding a 31st VPC needs connections from that VPC only, and no existing VPC config is edited. r7: the 80 TB/month avoids the per-GB processing charge the others incur, basis shown.
- Arithmetic: full mesh of 14 = 91 links, of 30 = 435 (not stated in the exercise). One best design: hub for all VPCs plus on-premises (peering does not transit and cannot serve the VPN/Direct Connect); the heavy pair additionally directly peered to avoid the hub's per-GB data charge.
- Taught: lesson 4.4 K06 "Peering ... does not transit"; "Transit Gateway ... billed separately for each VPC attachment-hour and for the data it processes"; "Choose peering for a small, static number of VPCs that need direct low-cost connectivity. Choose Transit Gateway once you have enough VPCs, VPNs, or Direct Connect gateways that a full mesh of peering connections would become unmanageable". Teacher point: the lesson does not say explicitly that the two can coexist for the heavy pair; if considered too far, r7 can be dropped. Possible lesson addition below.
- constraint_reason: unchanged, still true.

## de-throttling (SAA-4.4-S06, SAA-2.2-K10)
- New scenario: Saltmarsh Weather API; backend serves at most 1,500 req/s (15 per vCPU); 10 paid customers at 100 req/s and 100 free-tier developers at 4 req/s (1,000 + 400 = 1,400); own web front end calls without a key and once caused a 40-minute retry storm; recovery Region has 64 vCPUs of allowance from the initial setting and its copy of the API has no per-customer limits; partner apps retry rejected calls immediately.
- Added constraints: per-class rates; backend never above 1,500 req/s from any callers, own front end included; no limit raised after a disaster is declared.
- r6: every caller class held to its rate and total to the backend cannot exceed 1,500 even from the keyless front end. r7: before failover, the recovery Region's compute allowance and API rate settings admit and serve 1,500 req/s. requiredArtifact adds guidance for API callers on rejected requests (covers retry behaviour under r1 "requirements mapped").
- Arithmetic: 1,500 / 15 = 100 vCPUs needed vs 64 allowed, so an increase of at least 36 is needed in advance. The keyless front end is not covered by per-key limits, so a stage-wide limit is required; per-tier limits cover contracts.
- Taught: lesson 4.4 S06 "usage plans ... different API keys or customer tiers different limits"; "A stage-level or method-level throttle protects your backend and its cost from any client, including your own traffic spikes"; `429 Too Many Requests`. Lesson 2.2 K10 "an EC2 vCPU limit in the recovery Region ... Request the needed quota increases in the recovery Region ahead of time"; "workloads should retry with backoff". No service named in the scenario beyond EC2.
- constraint_reason: unchanged, still true.
- Residual: the two objectives are a slightly forced pair (one throttling, one quota); both are graded by separate rubric items.

## Lesson additions requested
None required. Optional: lesson 4.4 K06, one sentence (doc-verify before adding): "A VPC peering connection can be added alongside Transit Gateway to carry a heavy pair of VPCs directly and avoid the hub's per-GB data processing charge for that pair." Only needed if the Teacher keeps de-tgw r7.

## Script outputs
- `backend\.venv\Scripts\python.exe scripts\content_lint.py`: questions 429, aws 310, tf 119, labs 21 + 21, lessons 23, PASS.
- Teach-before-test regex (case-insensitive, backticks stripped) over lessons 2-2, 3-3, 4-3, 4-4: every term listed above matched True.
- Opening / organisation scan of all 60 exercises at finish: 8 of mine have distinct 6-word openings; organisations (Lindqvist, Tamarind Bay, Brightwater, Halloran, Ravenscar, Penhallow, Mossgiel, Saltmarsh) are unique among the exercises that had been rewritten. The only duplicates were template openings still present in files other writers had not yet reached (12 "You must design a solution addressing:" and the 4.1/4.2/3.x "Design a solution that demonstrates skill:" files). Re-check after the other writers finish.
