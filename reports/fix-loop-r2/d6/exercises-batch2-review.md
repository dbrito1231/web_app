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

---

## Teacher review (batch 2)

Saved by the Lead Dev from the Teacher's reply (condensed; replacement texts verbatim).

**Method.** The Teacher used a backtick-stripped, case-insensitive regex over lessons 3.1–3.5, 2.1, 4.1 and 4.4.
- **Teach-before-test:** passes except for Outposts in 3.4-s03 (AWS-DE2-007) and a replica-lag alarm in 3.3-s01 (TEACHER-DE2-003).
- **Arithmetic:** all of it was recomputed and holds.
- **Scenarios:** all are in operational language, and `constraint_reason` is consistent.

**Verdicts**
- **Approve:** 3.1-s01, 3.1-s02, 3.2-s04, 3.3-s03, de-cdn, de-data-lake, de-emr-glue, de-streaming.
- **Approve after fixes:** 3.4-s01 (T-001), 3.4-s02 (T-001, T-002), 3.4-s03 (AWS-007), 3.5-s03 (T-001).
- **Changes:** 3.3-s01 (AWS-003, T-003), 3.5-s06 (AWS-005), de-snow (AWS-001, AWS-002, T-001), de-visualization (AWS-006).

**Findings**
- **TEACHER-DE2-001 (minor):** four rubric items print the result of arithmetic the learner must do. Make each say "worked out and stated":
  - 3.4-s01 r7 tail: "with the rate each path must sustain worked out and stated".
  - 3.4-s02 r7 tail: "and the record shows, with the usable-address count worked out, why the existing /24 range alone cannot hold them".
  - 3.5-s03 r6: "(the required rate worked out and stated)".
  - de-snow r6: "the record shows, with the sustained rate required worked out, that it cannot be met over the existing 500 Mbps link".
- **TEACHER-DE2-002 (minor) 3.4-s02, constraint 3:** "Acquired companies' address ranges are all distinct, so no address translation is to be introduced, and every acquired VPC will be created in this same Region". This excludes Cloud WAN as an over-built multi-Region design.
- **TEACHER-DE2-003 (minor) 3.3-s01, constraint 3:** "operations must be alerted" needs a replica-lag alarm, which is not taught. No rubric item grades it. The Teacher recommends a lesson follow-up, or dropping the constraint.

**Second-role check on AWS-DE2-***
- **Agree:** 001, 002, 003, 005, 006, 007.
- **004:** accept either VPN attachment; the optional appended clause should not be applied.
- **Glue for Ray (CR-0019):** agree. It does not block batch 2.

Batch 2: not yet · Overall: concerns

## Lead Dev decision on TEACHER-DE2-003
Drop constraint 3 of de-saa-3.3-s01 in this pass: it is ungraded, and dropping it avoids a lesson change that would need user approval. The lesson idea ("raise an alarm on the replica-lag metric" in 3.3 S01) is recorded as an optional follow-up.

---

## Technical confirmation (fix pass)

Checked at 640fec8 ("D6 batch 2 fix pass"): `git diff b342969 640fec8 -- content` touches 8 exercise files (the lesson 2.2 and q-saa-2-2-s03-mc changes in that range are the separate CR-0018 work), read against the writer's "## Fix pass" table and the live JSON of de-saa-3.3-s01, 3.4-s02, 3.5-s06, de-snow and de-visualization.

### 1. AWS-DE2-001 to 007

| Id | Status |
| --- | --- |
| 001 | Gone. "Any other new network circuit, and none can be installed within the 30 days" excludes the Direct Connect hosted connection, so physical upload for the bulk load and DataSync for the monthly scans is the only design left. |
| 002 | Gone. "An AWS facility that accepts physical uploads" makes the physical design feasible without naming the service. |
| 003 | Gone. Aurora is excluded by name as an exclusion, not a solution. Same-Region replica plus cross-Region replica is now the only design. |
| 004 | Accept-either recorded. The optional clause was not applied, which is correct. r6 and r7 do not grade the attachment type. |
| 005 | Gone (a and b). "Fixed, pre-agreed capacity" rules out on-demand mode. r6 no longer names a partition concept and is checkable against the 60 percent and record-rate figures. |
| 006 | Gone (a and b). The scenario no longer states Athena's billing model. "Same cost Tuesday and Monday" plus 250 viewers and 3 s still decides the imported-dataset design. r6 is checkable against the scenario. |
| 007 | Gone. Outposts is excluded. Wavelength and Local Zone are unaffected, since the carrier's hardware is not installed by the firm or at the studio. |

### 2. Second-role check on the Teacher's findings

- **TEACHER-DE2-001 (four "worked out and stated" rewrites):** agree. All four rubric items (3.4-s01 r7, 3.4-s02 r7, 3.5-s03 r6, de-snow r6) are still checkable against the scenario's figures. The figures (0.13 Gbps, 251 usable addresses, 0.37 Gbps, 1.85 Gbps) are unchanged and correct, and the learner must now derive them. No answer is revealed.
- **TEACHER-DE2-002 (3.4-s02, same-Region constraint):** agree. It fits the scenario ("one Region"), excludes the multi-Region Cloud WAN design, and leaves Transit Gateway as the one best design. Accurate.
- **TEACHER-DE2-003 (3.3-s01 alerting constraint deleted):** agree. The constraint is gone and 6 constraints remain (4 generic, 2 stakeholder). The 30-second and 5-minute staleness figures are still in the scenario and r6 and r7, so the design is unchanged. A replica-lag alarm was never graded.

### 3. Changed-text checks

All 14 changed texts are accurate and determinate, and none names its solution service. Aurora (3.3-s01) and the physical facility (de-snow) appear only as exclusion or feasibility context. The scenario text, every r1 to r5 item and all fixed fields are unchanged. Two non-blocking notes:
- de-visualization: "each full read of the sales files has a cost" is a mild hint at per-scan billing but states no mechanism. Keep.
- de-snow: the five-hour-drive sentence is a stated premise. The doc says facility locations are shown only at reservation, which fits.

Batch 2: close

Overall: approve
