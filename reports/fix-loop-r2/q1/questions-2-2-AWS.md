# AWS Solutions Architect review — task 2.2 questions (32 rewritten)

Reviewer: Senior AWS Solutions Architect role (read-only). Date: 2026-09-26.
Scope: the 32 files `content/questions/q-saa-2-2-*.json` as of commit `1c1b725`, written against
`content/lessons/lesson-2-2.json`. Author notes: `reports/fix-loop-r2/q1/questions-2-2-impl-A.md`
(k01–k12, writer A) and `-impl-B.md` (s01–s08, writer B). Quality bar: the approved task 2.1 set
(`reports/fix-loop-r2/q1/questions-2-1-AWS.md`).

Method:
- Read `lesson-2-2.json` in full and solved each question cold against its stated constraints
  before checking the listed key.
- Verified load-bearing facts via the AWS Documentation MCP (`search_documentation`): Multi-AZ DB
  cluster (writer + two readable standbys across three AZs, confirmed verbatim against
  `multi-az-db-clusters-concepts.html` / `create-multi-az-db-cluster.html`); RDS Proxy failover
  benchmarks (confirmed both the lesson's "up to 66%" figure, from the DMS migration-playbook RDS
  Proxy benefit pages, and a separate Aurora-specific 24s→3.1s/87% benchmark from the prescriptive
  guidance page — two different, both-current, non-contradictory published figures; the lesson and
  all questions use only the 66% one, so no error); AWS Backup Vault Lock (compliance mode
  immutable to all users including root, governance mode removable by sufficiently privileged IAM
  users, minimum 72-hour/three-day cooling-off period, confirmed against `vault-lock` docs and
  CloudFormation `ChangeableForDays` reference); Application Load Balancer cross-zone load
  balancing (confirmed "enabled by default on Application Load Balancers, configurable at the
  target group level" against `application-load-balancers.html`); the four DR strategies' RTO/RPO
  bands (confirmed backup and restore, pilot light RPO-minutes/RTO-tens-of-minutes, warm standby
  RPO-seconds/RTO-minutes, and multi-site active/active against the Well-Architected
  `rel_planning_for_recovery_disaster_recovery` page). DynamoDB global tables' default multi-Region
  eventual consistency with automatic last-writer-wins conflict resolution (used by s02-mc/s08-mr)
  and MRSC's existence as a separate, opt-in mode were both confirmed and are consistent with how
  the questions describe "conflicting writes resolved automatically" (they never claim strong
  consistency, so no conflict with MRSC).
- Re-checked every fact carried over unchanged from the lesson (Route 53 policies, S3/EFS/EBS
  durability and AZ scope, X-Ray vs. CloudWatch scope, immutable infrastructure, NAT gateway/route
  table per-AZ design, RDS Multi-AZ instance vs. read replica) against the lesson body and this
  batch's rationale text for consistency; none is contradicted.
- Cross-checked all citation ids used across the 32 files against `content/citations/` (all
  resolve) and against `lesson-2-2.json`'s own `citationIds` array (one gap found — see
  AWS-Q22-002).
- Counted distractor-type reuse across both writers' 32 distractor-type tables and spot-checked
  the highest-frequency ideas by hand (RDS Proxy across k09-mc/k09-mr/s07-mc/s07-mr = 4 of 32,
  at but not over the cap; NAT-gateway-per-AZ across k03-mc/k03-mr/s04-mc = 3 of 32; DR-tier
  RTO/RPO across k04-mc/s06-mc/s06-mr = 3 of 32; Backup Vault Lock across s05-mr/s05-mc/s08-mr = 3
  of 32); none exceeds 4 of 32.
- No AWS calls were made, no servers were started, no files other than this report were written.

## Per-question results

| ID | Key correct | Distractors OK | Rationale accurate | Verdict |
|---|---|---|---|---|
| k01-mc | y (b) | y | y | Pass |
| k02-mc | y (a) | y | y | Pass |
| k03-mc | y (c) | y | y | Pass |
| k03-mr | y (a,d) | y | y | Pass |
| k04-mc | y (d) | y | y | Pass |
| k05-mc | y (a) | y | y | Pass |
| k06-mc | y (b) | y | y | Pass |
| k06-mr | y (b,e) | y | y | Pass |
| k07-mc | y (c) | y | y | Pass |
| k08-mc | y (d) | y | y | Pass (see AWS-Q22-002, citation-linkage only) |
| k09-mc | y (a) | y | y | Pass |
| k09-mr | y (c,d) | y | y | Pass |
| k10-mc | y (b) | y | y | Pass |
| k11-mc | y (c) | y | y | Pass |
| k12-mc | y (d) | y | y | Pass |
| k12-mr | y (a,e) | y | y | Pass |
| s01-mc | y (d) | y | y | Pass |
| s01-mr | y (a,b) | y | y | Pass |
| s02-mc | y (c) | y | y | Pass |
| s02-mr | y (c,d) | y | y | Pass |
| s03-mc | y (b) | y | y | Pass |
| s03-mr | y (a,e) | y | y | Pass |
| s04-mc | y (a) | y | y | Pass |
| s04-mr | y (b,c) | y | y | Pass |
| s05-mc | y (c) | y | y | Pass |
| s05-mr | y (d,e) | y | y | Pass |
| s06-mc | y (b) | y | y | Pass |
| s06-mr | y (a,b) | y | y | Pass |
| s07-mc | y (a) | see AWS-Q22-001 | y | Concerns |
| s07-mr | y (c,d) | y | y | Pass |
| s08-mc | y (d) | y | y | Pass |
| s08-mr | y (a,e) | y | y | Pass |

Notes on individual items worth calling out:

- **k08-mc** (cross-zone load balancing vs. ALB health checks / ASG health checks / Route 53
  multivalue): confirmed cross-zone load balancing is on by default for an ALB and spreads
  requests evenly across every healthy target in every enabled AZ, verbatim against current AWS
  docs. Correct and doc-verified; see AWS-Q22-002 for a citation-linkage-only note.
- **k06-mc / k06-mr** (Multi-AZ DB instance vs. cluster vs. read replica vs. Aurora Global
  Database): confirmed the Multi-AZ DB cluster's "writer + two readable standbys across three
  AZs" fact verbatim against current RDS docs. Distractors are real, current, and each fails the
  stated requirement for exactly one clear reason (instance's standby isn't readable; a read
  replica isn't auto-failover; Aurora Global Database is cross-Region, which the stem explicitly
  rules out).
- **k09-mc / k09-mr / s07-mr** (RDS Proxy pooling and failover-time reduction): the lesson's
  "up to 66%" failover-time figure is a genuine, current, separately-published AWS number (RDS
  Proxy benefit pages in the DMS migration playbooks) distinct from the newer Aurora-specific
  87% (24s→3.1s) benchmark; neither of the two RDS Proxy question rationales in this batch states
  a specific percentage, so there is nothing to correct in the question files themselves.
- **s05-mr / s08-mr** (Backup Vault Lock compliance vs. governance mode, 72-hour cooling-off):
  confirmed compliance mode's immutability (including against the root user) and the minimum
  72-hour/three-day cooling-off period verbatim against current AWS Backup docs. The distractor
  "24 hours" and "governance mode" are both real, current, wrong-for-this-requirement options, not
  strawmen.
- **s07-mc** (ALB/NLB vs. Route 53 failover vs. AWS DRS vs. RDS Proxy, for a legacy app that
  cannot be modified): see AWS-Q22-001 below — this is the one item in the batch with a real
  ambiguity concern.

## Issues

**AWS-Q22-001 (Medium)** — `content/questions/q-saa-2-2-s07-mc.json`, stem and choice b.
Problem: the stem only states "automated, health-checked failover in front of a legacy
application whose source code cannot be modified" — it does not say the application runs as a
multi-instance fleet, and it does not state any requirement (traffic-shifting speed, per-request
granularity, or an explicit "no DNS changes" constraint) that rules out DNS-layer failover.
Choice b ("Amazon Route 53 failover routing with health checks, pointing at a single instance as
the primary endpoint") is a real, current, no-code-change AWS mechanism that also provides
automated, health-checked active-passive failover — exactly the pattern the lesson's own K06
section teaches ("Route 53 failover routing, backed by health checks, implements active-passive
DNS failover... routing clients to the secondary resource instead"). The rationale's basis for
rejecting b — that it only "monitors and redirects away from one endpoint at DNS-resolution
speed" rather than "continuously health-check[ing] and rebalanc[ing] many targets in the fleet" —
is a real architectural distinction, but it depends on the stem implying a multi-target fleet,
which the stem never states. This is the same class of gap the task instructions flagged by name
("check whether Route 53 failover in s07-mc also satisfies the stem"), and it is inconsistent with
how this same batch handles the identical ambiguity elsewhere: `q-saa-2-2-k06-mr.json`'s stem
explicitly adds "...without any DNS changes" to unambiguously rule out its own Route 53 failover
distractor (choice c). `s07-mc` has no equivalent disambiguating clause, so a well-prepared
candidate could defensibly pick b.
Exact fix: add one clause to the stem that only a load balancer satisfies, matching the pattern
already used in k06-mr, e.g.: "...must add automated, health-checked failover across multiple
running instances of a legacy application whose source code cannot be modified, with unhealthy
instances removed from rotation within seconds." That constraint (per-instance, sub-DNS-TTL
speed, multiple existing instances) is not satisfied by Route 53 failover routing pointed at a
single primary endpoint, cleanly separating choice a from choice b without changing any choice
text, key, or rationale content beyond noting the added constraint.

**AWS-Q22-002 (Low)** — `content/lessons/lesson-2-2.json` `citationIds` array vs.
`content/citations/cite-saa-2-1-alb-cross-zone.json`.
Problem: `q-saa-2-2-k08-mc.json` cites `cite-saa-2-1-alb-cross-zone` (a real, doc-verified citation
carried over from task 2.1, confirmed to still accurately state that ALB cross-zone load balancing
is "enabled by default... but is a configurable... target-group attribute, not permanently on").
That id is not present in `lesson-2-2.json`'s own `citationIds` array (25 entries), so a reader who
opens lesson 2.2's attached citation list will not find the source backing K08's cross-zone claim
— the same linkage-gap pattern already recorded and accepted as Low in task 2.1's AWS-Q21-002.
Exact fix: add `"cite-saa-2-1-alb-cross-zone"` to `lesson-2-2.json`'s `citationIds` array (no
wording changes needed elsewhere, and no change needed to the question file — the citation content
itself is accurate and correctly used).

**AWS-Q22-003 (Low, informational)** — `content/questions/q-saa-2-2-k03-mc.json`,
`q-saa-2-2-k03-mr.json`, and `content/questions/q-saa-2-2-s04-mc.json`.
Problem: all three test the same underlying fact and the same fix — a NAT gateway shared across
AZs' route tables is a single point of failure, resolved by giving each AZ its own NAT gateway
referenced only by that AZ's own route table — under two different objectives (K03 "basic
networking concepts" and S04 "mitigate single points of failure"). This is not a factual error
(each question's scenario, distractor set, and phrasing differ enough that none is a verbatim
duplicate, and the lesson's own S04 section explicitly names "one NAT gateway shared by every AZ's
route table" as its flagship SPOF example, so the reuse traces back to the lesson's own choice of
example), and the batch-wide distractor-type cap (3 of 32 for this idea) is not exceeded. Flagging
only because a student who studies K03 first and S04 second will see the identical scenario twice
with only the frame ("why did this fail" vs. "which change removes this SPOF") changed. No fix
required to close this review; worth a note for anyone doing a future content refresh of S04 to
pick a different flagship SPOF example (e.g., a single EC2 instance outside an ASG, which S04-mr
already covers separately) if k03/s04 overlap needs reducing.

No factual errors, retired/incorrect services, or unsupported citations were found in any of the
32 question files. No MC item other than s07-mc has a second defensible answer, and no MR key set
is incomplete or over-selects.

## Cross-batch checks

- **Distractor-type reuse:** highest-frequency ideas across the combined 32 questions: RDS Proxy
  (k09-mc, k09-mr, s07-mc, s07-mr = 4/32, at the cap but not over it — each targets a different
  fact: connection pooling need, RDS Proxy's two named benefits, RDS Proxy as a no-code-change
  fix, RDS Proxy paired with AWS DRS); NAT-gateway-per-AZ (k03-mc, k03-mr, s04-mc = 3/32, see
  AWS-Q22-003); the four DR-strategy tiers by RTO/RPO (k04-mc, s06-mc, s06-mr = 3/32); Backup
  Vault Lock governance vs. compliance (s05-mc, s05-mr, s08-mr = 3/32); CloudWatch vs. X-Ray scope
  (k12-mc, k12-mr, s03-mr = 3/32). None reaches 5/32.
- **No two questions test the identical fact:** every `mc`/`mr` pair sharing an objective (k03,
  k06, k09, k12, and every s01–s08 pair) tests a different angle — one isolates a single best
  choice from a scenario, the other pairs two mechanisms against two separate stated needs or
  turns the same scenario into a "select two" with different distractors. The one near-duplicate
  found across different objectives is AWS-Q22-003 (K03 vs. S04), which is informational only, not
  a blocking overlap.
- **Nothing contradicts lesson 2.2:** every rationale traces to a specific sentence in
  `lesson-2-2.json`'s K01–K12/S01–S08 body (confirmed against the impl-A/impl-B per-question
  tables' "Lesson sentence" columns) and no rationale states a number, mode, or behavior that
  conflicts with the lesson text or current AWS documentation.

## Summary metrics

- Key correct: **32/32**. 31/32 MC/MR items have no second defensible answer under their stated
  constraints; **1 (s07-mc)** has a real ambiguity risk between its key and one distractor,
  described in AWS-Q22-001.
- Distractors real, current, non-strawman, non-giveaway: **32/32 questions pass** this check.
- Factual errors in the 32 question files: **0**.
- Citations: all distinct `citationIds` referenced across the batch resolve to files in
  `content/citations/`; one (`cite-saa-2-1-alb-cross-zone`, used by k08-mc) is not linked from
  `lesson-2-2.json`'s own `citationIds` array (AWS-Q22-002, Low, lesson-file fix only).
- Distractor-type reuse: highest is 4/32 (RDS Proxy), at but not over the stated cap of 4/32.

## Required fixes

**AWS-Q22-001 must be fixed before approval** — it is a real ambiguity in a live question file
(`q-saa-2-2-s07-mc.json`), not a lesson-file-only gap, and the fix is a one-clause stem edit that
does not require re-writing any choice, key, or rationale. AWS-Q22-002 and AWS-Q22-003 are Low /
informational and do not block approval of the other 31 files.

**Task 2.2: not yet**

Overall: concerns
