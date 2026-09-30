# Reopen: shortest-is-key, writer report (11 questions)

Lengths are characters, listed a/b/c/d. Rank is the key's ascending length rank (1 = shortest, 4 = longest). Options not listed under a question are unchanged.

## 4-3

### k03 (key c)
- c: "Add DynamoDB Accelerator in front of the table." -> "Add DynamoDB Accelerator (DAX) in front of the table as a read cache."
- Lengths before 84/89/47/63 rank 1; after 84/89/69/63 rank 2.
- Added detail, lesson: "Two common AWS choices are ElastiCache and DAX." and "**DAX** is specialized for DynamoDB. It is API-compatible with DynamoDB clients and targets eventually consistent read acceleration."
- Distractors untouched. Rationale unchanged and still accurate.

### k05 (key d)
- d: "Use on-demand capacity mode for launch traffic." -> "Use on-demand capacity mode, billed per read/write request unit consumed."
- b: "Run provisioned capacity with auto scaling and switch between provisioned and on-demand several times each day." -> "Run provisioned capacity with auto scaling and switch modes several times each day."
- Lengths before 81/111/65/47 rank 1; after 81/83/65/73 rank 2.
- Added detail, lesson: "For on-demand mode, DynamoDB bills per read/write request unit consumed."
- b still a real option? Yes (auto scaling plus mode switching is real). Lesson sentence making it wrong: "You can switch from provisioned mode to on-demand mode up to **four times in a 24-hour rolling window**." Failing requirement (frequent switching) kept in "switch modes several times each day".
- Removed stem echo "launch" (a baseline flag is gone). Rationale unchanged, accurate.

### k09 (key d)
- d: "Use DynamoDB as the primary key-value datastore." -> "Use DynamoDB as the primary non-relational key-value datastore."
- c: "Use ElastiCache as the durable system of record for session data." -> "Use ElastiCache as the durable system of record."
- Lengths before 68/84/65/48 rank 1; after 68/84/48/63 rank 2 (c now 48, key 63).
- Added detail, lesson: "Use **non-relational databases** like DynamoDB when low-latency key-based access at massive scale is the main requirement."
- c still a real option? Yes. Lesson sentence making it wrong: "Caching does not replace source-of-truth durability." and "Cache tiers are expendable; core database state is not." Failing requirement kept in "durable system of record".
- Rationale unchanged, accurate.

### s02 (key b)
- b: "Use PostgreSQL on Amazon RDS." -> "Use PostgreSQL on Amazon RDS or an Aurora-compatible offering."
- c: "Use MySQL on Amazon RDS with a larger instance class for extension compatibility." -> "Use MySQL on Amazon RDS with a larger instance class."
- Lengths before 84/29/81/51 rank 1; after 84/62/53/51 rank 3. "Advanced JSON" not put in the key.
- Added detail, lesson: "both MySQL and PostgreSQL can run on RDS and Aurora-compatible offerings".
- c still a real option? Yes. Lesson sentence making it wrong: "Choose PostgreSQL when you need advanced JSON handling, complex queries, or custom extensions." (MySQL, larger instance or not, is the compatibility-focused choice). Rationale unchanged, accurate.

## 4-1

### k05 (key a)
- a: "AWS Backup" -> "AWS Backup with a backup plan"
- b: "The EBS Snapshot Archive tier" -> "EBS Snapshot Archive tier"
- d: "EFS Lifecycle Management" -> "EFS Lifecycle Management policy"
- Lengths before 10/29/23/24 rank 1; after 29/25/23/31 rank 3.
- Parallel form: every option is a service name plus at most a short noun suffix; none is a justification.
- Added detail, lesson: "**AWS Backup** centralizes policy-driven backup across many AWS resource types" and "A backup plan's lifecycle can transition older recovery points to a **cold storage tier** automatically".
- b and d still real options? Yes, both unchanged in substance. Making them wrong: "the **EBS Snapshot Archive** tier for snapshots" and "**EFS Lifecycle Management** for files" (K07): single-service lifecycle features, not a cross-service backup. Rationale unchanged, accurate.

### s07 (key c)
- c: "Deploy AWS Storage Gateway" -> "Deploy AWS Storage Gateway for hybrid storage access"
- d: "Schedule a recurring AWS DataSync task between the on-premises share and S3" -> "Schedule a recurring AWS DataSync task to copy the data to S3"
- Lengths before 40/56/26/75 rank 1; after 40/56/52/61 rank 2.
- Added detail, lesson: "calls for **Storage Gateway** instead - that is hybrid access, not a migration you finish and turn off."
- d still a real option? Yes. Lesson sentence making it wrong: DataSync's job is "A one-time or recurring bulk copy ... into S3, EFS, or FSx", while "keep serving on-premises apps from a local cache backed by AWS" is Storage Gateway (K08 tip). Failing requirement (no local cache serving) intact; the recurring vs one-time distinction is kept. Rationale mentions the share and S3 in general terms; still accurate, unchanged.

### s06 (key b, unchanged)
- c: "Copy the EBS snapshots into an S3 Glacier Deep Archive bucket manually" -> "Copy the EBS snapshots into S3 Glacier Deep Archive"
- Rationale: "Copying snapshots into an S3 Glacier bucket manually treats" -> "Copying snapshots into S3 Glacier Deep Archive treats".
- Lengths before 81/55/70/63 rank 1; after 81/55/51/63 rank 2. Archive-tier price/minimum-duration facts not used since the key is unchanged.
- c still a real option? Yes. Lesson sentence making it wrong: "Choose direct **S3 Glacier** storage classes when the data being archived is already object data rather than a resource snapshot."

### k03 (key c)
- a: "AWS Cost Explorer" -> "AWS Cost Explorer custom reports"
- b: "S3 Storage Lens" -> "S3 Storage Lens metrics"
- c: "AWS Budgets" -> "AWS Budgets cost and usage budgets"
- d: "AWS Billing Conductor" -> "AWS Billing Conductor chargeback rates"
- Lengths before 17/15/11/21 rank 1; after 32/23/34/38 rank 3. All four got a parallel suffix; no stem wording in the key.
- Lesson support: "visualizes and forecasts cost and usage with built-in and custom reports" (a); "a free metrics tier and a paid advanced tier" (b); "watches actual or forecasted cost or usage against a threshold" (c); "model custom, chargeback-style rates per account or business unit" (d).
- Distractors still real options? Yes, all. Lesson sentence making them wrong: "**AWS Budgets** does not report history; it watches ... and alerts" (Cost Explorer is reporting); Storage Lens is S3 visibility; Billing Conductor is chargeback modeling. Rationale unchanged.

## 1-3

### k04 (key d)
- d: "AWS CloudHSM" -> "AWS CloudHSM with a multi-AZ cluster"
- Rationale: "AWS CloudHSM provisions single-tenant" -> "AWS CloudHSM, deployed as a multi-AZ cluster, provisions single-tenant".
- Lengths before 35/31/51/12 rank 1; after 35/31/51/36 rank 3. "PKCS #11" not added.
- Added detail, lesson: "A CloudHSM cluster gets its redundancy and high availability from spreading its HSMs across multiple Availability Zones".
- Distractors unchanged.

### s01 (key a)
- a: "Download the report from AWS Artifact" -> "Download the report on demand from AWS Artifact"
- b: "Export the current findings from AWS Config for the Regions in scope" -> "Export AWS Config findings for the in-scope Regions"
- c: "Open a support case asking AWS to email the report directly to the auditor" -> "Open a support case asking AWS for the report"
- Rationale: "adds a manual, multi-day round trip" -> "adds a manual round trip" (multi-day is not taught).
- Lengths before 37/68/74/64 rank 1; after 47/51/45/64 rank 2.
- Added detail, lesson: "**AWS Artifact** gives on-demand, no-cost downloads of AWS's own compliance reports".
- b and c still real options? Yes. Lesson sentence making them wrong: Config is for "prove our S3 buckets stay encrypted going forward" (customer resources), and the tip "get a copy of AWS's own SOC 2 report for our auditor" is AWS Artifact, so a support case is the manual alternative.
- Note: my first attempt dropped "report" from c and created a new stem-echo flag ("report -> a"); I restored "the report" in c and the flag is gone. The key/c length gap is only 2 characters (47 vs 45).

### s05 (key a)
- a: "AWS Backup" -> "AWS Backup with a backup plan and lifecycle rules"
- Lengths before 10/34/58/56 rank 1; after 49/34/58/56 rank 2.
- Added detail, lesson: "it centralizes backup plans across many services ... applies lifecycle rules that move older backups to a low-cost cold storage tier". Rationale unchanged, accurate. Distractors unchanged.

## Script outputs (final run)

- content_lint.py: PASS
- q1_batch_check.py 4-3: longest-is-key 3/14 = 21%, shortest-is-key 4/14 = 29%, RESULT PASS
- q1_batch_check.py 4-1: longest 6/21 = 29%, shortest 6/21 = 29%, RESULT WARN (pre-existing lesson "Snowball" warning only)
- q1_batch_check.py 1-3: longest 3/11 = 27%, shortest 2/11 = 18%, RESULT WARN (pre-existing since/must warnings in s02-mr, s03-mc, s04-mr, s06-mr; none on my questions)
- distractor_type_audit.py: 4-3 PASS; 1-3 PASS; 4-1 RESULT FAIL on EBS 26%, FSx 23%, EFS 23%, S3 Glacier 17%. I did not add or remove any of these keywords in any question (checked by inspection; baseline could not be run without git), so I attribute them to the existing content.
- stem_echo_check.py flags among my 11: 4-3 k03 dynamodb, 4-1 k05 backup, 1-3 s05 backup (all baseline). 4-3 k05 "launch" is removed. No new flag. Task-level RESULT is FAIL because of flags in other questions (advisory for these closed tasks).
- key_text_diff.py vs 289014c: 4-3 reports 4 mismatches, 4-1 reports 3, 1-3 reports 3. The script compares key option text, so each mismatch is a key I lengthened on purpose (4-3 k03, k05, k09, s02; 4-1 k03, k05, s07; 1-3 k04, s01, s05). `correctAnswerIds` and the choice ids and order are unchanged in all 11 files, so no question changed which option is correct. The literal "0 mismatches" target is not met because the keys' text changed.

## Lesson additions requested

None.
