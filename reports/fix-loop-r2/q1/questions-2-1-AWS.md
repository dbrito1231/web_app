# AWS Solutions Architect review — task 2.1 questions (35 rewritten)

Reviewer: Senior AWS Solutions Architect role (read-only). Date: 2026-09-26.
Scope: the 35 files `content/questions/q-saa-2-1-*.json` as of commit `f8709a9`, written against
`content/lessons/lesson-2-1.json`. Author notes: `reports/fix-loop-r2/q1/questions-2-1-impl-A.md`
(k*, writer A) and `-impl-B.md` (s*, writer B). Lead Dev pre-review:
`reports/fix-loop-r2/q1/questions-2-1-LEADDEV.md` (three findings — strawman distractors,
self-explaining/giveaway choices, loosely paired MR halves — all marked fixed by both writers in
the same commit range that produced the files reviewed here). Quality bar: the approved task 1.3
set (`reports/fix-loop-r2/q1/questions-1-3-AWS.md`).

Method:
- Solved each question cold against its stated constraints before checking the listed key.
- Verified every new or load-bearing fact via the AWS Documentation MCP (`search_documentation` /
  `read_documentation`): AWS AppConfig (gradual rollout + CloudWatch-alarm automatic rollback, no
  credential-rotation capability of its own); Amazon EventBridge Scheduler (one-time `at()` and
  recurring schedules, time-driven vs. a rule); AWS Application Migration Service / MGN
  (continuous block-level replication via the Replication Agent, rehosts to EC2, produces no
  container image); Classic Load Balancer (round-robin TCP / least-outstanding-requests HTTP,
  no path-based routing capability); Amazon EBS Multi-Attach (`io1`/`io2` only, up to 16
  Nitro-based instances, single Availability Zone, requires a clustered file system — confirmed
  verbatim against `ebs-volumes-multi.html`); AWS Step Functions Standard vs. Express (Standard:
  up to one year, exactly-once, full execution history; Express: up to five minutes,
  at-least-once — confirmed verbatim against `choosing-workflow-type.html`); Amazon SQS message
  retention. The remaining facts (API Gateway REST/HTTP/WebSocket split, ElastiCache Redis/
  Memcached, EventBridge rules/default bus, ALB/NLB/GWLB, App2Container, RDS read replica vs.
  Multi-AZ, ECS vs. EKS, Lambda/Fargate limits, SQS FIFO/standard, SNS fan-out, storage types,
  Auto Scaling policy types) were carried over from the already-approved `lesson-2-1-AWS.md`
  review and re-checked against the lesson body and this batch's rationale text for consistency;
  none has changed or been contradicted.
- Searched every file for "Copilot" to confirm the retired AWS Copilot CLI was not reintroduced
  as a distractor (it is not — see finding AWS-Q21-001 below for a related but different issue).
- Cross-checked all 33 `citationIds` used across the 35 files against `content/citations/` (all
  resolve) and against `content/lessons/lesson-2-1.json`'s own `citationIds` array (one gap found
  — AWS-Q21-002).
- Counted distractor-type reuse across both writers' tables (impl-A's 63-instance table + impl-B's
  35-instance table) and spot-checked the higher-frequency candidates (polling-on-interval,
  vertical-resize, standing/always-on compute, continuous Fargate) by hand; none exceeds 5 of 35.
- No AWS calls were made, no servers were started, no files other than this report were written.

## Per-question results

| ID | Key correct | Distractors OK | Rationale accurate | Verdict |
|---|---|---|---|---|
| k01-mc | y (a) | y | y | Pass |
| k02-mc | y (b) | y | y | Pass |
| k02-mr | y (a,c) | y | y | Pass |
| k03-mc | y (c) | y | y | Pass |
| k04-mc | y (d) | y | y | Pass |
| k05-mc | y (a) | y | y | Pass |
| k05-mr | y (b,d) | y | y | Pass |
| k06-mc | y (b) | y | y | Pass |
| k07-mc | y (c) | y | y | Pass (see AWS-Q21-002, citation-linkage only) |
| k08-mc | y (d) | y | y | Pass |
| k08-mr | y (a,e) | y | y | Pass |
| k09-mc | y (a) | y | y | Pass |
| k10-mc | y (b) | y | y | Pass |
| k11-mc | y (c) | y | y | Pass |
| k11-mr | y (c,e) | y | y | Pass |
| k12-mc | y (d) | y | y | Pass |
| k13-mc | y (a) | y | y | Pass |
| k14-mc | y (b) | y | y | Pass |
| k14-mr | y (b,d) | y | y | Pass |
| k15-mc | y (c) | y | y | Pass |
| k16-mc | y (d) | y | y | Pass |
| s01-mc | y (a) | y | y | Pass |
| s01-mr | y (a,d) | y | y | Pass |
| s02-mc | y (b) | y | y | Pass |
| s02-mr | y (b,e) | y | y | Pass |
| s03-mc | y (c) | y | y | Pass |
| s03-mr | y (a,c) | y | y | Pass |
| s04-mc | y (d) | y | y | Pass |
| s04-mr | y (b,d) | y | y | Pass |
| s05-mc | y (a) | y | y | Pass |
| s05-mr | y (c,e) | y | y | Pass |
| s06-mc | y (b) | y | y | Pass |
| s06-mr | y (a,d) | y | y | Pass |
| s07-mc | y (c) | y | y | Pass |
| s07-mr | y (b,e) | y | y | Pass |

Notes on individual items worth calling out (all still "Pass" — none blocks approval):

- **k07-mc** (Global Accelerator vs. CloudFront/Route 53/API Gateway cache): key and distractors
  are correct and doc-verified, but see AWS-Q21-002 — the citation it uses is not wired into the
  lesson's own citation list.
- **k13-mc** (EFS vs. EBS Multi-Attach vs. instance store vs. S3-via-FUSE): confirmed the EBS
  Multi-Attach distractor's "up to 16 Nitro-based instances… same Availability Zone… cluster-aware
  file system" language verbatim against current AWS docs — accurate and not overstated.
- **k16-mc** (Step Functions Standard vs. Express vs. SQS delay-queue chaining vs. chained Express
  workflows): confirmed Standard = up to one year / exactly-once / full history and Express = up
  to five minutes / at-least-once verbatim against `choosing-workflow-type.html`; the SQS
  delay-queue distractor's "14-day maximum retention, no execution history" framing is accurate.
- **k02-mc / k02-mr** (AppConfig distractor): confirmed AppConfig has gradual rollout with
  CloudWatch-alarm automatic rollback but no secret-rotation mechanism of its own — the "it has no
  credential-rotation capability" line in both rationales holds up. (AppConfig docs do describe
  redeploying a secret's *value* after Secrets Manager rotates it elsewhere; that is Secrets
  Manager doing the rotating and AppConfig redistributing the result, not AppConfig itself
  rotating a credential, so the rationale's claim is not contradicted.)
- **s04-mc / s06-mr / s01-mr** (LD-Q21-003 "plausible for one half" fix): re-checked that every
  distractor in these previously-flagged MR items now plausibly answers one of the two stated
  needs rather than being generic filler — confirmed for all of them (e.g., s06-mr's Classic Load
  Balancer choice plausibly answers "route requests," failing only the URL-path half).

## Issues

**AWS-Q21-001 (Low)** — `content/lessons/lesson-2-1.json`, K08 "Migrating applications into
containers" section, Exam tip sentence: `"...\"deploy an app that is already in a Dockerfile\" is
Copilot, and..."`.
Problem: commit `f8709a9` ("teach AppConfig, EventBridge Scheduler, MGN, Classic LB, EBS
Multi-Attach, SQS-vs-workflow for task 2.1 distractors; **drop retired Copilot**") removed the AWS
Copilot distractor from `q-saa-2-1-k08-mc.json` (confirmed: no question file in this task mentions
Copilot) but left the K08 Exam tip's own reference to Copilot in place. AWS Copilot CLI reached
end of support, so naming it as the correct answer to a hypothetical exam-tip scenario is now
teaching a retired tool as if it were current, and the sentence is also orphaned — no drill in this
task tests it any more.
Exact fix: in `lesson-2-1.json`'s `bodyMarkdown`, change the K08 Exam tip from
`"...\"deploy an app that is already in a Dockerfile\" is Copilot, and \"lift-and-shift a whole
server with no container involved\" is MGN."` to drop the Copilot clause entirely, e.g.: `"...
and \"lift-and-shift a whole server with no container involved\" is MGN."` This does not touch any
question file and needs no re-review of the 35 questions (none tests this clause).

**AWS-Q21-002 (Low)** — `content/lessons/lesson-2-1.json` `citationIds` array vs.
`content/citations/cite-saa-2-1-k-global-accelerator.json`.
Problem: `q-saa-2-1-k07-mc.json` cites `cite-saa-2-1-k-global-accelerator`, a real citation file
(confirmed to exist, pointing at the AWS Global Accelerator "how it works" doc, doc-verified) that
writer A added in the same commit specifically because "the lesson's existing `citationIds` list
had no Global Accelerator source even though K07's body discusses it" (per
`questions-2-1-impl-A.md`). That gap was never closed: the lesson's own `citationIds` array (33
entries) still does not include `cite-saa-2-1-k-global-accelerator`, so a reader who opens the
lesson's attached citation list will not find the source for a claim its own K07 section makes.
Separately, the id itself is inconsistently named (`cite-saa-2-1-k-global-accelerator` mixes the
`k-`-prefixed-topic convention used nowhere else in this citation set — every other id names the
service/topic directly, e.g. `cite-saa-2-1-mgn-overview`).
Exact fix: add `"cite-saa-2-1-k-global-accelerator"` to `lesson-2-1.json`'s `citationIds` array
(no wording changes needed elsewhere); optionally rename the citation file/id to
`cite-saa-2-1-global-accelerator` for consistency with the rest of the set, updating the one
reference in `q-saa-2-1-k07-mc.json` accordingly. Neither is a factual error in the question or
the citation's content — the citation itself is accurate and correctly used by the question — this
is purely a lesson-file linkage gap.

No other issues found. No factual errors, ambiguous keys, unsupported citations, strawman
distractors, self-explaining choices, or task-wide distractor-type overcounts were found in the 35
question files themselves.

## Cross-batch checks

- **Distractor-type reuse:** spot-checked the highest-frequency recurring ideas across both
  writers' combined 98 distractor slots: "poll an interval instead of reacting to an event" (4:
  k05-mc-d, k05-mr-e, s01-mr-b, s06-mr-e), "vertical/bigger-instance resize" (3: k04-mc-c,
  k06-mc-a, k15-mc-b), "standing/always-on compute the team must patch" (3: s04-mr-c, s05-mc-c,
  s06-mr-b), "long-lived/continuously-running Fargate container" (3: s04-mr-e, s05-mc-d,
  s05-mr-d), "self-managed SFTP/EC2 server the team patches" (2: k02-mr-b, s07-mc-a). None reaches
  the 5-of-35 cap.
- **No two questions test the identical fact:** each `mc`/`mr` pair sharing an objective (k02,
  k05, k08, k11, k14) tests a different angle of that objective — the `mc` is a scenario requiring
  a single service choice, the `mr` isolates two specific mechanics or pairs two services against
  two separate needs — consistent with the pattern already approved for task 1.3's `k04-mc`/`mr`
  pair. No overlapping fact pair was found.
- **Nothing contradicts lesson 2.1:** every question's rationale traces to a specific sentence in
  `lesson-2-1.json`'s K01–K16/S01–S07 body (confirmed against the impl-A/impl-B per-question
  tables' "Lesson sentence" column), and no rationale states a number, timeout, retention, or
  behavior that conflicts with the lesson text or current AWS documentation. The only
  inconsistency found is AWS-Q21-001 above, which is a stale lesson sentence, not a
  question-vs-lesson contradiction.

## Summary metrics

- Key correct: **35/35**. No MC item has a second defensible answer under its stated constraints;
  every MR key set is exactly `selectCount` answers, complete and correct.
- Distractors real, current, non-strawman, non-giveaway: **35/35 questions pass**, including every
  item the Lead Dev pre-review flagged (`LD-Q21-001/002/003`) — all confirmed fixed and re-verified
  independently against AWS documentation in this review.
- Factual errors in the 35 question files: **0**.
- Citations: all 33 distinct `citationIds` referenced resolve to files in `content/citations/`;
  one (`cite-saa-2-1-k-global-accelerator`) is not linked from the lesson's own `citationIds`
  array (AWS-Q21-002, Low, lesson-file fix only).
- One stale lesson sentence still names a retired tool (AWS-Q21-001, Low, lesson-file fix only).

## Required fixes

None block approval of the 35 question files. AWS-Q21-001 and AWS-Q21-002 are both scoped to
`content/lessons/lesson-2-1.json`, not to any question file, and neither is a factual error a
student would be tested on incorrectly — recommend Lead Dev take a small follow-up pass on the
lesson file when convenient.

**Task 2.1: approve**

Overall: approve
