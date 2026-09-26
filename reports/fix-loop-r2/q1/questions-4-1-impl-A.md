# Task 4.1 — Writer A: 15 knowledge (k*) questions

Covers `SAA-4.1-K01` through `SAA-4.1-K11`, including the four MR files (K02, K05, K08, K11). All 15 stems open with a company or team noun phrase. `q-saa-4-1-s*` files are untouched (Writer B's scope).

## Per-question table

| Question | Objective | What it tests | Key | Key — lesson quote | Distractors — lesson quotes (why wrong) |
|---|---|---|---|---|---|
| k01-mc | K01 | Requester Pays vs. cost-visibility/optimization tools | Requester Pays | "the account making the request pays for the request and any data downloaded, while the owner still pays only for storage" | Intelligent-Tiering: "optimize storage costs by automatically moving data... without performance impact" (optimizes owner's own cost, not who pays); cost allocation tags: "break spend down by team, project, or environment" (reporting, not cost-shifting); Storage Lens: "organization-wide visibility... cost-optimization recommendations" (visibility, not billing control) |
| k02-mc | K02 | Consolidated billing vs. Budgets/tags/CUR | Consolidated billing | "rolls every member account's usage into one payer account... to share the benefit of Reserved Instances and Savings Plans" | Budgets: "watches actual or forecasted cost or usage against a threshold... sends an alert" (alerting, not combining usage); cost allocation tags: per-account breakdown, not cross-account merge; CUR: "most granular line-item billing data" per account, not a combining mechanism |
| k02-mr | K02 | Cost allocation tags AND consolidated billing (two distinct needs) | Cost allocation tags + consolidated billing | Same lesson lines as k02-mc plus "must be activated in the Billing console before they appear as columns in Cost Explorer" | Budgets: alerts only; CUR (single account): granular but not combined; Billing Conductor: "model custom, chargeback-style rates... without changing what AWS actually charges" (rate modeling, not RI-sharing or tag breakdown) |
| k03-mc | K03 | Budgets vs. Cost Explorer/Storage Lens/Billing Conductor | AWS Budgets | "watches actual or forecasted cost or usage against a threshold... and sends an alert" | Cost Explorer: "visualizes and forecasts" (no push alert); Storage Lens: S3-specific usage/cost insights, not billing alerts; Billing Conductor: chargeback rate modeling, not alerting |
| k04-mc | K04 | S3's no-provisioning billing model vs. EBS/FSx/Backup | Amazon S3 | "bills only for what you store... no capacity to provision, so it is normally the cheapest option for object data at scale" | EBS: "pay for what you provisioned whether or not you use it"; FSx: "prices for a managed, purpose-built engine... usually the most expensive of the four"; AWS Backup: not a primary storage service at all |
| k05-mc | K05 | AWS Backup's cross-service + incremental model vs. single-service tools | AWS Backup | "centralizes policy-driven backup across many AWS resource types... most supported resources back up incrementally" | EBS Snapshot Archive: only lowers cost of existing EBS snapshots (K10/S06 citation); Glacier Deep Archive: S3 object archival, not a backup mechanism; EFS Lifecycle Management: moves files between EFS classes, not a backup tool |
| k05-mr | K05 | Building an AWS Backup plan AND its cold-storage lifecycle | AWS Backup plan (assign resources) + plan lifecycle to cold storage | "after the first, full backup, most supported resources back up incrementally" + "must stay in cold storage at least 90 days" | EBS Snapshot Archive: EBS-only; S3 Lifecycle on an export bucket: manages only the exported copies, not the live resources; EFS Lifecycle Management: EFS-only, not a backup mechanism |
| k06-mc | K06 | gp3 vs. gp2/io2/sc1 cost tradeoffs | Migrate gp2 to gp3 | "gp3... about 20% lower price per GiB than gp2 at equivalent performance... provisions IOPS and throughput independently of size" | io2: "premium worth paying only when a workload genuinely needs guaranteed high IOPS" (raises cost here); sc1: "price by throughput rather than IOPS," a different performance profile; enlarging gp2: "gp2 ties IOPS to size" so more size = more cost |
| k07-mc | K07 | S3 Lifecycle (scheduled, known pattern) vs. Intelligent-Tiering/Requester Pays/Batch Operations | S3 Lifecycle configuration | "S3 Lifecycle rules for objects... a number of days since creation or last access triggers a transition" | Intelligent-Tiering: "saving the per-object monitoring fee... for handling unknown or changing access" (pattern here is known, so Lifecycle is cheaper); Requester Pays: changes who pays, not storage class; S3 Batch Operations: one-time bulk job, not an ongoing age-based policy (S01 section) |
| k08-mc | K08 | Transfer Family vs. DataSync/Storage Gateway/FSx for an external SFTP need | AWS Transfer Family | "managed SFTP, FTPS, AS2, and FTP endpoints... for exchanging files with external partners... without standing up and patching EC2-hosted FTP servers" | DataSync: bulk/one-time transfer job, not an ongoing SFTP endpoint; Storage Gateway: NFS/SMB share for on-prem apps, not SFTP; FSx for Windows: internal SMB file system, not a partner exchange point |
| k08-mr | K08 | DataSync (finish migration) AND Storage Gateway (ongoing hybrid access) | AWS DataSync + AWS Storage Gateway | "lower-cost choice for a bulk, one-time, or recurring online migration" + "keep serving on-premises apps from a local cache backed by AWS" | Transfer Family: external partner SFTP, not this scenario; FSx for NetApp ONTAP: needs that specific engine, not a migration/gateway tool; AWS Backup: backup policy, not migration or hybrid access |
| k09-mc | K09 | Intelligent-Tiering vs. Standard-IA/Glacier Flexible/scheduled Lifecycle for unpredictable access | S3 Intelligent-Tiering | "designed for data that has unknown or changing access patterns... no retrieval fees" | Standard-IA: "Amazon S3 charges a retrieval fee for these objects" (costly on the frequently-fetched viral photos); Glacier Flexible Retrieval: minutes-to-hours retrieval, too slow; scheduled Lifecycle rule: assumes a stable, predictable pattern this isn't |
| k10-mc | K10 | Glacier Flexible Retrieval's retrieval-tier/cost balance vs. Instant Retrieval/Deep Archive/Standard-IA | S3 Glacier Flexible Retrieval | "Standard retrieval – Typically restores the object in 3–5 hours" + lower cost than Instant Retrieval/Standard-IA | Glacier Instant Retrieval: meets timing but costs more for rarely-accessed data; Glacier Deep Archive: cheapest, but "Standard retrieval... within 12 hours" exceeds "a few hours"; Standard-IA: meets timing but priced well above Glacier |
| k11-mc | K11 | S3's billing model vs. EBS/FSx (provisioned) and EFS (POSIX mismatch) | Amazon S3 | "has no capacity to provision and needs no minimum object size or duration... you pay per GB stored plus requests" | EBS: "must be sized... in advance, and that provisioned capacity bills whether or not it is used"; FSx for Lustre: "requires provisioning a file system's storage... capacity similarly to EBS"; EFS: usage-based but "exists specifically to provide a POSIX file interface" the workload doesn't need |
| k11-mr | K11 | EBS (block, provisioned) AND S3 (object, usage-based) vs. FSx/EFS/Storage Gateway | Amazon EBS + Amazon S3 | "must be sized... and provisioned for IOPS and throughput" + "billed only for what's actually stored" | FSx for OpenZFS: file storage requiring provisioning, not block or object; EFS: usage-based but POSIX-file storage, not block or object; Storage Gateway: a hybrid access gateway, not a storage type at all |

## Distractor-type table (this writer's 15 questions, cap 2 per type)

| Type (named wrong AWS feature) | Count | Questions |
|---|---|---|
| S3 Intelligent-Tiering (as distractor) | 2 | k01-mc, k07-mc |
| Cost allocation tags (as distractor) | 2 | k01-mc, k02-mc |
| S3 Storage Lens (as distractor) | 2 | k01-mc, k03-mc |
| AWS Budgets (as distractor) | 2 | k02-mc, k02-mr |
| AWS Cost and Usage Report / Data Exports (as distractor) | 2 | k02-mc, k02-mr |
| AWS Billing Conductor (as distractor) | 2 | k02-mr, k03-mc |
| AWS Cost Explorer (as distractor) | 1 | k03-mc |
| Amazon EBS (generic, "must provision") (as distractor) | 2 | k04-mc, k11-mc |
| Amazon FSx for Windows File Server (as distractor) | 2 | k04-mc, k08-mc |
| AWS Backup (as distractor) | 2 | k04-mc, k08-mr |
| EBS Snapshot Archive tier (as distractor) | 2 | k05-mc, k05-mr |
| S3 Glacier Deep Archive (as distractor) | 2 | k05-mc, k10-mc |
| EFS Lifecycle Management (as distractor) | 2 | k05-mc, k05-mr |
| S3 Lifecycle rule (generic scheduled rule, as distractor) | 2 | k05-mr, k09-mc |
| EBS io2 / Provisioned IOPS (as distractor) | 1 | k06-mc |
| EBS sc1 (as distractor) | 1 | k06-mc |
| EBS gp2 (resize, as distractor) | 1 | k06-mc |
| S3 Requester Pays (as distractor) | 1 | k07-mc |
| S3 Batch Operations (as distractor) | 1 | k07-mc |
| AWS DataSync (as distractor) | 1 | k08-mc |
| AWS Storage Gateway (as distractor) | 2 | k08-mc, k11-mr |
| AWS Transfer Family (as distractor) | 1 | k08-mr |
| Amazon FSx for NetApp ONTAP (as distractor) | 1 | k08-mr |
| S3 Standard-IA / One Zone-IA (as distractor) | 2 | k09-mc, k10-mc |
| S3 Glacier Flexible Retrieval (as distractor) | 1 | k09-mc |
| S3 Glacier Instant Retrieval (as distractor) | 1 | k10-mc |
| Amazon FSx for Lustre (as distractor) | 1 | k11-mc |
| Amazon EFS (generic / POSIX mismatch, as distractor) | 2 | k11-mc, k11-mr |
| Amazon FSx for OpenZFS (as distractor) | 1 | k11-mr |

No type exceeds 2 uses across these 15 questions. (Requester Pays, DataSync, Cost Explorer, io2, sc1, gp2-resize, Batch Operations, Transfer Family, FSx-ONTAP, Glacier Instant, Glacier Flexible, and FSx-OpenZFS are single-use here, leaving headroom for Writer B's 20 `s*` questions to stay under the whole-task cap of 5/35 named in the brief.)

## Checks run

- `backend\.venv\Scripts\python.exe scripts\q1_batch_check.py 4-1`: zero FAIL/WARN lines reference any `q-saa-4-1-k*` file. Task-level FAILs (`duplicate 6-word openings`, `longest-is-key 12/21`, i.e. across all 21 files scored so far) are driven by the still-placeholder `s*` files, out of scope for this writer per the brief.
- `backend\.venv\Scripts\python.exe scripts\content_lint.py`: PASS (questions 429, aws 310, tf 119, labs 21+21, lessons 23).
- Manual scan of all 15 files' choice text for the banned giveaway words (`since`, `even though`, `which does not`, `despite`, `requiring`, `must`, `without changing`): none found.
- Stem-opening check: all 15 stems begin with a distinct company/team noun phrase; no two share their first six words.

## Files touched

- `content/questions/q-saa-4-1-k01-mc.json`
- `content/questions/q-saa-4-1-k02-mc.json`
- `content/questions/q-saa-4-1-k02-mr.json`
- `content/questions/q-saa-4-1-k03-mc.json`
- `content/questions/q-saa-4-1-k04-mc.json`
- `content/questions/q-saa-4-1-k05-mc.json`
- `content/questions/q-saa-4-1-k05-mr.json`
- `content/questions/q-saa-4-1-k06-mc.json`
- `content/questions/q-saa-4-1-k07-mc.json`
- `content/questions/q-saa-4-1-k08-mc.json`
- `content/questions/q-saa-4-1-k08-mr.json`
- `content/questions/q-saa-4-1-k09-mc.json`
- `content/questions/q-saa-4-1-k10-mc.json`
- `content/questions/q-saa-4-1-k11-mc.json`
- `content/questions/q-saa-4-1-k11-mr.json`

No `s*` files, `lesson-4-1.json`, or citation files were modified.
