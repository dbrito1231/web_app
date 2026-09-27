# Student drill record: Task 4-3 (Cost-optimized databases)

## Committed answers (written before opening answer key)

1. q-saa-4-3-k01-mc — **d** — Need shared commitment discounts across accounts plus tag-based chargeback: that's consolidated billing (RDS RI sharing) + cost allocation tags together.
2. q-saa-4-3-k02-mc — **b** — "Trend and forecast" = Cost Explorer; "threshold alert" = Budgets, used together.
3. q-saa-4-3-k02-mr — **a, d** — CUR gives line-item SQL-analyzable chargeback data; Budgets gives proactive threshold warnings (actual + forecasted).
4. q-saa-4-3-k03-mc — **c** — Microsecond latency + lower RCU overbuy + no semantics change (API-compatible) is DAX's exact value prop.
5. q-saa-4-3-k04-mc — **a** — 30-day automated retention covers the recovery window; manual snapshots persist until deleted for long-term monthly copies (Aurora automated backups can't be indefinite).
6. q-saa-4-3-k05-mc — **d** — Unpredictable spikes + minimal capacity planning at launch = on-demand mode.
7. q-saa-4-3-k05-mr — **b, e** — b: RCU = 1 strongly consistent read/sec up to 4KB (correct definition). e: WCU = 1 write/sec up to 1KB (correct definition).
8. q-saa-4-3-k06-mc — **b** — Many short-lived Lambda connections + failover disruption is RDS Proxy's core use case (pooling + faster failover continuity).
9. q-saa-4-3-k07-mc — **c** — Removing commercial licensing means moving off Oracle to an open engine (heterogeneous); PostgreSQL on RDS with planned schema/type/query conversion is the realistic path.
10. q-saa-4-3-k08-mc — **a** — Offloading reporting reads, tolerating async lag, is the textbook read-replica use case.
11. q-saa-4-3-k08-mr — **c, e** — c: Multi-AZ DB instance = synchronous standby failover (HA). e: read replicas = asynchronous read offload (distinct mechanism for each stated goal).
12. q-saa-4-3-s03... wait mislabeled — q-saa-4-3-k09-mc — **d** — High-rate key-based lookups, no joins = DynamoDB.
13. q-saa-4-3-s01-mc — **b** — High criticality + limiting blast radius + cost control = tighter recovery coverage for critical pieces, isolated boundaries elsewhere.
14. q-saa-4-3-s01-mr — **b, d** — b: automated backups handle day-to-day operational restore. d: quarterly manual snapshots with cleanup of superseded ones gives long-term evidence at lower storage spend than "keep everything forever."
15. q-saa-4-3-s02-mc — **b** — Advanced JSON, custom extensions, complex query plans = PostgreSQL's known strengths.
16. q-saa-4-3-s02-mr — **a, e** — a: MySQL for compatibility/simple transactional. e: PostgreSQL for advanced JSON/extensions. Clean split of the two rule types asked for.
17. q-saa-4-3-s03-mc — **a** — Steady baseline + spikes, want less idle overprovisioning, keep managed relational = Aurora Serverless v2.
18. q-saa-4-3-s03-mr — **c, d** — c: on-demand for the unpredictable workload. d: provisioned + auto scaling for the stable known-throughput workload.
19. q-saa-4-3-s04-mc — **a** — Large column-subset scans + sustained analytical concurrency = Redshift columnar warehouse.
20. q-saa-4-3-s04-mr — **b, c** — b: correctly treat Timestream for LiveAnalytics as closed to new customers. c: evaluate Timestream for InfluxDB as the current alternative.
21. q-saa-4-3-s05-mc — **b** — DMS requires at least one endpoint (source or target) to be on an AWS service, so on-prem-to-on-prem directly is not supported.
22. q-saa-4-3-s05-mr — **d, e** — d: correctly classify as heterogeneous and plan conversion work (minimizes rework risk by not underestimating it). e: keep at least one endpoint on AWS to satisfy DMS constraints.

Note on Q12 numbering: I mislabeled mid-list while writing (called it "q-saa-4-3-s03..." then corrected) — the answer recorded for q-saa-4-3-k09-mc is d, unaffected by the typo.

No outright guesses this run — every answer matched a specific mechanism taught in the lesson text (K01–K09, S01–S05) rather than a coin-flip between two plausible options. Closest to a guess: Q9, where (b) Aurora MySQL-Compatible is tempting as "away from Oracle licensing," but the stem explicitly says "accepting schema and application query rework," which only matches (c)'s heterogeneous PostgreSQL path with planned conversion — so I'm confident, not guessing, but flagging that (b) is a plausible distractor for anyone who stops at "get off Oracle licensing" without reading the rework clause.

---

## Marking (after opening answer key)

| Q | Mine | Key | Result |
|---|------|-----|--------|
| 1 | d | d | correct |
| 2 | b | b | correct |
| 3 | a,d | a,d | correct |
| 4 | c | c | correct |
| 5 | a | a | correct |
| 6 | d | d | correct |
| 7 | b,e | b,e | correct |
| 8 | b | b | correct |
| 9 | c | c | correct |
| 10 | a | a | correct |
| 11 | c,e | c,e | correct |
| 12 | d | d | correct |
| 13 | b | b | correct |
| 14 | b,d | b,d | correct |
| 15 | b | b | correct |
| 16 | a,e | a,e | correct |
| 17 | a | a | correct |
| 18 | c,d | c,d | correct |
| 19 | a | a | correct |
| 20 | b,c | b,c | correct |
| 21 | b | b | correct |
| 22 | d,e | d,e | correct |

**Score: 22/22.**

---

## Fairness judgement

No questions were answered wrong, and I flagged no genuine guesses during the committed run (see the Q9 note above for the closest thing to a hesitation, which still resolved cleanly). So there is nothing to categorize under "wrong or guessed" — I'll answer the two standing questions honestly instead.

### Guessable stems (right answer findable by wording match alone, without needing the underlying concept)

- **Q1** — stem says "shared... plus... chargeback by... tags"; option d says "consolidated billing and... cost allocation tags." Near copy of the stem's two nouns.
- **Q3** — "chargeback-grade... for SQL analysis" → option a "Cost and Usage Report... line-item chargeback"; "proactive warning before... overspend" → option d "Budgets alerts on actual and forecasted." Both options echo stem vocabulary directly.
- **Q4** — stem says "microsecond read latency"; option c is literally "DynamoDB Accelerator" and the lesson text used the word "microseconds" for DAX specifically. Strong lexical giveaway.
- **Q9** — stem says "accepting schema and application query rework"; option c says "plan schema, data type, and query conversion." Near-verbatim match.
- **Q13** — stem says "limits blast radius impact"; option b says "isolate boundaries to reduce impact scope." Practically a paraphrase repeat.
- **Q17** — stem says "lower idle overprovisioning" + "managed relational"; only one option mentions elasticity within a managed relational service (Aurora Serverless v2, "bounded ACU range").
- **Q20** — stem says "avoid closed-to-new-customer guidance"; option b literally says "closed to new customers." Direct term reuse.
- **Q21** — stem asks about DMS "directly" on-prem-to-on-prem; option b restates the lesson's exact rule ("at least one endpoint... on an AWS service").
- **Q22** — same DMS endpoint rule restated near-verbatim in option e.

That's **9 of 22** (Q1, Q3, Q4, Q9, Q13, Q17, Q20, Q21, Q22) where I believe distinctive stem/option wording alone, without knowing the AWS mechanism, would get a test-taker to the right choice.

### Eliminable-on-sight distractors (ruled out because the service obviously does the wrong job, not because of lesson-specific knowledge)

- **Q2, option a** — "AWS Database Migration Service dashboards for spend forecasting" — DMS is a migration tool; it has no billing/forecasting function at all.
- **Q9, option a** — "Move to Oracle on EC2, keeping the same engine and licensing" — directly contradicts the stem's stated goal of removing licensing cost; self-eliminating on a plain read.
- **Q10, option d** — "Restore the latest automated backup into a separate reporting instance" — obviously a one-time stale copy, not a continuous reporting offload; wrong mechanism on its face.
- **Q12, option c** — "Use ElastiCache as the durable system of record" — ElastiCache is explicitly an in-memory cache; it is never a durable system of record, regardless of the specific lesson.
- **Q19, option d** — "Use a key-value primary table... for warehouse queries" — key-value point lookups obviously don't serve broad analytical scans/aggregations.

### Overall note

This drill scored 22/22, which is unusually clean for a 22-question set — worth flagging to Teacher/Lead Dev as a signal to watch, not celebrate blindly: with 9/22 stems solvable by wording match alone, roughly 40% of the set rewards recognizing the lesson's own phrasing rather than testing independent recall of the underlying AWS behavior. None of that makes any individual question wrong or unfair by the five-category rubric — every option that isn't correct is genuinely and clearly wrong, there's no ambiguity, no missing requirement, and no duplicate-answer pair — but a drill where distinctive lexical echoes from the lesson text repeatedly line up with the correct option is easier to pass by pattern-matching than a well-obfuscated drill would be. If the goal is to test transfer (can the student apply the concept when the wording doesn't hand it to them), consider rephrasing the ~9 flagged stems/options so they don't share such distinctive vocabulary with the correct choice.

