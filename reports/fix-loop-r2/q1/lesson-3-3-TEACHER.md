# Teacher review: lesson 3.3 (round 1)

Saved by Lead Dev from the Teacher's reply (AGENTS.md: the Teacher does not write files).

**Verdicts**

1. **Claim table spot-check (7 rows, beyond AWS's list):** K02 ElastiCache "microsecond latency" quote — verified verbatim (`whitepapers/latest/aws-overview/database.html`). K08 DynamoDB, DocumentDB, MemoryDB whitepaper quotes — all verified verbatim against the same page's compare table. K08/S03 Redshift MPP/columnar/compression quote — verified verbatim against `redshift/latest/dg/c_redshift_system_overview.html`. K07 RDS read-replica definition quote — see TEACHER-L33-001 below; not confirmed as page prose. Agree with AWS's approve verdict on the rows it checked.

2. **Coverage:** All 13 `SAA-3.3-*` objectives (K01–K08, S01–S05) each have their own `###` section, in id order, confirmed against `content/objectives/saa_c03.json` and the batch check.

3. **Teaching quality:** Clear, college-IT-student level. All named contrast pairs are present and correctly drawn: engine types→services (K08), Aurora vs RDS (S03/K08), DynamoDB on-demand vs provisioned (S02), GSI vs LSI (S02), DAX vs ElastiCache (S05), lazy loading vs write-through (K02), DMS vs SCT (K06), Redshift vs OLTP (K08/S03 vs relational). Exam tips read correct. No filler. No contradiction of lesson 2.2 — cross-checked K06/K07/S01 (read replicas), K05 (RDS Proxy), K08 (Aurora): 3.3 correctly defers to 2.2 for HA framing and stays in the performance lane, consistent wording throughout (e.g., read replica "not, by itself, a high-availability feature" matches 2.2's "not to fail over automatically").

4. **Length:** 2,823 words exactly — matches the target, acceptable.

5. **Format:** 0 single-asterisk spans, 0 pipe/table chars, 0 markdown links, 0 numbered-list lines, 14 `###` headings — all verified directly (not just via report claims). All 16 `citationIds` and all 21 `drillIds` resolve to existing files.

6. **Teach-before-test:** Checked the impl report's 21 question-concept mappings against the lesson body — every concept a question will need (Region/AZ latency, lazy-loading/write-through/TTL, read vs write-intensive fixes, gp3 vs io2, RDS Proxy, DMS+SCT ordering, read replica vs Aurora Replica vs Multi-AZ, K08 service mapping incl. Timestream EOL trap, hot partitions, GSI vs LSI, engine tradeoffs, DAX vs ElastiCache) is explicitly taught. No gaps found.

7. **Batch check** (`q1_batch_check.py 3-3`, lesson lines only):
```
PASS: lesson single-asterisk spans: 0
PASS: lesson tables/numbered lines: 0
PASS: lesson citations unresolved: []
PASS: drillIds match questions (missing [], extra [])
PASS: exam tips 13 for 13 objectives
```

**Issues**

- **TEACHER-L33-001** (low, K07, `cite-saa-3-3-rds-read-replicas` claim-table row: "Special RDS DB instance created from a source DB instance using built-in replication, receiving asynchronous updates and serving read queries to reduce load on the source"): This sentence does not appear in the rendered prose of `AmazonRDS/latest/UserGuide/USER_ReadRepl.html` (checked full visible text). It only surfaces as the AWS docs-search tool's auto-generated glossary "context" blurb for the term, not a quotable page sentence. Fix: replace with an actual page sentence, e.g. "A *read replica* is a read-only copy of a DB instance," or "Amazon RDS copies them asynchronously to the read replica" — both verbatim and present on the cited page.

Lesson 3.3: approve for question writing

Overall: approve
