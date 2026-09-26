# Lesson 3.1 — AWS Solutions Architect review

Reviewed: `content/lessons/lesson-3-1.json` (commit `2178696`, "rewritten for storage
performance/scalability, 17 doc citations, all 8 drillIds"). Author notes:
`reports/fix-loop-r2/q1/lesson-3-1-impl.md`. Objectives: `SAA-3.1-K01..K03`, `SAA-3.1-S01..S02` in
`content/objectives/saa_c03.json`. Standard used: approved review `reports/fix-loop-r2/q1/lesson-2-2-AWS.md`
(Overall: approve). Method: AWS Documentation MCP (`search_documentation` / `read_documentation`)
against docs.aws.amazon.com, all fetches dated 2026-09-26 (today). No AWS calls, no edits made
outside this report.

## 1. Per-section verdict

| Section | Verdict | Notes |
|---|---|---|
| K01 — Hybrid storage solutions | Accurate, one coverage gap | Storage Gateway's three living types (S3 File Gateway, Volume Gateway cached/stored, Tape Gateway) match `WhatIsStorageGateway.html`. FSx File Gateway EOL wording matches `filefsxw/what-is-file-fsxw.html` verbatim in substance. DataSync source/destination list (NFS/SMB/HDFS/object storage → S3/EFS/FSx Windows/Lustre/OpenZFS/ONTAP) matches `datasync/what-is-datasync.html` exactly. Snowball Edge EOL claim confirmed exact and, per AWS's own indexed metadata, covers the whole Snow Family (see §2, no fix needed to the claim itself). Gap: the lesson never says what Snowball Edge physically was — see AWS-L31-005. |
| K02 — Storage services with use cases (FSx family) | Accurate, two stale numbers | Lustre Scratch/Persistent and S3 data-repository linking match `LustreGuide/what-is.html`. Windows File Server (SMB/AD) and NetApp ONTAP (multi-protocol, dedup) descriptions match their "what is" pages. OpenZFS ZFS-feature/cache description is directionally right but its headline IOPS figure is stale — see AWS-L31-002. Lustre's throughput figure is also stale — see AWS-L31-001. |
| K03 — Storage types (object/file/block) | Accurate numbers, one coverage/count error | gp3 (3,000/125 baseline, 80,000 IOPS/2,000 MiB/s ceiling, no bursting), gp2 (IOPS-with-size, burst-credit), io2 Block Express (256,000 IOPS, 4,000 MiB/s, sub-ms latency, 99.999% durability), st1 (40/250 MiB/s per TiB, 500 cap), sc1 (12/80 MiB/s per TiB, 250 cap), and instance store (ephemeral, physically attached) all match current EBS/EC2 docs exactly, including the boot-volume restriction on st1/sc1. Problem: the lesson says EBS "comes in five volume types" and lists only gp3/gp2/io2 Block Express/st1/sc1 — this undercounts and omits `io1`, a distinct, still-current volume type. See AWS-L31-004. EFS performance-mode and throughput-mode figures (1,500 MiBps Elastic ceiling with a current client) match `efs/latest/ug/performance.html` exactly, including the client-version caveat. S3 Express One Zone figures (single-digit-ms, 10x S3 Standard, 200,000/100,000 default, up to 2,000,000/200,000 scaled) match `s3-express-performance.html` verbatim. |
| S01 — Performance-driven configuration | Accurate, one coverage gap | Byte-range fetch mechanics and the "8–16 MB" typical chunk size match AWS's S3 performance whitepaper and guidelines page exactly. Multipart upload and Transfer Acceleration descriptions match their respective pages. Prefix-scaling claim ("S3 scales request rate per prefix... no limit on the number of prefixes") is directionally correct but omits the specific, heavily-tested baseline figures (3,500 PUT/COPY/POST/DELETE and 5,500 GET/HEAD requests/sec per prefix) that current docs state explicitly. See AWS-L31-003. The EBS/EFS/FSx matching guidance (io2 for IOPS+latency, st1 for sequential throughput, EFS Max I/O+Elastic for many small parallel ops, FSx for Lustre for single-node HPC) is consistent with K02/K03. |
| S02 — Scaling for future needs | Accurate | S3's no-capacity-planning framing, EBS Elastic Volumes (live resize/retype, 64 TiB single-volume ceiling — matches `general-purpose.html`'s "A gp3 volume can range in size from 1 GiB to 64 TiB" and io2 Block Express's "storage capacity up to 64 TiB"), EFS auto-grow plus Elastic throughput auto-scaling, and FSx post-creation capacity/throughput increases are all accurate. DataSync's parallel-task/agent scaling and the now-closed Snowball Edge path are consistent with K01 and the Snowball Edge EOL notice. |

## 2. Verifying the two end-of-availability claims

Both claims were checked directly against the pages the lesson cites, and both are **confirmed
accurate, current, and precisely worded**:

- **FSx File Gateway.** `https://docs.aws.amazon.com/filegateway/latest/filefsxw/what-is-file-fsxw.html`
  opens with: *"Amazon FSx File Gateway is no longer available to new customers. Existing customers
  of FSx File Gateway can continue to use the service normally."* The lesson's wording ("is no
  longer available to new customers") matches this exactly, and its recommended alternative (S3 File
  Gateway, or a direct FSx for Windows File Server connection over VPN/Direct Connect) matches AWS's
  own linked migration guidance (the "switch your file share access from Amazon FSx File Gateway to
  Amazon FSx for Windows File Server" blog post).
- **The entire Snow Family.** `https://docs.aws.amazon.com/snowball/latest/developer-guide/snowball-edge-availability-change.html`
  states: *"AWS Snowball Edge is no longer available to new customers. New customers should explore
  AWS DataSync for online transfers, AWS Data Transfer Terminal for secure physical transfers, or AWS
  Partner solutions."* AWS's own documentation metadata indexes this same page under the entity **"AWS
  Snow Family"**, described as *"Collection of AWS physical devices for edge computing and data
  migration, no longer available to new customers"* — i.e., AWS itself treats the notice as covering
  the whole family (Snowball Edge, Snowcone, Snowmobile), not Snowball Edge alone. The lesson's
  extension of the claim to "the entire Snow Family" is therefore supported, not an overreach.
- **AWS Data Transfer Terminal** is a real, currently documented service
  (`docs.aws.amazon.com/datatransferterminal/latest/userguide/`), described in AWS's own docs as *"a
  secure, private physical location equipped with high-speed fiber optic connections for performing
  large data transfers between storage devices and AWS services."* This matches the lesson's "a
  physical facility with high-speed fiber connections" description exactly — not fabricated.

**Recommendation on Snowball Edge exam framing (not a factual error, a teaching gap):** the lesson
never explains what Snowball Edge physically *was* — a ruggedized, portable storage/compute
appliance that AWS shipped to a customer's site, was loaded with data on-premises, and shipped back
to an AWS facility for import into S3 (used for offline transfers where bandwidth was too slow or
unreliable for DataSync). SAA-C03 exam questions were written against the service catalog before this
2025 retirement and may still describe that shipping-appliance workflow as a distractor or answer
option. As written, a student who has never seen Snowball Edge described will only learn "it's
retired, the exam tip says the answer is DataSync/Data Transfer Terminal" without being able to
recognize the *scenario language* (physical device, petabyte-scale, no network at all, rugged
case, on-site data loading) that such a question would use to point at the old Snowball Edge answer.
Recommend adding one or two sentences to K01 describing what Snowball Edge was (rugged, physical,
shippable storage/compute device for offline bulk transfer and edge locations without reliable
network access) immediately before or after the EOL sentence, so the exam-pattern recognition survives
even though the purchasing decision does not. This is additive, not a correction — the current EOL
framing itself is accurate and should not change.

## 3. Issues

| # | Location | Severity | Problem | Fix | Doc URL |
|---|---|---|---|---|---|
| AWS-L31-001 | K02, FSx for Lustre paragraph | Medium | Lesson states FSx for Lustre delivers "hundreds of gigabytes per second of throughput." Current docs state Lustre's SSD and Intelligent-Tiering storage classes deliver "up to multiple TBps of throughput" (the HDD class tops out at "tens of GBps"), so "hundreds of gigabytes per second" understates the current top end by roughly an order of magnitude. | Change to: "...delivers up to multiple terabytes per second of throughput on its SSD and Intelligent-Tiering storage classes (tens of gigabytes per second on the HDD class) and millions of IOPS..." | https://docs.aws.amazon.com/fsx/latest/LustreGuide/what-is.html |
| AWS-L31-002 | K02, FSx for OpenZFS paragraph | Low-Medium | Lesson states the in-memory cache can "push a single file system past 1,000,000 IOPS." Current docs state FSx for OpenZFS delivers "up to 2 million IOPS with latencies of hundreds of microseconds" from cache (up to 400,000 IOPS / 10 GBps from disk). "Past 1,000,000" is technically true but understates the documented ceiling by half. | Change to: "...with an in-memory read cache that can push a single file system to up to 2,000,000 IOPS at latencies of a few hundred microseconds." | https://docs.aws.amazon.com/fsx/latest/OpenZFSGuide/what-is-fsx.html |
| AWS-L31-003 | S01, S3 prefix-scaling sentence | Low (coverage) | The review brief explicitly lists "S3 request rates per prefix" as a fact to check. The lesson only says S3 "scales request rate per prefix" without ever giving the baseline numbers, which are a frequently tested SAA-C03 fact. Current docs: request rates above roughly 3,500 PUT/COPY/POST/DELETE or 5,500 GET/HEAD requests per second **per prefix** are what trigger S3's internal scaling/503 behavior, and spreading load across more prefixes raises the achievable aggregate rate. | Add to S01: "As a baseline, a single prefix supports around 3,500 PUT/COPY/POST/DELETE or 5,500 GET/HEAD requests per second; a workload that will exceed this should use multiple prefixes from the start rather than wait for a 503 (Slow Down) response." | https://docs.aws.amazon.com/AmazonS3/latest/userguide/optimizing-performance-design-patterns.html |
| AWS-L31-004 | K03, opening sentence of the block-storage paragraph | Medium | The lesson states "Block storage (Amazon EBS) comes in five volume types" and then only describes gp3, gp2, io2 Block Express, st1, and sc1. This both undercounts (EBS currently has six volume types) and omits `io1` (Provisioned IOPS SSD, non-Block-Express) entirely, even though `io1` is a distinct, still-current, purchasable volume type documented on the very citation page this lesson already links (`ebs-provisioned-iops.html`) and is referenced elsewhere in the workbook (lesson 2.1's EBS Multi-Attach section: "a single Provisioned IOPS (io1/io2) volume"). This is also one of the six volume types the review brief explicitly asked to check. | Change "five volume types" to "six volume types" and add one sentence for `io1`, e.g.: "**io1** is the earlier Provisioned IOPS SSD volume (up to 64,000 IOPS, up to 1,000 MiB/s, available on all instance types, up to 16 TiB) — for new volumes, prefer io2 Block Express, which delivers higher IOPS/throughput ceilings and better durability at the same or lower cost." | https://docs.aws.amazon.com/ebs/latest/userguide/provisioned-iops.html |
| AWS-L31-005 | K01, Snowball Edge paragraph | Low (pedagogical, not factual) | See §2 above: the lesson never describes what Snowball Edge physically was, only that it's retired and what replaces it. A student cannot pattern-match an exam stem describing the old shipping-appliance workflow without this context. | Add one clause describing Snowball Edge as a ruggedized, physical storage/compute device AWS shipped to a customer site for offline bulk data transfer (and edge compute) before this retirement, immediately preceding or following the existing EOL sentence. | https://docs.aws.amazon.com/snowball/latest/developer-guide/snowball-edge-availability-change.html |

No factual error was found in the two end-of-availability claims, in any EBS/EFS/S3 numeric figure
that has a citation, in any Storage Gateway or DataSync claim, or in the AWS Data Transfer Terminal
description. All issues above are either stale/conservative numbers on two FSx figures that AWS has
since increased, or coverage gaps (missing `io1`, missing S3 per-prefix baseline numbers, missing
"what was Snowball Edge" context) rather than corrections to something stated incorrectly.

## 4. Exam tips

All 5 `**Exam tip:**` lines were checked against their paired section content:

- K01's tip (S3 File Gateway vs. Volume Gateway vs. "the current answer... is DataSync or Data
  Transfer Terminal") is correct and consistent with §2.
- K02's tip (Lustre for HPC/ML tied to S3, Windows File Server for AD lift-and-shift, ONTAP for
  NetApp shops) draws correct, testable distinctions; unaffected by the AWS-L31-001/002 number fixes.
- K03's tip ("EFS Max I/O" vs. "S3 Express One Zone" vs. "io2 Block Express, not gp3") is correct and
  matches the documented performance profiles.
- S01's tip (match the stem's number to the documented ceiling) is a correct, generically useful
  strategy and becomes more concrete once AWS-L31-003's baseline figures are added.
- S02's tip (S3/EFS need no resize project vs. EBS Elastic Volumes under the 64 TiB ceiling) is
  correct; the 64 TiB ceiling is confirmed both for gp3 ("1 GiB to 64 TiB") and io2 Block Express
  ("up to 64 TiB (65,536 GiB)").

None of the exam tips are stale or misleading.

## 5. Coverage and consistency

- All 5 `SAA-3.1-*` objective bullets (K01–K03, S01–S02) get their own `###` section, matching
  `content/objectives/saa_c03.json` exactly — no missing or extra objective.
- All 17 `citationIds` resolve to existing files under `content/citations/`; every citation's `note`
  names the specific claim it backs (a real improvement over the generic-boilerplate regression
  flagged as AWS-L22-001 in the lesson 2.2 review — this lesson's citation notes meet the
  lesson-2-1/1-3 standard). Spot-checked all 17 against the URLs fetched in this review: no orphaned
  or topically mismatched citation.
- All 8 `drillIds` resolve to existing `q-saa-3-1-*` files per the impl notes; these are still
  unrewritten placeholders restating the objective text, consistent with the impl notes' own
  statement that question rewriting is a separate pass.
- No contradiction found with lesson 2.1 or lesson 2.2: lesson 2.1's "instance store is lost when the
  instance stops/hibernates/terminates" and its io1/io2 Multi-Attach mention are consistent with (and,
  per AWS-L31-004, actually argue for extending) this lesson's K03 section; lesson 2.2's "io2 volume
  is designed for 99.999% durability" and "S3 stores objects across 3+ AZs, eleven nines durability"
  match this lesson's K03/K03 S3 Express contrast without conflict (S3 Express One Zone is correctly
  scoped as a single-AZ trade-off against the multi-AZ durability lesson 2.2 already established for
  S3 Standard).
- No stale numeric claim was found other than the two FSx figures in AWS-L31-001/002; every EBS,
  EFS, and S3 figure independently checked (gp3 3,000/125 baseline and 80,000/2,000 ceiling, gp2
  IOPS-per-GiB, io2 Block Express 256,000 IOPS/4,000 MiB/s/99.999%, st1 40↔250/TiB with 500 cap, sc1
  12↔80/TiB with 250 cap, EFS 1,500 MiBps Elastic ceiling, S3 Express One Zone's 200,000/100,000 and
  2,000,000/200,000 figures, the 64 TiB EBS ceiling, byte-range's 8–16 MB chunk guidance) matched
  current AWS documentation exactly.

**Lesson 3.1: not yet**

## Overall: concerns

The two headline end-of-availability claims (FSx File Gateway, the Snow Family) are exactly right and
well-cited — no change needed there, and AWS Data Transfer Terminal is real and accurately described.
However, one factual precision issue (AWS-L31-004: "five volume types" undercounts EBS and omits
`io1`, which the review brief specifically asked to check and which the workbook already references
in lesson 2.1) should be fixed before this lesson is used to write drill questions, since a question
writer could otherwise ask about `io1` with no supporting lesson text, or a student could be told
there are only five EBS volume types. The two stale FSx throughput/IOPS figures (AWS-L31-001,
AWS-L31-002) and the missing S3 per-prefix baseline numbers (AWS-L31-003) are lower-severity
undercounts, not wrong-direction errors, but the prefix numbers were explicitly named in this
review's brief and are a common exam fact worth adding. AWS-L31-005 (explaining what Snowball Edge
was) is a recommendation, not a required fix. Recommend Lead Dev apply AWS-L31-001 through
AWS-L31-004 (and consider AWS-L31-005) in a small follow-up edit, then this lesson can be re-validated
and approved.
