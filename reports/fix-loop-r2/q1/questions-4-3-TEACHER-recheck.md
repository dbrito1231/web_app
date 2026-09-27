# Teacher re-validation: task 4.3 (commit dcd1633)

## Findings from my round-2 report

- **TEACHER-Q43-001** (`q-saa-4-3-k07-mc` mistested S02's fact instead of K07's own content) — **Gone.** The rewritten stem (Cobalt Freight, self-managed Oracle, wants to drop commercial licensing, accepts schema/query rework) now tests homogeneous (choice a: Oracle-on-EC2, same engine/licensing) vs heterogeneous (choice c, the key: RDS PostgreSQL with planned schema/data-type/query conversion) migration selection — K07's own objective content. Choice b (Aurora MySQL-Compatible, "keep the existing SQL dialect unchanged") is a real, taught-inferable distractor: Oracle-to-MySQL-compatible is still heterogeneous, so dialect does not carry over unchanged. Choice d (rely on DMS alone to convert stored procedures) is grounded in the lesson's K07 line that heterogeneous moves "must evaluate SQL dialect differences, data types, and application compatibility" — DMS moves data, not code, so "DMS alone" is a fair miss. It does not duplicate S05: S05-mc tests the on-prem/on-prem endpoint-location rule, S05-mr tests classify-plus-endpoint-rule; this question is a distinct target-selection decision under a licensing/rework constraint. `objectiveIds` is `SAA-4.3-K07`, correctly matched. `key_text_diff.py 4-3 c063d52` confirms this is the only key-text change since the last closed baseline, which matches intent.

- **TEACHER-Q43-002 / TEACHER-Q43-003** (duplicated S02 and S05 sentences) — **Gone.** Re-read both sections in `content/lessons/lesson-4-3.json`: the MySQL/PostgreSQL discriminator now appears exactly once in S02, and the DMS one-endpoint-on-AWS sentence now appears exactly once in S05. Both read cleanly.
  - **Third instance you found and fixed (K05 "four times in a 24-hour rolling window", stated three ways):** confirmed gone. K05 now states the provisioned→on-demand switch limit exactly once: "You can switch from provisioned mode to on-demand mode up to **four times in a 24-hour rolling window**." I re-ran a full duplicate-sentence sweep over the whole lesson body (not just these three sections) and found zero repeated sentences anywhere in `lesson-4-3.json`. Good catch — that one was outside what I checked in round 2, and I confirm no further instances exist anywhere else in the file.

- **TEACHER-Q43-004** (`s03-mc` choice c reintroduced a category-error strawman: "DynamoDB as a drop-in relational replacement for SQL joins") — **Gone.** New choice c ("Use ElastiCache in front of a peak-sized cluster to absorb the traffic spikes") is a real option that fails only the stated idle-overprovisioning requirement, not an absurdity — a cache can genuinely offload reads, but the underlying cluster stays sized at peak, so the idle cost the stem asks to reduce is still paid. This is taught (K03 caching + S03/K09 provisioned-vs-elastic framing). One observation, not reopening the finding: this failure mode ("still paid for at peak") is close to choice b's failure mode (Aurora provisioned sized for peak at all times) — both distractors ultimately fail because the cluster stays peak-sized. They are worded differently and target different misconceptions (no-change vs cache-doesn't-fix-provisioning), so this clears the "not identical to another choice" bar, but if this question comes up again I'd suggest giving c a genuinely different failure axis (e.g., a commitment/reservation-based distractor) for sharper separation from b.

- **"as the only" pattern note** — confirmed reworded in all four locations (`k02-mr` choice c, `k08-mr` choice a, `k09-mc` choice c, `s01-mr` choice a); grep for the phrase across all 22 question files now returns zero matches. No key text changed in any of the four, consistent with `key_text_diff.py` reporting only `k07-mc`.

## Two changes I did not ask for

### 1. Read-replica / snapshot cap fix (matcher bug in `distractor_type_audit.py`)

Reviewed the five replacement choices:

- `q-saa-4-3-s02-mc` choice c: "Use MySQL on Amazon RDS with a larger instance class for extension compatibility." — Real, fails the stated requirement (extension/JSON support is an engine capability, not a compute-sizing lever) — taught by the S02 discriminator. Good.
- `q-saa-4-3-k09-mc` choice b: "Use a general-purpose managed MySQL instance with secondary indexes for key lookups." — Real feature, fails because it's still a relational-first approach for a stated key-value/no-joins access pattern — taught by K09's relational-vs-non-relational framing. Good.
- `q-saa-4-3-s03-mc` choice c: covered above under `TEACHER-Q43-004`. Good.
- `q-saa-4-3-k08-mc` choice d: "Restore the latest automated backup into a separate reporting instance." — Real action, fails because a restore is a one-time point-in-time copy that goes stale immediately and would have to be repeated, not a continuous read-offload path. This isn't spelled out verbatim in the K08 section, but it follows directly from the backup-vs-replica distinction taught across K04/K08 (backups/snapshots are point-in-time artifacts; only replicas continuously receive updates). Acceptable — a candidate who has read K04 and K08 can eliminate it on content, not on absurdity.
- `q-saa-4-3-k08-mr` choice d: "Use a larger writer instance class as the read-scaling mechanism." — Real, fails because it adds capacity to the single writer endpoint rather than providing a mechanism distinct from the availability design (the stem explicitly asks for two *distinct* mechanisms) — taught. Good.

All five are real AWS options, each fails exactly one stated requirement for a reason the lesson supports, and none is a category-error strawman. `distractor_type_audit.py 4-3` now shows a 14% ceiling (RDS, ElastiCache, Multi-AZ, read replica, Aurora, DMS all at 3/22) with no type over the 15% cap. Confirmed by direct tool run, not just the writer's report.

### 2. Six rewritten rationales — re-read for teach-before-test

`k07-mc`, `k08-mc`, `k08-mr`, `k09-mc`, `s02-mc`, `s03-mc` — all re-read in full above alongside their choice text. Every claim in each rationale traces to lesson content: K07 homogeneous/heterogeneous framing and its "must evaluate SQL dialect... application compatibility" line; K08's read-replica-is-asynchronous / standby-is-not-a-read-endpoint contrast; K09's relational-vs-non-relational and cache-is-not-durable framing; S02's MySQL/PostgreSQL discriminator; S03's Aurora Serverless v2 elasticity vs peak-sized-cluster framing. No rationale references choice letters, and none introduces a fact absent from the lesson. All clear.

## Verification performed directly (not just trusting the writer's report)

- Ran `content_lint.py`: PASS.
- Ran `distractor_type_audit.py 4-3`: PASS, top type 14% (RDS/ElastiCache/Multi-AZ/read replica/Aurora/DMS all tied at 3/22).
- Ran `q1_batch_check.py 4-3`: PASS on all checks, including MR key-set distribution (no combination over 12%) and MC longest-is-key (21%).
- Ran a full duplicate-sentence sweep over the entire `lesson-4-3.json` body (not limited to S02/S05/K05): zero repeats found.
- Grepped all 22 question files for "as the only": zero matches.
- Confirmed all citation IDs referenced by the 22 question files resolve to existing citation files (checked in round 2, unaffected by this diff).

## Gone / not-gone summary

- TEACHER-Q43-001: Gone
- TEACHER-Q43-002: Gone
- TEACHER-Q43-003: Gone (plus the K05 triple-repeat you found and fixed independently: confirmed gone, and confirmed no further duplicate sentences exist anywhere else in the lesson)
- TEACHER-Q43-004: Gone
- "as the only" pattern note: Gone (all four reworded, no key text changed)
- Read-replica/snapshot cap fix (unrequested): reviewed, all five replacement distractors are real, each fails one stated requirement, none is a strawman — approved
- Six rewritten rationales (unrequested): reviewed, all teach-before-test compliant — approved

Task 4.3: close
Overall: approve
