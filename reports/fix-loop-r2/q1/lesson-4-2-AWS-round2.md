# Task 4.2 — Senior AWS Solutions Architect review (Round 2)

Scope completed:
- (a) Re-check of prior AWS findings
- (b) Second-role check of Teacher findings
- (c) Full review of all 24 questions
- (d) Verification of every number used in a key
- (e) Adjudication of distractor-type counting dispute

## (a) Prior AWS findings status

- `AWS-L42-001` (claim row 22 RI term quote) — **Gone**  
  Verified in `reports/fix-loop-r2/q1/lesson-4-2-impl.md` row 22: quote now reads `"You can purchase a Reserved Instance for a one-year or three-year commitment"` with correct source URL.

- `AWS-L42-002` (claim row 53 On-Demand per-second quote) — **Gone**  
  Verified in `reports/fix-loop-r2/q1/lesson-4-2-impl.md` row 53: quote now includes per-second granularity wording from the EC2 purchasing-options guide.

- `AWS-L42-004` (K07 bare-metal `.metal` naming) — **Gone**  
  Verified in `content/lessons/lesson-4-2.json` K07 prose: sentence explicitly teaches `.metal` as bare metal instance size.

- `AWS-L42-003` (top `##` heading) — **Resolved/Accepted (policy update)**  
  I accept the Lead Dev resolution. `reports/fix-loop-r2/q1/RULES.md` now explicitly states one top-level `##` lesson title as the established workbook pattern. This is no longer a 4.2 defect.

## (b) Second-role check: Teacher findings

- `TEACHER-L42-001` — **Gone**  
  Claim-table row 22 quote mismatch fixed as noted above.

- `TEACHER-L42-002` — **Gone**  
  K01 now explicitly teaches that management can turn off commitment discount sharing for account-level isolation. Doc support: `https://docs.aws.amazon.com/awsaccountbilling/latest/aboutv2/ri-behavior.html`.

- `TEACHER-L42-003` — **Gone**  
  K01 now explicitly teaches timing: up to 24 hours for tag keys to appear and up to another 24 hours to activate. Doc support: `https://docs.aws.amazon.com/awsaccountbilling/latest/aboutv2/activating-tags.html`.

- `TEACHER-L42-004` — **Gone**  
  K08 now explicitly teaches Lambda timeout default and range for standard functions: default 3 seconds, configurable 1 to 900 seconds (15 minutes). Doc support: `https://docs.aws.amazon.com/lambda/latest/dg/configuration-timeout.html`.

- `TEACHER-L42-006` — **Gone**  
  K09 now defines `SLO` and `blast radius` in learner-friendly prose at first use.

## (c) Question review (all 24)

Reviewed files: all `content/questions/q-saa-4-2-*.json` (24/24).

Checks completed per file:
- key correctness / single-best-answer (MC) or exact `selectCount` best set (MR)
- distractor realism/current AWS status
- no retired/closed/renamed service used as current correct advice
- rationale quality (key and distractors explained by content)
- citations present and resolvable
- metadata present (`citationIds`, `reviewedOn`, `mcpStatus`)

### Findings

- `AWS-Q42-001` — **moderate**  
  **Location:** `content/questions/q-saa-4-2-s03-mr.json`, choice `"c": "AWS Fargate for the short event handlers"`  
  **Issue:** distractor plausibility gap relative to stem constraints. As written, stem states workload shape and "avoid managing servers," but does not explicitly state a cost-optimization requirement for the short-handler tier. That makes `c` technically viable and risks a second defensible answer set (`c` + `d`).  
  **Doc-verified fix:** tighten stem to include explicit cost-fit constraint for the short handler path, for example: `"...and wants the lowest-cost fit for bursty short handlers while avoiding server management."` Keep key `a,d` unchanged.  
  **URL(s):**
  - `https://aws.amazon.com/lambda/pricing/` (requests + duration model for short bursty handlers)
  - `https://aws.amazon.com/fargate/pricing/` (task runtime billing model, typically less optimal for very short burst handlers)

## (d) Every number used in a key — verification

Numeric key dependencies identified and verified:

- `q-saa-4-2-s03-mr` key (`a,d`) depends on Lambda duration bound for standard functions (`900 seconds`, `15 minutes`) for rejecting Lambda on long-running job tier — **verified accurate** against `https://docs.aws.amazon.com/lambda/latest/dg/configuration-timeout.html`.
- `q-saa-4-2-s06-mc` key (`b`) depends on C7g size progression used for smallest safe next-step sizing (`large -> xlarge`, with `2 vCPU/4 GiB` to `4 vCPU/8 GiB`) — **verified accurate** against `https://aws.amazon.com/ec2/instance-types/c7g/`.

No wrong numeric fact found in any key.  
No key was found to misuse Spot notice timing, Savings Plans/RI term lengths, timeout defaults/bounds, or billing granularity.

## (e) Distractor-type adjudication

Reading applied: **semantic distractor type by underlying misconception**, with a secondary sanity check by literal service-name frequency in distractors.

Verdict:
- **Outposts/Local Zones call:** cap is **met** on fair reading. In current files, literal distractor mentions are 3 each (not 4 each), and semantic grouping ("edge/hybrid placement misalignment") is 3 total, within 15% cap.
- **Auto Scaling call:** cap is **met** on fair reading. Repeated wording spans different misconceptions (elastic method selection, compute-service mapping, and post-rightsizing guardrails), not one repeated distractor type. Literal "Auto Scaling" token reuse alone is not a reliable type signal.

Task 4.2: not yet

Overall: concerns
