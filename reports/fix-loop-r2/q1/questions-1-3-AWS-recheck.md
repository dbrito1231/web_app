# AWS re-check — task 1.3 fixes (commit `78dd93b`)

Reviewer: Senior AWS Solutions Architect role (read-only). Date: 2026-09-26.
Scope: only the two fixes in commit `78dd93b` — TEACHER-Q13-001 and AWS-Q13-001. No other
files in that commit (lesson-2-1/2-2 changes) were in scope, per instructions. No AWS calls
made, no files written other than this report.

## 1. AWS-Q13-001 — Gone

`content/citations/cite-saa-1-3-cloudhsm-ha.json` now points to
`https://docs.aws.amazon.com/cloudhsm/latest/userguide/cluster-high-availability-load-balancing.html`.

Fetched that page via the AWS Documentation MCP. It states both halves of the K04 sentence
directly:

- "When you create an AWS CloudHSM cluster with more than one HSM, you automatically get load
  balancing. Load balancing means that the AWS CloudHSM client distributes cryptographic
  operations across all HSMs in the cluster..." — supports "the cluster automatically
  load-balances cryptographic operations across every HSM it contains."
- "When you create the HSMs in different AWS Availability Zones, you automatically get high
  availability..." — supports "gets its redundancy and high availability from spreading its
  HSMs across multiple Availability Zones."

Both halves of the sentence are now fully supported by the single cited page. **Verdict: Gone.**

## 2. TEACHER-Q13-001 (second-role check) — Gone

New K04 sentence in `content/lessons/lesson-1-3.json`: "When a KMS key is backed by a
customer-controlled (custom) key store, applications still call the AWS KMS API — not PKCS #11,
JCE, or CNG directly against the HSMs."

Fetched `https://docs.aws.amazon.com/kms/latest/developerguide/key-store-overview.html` in full
(three pages via `start_index`) via the AWS Documentation MCP:

- **AWS CloudHSM key store:** "You can configure AWS KMS to use an AWS CloudHSM key store, where
  keys are generated, stored and used in an AWS CloudHSM cluster that you own and manage.
  **Requests to AWS KMS are forwarded to your AWS CloudHSM cluster.**"
- **External key store:** "You can configure AWS KMS to use an external key store (XKS)...
  **Requests to AWS KMS are forwarded to your externally hosted system** through an XKS proxy in
  your network."

Both custom-key-store types confirm the same mechanism: the caller always goes through the AWS
KMS API, and KMS internally forwards the request to the backing HSM cluster or external key
manager — the application never calls PKCS #11, JCE, or CNG directly against the HSMs. This
supports the lesson sentence's claim that it "covers both AWS CloudHSM key stores and external
key stores." Accurate, and not overstated.

- Citation `content/citations/cite-saa-1-3-kms-custom-key-store.json` resolves; its `url` and
  `note` match the confirmed doc content above.
- `content/questions/q-saa-1-3-k04-mr.json` distractor c ("Put an AWS KMS custom key store in
  front of the cluster so the application calls KMS APIs instead") and its rationale clause
  ("Placing an AWS KMS custom key store in front of the cluster means the application talks to
  the KMS API, not PKCS #11, directly against the HSMs, so it does not preserve the required
  interface") are both correct and now grounded in the lesson body and the new citation. No
  change needed to the question file's text — only the `citationIds` addition, which is correct.

**Verdict: Gone.**

## 3. Nothing new is wrong

- Re-read the full `lesson-1-3.json` K04 paragraph as changed by the diff: the new sentence is
  inserted in a sensible place (after the "customer-controlled key store" clause, before the
  multi-AZ HA sentence) and does not contradict or duplicate any other K04 content.
- `citationIds` on both `lesson-1-3.json` and `q-saa-1-3-k04-mr.json` all resolve to existing
  files under `content/citations/`.
- `backend\.venv\Scripts\python.exe scripts\content_lint.py` → **PASS** (`questions 429 aws 310
  tf 119 / labs 21 + 21 / lessons 23`), matching the Teacher's own re-check run.
- No new factual, citation, or consistency issues found. No AWS-Q13-R-### items to open.

## Summary

Both AWS-Q13-001 and TEACHER-Q13-001 are resolved by commit `78dd93b`, confirmed independently
against current AWS documentation (CloudHSM HA/load-balancing page and the KMS key-store-overview
page, including the AWS CloudHSM key store and external key store sections). No regressions.

**Task 1.3: close**

**Overall: approve**
