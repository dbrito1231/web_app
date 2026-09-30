# Teacher review (e668531) — D6 batch 3 (24 exercises)

Saved by the Lead Dev from the Teacher's reply. Replacement texts are verbatim.

**Method.** The Teacher used backtick-stripped, case-insensitive regex checks over lessons 4.1–4.4, 3.3 and 2.2. Results:
- `content_lint` PASS.
- No AWS dollar prices; every budget is a cap or a relative target.
- Teach-before-test passes everywhere, except the de-tgw inference (TEACHER-DE3-007).
- SCT plus DMS is taught in 3.3 K06, which de-db-migration lists among its objectives.

**Verdicts**
- **Approve:** 4.1-s01, s02, s06, s08, s09, s10; de-outposts; de-purchasing; 4.2-s01, s03, s04; de-db-migration; 4.3-s02; 4.4-s03, s05, s07.
- **Approve with minor:** de-storage-migration (008), 4.2-s02 (009), de-tgw (007), de-throttling (006).
- **Changes:** 4.1-s04 (003, 004); 4.1-s05 (002).
- **Changes, major:** 4.2-s05 (001); 4.3-s04 (005).

**Findings**
- **TEACHER-DE3-001 (major) de-saa-4.2-s05 r7.** The scenario gives averages only, and r7 would penalise keeping transcription's 128 vCPUs.
  - New r7: "Each new fleet keeps at least the vCPUs and the memory that its stated utilisation requires, with the vCPU and GiB totals before and after stated for both services".
- **TEACHER-DE3-005 (major) de-saa-4.3-s04 r7.** It cannot be checked, because the scenario has no cost figures.
  - New r7: "Analyst scans no longer compete with the permit registry's transactions, and the record names what would be measured to confirm it".
- **TEACHER-DE3-002 (minor) de-saa-4.1-s05 r6.** It gives away the selection rule for Glacier Instant Retrieval against Standard-IA.
  - New r6: "Every scan older than 30 days costs less to store than today and still opens in under a second, with no early-removal charge before the 7-year deletion, while thumbnail storage and request cost does not rise".
- **TEACHER-DE3-003 (minor) de-saa-4.1-s04 scenario.** 800 GB plus a 150 GB import does not fill 1 TB.
  - Change "holding 800 GB today" to "holding 900 GB today".
- **TEACHER-DE3-004 (minor) de-saa-4.1-s04 r6.** It reveals that some stores need no work.
  - New r6: "For each of the three stores the record says how its capacity grows and why, using the scenario's figures".
- **TEACHER-DE3-006 (minor) de-throttling.** The caller guidance is required by `requiredArtifact` but is not graded.
  - Append to r6: "; the caller guidance tells rejected callers to wait and retry with increasing delay, not immediately" (backoff is taught in 2.2 K10).
- **TEACHER-DE3-007 (minor) de-tgw.** Peering alongside TGW is untaught; lessons 4.4 K06 and 3.4 S01 present the two as alternatives. There are two ways to fix it:
  - Preferred: keep r7 and add a lesson 4.4 K06 sentence, doc-confirmed: "Peering and Transit Gateway can coexist: a pair of VPCs that exchanges very heavy traffic can also be peered directly, so that pair's traffic skips the gateway's per-GB processing charge while every other VPC keeps using the gateway."
  - Otherwise: remove constraint 2 and r7.
  - Either way, add "All of the VPCs are in one Region." to the scenario.
- **TEACHER-DE3-008 (minor) de-storage-migration.**
  - Change "an address Dovecote controls" to "a hostname in Dovecote's own domain".
  - In r6, drop "(about 24)", so it reads "...at the 700 Mbps the scenario leaves free, and the record shows the days needed".
- **TEACHER-DE3-009 (minor) de-saa-4.2-s02 r6.** It over-claims a 3-minute resume, which no source guarantees.
  - New r6: "The engine is not billed for server time during its idle hours and is usable at 07:30 without the 25-minute rebuild, and the record says how the 3-minute start limit will be confirmed".

Batch 3: not yet · Overall: concerns

---

## Teacher confirmation (batch 3 fix passes: 989f0bf, e994421)

Saved by the Lead Dev (condensed).

- **The Teacher's own findings:** TEACHER-DE3-001 to 008 are Gone.
  - 003 was fixed through AWS-DE3-002 (900 + 200 GiB now overflows 1,000 GiB).
  - 007 was fixed by the user's trim; Transit Gateway alone is fully taught.
- **009 is partly gone.** de-saa-4.2-s02 r6 ends "including the root-volume throughput it assumes", which leans toward hibernation, since lesson 4.2 K09 ties the root volume to saved RAM. This is minor and not a condition; the answer is already forced by the constraints.
  - Recommended r6 tail: "...and the record says how the 3-minute start limit will be confirmed and what it assumes".
- **Second-role check:** agree with all 19 AWS-DE3 findings as applied.
  - 001, 007, 009, 010 and 011 fix real determinacy holes. 4.2-s04 at 75% forces the schedule plus single-AZ answer: a schedule alone gives 70.2%, and the two together give about 85%.
  - 012 was replaced by the Teacher's text, which was right, because the AWS text printed the answers.
  - 017's answer, 2 connections (4 tunnels), is taught in lesson 4.4 K05.
- **Changed texts:** all operational, all using taught services only, and all outcome-based.

Batch 3: close · Overall: approve
