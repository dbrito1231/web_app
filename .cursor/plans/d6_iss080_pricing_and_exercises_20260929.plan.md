# Plan: D6 / ISS-080 — dated lab cost estimates and realistic design exercises

Status: **draft. It needs Teacher validation and then the user's approval.** Nothing is implemented before the user approves.
Author: Lead Dev, 2026-09-29. This implements the user's decision D6 ("fix", 2026-09-25; scheduled for this sitting on 2026-09-28).

## Goal

1. **Part A (AWS-210).** Each hourly lab's two cost figures are reconciled to official AWS pricing read on a stated date, and the learner can see what each figure assumes. This falls under the KISS rule's "protect you from a surprise bill".
2. **Part B (TEACHER-211).** The 60 design exercises stop being templates and become realistic case studies whose stakeholder constraints make the exercise's own exam objectives the deciding factors. This falls under the KISS rule's "teach an exam bullet".

## What is wrong today (measured)

**Part A**
- 16 labs are `hourly: true`: gl/ul-06, 07, 08, 09, 14, 18, 19 and 21. In every one, `forgotten24hEstimateUsd` is exactly 24 × `sameHourEstimateUsd`. The figures were derived mechanically, not priced.
- No lab states its assumptions. The only cost instruction is the generic "Review same-hour and 24-hour estimates".
- The two errors run in opposite directions:
  - **gl-08 (ALB) is likely too low.** It says $0.96 for a forgotten day. At the doc's own 2026-09-23 rates, ALB $0.0225/h plus t3.micro $0.0104/h plus public IPv4 addresses at $0.005/h each is already about $1.10/day, before any LCU charge.
  - **gl-14 (RDS, smallest single-AZ PostgreSQL) looks far too high.** It says $12.00 per forgotten day. That needs checking against the instance class the lab actually creates.
- An underestimate is the dangerous direction. An overestimate teaches the learner to distrust every figure.
- `docs/labs-and-safety.md` "Example rates" was read on 2026-09-23. It says "Fill before publish" for RDS, EBS, EFS, ElastiCache, Fargate, Step Functions, Athena, Route 53, WAF, Secrets Manager, GuardDuty and Macie, and was never filled.

**Part B**
- All 60 `content/exercises/de-*.json` share 3 scenario templates. Most read "You must design a solution addressing: <title>".
- All 60 share 3 constraint lists, which are generic safety rules (do not claim live experience, cite docs, and so on).
- Rubrics are adequate: TEACHER-211 rated them fine.
- All objectives are SAA. The most-used domains are 4.1 (11), 3.5 (9) and 2.2 (8).

## Part A — method

For each of the 8 guided labs, read the lab's own `steps`/`body` for exactly what it creates: instance class, count, storage, public IPv4 addresses, Availability Zones. Then:

1. **Price each resource** from the official AWS pricing page for `us-east-1`, read on the day of the work, and record the URL, a verbatim rate and the date in a claim table (`reports/fix-loop-r2/d6/pricing-claims.md`).
2. **Recompute both figures:**
   - `sameHourEstimateUsd`: the lab run at its `estimatedMinutes`, with partial hours billed as full hours where the pricing page says so (ALB, for example).
   - `forgotten24hEstimateUsd`: every resource left running for 24 hours.
   - Round **up** to the cent; never round down.
3. **Show the assumption to the learner** without a code change. Replace the generic "Review same-hour and 24-hour estimates" item in `beforeYouStart`, which the app already renders, with one line such as: "Cost basis (us-east-1, priced 2026-09-29): 1 ALB $0.0225/h + LCU, 1 t3.micro $0.0104/h, 3 public IPv4 $0.005/h each; forgotten 24 h ≈ $X."
4. **The ul-* twin** of each lab gets the same treatment. Its extra resources (WAF web ACL, EFS, Fargate profile and so on) are added to its own basis line.
5. **Fill the "Fill before publish" rates** in `docs/labs-and-safety.md` for the services these labs use, and re-date the section.

### Decision needed from the user: price source

The rule is "agents never call AWS". The options for reading prices:
- **(Recommended) the public AWS pricing web pages** (aws.amazon.com/<service>/pricing), read as rendered page text, the same way documentation is read. No credentials, no API, no account.
- **The public Price List bulk JSON files** (`pricing.us-east-1.amazonaws.com/offers/...`). No credentials, but it is an AWS service endpoint, so it is arguably "calling AWS". Not used unless the user allows it.
- **The Pricing API, the Pricing Calculator or any credentialed call: never.**

Some pricing pages load their tables with JavaScript. If a rate cannot be read as page text, the writer says so for that row and does **not** estimate it. The lab then keeps a conservative figure, marked "not reconciled".

## Part B — method

For each exercise, keep `id`, `title`, `practiceMode`, `objectiveIds`, `rubric`, `requiredArtifact` and `constraint_reason`. Rewrite:

- **`scenario`:** a named organisation and its situation, in 3–5 sentences. It gives concrete figures (users, request rate, data size, RPO/RTO, budget ceiling, compliance regime, team skill) chosen so that the exercise's own `objectiveIds` are what the design must turn on. It is written in the scenario's operational language, not the objective text (the paraphrase rule). No two scenarios share an organisation or opening words.
- **`constraints`:** keep the 4 safety constraints, and add 2–3 stakeholder constraints specific to the scenario. For example: "Finance caps the monthly run-rate at $400"; "The security lead requires customer-managed keys"; "Operations has no Kubernetes experience".
- **Accuracy:** every AWS fact a scenario relies on is checked with the AWS Knowledge MCP and recorded in a claim table.
- **Teach-before-test:** the services and trade-offs the exercise is meant to draw out must be taught in the lessons for its objectives. Anything else goes under "Lesson additions requested" rather than into the exercise.

**Batches:** 3 batches of 20, grouped by objective domain so one writer holds one domain's lessons. Each batch runs:
writer → Lead Dev pre-check (lint, an opening-words duplicate scan, and reading every scenario) → technical reviewer + Teacher (2 in parallel) → one fix pass → confirmation → commit.
A single Student run at the end reads 12 exercises across the batches and judges realism, whether each is answerable from the lessons, and whether any scenario gives its design away.

## Files touched

- **Part A:**
  - `content/labs/{gl,ul}-{06,07,08,09,14,18,19,21}.json` (the two estimate fields and one `beforeYouStart` line each);
  - `docs/labs-and-safety.md` (the rates section);
  - `reports/fix-loop-r2/d6/pricing-claims.md`.
- **Part B:** `content/exercises/de-*.json` (60 files) and `reports/fix-loop-r2/d6/exercises-batch{1,2,3}-*.md`.
- **Close:** `reports/fix-loop/issue-register.md` (D6 and ISS-080), `docs/status.md`, `HANDOFF.md`, `docs/change-requests.md` (CR-0016 note).
- **No app code, no schema change, no migration.**

## Learning content affected?

**Yes.** Labs (cost figures and the text the learner sees before starting), exercises (all 60), and a content-facing doc (`docs/labs-and-safety.md`). Per AGENTS.md the Teacher validates this plan before it goes to the user, and validates the result after.

## Risks

- **Wrong prices are worse than no prices.** Mitigation: verbatim rate plus URL plus date for every row; the technical reviewer re-reads every row; unreadable rates are marked, not guessed; figures round up.
- **Prices go stale.** Mitigation: every basis line carries its date, and the docs section says to re-read pricing before a lab run. This is the same stance the docs already take.
- **A lab's actual resources differ from what its text says.** Mitigation: price from the lab's steps, not its title. Any mismatch goes to the register as a separate finding and is not fixed silently.
- **Exercise scenarios drift into untaught material, or become strawman puzzles.** Mitigation: the teach-before-test rule, both reviewers, and the Student run.
- **Size.** 60 exercises is about the size of three question tasks. Mitigation: 3 batches, with a stop and report to the user after each sitting's quota.

## Tests (definition of done)

- `content_lint.py` PASS after every batch.
- **Part A:**
  - every one of the 16 labs has a dated basis line;
  - both figures trace to claim-table rows;
  - no figure lower than its computed cost;
  - the technical reviewer and the Teacher both close.
- **Part B:**
  - 60 distinct scenarios, with no shared 6-word opening (checked by a one-off read-only scan);
  - every scenario's objectives are checked against the lessons;
  - both reviewers close each batch;
  - the Student verdict is fair.
- `python manage.py test workbook` and `npm run build` still pass (no code changes are expected; run once at the end of Part A as a guard).
- The DB fingerprint is unchanged. `docs/status.md` is updated, and D6/ISS-080 is closed in the register.

## Order and sittings

This sitting: Teacher validation → user approval → **Part A** (1 writer, 2 reviewers) → **Part B batch 1**. Then tf-g5 when there is room.
Part B batches 2–3 go in the next sitting, alongside tf-g6.

## Estimated cost

- Part A: about 0.5M subagent tokens.
- Part B: about 0.5M per batch, so about 1.5M in total.
- The Student run: about 0.1M.

## Teacher validation (before user approval)

_Pending._
