# Teacher review — task 2.2 questions (32, as of commit `93b13b4`)

Saved by Lead Dev from the Teacher's reply (AGENTS.md: the Teacher does not write files).

**Scope:** all 32 `content/questions/q-saa-2-2-*.json` files against `content/lessons/lesson-2-2.json`, author notes (impl-A/impl-B), and the AWS review (`questions-2-2-AWS.md`, "not yet"/concerns) plus Lead Dev's fixes in `042688e` and `93b13b4`.

## Per-question table

| ID | Objective fit | Teach-before-test | Difficulty | Strawman check | No giveaway wording | Rationale covers all | Fairness |
|---|---|---|---|---|---|---|---|
| k01-mc | OK | OK | OK | OK | OK | OK | OK |
| k02-mc | OK | OK | OK | OK | OK | OK | OK |
| k03-mc | OK | OK | OK | OK | OK | OK | OK |
| k03-mr | OK | OK | OK | OK | OK | OK | OK |
| k04-mc | OK | OK | OK | OK | OK | OK | OK |
| k05-mc | OK | OK | OK | OK | OK | OK | OK |
| k06-mc | OK | OK | OK | OK | OK | OK | OK |
| k06-mr | OK | OK | OK | OK | OK | OK | OK |
| k07-mc | OK | OK | OK | OK | OK | OK | OK |
| k08-mc | OK | OK | OK | OK | OK | OK | OK (see TEACHER note: relies on `cite-saa-2-1-alb-cross-zone`, now correctly linked from the lesson per AWS-Q22-002 fix) |
| k09-mc | OK | OK | OK | OK | OK | OK | OK |
| k09-mr | OK | OK | OK | OK | OK | OK | OK |
| k10-mc | OK | OK | OK | OK | OK | OK | OK |
| k11-mc | OK | OK | OK | OK | OK | OK | OK |
| k12-mc | OK | OK | OK | OK | OK | OK | OK |
| k12-mr | OK | OK | OK | OK | OK | OK | OK |
| s01-mc | OK | OK | OK | OK | OK | OK | OK |
| s01-mr | OK | OK | OK | OK | OK | OK | OK |
| s02-mc | OK | OK | OK | OK | OK | OK | OK |
| s02-mr | OK | OK | OK | OK | OK | OK | OK |
| s03-mc | OK | OK | OK | OK | OK | OK | OK |
| s03-mr | OK | OK | OK | OK | OK | OK | OK |
| s04-mc | OK | OK | OK | OK | OK | OK | OK (see AWS-Q22-003, informational only) |
| s04-mr | OK | OK | OK | OK | OK | OK | OK |
| s05-mc | OK | OK | OK | OK | OK | OK | OK (see TEACHER-Q22-001, Low) |
| s05-mr | OK | OK | OK | OK | OK | OK | OK |
| s06-mc | OK | OK | OK | OK | OK | OK | OK |
| s06-mr | OK | OK | OK | OK | OK | OK | OK |
| s07-mc | OK | OK | OK | OK | OK | OK | OK — AWS-Q22-001 confirmed fixed; stem now says "without depending on DNS changes reaching clients," which cleanly rules out Route 53 failover (choice b) |
| s07-mr | OK | OK | OK | OK | OK | OK | OK |
| s08-mc | OK | OK | OK | OK | OK | OK | OK |
| s08-mr | OK | OK | OK | OK | OK | OK | OK |

Every key and every distractor across all 32 files traces to a specific sentence in `lesson-2-2.json` (K01–K12/S01–S08). No self-explaining wording remains, no cross-choice references, no choice describes a nonexistent or retired feature.

## Batch metrics (my own script over all 32 files)

| Check | Result |
|---|---|
| Distractor-type max share | RDS Proxy (k09-mc, k09-mr, s07-mc, s07-mr) = 4/32, at the cap, not over |
| Longest-is-key (MC) | 5/20 = 25.0% (≤35% required) |
| MC key positions | a:5, b:5, c:5, d:5 — perfectly even |
| MR key-slot positions | a:6, b:4, c:4, d:5, e:5 |
| Unique 6-word stem openings | 32/32, 0 duplicates |
| Letter references in rationale | 0 |
| Objective text pasted verbatim | 0 (checked against `content/objectives/saa_c03.json`) |
| Citations resolve | 27 distinct `citationIds` used, all resolve to files in `content/citations/` |
| `mcpStatus`/`reviewedOn` | 32/32 `verified` / `2026-09-26` |
| MR count | 12 of 32 (k03, k06, k09, k12, s01–s08 each have an mr) |
| `selectCount` matches `correctAnswerIds` length | 32/32 |
| lesson `drillIds` lists all 32 | yes, exact match, no extras/missing |
| `python scripts\content_lint.py` | PASS (`questions 429 aws 310 tf 119`) |

## Second-role checks

- **AWS-Q22-001** (s07-mc DNS-failover ambiguity): confirmed fixed. The stem now adds "without depending on DNS changes reaching clients," which the rationale correctly uses to reject Route 53 failover routing (choice b) on TTL-propagation grounds, not just a fleet-size assumption. Closed.
- **AWS-Q22-002** (missing lesson citation link): confirmed fixed. `cite-saa-2-1-alb-cross-zone` is now in `lesson-2-2.json`'s `citationIds` array (line 92), matching the citation `q-saa-2-2-k08-mc.json` already used. Closed.
- **AWS-Q22-003** (NAT-gateway-per-AZ tested three times: k03-mc, k03-mr, s04-mc): I agree this is worth a note but not a blocker — the batch cap (4/32) isn't exceeded and each of the three frames the fact differently (diagnose-the-cause / select-two-fixes / pick-the-fix-for-a-named-SPOF). My recommendation: for a future refresh, retarget **s04-mc** to test a different SPOF the lesson names in its S04 list — specifically **"a deployment confined to a single Availability Zone"** (e.g., an ALB/Auto Scaling group whose subnets never span more than one AZ), rather than the NAT-gateway case s04-mr's sibling questions already own. That SPOF is named explicitly in the lesson's S04 paragraph and isn't tested anywhere else in the batch, so swapping it in would remove the k03/s04 overlap without losing coverage.

## New issue

**TEACHER-Q22-001 (Low)** — `content/questions/q-saa-2-2-s05-mc.json`, `citationIds`.
The array includes `cite-saa-2-2-rds-multiaz`, but none of the four choices or the rationale mentions RDS Multi-AZ, read replicas being the only database-adjacent distractor (choice d). The citation appears to be a leftover and doesn't back anything actually tested in this question. Not a factual problem and doesn't affect the key or any distractor's correctness.
Exact fix: remove `"cite-saa-2-2-rds-multiaz"` from `q-saa-2-2-s05-mc.json`'s `citationIds` array; no other change needed.

**Task 2.2: close**

**Overall: approve**
