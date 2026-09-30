# Reopen shortest-is-key: reviews

## Technical review (c417d0c)

Method: read all 11 files (current text, and old text via the writer's report), lessons for 4-3/4-1/1-3, AWS docs MCP (DynamoDB on-demand request units, AWS Budgets budget types, Billing Conductor showback/chargeback). Key ranks re-computed from the files: all 11 keys sit at length rank 2 or 3, choice ids/order/correctAnswerIds unchanged. Scripts: `q1_batch_check.py` 4-3 PASS, 4-1 WARN (pre-existing Snowball lesson warning), 1-3 WARN (pre-existing since/must in other questions). `stem_echo_check.py` RESULT FAIL on all three tasks, but none of the flags on the 11 are new: 4-3 k03 dynamodb, 4-1 k05 backup, 1-3 s05 backup, all baseline structural (the stem names the object). 4-3 k05, k09, s02, 4-1 k03, s06, s07, 1-3 k04, s01 have no flag.

### Verdicts

- 4-3 k03: OK. DAX "as a read cache" is accurate. Rank 2.
- 4-3 k05: OK. "Billed per read/write request unit consumed" is accurate (read request units and write request units, DynamoDB on-demand docs; also verbatim in the lesson). Rank 2. See AWS-RSK-002 (low, optional).
- 4-3 k09: OK. Rank 2. Distractor c still wrong on "durable system of record" (taught in lesson).
- 4-3 s02: concerns, AWS-RSK-001 (medium): "Aurora-compatible offering" is loose wording.
- 4-1 k05: OK. Rank 3. Key suffix "with a backup plan" mirrors the stem's "one retention policy" only loosely; acceptable.
- 4-1 s07: OK. Rank 2. All distractors real and still fail (one-time cutover, external partner endpoints, no local cache).
- 4-1 s06: OK with AWS-RSK-003 (low, pre-existing, optional). Key unchanged, rank 2.
- 4-1 k03: OK. All four descriptors are real features. Rank 3. Answers to the Lead Dev concern below.
- 1-3 k04: OK. A CloudHSM cluster can span AZs, so the added detail is accurate. Rank 3.
- 1-3 s01: OK with AWS-RSK-004 (low, optional). Rank 2.
- 1-3 s05: OK. "Backup plan and lifecycle rules" is accurate (plans carry lifecycle rules). Rank 2.

### Rulings on the Lead Dev concerns

1. 4-3 s02: "Aurora-compatible offering" is accurate only in a loose sense. It is not an AWS product name, and Aurora MySQL-Compatible also exists, so a strict reader can parse "PostgreSQL ... or an Aurora-compatible offering" as PostgreSQL on RDS or any Aurora. The correct choice is still unambiguous (the only PostgreSQL option), but the wording should name the engine. The lesson says only "Aurora variants" and "Aurora-compatible offerings"; it does not teach "Aurora PostgreSQL". Aurora PostgreSQL appears as an option in 4-3 k09, so the name is familiar in this task. Use AWS-RSK-001 text (57 chars, rank 3 vs 84/53/51).
2. 4-1 k03: "AWS Budgets cost and usage budgets" is accurate terminology (AWS Budgets has cost budgets and usage budgets, per docs). It is slightly redundant ("Budgets ... budgets") but not misleading, and the parallel suffixes on all four options remove the descriptor asymmetry. Keep. Distractor descriptors are real: Cost Explorer has built-in and custom reports (lesson); S3 Storage Lens has free and advanced metrics; Billing Conductor is documented for showback and chargeback with custom pricing plans/rates. "Chargeback rates" is loose but correct in spirit.
3. 4-3 k05: "billed per read/write request unit consumed" is accurate. It is a descriptor the other three options lack (only b has a longer descriptor), but it is a fact about the mode, not a restatement of the stem ("minimal capacity planning"), so it is not a tell.

### Findings

- AWS-RSK-001 | Medium | q-saa-4-3-s02-mc choice b (key). Loose, non-product wording "an Aurora-compatible offering". Replace with: `Use PostgreSQL on Amazon RDS or Amazon Aurora PostgreSQL.` (57 chars; lengths become a 84, b 57, c 53, d 51, key rank 3). Rationale needs no change. No lesson addition required; optional lesson sentence: "Amazon Aurora is offered in MySQL-compatible and PostgreSQL-compatible editions."
- AWS-RSK-002 | Low, optional | q-saa-4-3-k05-mc choice b. The lesson says you can switch modes up to four times per 24 hours, so "switch modes several times each day" is arguably within the limit; the option really fails "minimal capacity planning overhead" (auto scaling still needs min/max settings) rather than the switching cap. The rationale ("constrained and adds operational complexity") already covers both. If changed, use: `Run provisioned capacity with auto scaling and target tracking policies.` (72 chars; key 73 becomes rank 3 of 81/72/65/73, still rank 3, acceptable). Not required to close.
- AWS-RSK-003 | Low, optional, pre-existing | q-saa-4-1-s06-mc choice c. "Copy the EBS snapshots into S3 Glacier Deep Archive" is not a native operation (snapshots live in AWS-managed storage); removing "manually" makes it read as a real feature. The rationale states exactly this, so it still reads as a plausible-but-wrong idea. No change required for this reopen.
- AWS-RSK-004 | Low, optional | q-saa-1-3-s01-mc choice a (key). "on demand" half-echoes the stem's "least effort" (it is also the rationale's justification). Not flagged by the stem-echo script. If tightened, use: `Download the report from AWS Artifact Reports` (45 chars; ties c at 45, rank 1-2, so use instead `Download the AWS compliance report from AWS Artifact` at 52 chars, rank 3 of 52/51/45/64). Not required to close. Also choice b "AWS Config findings" is loose (Config reports compliance results), unchanged in substance from the old text.

No banned words (since, even though, which does not, despite, requiring, must, without changing, so that) appear in any changed choice. Rationales reference options by content, no letters, and remain consistent with the new option text.

Reopen: not yet
Overall: concerns

(Only AWS-RSK-001 blocks; apply it, re-run `q1_batch_check.py 4-3` and `stem_echo_check.py 4-3`, then Reopen becomes "close". RSK-002 to 004 are optional.)

---

## Teacher review (c417d0c)

Saved by Lead Dev from the Teacher's reply (condensed; the proposed texts are verbatim).

**Plan conditions**
- Parallel option form: met in all 11.
- A quoted lesson sentence for every added detail: met, except for the weak case in RSK-003.
- Every key is now at rank 2–3.

**Verdicts**
- **Approve:** 4-3 k03, 4-3 k05, 4-1 k05, 4-1 s06, 1-3 k04, 1-3 s05.
- **Approve with a note:** 4-1 s07 (RSK-004).
- **Approve with a fix:** 4-3 k09 (RSK-002), 4-3 s02 (RSK-001), 4-1 k03 (RSK-003, optional), 1-3 s01 (RSK-006).

**Findings**
- **TEACHER-RSK-001 (Low)**, 4-3 s02 key. "An Aurora-compatible offering" is vague. Proposed: `Use PostgreSQL on Amazon RDS or Aurora PostgreSQL-Compatible.`
- **TEACHER-RSK-002 (Low–Medium)**, 4-3 k09 key. "Non-relational key-value" restates the stem's "by key … without SQL joins". Proposed: `Use Amazon DynamoDB as the primary key-value datastore.`
- **TEACHER-RSK-003 (Low, optional)**, 4-1 k03 key. "Cost and usage budgets" is close to taught but is not quoted from the lesson. Optional: `AWS Budgets threshold alerts`.
- **TEACHER-RSK-004 (Low, note)**, 4-1 s07. "For hybrid storage access" is a category label, not a justification. No change.
- **TEACHER-RSK-005 (Low, pre-existing, note)**, 4-1 s06 choice c. Dropping "manually" makes it a realistic option. No change.
- **TEACHER-RSK-006 (Low–Medium)**, 1-3 s01 key. "On demand" hints at the stem's "least effort". Proposed: `Download the report from the AWS Artifact console`.

Reopen: not yet · Overall: concerns (approve once RSK-001, 002 and 006 are applied)

---

## Lead Dev fix pass (after both reviews)

| Item | Decision | Applied text | Length rank |
|---|---|---|---|
| AWS-RSK-001 = TEACHER-RSK-001 (4-3 s02) | Applied, AWS wording. It names the engine; the Teacher's version was equivalent. | `Use PostgreSQL on Amazon RDS or Amazon Aurora PostgreSQL.` | 57 against 51/53/84, rank 3 |
| TEACHER-RSK-002 (4-3 k09) | Applied, Teacher wording. AWS had marked k09 OK and did not object. | `Use Amazon DynamoDB as the primary key-value datastore.` | 55 against 48/68/84, rank 2 |
| TEACHER-RSK-006 = AWS-RSK-004 (1-3 s01) | Applied, Teacher wording. AWS's "Download the AWS compliance report from AWS Artifact" was also acceptable. | `Download the report from the AWS Artifact console` | 49 against 45/51/64, rank 2 |
| AWS-RSK-002 (4-3 k05 distractor b) | Not applied, optional. The proposed "target tracking policies" is not confirmed as taught in lesson 4-3, and the rationale already covers the failure. | — | — |
| AWS-RSK-003, TEACHER-RSK-004/005 | No change, notes only. | — | — |
| TEACHER-RSK-003 (4-1 k03) | Not applied, optional. AWS confirms "cost and usage budgets" is accurate AWS terminology. | — | — |

**Checks after the fix pass:** `content_lint` PASS. `q1_batch_check` 4-3 PASS (shortest-is-key 29%, longest-is-key 21%) and 1-3 WARN (pre-existing; shortest-is-key 18%, longest-is-key 27%). Stem echo totals are unchanged at 14 and 12, with no flag on an edited question. `correctAnswerIds` are unchanged.

## Technical confirmation (22f9ca8)

1. **AWS-RSK-001: Gone.** 4-3 s02 key is now "Use PostgreSQL on Amazon RDS or Amazon Aurora PostgreSQL." (57 chars vs 84/53/51, rank 3). It names the engine, is accurate, and is unambiguous. Not flagged by stem echo.
   **AWS-RSK-004: Gone.** 1-3 s01 key is now "Download the report from the AWS Artifact console" (49 vs 51/45/64, rank 2). "On demand" is removed. Accurate (Artifact is a console feature). No new tell.
2. Second-role check:
   - **TEACHER-RSK-001: Gone**, same fix as AWS-RSK-001.
   - **TEACHER-RSK-002: Gone.** 4-3 k09 key "Use Amazon DynamoDB as the primary key-value datastore." (55 vs 48/68/84, rank 2) is accurate. "Key-value" also appears in distractor b ("key lookups") and only names the data model, so it is not a defect. No stem-echo flag.
   - **TEACHER-RSK-006: Gone**, same fix as AWS-RSK-004.
3. AWS-RSK-002 and AWS-RSK-003 unapplied: **accepted.** RSK-002 is optional (the rationale already covers why the distractor fails). RSK-003 is a pre-existing note, and it is a plausible but wrong idea with a reason taught in the lesson. Teacher's optional RSK-003 (4-1 k03) also accepted as unapplied.
4. Scripts: `q1_batch_check` 4-3 PASS (shortest 29%, longest 21%), 1-3 WARN (pre-existing since/must in other questions; shortest 18%, longest 27%). `stem_echo_check` 4-3 and 1-3 RESULT FAIL from baseline flags in other questions only. The three edited questions (4-3 k09, 4-3 s02, 1-3 s01) have no flag. Remaining flags on the 11 are the known structural ones (4-3 k03 dynamodb, 1-3 s05 backup).

Reopen: close
Overall: approve

---

## Teacher confirmation (22f9ca8)

Saved by the Lead Dev from the Teacher's reply (condensed).

- **The Teacher's own findings:** TEACHER-RSK-001, TEACHER-RSK-002 and TEACHER-RSK-006 are Gone.
- **Second-role check:** AWS-RSK-001 and AWS-RSK-004 are Gone.
- **"Amazon Aurora PostgreSQL":** readable from what the lesson already teaches ("both MySQL and PostgreSQL can run on RDS and Aurora-compatible offerings"). k09 also shows Aurora PostgreSQL as an option. No lesson addition is required. The optional editions sentence would need a note to the user first, and it is not applied.
- **TEACHER-RSK-003:** accepted as it stands. The technical reviewer confirmed the AWS terminology.

Reopen: close · Overall: approve
