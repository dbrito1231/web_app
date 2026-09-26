# Teacher review â€” SAA task 1.3 questions (commit `874d8e9`)

## Scope reviewed
- 20 files: `content/questions/q-saa-1-3-{k01-mc,k01-mr,k02-mc,k03-mc,k04-mc,k04-mr,s01-mc,s01-mr,s02-mc,s02-mr,s03-mc,s03-mr,s04-mc,s04-mr,s05-mc,s05-mr,s06-mc,s06-mr,s07-mc,s07-mr}.json`
- `content/lessons/lesson-1-3.json` (the two added sentences: CloudHSM multi-AZ HA, ACME-cert attachment restriction)
- New citations: `cite-saa-1-3-aws-config`, `cite-saa-1-3-kms-grants`, `cite-saa-1-3-cloudhsm-ha`, `cite-saa-1-3-acm-acme`
- Author's notes: `reports/fix-loop-r2/q1/questions-1-3-impl.md`
- Baseline: `reports/fix-loop-r2/q1/questions-1-2-TEACHER.md`, Amendment 2/3 of `.cursor/plans/lead_dev_fix_loop_round2_20260926.plan.md`

Both new lesson sentences were checked against `docs.aws.amazon.com` via the AWS Documentation MCP:
- CloudHSM multi-AZ redundancy/load-balancing claim â€” confirmed (`cloudhsm/.../bp-cluster-management.html`, `cluster-architecture.html`).
- "ACME-issued certificate cannot be attached to ELB/CloudFront/API Gateway" â€” confirmed verbatim by ACM docs: "ACME certificates ... cannot be used with AWS integrated services" (`acm/.../acm-services.html`, `automation-outside-integrated.html`).
- KMS grants "without editing the key policy" claim (s04-mr) â€” confirmed (`kms/.../grants.html`).
- Custom key store mechanics (k04-mr) â€” confirmed accurate in the rationale, but see issue below on where it's taught.

## Per-question table

| id | objective fit | teach-before-test | difficulty | rationale covers all choices | fairness |
|---|---|---|---|---|---|
| k01-mc | OK | OK | OK | OK | OK |
| k01-mr | OK | OK (permissions boundary from lesson 1.1; Vault Lock accurately described) | OK | OK | OK |
| k02-mc | OK | OK (CloudWatch alarm is baseline knowledge, same tolerance as 1.2's s01-mc) | OK | OK | OK |
| k03-mc | OK | OK | OK | OK | OK |
| k04-mc | OK | OK (Secrets Manager from lesson 1.2) | OK | OK | OK |
| k04-mr | OK | **Gap** â€” see TEACHER-Q13-001 | OK | OK | OK |
| s01-mc | OK | OK (Access Analyzer from lesson 1.1) | OK | OK | OK |
| s01-mr | OK | OK | OK | OK | OK |
| s02-mc | OK | OK | OK | OK | OK |
| s02-mr | OK | OK â€” April 2026 SSE-C default block used correctly | OK | OK | OK |
| s03-mc | OK | OK | OK | OK | OK |
| s03-mr | OK | OK â€” new ACME sentence covers it | OK | OK | OK |
| s04-mc | OK | OK | OK | OK | OK |
| s04-mr | OK | OK â€” new KMS grants sentence covers it | OK | OK | OK |
| s05-mc | OK | OK | OK | OK | OK |
| s05-mr | OK | OK | OK | OK | OK |
| s06-mc | OK | OK | OK | OK | OK |
| s06-mr | OK | OK | OK | OK | OK |
| s07-mc | OK | OK | OK | OK | OK |
| s07-mr | OK | OK | OK | OK | OK |

No question has a choice that refers to another choice, a stem that describes the key as already done, or a made-up/retired feature. Glacier Vault Lock (k01-mr) is described accurately (legacy standalone Glacier vault WORM control, not applicable to S3 buckets), matching the lesson and AWS docs.

## Batch metrics (my own script, run over all 20 files)

| Check | Result |
|---|---|
| Distractor types, max share | 3/20 (15%) â€” no type exceeds this |
| Longest-choice-is-key rate (MC, 11 questions) | 3/11 = 27.3% (â‰¤35% required) |
| MC key positions | a:3 b:3 c:3 d:2 |
| MR key positions (18 key slots across 9 MR) | a:3 b:3 c:4 d:4 e:4 |
| Unique 6-word stem openings | 20/20, 0 duplicates |
| Letter references in rationale | 0 (one regex false-positive on "answer a different question" in s01-mc â€” not an actual letter reference) |
| Objective text pasted verbatim | 0 matches against `content/objectives/saa_c03.json` |
| Citations resolve + verified | 20/20 resolve to existing citation files; all `mcpStatus: "verified"`, `reviewedOn: "2026-09-26"` |
| MR stems state the count | 9/9 say "(Select TWO.)" |
| `selectCount` matches `correctAnswerIds` length | 20/20 |
| `drillIds` lists all 20 | yes, exact match, no extras/missing |
| `scripts\content_lint.py` | PASS (`questions 429 aws 310 tf 119 / labs 21 + 21 / lessons 23`) |

## New issues

**TEACHER-Q13-001 (Low).** `q-saa-1-3-k04-mr`, distractor c ("Put an AWS KMS custom key store in front of the cluster so the application calls KMS APIs instead") and its rationale rely on a fact lesson 1.3 doesn't actually teach: that a KMS **custom key store** backed by CloudHSM routes cryptographic calls through the KMS API rather than PKCS #11/JCE/CNG directly against the HSMs. The lesson's K04 section mentions "a customer-controlled key store" exactly once, in passing, with no explanation of its interface â€” and neither of the question's citations (`cite-saa-1-3-cloudhsm-ha`, `cite-saa-1-3-cloudhsm`) documents this point. This is a bigger inferential gap than the "one light inferential step" tolerated in task 1.2's s01-mc.
- Exact fix: add one clause to the K04 CloudHSM paragraph in `content/lessons/lesson-1-3.json`, e.g. "When a KMS key is backed by a customer-controlled (custom) key store, applications still call the AWS KMS API â€” not PKCS #11, JCE, or CNG directly against the HSMs." Add a citation for it (AWS KMS custom key store docs, e.g. `kms/latest/developerguide/create-keystore.html`) and reference that new `citationId` from `q-saa-1-3-k04-mr.json`.

No other issues found.

**Task 1.3: not yet.**
**Overall: concerns.**
