# Teacher review: lesson 4.3 (round 1)

- Saved by Lead Dev from the Teacher reply (`AGENTS.md`: Teacher is read-only and writes no files).
- Scope completed: claim-table verification, pedagogy, exam-tip quality, teach-before-test readiness, markdown-subset check, and AWS-doc validation via `mcp-exec` (`search_documentation` + `read_documentation`).
- **Claim rows verified (13):** `3, 15, 16, 17, 22, 24, 28, 29, 33, 34, 35, 36, 38`.
- **Claim-table verdict for verified rows:** quotes are verbatim and support their paired claims.
- Specific check requested by Lead Dev: the five newly added numbers read naturally in prose (not bolted on): DynamoDB provisioned->on-demand switch limit (`K05`), DynamoDB reserved capacity discounts + 100-unit block sizing (`K09`), and Standard-IA 50% threshold (`K09`).

## Coverage and pedagogy

- All 14 objectives (`K01-K09`, `S01-S05`) are present in order with one `###` section each.
- Required confusion contrasts are explicitly taught:
  - RDS vs Aurora vs Aurora Serverless v2
  - Aurora Standard vs Aurora I/O-Optimized
  - Multi-AZ DB instance vs Multi-AZ DB cluster
  - read replicas vs standby
  - DynamoDB on-demand vs provisioned vs reserved capacity
  - DynamoDB Standard vs Standard-IA
  - ElastiCache vs DAX
- Section order is sensible for a no-background learner (cost controls -> tools -> cache -> retention -> capacity -> connection behavior -> engine/migration -> replication -> service economics -> scenario skills).
- Pedagogy gaps remain where jargon/discriminators needed for fair distractor handling are not explicit yet (findings below).

## Exam-tip check

- Every objective section ends with an `**Exam tip:**` line.
- Most tips are usable discriminators under time pressure (not pure restatement).

## Teach-before-test readiness by objective

- `SAA-4.3-K01` - Ready
- `SAA-4.3-K02` - Ready
- `SAA-4.3-K03` - Ready
- `SAA-4.3-K04` - Ready
- `SAA-4.3-K05` - Ready
- `SAA-4.3-K06` - Ready
- `SAA-4.3-K07` - Ready
- `SAA-4.3-K08` - Ready
- `SAA-4.3-K09` - **Gap** (undefined `ACID`; see `TEACHER-L43-004`)
- `SAA-4.3-S01` - **Gap** (undefined `blast radius`; see `TEACHER-L43-003`)
- `SAA-4.3-S02` - **Gap** (needs explicit MySQL vs PostgreSQL discriminator sentence; see `TEACHER-L43-001`)
- `SAA-4.3-S03` - Ready
- `SAA-4.3-S04` - Ready
- `SAA-4.3-S05` - **Gap** (DMS endpoint constraint not taught in prose; see `TEACHER-L43-002`)

## Format check (markdown subset)

- Pass: single `##` lesson title at top is now established/accepted pattern.
- Pass: objective sections use `###`, bullets use `- `, and emphasis/code style is consistent with allowed subset.

## Findings

- `TEACHER-L43-001` - **moderate**
  - **Location:** `SAA-4.3-S02` section in `content/lessons/lesson-4-3.json`
  - **Issue:** teach-before-test gap; section says engine behavior differs but does not give concrete, exam-usable MySQL vs PostgreSQL discriminator facts for wrong-choice elimination.
  - **Doc-verified fix (add exact sentence):** `Choose MySQL when broad framework/tool compatibility and simpler transactional workloads are the priority; choose PostgreSQL when you need advanced JSON handling, complex queries, or custom extensions.`
  - **URL:** `https://docs.aws.amazon.com/AmazonRDS/latest/gettingstartedguide/choosing-engine.html`

- `TEACHER-L43-002` - **moderate**
  - **Location:** `SAA-4.3-S05` (also relevant to `K07`) in `content/lessons/lesson-4-3.json`
  - **Issue:** claim table includes a key DMS constraint, but lesson prose does not teach it; this makes a common migration-location distractor family unfair.
  - **Doc-verified fix (add exact sentence):** `With AWS DMS, at least one endpoint (source or target) must be on an AWS service; DMS cannot migrate from one on-premises database directly to another on-premises database.`
  - **URL:** `https://docs.aws.amazon.com/dms/latest/userguide/CHAP_Introduction.html`

- `TEACHER-L43-003` - **low**
  - **Location:** `SAA-4.3-S01`, sentence using `blast radius`
  - **Issue:** jargon appears without plain-language definition for no-background learners.
  - **Doc-verified fix (add exact sentence):** `Here, blast radius means how much of the workload is affected by a failure; fault-isolated boundaries keep unaffected components outside that failure scope.`
  - **URL:** `https://docs.aws.amazon.com/wellarchitected/2023-10-03/framework/rel-10.html`

- `TEACHER-L43-004` - **low**
  - **Location:** `SAA-4.3-K09`, first use of `ACID`
  - **Issue:** acronym is used before plain-language definition.
  - **Doc-verified fix (add exact sentence):** `ACID means atomicity, consistency, isolation, and durability: all related changes complete together or fail together while preserving data correctness.`
  - **URL:** `https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/transactions.html`

Lesson 4.3: not yet
Overall: concerns

---

## Lead Dev notes

### S02 is reported by both reviewers; the Teacher's fix is the one being used

`TEACHER-L43-001` and `AWS-L43-001` are the same gap, found independently: the S02
section never gives a concrete engine discriminator a question could test.

`AWS-L43-001` proposed the sentence `RDS for PostgreSQL supports many PostgreSQL
extensions.` That is too vague to separate two options in a question, which is the
very thing the finding asks for. The Teacher's MySQL-versus-PostgreSQL sentence is
specific enough to build a fair distractor against, so the writer was given that
one. The AWS reviewer will be asked in round 2 to confirm its finding is Gone on
that basis.

### The prose-gap checker has a known blind spot

`scripts/claim_prose_check.py` compares only NUMBERS between the claim table and
the lesson prose, so it caught the five numeric gaps in this lesson but could not
catch `TEACHER-L43-002`, where a non-numeric DMS constraint sits in the claim table
without being taught. Extending the script to non-numeric claims would need fuzzy
matching and would likely be noisy, so for now the Teacher's read remains the
control for non-numeric teach-before-test gaps. Noted so the checker is not
mistaken for full coverage on the remaining nine tasks.
