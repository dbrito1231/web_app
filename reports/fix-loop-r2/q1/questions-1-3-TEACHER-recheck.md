# Task 1.3 targeted re-check — Teacher review (second pass)

Saved by Lead Dev from the Teacher's reply (AGENTS.md: the Teacher does not write files).

**Scope:** commit `78dd93b` only — the two fixes (TEACHER-Q13-001, AWS-Q13-001). Ignored lesson-2-1/2-2 changes as instructed. Read-only checks: file reads, `content_lint.py`, AWS Documentation MCP.

### 1. TEACHER-Q13-001 — Gone

- New sentence in `content/lessons/lesson-1-3.json` K04: "When a KMS key is backed by a customer-controlled (custom) key store, applications still call the AWS KMS API — not PKCS #11, JCE, or CNG directly against the HSMs."
- Verified against `kms/latest/developerguide/key-store-overview.html` (fetched via AWS Documentation MCP): "You can configure AWS KMS to use an AWS CloudHSM key store, where keys are generated, stored and used in an AWS CloudHSM cluster that you own and manage. **Requests to AWS KMS are forwarded to your AWS CloudHSM cluster.**" This directly supports the sentence — the application still calls the KMS API; KMS internally forwards to the HSM cluster, not the app calling PKCS #11/JCE/CNG.
- New citation `content/citations/cite-saa-1-3-kms-custom-key-store.json` resolves and its `url`/`note` matches the doc content confirmed above.
- `content/questions/q-saa-1-3-k04-mr.json` now lists `cite-saa-1-3-kms-custom-key-store` in `citationIds`, and its existing rationale for distractor c ("the application talks to the KMS API, not PKCS #11, directly against the HSMs") now has lesson grounding it lacked before. Rationale wording is consistent with the new lesson sentence.

### 2. AWS-Q13-001 (second-role check) — Gone

- `content/citations/cite-saa-1-3-cloudhsm-ha.json` now points to `cloudhsm/latest/userguide/cluster-high-availability-load-balancing.html`.
- Fetched that page via MCP: it explicitly states both halves of the lesson sentence — "When you create an AWS CloudHSM cluster with more than one HSM, you automatically get load balancing... distributes cryptographic operations across all HSMs in the cluster" and "When you create the HSMs in different AWS Availability Zones, you automatically get high availability." Confirmed accurate and complete support for the sentence (both the multi-AZ HA half and the load-balancing-across-every-HSM half).

### 3. Nothing else changed or broke

- Single-asterisk spans: 0 (checked `lesson-1-3.json` bodyMarkdown programmatically — no stray single `*` outside `**bold**` pairs).
- `drillIds` in `lesson-1-3.json`: 20 entries, unchanged, all resolve to existing question files.
- Citations: all 28 `citationIds` referenced across `lesson-1-3.json` + `q-saa-1-3-k04-mr.json` (including the new one) resolve to existing files under `content/citations/`.
- `backend\.venv\Scripts\python.exe scripts\content_lint.py` → **PASS** (`questions 429 aws 310 tf 119 / labs 21 + 21 / lessons 23`).

No new issues found (no TEACHER-Q13-R-### needed).

**Task 1.3: close**
**Overall: approve**
