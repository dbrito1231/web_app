# Lesson 1.3 — AWS re-check (post Amendment 3 fixes)

Reviewed: `content/lessons/lesson-1-3.json` (commit `66b357f`, "Lesson 1.3: SSE-C default block (April
2026), Bucket Keys, DSSE-KMS, EBS default encryption, all drills linked (Q1 LF)"). Prior findings:
`reports/fix-loop-r2/q1/lesson-1-3-AWS.md` (AWS-L13-001..004), `lesson-1-3-TEACHER.md` (TEACHER-L13-001).
Fixes described in `reports/fix-loop-r2/q1/lesson-1-3-impl.md`, "Fixes (Amendment 3)" section. All docs
re-fetched live via the AWS Documentation MCP (`docs.aws.amazon.com`), today 2026-09-26.

## 1. AWS-L13-001..004 — Gone / Not gone

| # | Item | Verdict | Verification |
|---|---|---|---|
| AWS-L13-001 | SSE-C default block (April 2026) | **Gone** | S02 bullet now reads: "Since April 2026, SSE-C is disabled by default on new general-purpose buckets (and on existing buckets with no SSE-C objects yet) — you must explicitly re-enable it via `PutBucketEncryption` before it works." Matches `blocking-unblocking-s3-c-encryption-gpb.html` verbatim ("Starting April 2026, Amazon S3 automatically disables... SSE-C for all new general purpose buckets," extends to accounts with no SSE-C objects, rejected with 403 `AccessDenied`, re-enabled via `PutBucketEncryption`). The S02 exam tip was also updated with the same caveat — confirmed present. |
| AWS-L13-002 | S3 Bucket Keys | **Gone** | SSE-KMS bullet now states Bucket Keys reuse "a short-lived, bucket-level data key instead of calling KMS for every object, cutting those KMS request costs by up to 99%." Matches `bucket-key.html`: "reduce AWS KMS request costs by up to 99 percent," bucket-level key reused, override via `x-amz-server-side-encryption-bucket-key-enabled`. |
| AWS-L13-003 | DSSE-KMS | **Gone** | New bullet: "two independent AES-256 encryption layers — a KMS-generated data key, then a separate S3-managed key... S3 Bucket Keys are not supported for it." Matches `UsingDSSEncryption.html` exactly (two independent AES-256 layers, same layer order, "S3 Bucket Keys aren't supported for DSSE-KMS," higher cost from "increased processing overhead and AWS KMS API calls"). Intro correctly updated from "four ways" to "five ways," and the client-side bullet's superlative updated from "of the four" to "of the five." |
| AWS-L13-004 | EBS encryption by default | **Gone** | New sentence: "a per-Region account setting that forces every new EBS volume and snapshot copy created in that Region to be encrypted — it has no effect on volumes or snapshots that already exist." Matches `encryption-by-default.html`: "Region-specific setting," "Encryption by default has no effect on existing EBS volumes or snapshots." |

All four are resolved with no remaining unqualified or stale claims.

## 2. New/changed statement accuracy and citation support

Four new citation files, each `accessed: "2026-09-26"`, checked against the live doc and against the
lesson sentence(s) they back:

- `cite-saa-1-3-s3-sse-c-default-block` → `blocking-unblocking-s3-c-encryption-gpb.html`. Note text
  (default-block trigger, scope, 403 AccessDenied, `PutBucketEncryption` re-enable) matches the doc and
  the lesson sentence. Supports the claim fully.
- `cite-saa-1-3-s3-bucket-keys` → `bucket-key.html`. Note text (bucket-level key, up to 99% KMS cost
  reduction, per-bucket/per-request control via the bucket-key header, not supported for DSSE-KMS) matches
  the doc and the lesson sentence.
- `cite-saa-1-3-s3-dsse-kms` → `UsingDSSEncryption.html`. Note text (two independent AES-256 layers, KMS
  data key then S3-managed key, higher cost, no Bucket Key support) matches the doc and the lesson
  sentence.
- `cite-saa-1-3-ebs-encryption-by-default` → `encryption-by-default.html`. Note text (per-Region setting,
  new volumes/snapshot copies only, no retroactive effect, cannot be overridden per-volume once enabled in
  a Region) matches the doc and the lesson sentence.

No inaccuracies found in any of the four new statements or their citations. The S04 and S07 trims (removing
the "that behavior only exists because the key policy allows it" and "so it does not, by itself, recover
from a key that may have been compromised" clauses) leave both sections factually intact — the surrounding
sentences already carry the necessary meaning and nothing incorrect was introduced by the cut.

## 3. TEACHER-L13-001 — drillIds

`lesson-1-3.json`'s `drillIds` now has 20 entries: `k01-mc/mr`, `k02-mc`, `k03-mc`, `k04-mc/mr`,
`s01-mc/mr` through `s07-mc/mr` (9 `-mc` + 9 `-mr` + `k02-mc` + `k03-mc` = 20). All 20 resolve to an
existing file under `content/questions/` (checked programmatically; zero missing). Objective order is
correct — each `-mr` immediately follows its `-mc` sibling. **Gone.**

## 4. Nothing new wrong — re-scan

- Re-read the full S02, S04, S05 (opening), and S07 sections in the current file: no new factual claims
  beyond the four fixes, and no regressions in the surrounding text from the edits.
- `python scripts\content_lint.py` → `PASS` (questions 429, aws 310, tf 119, labs 21+21, lessons 23).
- All 23 `citationIds` resolve to a file under `content/citations/` (19 original + 4 new; checked
  programmatically, zero missing).
- All 20 `drillIds` resolve to a file under `content/questions/` (checked programmatically, zero missing).
- No new coverage gaps found against the K01-K04/S01-S07 objective set.

No new issues found (no AWS-L13-R-### items).

## Verdict

**Lesson 1.3: approve for question writing**

**Overall: approve**
