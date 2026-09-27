# Teacher review: task 4.2 (round 2)

Saved by Lead Dev from the Teacher reply (`AGENTS.md`: Teacher is read-only, writes no files).

## (a) My round-1 lesson findings status

- `TEACHER-L42-001` - **Gone**
  Claim-table row 22 now uses the correct RI term quote.
- `TEACHER-L42-002` - **Gone**
  `K01` now explicitly teaches management account can turn off RI/Savings Plans sharing.
- `TEACHER-L42-003` - **Gone**
  `K01` now explicitly teaches both timing windows in lesson prose: up to 24 hours to appear, plus up to another 24 hours to activate.
- `TEACHER-L42-004` - **Gone**
  `K08` now explicitly teaches Lambda timeout default (3 seconds) and range (1 to 900 seconds for standard functions).
- `TEACHER-L42-006` - **Gone**
  `K09` now defines `SLO` and `blast radius` in plain language in-body.

Confirmation requested: yes, the `24 hours` and `3 seconds` facts are now genuinely in lesson prose, not only in claim-table metadata.

## (b) Rejected finding `TEACHER-L42-005` resolution

- I **accept** the resolution.
- `RULES.md` now explicitly defines the single top-level `##` lesson title as the established workbook pattern.
- I do **not** treat `## Cost-optimized compute` as a current task-level violation.

## (c) Second-role check on AWS reviewer lesson findings

- `AWS-L42-001` - **Gone** (row 22 quote corrected).
- `AWS-L42-002` - **Gone** (row 53 quote corrected to include per-second granularity statement).
- `AWS-L42-004` - **Gone** (`K07` now teaches `.metal` bare metal size distinction).

## (d) Question review: fairness and teach-before-test (all 24)

- `q-saa-4-2-k01-mc` - Fair; key and distractor logic taught.
- `q-saa-4-2-k02-mc` - Fair; tool-role discrimination taught.
- `q-saa-4-2-k02-mr` - Fair; alarm vs line-item-export split taught.
- `q-saa-4-2-k03-mc` - Fair; multi-AZ reliability contrast taught.
- `q-saa-4-2-k04-mc` - Fair; baseline commitment + Spot contrast taught.
- `q-saa-4-2-k05-mc` - Fair; Wavelength vs Local Zone/Outposts taught.
- `q-saa-4-2-k05-mr` - Fair; edge-vs-region split taught.
- `q-saa-4-2-k06-mc` - Fair; Outposts vs other edge models taught.
- `q-saa-4-2-k07-mc` - Fair; `.metal` distinction now taught.
- `q-saa-4-2-k08-mc` - Fair; Lambda burst/event fit taught.
- `q-saa-4-2-k08-mr` - Fair; Fargate host-removal and microservice scaling taught.
- `q-saa-4-2-k09-mc` - Fair; hibernation vs scaling role separation taught.
- `q-saa-4-2-s01-mc` - **Concern** (see `TEACHER-Q42-001`).
- `q-saa-4-2-s01-mr` - **Concern** (see `TEACHER-Q42-002`).
- `q-saa-4-2-s02-mc` - Fair; horizontal target-tracking fit taught.
- `q-saa-4-2-s02-mr` - Fair; scale-out plus hibernation niche taught.
- `q-saa-4-2-s03-mc` - Fair; mixed execution model mapping taught.
- `q-saa-4-2-s03-mr` - Fair; Lambda short-run vs Fargate long-run taught.
- `q-saa-4-2-s04-mc` - Fair; production vs non-production availability tiers taught.
- `q-saa-4-2-s04-mr` - **Concern** (see `TEACHER-Q42-003`).
- `q-saa-4-2-s05-mc` - Fair; family-by-bottleneck taught.
- `q-saa-4-2-s05-mr` - Fair; C vs R mapping taught.
- `q-saa-4-2-s06-mc` - Fair; stepwise same-family sizing taught.
- `q-saa-4-2-s06-mr` - Fair; rightsize + preserve scale-out taught.

Additional fairness checks:
- Stem realism and clarity: generally good.
- Elimination-by-wording: no giveaway forbidden phrasing found.
- Duplicate fact testing: overlap exists by design across adjacent objectives, but no exact duplicate question pair that tests the identical fact in identical framing.
- Rationales: mostly explanatory and content-based, not letter-based.

## (e) Counting adjudication (Lead Dev open question)

- I apply **conceptual distractor-type** interpretation (not raw literal service-token counting across all choices).
- Under that reading, "edge/hybrid placement misalignment" at 3/24 is within cap.
- I agree with Lead Dev that repeated appearances of `Outposts`/`Local Zones` in the specific placement objectives are on-topic and not materially guessable.
- I also accept the `Auto Scaling` distractor handling as conceptually distinct across scaling, hibernation interaction, and rightsizing contexts; repetition does not make outcomes guessable or the set monotonous for a learner.

## Issues

- `TEACHER-Q42-001` - **moderate**
  - **Location:** `q-saa-4-2-s01-mc`, distractor `"Classic Load Balancer"` and rationale phrase `"lacks the modern application-routing feature set"`
  - **Problem:** distractor-wrongness depends on CLB-specific knowledge not taught in lesson 4.2; teach-before-test is weaker here.
  - **Exact doc-verified fix:** replace distractor `d` with `Network Load Balancer with TLS listeners and static IPs` so wrongness is purely the taught Layer 4 vs Layer 7 routing contrast.
  - **URL:** `https://docs.aws.amazon.com/cli/latest/reference/elbv2/index.html`

- `TEACHER-Q42-002` - **moderate**
  - **Location:** `q-saa-4-2-s01-mr`, distractor `"AWS Global Accelerator endpoint group"`
  - **Problem:** wrongness relies on service behavior not taught in lesson; this creates out-of-scope elimination pressure.
  - **Exact doc-verified fix:** replace choice `d` with `Application Load Balancer with host/path routing rules` so the distractor is wrong for the taught reason (not appliance insertion/chaining).
  - **URL:** `https://docs.aws.amazon.com/cli/latest/reference/elbv2/index.html`

- `TEACHER-Q42-003` - **low**
  - **Location:** `q-saa-4-2-s04-mr`, distractor `"Store the checkout database on instance store volumes only"`
  - **Problem:** distractor shifts to storage-implementation trivia not taught in lesson 4.2 availability-class framing.
  - **Exact doc-verified fix:** replace choice `d` with `Run checkout in one Availability Zone with larger instances` so wrongness maps directly to taught multi-AZ production requirement.
  - **URL:** `https://docs.aws.amazon.com/wellarchitected/latest/reliability-pillar/rel_fault_isolation_multiaz_region_system.html`

Task 4.2: not yet
Overall: concerns

---

## Lead Dev notes on this report

### The three findings are accepted in substance; two of the proposed fixes are not

All three concerns are valid teach-before-test problems: the distractor's
wrongness depends on a fact lesson 4.2 never teaches. But two of the literal
replacements would create a duplicate concept inside the same question.

- `TEACHER-Q42-001`: `s01-mc` choice `a` is already
  `Network Load Balancer with TCP listeners`. Adding
  `Network Load Balancer with TLS listeners and static IPs` as choice `d` would put
  two NLB options in one question, both wrong for the identical reason (Layer 4,
  no path routing). That weakens the question rather than fixing it.
- `TEACHER-Q42-002`: `s01-mr` choice `a` is already
  `Application Load Balancer with path rules`. The proposed
  `Application Load Balancer with host/path routing rules` for choice `d` is a
  near-verbatim duplicate of it.

`TEACHER-Q42-003`'s proposed replacement is fine and creates no duplicate.

The writer has been asked to satisfy each concern while keeping all choices within
a question conceptually distinct, and to prefer RULES' other sanctioned remedy
where a distinct real option is hard to find: teach the missing fact in the lesson
with a doc-verified sentence and a citation, rather than swap the distractor.

### Citation quality

`TEACHER-Q42-001` and `-002` both cite
`https://docs.aws.amazon.com/cli/latest/reference/elbv2/index.html`, a CLI command
reference. That page does not explain load balancer selection. Any lesson sentence
added for these must cite a user-guide page, not the CLI reference.

### Correction to the distractor-count premise given to both reviewers

Lead Dev's pre-check figures (Outposts 4/24, Local Zones 4/24, Auto Scaling 6/24)
were **wrong, and too high**. The audit script matched on a non-existent `answer`
field, so correct answers were counted as distractors.

Re-measured against the real `correctAnswerIds` field, distractor-only counts are:

- Outposts 3 (k03-mc, k05-mc, k05-mr)
- Local Zones 3 (k03-mc, k05-mc, k06-mc)
- Spot 3, Reserved Instance 3, Fargate 3, Auto Scaling 3, Lambda 3
- everything else 2 or fewer

Every type is at or under 3 of 24 (12%), inside the 15% cap, on the literal
service-name reading as well as the conceptual one. The adjudication question put
to both reviewers is therefore moot: the task passes either way. The earlier
pre-check round was still worthwhile on its other two grounds (a distractor phrase
recycled near-verbatim in three questions, and one fixed-fleet strawman), both of
which were real and are now fixed.
