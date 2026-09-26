# Student fairness check — Task 1.3 "Data security controls" (rewritten questions)

Reviewer: College IT Student persona (read-only). Lesson 1.3 read in full at `/start?lesson=lesson-1-3` before attempting any question. No question JSON files were read.

## Method

For each question: navigated to `/exam?q=<id>`, read the stem and choices, wrote my answer + one-line reason below *before* clicking Check answers, clicked Check answers once, recorded the result and explanation.

## Per-question table

| # | ID | My answer (before submitting) | My reason | Result | Fair? | Why |
|---|----|-------------------------------|-----------|--------|-------|-----|
| 1 | q-saa-1-3-k01-mr | B: AWS Config rule (encryption) + E: Org tag policy (DataClassification) | Config = ongoing config compliance check; tag policy = standardizes/enforces the tag value org-wide. Neither a one-time review nor an IAM boundary "verifies" anything continuously. | Correct (100%) | Y | Directly answerable from K01. Distractors (Glacier Vault Lock, IAM permissions boundary, one-time review) are clearly off-topic once you know what each service does. No giveaway wording; explanation matched exactly what I read. |
| 2 | q-saa-1-3-k02-mc | AWS Backup, using an existing backup plan (tag-based) | Need centralized, tag-based, cross-instance EBS recovery to a prior point in time — that's AWS Backup's whole pitch in K02. | Correct (100%) | Y | Only one defensible answer — CloudWatch alarm/S3 CRR/EBS-encryption-by-default don't restore anything. Explanation taught why each distractor fails, matched the choices shown. |
| 3 | q-saa-1-3-k03-mc | S3 Object Lock, compliance mode | Lesson is explicit: compliance mode blocks even the root user; governance mode allows bypass permission; a bucket policy or Lifecycle rule can still be routed around. | Correct (100%) | Y | Single defensible answer. Distinguishing compliance vs. governance mode is exactly the exam-relevant nuance from K03, tested well without a giveaway. |
| 4 | q-saa-1-3-k04-mr | CloudHSM PKCS #11 library + cluster spread across ≥2 AZs | Need to keep the *same* interface (PKCS #11, not JCE) and survive an AZ outage (multi-AZ cluster, not a single HSM "backed by KMS" which isn't a real relationship). | Correct (100%) | Y | Answerable from K04's CloudHSM paragraph. This question references "that contractor" from a sibling question, but the requirement stated is self-contained (AZ resilience + same interface) — no missing context needed. |
| 5 | q-saa-1-3-s01-mc | Download the report from AWS Artifact | Lesson explicitly says Artifact gives on-demand downloads of AWS's own SOC/ISO/PCI reports at no cost. | Correct (100%) | Y | Only one tool in S01 answers "AWS's own report" — Config and Access Analyzer describe the customer's resources, not AWS's. Clear, no giveaway. |
| 6 | q-saa-1-3-s02-mr | Enable S3 Bucket Key on the high-volume bucket + explicitly re-enable SSE-C via PutBucketEncryption | Bucket Key cuts KMS request costs (up to 99% per lesson); SSE-C is disabled by default on new buckets since April 2026, so it must be explicitly turned back on. | Correct (100%) | Y | Matches S02 precisely. Minor note: the "since April 2026" SSE-C default-change detail is very specific/date-based and could feel like an obscure memorization point, but it's stated plainly in the lesson text, so it's fair, just a bit dense. |
| 7 | q-saa-1-3-s03-mc | US East (N. Virginia), regardless of origin Region | Lesson states CloudFront-attached ACM certs must be requested in us-east-1 no matter where the origin lives. | Correct (100%) | Y | Directly taught fact, single answer, no ambiguity. |
| 8 | q-saa-1-3-s04-mr | KMS grant (temporary, no key-policy edit) + key policy is Regional (configure independently per Region) | Grants exist specifically to avoid editing the key policy; key policies never apply cross-Region even with a shared alias. | Correct (100%) | Y | Matches S04 exactly; distractors (IAM alone sufficient, one policy for both Regions, "editing key policy is the only way") are each directly contradicted by the lesson text. |
| 9 | q-saa-1-3-s05-mc | AWS Backup | Only service in S05/K02 that gives one policy-driven, tag-based plan spanning EBS + RDS + DynamoDB with cross-Region copy. | Correct (100%) | Y | Distractors each cover only one resource type or aren't policy-driven — no ambiguity. |
| 10 | q-saa-1-3-s07-mr | ACM cert renews automatically (DNS-validated + attached to API Gateway) + asymmetric key not eligible for auto/on-demand rotation, must be manually re-created and swapped | Lesson states asymmetric keys are excluded from automatic/on-demand rotation and that DNS-validated certs on integrated services renew themselves. | Correct (100%) | Y | Matches S07 precisely; distractors (convert asymmetric to symmetric, annual auto-rotation for asymmetric keys, manual cert re-import) are each explicitly ruled out in the lesson. |

## Fairness rate

10 / 10 fair = **100%** (target ≥90% — met).

## Anything confusing

- Q6 (s02-mr) leans on a fairly specific, date-stamped AWS behavior change ("since April 2026, SSE-C is disabled by default on new general-purpose buckets"). It's clearly stated in the lesson, so it's answerable and not unfair, but it's the single densest/most "trivia-like" fact in this batch — worth knowing it's there if this fact ever needs a citation recheck.
- Q4 (k04-mr) is phrased as a follow-on to a sibling question ("That contractor's compliance team also requires...") — it read fine standalone since the requirement is fully self-contained, but the phrasing assumes the reader has just seen the previous scenario about a defense contractor migrating on-prem PKI. Not a fairness problem, just a stylistic note.
- All ten explanations matched the choices actually shown and taught a specific "why," including why the runner-up distractors fail — good exam-prep quality throughout.

## Verdict

**Task 1.3: close**

**Overall: approve**
