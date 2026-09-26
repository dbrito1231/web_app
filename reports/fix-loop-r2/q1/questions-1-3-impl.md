# Q1 implementation report — SAA task 1.3 (Data security controls)

Scope: rewrite of all 20 `content/questions/q-saa-1-3-*.json` files, per Amendment 3 of
`.cursor/plans/lead_dev_fix_loop_round2_20260926.plan.md`. Lesson `content/lessons/lesson-1-3.json`
was already Teacher/AWS-approved; it needed two small doc-verified additions (below) to teach two
concepts new questions test. Four new citation files were added.

## Files changed

- `content/questions/q-saa-1-3-{k01-mc,k01-mr,k02-mc,k03-mc,k04-mc,k04-mr,s01-mc,s01-mr,s02-mc,s02-mr,s03-mc,s03-mr,s04-mc,s04-mr,s05-mc,s05-mr,s06-mc,s06-mr,s07-mc,s07-mr}.json` (20 files, full rewrite)
- `content/lessons/lesson-1-3.json` (two added sentences + 4 new `citationIds`; no other content changed)
- New citations: `content/citations/cite-saa-1-3-aws-config.json`, `cite-saa-1-3-kms-grants.json`, `cite-saa-1-3-cloudhsm-ha.json`, `cite-saa-1-3-acm-acme.json`

## Lesson edits (fact-checked against AWS docs via the AWS Documentation MCP)

1. **K04 (CloudHSM):** added — "A CloudHSM cluster gets its redundancy and high availability from
   spreading its HSMs across multiple Availability Zones, and the cluster automatically load-balances
   cryptographic operations across every HSM it contains — a single HSM in a single Availability Zone
   has none of that redundancy." Needed because `q-saa-1-3-k04-mr` tests multi-AZ CloudHSM cluster
   design. Source: `cite-saa-1-3-cloudhsm-ha` (docs.aws.amazon.com/cloudhsm/.../bp-cluster-management.html).
2. **S03 (ACM):** added — "An ACME-issued certificate cannot be attached to Elastic Load Balancing,
   Amazon CloudFront, or Amazon API Gateway — it is only for use directly on the infrastructure outside
   those integrated services." Needed because `q-saa-1-3-s03-mr` tests that an ACME cert can't be
   attached to an ALB. Source: `cite-saa-1-3-acm-acme` (docs.aws.amazon.com/acm/.../automation-outside-integrated.html).

The lesson already taught AWS Config, KMS grants, S3 Bucket Keys, DSSE-KMS/Bucket-Key incompatibility,
the April 2026 SSE-C default block, Object Lock governance/compliance modes and
`s3:BypassGovernanceRetention`, S3 replication/RTC/Batch Replication, and key-policy Regionality —
all reused directly by the new questions with no other lesson changes needed.

## New citations (fact-checked via AWS Documentation MCP)

| id | doc | used by |
|---|---|---|
| `cite-saa-1-3-aws-config` | `config/.../WhatIsConfig.html` | k01-mc, k01-mr, s01-mr |
| `cite-saa-1-3-kms-grants` | `kms/.../grants.html` | s04-mr |
| `cite-saa-1-3-cloudhsm-ha` | `cloudhsm/.../bp-cluster-management.html` | k04-mr |
| `cite-saa-1-3-acm-acme` | `acm/.../automation-outside-integrated.html` | s03-mr |

## Per-question table

| id | objective | tests | key | doc(s) |
|---|---|---|---|---|
| k01-mc | K01 Data access & governance | tag policy vs. manual fix, Config (report-only), SCP (can't standardize values) | a | tag-policies, aws-config |
| k01-mr | K01 | Config rule (ongoing) + tag policy together vs. one-time review, permissions boundary, Vault Lock (wrong resource) | a,c | aws-config, tag-policies, glacier-vault-lock |
| k02-mc | K02 Data recovery | AWS Backup restore vs. S3 CRR (wrong resource), EBS default encryption (not recovery), CloudWatch alarm (not recovery) | a | aws-backup, ebs-encryption-by-default |
| k03-mc | K03 Retention & classification | Object Lock compliance mode vs. governance mode (bypassable), Lifecycle (doesn't block early delete), bucket policy (editable) | a | object-lock, s3-lifecycle |
| k04-mc | K04 Encryption/key mgmt | CloudHSM vs. KMS customer/managed key (multi-tenant), Secrets Manager (not an HSM) | a | cloudhsm, kms-concepts |
| k04-mr | K04 | multi-AZ CloudHSM cluster + PKCS#11 integration vs. single-AZ/KMS "standby" (not possible), custom key store (wrong interface), JCE-only (wrong interface) | a,d | cloudhsm-ha, cloudhsm |
| s01-mc | S01 Compliance alignment | AWS Artifact vs. Config (wrong evidence), support case (manual), Access Analyzer (wrong evidence) | b | artifact |
| s01-mr | S01 | Config rule (continuous) + Object Lock compliance mode vs. one-time Artifact download, Lifecycle expiration (doesn't stop early delete), IAM deny (editable) | a,b | aws-config, object-lock, artifact |
| s02-mc | S02 Encrypt at rest | SSE-C (caller-supplied key) vs. SSE-KMS/SSE-S3 (AWS holds key), DSSE-KMS (also AWS-KMS-backed, no Bucket Key support) | a | s3-sse-c, s3-sse-kms, s3-dsse-kms |
| s02-mr | S02 | re-enable SSE-C (April 2026 default block) + S3 Bucket Key (cost) vs. false assumption, DSSE-KMS (costs more), disabling default encryption (wrong control) | a,b | s3-sse-c-default-block, s3-bucket-keys, s3-dsse-kms |
| s03-mc | S03 Encrypt in transit | CloudFront cert must be us-east-1 vs. origin Region, visitor-proximity Region, "global resource" myth | a | acm-overview |
| s03-mr | S03 | DNS-validated ACM cert on ALB + ACME client on EC2 vs. imported cert (never eligible), ACME cert on ALB (not allowed), manual re-import | a,b | acm-renewal, acm-acme |
| s04-mc | S04 Key policies | missing IAM-enabling statement in key policy vs. expired session, disabled/pending-deletion key, cross-account key | c | kms-key-policies |
| s04-mr | S04 | KMS grant (no key-policy edit) + per-Region key policies vs. "only editing works", "one policy across Regions", "IAM alone is enough" | a,d | kms-grants, kms-key-policies |
| s05-mc | S05 Backups & replication | AWS Backup (multi-service, tag-based, cross-Region) vs. S3 CRR (wrong resource), manual EBS snapshots, DynamoDB PITR alone | a | aws-backup |
| s05-mr | S05 | CRR + S3 RTC (15-min SLA) vs. S3 Batch Replication (existing objects only), AWS Backup copy job (not near-real-time), destination-only versioning | a,c | s3-replication, aws-backup |
| s06-mc | S06 Access/lifecycle/protection policies | Lifecycle actions bypass bucket-policy evaluation vs. business-hours myth, "Lifecycle overrides policy" myth, policy-creation-order myth | a | s3-lifecycle |
| s06-mr | S06 | governance-mode bypass permission+header + legal hold independence vs. auto-expiring legal hold, compliance-mode bypass myth, root-user myth | c,e | object-lock-managing, object-lock |
| s07-mc | S07 Rotate keys/renew certs | on-demand rotation vs. delete+recreate (breaks ARN), waiting for schedule (not immediate), realias (no rotation) | a | kms-rotation |
| s07-mr | S07 | asymmetric key = manual rotation + DNS-validated ACM on API Gateway = auto-renew vs. false auto-rotation claim, false manual-reimport claim, false symmetric-conversion claim | a,b | kms-rotation, acm-renewal |

## Distractor-type diversity (task-level, ≤3 questions per type per Amendment 3 rule)

| type | description | questions using it |
|---|---|---|
| manual-workaround | requires ongoing human effort instead of the automated control asked for | k01-mc, s01-mc, s05-mc (3) |
| wrong-resource-type | control is real but doesn't apply to the resource type in the stem (e.g. S3 replication for EBS) | k02-mc, s05-mc, s05-mr (3) |
| bypassable-control | looks like a hard guarantee but can be edited/overridden by an admin | k03-mc, s01-mr (2) |
| wrong-mode-or-tier | right feature, wrong mode (governance vs. compliance) | k03-mc, s06-mr (2) |
| multi-tenant-vs-dedicated | confuses KMS (managed/multi-tenant) with CloudHSM (dedicated) | k04-mc, k04-mr (2) |
| wrong-interface | right service, wrong client interface (JCE vs PKCS#11, KMS API vs PKCS#11) | k04-mr (1) |
| point-in-time-vs-continuous | one-time snapshot/report offered where ongoing/continuous proof is required | s01-mc, s01-mr (2) |
| key-custody-confusion | AWS-held key offered where caller-supplied/caller-held key is required | s02-mc (1) |
| stale-default-assumption | assumes pre-April-2026 SSE-C default still holds | s02-mr (1) |
| cost-direction-reversed | technically valid feature but moves cost the wrong way | s02-mr (1) |
| wrong-region-or-scope | Regional requirement satisfied with the wrong Region or "it's global" myth | s03-mc (1) |
| renewal-eligibility-gap | imported/non-integrated certs assumed eligible for managed renewal | s03-mr (1) |
| attachment-incompatibility | ACME cert wrongly attached to an integrated service | s03-mr (1) |
| key-policy-gate-myth | assumes IAM alone, or editing the key policy, is the only lever | s04-mc, s04-mr (2) |
| region-scope-myth (KMS) | assumes one key policy spans Regions | s04-mr (1) |
| replication-scope-gap | replication/backup feature that only covers existing objects, not new/ongoing ones | s05-mr (1) |
| policy-evaluation-myth | invents a rule about when a bucket policy does/doesn't apply | s06-mc (1) |
| hold-vs-retention-confusion | conflates legal hold lifecycle with retention-period lifecycle | s06-mr (1) |
| root-user-myth | attributes an unrelated permission's effect to root-user status | s06-mr (1) |
| arn-breaking-action | "fix" that breaks the key's ARN/alias instead of rotating material | s07-mc (1) |
| rotation-eligibility-myth | asserts automatic/on-demand rotation for an ineligible key type | s07-mr (1) |

No type is used in more than 3 of the 20 questions (15%).

## Scripted checks (run against the final files)

- **Stem 6-word-opening duplicates:** 0 (all 20 unique)
- **Longest-choice-is-key rate (MC only):** 3/11 = 27.3% (≤ 35% required) — fixed 2 of an initial 5 by
  lengthening a distractor in `k01-mc` and `s06-mc` without changing its meaning
- **Key-letter balance across the task (MC key + both MR keys):** a:6, b:6, c:7, d:6, e:4 (of 29 key
  slots; MC has no `e` option, so `e` is necessarily lower) — all choices were re-ordered (ids
  reassigned a–e) to hit this spread; wording/meaning of every choice is unchanged, only position moved
- **Letter references in rationale ("choice a", "option b", etc.):** 0
- **Objective text pasted verbatim into stem/choices/rationale:** 0 (checked against all 11 task-1.3
  objective `text` fields in `content/objectives/saa_c03.json`)
- **"Apply the objective" placeholder text:** 0 remaining (was 20/20 before this rewrite)
- **Citations:** all 20 questions have ≥ 1 valid `citationId` that resolves to an existing citation file,
  `mcpStatus: "verified"`, `reviewedOn: "2026-09-26"`
- **selectCount vs. key length:** matches on all 20 (MC: 1/1, MR: 2/2)
- **MR stems say "(Select TWO.)":** all 9
- **Teach-before-test:** every AWS fact a question or rationale relies on is present in
  `lesson-1-3.json` bodyMarkdown (2 gaps found and fixed — see "Lesson edits" above)
- **Lesson `drillIds`:** unchanged, already lists all 20 question ids; verified all 20 ids present
- **`scripts\content_lint.py`:** PASS (`questions 429 aws 310 tf 119 / labs 21 + 21 / lessons 23`)
- **`python manage.py test workbook`:** 90/90 passed

## Not yet done (out of this batch's scope)

- AWS Architect fact-check verdict, Teacher pedagogy review, and Student fairness review (30% sample)
  per Amendment 3's pipeline step 4 are still needed before this task can close in the tracker/register.
- No `npm run build` or Terraform fixture check was run — this batch touched only JSON content, not
  frontend or lab-fixture code.
