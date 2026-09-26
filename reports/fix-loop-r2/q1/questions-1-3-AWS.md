# AWS Solutions Architect review — task 1.3 questions (20 rewritten)

Reviewer: Senior AWS Solutions Architect role (read-only). Date: 2026-09-26.
Scope: the 20 files `content/questions/q-saa-1-3-*.json`, the two lesson-1.3 additions in the
same commit (`content/lessons/lesson-1-3.json` — CloudHSM multi-AZ HA sentence in K04, ACME
attachment-limit sentence in S03), the 4 new citation files, and the author notes
`reports/fix-loop-r2/q1/questions-1-3-impl.md`. Quality bar: the approved
`content/questions/q-saa-1-2-*.json` set (`reports/fix-loop-r2/q1/questions-1-2-AWS.md`).

Method:
- Solved each question cold against its stated constraints before checking the listed key.
- Verified every load-bearing claim via the AWS Documentation MCP (`search_documentation` /
  `read_documentation`): AWS Organizations tag policies vs. Config vs. SCPs; AWS Backup
  cross-Region/tag-based backup; S3 Object Lock governance vs. compliance mode and
  `s3:BypassGovernanceRetention`; legal hold independence from retention bypass; Glacier Vault
  Lock as the legacy standalone-service WORM control; AWS CloudHSM cluster multi-AZ HA and
  automatic load balancing across every HSM; CloudHSM PKCS #11 vs. JCE vs. KMS custom key store;
  SSE-C/SSE-KMS/SSE-S3/DSSE-KMS key custody and cost, including S3 Bucket Keys not being
  supported for DSSE-KMS; the April 2026 SSE-C default block on new general purpose buckets;
  ACM Regional certificates and the CloudFront us-east-1 requirement; ACM managed renewal
  eligibility (DNS-validated + attached to an integrated service; imported certs never eligible);
  ACM ACME certificate automation and the explicit statement that ACME-issued certificates
  "cannot be bound to... Elastic Load Balancing, CloudFront, or API Gateway"; KMS key policies
  (the IAM-enabling statement, Regionality) and KMS grants; S3 Lifecycle actions running through
  an internal S3 endpoint that bypasses bucket-policy Deny statements; KMS automatic/on-demand
  rotation vs. asymmetric/HMAC/custom-key-store manual rotation; EBS encryption by default as a
  per-Region setting with no retroactive effect.
- Confirmed all 26 `citationIds` referenced across the 20 files (22 pre-existing + the 4 new:
  `cite-saa-1-3-aws-config`, `cite-saa-1-3-kms-grants`, `cite-saa-1-3-cloudhsm-ha`,
  `cite-saa-1-3-acm-acme`) resolve to existing files under `content/citations/`, each pointing
  to a `docs.aws.amazon.com` URL that supports the claim cited.
- Cross-checked all 11 `objectiveIds` (`SAA-1.3-K01`…`K04`, `S01`…`S07`) against
  `content/objectives/saa_c03.json` — all present with matching `task_id: "1.3"`.
- No AWS calls were made, no files other than this report were written.

## Per-question results

| ID | Key correct | Rating | Issues / notes | Doc URL |
|---|---|---|---|---|
| q-saa-1-3-k01-mc | y (a) | Exam-realistic and correct | Tag policy is the only choice that defines/enforces standard values org-wide; Config-report-only and SCP distractors are accurate, non-strawman traps. | organizations/.../orgs_manage_policies_tag-policies.html |
| q-saa-1-3-k01-mr | y (a, c) | Exam-realistic and correct | Config (ongoing) + tag policy (values) correctly paired; permissions boundary and Glacier Vault Lock (wrong resource) are clean distractors. | config/.../WhatIsConfig.html |
| q-saa-1-3-k02-mc | y (b) | Exam-realistic and correct | AWS Backup is the only tag-based, multi-instance EBS restore option; CRR (wrong resource), EBS-encryption-by-default (not recovery), CloudWatch alarm (not recovery) are all correctly ruled out. | aws-backup/.../whatisbackup.html |
| q-saa-1-3-k03-mc | y (c) | Exam-realistic and correct | Compliance mode vs. governance mode (bypassable) is the classic exam pairing and is tested precisely; Lifecycle and bucket-policy distractors are accurate. | AmazonS3/.../object-lock.html |
| q-saa-1-3-k04-mc | y (d) | Exam-realistic and correct | CloudHSM vs. KMS CMK (still multi-tenant HSM) vs. Secrets Manager (not an HSM) is well-built; confirmed CloudHSM gives single-tenant, FIPS-validated, customer-administered HSMs with PKCS #11 access. | cloudhsm/.../introduction.html |
| q-saa-1-3-k04-mr | y (a, d) | Exam-realistic and correct | Confirmed via docs: a cluster with >1 HSM gets automatic load balancing, and HSMs spread across AZs get HA; PKCS #11 library is the correct interface. Distractors (KMS "standby," custom key store, JCE-only) are each a genuine, accurate wrong-interface/wrong-mechanism trap, not a strawman. | cloudhsm/.../cluster-high-availability-load-balancing.html |
| q-saa-1-3-s01-mc | y (a) | Exam-realistic and correct | AWS Artifact is the only on-demand, no-cost source of AWS's own SOC 2 report; Config/Access Analyzer distractors correctly describe the customer's own resources, not AWS's. | artifact/.../what-is-aws-artifact.html |
| q-saa-1-3-s01-mr | y (a, e) | Exam-realistic and correct | Config rule (continuous) + Object Lock compliance mode (guaranteed immutability) correctly answer the two-part ask; Artifact (point-in-time), Lifecycle expiration (doesn't stop early delete), and an editable IAM deny are all accurate, well-reasoned distractors. | AmazonS3/.../object-lock.html |
| q-saa-1-3-s02-mc | y (b) | Exam-realistic and correct | SSE-C is the only option where S3 never holds the key; SSE-KMS/SSE-S3/DSSE-KMS are correctly ruled out for still relying on an AWS-held key, and the DSSE-KMS distractor is strengthened by the accurate detail that Bucket Keys aren't supported for it anyway. | AmazonS3/.../ServerSideEncryptionCustomerKeys.html |
| q-saa-1-3-s02-mr | y (b, c) | Exam-realistic and correct | Tests the new April 2026 SSE-C default-block fact directly and correctly; Bucket Key for cost reduction is accurate. DSSE-KMS-for-cost-savings and disable-default-encryption distractors are accurate reversals, not strawmen. | AmazonS3/.../blocking-unblocking-s3-c-encryption-gpb.html |
| q-saa-1-3-s03-mc | y (c) | Exam-realistic and correct | Confirmed CloudFront certificates must be requested in us-east-1 regardless of origin Region; "global resource" and origin-Region distractors are the standard, accurate misconceptions tested here. | acm/.../acm-overview.html |
| q-saa-1-3-s03-mr | y (b, d) | Exam-realistic and correct | Confirmed against `acm-acme.html`: "ACME-issued certificates cannot be bound to... Elastic Load Balancing, CloudFront, or API Gateway" — matches the new lesson sentence and rules out choice (c) exactly. DNS-validated ACM cert on the ALB and an ACME client on the EC2 host are the correct, accurate pairing. | acm/.../acm-acme.html |
| q-saa-1-3-s04-mc | y (d) | Exam-realistic and correct | The missing IAM-enabling key-policy statement is the best-fit explanation for "IAM allows it, nothing denies it, call still fails"; expired-session and cross-account distractors are real but produce different symptoms, which the rationale correctly distinguishes. | kms/.../key-policies.html |
| q-saa-1-3-s04-mr | y (b, e) | Exam-realistic and correct | KMS grants (no key-policy edit) and Regional key policies are both confirmed facts; "IAM alone is enough" and "one policy across Regions" are accurate, well-known myths to test. | kms/.../grants.html |
| q-saa-1-3-s05-mc | y (a) | Exam-realistic and correct | AWS Backup is the only single service spanning EBS/RDS/DynamoDB by tag with cross-Region copy; distractors are each correctly scoped to only one resource type or manual. | aws-backup/.../whatisbackup.html |
| q-saa-1-3-s05-mr | y (c, d) | Exam-realistic and correct | CRR + S3 RTC's 99.99%/15-minute SLA confirmed against docs; Batch Replication (existing objects only) and AWS Backup copy job (not near-real-time) are accurate, non-trivial distractors. | AmazonS3/.../replication-time-control.html |
| q-saa-1-3-s06-mc | y (b) | Exam-realistic and correct | Confirmed: S3 Lifecycle actions run through an internal S3 endpoint that bypasses bucket-policy Deny statements — this is a genuinely obscure but documented mechanism, well tested here without overreaching into an invented "Lifecycle overrides policy" framing (which the rationale explicitly rejects as choice c). | AmazonS3/.../troubleshoot-lifecycle.html |
| q-saa-1-3-s06-mr | y (c, e) | Exam-realistic and correct | Bypass permission + independent legal-hold removal both confirmed against `object-lock-managing.html`; "legal hold auto-expires," "compliance mode is bypassable too," and "root-user status is what mattered" are all accurate, well-reasoned myths. | AmazonS3/.../object-lock-managing.html |
| q-saa-1-3-s07-mc | y (c) | Exam-realistic and correct | On-demand rotation is the only choice that is immediate, code-free, and ARN-preserving; delete-and-recreate (breaks ARN) is a strong, realistic trap. | kms/.../rotate-keys.html |
| q-saa-1-3-s07-mr | y (d, e) | Exam-realistic and correct | Asymmetric-key manual-rotation requirement and API Gateway's DNS-validated auto-renewal are both confirmed; the false auto-rotation, false manual-reimport, and false symmetric-conversion distractors are each a clean, accurate reversal. | kms/.../rotate-keys.html |

## Lesson change verification

- **K04 (CloudHSM multi-AZ HA):** "A CloudHSM cluster gets its redundancy and high availability
  from spreading its HSMs across multiple Availability Zones, and the cluster automatically
  load-balances cryptographic operations across every HSM it contains — a single HSM in a single
  Availability Zone has none of that redundancy." Confirmed accurate against
  `cloudhsm/latest/userguide/cluster-high-availability-load-balancing.html` ("When you create an
  AWS CloudHSM cluster with more than one HSM, you automatically get load balancing... When you
  create the HSMs in different AWS Availability Zones, you automatically get high availability").
  **Citation-precision note (Low):** the sentence is cited to `cite-saa-1-3-cloudhsm-ha`, which
  points to `bp-cluster-management.html`. That page fully supports the AZ-spreading/HA half of
  the sentence but does not itself state the "automatically load-balances... across every HSM"
  half — that specific wording is on `cluster-high-availability-load-balancing.html`, a sibling
  page. Both pages agree factually, so this is not a factual error, just a citation-target gap.
- **S03 (ACME attachment limit):** "An ACME-issued certificate cannot be attached to Elastic
  Load Balancing, Amazon CloudFront, or Amazon API Gateway — it is only for use directly on the
  infrastructure outside those integrated services." Confirmed **verbatim in substance** against
  `acm/latest/userguide/acm-acme.html`: "ACME-issued certificates cannot be bound to Managed
  automation with integrated services such as Elastic Load Balancing, CloudFront, or API
  Gateway." Accurate.

## Citation and objective checks

- All 26 `citationIds` referenced by the 20 questions and the lesson resolve to existing files
  in `content/citations/`; each file's `url` is a live `docs.aws.amazon.com` page and its `note`
  accurately summarizes the claim it supports.
- All 11 `SAA-1.3-K01`…`S07` objective ids referenced by the questions and the lesson exist in
  `content/objectives/saa_c03.json` with `task_id: "1.3"`.
- Every question's key is internally consistent with its own rationale text (the rationale names
  the same concepts as the labeled correct choice(s) in every one of the 20 files); the impl
  report's per-question letter table is stale in a couple of spots relative to the final,
  rebalanced choice ordering (e.g., s01-mr), but that is a documentation artifact in the impl
  report, not an error in the shipped question files, which are correct.

## Summary metrics

- Key correct: **20/20**. No MC item has a second defensible answer under its stated
  constraints; every MR key set is exact and complete.
- Rated "exam-realistic and correct": **20/20 = 100%** (target ≥ 95%).
- Factual errors found: **0**. Every checked claim — including the two new lesson-body sentences
  these questions depend on and the April 2026 SSE-C default-block fact carried over from the
  existing lesson — matches current AWS documentation.
- Every question tests its mapped `objectiveIds`, and every fact a question or rationale relies
  on is taught in the `lesson-1-3.json` body (teach-before-test holds, including the two new
  sentences added specifically to cover K04-mr and S03-mr).

## Required fixes

None. No factual errors, ambiguous keys, or unsupported citations were found.

## Recommended (non-blocking) improvements

1. **AWS-Q13-001 (Low, citation precision):** in `content/lessons/lesson-1-3.json`, the K04
   CloudHSM multi-AZ HA sentence cites only `cite-saa-1-3-cloudhsm-ha`
   (`bp-cluster-management.html`), which supports the AZ/HA half of the claim but not the
   "automatically load-balances... across every HSM" half. Optional fix: either retitle/repoint
   `cite-saa-1-3-cloudhsm-ha`'s `url` to
   `https://docs.aws.amazon.com/cloudhsm/latest/userguide/cluster-high-availability-load-balancing.html`
   (which states both halves directly), or add a second citation id for that page. Not required
   for approval — no factual claim is unsupported by AWS documentation generally, only the
   specific citation target is imprecise.

Any edit would require re-review under the freeze rule.

## Overall: approve
