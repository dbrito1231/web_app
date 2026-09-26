# Lesson 1.3 — Senior AWS Solutions Architect review

Reviewed: `content/lessons/lesson-1-3.json` (commit `cd64413`, "Lesson 1.3 rewritten to teach task 1.3
data security (doc-cited)"). Author notes: `reports/fix-loop-r2/q1/lesson-1-3-impl.md`. Objectives:
`SAA-1.3-K01..K04`, `SAA-1.3-S01..S07` in `content/objectives/saa_c03.json`. Quality bar: approved
lessons 1.1 and 1.2 (`content/lessons/lesson-1-1.json`, `lesson-1-2.json`).

## 1. Accuracy

Verified against AWS Documentation MCP (`docs.aws.amazon.com`), all fetches dated 2026-09-26 (today).

| # | Location | Statement checked | Result | Doc URL |
|---|---|---|---|---|
| 1 | K04 | Customer/AWS-managed/AWS-owned key control, cost, rotation table | Matches `kms/concepts.html` table exactly (annual AWS-managed rotation, optional CMK rotation, AWS-owned no fee/no audit) | kms/latest/developerguide/concepts.html |
| 2 | K04, S07 | Automatic rotation default 1 yr, custom rotation period, on-demand rotation independent of schedule, previous key material retained for decrypt, asymmetric/HMAC/custom-key-store keys need manual rotation | Matches `kms/rotate-keys.html` verbatim | kms/latest/developerguide/rotate-keys.html |
| 3 | K04 | CloudHSM: single-tenant, FIPS 140-2/140-3 Level 3–validated HSM, customer administers directly, AWS cannot see key material | Matches; current fleet is a documented mix of FIPS 140-2 Level 3 (hsm1) and FIPS 140-3 Level 3 (newer instance families), so the "140-2/140-3" hedge is correct, not sloppy | cloudhsm/latest/userguide/fips-validation.html |
| 4 | S02 | SSE-S3 is the automatic default for every new upload since Jan 2023, no charge | Matches (effective date Jan 5, 2023) | AmazonS3/latest/userguide/bucket-encryption.html |
| 5 | S02 | SSE-KMS requires `kms:GenerateDataKey` to upload / `kms:Decrypt` to download, in addition to S3 permissions | Matches | AmazonS3/latest/userguide/UsingKMSEncryption.html |
| 6 | S02 | SSE-C: S3 never stores the key, caller supplies it every request over HTTPS, caller tracks/rotates it, lost key = unrecoverable object | Matches | AmazonS3/latest/userguide/ServerSideEncryptionCustomerKeys.html |
| 7 | S02 | Client-side encryption via the S3 Encryption Client; S3/AWS never see plaintext or key | Matches | AmazonS3/latest/userguide/UsingClientSideEncryption.html |
| 8 | S02 | EBS/RDS encryption is KMS-backed; cannot encrypt an existing unencrypted resource in place | Matches (snapshot-and-recreate pattern) | AWSEC2/latest/UserGuide/EBSEncryption.html |
| 9 | S03 | ACM issues public/private certs for integrated services at no extra charge; certs are Regional; CloudFront requires the cert in us-east-1 | Matches | acm/latest/userguide/acm-overview.html; AmazonCloudFront/latest/DeveloperGuide/cnames-and-https-requirements.html |
| 10 | S03, S07 | Managed renewal requires DNS validation + attachment to an integrated service (or export); imported/expired certs are not eligible | Matches | acm/latest/userguide/managed-renewal.html |
| 11 | S03 | ACM's ACME protocol support can automate issuance/renewal on a non-integrated host | Confirmed as a current, real ACM feature | acm/latest/userguide/acm-acme.html |
| 12 | S04 | A KMS key policy is mandatory; IAM alone cannot grant access unless the key policy enables IAM policies; IAM can still explicitly deny; key policies are Regional; grants delegate without editing the key policy | Matches | kms/latest/developerguide/key-policies.html; kms/latest/developerguide/grants.html |
| 13 | K03, S06 | Object Lock WORM model: retention period vs. legal hold; compliance mode blocks even the root user; governance mode bypass needs `s3:BypassGovernanceRetention` + the `x-amz-bypass-governance-retention` header; a legal hold is unaffected by that bypass | Matches, including the exact permission/header names | AmazonS3/latest/userguide/object-lock.html; object-lock-managing.html |
| 14 | K03, S06 | A Lifecycle expiration rule cannot delete a locked object version; S3 places a delete marker instead | Matches | AmazonS3/latest/userguide/lifecycle-expire-general-considerations.html; object-lock-managing.html |
| 15 | K03 | Amazon Glacier (standalone vault service) no longer accepts new customers; Vault Lock policies, once locked, can never be changed; new WORM designs use S3 Object Lock (including S3 Glacier storage classes) instead | Matches | amazonglacier/latest/dev/introduction.html; amazonglacier/latest/dev/vault-lock.html |
| 16 | K02, S05 | AWS Backup centralizes backup plans across EBS/RDS/DynamoDB/EFS/S3 etc., tag-based assignment, cold-storage lifecycle, cross-Region/cross-account copies | Matches | aws-backup/latest/devguide/whatisbackup.html |
| 17 | K02, S05 | Live S3 replication (CRR/SRR) is asynchronous and only replicates new/changed objects going forward, not a backup by itself; S3 Batch Replication fills the pre-existing-object gap; S3 RTC gives a 99.99%-in-15-minutes SLA | Matches | AmazonS3/latest/userguide/replication.html; replication-time-control.html |
| 18 | S01 | AWS Artifact gives on-demand, free downloads of AWS's own compliance reports (SOC/ISO/PCI) | Matches | artifact/latest/ug/what-is-aws-artifact.html |
| 19 | K01, S01 | AWS Organizations tag policies standardize tag keys/values org-wide and can enforce compliance on specified resource types | Matches | organizations/latest/userguide/orgs_manage_policies_tag-policies.html |

**19 distinct technical statements verified, all confirmed accurate as written — no factual corrections needed.**

### Currency / coverage gap found during verification

**AWS-L13-001 (Medium).** S02's SSE-C paragraph is stated as unconditionally available ("has S3 perform
the encryption, but you supply the raw key on every request"), but current AWS documentation carries an
active notice: *"Starting April 2026, SSE-C is disabled by default for all new general purpose buckets
and existing buckets in accounts with no SSE-C encrypted objects."* Since today's date is 2026-09-26,
this change is now in effect for any bucket the learner would create today — a request using SSE-C on a
fresh bucket gets an HTTP 403 `AccessDenied` unless `PutBucketEncryption` explicitly sets
`BlockedEncryptionTypes: NONE` first. This is exactly the kind of "current facts" AWS re-tests that
SAA-C03 candidates get tripped on.
**Fix:** add one sentence to the SSE-C bullet: "Since April 2026, SSE-C is disabled by default on new
general-purpose buckets (and on existing buckets with no SSE-C objects yet) — you must explicitly
re-enable it via `PutBucketEncryption` before it works."
**Doc:** https://docs.aws.amazon.com/AmazonS3/latest/userguide/ServerSideEncryptionCustomerKeys.html

**AWS-L13-002 (Low, coverage).** S02 (K04's objective area, "encrypting data at rest") never mentions
**S3 Bucket Keys**, a named, testable SSE-KMS cost-optimization feature (reduces KMS request volume by
generating a bucket-level data key). The section otherwise covers SSE-S3/SSE-KMS/SSE-C/client-side in
detail, so this is a notable omission against the stated topic list.
**Fix:** one sentence in the SSE-KMS bullet noting S3 Bucket Keys reduce per-object KMS API calls/cost,
enabled per bucket or per PUT.
**Doc:** https://docs.aws.amazon.com/AmazonS3/latest/userguide/bucket-key.html

**AWS-L13-003 (Low, coverage).** S02 also never mentions **DSSE-KMS** (dual-layer server-side encryption
with KMS keys), which is one of the three SSE options `bucket-encryption.html` documents alongside
SSE-S3/SSE-KMS and is explicitly in the review's topic list.
**Fix:** short mention that DSSE-KMS applies two independent encryption layers for workloads with a
compliance requirement for layered encryption, at roughly double the KMS cost of SSE-KMS.
**Doc:** https://docs.aws.amazon.com/AmazonS3/latest/userguide/bucket-encryption.html

**AWS-L13-004 (Low, coverage).** K04/S02 cover EBS encryption via KMS and the "cannot encrypt in place"
rule, but never mention **EBS encryption by default** — the account/Region-level setting that
auto-encrypts every new EBS volume and snapshot copy without per-volume action. This is a distinct,
commonly tested exam bullet (e.g., "how do we guarantee no unencrypted EBS volume can ever be created")
that the current text doesn't answer.
**Fix:** one sentence noting the per-Region "Always encrypt new EBS volumes" account setting, and that it
does not retroactively encrypt existing unencrypted volumes.
**Doc:** https://docs.aws.amazon.com/ebs/latest/userguide/encryption-by-default.html

None of the four items above are factual errors in the text as written — everything stated is correct —
they are gaps against the stated review topic list and against what SAA-C03 tests for "encrypting data
at rest" (K04/S02).

## 2. Coverage and exam tips

All 11 objective bullets (K01–K04, S01–S07) get a dedicated section with exam-relevant depth, matching
the lesson-1-1/1-2 structure (heading per bullet, worked contrast, one exam tip per section). Exam tips
checked against the corresponding accuracy items above — all correct and non-trivial (e.g., the S04 tip
correctly identifies "IAM allows but the call still fails" as a key-policy gate, not an IAM bug; the K03
tip correctly distinguishes Object Lock compliance mode from a Lifecycle rule). No stale or misleading
exam tips found. The three coverage gaps above (Bucket Keys, DSSE-KMS, EBS encryption by default) are the
only places where an objective bullet's AWS-doc surface area is not fully represented.

## 3. Citations

All 19 `citationIds` referenced in `lesson-1-3.json` resolve to an existing file under
`content/citations/cite-saa-1-3-*.json`, each with `accessed: "2026-09-26"` and a `note` that accurately
summarizes the claim it backs, matching the `Doc URLs used` list in the impl notes. Spot-checked
`kms-concepts`, `kms-rotation`, `object-lock`, `object-lock-managing`, `s3-sse-c`, `s3-replication`,
`glacier-vault-lock`, `acm-overview`, `acm-renewal`, `tag-policies` against live docs — all citation notes
support the corresponding lesson claims with no drift. No citation exists for S3 Bucket Keys or
DSSE-KMS, consistent with those topics being absent from the body text (AWS-L13-002/003 above).

## Verdict

**Overall: concerns**

Reasoning: zero factual errors across 19 verified statements — the lesson is technically sound and meets
the lesson-1-1/1-2 quality bar in structure, tone, and citation hygiene. The "concerns" verdict is driven
solely by AWS-L13-001 (a real, dated behavior change that makes an unqualified SSE-C claim stale as of
today, 2026-09-26) plus two coverage gaps in the review's own topic list (S3 Bucket Keys, DSSE-KMS) and
one missing but commonly-tested exam bullet (EBS encryption by default). These are small, additive fixes
(a few sentences, no restructuring) rather than corrections to existing text — Lead Dev can resolve all
four in one pass without touching citations already in good shape (three new citation files would be
needed for Bucket Keys, DSSE-KMS, and EBS-encryption-by-default if those get their own doc-backed
sentences).
