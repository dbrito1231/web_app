# Lesson 1.3 rewrite — implementation notes (Q1, lesson-first rewrite, Amendment 3)

Scope: `content/lessons/lesson-1-3.json` rewritten in the lesson-1-1 / lesson-1-2 model. 19 new citation
files added under `content/citations/cite-saa-1-3-*.json`. Questions were **not** touched (they remain the
placeholder set and will be rewritten in a later round).

## Section outline mapped to objectives

| Section | Objective | Core content |
| --- | --- | --- |
| K01 | SAA-1.3-K01 — Data access and governance | Governance = the 1.1 access controls (IAM, bucket policies, SCPs) plus enforcement/audit layers: AWS Organizations tag policies (classification tags) and AWS Config (continuous compliance rules). |
| K02 | SAA-1.3-K02 — Data recovery | AWS Backup as the cross-service recovery tool (plans, tag-based assignment, cold-storage lifecycle, cross-Region/cross-account copies); contrast with S3 replication, which is not a backup. |
| K03 | SAA-1.3-K03 — Data retention and classification | Classification (links to Macie in lesson 1.2); retention via S3 Lifecycle expiration, S3 Object Lock (retention periods, legal holds, compliance vs governance mode, interaction with Lifecycle), and legacy Glacier Vault Lock. |
| K04 | SAA-1.3-K04 — Encryption and appropriate key management | KMS key types (customer managed / AWS managed / AWS owned) contrasted on control, cost, rotation; KMS vs CloudHSM (managed multi-tenant vs single-tenant customer-administered HSM). |
| S01 | SAA-1.3-S01 — Aligning AWS technologies to meet compliance requirements | AWS Artifact (AWS's own compliance reports), AWS Config (continuous proof), tag policies (classification/scope), S3 Object Lock compliance mode (WORM requirement) — each proving something different. |
| S02 | SAA-1.3-S02 — Encrypting data at rest (AWS KMS) | SSE-S3 vs SSE-KMS vs SSE-C vs client-side encryption, contrasted on who manages the key and who can see plaintext; extended to EBS/RDS (KMS-backed, cannot encrypt in place). |
| S03 | SAA-1.3-S03 — Encrypting data in transit (ACM/TLS) | ACM issuance for integrated services, Regional certs (CloudFront needs us-east-1), managed renewal eligibility rules, ACME for non-integrated hosts. |
| S04 | SAA-1.3-S04 — Implementing access policies for encryption keys | KMS key policies are mandatory and gate IAM policies (IAM can deny but not allow without the key policy's consent); key policies are Regional; grants as a third permission path. |
| S05 | SAA-1.3-S05 — Implementing data backups and replications | AWS Backup (K02) vs S3 replication (CRR/SRR, Batch Replication for pre-existing objects, S3 RTC 15-minute SLA) — recovery copy vs live copy, and how to combine them. |
| S06 | SAA-1.3-S06 — Implementing policies for data access, lifecycle, and protection | Three independent layers on S3 data: access (IAM/bucket policy), lifecycle (transition/expiration rules, immune to a denying bucket policy), protection (Object Lock, immune to lifecycle and to governance bypass except via explicit permission). |
| S07 | SAA-1.3-S07 — Rotating encryption keys and renewing certificates | KMS automatic vs on-demand vs manual rotation (asymmetric/HMAC/custom-key-store keys are not eligible for automatic/on-demand); AWS managed key fixed annual rotation; ACM managed renewal vs imported certificates. |

## Current question topics covered (per objective ID)

The existing `q-saa-1-3-*.json` files are all still the generic placeholder pattern ("Apply the objective
directly: <objective text>" / "Design against the stated requirement and document tradeoffs" /
"Validate with official documentation before applying") — they test process hygiene, not the underlying
AWS concept. They were read to confirm which objective each question ID maps to, but they carry no
service-specific content to preserve. The lesson was written directly from the objective text and from
AWS documentation, so that a future rewrite of these questions has real KMS/S3/ACM/Backup concepts to
draw on:

- `q-saa-1-3-k01-mc` / `-mr` → K01 data access and governance
- `q-saa-1-3-k02-mc` → K02 data recovery
- `q-saa-1-3-k03-mc` → K03 data retention and classification
- `q-saa-1-3-k04-mc` / `-mr` → K04 encryption and key management
- `q-saa-1-3-s01-mc` / `-mr` → S01 compliance alignment
- `q-saa-1-3-s02-mc` / `-mr` → S02 encryption at rest
- `q-saa-1-3-s03-mc` / `-mr` → S03 encryption in transit
- `q-saa-1-3-s04-mc` / `-mr` → S04 key access policies
- `q-saa-1-3-s05-mc` / `-mr` → S05 backups and replication
- `q-saa-1-3-s06-mc` / `-mr` → S06 data access/lifecycle/protection policies
- `q-saa-1-3-s07-mc` / `-mr` → S07 key rotation and certificate renewal

## Doc URLs used (all fetched via the AWS Documentation MCP, accessed 2026-09-26)

- https://docs.aws.amazon.com/kms/latest/developerguide/concepts.html
- https://docs.aws.amazon.com/kms/latest/developerguide/rotate-keys.html
- https://docs.aws.amazon.com/kms/latest/developerguide/key-policies.html
- https://docs.aws.amazon.com/cloudhsm/latest/userguide/introduction.html
- https://docs.aws.amazon.com/AmazonS3/latest/userguide/UsingKMSEncryption.html
- https://docs.aws.amazon.com/AmazonS3/latest/userguide/ServerSideEncryptionCustomerKeys.html
- https://docs.aws.amazon.com/AmazonS3/latest/userguide/UsingClientSideEncryption.html
- https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/EBSEncryption.html
- https://docs.aws.amazon.com/acm/latest/userguide/acm-overview.html
- https://docs.aws.amazon.com/acm/latest/userguide/managed-renewal.html
- https://docs.aws.amazon.com/AmazonS3/latest/userguide/object-lock.html
- https://docs.aws.amazon.com/AmazonS3/latest/userguide/object-lock-managing.html
- https://docs.aws.amazon.com/amazonglacier/latest/dev/vault-lock.html
- https://docs.aws.amazon.com/aws-backup/latest/devguide/whatisbackup.html
- https://docs.aws.amazon.com/AmazonS3/latest/userguide/replication.html
- https://docs.aws.amazon.com/AmazonS3/latest/userguide/object-lifecycle-mgmt.html
- https://docs.aws.amazon.com/artifact/latest/ug/what-is-aws-artifact.html
- https://docs.aws.amazon.com/organizations/latest/userguide/orgs_manage_policies_tag-policies.html
- https://docs.aws.amazon.com/wellarchitected/latest/framework/sec-07.html

Each URL has a matching citation file (`cite-saa-1-3-*.json`, `accessed: "2026-09-26"`), all listed in
`lesson-1-3.json`'s `citationIds`.

## Verification performed

- Word count: 2,841 words (lesson-1-1 is 2,572; lesson-1-2 is 2,363 — in the same range as the approved
  model lessons, above the 1,200–2,500 guideline but consistent with precedent).
- 0 single-asterisk spans (checked programmatically after fixing one `*deny*` slip to `**deny**`).
- All 19 `citationIds` resolve to an existing file under `content/citations/`, each with `id` matching the
  filename and `accessed: "2026-09-26"`.
- Markdown restricted to `###`/`####` headings, `- ` bullets, `**bold**`, and backticks — no tables, links,
  numbered lists, or single-asterisk italics.
- File written with `json.load` / `json.dumps(..., indent=2, ensure_ascii=True) + "\n"` via
  `backend\.venv\Scripts\python.exe`, UTF-8 text mode, matching the existing file format.
- `python scripts\content_lint.py` → `PASS` (questions 429, aws 310, tf 119, labs 21+21, lessons 23).
- `objectiveIds`, `drillIds`, `labIds`, `exerciseIds`, `id`, `title`, `module`, `tier`, `practiceMode` left
  unchanged from the original file.

## Not done (out of scope for this change)

- Questions (`content/questions/q-saa-1-3-*.json`) were read but not edited, per instructions.
- `npm run build` / Terraform fixture checks not applicable (no frontend or lab-fixture changes).
- `python manage.py test workbook` not run (no backend/model changes); Lead Dev should still run it as
  part of the overall Definition of Done before closing the CR.
