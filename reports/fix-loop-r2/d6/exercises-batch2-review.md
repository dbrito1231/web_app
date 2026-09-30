# D6 Part B batch 2: exercises review (issue ids AWS-DE2-###)

## Technical review (batch 2)

Method: read the 16 files at HEAD, the writer report, lessons 3.1 to 3.5 (plus 4.1 for de-snow), and RULES. AWS facts re-checked with the AWS docs MCP: Data Transfer Terminal (what-is-dtt: "available only to AWS Enterprise Support customers at this time"; facilities have 100 Gbps LR4 fiber; location shown at reservation), Snowball Edge availability page ("AWS will no longer offer any AWS Snow Family devices for new customers to order"; it also names DataSync with a Direct Connect hosted connection and AWS Partner solutions as alternatives), Aurora Serverless v2 scale to zero ACU (auto-pause), Glue DataBrew (current; no closure notice). Arithmetic re-done: Lambda GB-s 6.60 / 6.40 / 5.87 / 9.69 / 33.0 (1,769 MB cheapest and meets 4 s); st1 12 TiB = 480 MiB/s; 350 GB in 6 h = 0.13 Gbps; /24 = 251 usable, 251 - 230 = 21 < 60; 8 TB in 48 h = 0.37 Gbps; 18,000 rec/s x 400 B = 6.87 MiB/s, shards 18 by records, 21 max at +20 percent (21.6); 600 TB in 30 days = 1.85 Gbps, 111 days at 500 Mbps; 3,500 x 1 KiB = 3.42 MiB/s, 4 shards, 3 readers = 10.3 against 8 MiB/s shared. All correct. No closed service is used as an answer; Snow Family is labelled closed in de-snow scenario, constraint 1 and r6.

### Verdicts

| # | Exercise | Verdict |
| --- | --- | --- |
| 1 | de-saa-3.1-s01 | approve |
| 2 | de-saa-3.1-s02 | approve |
| 3 | de-saa-3.2-s04 | approve (naming Lambda is acceptable) |
| 4 | de-saa-3.3-s01 | changes required (major, 003) |
| 5 | de-saa-3.3-s03 | approve |
| 6 | de-cdn | approve |
| 7 | de-saa-3.4-s01 | approve (one minor, 004) |
| 8 | de-saa-3.4-s02 | approve |
| 9 | de-saa-3.4-s03 | approve (one minor, 007) |
| 10 | de-data-lake | approve |
| 11 | de-emr-glue | approve |
| 12 | de-saa-3.5-s03 | approve |
| 13 | de-saa-3.5-s06 | changes required (minor, 005) |
| 14 | de-snow | changes required (major, 001; minor, 002) |
| 15 | de-streaming | approve |
| 16 | de-visualization | changes required (minor, 006) |

### Findings

**AWS-DE2-001 (major) de-snow, constraint 2.** A second defensible design exists. AWS's own Snow closure page recommends DataSync over a Direct Connect hosted connection bought from a delivery partner for the length of the project. "Faster internet circuit" does not exclude it, and the scenario gives no lead time for it. Replace constraint 2 ("Finance will not fund a faster internet circuit") with: "Finance will not fund a faster internet circuit or any other new network circuit, and none can be installed within the 30 days". The physical-transfer design then stands alone for the bulk load and DataSync for the monthly scans.

**AWS-DE2-002 (minor) de-snow, scenario last sentence.** The design depends on a physical upload facility being reachable, but nothing says one is. Replace "and its staff can transport storage devices up to a five-hour drive." with "and its staff can transport storage devices up to a five-hour drive, which is enough to reach an AWS facility that accepts physical uploads." Other de-snow checks, all fine:
- Data Transfer Terminal exists and is current. The user guide says it is available only to Enterprise Support customers at this time, so the scenario's "holds an AWS Enterprise Support plan" is correct and necessary. Keep it.
- It is taught: lessons 3.1 K01, 3.5 K03 and S03, and 4.1 S07 all name it with the "no viable network / far too much for the link" discriminator.
- The closure wording is accurate ("closed to new customers ... no device can be ordered"). The doc says "any AWS Snow Family devices", which covers the three named devices.
- The Enterprise Support requirement itself is not taught. Stating it in the scenario is the right handling. The optional lesson sentence in the writer's report is doc-verified and can go in a later lesson pass.

**AWS-DE2-003 (major) de-saa-3.3-s01, constraint 2.** Aurora PostgreSQL is a second defensible design. "Will not certify a change of database engine" does not clearly exclude Aurora, which is PostgreSQL-compatible and which lesson 3.3 recommends by default. Aurora replicas for reports plus Aurora Global Database for Sydney meets every figure. Replace constraint 2 with: "The vendor certifies only RDS for PostgreSQL; a move to Amazon Aurora or any other database product is not certified this year".

**AWS-DE2-004 (minor) de-saa-3.4-s01.** Answer to the Lead Dev question: a virtual private gateway and a transit gateway attachment are two defensible ways to attach one VPC. The scenario does not decide between them, and nothing graded depends on it. r6 and r7 only grade subnets, routes, the private path and the VPN backup. Accept-either is acceptable if Lead Dev records it. To pin it cheaply, append to constraint 5 ("The first release uses one VPC ..."): ", and no other VPC, Region or data centre will connect to it for at least two years; Finance pays for no capability beyond that".

**AWS-DE2-005 (minor) de-saa-3.5-s06, constraint 1 and r6.** Two points.
- (a) Kinesis on-demand capacity mode is a second defensible design: it has no computed minimum and its cost cannot be checked against "20 percent headroom". Replace constraint 1 with: "Finance wants a fixed, pre-agreed write capacity that is at most 20 percent above the computed minimum, not capacity that scales by itself".
- (b) r6 ("no single partition of the stream ... documented write limit") names a partition concept, and so half-names the mechanism. The scenario's 60 percent figure already creates the hot-spot problem. Replace r6 with: "Write capacity covers the 18,000 records per second peak (arithmetic shown from both the record rate and the byte rate), stays within 20 percent above the computed minimum, and the record shows that the 60 percent concentration in one metro area cannot push any single unit of that capacity past its documented write limit".
- Figures are right: 18 needed by records, 21 at most, and 18 alone would leave no margin for uneven key hashing. That makes the "at most 21" window a genuine design tension, not a giveaway.

**AWS-DE2-006 (minor) de-visualization, scenario last sentence and r6.** Both hand the learner the mechanism. "The query service bills for the data each query scans" explains the cost model, and r6 "scanned no more than once per nightly load" states the import-once design. The figures already decide it without either: 250 concurrent viewers, 3 s, and "same cost on Tuesday as Monday". Replace the scenario clause "and notes that the query service bills for the data each query scans" with "and each full read of the sales files has a cost". Replace r6 with: "The first dashboard answers 250 concurrent viewers within 3 seconds per interaction, and its cost on a busy Monday is the same as on a quiet Tuesday". r7 and the rest stand. Lesson 3.5 teaches Athena's per-scan billing and SPICE, so the learner can still derive the design.

**AWS-DE2-007 (minor) de-saa-3.4-s03, constraint 3.** AWS Outposts (hardware in the studio) also meets the 8 ms figure. It is not taught in lesson 3.4, so this is low risk. Replace constraint 3 with: "Editing workstations and the compute and storage they use must be in the same metropolitan area, and no AWS-owned hardware may be installed at the studio".

### Checked and no finding

- **de-saa-3.2-s04 (Lambda named):** acceptable. The exercise sizes Lambda's memory, so Lambda is context, not the answer. The decision (1,769 MB) is found by arithmetic on the figures, and the writer states the billing rule in the scenario. r6 and r7 grade outcomes.
- **de-saa-3.3-s03:** lesson 3.3 S04 and the K-section say "choose Aurora Serverless when traffic is intermittent or hard to forecast" and "including down to zero". This matches the docs (Aurora Serverless v2 scales to zero ACU with auto-pause). RDS has no serverless option, so provisioned RDS is excluded by the "nobody sizes or resizes" constraint. Aurora PostgreSQL supports PostGIS and pg_trgm. r6 asks for the reason the other open-source engine does not fit, which is teachable from the lesson's extension sentence.
- **de-cdn:** one best design (CloudFront with separate /api/* behaviour and Origin Shield, plus Global Accelerator for UDP). Route 53 failover would change addresses, which constraint 6 excludes. A 30 s health-check setting meets the 60 s figure. Neither r6 nor r7 names a service.
- **de-saa-3.1-s01, 3.1-s02, 3.4-s02, 3.5-s03, de-data-lake, de-emr-glue, de-streaming:** determinate. Hybrid access mode is taught in lesson 3.5 S01. Rubrics grade outcomes against the scenario's figures.
- **constraint_reason:** both kept texts still fit all 16. No closed or retired service is used as an answer. Side note outside batch 2: lesson 3.5 still lists "Glue for Ray" as an option, which AWS closed to new customers on 2026-04-30 (Glue docs "end of support" page). Log for the lesson pass.

Batch 2: not yet

Overall: concerns
