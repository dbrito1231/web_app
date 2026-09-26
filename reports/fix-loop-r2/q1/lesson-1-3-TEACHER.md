# Teacher review: lesson 1.3 (commit `cd64413`)

Saved by Lead Dev from the Teacher's reply. The Teacher does not write files (AGENTS.md).

## AWS-L13-001: agreed, verified independently

From `docs.aws.amazon.com/AmazonS3/latest/userguide/blocking-unblocking-s3-c-encryption-gpb.html`:

> Starting April 2026, Amazon S3 automatically disables server-side encryption with customer-provided keys (SSE-C) for all new general purpose buckets.

It also applies to existing buckets in accounts that have no SSE-C objects, and SSE-C uploads are rejected with 403 AccessDenied by default. The lesson's S02 SSE-C bullet is stale.

The Teacher also concurs with AWS-L13-002/003/004 (Bucket Keys, DSSE-KMS, EBS encryption by default) as low-severity coverage gaps.

## Checks

- **Objectives:** all 11 `SAA-1.3-*` bullets have sections.
- **Teach-before-test:** vacuous for now. The current 19 questions are placeholders.
- **Pedagogy:** the five confusing pairs are contrasted, all 11 exam tips are correct, and nothing from lesson 1.2 is repeated.
- **Length:** 2,841 words. Two sentences can be cut without losing content:
  - S04: "…that behavior only exists because the key policy allows it"
  - S07: "…so it does not, by itself, recover from a key that may have been compromised"
- **Format:** clean. All 19 citations resolve.
- **Accuracy:** 6 more facts spot-checked (Config rules, tag policy enforcement, CloudHSM interfaces, Lifecycle vs bucket-policy deny, AWS Backup scope, Vault Lock / Glacier no new customers). All accurate.
- **`content_lint.py`:** PASS.

## New issue

**TEACHER-L13-001 (Medium).** `drillIds` omits the 9 existing `-mr` questions (k01, k04, s01–s07). Add them in objective order.

**Lesson 1.3: not yet.** It is pending AWS-L13-001 and TEACHER-L13-001. Overall: concerns.
