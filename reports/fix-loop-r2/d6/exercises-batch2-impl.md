# D6 Part B batch 2: exercises impl report (domain 3, 16 files)

Writer: Sonnet. Files edited: the 16 batch-2 exercise files only. Kept: id, title, practiceMode, objectiveIds, constraint_reason, r1-r5, the 4 generic constraints, requiredArtifact (unchanged in all 16; each already asks for decision notes/record + diagram + citation, and the generic constraints cover cost). Added: new scenario, 3 stakeholder constraints each, r6 and r7 (2 points each).

Old scenario, all 16: either "Design a solution that demonstrates skill: <objective text>" (10 files) or "You must design a solution addressing: <title>. You have one personal account and cannot provision unavailable services." (de-cdn, de-data-lake, de-emr-glue, de-snow, de-streaming, de-visualization). New scenarios are in the files.

## Claim table (AWS docs MCP)

| Claim | Source | Quote / fact |
| --- | --- | --- |
| st1 caps at 500 MiB/s, baseline 40 MiB/s per TiB (12 TiB = 480), not bootable, max 16 TiB | docs.aws.amazon.com/ebs/latest/userguide/hdd-vols.html | "baseline throughput varies from 5 MiB/s to a cap of 500 MiB/s" |
| gp3 single-digit ms; io2 Block Express under 500 microseconds average; 99.999% durability | .../ebs/latest/userguide/general-purpose.html; .../provisioned-iops.html | "gp3 volumes provide single-digit millisecond latency"; io2 Block Express "average latency of under 500 microseconds" |
| Lambda 1,769 MB = one vCPU; CPU proportional to memory | .../lambda/latest/dg/configuration-memory.html | "At 1,769 MB, a function has the equivalent of one vCPU" |
| Snow Family closed | .../snowball/latest/developer-guide/snowball-edge-availability-change.html | "AWS will no longer offer any AWS Snow Family devices for new customers to order" |
| DataSync single task can use 10 Gbps; Data Transfer Terminal is a physical location where customers bring their own devices; Enterprise Support only at present | same Snow page; .../datatransferterminal/latest/userguide/what-is-dtt.html | "available only to AWS Enterprise Support customers at this time" (so the scenario states the consortium holds that plan) |
| Kinesis enhanced fan-out: dedicated 2 MB/s per shard per consumer | docs.aws.amazon.com/streams/latest/dev/enhanced-consumers.html | "up to 2 MB/sec per shard ... independently of other consumers" |
| Global Accelerator: static anycast IPs; endpoints ALB, NLB, EC2, Elastic IP | global-accelerator dg introduction-components.html, about-endpoints.html | as stated |
| Aurora PostgreSQL supports extensions such as PostGIS | AuroraPostgreSQL.Extensions.html | extension list |

Other facts (VPN tunnel 1.25 Gbps, five reserved subnet addresses, peering not transitive, Local Zone/Wavelength, Lake Formation hybrid mode, SPICE vs direct query, Firehose buffering, shard limits) come from the batch's own lessons, verified in earlier tasks. The Lambda GB-seconds billing rule is stated in the scenario itself.

## Arithmetic

- 3.2-s04: GB-s = (MB/1024) x s: 512 -> 0.5 x 13.2 = 6.60; 1,024 -> 6.40; 1,769 -> 1.7275 x 3.4 = 5.87; 3,008 -> 2.9375 x 3.3 = 9.69; 10,240 -> 10 x 3.3 = 33.0. Meeting under 4 s: 1,769, 3,008, 10,240; cheapest = 1,769 MB.
- 3.1-s01: st1 at 12 TiB = 480 MiB/s baseline, at least 400; sc1 caps at 250 (baseline 144 at 12 TiB) fails; gp3 could reach 400 but costs more; gp3 is single-digit ms so fails "under 1 ms".
- 3.4-s01: 350 GB in 6 h = 2.8e12 bits / 21,600 s = 0.13 Gbps (below the 1.25 Gbps tunnel).
- 3.4-s02: /24 = 256 - 5 = 251 usable; 251 - 230 = 21, below the 60 needed.
- 3.5-s03: 8 TB in 48 h = 6.4e13 bits / 172,800 s = 0.37 Gbps (below 1 Gbps).
- 3.5-s06: 45,000 / 2.5 s = 18,000 rec/s; 18,000 x 400 B = 7.2 MB/s = 6.87 MiB/s; the 1,000 records/s limit gives 18 shards minimum, the byte limit only 7; 20 percent headroom = at most 21 shards (21.6).
- de-snow: 600 TB = 4.8e15 bits; at 500 Mbps = 9.6e6 s = 111 days; to finish in 30 days (2.592e6 s) needs 1.85 Gbps.
- de-streaming: 3,500 x 1 KiB = 3.42 MiB/s, 4 shards; three full readers = 10.3 MiB/s against 8 MiB/s of shared reads.

## Per exercise

Format: decisive figures -> why one best design; services needed with the lesson sentence. r6/r7 are in the files.

1. **de-saa-3.1-s01 (Harlow Bay Commodities).** 45,000 IOPS plus average under 1 ms plus highest published durability decide io2 Block Express over gp3 (single-digit ms) and io1 (lesson: prefer io2 Block Express); 12 TiB sequential 400 MiB/s read nightly decides st1 (sc1 caps at 250; gp3 loses on cost). Lesson 3.1 K03: "io2 Block Express ... sub-millisecond average latency, and 99.999% durability"; "st1 ... baseline throughput of 40 MiB/s per TiB ... per-volume cap of 500 MiB/s".
2. **de-saa-3.1-s02 (Kellerman Render House).** Ordinary folder paths that cannot change, 3 AZs, 300 TB (far past one EBS volume), no resize projects, pay only for stored data decide EFS (S3 needs API change, EBS is single-AZ, FSx needs capacity increases). Lesson 3.1 S02: "Amazon EFS grows and shrinks automatically ... with Elastic throughput mode, available bandwidth scales automatically with demand".
3. **de-saa-3.2-s04 (Ashgrove Survey Maps).** Measured durations, the 4 s target and the GB-seconds rule decide 1,769 MB uniquely (only measured settings allowed). Lesson 3.2 K05/S04: "at 1,769 MB a function gets the equivalent of one full vCPU"; "raising the memory setting on a CPU-bound function can shorten its billed duration enough to lower the total cost per invocation". Names Lambda in the scenario because the exercise sizes it (the answer is the setting, not the service).
4. **de-saa-3.3-s01 (Pelham Ridge Insurance).** 92 percent reads; ad hoc non-repeating reports (caching does not help, stated); Sydney 280 ms against under 100 ms; one writable copy; engine fixed -> same-Region replica for reports plus cross-Region replica for Sydney. Lesson 3.3 S01: "add same-Region read replicas to offload reporting ... add cross-Region read replicas to serve geographically distant readers ... monitor replica lag".
5. **de-saa-3.3-s03 (Teasel Hollow Conservation Trust).** Two extension-based features decide the PostgreSQL family; about 20 idle hours, fifty-fold unpredictable bursts and no instance sizing decide Aurora Serverless over provisioned. Lesson 3.3 S03/S04: "PostgreSQL adds richer data types, extensions"; "choose Aurora Serverless when traffic is intermittent or hard to forecast".
6. **de-cdn (Nightjar Studios).** Cacheable HTTP patches versus per-player API on /api/ of one hostname (separate cache behaviours) versus UDP with fixed allow-listed IPs and 60 s Region failover (Global Accelerator); origin serving each patch only a few times decides Origin Shield. Lessons 3.4 K01 ("cache behavior ... /api/*"; "Origin Shield ... consolidates those requests"), 4.4 S04 (CloudFront cost and origin fees; Global Accelerator for fixed-IP non-HTTP), 2.1 K07.
7. **de-saa-3.4-s01 (Copperleaf Credit Union).** Tier and AZ rules fix the multi-tier VPC; no public-internet path for member data in normal operation decides Direct Connect over VPN; the batch during an outage needs 0.13 Gbps, met by a VPN backup; one circuit funded. Lesson 3.4 K04/S01: "a common resilience pattern also keeps a Site-to-Site VPN as an automatic backup path"; multi-tier topology sentence. Attachment (virtual private gateway or transit gateway) is not graded; either is accepted for one VPC.
8. **de-saa-3.4-s02 (Ferrous Lane Logistics).** Six VPCs growing to 20, the observed non-transitive peering failure and "change only the new VPC and one shared place" decide Transit Gateway; a /24 with 251 usable against 230+60 decides a secondary CIDR. Lesson 3.4 S02.
9. **de-saa-3.4-s03 (Tenmouth Post-Production).** 8 ms against 40 ms to the Region decides a Local Zone; 12 ms inside the carrier's 5G network decides Wavelength; the database with a 50 ms tolerance stays in a Region, private subnets, two AZs. Lesson 3.4 S03.
10. **de-data-lake (Saltmarsh Retail Group).** 9 teams x 35 tables, one-action revoke, no per-team bucket policies -> Lake Formation grants; new columns -> Glue crawler and Data Catalog; unchangeable legacy pipelines and gradual migration -> hybrid access mode; overwritten sources -> raw/curated layering. Lesson 3.5 S01 (all four sentences present).
11. **de-emr-glue (Brackenridge Fisheries Co-op).** Native library on every worker, self-picked instance types, 10 h nightly -> EMR cluster mode; non-coding bookkeepers -> Glue DataBrew; occasional SQL paid only when run -> Athena. Lesson 3.5 K04 ("DataBrew ... without writing code") and S05 ("EMR ... custom cluster software, or fine-grained control over instance types"; Athena).
12. **de-saa-3.5-s03 (Fairlight Packaging).** Weekly 8 TB scheduled bulk with permissions and verification -> DataSync; shared folder with local cache and objects in S3 -> S3 File Gateway; 2-minute landing with no logic or replay -> Firehose. Lessons 3.5 S03, 3.1 K01. No appliance flow (constraint).
13. **de-saa-3.5-s06 (Gorse Valley Bike Share).** 18,000 rec/s of 400 B -> the record limit sets 18 shards; no Kafka skills and SDK producers -> Kinesis Data Streams (MSK excluded by stated skills); a device-spread key avoids the 60 percent metro hot shard; Firehose buffering for large files within 5 minutes; date/city prefix scheme. Lesson 3.5 K06/S06.
14. **de-snow (Alderwick Museums Consortium).** Snow Family stated closed; 600 TB in 30 days needs 1.85 Gbps against a 500 Mbps link frozen for 12 weeks -> the physical Data Transfer Terminal for the bulk load (Enterprise Support stated, as the docs restrict access) and DataSync for 400 GB a month over the existing link. Lessons 3.1 K01 and 3.5 K03/S03 state that Snowball Edge is closed and name both alternatives; 4.1 S07 for DataSync.
15. **de-streaming (Marigold Cabs).** No Kafka skills and SDK producers -> Kinesis Data Streams; three full readers with no interference -> enhanced fan-out; 12-hour re-read -> retained, replayable stream; no-code landing -> Firehose; rolling 5-minute per-city counts -> Managed Service for Apache Flink. Lesson 3.5 K07/S02.
16. **de-visualization (Thistledown Grocers).** 250 concurrent viewers, day-old data acceptable, no new database -> an imported (SPICE) dataset on Athena over a crawled catalog; the 60-second order view -> direct query. Lesson 3.5 S04 (SPICE for concurrent viewers; direct query for last-write freshness; crawler, Athena, QuickSight chain).

## constraint_reason check

All 16 keep one of two texts: "Mapped as design_exercise to complete skill coverage when no dedicated live lab step exists" (10) or "Service unavailable or not disposable in a personal same-day lab" (de-cdn, de-data-lake, de-emr-glue, de-snow, de-streaming, de-visualization). Both still make sense; no mismatch to report. The r4 item "Why live lab was unsuitable documented" is unchanged.

## Notes for reviewers

- Only 3.2-s04 names its service (Lambda, because the exercise sizes it) and de-snow names Snow Family (as closed). No scenario names the intended solution service; some name an engine or protocol as context (PostgreSQL, Apache Kafka as a skill the team lacks).
- de-saa-3.4-s01: a virtual private gateway or a transit gateway attachment is accepted; r6/r7 do not grade it.
- Probe points: 3.3-s03 relies on Aurora Serverless as the fit for intermittent load (lesson 3.3 S04); de-snow relies on Enterprise Support being stated in the scenario; 3.1-s01 uses "under 1 millisecond" (docs: io2 Block Express under 500 microseconds average; gp3 single-digit ms).

## Lesson additions requested

None required. Optional, doc-verified: lesson 3.1 K01 or 3.5 K03 could add "AWS Data Transfer Terminal is currently available only to AWS Enterprise Support customers; you reserve a slot at a facility, bring your own storage devices and upload over its fiber links." (source: docs.aws.amazon.com/datatransferterminal/latest/userguide/what-is-dtt.html). The scenario states the support plan, so the exercise does not depend on it.

## Script outputs

- content_lint.py: questions 429 aws 310 tf 119; labs 21 + 21; lessons 23; PASS.
- Scan of all 60 exercises (scenarios not in the two old templates): duplicate 6-word openings: none; duplicate organisation names: none.
- Teach-before-test regex (case-insensitive, backticks stripped) over lessons 2.1, 3.1-3.5, 4.1, 4.4 for every service or feature each solution needs: no misses.
