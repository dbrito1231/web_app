# Lesson 4.3 / Task 4.3 questions - Senior AWS Solutions Architect review (Round 2)

Reviewed against:
- `content/lessons/lesson-4-3.json` (current)
- `reports/fix-loop-r2/q1/lesson-4-3-AWS.md` (my round-1 report)
- `reports/fix-loop-r2/q1/lesson-4-3-TEACHER.md` (Teacher round-1 report)
- `reports/fix-loop-r2/q1/lesson-4-3-impl.md`, `questions-4-3-impl.md`
- All 22 files `content/questions/q-saa-4-3-*.json`
- `scripts/distractor_type_audit.py 4-3` and `scripts/q1_batch_check.py 4-3` (read-only), both PASS
- AWS docs via `mcp-exec` (`search_documentation`, `read_sections`, `read_documentation`)

## (a) My own round-1 findings - Gone / not gone

- **AWS-L43-001** (S02 lacked a concrete engine discriminator) - **Gone.**
  The section now reads: "Choose MySQL when broad framework and tool compatibility plus simpler transactional workloads are the priority. Choose PostgreSQL when you need advanced JSON handling, complex queries, or custom extensions." This is the Teacher's wording, not my round-1 suggestion. Per the Lead Dev's framing, I am not re-litigating the wording choice, only judging whether a student can now discriminate. Verified against `https://docs.aws.amazon.com/AmazonRDS/latest/gettingstartedguide/choosing-engine.html`, which states verbatim: "Choose MySQL if your application needs broad compatibility with existing tools or frameworks, or if your workload involves simple transactional operations. Choose PostgreSQL if your application requires advanced features such as JSON data handling, complex queries, or support for custom extensions." The lesson sentence is a faithful paraphrase and gives a real, testable criterion (JSON/extensions/complex queries vs. compatibility/simple transactions). A student can now eliminate a MySQL option in a JSON/extension-heavy stem and vice versa. **Confirmed Gone on the Teacher's sentence.**
  - Minor observation (not a re-opening of the finding): the sentence is duplicated verbatim back-to-back in the S02 prose (an apparent copy-paste artifact from the fix), and the same duplication pattern also appears in K05 ("switch... four times in a 24-hour rolling window" appears twice, plus a third paraphrase) and in S05 (the DMS constraint sentence is duplicated). This does not affect correctness or teach-before-test readiness, so it does not block closure, but it is untidy prose the Lead Dev may want to clean up in a later pass.

## (b) Second-role check on Teacher's round-1 findings

- **TEACHER-L43-001** (S02 MySQL vs PostgreSQL discriminator) - **Gone.** Same finding as `AWS-L43-001`; see (a) above. Doc-verified.
- **TEACHER-L43-002** (DMS "at least one endpoint on AWS" constraint) - **Gone.** S05 now states: "With AWS DMS, at least one endpoint, source or target, must be on an AWS service, so it cannot migrate directly from one on-premises database to another on-premises database." Verified verbatim against `https://docs.aws.amazon.com/dms/latest/userguide/CHAP_Introduction.html`: "The only requirement to use AWS DMS is that one of your endpoints must be on an AWS service. You can't use AWS DMS to migrate from an on-premises database to another on-premises database." Present in lesson prose (not just the claim table), confirmed.
- **TEACHER-L43-003** (blast radius plain-language definition) - **Gone.** S01 now states: "Blast radius means how much of your workload is affected when one component fails, and fault-isolated boundaries keep unaffected components outside that impact scope." Consistent with `https://docs.aws.amazon.com/wellarchitected/2023-10-03/framework/rel-10.html` ("fault isolated boundary": "A boundary that restricts the effect of a failure within a workload to a limited number of components, leaving components outside unaffected"). Present in prose, confirmed.
- **TEACHER-L43-004** (ACID plain-language definition) - **Gone.** K09 now states: "ACID means atomicity, consistency, isolation, and durability: related changes complete together or fail together while preserving data correctness." Matches `https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/transactions.html`: "Transactions provide atomicity, consistency, isolation, and durability (ACID) in DynamoDB, helping you to maintain data correctness in your applications." Present in prose, confirmed.

All four Teacher findings and my one finding are Gone.

## (c) Per-question review (all 22)

| id | verdict | notes |
|---|---|---|
| q-saa-4-3-k01-mc | OK | Key (d) matches taught consolidated-billing + tag-activation pattern. Distractors are real, each misses one stated requirement (no tags, no account sharing, wrong discount type). No strawmen. |
| q-saa-4-3-k02-mc | OK | Key (b) correct tool pairing. Distractors are real services/features used for the wrong purpose (DMS, Backup inventory, failover notifications), not strawmen. |
| q-saa-4-3-k02-mr | OK | Key (a,d) correct. Distractor (b) "buy reserved capacity to produce alerts" is a real action but a logically confused claim (buying capacity doesn't create alerts) - acceptable as a "real option applied wrong," not a strawman. |
| q-saa-4-3-k03-mc | OK | Key (c) DAX correct for the stated microsecond + no-semantics-change requirement. ElastiCache distractor correctly framed as requiring redesign (real tradeoff, not strawman). |
| q-saa-4-3-k04-mc | OK | Key (a) correct: automated retention for the 30-day window + manual snapshots for indefinite retention. "30-day" is within the taught 0-35 day RDS / 1-35 day Aurora ranges. |
| q-saa-4-3-k05-mc | OK | Key (d) on-demand for unpredictable/minimal-planning launch traffic is correct and matches K05 teaching. |
| q-saa-4-3-k05-mr | OK, numbers verified | Key (b,e): "1 RCU = 1 strongly consistent read/sec up to 4 KB" and "1 WCU = 1 write/sec up to 1 KB." Verified directly against `https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/provisioned-capacity-mode.html`: "For an item up to 4 KB, one read capacity unit (RCU) represents one strongly consistent read operation per second... A write capacity unit (WCU) represents one write per second for an item up to 1 KB." Exact match. Distractors (a, d) swap read/write meanings; (c) invents a false "always 8 KB" on-demand unit - correctly a real-option-applied-wrong distractor, not a strawman. |
| q-saa-4-3-k06-mc | OK | Key (b) RDS Proxy for connection pooling + failover smoothing is correct and matches K06 lesson content. |
| q-saa-4-3-k07-mc | OK | Key (c) PostgreSQL for JSON/complex queries/extensions matches the doc-verified S02 discriminator. MariaDB distractor (b) is a real, current RDS engine, not retired - acceptable as a plausible option that doesn't meet the JSON/extension requirement. |
| q-saa-4-3-k08-mc | OK | Key (a) read replicas for async read offload; Multi-AZ standby distractor correctly identified as not serving reads. |
| q-saa-4-3-k08-mr | OK | Key (c,e): Multi-AZ DB instance for sync failover + read replicas for async read scaling. Correct and matches lesson K08 content precisely. |
| q-saa-4-3-k09-mc | OK | Key (d) DynamoDB for key-based, join-free, high-scale access. Reasonable distractors (Aurora, MySQL, ElastiCache-as-durable-store). |
| q-saa-4-3-s01-mc | OK | Key (b) tighter recovery + isolated blast-radius boundaries for high-criticality data, now teach-before-test ready since S01 defines "blast radius" in prose. |
| q-saa-4-3-s01-mr | OK | Key (b,d): automated backups for operational restore + manual snapshot lifecycle policy for cost-controlled long-term evidence. Matches K04/S01 teaching. |
| q-saa-4-3-s02-mc | OK | Key (b) PostgreSQL on RDS for JSON/extensions/complex queries. Directly traceable to the now-fixed S02 discriminator sentence. |
| q-saa-4-3-s02-mr | OK | Key (a,e): MySQL-for-compatibility / PostgreSQL-for-advanced-features pairing is exactly the taught discriminator; distractors correctly invert or misapply the criteria. |
| q-saa-4-3-s03-mc | OK | Key (a) Aurora Serverless v2 with bounded ACU range for steady+spiky traffic. Matches S03/K05 teaching on ACU-based elasticity. |
| q-saa-4-3-s03-mr | OK | Key (c,d): on-demand for unpredictable, provisioned+auto scaling for stable known throughput. Correct per S03/K09 lesson content. |
| q-saa-4-3-s04-mc | OK | Key (a) Redshift columnar for large-column-subset analytical scans, matching S04 and the verified Redshift claim. |
| q-saa-4-3-s04-mr | OK | Key (b,c): Timestream for LiveAnalytics correctly flagged closed-to-new-customers, InfluxDB correctly flagged as the current alternative - matches lesson status framing exactly. |
| q-saa-4-3-s05-mc | OK, number/constraint verified | Key (b): "AWS DMS requires at least one endpoint, source or target, on an AWS service." Verified directly against DMS docs (see (b) above) - exact match, both clauses correct (no direct on-prem-to-on-prem). |
| q-saa-4-3-s05-mr | OK, constraint verified | Key (d,e): heterogeneous classification + at-least-one-AWS-endpoint rule. Same doc verification as s05-mc applies to choice (e). |

No `AWS-Q43-###` issues found. All 22 questions have a doc-supportable key, real (non-strawman) distractors that each fail exactly one stated requirement, rationales that explain by content (no letter references), and citations pointing to relevant, already-verified citation files.

## (d) Numbers-in-keys verification

Scanned every correct-answer choice text across all 22 questions for numeric claims. Only two questions have numbers in their key text:

- `q-saa-4-3-k05-mr`: key choices (b) "4 KB" strongly-consistent-read RCU definition and (e) "1 KB" WCU definition. **Verified** directly against `provisioned-capacity-mode.html` (quoted in full in (c) above) - exact match.
- `q-saa-4-3-k04-mc`: key choice (a) uses "30-day" as the audit's automated-retention figure. This is a scenario-chosen value, not a service-limit claim; it sits inside the doc-verified ranges already confirmed in round 1 (RDS DB instance: 0-35 days; Aurora cluster: 1-35 days), so no separate citation is needed.

No other key choice in the remaining 20 questions contains a number. All numeric values that do appear in keys check out against AWS documentation.

## RDS-family distractor adjudication

`distractor_type_audit.py 4-3` output: `RDS 3 14% (k01-mc, k02-mc, s02-mc)`. Also at 3/22 (14%): `Multi-AZ` and `On-Demand`. All three sit under the 15% cap and the script's overall result is `PASS`.

**Verdict: acceptable, on-topic** - RDS is the flagship relational database service and the direct subject of multiple objectives in this lesson (K01 reserved discounts, K06 proxy, K08 replication, S02 engine choice), so RDS-family terms recurring as distractors or keys across a handful of questions in a *databases* lesson is expected topical density, not genuine over-reuse. This mirrors the precedent set for Outposts-at-3 in task 4.2 (acceptable, on-topic), and the 14% figure is both below the 15% per-type cap and spread across three unrelated objectives (K01 discount scope, K02 tooling, S02 engine choice) rather than repeating the same RDS fact three times.

## Findings summary

- Round-1 findings closed: 1 of 1 (`AWS-L43-001`).
- Teacher findings confirmed closed (second-role check): 4 of 4 (`TEACHER-L43-001` through `-004`).
- New question findings (`AWS-Q43-###`): **0**.
- Non-blocking observation: duplicated sentences in lesson prose (S02, K05, S05) - cosmetic, does not affect correctness or teach-before-test readiness; flagged for optional cleanup only.

Task 4.3: close

Overall: approve

## Round 2 recheck

Re-reviewed after Teacher's `TEACHER-Q43-001` through `-004` and the corrected distractor-cap violations landed (commit `dcd1633`, per coordinator). Re-read the eight changed files (`q-saa-4-3-k07-mc`, `k08-mc`, `k08-mr`, `k09-mc`, `s02-mc`, `s03-mc`, `k02-mr`, `s01-mr`), re-ran `distractor_type_audit.py 4-3`, `q1_batch_check.py 4-3`, `content_lint.py`, and re-checked the lesson body for the duplicated-sentence artifact I had flagged as non-blocking. Verified new/changed claims against AWS docs via `mcp-exec`.

### Second-role check on Teacher's findings

- **TEACHER-Q43-001 (high, `q-saa-4-3-k07-mc` tested S02's fact instead of K07's)** - **Gone.** The rewritten question now tests K07's own objective (homogeneous vs. heterogeneous migration and its cost/effort consequences), not the S02 JSON/extensions discriminator. No overlap remains with `s02-mc` (which still tests the JSON/extensions criterion) or with `s05-mc`/`s05-mr` (which test the DMS AWS-endpoint constraint and heterogeneous-classification planning) - `k07-mc` instead tests licensing-cost impact of homogeneous vs. heterogeneous engine choice, a distinct fact. Doc-verified all four choices:
  - Key (c), "Move to Amazon RDS for PostgreSQL and plan schema, data type, and query conversion": Oracle -> PostgreSQL is heterogeneous (different engine), matching `CHAP_Introduction.html`'s own worked example, "such as from an Oracle database to a PostgreSQL database," and correctly requires conversion work.
  - (a), Oracle on EC2, same engine/licensing: confirmed homogeneous (same engine, only hosting changes) and confirmed Oracle requires a commercial license under both License-Included and BYOL models per `https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/Oracle.Concepts.Licensing.html` and the Oracle-on-AWS best-practices whitepaper - self-managing Oracle on EC2 does not remove that licensing requirement, so "keeping ... its current licensing profile" is accurate.
  - (b), Aurora MySQL-Compatible Edition from Oracle: confirmed heterogeneous. AWS's own DMS sample playbook is titled "AWS DMS heterogeneous migration" for exactly this Oracle-to-Aurora-MySQL case (`https://docs.aws.amazon.com/dms/latest/oracle-to-aurora-mysql-migration-playbook/chap-oracle-aurora-mysql.tools.awsdms.html`), so "keep the existing SQL dialect unchanged" is correctly the flaw (dialect and data types do change).
  - (d), "rely on AWS DMS alone to convert stored procedures and application SQL": confirmed wrong. AWS's own migration guides pair DMS (data movement) with a separate tool - AWS SCT or DMS Schema Conversion - specifically for stored procedures/schema/code conversion (e.g., "AWS SCT for schema conversion and AWS DMS for data migration," `https://docs.aws.amazon.com/dms/latest/sbs/chap-sqlserver2aurora.html`). DMS does not by itself convert stored procedures or application SQL, so (d) is a real but incomplete option, not a strawman.
  - Rationale explains each option by content, no letter references, no giveaway wording. **Confirmed Gone.**
- **TEACHER-Q43-002 / -003 (moderate, duplicated lesson prose in S02/S05, plus K05's "four times in 24 hours" tripled)** - **Gone.** Re-scanned `content/lessons/lesson-4-3.json` bodyMarkdown for any sentence longer than 40 characters repeated more than once: none found (script check, see below). The S02 MySQL/PostgreSQL sentence, the S05 DMS-endpoint sentence, and the K05 switch-limit sentence each now appear exactly once.
- **TEACHER-Q43-004 (low, `s03-mc` choice (c) strawman)** - **Gone.** Choice (c) is now "Use ElastiCache in front of a peak-sized cluster to absorb the traffic spikes" - a real, plausible architecture choice, not an anti-pattern. The rationale correctly explains why it misses the stated requirement (the relational cluster stays provisioned at peak size, so the idle-cost problem the question asks to solve is not actually removed). No strawman wording remains.

### Doc verification of new/changed choice text and rationale (8 files)

- `q-saa-4-3-k07-mc`: all four choices and the rationale doc-verified above under TEACHER-Q43-001.
- `q-saa-4-3-k08-mc`: new distractor (d), "Restore the latest automated backup into a separate reporting instance," is a real but stale/non-continuous approach - consistent with K04/S01 teaching that restores create point-in-time copies, not live continuous replicas. No factual issues; key (a) unchanged and previously verified.
- `q-saa-4-3-k08-mr`: choice (a) reworded to "Use read replicas to provide synchronous standby failover" (still a real-option-applied-wrong distractor: read replicas are asynchronous per `USER_ReadRepl.html`, so pairing them with "synchronous standby failover" is the stated error). Choice (d) reworded to "Use a larger writer instance class as the read-scaling mechanism" - real action, correctly insufficient as a distinct read-scaling mechanism. Key (c, e) unchanged and previously verified.
- `q-saa-4-3-k09-mc`: distractor (b) now "MySQL instance with secondary indexes for key lookups" and (c) now "ElastiCache as the durable system of record for session data" - both real, on-topic distractors; (c)'s flaw (ElastiCache is not a durable system of record) is accurate per ElastiCache's in-memory-cache positioning. Key (d) unchanged.
- `q-saa-4-3-s02-mc`: distractor (c) reworded to "MySQL on Amazon RDS with a larger instance class for extension compatibility" - real action, correctly does not add PostgreSQL-style extensions. Key (b) unchanged and previously doc-verified against `choosing-engine.html`.
- `q-saa-4-3-s03-mc`: distractor (c) verified above under TEACHER-Q43-004. Key (a) unchanged and previously verified.
- `q-saa-4-3-k02-mr`: choice (c) reworded to "Use Cost Explorer dashboards for detailed line-item SQL reconciliation" (dropped "as the only source," removing a giveaway-adjacent absolute qualifier) - still correctly wrong because Cost Explorer is trend/forecast-oriented, not a line-item SQL reconciliation source; CUR is. Key (a, d) unchanged.
- `q-saa-4-3-s01-mr`: choice (a) reworded to "Use read replicas to meet backup and point-in-time retention needs" - real service, correctly wrong (read replicas are not a backup/PITR mechanism). Key (b, d) unchanged and previously verified.

No new `AWS-Q43-###` issues found in the reworked or surrounding content.

### Numbers-in-keys re-check

None of the eight changed files introduced a new number in a correct-answer choice. The two numeric keys identified in round 2 (`q-saa-4-3-k05-mr`'s 4 KB/1 KB RCU/WCU definitions, and `q-saa-4-3-k04-mc`'s 30-day scenario value, both untouched by this round's edits) remain doc-verified as reported above.

### Script re-verification

- `distractor_type_audit.py 4-3` (word-boundary fix applied): **PASS**, 15% cap = 3 questions. Highest counts are now RDS 3 (14%, `k01-mc,k02-mc,s02-mc`), Aurora 3 (14%, `k07-mc,k09-mc,s03-mc`), ElastiCache 3 (14%, `k03-mc,k09-mc,s03-mc`), Multi-AZ 3 (14%, `k04-mc,k08-mc,k08-mr`), DMS 3 (14%, `k07-mc,s05-mc,s05-mr`), read replica 3 (14%, `k06-mc,k08-mr,s01-mr`). All other types at or below 9%. No type exceeds the cap.
- `q1_batch_check.py 4-3`: **PASS** on every check (lesson formatting, drillIds, exam tips, duplicate stem openings, longest-is-key 21%, MC key positions, MR key slots, MR key-set distribution).
- `content_lint.py`: **PASS** across the full project (429 AWS + 119 TF questions, 21+21 labs, 23 lessons).
- Lesson-prose duplicate-sentence scan: **0 duplicates found** (previously 3: S02, K05, S05).

### RDS adjudication re-confirmed

RDS-family terms remain at 3 of 22 (14%), unchanged from round 1's adjudication and still under the 15% cap. The corrected audit now also shows Aurora, ElastiCache, Multi-AZ, DMS, and read replica each at exactly 3 of 22 (14%) as well - six service families tied at the same count, none over cap. This is a *more* even spread across on-topic database services than the pre-fix state (which had concentrated overuse in read replica at 27% and snapshot at 18%, now both corrected to 14% and 9% respectively). **Verdict unchanged: acceptable, on-topic** - a databases lesson naturally cites RDS, Aurora, Multi-AZ, DMS, ElastiCache, and read replicas repeatedly across its 14 objectives; each occurrence tests a different fact (discount scope, engine choice, failover vs. read-scaling, migration classification, caching durability), and no single type crosses the 15% ceiling.

### Summary

- `TEACHER-Q43-001` (high): Gone, confirmed with full doc verification of the rewritten question.
- `TEACHER-Q43-002`/`-003` (moderate, duplicated prose): Gone, confirmed via lesson-body scan.
- `TEACHER-Q43-004` (low, strawman): Gone, confirmed.
- Distractor-cap corrections (read replica 27%->14%, snapshot 18%->9%): confirmed via re-run of `distractor_type_audit.py`, both now PASS.
- New `AWS-Q43-###` issues from this round: **0**.

Task 4.3: close

Overall: approve
