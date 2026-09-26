# Teacher round 2: task 3.3 (lesson fixes + 21 questions)

Saved by Lead Dev from the Teacher's reply (AGENTS.md: the Teacher does not write files).

**(a) TEACHER-L33-001:** Gone. Confirmed independently: I re-fetched `AmazonRDS/latest/UserGuide/USER_ReadRepl.html` in Round 1 and it contains "A *read replica* is a read-only copy of a DB instance" and "Amazon RDS copies them asynchronously to the read replica" as visible page prose — the claim table and `cite-saa-3-3-rds-read-replicas` now use these, not the search-index glossary blurb.

**(b) Second-role check:**
- AWS-L33-001 (gp3 threshold wording): Gone — confirmed in current `lesson-3-3.json` K04.
- AWS-L33-002 (TTL quote): Gone — confirmed verbatim quote now in claim table.
- AWS-L33-003 (Optimized Reads family): Gone — confirmed K04 lists all five families.
- AWS-L33-004 (Aurora Serverless quote/URL mismatch): Gone — accept AWS's fix (didn't re-fetch the how-it-works page myself, no reason to doubt).
- AWS-L33-005 (DMS/SCT citation scope, informational): Gone, no fix needed, agree.
- AWS-Q33-001 (`k03-mc` distractor d, Aurora-specific wording removed, replaced with engine-agnostic "Multi-AZ DB instance" distractor, citing `cite-saa-2-2-rds-multiaz`): **Acceptable as fixed.** The wrongness reason ("the standby does not serve traffic") is prior-taught material from lesson 2.2 K06, properly cited, and lesson 3.3 already leans on this same 2.2 fact elsewhere (K07's "don't confuse it with Multi-AZ automatic failover (task 2.2, K06)"). No lesson 3.3 sentence needed.

**(c)/(d) Per-question review**

| Question | Objective fit | Teach-before-test | Difficulty | Strawman/giveaway | Rationale/fairness |
|---|---|---|---|---|---|
| k01-mc | Yes | Yes | Fair | None | Fair |
| k01-mr | Yes | Yes | Fair | None | Fair |
| k02-mc | Yes | Yes | Fair | None | Fair |
| k03-mc | Yes | Yes (now cited) | Fair | None | Fair |
| k04-mc | Yes | Yes | Fair | None | Fair |
| k04-mr | Yes | Yes | Fair | None | Fair |
| k05-mc | Yes | Yes | Fair | None | Fair |
| k06-mc | Yes | Yes | Fair | None | Fair |
| k07-mc | Yes | See TEACHER-Q33-001 | Fair | None | Fair |
| k07-mr | Yes | Yes | Fair | None | Fair |
| k08-mc | Yes | Yes | Fair (easy but on-objective) | None | Fair |
| s01-mc | Yes | Yes | Fair | None | Fair |
| s01-mr | Yes | Yes | Fair | None | Fair |
| s02-mc | Yes | Yes | Fair | None | Fair |
| s02-mr | Yes | Yes | Fair | None | Fair |
| s03-mc | Yes | Yes | Fair | None | Fair |
| s03-mr | Yes | Yes (dual-need, each distractor answers one need) | Fair | None | Fair |
| s04-mc | Yes | Yes | Fair | None | Fair |
| s04-mr | Yes | Yes (dual-need, valid) | Fair | None | Fair |
| s05-mc | Yes | Yes | Fair | None | Fair |
| s05-mr | Yes | Yes (dual-need, valid) | Fair | None | Fair |

No giveaway words, no strawmen (no manual/anti-pattern distractors), no letter-references in rationales, no choice referring to another choice, found in any of the 21 — confirmed by direct read of all files.

**Issues**

- **TEACHER-Q33-001** (low, `q-saa-3-3-k07-mc`, distractor b: "Enable a Multi-AZ DB cluster deployment with two additional readable standbys"): the rationale's wrongness reason ("a Multi-AZ DB cluster caps out at two readable standbys, short of the several more readers asked for here") is a lesson-2.2 fact (K06), same class of gap as AWS-Q33-001, but unlike the fixed `k03-mc` this question's `citationIds` only lists `cite-saa-3-3-aurora-scalability` — the 2.2 fact is uncited. Fix: add `cite-saa-2-2-rds-multiaz-cluster` (already exists, note: "a Multi-AZ DB cluster keeps a writer and two readable standby instances across three separate Availability Zones") to `q-saa-3-3-k07-mc`'s `citationIds`, matching the precedent set for `k03-mc`.

Task 3.3: not yet (pending TEACHER-Q33-001, a one-line citation fix)

Overall: concerns
