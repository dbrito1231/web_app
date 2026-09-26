# Teacher review: lesson 2.2 (commit `e208455`)

Saved by Lead Dev from the Teacher's reply (AGENTS.md: the Teacher does not write files).

**1. Coverage:** All 20 objectives (K01–K12, S01–S08) have their own `###` section, in exact id order, matching `SAA-2.2-*` in `content/objectives/saa_c03.json`. Confirmed complete.

**2. Accuracy:** Spot-checked 11 facts against the AWS Documentation MCP, all correct:
- DR strategy ordering and RPO/RTO figures (backup and restore: RPO hours/RTO ≤24h; pilot light: RPO minutes/RTO tens of minutes; warm standby: RPO seconds/RTO minutes; multi-site active/active: near-zero) — verbatim match to Well-Architected `rel_planning_for_recovery_disaster_recovery`.
- RDS Multi-AZ DB instance (non-readable standby) vs Multi-AZ DB cluster (two readable standbys across three AZs) — matches docs exactly.
- Aurora Global Database secondary-cluster promotion — accurate, and the lesson correctly avoids over-claiming a specific RTO number.
- Route 53 routing policies (simple, weighted, latency, geolocation, multivalue, failover) — all six are accurate descriptions.
- DynamoDB global tables multi-active replication with conflict handling — accurate (docs confirm last-writer-wins under MREC).
- RDS Proxy failover-time reduction "up to 66%" — confirmed against docs.
- S3 eleven-nines durability across ≥3 AZs, S3 One Zone-IA single-AZ tradeoff — confirmed.
- EBS io2 99.999% durability, single-AZ scope — confirmed.
- ALB cross-zone load balancing on by default — confirmed.
- AWS DRS continuous block-level replication into a low-cost staging area, minutes-scale recovery — confirmed.

No inaccuracies found.

**3. Teaching quality:** Clear and appropriately pitched. Confused-pair contrasts are all present and correct: Multi-AZ instance vs cluster vs read replica vs Aurora Replicas vs Aurora Global Database (K06); RPO vs RTO (K04); CloudWatch vs X-Ray (K12); replication vs backup for point-in-time restore (S05). All `**Exam tip:**` lines checked are logically sound and consistent with the body text. No filler. References back to lesson 2.1 (ALB/NLB mechanics, read replicas, SQS, Auto Scaling) are brief pointers, not restatements — no contradiction found (cross-checked lesson-2-1.json's K15 read-replica/Multi-AZ contrast and cross-zone load balancing mention; both are consistent with 2.2's treatment).

**4. Length:** Word count (stripping markdown markers) is 3,078 words for 20 objectives (~154 words/objective) — consistent with the author's reported 3,004 and with lesson 2.1's precedent (3,101 words/23 objectives, ~135/objective). Acceptable; nothing flagged for cutting.

**5. Format:** Clean.
- 0 single-asterisk spans, 0 pipe characters (no tables), 0 markdown links, 0 numbered lists — verified programmatically.
- All 24 `citationIds` resolve to existing files in `content/citations/`.
- All 32 `drillIds` resolve to existing `q-saa-2-2-*` files and are listed in exact objective order (K01→S08).

**6. Teach-before-test readiness:** One gap — Route 53 actually has 8 routing policy types (also geoproximity and IP-based), but K01 names only 6. A question testing geoproximity or IP-based routing could not be grounded in this lesson. Otherwise no gaps found for the 20 objectives' testable concepts.

**7. Lint:** `backend\.venv\Scripts\python.exe scripts\content_lint.py` → **PASS** (questions 429, labs 21+21, lessons 23).

### Issues

- **TEACHER-L22-001** (Low, K01): Route 53 routing-policy list omits geoproximity and IP-based routing. Fix: append a short clause, e.g. "(two further policies, geoproximity and IP-based routing, exist but are rarely tested)" or add one sentence covering geoproximity briefly, so a question writer isn't left ungrounded if a drill later touches it.

No Medium/High issues found.

**Lesson 2.2: approve for question writing.**

Overall: approve
