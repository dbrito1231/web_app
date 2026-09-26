# Task 3.3 AWS review -- Round 2

Reviewer: Senior AWS Solutions Architect (read-only). Lesson fix commit `4eb7f84`;
questions in `content/questions/q-saa-3-3-*.json` (21 files), notes in
`reports/fix-loop-r2/q1/questions-3-3-impl.md`.

## (a) AWS-L33 findings -- Gone or not gone

Verified directly against the current `content/lessons/lesson-3-3.json` body (not just
the impl report's claim):

- **AWS-L33-001** (gp3 "independent of volume size"): **Gone.** K04 now reads "...a
  baseline of 3,000 IOPS and 125 MiB/s up to a per-engine storage-size threshold, above
  which RDS stripes the volume across four volumes and the baseline rises to 12,000 IOPS
  and 500 MiB/s..." -- matches `CHAP_Storage.html`.
- **AWS-L33-002** (TTL claim-table quote was a paraphrase): **Gone.** Claim table row now
  quotes "By adding a time to live (TTL) value to each write, you can have the advantages
  of each strategy" verbatim from `Strategies.html`.
- **AWS-L33-003** (instance-class family list incomplete): **Gone.** K04 now lists all
  five families including "Optimized Reads," matching `Concepts.DBInstanceClass.Types.html`.
- **AWS-L33-004** (Aurora Serverless scale-to-zero quote/URL mismatch): **Gone.** Claim
  table quote replaced with "With the minimum capacity of 0 ACUs, the cluster will scale
  to 0 when there is no workload running," which is on the cited how-it-works page.
- **AWS-L33-005** (DMS/SCT citation scoped to SQL Server guide, informational): **Gone**
  (no fix needed; noted, left as is by design).

## (b) Second-role check: TEACHER-L33-001

Re-fetched `AmazonRDS/latest/UserGuide/USER_ReadRepl.html` directly. Confirmed both
replacement quotes are exact, verbatim page text: "A read replica is a read-only copy of
a DB instance." (opening sentence) and "...Amazon RDS copies them asynchronously to the
read replica." (How read replicas work). The claim-table row and
`cite-saa-3-3-rds-read-replicas` now cite real page prose, not a search-tool glossary
blurb. **TEACHER-L33-001: Gone**, confirmed by second role.

## (c)/(d) Per-question review

| Question | Key correct/best | Distractors real, wrong-for-one-reason | Rationale accurate | Stem unambiguous | Citations fit | Numbers verified |
| --- | --- | --- | --- | --- | --- | --- |
| k01-mc | Yes (a) | Yes | Yes | Yes | Yes | n/a |
| k01-mr | Yes (a,c) | Yes | Yes | Yes | Yes | n/a |
| k02-mc | Yes (b) | Yes | Yes | Yes | Yes | n/a |
| k03-mc | Yes (c) | Yes, but see AWS-Q33-001 | Yes | Yes | Yes | n/a |
| k04-mc | Yes (d) | Yes | Yes | Yes | Yes | n/a |
| k04-mr | Yes (b,d) | Yes | Yes | Yes | Yes | n/a |
| k05-mc | Yes (a) | Yes | Yes | Yes | Yes | n/a |
| k06-mc | Yes (b) | Yes | Yes | Yes | Yes | n/a |
| k07-mc | Yes (c) | Yes | Yes | Yes | Yes | 15-replica cap not itself in this key's text, n/a |
| k07-mr | Yes (a,b) | Yes | Yes | Yes | Yes | "up to 15" verified against `aurora-features-scalability.html` |
| k08-mc | Yes (d) | Yes | Yes | Yes | Yes | 6/20/25 date verified against Timestream EOL page |
| s01-mc | Yes (a) | Yes | Yes | Yes | Yes | n/a |
| s01-mr | Yes (b,e) | Yes | Yes | Yes | Yes | n/a |
| s02-mc | Yes (b) | Yes | Yes | Yes | Yes | n/a |
| s02-mr | Yes (a,d) | Yes | Yes | Yes | Yes | n/a |
| s03-mc | Yes (c) | Yes | Yes | Yes | Yes | "up to 15 low-lag replicas" verified |
| s03-mr | Yes (a,b) | Yes | Yes | Yes | Yes | n/a |
| s04-mc | Yes (d) | Yes | Yes | Yes | Yes | n/a |
| s04-mr | Yes (a,b) | Yes | Yes | Yes | Yes | n/a |
| s05-mc | Yes (a) | Yes | Yes | Yes | Yes | n/a |
| s05-mr | Yes (a,b) | Yes | Yes | Yes | Yes | n/a |

`q1_batch_check.py 3-3`: PASS on every metric (drillIds match, 13/13 exam tips, 0
duplicate 6-word openings, longest-is-key 23%, MC key positions {a:4,b:3,c:3,d:3}, MR key
slots {a:6,b:6,c:1,d:2,e:1}). `content_lint.py`: PASS (429 questions, 21+21 labs, 23
lessons). No banned giveaway words (`since`, `even though`, `which does not`, `despite`,
`requiring`, `must`, `without changing`) found in any choice text. No choice refers to
another choice.

## Issues

- **AWS-Q33-001** (low, `q-saa-3-3-k03-mc`, distractor d): The stem never states the
  database engine is Aurora ("An ingestion pipeline ... writes ... to its relational
  database"), but distractor d says "Point reporting queries at the Aurora reader
  endpoint instead of the primary instance," presupposing Aurora specifically. It is
  still wrong for the stated reason (a read-side fix for a write bottleneck) so the key
  and rationale are not affected, but the distractor references a feature not established
  as available in this scenario. Fix: reword distractor d to "Add a read replica and
  point reporting queries at it instead of the primary instance" so it matches the
  engine-agnostic stem, or add "...running on Amazon Aurora" to the stem.
- **AWS-Q33-002** (informational, cross-question overlap): `k07-mc`, `k07-mr`, `s01-mr`,
  and `s03-mc`/`s03-mr` all draw on the same Aurora Replica facts (15-replica cap, shared
  storage, reader endpoint). Each tests a different objective (K07 mechanism selection and
  true/false recall vs. S01 post-scaling operations vs. S03 engine choice), so this is not
  a same-objective duplicate under the "no two questions test the identical fact" rule, but
  it is worth flagging since a student who misses the underlying Aurora-Replica facts will
  likely miss several questions at once. No fix required.

Task 3.3: close

Overall: approve
