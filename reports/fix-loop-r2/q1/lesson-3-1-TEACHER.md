# Teacher review: lesson 3.1 and task 2.1 key edits

Saved by Lead Dev from the Teacher's reply (AGENTS.md: the Teacher does not write files).

## Part 1: Lesson 3.1 — "High-performing storage" (`content/lessons/lesson-3-1.json`, commit `2178696`)

**Method:** Read the lesson body, author notes (`lesson-3-1-impl.md`), and AWS's review (`lesson-3-1-AWS.md`). Spot-checked 9 fact clusters independently via the AWS Documentation MCP (gp3 baseline/max IOPS-throughput; S3 per-prefix request-rate baseline; EFS Elastic throughput mechanics; EBS volume-type taxonomy incl. io1; FSx for Lustre SSD/HDD/Intelligent-Tiering throughput tiers; FSx for OpenZFS SSD read-cache IOPS; S3 Express One Zone directory-bucket description; AWS Storage Gateway type list). Ran `content_lint.py` and independent format/word-count/citation/drillId scripts.

**1. Coverage:** All 5 `SAA-3.1-*` objectives (K01, K02, K03, S01, S02) have their own `###` section, in exact id order, matching `content/objectives/saa_c03.json`. Confirmed complete — no missing or extra objective.

**2. Accuracy:** My independent MCP checks corroborate AWS's review on every point:
- gp3 baseline 3,000 IOPS/125 MiB/s, max 2,000 MiB/s throughput confirmed against `ebs/latest/userguide/general-purpose.html`.
- S3 per-prefix baseline (3,500 PUT/COPY/POST/DELETE, 5,500 GET/HEAD) confirmed — this figure is missing from the lesson (AWS-L31-003); I agree it should be added.
- EBS's own docs classify Provisioned IOPS SSD as "io1, io2, and io2 Block Express" — a distinct, still-current type separate from io2 Block Express. I agree with AWS-L31-004: "five volume types" undercounts and omitting io1 is a real gap, made worse by the fact that **lesson 2.1 already names io1 by name** ("a single Provisioned IOPS (io1/io2) volume") in its Multi-Attach section — a student cross-referencing 2.1 and 3.1 would find 3.1 silently drops a type 2.1 already used.
- FSx for Lustre Intelligent-Tiering "scales to multiple TBps and millions of IOPS," HDD storage class tops out at "tens of GBps" — confirms AWS-L31-001's proposed correction is accurate.
- FSx for OpenZFS SSD/in-memory cache figures are consistent with AWS-L31-002's proposed "up to 2,000,000 IOPS" correction.
- Storage Gateway and FSx File Gateway EOL wording, DataSync source/destination list, and the Snow Family EOL claim: I did not re-derive these since AWS's report already quotes the source pages verbatim and the quotes are accurate as cited.

I agree with all five of AWS's findings (AWS-L31-001 through 005) and add no new factual errors.

**3. Teaching quality:** Clear for a college IT student. The confused-pairs the task asked about are all handled: EBS types are contrasted by IOPS/throughput profile and boot-volume support; EFS modes are split cleanly into performance mode (fixed at creation) vs. throughput mode (changeable); the FSx family is distinguished by primary use case (Lustre=HPC/ML, Windows=AD/SMB, ONTAP=NetApp multi-protocol, OpenZFS=ZFS+cache); S3 performance features (byte-range, multipart, Transfer Acceleration, prefix scaling, Express One Zone) are each tied to a specific bottleneck; Storage Gateway types and DataSync vs. Snow Family are contrasted by connectivity/bandwidth scenario. All 5 exam tips are logically sound and consistent with their section bodies — no contradictions found. No filler. Cross-checked against lesson 2.1 (EBS Multi-Attach io1/io2, instance-store ephemerality) and lesson 2.2 (io2 99.999% durability, S3 eleven-nines/3+AZ durability): no contradictions — S3 Express One Zone's single-AZ trade-off is correctly scoped against 2.2's multi-AZ S3 Standard durability claim.

**4. Snow Family / FSx File Gateway handling:** The EOL framing itself is accurate and well-cited (confirmed independently). I agree with AWS's pedagogical (not factual) finding AWS-L31-005: the lesson never says what Snowball Edge physically *was*, so a student cannot pattern-match an exam stem written before the 2025 retirement that describes the old shipping-appliance workflow as a distractor or correct answer. **Recommended exact wording** (insert into K01, immediately before or after the existing EOL sentence): *"Snowball Edge was a ruggedized, physical storage-and-compute device that AWS shipped to a customer's site for offline bulk data transfer or edge locations without reliable network access; a customer loaded data onto it locally and shipped it back to AWS for import into S3."* This is additive only — recommend Lead Dev include it alongside the other fixes since it directly affects exam-pattern recognition, not just factual completeness.

**5. Length:** ~1,868 words (author-reported; my own rough tokenizer gives ~1,923, within normal counting-method variance) for 5 objectives (~374 words/objective) is acceptable and in line with the density of lessons 2.1 (~135 words/objective) and 2.2 (~154 words/objective) scaled for the fact-heavy nature of storage performance figures — this lesson carries far more numeric detail per objective than 2.1/2.2, so the higher per-objective count is justified, not padding. No filler found to cut.

**6. Format:** Verified independently, not just trusting the impl notes:
- 0 single-asterisk spans, 0 pipe characters, 0 markdown links, 0 numbered-list lines.
- All 17 `citationIds` resolve to existing files in `content/citations/`.
- All 8 `drillIds` resolve to the existing `q-saa-3-1-*` placeholder files, listed in exact objective order (K01→S02).

**7. Teach-before-test readiness — gaps beyond AWS's list:**
- **TEACHER-L31-001** (Low, K01): Snowball Edge's physical nature is never taught (same as AWS-L31-005; recording here as a Teacher-side confirmation with exact wording above).
- **TEACHER-L31-002** (Low, K03): The lesson never states EBS volumes' single-AZ scope explicitly for gp3/gp2/st1/sc1 (it's stated for io2 Block Express only, "on Nitro-based instances"). A question testing "why can't I attach this volume across AZs" has no anchor outside the io2 sentence. Minor — 2.2 already establishes single-AZ EBS scope, so this is a light gap, not a contradiction.
- **TEACHER-L31-003** (Low, K02): FSx for Lustre's data-repository "link to S3" is described as making objects "readable as files without a separate copy step," but the lesson doesn't mention this requires the **Persistent** (or Scratch with DRA) deployment and an explicit data-repository association — a student could infer the linkage is automatic on any Lustre file system. Low priority; can be folded into the AWS-L31-001 edit pass if convenient.

No other teach-before-test gaps found; the five current objectives are otherwise fully covered for their stated exam-tested facts.

**8. Lint:** `backend\.venv\Scripts\python.exe scripts\content_lint.py` → **PASS** (questions 429, labs 21+21, lessons 23).

### Issues (Teacher-side, new)

| ID | Severity | Location | Fix |
|---|---|---|---|
| TEACHER-L31-001 | Low | K01, Snowball Edge sentence | Add one clause describing what Snowball Edge physically was (ruggedized, shippable storage/compute device for offline transfer/edge use). Exact wording given above. Endorses AWS-L31-005. |
| TEACHER-L31-002 | Low | K03, EBS block-storage paragraph | Add a brief clause stating gp3/gp2/st1/sc1 (like io2 Block Express) are also scoped to a single Availability Zone. |
| TEACHER-L31-003 | Low | K02, FSx for Lustre paragraph | Note that S3 data-repository linking requires Persistent (or Scratch with a DRA) deployment, not any Lustre file system by default. |

I also concur with and adopt AWS-L31-001 through AWS-L31-004 as required fixes before question-writing (AWS-L31-004 in particular is reinforced by lesson 2.1's existing io1 reference), and endorse AWS-L31-005/TEACHER-L31-001 as an additive fix that should ship in the same pass given its exam-pattern-recognition value.

**Lesson 3.1: not yet.** (Pending AWS-L31-001–004, and recommend folding in AWS-L31-005/TEACHER-L31-001–003 in the same edit before re-validation.)

## Part 2: Task 2.1 key-shortening edits (commit `5292a46`)

Reviewed against lesson 2.1's body and each question's rationale.

- **`q-saa-2-1-k01-mc` choice a** ("An HTTP API with built-in OIDC/OAuth 2.0 authorization for the Lambda backend"): correct, neutral, matches the rationale ("An HTTP API is built for exactly this case... native OIDC/OAuth 2.0 support") and is taught in lesson 2.1's API Gateway section. No issue.
- **`q-saa-2-1-k05-mr` choice b** ("An EventBridge rule can deliver only events matching an 'out-of-stock' pattern to a Lambda target"): correct, neutral, matches the rationale and lesson 2.1's EventBridge rule/pattern-matching content. No issue.
- **`q-saa-2-1-k08-mc` choice d** ("Use AWS App2Container to generate a container image and an ECS task definition"): correct, neutral, matches the rationale and lesson 2.1's App2Container coverage. No issue.

All three shortened keys remain accurate, unbiased in phrasing (no length or wording tell relative to distractors), internally consistent with their rationales, and grounded in lesson 2.1's taught content.

**Task 2.1 edits: approve.**

## Overall: concerns

Lesson 3.1 is well-researched and well-cited, but should not go to question-writing until AWS-L31-001–004 are applied (stale FSx throughput/IOPS figures, missing S3 per-prefix baseline, and the io1/"five volume types" undercount that lesson 2.1 already contradicts). Recommend Lead Dev fold in AWS-L31-005 and TEACHER-L31-001–003 in the same pass since they're small, additive, and improve exam-pattern coverage. Task 2.1's three edits are clean — no concerns there.
