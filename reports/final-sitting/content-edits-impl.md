# Final sitting content edits: implementation report (2026-10-01)

No `accessed` or `reviewedOn` value was changed; new citation files carry `accessed` "2026-09-26" (the sweep updates them). No git, terraform, AWS or server commands were run.

## Item 1, CR-0019 (Glue for Ray)
- lesson-3-5 K04: "in one of three engines: Spark, Python shell, or Glue for Ray (...)" -> "in one of two engines: **Glue for Apache Spark** (...) or **Python shell** (...)". S05: "serverless Spark, Python shell, or Ray transforms" -> "serverless Spark or Python shell transforms". No Ray aside.
- cite-saa-3-5-glue-job-engines: title -> "AWS Glue for Spark and Python shell job types (AWS Glue for Ray is closed to new customers)"; note now says the page still lists Glue for Ray, which AWS closed to new customers on 2026-04-30 (per AWS-facts.md).
- RULES.md closed list: added "AWS Glue for Ray: closed to new customers (2026-04-30)." after FSx File Gateway.
- Distractors (taught-reason check against lesson-3-5):
  - k04-mr d -> "An AWS Glue Python shell job for the schema discovery". Taught: K04 says the crawler infers schema and writes the Data Catalog; the ETL job (Python shell = scripts on a single machine) acts once cataloged. Rationale updated. citation glue-job-engines kept.
  - k07-mr b -> "AWS DataSync for delivering the copy to S3". Taught: K03/S03 DataSync is file transfer into S3 and "don't reach for DataSync to solve a live event stream". Rationale updated. citationIds: glue-job-engines replaced by cite-saa-3-5-datasync-what-is (existing).
  - s01-mc c -> "Run an AWS Glue crawler so each analyst group sees only its own tables". Taught: K04/S01 crawler infers schema and populates the Catalog; grants come via Lake Formation grant/revoke. Rationale updated. glue-job-engines replaced by cite-saa-3-5-glue-data-catalog.
  - s04-mc d -> "Schedule an AWS Glue DataBrew job that writes a CSV extract to S3 each morning". Taught: DataBrew is a visual data-preparation tool for cleaning/normalising data (K04); QuickSight builds interactive dashboards (S04). NOT taught: that DataBrew jobs can be scheduled; the rationale therefore rests only on "data preparation, not a dashboard". glue-job-engines replaced by cite-saa-3-5-glue-databrew.
- Side effect: s04-mc key (63 chars) became the shortest choice, which worsened the pre-existing shortest-is-key line (5/14 -> 6/14). Key lengthened to "Import the dataset into Amazon QuickSight and hold it in SPICE memory storage" (77 chars, within the lengths of the other choices, no stem wording added). Final result identical to baseline.
- grep "Ray" in lesson-3-5, q-saa-3-5-*, cite-saa-3-5-*: only the cite note/title that labels the closure. (Other "Ray" hits are X-Ray, unrelated.)

## Item 2, CR-0021
- lesson-tf-g4 Warnings: replaced "Treat any state file containing sensitive or ephemeral-adjacent resources as itself sensitive, per group 3's state-security guidance." with the Teacher's sentence. Both quoted fragments verified verbatim: lesson-tf-g2 ("so it can contain sensitive values (such as...") and lesson-tf-g6 ("state data contains extremely sensitive information."), so the main sentence was used, not the fallback. No citation change (lesson wording only).

## Item 3, D6-FU
- lesson-4-4 K05: appended "By default AWS-to-on-premises traffic prefers one tunnel; with a transit gateway, dynamic (BGP) routing and ECMP enabled, multiple tunnels can carry traffic at once, which raises throughput beyond the 1.25 Gbps of a single tunnel." 1.25 Gbps is already in lesson 4.4 S07 and cite-saa-4-4-vpn-tunnels. Citations: new cite-saa-4-4-vpn-limits-ecmp (vpn-limits.html) added to lesson citationIds; cite-saa-4-4-vpn-tunnels (VPNTunnels.html, already cited) note extended with "AWS-to-on-premises traffic prefers one of the tunnels".
- lesson-3-3 S01: "monitor replica lag, since a replica" -> "monitor replica lag with the Amazon RDS `ReplicaLag` metric in CloudWatch, and set a CloudWatch alarm on it so the team hears when a replica falls too far behind, since a replica". New cite-saa-3-3-rds-replica-lag-monitoring (USER_ReadRepl.Monitoring.html), added to lesson citationIds. Note: per AWS-facts.md, no single page states "alarm on ReplicaLag"; the cite backs the metric only.
- de-saa-4.2-s05 r7 label: appended ", and neither fleet keeps more vCPUs or memory than its utilisation plus the headroom the record states". Grep of backend/ and scripts/ found no dependency on r7 text (only reports/ mention it). Teacher re-validation of this rubric change is still required.
- Regional NAT gateway: skipped as instructed.

## Item 4, LD-Qg7-002
Appended after the existing final full stop (one space) to the seven stems: 1a-mr, 1b-mr, 1c-mr, 2a-mr, 2b-mr, 2d-mr (all q-tf-004-*), and 4a-mc, with the exact texts given.

## Checks (before -> after)
Before and after outputs were identical for every script (diff empty); full list below is the after run, which equals baseline.

```
## content_lint
labs 21 + 21
lessons 23
PASS
## q1_batch_check 3-3
FAIL: MR key sets: most common 'a,b' in 4/8 (50%); all {'a,b': 4, 'a,c': 1, 'b,d': 1, 'b,e': 1, 'a,d': 1}
RESULT: FAIL
## distractor_type_audit 3-3
RESULT: FAIL (RDS, read replica, DynamoDB, ElastiCache, Aurora, Redshift)
## stem_echo_check 3-3
RESULT: FAIL
## claim_prose_check 3-3
## q1_batch_check 3-5
FAIL: shortest-is-key 5/14 = 36%
RESULT: FAIL
## distractor_type_audit 3-5
RESULT: FAIL (EMR, Glue, Athena)
## stem_echo_check 3-5
RESULT: FAIL
## claim_prose_check 3-5
## q1_batch_check 4-2
RESULT: PASS
## distractor_type_audit 4-2
RESULT: PASS
## stem_echo_check 4-2
RESULT: FAIL
## claim_prose_check 4-2
## q1_batch_check 4-4
RESULT: PASS
## distractor_type_audit 4-4
RESULT: PASS
## stem_echo_check 4-4
RESULT: FAIL
## claim_prose_check 4-4
## q1_batch_check tf-g1
RESULT: PASS
## distractor_type_audit tf-g1
RESULT: PASS
## stem_echo_check tf-g1
RESULT: PASS
## claim_prose_check tf-g1
## q1_batch_check tf-g2
RESULT: PASS
## distractor_type_audit tf-g2
RESULT: PASS
## stem_echo_check tf-g2
RESULT: PASS
## claim_prose_check tf-g2
## q1_batch_check tf-g4
RESULT: PASS
## distractor_type_audit tf-g4
RESULT: PASS
## stem_echo_check tf-g4
RESULT: PASS
## claim_prose_check tf-g4
## test_q1_letter
PASS: 12 bad, 10 good, 0 failures
## scan_lab
PASS 42 labs scanned
```

Pre-existing FAILs (present in baseline, unchanged): q1_batch_check 3-3 and 3-5; distractor_type_audit 3-3 and 3-5; stem_echo_check 3-3, 3-5, 4-2, 4-4. No new FAIL introduced. claim_prose_check prints WARN lines only (no RESULT line).
