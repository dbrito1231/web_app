# Lesson 2.2 — AWS Solutions Architect review

Reviewed: `content/lessons/lesson-2-2.json` (commit `e208455`, "Lesson 2.2: rewritten, one section per
objective, 24 doc citations, all 32 drillIds"). Author notes: `reports/fix-loop-r2/q1/lesson-2-2-impl.md`.
Objectives: `SAA-2.2-K01..K12`, `SAA-2.2-S01..S08` in `content/objectives/saa_c03.json`. Standard used:
approved reviews `reports/fix-loop-r2/q1/lesson-2-1-AWS.md` (Overall: approve) and `lesson-1-3-AWS.md`
(Overall: concerns). Method: AWS Documentation MCP (`search_documentation` / `read_documentation`)
against docs.aws.amazon.com, all fetches dated 2026-09-26 (today). No AWS calls, no edits made outside
this report.

## 1. Per-section verdict

| Section | Verdict | Notes |
|---|---|---|
| K01 — AWS global infrastructure | Accurate | Region/AZ definitions and Route 53 routing-policy summary confirmed against `routing-policy.html`. Lists 6 of the 8 current policies (omits geoproximity, IP-based) — informational only, see §4. |
| K02 — AWS Managed Services | Accurate | Comprehend/Polly descriptions match `comprehend/what-is.html` and `polly/what-is.html`. |
| K03 — Basic networking | Accurate | Route table / per-AZ NAT gateway pattern matches `vpc/RouteTables.html` and AWS's documented per-AZ NAT recommendation. |
| K04 — DR strategies | Accurate, verbatim | RPO/RTO figures and cost/complexity ordering for backup-and-restore, pilot light, warm standby, multi-site active/active match `rel_planning_for_recovery_disaster_recovery.html` word-for-word (including the "PITR to ~5 minutes" detail). |
| K05 — Distributed design patterns | Accurate | No specific numeric claims to verify; consistent with the Reliability Pillar's redundancy guidance. |
| K06 — Failover strategies | Accurate | Multi-AZ DB instance (non-readable standby) vs. Multi-AZ DB cluster (two readable replicas across three AZs) matches `multi-az-db-clusters-concepts.html` exactly ("writer DB instance and two reader DB instances in three separate Availability Zones"). Read replica / Aurora Replicas / Aurora Global Database contrast matches `Concepts.AuroraHighAvailability.html`. Consistent with lesson 2.1's K15 read-replica-vs-Multi-AZ contrast (no contradiction). |
| K07 — Immutable infrastructure | Accurate | Matches Well-Architected REL08-BP04. |
| K08 — Load balancing | Accurate | "Cross-zone load balancing, on by default for an ALB" is correctly hedged as a default rather than an absolute — this avoids the overstatement flagged as AWS-L21-001 in the lesson 2.1 review. |
| K09 — Proxy concepts | Accurate | RDS Proxy pooling/multiplexing matches `rds-proxy.howitworks.html`. The "up to 66%" failover-time reduction figure is a real, AWS-documented number (confirmed via MCP: "RDS Proxy failover reduction... reduce failover times for Aurora and Amazon RDS databases by up to 66%", cited in AWS's DMS migration playbooks and referenced from `Concepts.AuroraHighAvailability.html`). Not fabricated. |
| K10 — Service quotas and throttling | Accurate | Standard, uncontroversial description; matches `servicequotas/request-quota-increase.html`. |
| K11 — Storage options | Accurate | EBS io2 "99.999% durability" confirmed (`ebs-volume-features.html`, `provisioned-iops.html`). S3 "3+ AZs" and "eleven nines" confirmed (`AmazonS3/.../DataDurability.html`: "stores objects across a minimum of three Availability Zones... designed to exceed 99.999999999% (11 nines)"). S3 One Zone-IA single-AZ trade-off is correct. |
| K12 — Workload visibility | Accurate | CloudWatch vs. X-Ray contrast matches each service's "what is" page. |
| S01 — Automation strategies | Accurate | No new factual claims beyond K07/K04 cross-references. |
| S02 — Region/AZ HA services | Accurate | Aurora Global Database, DynamoDB global tables, S3 CRR, Route 53, AWS DRS/Backup cross-Region copy are all real, purpose-built Region-spanning services. See AWS-L22-002 for a coverage gap (consistency modes). |
| S03 — Metrics from business requirements | Accurate | 99.9%/99.99% downtime-budget figures (8.7h/yr, ~52 min/yr) are the standard, correct "nines" math. |
| S04 — Mitigating SPOFs | Accurate | Standard, correct examples and mitigations. |
| S05 — Data durability/availability strategies | Accurate but incomplete | AWS Backup and S3 CRR descriptions are correct; PITR-vs-replication point is correct and well-reasoned. Missing AWS Backup Vault Lock, which the review brief explicitly lists — see AWS-L22-003. |
| S06 — Selecting a DR strategy | Accurate | Correctly maps K04's catalog to RTO/RPO/budget with cost as tiebreaker. |
| S07 — Legacy/non-cloud-native reliability | Accurate | AWS Elastic Disaster Recovery description (block-level continuous replication, low-cost staging area, minutes-scale launch, no source changes) matches `drs/what-is-drs.html`. RDS Proxy and ALB/NLB drop-in framing is correct. |
| S08 — Purpose-built services | Accurate | Restates K06/S02/S05/S07 services correctly as "don't build it yourself" examples; no new factual claims. |

## 2. Issues

| # | Location | Severity | Problem | Fix | Doc URL |
|---|---|---|---|---|---|
| AWS-L22-001 | All 24 `content/citations/cite-saa-2-2-*.json` files, `note` field | Low | Every citation's `note` is identical boilerplate — "Q1 lesson-first rewrite (SAA task 2.2): fetched from docs.aws.amazon.com and checked against the lesson claims." — with no statement of which specific claim it backs. This is a real regression from the approved standard: lesson 2.1's citations (e.g. `cite-saa-2-1-alb-cross-zone.json`) each name the exact claim verified (e.g. "...confirmed cross-zone load balancing is enabled by default... but is a configurable... attribute, not permanently on."), and lesson 1.3's citations do the same. A generic note can't be used to spot-check whether a citation actually supports its sentence. | Rewrite each of the 24 `note` fields to name the specific lesson claim it backs (one sentence each), matching the pattern in `cite-saa-2-1-*.json` / `cite-saa-1-3-*.json`. | N/A (process/citation-hygiene issue, not a doc-content issue) |
| AWS-L22-002 | K06 / S02, DynamoDB global tables | Low (coverage) | The review brief explicitly asks to check DynamoDB global tables' consistency modes. The lesson only says "multi-Region, multi-active replication with automatic conflict handling" and never names a consistency mode. Current docs describe two selectable modes — multi-Region eventual consistency (MREC, the default) and multi-Region strong consistency (MRSC, same-account only) — and the actual conflict-resolution mechanism is last-writer-wins, not an unspecified "automatic" handling. | Add to S02 (or K06): "Global tables default to multi-Region eventual consistency (MREC); an MRSC (multi-Region strong consistency) mode is available for same-account tables. Conflicting writes to the same item are resolved last-writer-wins." | https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/GlobalTables.html |
| AWS-L22-003 | S05, AWS Backup | Low (coverage) | The review brief explicitly lists "AWS Backup (cross-Region/cross-account copy, Vault Lock)" as a fact to check. S05 covers cross-account/cross-Region copy but never mentions **Vault Lock** at all, even though it's a commonly tested SAA-C03 ransomware/compliance-protection feature (WORM backup vault, immutable once locked, mandatory 3-day/72-hour cooling-off period before it takes permanent effect). | Add one sentence to S05: "AWS Backup Vault Lock makes a backup vault's retention policy immutable — not even the root user can delete a recovery point or shorten retention once the vault is locked — after a mandatory 72-hour cooling-off period during which the lock can still be removed." | https://docs.aws.amazon.com/aws-backup/latest/devguide/vault-lock.html |

No factual error, retired service, renamed service, or stale number was found anywhere in the lesson body. Every numeric claim independently checked (DR strategy RPO/RTO figures, Multi-AZ DB cluster's "two readable standbys / three AZs," RDS Proxy's "up to 66%," EBS io2's "99.999%," S3's "eleven nines" / "3+ AZs," the 99.9%/99.99% downtime-budget figures) matched current AWS documentation exactly.

## 3. Exam tips

All 20 `**Exam tip:**` lines were checked against the paired section content. Each one draws a correct, testable distinction (Multi-AZ vs. second Region; Multi-AZ DB instance vs. cluster; Route 53 failover vs. instance-level health checks; immutable infrastructure vs. in-place patching; cross-zone load balancing; RDS Proxy for both connection exhaustion and failover perception; service-quota gaps in a scaled-down DR Region; S3/EFS vs. bare EBS durability; X-Ray vs. CloudWatch; RTO/RPO-driven DR strategy selection; PITR vs. replication for accidental deletes; drop-in services for legacy apps; purpose-built services vs. hand-rolled equivalents). None found stale or misleading.

## 4. Coverage and consistency

- All 20 `SAA-2.2-*` objective bullets (K01–K12, S01–S08) get their own `###` section, matching `content/objectives/saa_c03.json` exactly — no missing or extra objective.
- All 24 `citationIds` resolve to existing files under `content/citations/`; each citation's title/URL is topically correct for the section that cites it (spot-checked all 24 against the URLs actually fetched in this review — no orphaned or mismatched citation), but see AWS-L22-001 for the generic-`note` issue.
- All 32 `drillIds` resolve to existing `q-saa-2-2-*` files per the impl notes; these are still unrewritten placeholders restating the objective text, so the lesson body is the only content-accuracy surface for this pass (consistent with the impl notes' own statement).
- No contradiction found with lesson 2.1: K06's read-replica framing ("asynchronous, promotable copy... not to fail over automatically") is consistent with lesson 2.1 K15's read-replica-vs-Multi-AZ section, and K08's ALB cross-zone wording is consistent with (and improves on) the corrected wording from the lesson 2.1 review (AWS-L21-001).
- Route 53 K01 names 6 of the 8 current routing policies (omits geoproximity and IP-based routing). This is a scope choice, not an error — the objective text itself only asks for "Amazon Route 53" generally and the 6 named policies are the ones SAA-C03 tests most often. Flagged as informational only, no fix required, matching how the lesson 2.1 review treated the Kinesis Data Firehose omission.
- No retired or renamed AWS services and no stale numeric claims were found anywhere in the lesson.

**Lesson 2.2: approve for question writing**

## Overall: approve

Zero factual errors found across every numeric and conceptual claim independently checked against current AWS documentation (DR strategy RPO/RTO ordering, RDS HA option contrasts, RDS Proxy's 66% figure, storage durability figures, Route 53/ELB/ASG failover mechanics, AWS Backup, S3 CRR, DynamoDB global tables, RDS Proxy, Service Quotas, CloudWatch/X-Ray, AWS DRS). The three items above are additive, doc-backed improvements (two coverage gaps on topics the review brief explicitly named — DynamoDB consistency modes, AWS Backup Vault Lock — plus a citation-note quality regression versus the lesson 2.1/1.3 standard) rather than corrections to existing text, and none blocks writing drill questions against the current lesson body.
