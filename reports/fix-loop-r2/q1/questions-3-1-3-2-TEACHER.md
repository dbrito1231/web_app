# Teacher review — Tasks 3.1 (8) and 3.2 (16) questions, commit e030fd2

Saved by Lead Dev from the Teacher's reply (AGENTS.md: the Teacher does not write files).

### Batch check results
- `q1_batch_check.py 3-1` → **RESULT: WARN** (only the two labelled retired-service WARNs: `FSx File Gateway` in `k01-mc`, `Snowball` in `k01-mr`, plus 3 lesson-body mentions of Snowball/FSx File Gateway that are all explicitly EOL-labelled — expected, no action).
- `q1_batch_check.py 3-2` → **RESULT: PASS**.

### Second-role check
- **AWS-Q31-001** (Snowball diversity fix, `q-saa-3-1-s02-mr` choice b → S3 Transfer Acceleration): applied exactly as specified — choice text, rationale clause, and `citationIds` (dropped `cite-saa-3-1-snowball-edge-eol`, added `cite-saa-3-1-s3-transfer-acceleration`) all match. Accurate and clear. Gone.
- **AWS-Q32-001** (Reserved-concurrency diversity fix, `q-saa-3-2-k05-mr` choice a → function timeout): applied exactly as specified — choice text, rationale clause, `citationIds` (added `cite-saa-3-2-lambda-timeout`) all match. Gone.
- **Lesson 3.2 K05 timeout sentence** ("Each function also has a separate configurable timeout, up to 15 minutes... raising it does not pre-initialize anything and has no effect on cold-start latency."): accurate (matches AWS Lambda timeout docs) and clearly worded; it also incidentally backs `q-saa-3-2-k01-mc`'s "Lambda's execution limits" rationale clause, so teach-before-test holds there too.

### Closed-service distractor fairness (3.1)
`FSx File Gateway` (`k01-mc` choice d) and `Snowball` (`k01-mr` choice b): both fair. Lesson K01 explicitly states each is "no longer available to new customers" and names the current alternative; the exam tip repeats the Snow Family point. Each choice/rationale also independently labels the EOL status, and each fails the stem on a stated functional ground (wrong protocol/wrong transfer pattern) independent of its EOL status. Diversity is now resolved post-fix (1 use each of 8, 12.5%, under the 15% cap).

### Per-question table

| ID | Objective fit | Teach-before-test | Strawman | Giveaway wording | Rationale | Fairness | Verdict |
|---|---|---|---|---|---|---|---|
| q-saa-3-1-k01-mc | OK | OK | None | None | Covers all 4 | Fair | OK |
| q-saa-3-1-k01-mr | OK | OK | None | None | Covers all 5 | Fair | OK |
| q-saa-3-1-k02-mc | OK | OK | None | None | Covers all 4 | Fair | OK |
| q-saa-3-1-k03-mc | OK | OK | None | None | Covers all 4 | Fair | OK |
| q-saa-3-1-s01-mc | OK | OK | None | None | Covers all 4 | Fair | OK |
| q-saa-3-1-s01-mr | OK | OK | None | None | Covers all 5 | Fair | OK |
| q-saa-3-1-s02-mc | OK | OK | None | None | Covers all 4 | Fair | OK |
| q-saa-3-1-s02-mr | OK | OK (fix applied) | None | None | Covers all 5 | Fair | OK |
| q-saa-3-2-k01-mc | OK | OK | None | None | Covers all 4 | Fair | OK |
| q-saa-3-2-k02-mc | OK | OK | None | None | Covers all 4 | Fair | OK |
| q-saa-3-2-k02-mr | OK | OK | None | None | Covers all 5 | Fair | OK |
| q-saa-3-2-k03-mc | OK | OK | None | None | Covers all 4 | Fair | OK |
| q-saa-3-2-k04-mc | OK | OK | None | None | Covers all 4 | Fair | OK |
| q-saa-3-2-k05-mc | OK | OK | None | None | Covers all 4 | Fair | OK |
| q-saa-3-2-k05-mr | OK | OK (fix applied) | None | None | Covers all 5 | Fair | OK |
| q-saa-3-2-k06-mc | OK | OK | None | None | Covers all 4 | Fair | OK |
| q-saa-3-2-s01-mc | OK | OK | None | None | Covers all 4 | Fair | OK |
| q-saa-3-2-s01-mr | OK | OK | None | None | Covers all 5 | Fair | OK |
| q-saa-3-2-s02-mc | OK | OK | None | None | Covers all 4 | Fair | OK |
| q-saa-3-2-s02-mr | OK | OK | None | None | Covers all 5 | Fair | OK |
| q-saa-3-2-s03-mc | OK | OK | None | None | Covers all 4 | Fair | OK |
| q-saa-3-2-s03-mr | OK | OK | None | None | Covers all 5 | Fair | OK |
| q-saa-3-2-s04-mc | OK | OK | None | None | Covers all 4 | Fair | OK |
| q-saa-3-2-s04-mr | OK | OK | None | None | Covers all 5 | Fair | OK |

No new TEACHER-Q31/Q32 issues found.

Task 3.1: close
Task 3.2: close
Overall: approve
