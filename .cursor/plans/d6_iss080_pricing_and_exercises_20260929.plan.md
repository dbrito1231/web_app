# Plan: D6 / ISS-080 — dated lab cost estimates and realistic design exercises

Status: **approved by the user 2026-09-29.** Decision 1: **public pricing pages only**, read as page text. Decision 2: **B-2**, the small app change that shows constraints, deliverable and rubric on the exercise card. Nothing is implemented before the user approves.
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
3. **Show the assumption to the learner** without a code change:
   - **`beforeYouStart`.** Replace the generic "Review same-hour and 24-hour estimates" item with one basis line, for example: "Cost basis (us-east-1, priced 2026-09-29): 1 ALB $0.0225/h + LCU, 1 t3.micro $0.0104/h, 3 public IPv4 $0.005/h each; forgotten 24 h ≈ $X. This is a floor: it excludes data transfer and LCU/usage charges. Re-read the pricing page before you run the lab." Where a lab has no such item (for example `ul-08`), **add** the line instead.
   - **`stopChargesPanel`.** Add "Forgotten 24 h ≈ $X (a floor; see the cost basis)" here too, because this is where the learner is when deciding to stop (Teacher (a)).
   - **Every billable resource the steps create appears in the basis:** instances, public IPv4 addresses (their count differs by lab), Elastic IPs, NAT, load balancers, storage and add-ons such as the WAF web ACL.
4. **Each ul-* twin is priced from its own steps**, not copied from its gl-* pair. `ul-08` currently shows the same 0.04/0.96 as `gl-08` despite adding a WAF web ACL. Its basis line is added where no estimate item exists (Teacher (b)).
5. **Fill the "Fill before publish" rates** in `docs/labs-and-safety.md` for the services these labs use, and re-date the section.

### Decision 1 needed from the user: price source

The rule is "agents never call AWS". The options for reading prices:
- **(Recommended) the public AWS pricing web pages** (aws.amazon.com/<service>/pricing), read as rendered page text, the same way documentation is read. No credentials, no API, no account.
- **The public Price List bulk JSON files** (`pricing.us-east-1.amazonaws.com/offers/...`). No credentials, but it is an AWS service endpoint, so it is arguably "calling AWS". Not used unless the user allows it.
- **The Pricing API, the Pricing Calculator or any credentialed call: never.**

Some pricing pages load their tables with JavaScript. If a rate cannot be read as page text, the writer says so for that row and does **not** estimate it. The lab keeps a conservative figure, and the learner-facing wording says what that means: "rate not verified on <date>; assume it is higher" — never a bare "not reconciled" label (Teacher (f)).

## Part B — method

For each exercise, keep `id`, `title`, `practiceMode`, `objectiveIds`, `rubric`, `requiredArtifact` and `constraint_reason`. Rewrite:

- **`scenario`:** a named organisation and its situation, in 3–5 sentences. It gives concrete figures (users, request rate, data size, RPO/RTO, budget ceiling, compliance regime, team skill) chosen so that the exercise's own `objectiveIds` are what the design must turn on. It is written in the scenario's operational language, not the objective text (the paraphrase rule). No two scenarios share an organisation or opening words.
- **`constraints`:** keep the 4 safety constraints, and add 2–3 stakeholder constraints specific to the scenario. For example: "Finance caps the monthly run-rate at $400"; "The security lead requires customer-managed keys"; "Operations has no Kubernetes experience".
- **Accuracy:** every AWS fact a scenario relies on is checked with the AWS Knowledge MCP and recorded in a claim table.
- **Teach-before-test:** the services and trade-offs the exercise is meant to draw out must be taught in the lessons for its objectives. Anything else goes under "Lesson additions requested" rather than into the exercise.

- **Rubric (Teacher (c)):** add 1–2 scenario-specific rubric items per exercise (for example, "Meets the stated RTO of 15 minutes" or "Stays under the $400 monthly cap"). Each must be checkable against the scenario's own figures. The 5 generic items stay.
- **Named services are taught (Teacher (e)):** every AWS service a scenario names must appear in a lesson for one of its `objectiveIds`. This is checked with a case-insensitive, backtick-tolerant regex.
- **Consistency:** the scenario's figures must be internally consistent, and must not leave two defensible designs. The technical reviewer confirms the objectives really are the deciding factors. There are no real customer names, and no dollar prices in scenarios (they date quickly); budgets are stated as caps.
- **Keep `constraint_reason` and the "why live lab was unsuitable" rubric item consistent with the new scenario.**

**Batches:** 3 batches of 20, grouped by objective domain so one writer holds one domain's lessons. **Assignment rule (Teacher (d)):** an exercise goes to the batch of its first `objectiveIds` entry. The batch lists are fixed and written into batch 1's report before any writing starts. Each batch runs:
writer → Lead Dev pre-check (lint, an opening-words duplicate scan, and reading every scenario) → technical reviewer + Teacher (2 in parallel) → one fix pass → confirmation → commit.
A single Student run at the end reads 12 exercises across the batches and judges realism, whether each is answerable from the lessons, and whether any scenario gives its design away.

### Decision 2 needed from the user: learners cannot see most of an exercise today

Found while checking the Teacher's point 5. For a design exercise, the app sends and shows only **`title` and `scenario`**: `backend/workbook/content_loader.py` `exercise_index()` serves id, title, objectiveIds and scenario, and `StartHereTab.tsx` renders the scenario. `constraints`, `rubric` and `requiredArtifact` exist in the JSON but **have never reached a learner**. The options:

- **(Recommended) B-2: a small app change to show them.** `exercise_index()` also serves `constraints`, `requiredArtifact` and `rubric`, and the Start here exercise card renders them as a short list with points. This is roughly 20–30 lines of backend and frontend code plus one Django test. Without it, a learner cannot self-grade, and the Teacher's rubric change is invisible. The change passes the KISS rule: it lets you score your own design against the exam bullet.
- **B-1: content only.** Put the stakeholder constraints and the deliverable into the `scenario` text, which is visible, and drop the rubric additions, which nobody would see. Cheaper, but the exercise stays ungradable by the learner.

## Files touched

- **Part A:**
  - `content/labs/{gl,ul}-{06,07,08,09,14,18,19,21}.json` (the two estimate fields and one `beforeYouStart` line each);
  - `docs/labs-and-safety.md` (the rates section);
  - `reports/fix-loop-r2/d6/pricing-claims.md`.
- **Part B:** `content/exercises/de-*.json` (60 files) and `reports/fix-loop-r2/d6/exercises-batch{1,2,3}-*.md`.
- **Close:** `reports/fix-loop/issue-register.md` (D6 and ISS-080), `docs/status.md`, `HANDOFF.md`, `docs/change-requests.md` (CR-0016 note).
- **Part A: no app code.** Part B with option B-2: `backend/workbook/content_loader.py`, `frontend/src/components/StartHereTab.tsx`, `frontend/src/types/index.ts`, one test in `backend/workbook/tests*`. No schema change, no migration.

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

Fresh Sonnet Teacher, 2026-09-29. Verdict: **Plan: concerns**, with six required changes. **All six are now applied above:**
- (a) the forgotten-24h figure, the floor and exclusions note, and the "re-read pricing" line go into `stopChargesPanel` and the basis line;
- (b) ul-* twins are priced from their own steps, and the line is added where there is no item to replace;
- (c) 1–2 scenario-specific rubric items per exercise;
- (d) the batch-assignment rule;
- (e) a check that every named service is taught;
- (f) "not reconciled" is worded as "assume higher".

Also from the Teacher:
- Put a real stakeholder layer into the scenarios. 40+ of them are currently the pasted objective text ("Design a solution that demonstrates skill: …").
- Keep `constraint_reason` consistent with each new scenario.
- On price source, either option is acceptable from a teaching point of view, provided every row keeps its verbatim rate, URL and date.

Lead Dev follow-up to the Teacher's point 5 ("confirm no code reads `scenario`/`constraints`"): code does read `scenario`, for display only, with no scoring. **Nothing reads `constraints` or `rubric` at all.** That is Decision 2 above.

## Progress (2026-09-29)

- **B-2 app change: done** (`fc06fdb`). 91 Django tests OK; build OK.
- **Part A: closed** (`44ea124`). Reports: `reports/fix-loop-r2/d6/pricing-{claims,review,review-TEACHER,leaddev-precheck}.md`.
  - **Method finding:** the JavaScript pricing tables can be read from the `c0.b0.p.awsstatic.com` widget iframe, set to US East (N. Virginia).
  - **Still unverified** (marked in the labs): NAT, WAF, RDS storage (priced at io1 as an upper bound), EFS and the CloudWatch alarm.
  - **LD-PA-001 was withdrawn:** EC2, EBS, public IPv4 and Fargate bill per second.
- **Part B batch 1: closed** (`10fe035`). Reports: `exercises-batch1-{impl,review}.md`.
- **Remaining:** Part B batch 2 (16 exercises, domain 3, including de-snow with its closed-service label) and batch 3 (24, domain 4); the Student run across the batches; close-out.
- **Spun off:** CR-0018 (lesson 2.2 "8.7 hours" / "52 minutes" and q-saa-2-2-s03-mc), which needs its own inline plan.

## Close-out (2026-09-30)
- **Exercise batches:** batch 2 (16) and batch 3 (24; split 3a/3b across two writers at the user's request) are closed. Tech and Teacher closed both after one fix pass, and every finding was confirmed Gone by its reporter and a second role.
  - de-tgw was trimmed per the user's decision on CR-0020.
- **Student:** two runs (run 1 stopped on an API false positive after committing all designs). 12/12 designs match, verdict fair. One ambiguity (de-saa-4.1-s05) was fixed at c47c3de and confirmed Gone by the Teacher.
- **Spun off:**
  - CR-0018: done.
  - CR-0019 (Glue for Ray): deferred to the final sitting.
  - CR-0020: decided (trim).
  - Lesson follow-ups: register row D6-FU.
- **Definition of done:** 91 Django tests OK, `npm run build` OK, `content_lint` PASS, `scan_lab_placeholders` PASS 42, letter self-test PASS, DB fingerprint unchanged, 0 of 60 template scenarios left.
