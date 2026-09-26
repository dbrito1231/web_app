# Teacher review — Task 3.5 questions, Round 2

Saved by Lead Dev from the Teacher's reply (AGENTS.md: the Teacher does not write files).

`q1_batch_check.py 3-5`: RESULT WARN — but the only WARNs are the two pre-existing, already-approved "Snowball" mentions in the lesson body (retired status labeled). No question-level FAIL/WARN. Confirmed independently.

**My view on the Lake Formation/EMR/Athena reuse (RULES.md 15%/3-question cap):** I agree with AWS's call, with one caveat. Read literally by raw service name, Lake Formation appears as a wrong-role distractor 5 times (20.8%), over the cap. But I checked all 5 uses myself (k01-mc: no query engine; k05-mc: bucket-wide governance vs. narrow VPC/prefix scoping; s03-mc: no mount/file-share capability; s04-mr: not a QuickSight data source; s05-mr: doesn't execute SQL) — each teaches a genuinely distinct fact, not a repeated crutch (unlike round 1's DataBrew problem, which the writer already fixed). Given the lesson only names ~13 services across 14 objectives and 24 questions each need 3-4 real same-area distractors, some recurrence is structurally unavoidable. I read the RULES' intent as "don't lean on the same lazy gag repeatedly," which this doesn't do. Not a blocker — but flagging as a pattern worth watching if it recurs lesson after lesson, since raw-service reuse this high could still erode a student's ability to eliminate answers by service alone.

**Per-question table**

| id | objective fit | teach-before-test | difficulty | strawman | giveaway wording | rationale | fairness | verdict |
|---|---|---|---|---|---|---|---|---|
| k01-mc | yes | yes | appropriate | none | none | full coverage | fair | OK |
| k01-mr | yes | yes | appropriate | none | none | full coverage | fair | OK |
| k02-mc | yes | yes | appropriate | none | none | full coverage | fair | OK |
| k03-mc | yes | yes (3.1-grounded) | appropriate | none | none | full coverage | fair | OK |
| k04-mc | yes | yes | appropriate | none | none | full coverage | fair | OK |
| k04-mr | yes | yes | appropriate | none | none | full coverage | fair | OK |
| k05-mc | yes | yes | appropriate | none | none | full coverage | fair | OK |
| k06-mc | yes | yes, math verified (8500/1000→9) | appropriate | none | none | full coverage | fair | OK |
| k07-mc | yes | yes | appropriate | none | none | full coverage | fair | OK |
| k07-mr | yes | yes | appropriate | none | none | full coverage | fair | OK |
| s01-mc | yes | yes | appropriate | none | none | full coverage | fair | OK |
| s01-mr | yes | yes | appropriate | none | none | full coverage | fair | OK |
| s02-mc | yes | yes | appropriate | none | none | full coverage | fair | OK |
| s02-mr | yes | yes, math verified (2 MiB/s/shard/consumer) | appropriate | none | none | full coverage | fair | OK |
| s03-mc | yes | yes (3.1-grounded) | appropriate | none | none | full coverage | fair | OK |
| s03-mr | yes | yes (3.1 Snowball-EOL grounded) | appropriate | none | none | full coverage | fair | OK |
| s04-mc | yes | yes | appropriate | none | none | full coverage | fair | OK |
| s04-mr | yes | yes | appropriate | none | none | full coverage | fair | OK |
| s05-mc | yes | yes, watch item satisfied (no Lambda/Redshift) | appropriate | none | none | full coverage | fair | OK |
| s05-mr | yes | yes, watch item satisfied | appropriate | none | none | full coverage | fair | OK |
| s06-mc | yes | yes | appropriate | see TEACHER-Q35-001 | none | full coverage | fair | OK |
| s06-mr | yes | yes | appropriate | none | none | full coverage | fair | OK |
| s07-mc | yes | yes | appropriate | none | none | full coverage | fair | OK |
| s07-mr | yes | yes, benchmark verified | appropriate | none | none | full coverage | fair | OK |

**Issues**

- **TEACHER-Q35-001** (low, non-blocking) — `s06-mc` choice d, "Add more broker nodes to the Kinesis Data Streams cluster." Kinesis Data Streams has no "broker node" concept at all (that's an MSK term), so this isn't strictly a "real AWS option" per RULES.md's distractor requirement — it's a manufactured category-confusion phrase. It is, however, pedagogically grounded (the lesson's K07 exam tip explicitly contrasts Kinesis shards vs. MSK brokers), reads as a plausible trap for a student who conflates the two services, and is not a strawman/anti-pattern. Optional fix if the team wants strict literal compliance: reword to a real Kinesis action that still fails, e.g. "Increase the stream's provisioned read capacity" (real lever, wrong because it doesn't fix hot-shard skew). Not required for closure.

No other issues found. All 24 questions test their own objective, are grounded in lesson 3.5 (or 3.1 where flagged), free of strawmen and giveaway wording, and have complete per-choice rationale.

Task 3.5: close

Overall: approve

## Lead Dev action on TEACHER-Q35-001

The made-up "broker nodes" choice in  is replaced with a real Kinesis option taught in lesson 3.5: "Register the stream's consumers for enhanced fan-out". It is wrong because it adds read throughput, not write distribution. The rationale is updated and  is added.
