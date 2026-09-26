# Teacher re-check: lesson 3.1 (commit 90fbeff)

Saved by Lead Dev from the Teacher's reply (AGENTS.md: the Teacher does not write files).

**Method:** Read `content/lessons/lesson-3-1.json` body directly, cross-checked against `lesson-3-1-impl.md` (Fixes section) and `lesson-3-1-AWS-recheck.md`. Independently re-verified two of the highest-stakes claims via AWS Documentation MCP (`search_documentation`) rather than trusting either prior report's quotes: EBS io1/six-type taxonomy, and S3 per-prefix request-rate baseline. Ran my own Python format checks (word count, single-asterisk scan, heading markers, citation/drillId resolution) and re-ran `backend\.venv\Scripts\python.exe scripts\content_lint.py` myself.

## 1. TEACHER-L31-001 to 003 — Gone / not gone

- **TEACHER-L31-001** (Snowball Edge physical description): **Gone.** K01 now reads "Snowball Edge was a ruggedized, physical storage-and-compute device that AWS shipped to a customer's site for offline bulk data transfer or edge locations without reliable network access; a customer loaded data onto it locally and shipped it back to AWS for import into S3" — matches the exact wording I recommended in the prior review.
- **TEACHER-L31-002** (EBS single-AZ scope): **Gone.** K03 now states "Every EBS volume type, regardless of class, lives in a single Availability Zone and can only attach to instances there," generalizing beyond the earlier io2-only mention.
- **TEACHER-L31-003** (FSx Lustre DRA deployment scope): **Gone.** K02 now reads the data repository association "can link it directly to an S3 bucket so objects are readable as files without a separate copy step — supported on Persistent and Scratch 2 deployments, but not on Scratch 1," addressing the "any Lustre file system" ambiguity I flagged.

## 2. AWS-L31-001 to 005 — second-role check

- **io1 / six EBS types:** Independently confirmed via MCP search — docs classify current EBS types as gp3, gp2, io2 Block Express, io1, st1, sc1 (six types), with io1 "designed for I/O-intensive workloads requiring consistent, low-latency performance with user-specified IOPS." The lesson's "six volume types" plus io1's stated figures (64,000 IOPS, 1,000 MiB/s, 4 GiB–16 TiB, all instance types) are consistent with this and with lesson 2.1's existing io1/io2 Multi-Attach reference — no contradiction between lessons.
- **FSx figures** (Lustre "multiple TBps SSD/Intelligent-Tiering, tens of GBps HDD"; OpenZFS "up to 2,000,000 IOPS, hundreds of microseconds"): consistent with the AWS recheck's verbatim doc quotes; wording in the lesson is a faithful paraphrase, not an overstatement.
- **S3 per-prefix rates:** Independently confirmed via MCP search — "at least 3,500 PUT/COPY/POST/DELETE or 5,500 GET/HEAD requests per second per prefix" is the documented baseline, matching the lesson's S01 sentence word-for-word, including the 503 (Slow Down) framing.
- **Snowball wording clarity for a student:** Clear. The new sentence gives a concrete mental model (rugged device, local load, ship back, offline/edge use case) before the EOL sentence, so a student can now pattern-match an older exam stem describing the physical-appliance workflow as a retired distractor.

## 3. Placement and clarity

Reads well. The Snowball sentence sits naturally before the existing EOL sentence in K01; the single-AZ clause sits naturally after the io1 sentence in K03's EBS paragraph; the DRA deployment-scope clause is folded into the same sentence that introduces data repository associations in K02, not bolted on awkwardly. No redundancy or contradiction introduced. Word count: 2,048 (I counted independently) — reasonable for 5 fact-heavy objectives and within the ~2,200 ceiling noted in the impl report.

## 4. Format

- Markdown subset: only `##`/`###` headings, `- ` bullets, `**bold**`, backticks — confirmed by my own scan, no tables/links/numbered lists.
- Single-asterisk spans: 0 (confirmed by regex scan).
- Citations: all 20 `citationIds` resolve to files in `content/citations/` (confirmed by filesystem check).
- `drillIds`: all 8 present, in exact K01→S02 order, and all 8 resolve to existing `content/questions/q-saa-3-1-*.json` files (confirmed by filesystem check).
- `backend\.venv\Scripts\python.exe scripts\content_lint.py` → **PASS** (questions 429, aws 310, tf 119, labs 21+21, lessons 23) — I ran this myself, not just trusting the impl report.

## 5. Teach-before-test readiness

All 5 objectives (K01–K03, S01–S02) have complete sections with concrete numeric anchors a question can test against (six EBS types w/ io1 ceiling, FSx throughput/IOPS ceilings, EFS mode matrix, S3 per-prefix baseline and Express One Zone limits, EBS Elastic Volumes ceiling). The three teach-before-test gaps I flagged last round are closed. No new gaps found for these 5 objectives.

## New issues

None. No new TEACHER-L31-R-### issues raised.

## Verdicts

- TEACHER-L31-001: Gone
- TEACHER-L31-002: Gone
- TEACHER-L31-003: Gone
- AWS-L31-001 (FSx Lustre throughput): confirmed accurate
- AWS-L31-002 (FSx OpenZFS IOPS): confirmed accurate
- AWS-L31-003 (S3 per-prefix baseline): confirmed accurate (independently re-verified via MCP)
- AWS-L31-004 (io1 / six EBS types): confirmed accurate (independently re-verified via MCP)
- AWS-L31-005 (Snowball Edge description): confirmed accurate and clear for a student

**Lesson 3.1: approve for question writing**

**Overall: approve**
