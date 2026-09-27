# Teacher review: task 4.3 (round 2)

## (a) Round-1 Teacher findings: Gone / not gone

- **TEACHER-L43-001** (S02 MySQL vs PostgreSQL discriminator) — **Gone**, in the prose. `content/lessons/lesson-4-3.json`, S02 section now contains the exact requested sentence: "Choose MySQL when broad framework and tool compatibility plus simpler transactional workloads are the priority. Choose PostgreSQL when you need advanced JSON handling, complex queries, or custom extensions." It gives a usable discriminator (compatibility/simple-transactional vs JSON/complex-query/extensions), and `q-saa-4-3-s02-mc`/`-mr` exercise it correctly.
  - **New defect found while confirming this:** the whole two-sentence discriminator is **duplicated verbatim** in the S02 paragraph (it appears twice in a row). See `TEACHER-Q43-002` below.

- **TEACHER-L43-002** (DMS "at least one endpoint on AWS" rule) — **Gone**, in the prose. S05 now states: "With AWS DMS, at least one endpoint, source or target, must be on an AWS service, so it cannot migrate directly from one on-premises database to another on-premises database." `q-saa-4-3-s05-mc` and `-mr` correctly test it.
  - **New defect found while confirming this:** that sentence is also **duplicated verbatim** back-to-back in S05. See `TEACHER-Q43-003` below.

- **TEACHER-L43-003** (undefined "blast radius") — **Gone**. S01 now reads: "Blast radius means how much of your workload is affected when one component fails, and fault-isolated boundaries keep unaffected components outside that impact scope." Appears once, cleanly. `q-saa-4-3-s01-mc` uses the term correctly and is answerable from this sentence.

- **TEACHER-L43-004** (undefined "ACID") — **Gone**. K09 now reads: "ACID means atomicity, consistency, isolation, and durability: related changes complete together or fail together while preserving data correctness." Appears once, cleanly, before the term is used for a decision.

## (b) Second-role check on AWS-L43-001

**Gone**, with the same caveat as `-001` above. `AWS-L43-001` and my `TEACHER-L43-001` were the same S02 gap. The writer used my MySQL-vs-PostgreSQL sentence rather than AWS's vaguer "RDS for PostgreSQL supports many PostgreSQL extensions" wording. I confirm this is the right call: my sentence gives a two-sided, concrete discriminator (what makes each engine the right pick), while the AWS sentence only asserts a PostgreSQL fact with nothing to contrast it against. A student can now eliminate a MySQL distractor in a JSON/extension-requirement question, and eliminate a PostgreSQL distractor in a compatibility/simple-transactional question. The only outstanding problem is the duplication defect noted in `TEACHER-Q43-002`, which is cosmetic, not a comprehension gap.

## (c) Per-question review (all 22)

| id | verdict | issues |
|---|---|---|
| q-saa-4-3-k01-mc | OK | Real distractors, each fails one stated requirement (tag activation, account-level sharing, wrong discount product). Taught in K01. |
| q-saa-4-3-k02-mc | OK | Clean three-tool contrast (Cost Explorer / Budgets / CUR-adjacent). Distractors (DMS dashboards, Backup inventory, failover notifications) are real services doing the wrong job, but the stem's specific ask (trend+forecast, then threshold alert) makes them fail on stated requirement, not on absurdity. |
| q-saa-4-3-k02-mr | OK | See `TEACHER-Q43-001` pattern note (choice c uses "as the only"). Facts (CUR for chargeback, Budgets for alerts) are taught. |
| q-saa-4-3-k03-mc | OK | DAX vs ElastiCache vs Standard-IA vs raise-RCUs is a fair, taught contrast. |
| q-saa-4-3-k04-mc | OK | Automated-retention-vs-manual-snapshot contrast is taught; 30-day number is inside the valid Aurora 1–35 day range. |
| q-saa-4-3-k05-mc | OK | On-demand vs provisioned-with-frequent-switching vs reserved-before-baseline is taught and fair. |
| q-saa-4-3-k05-mr | OK | RCU/WCU 4 KB/1 KB definitions match lesson and doc exactly; distractors swap read/write correctly to test the confusion. |
| q-saa-4-3-k06-mc | OK | RDS Proxy vs upsize vs replica vs DNS-tuning is taught and each distractor fails a named part of the stem (connection pooling vs capacity vs read-scaling vs endpoint-refresh). |
| q-saa-4-3-k07-mc | **Not OK — `TEACHER-Q43-001`** | See below. |
| q-saa-4-3-k08-mc | OK | Read replica vs Multi-AZ standby vs upsize vs snapshot-as-read-path is the core K08 contrast and is taught. |
| q-saa-4-3-k08-mr | OK | Distinct-mechanism-for-distinct-goal framing is taught and fair; keys (c, e) match the "standby=failover, replica=read scaling" lesson pairing. |
| q-saa-4-3-k09-mc | Minor — `TEACHER-Q43-004` | DynamoDB vs relational vs cache; see strawman note on choice c. |
| q-saa-4-3-s01-mc | OK | Blast-radius language now taught (see (a)); tighter-recovery-for-critical vs one-size-fits-all is a fair S01 test. |
| q-saa-4-3-s01-mr | OK | See `TEACHER-Q43-001` pattern note (choice a uses "as the only"). Otherwise fair and taught. |
| q-saa-4-3-s02-mc | Fact overlap — `TEACHER-Q43-001` | Correct in isolation, but see the K07 duplicate finding. |
| q-saa-4-3-s02-mr | Fact overlap — `TEACHER-Q43-001` | Correct in isolation, but see the K07 duplicate finding. |
| q-saa-4-3-s03-mc | Minor — `TEACHER-Q43-004` | Aurora Serverless v2 vs peak-sized provisioned vs DynamoDB-as-relational-substitute vs manual resize; see strawman note on choice c. |
| q-saa-4-3-s03-mr | OK | On-demand-for-unpredictable / provisioned+autoscaling-for-stable is the core S03 contrast and is taught. |
| q-saa-4-3-s04-mc | OK | Redshift columnar vs Athena vs transactional vs key-value point-lookup is taught and each distractor fails the stated "large column subsets + sustained concurrency" requirement for a distinct reason. |
| q-saa-4-3-s04-mr | OK | Timestream status-awareness is taught (closed-to-new-customers date, InfluxDB alternative). Fair and current. |
| q-saa-4-3-s05-mc | OK | DMS endpoint-location rule is taught and directly testable; distractors (schema conversion doesn't remove the constraint, VPN doesn't either, "homogeneous only" is false) are all real misconceptions. |
| q-saa-4-3-s05-mr | Minor overlap noted | Choice e restates the same DMS endpoint fact that is the entire point of `q-saa-4-3-s05-mc`. Combined with the heterogeneous-classification fact (d) this is a defensible MR design (two facts, one shared with the MC), not a hard duplicate-question violation, but flag if a 23rd S05 question is ever added — don't reuse this fact a third time. |

### `TEACHER-Q43-001` — high — duplicate fact / objective mismatch across three questions
- **Location:** `content/questions/q-saa-4-3-k07-mc.json`, `q-saa-4-3-s02-mc.json`, `q-saa-4-3-s02-mr.json`
- **Issue:** `q-saa-4-3-k07-mc` is tagged `objectiveIds: ["SAA-4.3-K07"]` (database engines with appropriate use cases, *for example, heterogeneous/homogeneous migrations*), but its stem, choices, key, and rationale test the exact same fact as the two S02 questions: "MySQL = compatibility/simple transactional; PostgreSQL = JSON/complex queries/extensions." The correct-choice text in `k07-mc` ("Choose PostgreSQL for advanced JSON handling, complex queries, and extension support") is near-verbatim identical to the correct-choice text in `s02-mc` ("Use PostgreSQL on Amazon RDS" — same rationale) and to one of the two correct choices in `s02-mr`. K07's actual objective content (homogeneous vs heterogeneous migration, which the lesson teaches at length in its own K07 section) is never tested by any question in the task — S05 tests DMS endpoint rules and heterogeneous/homogeneous classification instead, so migration-type knowledge is only exercised under the S05 tag, and K07 is left testing S02's fact three times over.
- **Doc-verified fix:** Rewrite `q-saa-4-3-k07-mc` to test K07's own content — homogeneous vs heterogeneous migration selection — using the lesson's own K07 sentence: `"AWS DMS supports both: homogeneous migration (same engine to same engine, such as Oracle to Oracle), heterogeneous migration (different engines, such as Oracle to PostgreSQL)."` (source: `https://docs.aws.amazon.com/dms/latest/userguide/CHAP_Introduction.html`, matches claim-table row 23). A safe pattern: a stem where a company is moving Oracle-to-Oracle for a lift-and-shift with minimal code changes (homogeneous, lower risk) vs. Oracle-to-PostgreSQL for cost reasons (heterogeneous, more conversion risk), asking which term applies to a stated scenario, with distractors drawn from real migration-tool confusions (e.g., calling an Oracle-to-Oracle move "heterogeneous," or claiming homogeneous moves eliminate all code changes). Make sure the new choices are not already used verbatim in `s05-mc`/`s05-mr`.

### `TEACHER-Q43-002` — moderate — duplicated sentence in lesson prose (S02)
- **Location:** `content/lessons/lesson-4-3.json`, S02 section, first paragraph
- **Issue:** The two-sentence MySQL/PostgreSQL discriminator appears twice back-to-back: "Choose MySQL when broad framework and tool compatibility plus simpler transactional workloads are the priority. Choose PostgreSQL when you need advanced JSON handling, complex queries, or custom extensions." (x2). This is very likely a copy-paste artifact from applying the round-1 fix. It doesn't misstate anything, but it reads as broken prose to a student and is worth cleaning up.
- **Fix:** Delete the second occurrence of the two sentences.

### `TEACHER-Q43-003` — moderate — duplicated sentence in lesson prose (S05)
- **Location:** `content/lessons/lesson-4-3.json`, S05 section, first paragraph
- **Issue:** "With AWS DMS, at least one endpoint, source or target, must be on an AWS service, so it cannot migrate directly from one on-premises database to another on-premises database." appears twice back-to-back. Same likely cause as `TEACHER-Q43-002`.
- **Fix:** Delete the second occurrence of the sentence.

### `TEACHER-Q43-004` — low — reintroduced category-error-style distractor (2 occurrences)
- **Location:** `content/questions/q-saa-4-3-s03-mc.json` choice c: "Use DynamoDB on-demand as a drop-in relational replacement for SQL joins."; `content/questions/q-saa-4-3-k09-mc.json` choice c: "Use ElastiCache as the only durable system of record for all sessions."
- **Issue:** The task previously had ~24 category-error strawmen removed (a real service doing a job it was never built for, eliminable on sight with zero course knowledge). "DynamoDB as a drop-in replacement for SQL joins" is the same shape: DynamoDB's lack of joins is a headline, first-day fact, not something requiring K09/S03-level knowledge to rule out, so it doesn't test the stem's actual point (idle overprovisioning / elasticity). The ElastiCache-as-durable-store choice is milder — durability-vs-cache is genuinely taught content in K03, so I'd keep that one, but flag the DynamoDB/joins one.
- **Doc-verified fix:** Replace `s03-mc` choice c with a same-family distractor that fails only the *stated* requirement (idle-cost reduction while staying managed-relational), e.g. "Use RDS Reserved Instances sized for peak demand at all times" (real option, fails because it still pays for idle peak capacity — same failure mode as choice b, so pick a different angle) or "Use Aurora Standard provisioned at a fixed instance size with manual scheduled resizing" (real, fails because it still requires manual capacity planning, distinct from choice d's "fixed provisioned... manual resize windows" — ensure it doesn't duplicate choice d; recommend Lead Dev pick wording that differs from d's "schedule manual resize windows").

### Pattern note — "as the only" wording (not a hard-rule violation, flagging as requested)
Four distractors across the task use the phrase "as the only" (`q-saa-4-3-k02-mr` choice c, `q-saa-4-3-k08-mr` choice a, `q-saa-4-3-k09-mc` choice c, `q-saa-4-3-s01-mr` choice a). This isn't on the RULES.md banned-phrase list (`since/even though/which does not/despite/requiring/must/without changing`), but it's adjacent to the "self-explaining choices" family the prompt asked me to hunt for: an absolute qualifier ("only") is a classic test-taking tell that lets a strong test-taker eliminate the choice by pattern-matching absolutism rather than by database knowledge. None of these rise to a hard finding since AWS knowledge is still needed to know *why* "only" is wrong in each case (e.g., you need to know ElastiCache isn't durable), but if the Lead Dev is doing a wording pass, I'd suggest varying this phrasing so it isn't a repeated tell.

### RDS-family terms in distractors (known-allowed pattern, per instructions)
RDS-family terms (RDS, Aurora, MariaDB, etc.) show up as distractors in more than 3 of 22 questions when I count generously (`k07-mc`, `k09-mc`, `s01-mc`(indirectly), `s02-mc`, `s02-mr`, `s03-mc`), but the writer's own count (3/22 = 14%) was scoped to RDS-specific terms as a family for a *databases* lesson. I agree with the Lead Dev's position: RDS/Aurora/MariaDB terms are on-topic core content for this lesson, not off-topic padding, so I'm not opening a finding on this.

## (d) Numbers-in-keys verification

I checked every correct-answer choice and its rationale for numeric or countable claims:

- `q-saa-4-3-k04-mc` key a: "30-day automated retention" — 30 falls inside Aurora's documented 1–35 day automated-backup-retention range (claim-table row 9, verified round 1). Consistent.
- `q-saa-4-3-k05-mr` keys b, e: "one RCU ... item up to 4 KB" and "one WCU ... item up to 1 KB" — match `cite-saa-4-3-dynamodb-provisioned` exactly (claim-table rows 13–14, verified round 1) and the lesson's K05 prose. Consistent.
- `q-saa-4-3-s05-mc` key b / `q-saa-4-3-s05-mr` key e: "at least one endpoint ... on an AWS service" — matches `cite-saa-4-3-dms-introduction` (claim-table row 24, verified round 1). Consistent.
- All other correct-answer texts and rationales across the remaining 19 questions contain no numeric or countable claims (no percentages, unit counts, time windows, or thresholds appear in any other key/rationale).

No numeric discrepancies found in any key.

## Lesson additions requested

None. All teach-before-test gaps identified in round 1 are closed in prose (see (a)). The K07/S02 duplicate-fact problem in `TEACHER-Q43-001` is a question-authoring issue, not a missing-lesson-fact issue — the lesson already teaches homogeneous/heterogeneous migration in its own K07 section; the question just isn't testing it.

## Summary of new findings

- High: 1 (`TEACHER-Q43-001`)
- Moderate: 2 (`TEACHER-Q43-002`, `TEACHER-Q43-003`)
- Low: 1 (`TEACHER-Q43-004`)
- Pattern notes (no severity, informational): "as the only" wording; RDS-family-term count (agree, no finding).

Task 4.3: not yet
Overall: concerns
