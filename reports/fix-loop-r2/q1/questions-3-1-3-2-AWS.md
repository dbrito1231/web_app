# AWS review — Task 3.1 (8) and Task 3.2 (16) questions (commit d114785)

Reviewed against `lesson-3-1.json` / `lesson-3-2.json` bodies and the writer's claim tables in `questions-3-1-impl.md` / `questions-3-2-impl.md`. Numbers used in keys (io2 256,000 IOPS/4,000 MiB/s, io1 64,000 IOPS/1,000 MiB/s, gp3 80,000 IOPS, FSx Lustre "multiple TB/s", Lambda 1,769 MB = 1 vCPU) all match the lesson text, which was already AWS-verified in Round 1 — no live doc refetch needed for those. No new retired/closed services found beyond the two already on the RULES.md list.

## Per-question table

| ID | Key ok | Distractors ok | Rationale ok | Verdict |
|---|---|---|---|---|
| q-saa-3-1-k01-mc | Yes | Yes | Yes | OK |
| q-saa-3-1-k01-mr | Yes | Yes, but see AWS-Q31-001 | Yes | OK (diversity) |
| q-saa-3-1-k02-mc | Yes | Yes | Yes | OK |
| q-saa-3-1-k03-mc | Yes | Yes | Yes | OK |
| q-saa-3-1-s01-mc | Yes | Yes | Yes | OK |
| q-saa-3-1-s01-mr | Yes | Yes | Yes | OK |
| q-saa-3-1-s02-mc | Yes | Yes | Yes | OK |
| q-saa-3-1-s02-mr | Yes | No — see AWS-Q31-001 | Yes | Fix needed |
| q-saa-3-2-k01-mc | Yes | Yes | Yes | OK |
| q-saa-3-2-k02-mc | Yes | Yes | Yes | OK |
| q-saa-3-2-k02-mr | Yes | Yes | Yes | OK |
| q-saa-3-2-k03-mc | Yes | Yes | Yes | OK |
| q-saa-3-2-k04-mc | Yes | Yes | Yes | OK |
| q-saa-3-2-k05-mc | Yes | Yes | Yes | OK |
| q-saa-3-2-k05-mr | Yes | No — see AWS-Q32-001 | Yes | Fix needed |
| q-saa-3-2-k06-mc | Yes | Yes | Yes | OK |
| q-saa-3-2-s01-mc | Yes | Yes | Yes | OK |
| q-saa-3-2-s01-mr | Yes | Yes | Yes | OK |
| q-saa-3-2-s02-mc | Yes | Yes | Yes | OK |
| q-saa-3-2-s02-mr | Yes | Yes | Yes | OK |
| q-saa-3-2-s03-mc | Yes | Yes | Yes | OK |
| q-saa-3-2-s03-mr | Yes | Yes | Yes | OK |
| q-saa-3-2-s04-mc | Yes | Yes | Yes | OK |
| q-saa-3-2-s04-mr | Yes | Yes | Yes | OK |

## Fairness judgment on the batch-check flags

- **FSx File Gateway distractor, `q-saa-3-1-k01-mc` choice d.** Fair. It fails on a functional ground stated in the stem (workstations need a plain NFS share backed by S3; FSx File Gateway is for accessing FSx for Windows File Server, an unrelated file system) independent of its EOL status, and the choice text and rationale both clearly label it "no longer available to new customers." No fix needed.
- **Snowball distractor, `q-saa-3-1-k01-mr` choice b.** Fair standing alone: the rationale states plainly it is closed to new customers, matching the RULES.md retired-services list, and a slow/unreliable-WAN-link scenario is the realistic context where a candidate would otherwise consider it. No fix needed in isolation.
- **Snowball distractor, `q-saa-3-1-s02-mr` choice b.** Same reasoning as above holds in isolation, but see AWS-Q31-001 — the *pair* breaks the task's diversity cap.

## Issues

**AWS-Q31-001** (Medium — distractor diversity, `content/questions/q-saa-3-1-s02-mr.json`)
Two of the task's 8 questions (`k01-mr` choice b, `s02-mr` choice b) use "AWS Snowball Edge, closed to new customers" as the wrong-answer reason. That is 25% of the task on one distractor type against the 15%-of-8 (cap 1) limit in RULES.md, even though each use is individually fair. Fix: replace `s02-mr` choice **b** — text "AWS Snowball Edge devices, ordered again each time the dataset grows" — with **"S3 Transfer Acceleration enabled for the pipeline's uploads to cut per-transfer latency"**, and replace its rationale clause "Snowball Edge is closed to new customers, so it is not an available way to keep scaling this pipeline." with **"S3 Transfer Acceleration reduces the distance-driven latency of an individual upload; it adds no parallel transfer capacity to a growing migration pipeline the way running more DataSync tasks or agents does."** Swap `citationIds`: drop `cite-saa-3-1-snowball-edge-eol`, add `cite-saa-3-1-s3-transfer-acceleration` (already an existing citation file, backing this exact claim from lesson S01). Both the key fact (DataSync parallel scaling) and the new distractor's fact (Transfer Acceleration's purpose) are already taught in lesson-3-1 S01/S02, so no lesson change is needed.

**AWS-Q32-001** (Medium — distractor diversity, `content/questions/q-saa-3-2-k05-mr.json`)
"Reserved concurrency" is used as a wrong-answer distractor 3 times in the 16-question task (`k05-mc` choice c, `k05-mr` choice a, `s04-mc` choice a) — 18.75%, over the 15%-of-16 (cap 2) limit, and each use gives the identical wrong-answer reason ("only sets a floor/ceiling on invocation count, no effect on speed/cost"). Fix: in `k05-mr`, replace choice **a** — text "Reserved concurrency" — with **"Increasing the function's timeout setting to the maximum"**, and replace its rationale clause with **"Increasing the function's timeout only changes how long a single invocation may run before Lambda terminates it; it does not pre-initialize any execution environment and has no effect on Init-phase cold-start latency."** This needs a **lesson addition** to lesson-3-2 K05 (not currently taught): add the sentence *"Each function also has a separate configurable timeout, up to 15 minutes, that limits how long a single invocation may run — raising it does not pre-initialize anything and has no effect on cold-start latency."*, cited to a new `cite-saa-3-2-lambda-timeout` pointing at `https://docs.aws.amazon.com/lambda/latest/dg/configuration-timeout.html`. Update `k05-mr`'s `citationIds` to include it.

## Duplicate-fact check

No two questions in either task test the identical fact. Two pairs share a *feature* across different combinations (`q-saa-3-2-s01-mc`/`s01-mr` both credit "SQS + queue depth" as a decoupling mechanism; `q-saa-3-2-k03-mc`/`s02-mr` both credit `ApproximateNumberOfMessagesVisible` as the right scaling metric), but each question pairs that fact with a distinct second decision (EventBridge decoupling, or Compute Optimizer rightsizing) that the other does not test — acceptable reinforcement, not duplication.

Task 3.1: not yet
Task 3.2: not yet
Overall: concerns
