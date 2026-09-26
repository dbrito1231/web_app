# Teacher round 2: task 4.1 (lesson fixes + 35 questions)

Saved by Lead Dev from the Teacher's reply (AGENTS.md: the Teacher does not write files).

**(a) Round-1 findings — Gone/not gone:**
- **TEACHER-L41-001** (K09 Intelligent-Tiering vs Lifecycle wording): **Gone.** New sentence names the mechanism ("a scheduled S3 Lifecycle rule instead of S3 Intelligent-Tiering") — clear for a student.
- **TEACHER-L41-002** (Glacier retrieval-time tiers missing): **Gone.** New K10 sentence gives Expedited/Standard/Bulk for Flexible Retrieval and Standard/Bulk for Deep Archive, matching the doc quotes. Clear and now correctly exercised by k10-mc, s08-mc, s08-mr.
- **TEACHER-L41-003** (EFS lifecycle day thresholds missing): **Gone.** New K10 sentence gives 30/90 days and correctly labels them as configurable defaults, not fixed limits — good, avoids a false-absolute claim.

**(b) Second-role check on AWS's round-1 findings:** AWS raised no lesson issues in round 1 per the writer's report; nothing to countersign.

**(c) Question review — teach-before-test on Writer B's new citations:** Both "multipart upload" (S01) and "S3 Batch Operations" (S01) are taught directly in lesson 4.1's S01 paragraph, and "EBS Elastic Volumes" is taught directly in S02. The three new citation files are doc-verification for facts already in the lesson body, not undisclosed lesson-addition requests — no gap.

**(d) Batch check** (`q1_batch_check.py 4-1`): all PASS except the expected WARN.
```
PASS: drillIds match questions
PASS: exam tips 21 for 21 objectives
WARN: lesson names retired/closed service 'Snowball' (correctly labeled, expected)
PASS: duplicate 6-word openings: []
PASS: longest-is-key 6/21 = 29%
PASS: MC key positions {a:6, b:6, c:5, d:4}
PASS: MR key slots {a:6, b:5, c:5, d:6, e:6}
```

**Per-question table** (all 35; objective fit / teach-before-test / difficulty / strawman / giveaway / rationale / fairness all checked — no issues found in any row):

| Question | Verdict |
|---|---|
| k01-mc, k02-mc, k02-mr, k03-mc, k04-mc, k05-mc, k05-mr, k06-mc, k07-mc, k08-mc, k08-mr, k09-mc, k10-mc, k11-mc, k11-mr | OK |
| s01-mc, s01-mr, s02-mc, s02-mr, s03-mc, s03-mr, s04-mc, s04-mr, s05-mc, s05-mr, s06-mc, s06-mr, s07-mc, s07-mr, s08-mc, s08-mr, s09-mc, s09-mr, s10-mc, s10-mr | OK |

Every key and distractor traces to lesson 4.1 text (post-fix), including the newly taught Glacier retrieval tiers and EFS day thresholds. No strawmen, no banned giveaway words, no letter cross-references, rationale addresses every choice by content. Difficulty is uniformly "applied" across all 35 — not a rule violation, just worth Lead Dev's awareness if question-bank variety is later desired.

Minor non-blocking note: k08-mc/k08-mr/s03-mc/s07-mc/s03-mr/s07-mr cite lesson-3.1/2.1 sources rather than a lesson-4.1-specific citation for the K08/S07 cost framing, since lesson 4.1 itself has no dedicated citation for that material — acceptable, as the underlying facts are doc-verified in those cited files and the cost-angle prose reuses lesson 3.1/2.1 mechanics by design.

No new issues (no TEACHER-Q41-### items).

Task 4.1: close.

Overall: approve.
