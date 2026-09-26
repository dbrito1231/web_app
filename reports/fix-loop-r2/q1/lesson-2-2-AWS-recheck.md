# Lesson 2.2 — AWS re-check (fixes from commit 56d6a3e)

Reviewed: `content/lessons/lesson-2-2.json` and `content/citations/cite-saa-2-2-*.json` at commit
`56d6a3e` ("Lesson 2.2: specific citation notes, DynamoDB MREC/MRSC, Backup Vault Lock, all Route 53
policies, S3 durability citation"). Original findings: `lesson-2-2-AWS.md` (AWS-L22-001..003),
`lesson-2-2-TEACHER.md` (TEACHER-L22-001). Fix description: "Fixes" section of `lesson-2-2-impl.md`.
Method: AWS Documentation MCP (`search_documentation` / `read_documentation`), all fetches dated
2026-09-26 (today). Read-only — no edits made outside this report, no AWS calls, no servers.

## 1. Verdict per item

| # | Item | Verdict |
|---|---|---|
| AWS-L22-001 | Generic boilerplate `note` on all 24 citations | **Gone.** Checked all 25 `cite-saa-2-2-*.json` files (24 original + new `cite-saa-2-2-backup-vault-lock`). Every `note` now names the specific lesson claim it backs (e.g. `cite-saa-2-2-rds-multiaz-cluster`: "confirmed a Multi-AZ DB cluster keeps a writer and two readable standby instances across three separate Availability Zones..."), matching the `cite-saa-2-1-*` pattern. No generic/boilerplate note remains. |
| AWS-L22-002 | DynamoDB global tables missing consistency mode / conflict resolution | **Gone.** S02 now reads: "defaults to multi-Region eventual consistency (MREC), with an MRSC same-account option for multi-Region strong consistency, and conflicting writes resolved last-writer-wins." Re-verified live against `GlobalTables.html` — see §2 below; exact match. |
| AWS-L22-003 | AWS Backup Vault Lock missing from S05 | **Gone.** S05 now has a full sentence on Vault Lock: governance mode "removable by users with sufficient IAM permissions" vs. compliance mode "immutable... once a mandatory cooling-off period of at least 72 hours expires." Re-verified live against `vault-lock.html` — exact match, including the "at least 3 days (72 hours)" minimum grace time. New citation `cite-saa-2-2-backup-vault-lock.json` added and included in `citationIds`. |
| TEACHER-L22-001 | Route 53 K01 omitted geoproximity and IP-based routing | **Gone.** K01 now lists all 8 current policies: simple, weighted, latency-based, geolocation, geoproximity, IP-based, multivalue answer, failover — matching `routing-policy.html`'s current list exactly, with correct one-line definitions for the two added policies. |

## 2. Live doc verification detail

**DynamoDB global tables (`GlobalTables.html`, re-fetched):** "If you do not specify a consistency
mode when creating a global table, the global table defaults to multi-Region eventual consistency
(MREC)." / "Global tables configured for MRSC only support same-account configurations." /
"Both same-account and multi-account models support ... last-writer-wins conflict resolution."
The lesson's S02 clause matches this exactly, word for word on the substantive facts.

**AWS Backup Vault Lock (`vault-lock.html`, re-fetched):** "Vaults locked in governance mode can have
the lock removed by users with sufficient IAM permissions." / "Vaults locked in compliance mode
cannot be deleted once the cooling-off period ('grace time') expires..." / "it must be at least 3
days (72 hours)." / "Once the grace time expires, the vault and its lock are immutable and cannot be
changed or deleted by any user or by AWS." The lesson's S05 sentence matches this exactly, including
the "at least 72 hours" figure and "even root user" scope.

**Route 53 routing policies (`routing-policy.html`, re-fetched):** current page lists exactly 8
policies — simple, failover, geolocation, geoproximity, latency, IP-based, multivalue answer,
weighted. Geoproximity: "route traffic based on the location of your resources and, optionally,
shift traffic from resources in one location to resources in another location" — matches the
lesson's "route by resource location with an optional bias to shift traffic between resources."
IP-based: "route traffic based on the location of your users, and have the IP addresses that the
traffic originates from" — matches the lesson's "route by the client's IP address using a
customer-supplied CIDR map" (the CIDR-map mechanism detail is accurate per the IP-based routing
sub-page and is not contradicted here).

**S3 durability (`DataDurability.html`, re-fetched, spot-check of new `cite-saa-2-2-s3-durability`):**
"Designed to provide 99.999999999% durability" / "redundantly store objects on multiple devices
across a minimum of three Availability Zones." Matches K11's "eleven nines" / "at least three AZs"
claim exactly.

**Additional spot-checks (unchanged text, re-confirmed still current):**
- `Multi-AZ DB clusters` (`multi-az-db-clusters-concepts.html`): "a writer DB instance and two reader
  DB instances in three separate Availability Zones" — matches K06 verbatim.
- RDS Proxy (`rds-proxy.howitworks.html`): connection pooling and multiplexing confirmed; the "up to
  66%" failover-time reduction figure (K09) is still live and documented (confirmed via MCP search
  against AWS's DMS migration playbook pages, which quote AWS's own RDS Proxy benefits page).
- Aurora Global Database (`Concepts.Aurora_Fea_Regions_DB-eng.Feature.GlobalDatabase.html`): "spans
  multiple AWS Regions, enabling low-latency global reads and disaster recovery from any Region-wide
  outage" — consistent with K06/S02's "secondary, read-only clusters in other Regions, promotable if
  the primary Region is lost."

8 citations spot-checked in total (s3-durability, backup-vault-lock, ddb-global-tables,
route53-routing, rds-multiaz-cluster, rds-proxy ×2 facts, aurora-global). No factual error found in
any of them.

## 3. New issues found

None. No new factual error, stale figure, retired/renamed service, or citation/claim mismatch was
introduced by the fix commit. `content_lint.py` still passes (questions 429, labs 21+21, lessons 23),
and word count (3,173, per the impl notes) remains within the accepted band for the four small,
additive fixes.

## 4. Overall

**Lesson 2.2: approve for question writing**

## Overall: approve

All four original findings (AWS-L22-001, AWS-L22-002, AWS-L22-003, TEACHER-L22-001) are confirmed
fixed and independently re-verified against live AWS documentation as of 2026-09-26. No new issue
found. Lesson 2.2 is clear to use as the factual basis for drill-question writing.
