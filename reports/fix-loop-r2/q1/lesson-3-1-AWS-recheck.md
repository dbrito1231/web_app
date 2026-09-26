# Lesson 3.1 — AWS re-check of fix pass (commit `90fbeff`)

Reviewed: `content/lessons/lesson-3-1.json` after `90fbeff` ("Lesson 3.1: io1 and six EBS types,
current FSx figures, S3 per-prefix rates, Snowball Edge explained, EBS single-AZ, FSx Lustre DRA
(Q1 LF)"). Baseline findings: `reports/fix-loop-r2/q1/lesson-3-1-AWS.md` (AWS-L31-001..005) and
`reports/fix-loop-r2/q1/lesson-3-1-TEACHER.md` (TEACHER-L31-001..003). Fix log:
`reports/fix-loop-r2/q1/lesson-3-1-impl.md` "Fixes" section. Method: AWS Documentation MCP
(`search_documentation` / `read_documentation`) against docs.aws.amazon.com, all fetches dated
2026-09-26 (today). No AWS calls, no state-changing commands; only read-only checks and
`content_lint.py`.

## 1. AWS-L31 items — Gone / not gone

| ID | Claim fixed | Verdict | Confirming source |
|---|---|---|---|
| AWS-L31-001 | FSx for Lustre throughput ("hundreds of GBps" → "up to multiple TBps on SSD/Intelligent-Tiering, tens of GBps on HDD") | **Gone** | `fsx/latest/LustreGuide/what-is.html`: SSD "up to TBps", Intelligent-Tiering "up to multiple TBps", HDD "up to tens of GBps" — matches lesson wording exactly. |
| AWS-L31-002 | FSx for OpenZFS IOPS ("past 1,000,000" → "up to 2,000,000 IOPS, a few hundred microseconds") | **Gone** | `fsx/latest/OpenZFSGuide/what-is-fsx.html`: "delivers up to 2 million IOPS with latencies of hundreds of microseconds" — matches exactly. |
| AWS-L31-003 | S3 per-prefix baseline (3,500 PUT/COPY/POST/DELETE, 5,500 GET/HEAD) added to S01 | **Gone** | `AmazonS3/latest/userguide/optimizing-performance-design-patterns.html`, "Optimizing for high-request rate workloads": "more than 3,500 PUT/COPY/POST/DELETE or 5,500 GET/HEAD requests per second per prefix" — matches exactly, including the 503 (Slow Down) framing. |
| AWS-L31-004 | "five volume types" → "six volume types", io1 added | **Gone** | `ebs/latest/userguide/ebs-volume-types.html` table lists exactly six current-generation types: gp3, gp2, io2 Block Express, io1, st1, sc1. `provisioned-iops.html` confirms io1: up to 64,000 IOPS, up to 1,000 MiB/s, 4 GiB–16 TiB, "available for all Amazon EC2 instance types" — matches lesson's io1 sentence. |
| AWS-L31-005 | Snowball Edge physical description added before EOL sentence | **Gone** | `snowball/latest/developer-guide/whatisedge.html`: "Snowball Edge is a device with on-board storage and compute power... can process data locally, run edge-computing workloads, and transfer data to or from the AWS Cloud... transport data at speeds faster than the internet... shipping the data in the devices through a regional carrier. The appliances are rugged" — matches the lesson's added clause in substance. |

## 2. Second-role check of TEACHER-L31-001 to 003

- **TEACHER-L31-001 (Snowball Edge description).** Independently re-derived from
  `whatisedge.html` (not just trusting the impl notes' quote): confirmed Snowball Edge is a rugged,
  on-board storage-and-compute device, shipped via regional carrier, used for offline transfer and
  edge compute. The lesson's added sentence ("ruggedized, physical storage-and-compute device...
  shipped to a customer's site for offline bulk data transfer or edge locations without reliable
  network access; a customer loaded data onto it locally and shipped it back to AWS for import into
  S3") is accurate and not overstated. **Confirmed correct.**
- **TEACHER-L31-002 (EBS single-AZ scope).** Independently checked `ebs/latest/userguide/EBSFeatures.html`:
  "When you create an EBS volume, it is automatically replicated within its Availability Zone...
  You can attach an EBS volume to any EC2 instance in the same Availability Zone." This is stated
  as a property of EBS volumes generally, with no per-type exception — confirming the lesson's new
  sentence ("Every EBS volume type, regardless of class, lives in a single Availability Zone and
  can only attach to instances there") is accurate for gp3/gp2/io1/io2 Block Express/st1/sc1 alike.
  **Confirmed correct.**
- **TEACHER-L31-003 (FSx for Lustre DRA deployment-type scope).** Independently checked
  `fsx/latest/LustreGuide/overview-dra-data-repo.html`: "Data repository associations, automatic
  export, and support for multiple data repositories aren't available on FSx for Lustre 2.10 file
  systems or Scratch 1 file systems." This confirms DRAs are unavailable on Scratch 1 and available
  elsewhere (Persistent and Scratch 2), matching the lesson's "supported on Persistent and Scratch 2
  deployments, but not on Scratch 1." **Confirmed correct.**

All three Teacher items check out under independent re-derivation, not just re-reading the impl
notes' quotes.

## 3. New/changed numbers and citations

Every number changed or added in the diff was independently re-verified against the live doc page
(not just the citation's own note text):

- io2 Block Express: 256,000 IOPS / 4,000 MiB/s / sub-ms / 99.999% — matches `provisioned-iops.html`
  and `ebs-volume-types.html` table exactly (unchanged from prior review, re-confirmed).
- io1: 64,000 IOPS, 1,000 MiB/s, 4 GiB–16 TiB, "available for all Amazon EC2 instance types" —
  matches `provisioned-iops.html` exactly. Minor nuance not stated in the lesson (not an error): the
  docs note the 64,000 IOPS ceiling and 1,000 MiB/s max throughput are reached only on Nitro-based
  instances ("You can achieve up to 64,000 IOPS only on Nitro-based instances. On other instances,
  you can achieve up to 32,000 IOPS."). The lesson's "up to 64,000 IOPS... available on all instance
  types" is still true as written (availability ≠ guaranteed ceiling on every instance type) and
  mirrors the same level of abstraction used for gp3/gp2 elsewhere in the lesson, so this is not
  logged as a new issue — flagging only for awareness if a drill question later asks about non-Nitro
  io1 ceilings.
- FSx for Lustre: SSD/Intelligent-Tiering "up to multiple TBps", HDD "tens of GBps", millions of
  IOPS — matches `LustreGuide/what-is.html` exactly.
- FSx for OpenZFS: "up to 2,000,000 IOPS... a few hundred microseconds" — matches
  `OpenZFSGuide/what-is-fsx.html` ("up to 2 million IOPS with latencies of hundreds of microseconds")
  exactly.
- S3 per-prefix: 3,500 PUT/COPY/POST/DELETE, 5,500 GET/HEAD per second — matches
  `optimizing-performance-design-patterns.html` exactly, word for word.
- EBS single-AZ: confirmed against `EBSFeatures.html` (see §2).
- FSx Lustre DRA deployment scope: confirmed against `overview-dra-data-repo.html` (see §2).

**Citations:** all 3 new citation files (`cite-saa-3-1-snowball-edge-overview`,
`cite-saa-3-1-ebs-single-az`, `cite-saa-3-1-fsx-lustre-data-repo-associations`) and all 4 updated
citation notes (`cite-saa-3-1-fsx-lustre`, `cite-saa-3-1-fsx-openzfs`,
`cite-saa-3-1-s3-performance-design-patterns`, `cite-saa-3-1-ebs-provisioned-iops`) point to the
correct URL for the claim they back, and each note's stated figure/claim matches what that URL
currently says (spot-checked all 7 directly, not just read from the note text). No orphaned or
mismatched citation. `citationIds` in `lesson-3-1.json` includes all 3 new ids (20 total, up from
17), consistent with the impl notes.

## 4. Anything new wrong?

No new factual error introduced by the fix pass. `lesson-3-1.json`'s `objectiveIds`, `drillIds` (8,
unchanged, in K01→S02 order), and `labIds`/`exerciseIds` are untouched by the diff — only
`citationIds` (+3) and `bodyMarkdown` changed, matching `git show 90fbeff --stat` (lesson file,
4 citation files, impl notes; no question files touched).

`backend\.venv\Scripts\python.exe scripts\content_lint.py` → **PASS** (questions 429, aws 310, tf
119, labs 21+21, lessons 23).

## 5. Verdict

**Lesson 3.1: approve for question writing**

## Overall: approve
