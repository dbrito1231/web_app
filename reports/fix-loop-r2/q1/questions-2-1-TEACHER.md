# Teacher review — task 2.1 questions (35, as of commit `e89e1b5`)

Saved by Lead Dev from the Teacher's reply (AGENTS.md: the Teacher does not write files).

**Scope:** all 35 `content/questions/q-saa-2-1-*.json` files, `content/lessons/lesson-2-1.json`, author notes (impl-A/B), Lead Dev pre-review, lesson additions (`lesson-2-1-impl.md`), and the AWS review/approval.

### Per-question table

| ID | Objective fit | Teach-before-test | Difficulty | Strawman check | No giveaway wording | Rationale covers all | Fairness |
|---|---|---|---|---|---|---|---|
| k01-mc | OK | OK | OK | OK | OK | OK | OK |
| k02-mc | OK | OK | OK | OK | OK | OK | OK |
| k02-mr | OK | OK | OK | OK | OK | OK | OK |
| k03-mc | OK | OK | OK | OK | OK | OK | OK |
| k04-mc | OK | OK | OK | OK | OK | OK | OK |
| k05-mc | OK | OK | OK | OK | OK | OK | OK |
| k05-mr | OK | OK | OK | OK | OK | OK | OK |
| k06-mc | OK | OK | OK | OK (3 resize distractors now distinguishable: template resize, no-policy trap, consolidation) | OK | OK | OK |
| k07-mc | OK | OK | OK | OK | OK | OK | OK |
| k08-mc | OK | OK | OK | OK | OK | OK | OK |
| k08-mr | OK | OK | OK | OK | OK | OK | OK |
| k09-mc | OK | OK | OK | OK | OK | OK | OK |
| k10-mc | OK | OK | OK | OK | OK | OK | OK |
| k11-mc | OK | OK | OK | OK | OK | OK | OK |
| k11-mr | OK | OK | OK | OK | OK (absolutes removed) | OK | OK |
| k12-mc | OK | OK | OK | OK | OK | OK | OK |
| k13-mc | OK | OK | OK | OK | OK | OK | OK |
| k14-mc | OK | OK | OK | OK | OK | OK | OK |
| k14-mr | OK | OK | OK | OK | OK | OK | OK |
| k15-mc | OK | OK | OK | OK | OK | OK | OK |
| k16-mc | OK | OK | OK | OK | OK | OK | OK |
| s01-mc | OK | OK | OK | OK | OK | OK | OK |
| s01-mr | OK | OK | OK | OK | OK | OK | OK |
| s02-mc | OK | OK | OK | OK | OK | OK | OK |
| s02-mr | OK | OK | OK | OK | OK | OK | OK |
| s03-mc | OK | OK | OK | OK | OK | OK | OK |
| s03-mr | OK | OK | OK | OK | OK | OK | OK |
| s04-mc | OK | OK | OK | OK | OK | OK | OK |
| s04-mr | OK | OK | OK | OK | OK (self-explaining "nothing to containerize" clause removed) | OK | OK |
| s05-mc | OK | OK | OK | OK | OK | OK | OK |
| s05-mr | OK | OK | OK | OK | OK (absolutes removed) | OK | OK |
| s06-mc | OK | OK | OK | OK | OK (self-explaining EBS clause removed) | OK | OK |
| s06-mr | OK | OK | OK | OK (Global Accelerator swapped for a plausible-per-half distractor per LD-Q21-003) | OK | OK | OK |
| s07-mc | OK | OK | OK | OK | OK | OK | OK |
| s07-mr | OK | OK | OK | OK | OK | OK | OK |

Every distractor traces to a real, current AWS service or behavior; the three previously-flagged issue classes (LD-Q21-001 strawmen, LD-Q21-002 giveaway wording, LD-Q21-003 loosely-paired MR halves) are all resolved in the files as they stand.

### Batch metrics (own script over all 35 files)

| Check | Result |
|---|---|
| Distractor-type max share | ≤5/35 for every category checked (self-managed-server family 5, poll-on-interval family 5, vertical-resize 3, standing/always-on 3) — at or under the 5-of-35 cap, and each cap-hitting family splits into distinct sub-ideas (self-managed SFTP ×2, self-managed K8s ×2, EC2 Spot ×1) so no single repeated trick recurs more than twice |
| Longest-is-key (MC) | 5/23 = 21.7% (≤35% required) |
| MC key positions | a:6 b:6 c:6 d:5 |
| MR key positions | a:5 b:5 c:4 d:5 e:5 |
| Unique 6-word stem openings | 35/35, 0 duplicates |
| Letter references in rationale | 0 |
| Objective text pasted verbatim | 0 matches |
| Citations resolve, `verified`/`2026-09-26` | 35/35 questions, 26 distinct citationIds, all resolve, all `mcpStatus: verified`, `reviewedOn: 2026-09-26` |
| MR stems state the count | 12/12 say "(Select TWO.)" |
| `selectCount` matches `correctAnswerIds` length | 35/35 |
| lesson `drillIds` lists all 35 | yes, exact match, no extras/missing |
| `content_lint.py` | PASS (`questions 429 aws 310 tf 119 / labs 21+21 / lessons 23`) |

### Second-role checks

- **AWS-Q21-001** (K08 exam tip naming retired Copilot): confirmed fixed — `"Copilot"` no longer appears anywhere in `lesson-2-1.json`.
- **AWS-Q21-002** (`cite-saa-2-1-k-global-accelerator` missing from lesson `citationIds`): confirmed fixed — it is now in the array, and it also correctly resolves as a citation file and is used by `q-saa-2-1-k07-mc.json`.
- **Six lesson additions** (AppConfig, EventBridge Scheduler, MGN, Classic LB, EBS Multi-Attach, SQS-vs-workflow): read in place in the current lesson body — each sits directly next to the concept it supports (K02/K05/K08/K09/K13/K16 respectively), is one to two sentences, doesn't disrupt the surrounding paragraph, and each has a matching exam tip or citation. Spot-verified two of the newer facts directly against AWS docs via MCP: EBS Multi-Attach is confirmed "up to 16 Nitro-based instances... same Availability Zone" for both io1 and io2 (lesson/k13-mc text is accurate); Classic Load Balancer is confirmed to have no path-based routing capability (round-robin TCP / least-outstanding-requests HTTP only), matching K09's added sentence.

### New issues

None. No new TEACHER-Q21-### items — I found no factual errors, no teach-before-test gaps, no fairness problems, and no unresolved items beyond what AWS and Lead Dev already closed.

**Task 2.1: close**

**Overall: approve**
