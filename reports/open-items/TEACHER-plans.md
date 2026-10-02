# Teacher pre-validation — master plan and P1–P5 (2026-10-02)

Saved by the Lead Dev (condensed). The Teacher ran `content_lint.py` (PASS) and `distractor_type_audit.py` on 10 SAA tasks, and read the registry, the lab files, `curriculum.ts` and both tab components. It had no AWS docs access in this run.

## P1 registry: concerns (folded in)
- **Wrong fact:** "2 rows drift" is false. K04 and K05 `drill_refs` match the questions' `objectiveIds`. The real issue is that they include the demo questions `q-a0-mr-001` and `q-a0-mc-001`, which have no `mcpStatus` and no citations.
- `docs/coverage-and-metrics.md` is still the Phase-0 skeleton ("0 / 189", every row `missing`) and must be refreshed.
- Define "verified" narrowly: reviewed on paper by the technical reviewer, the Teacher and a blind Student, with official citations. Never "tested", "exam-ready" or "run in AWS".
- The 25 live_aws rows must carry "paper review only; not run in AWS (D5)" in the row itself.
- Add pass criteria: the task's audit has no real-reuse FAIL (so P2 runs first), and every `validation_refs` path exists (the 1-1 evidence is a line in `progress.md`).
- The 20-row spot-check must include K04, K05, a single-drill row (there are 69), a design_exercise row and several live_aws rows.

## P2 audit scope: concerns (folded in)
- The facts are correct (9 FAIL tasks; 1-1 PASSes).
- Whole-task exclusions are blunt. For example, Lambda is 2.1-K12's subject but appears in unrelated 2-1 distractors.
- Subject terms should be printed and given a looser cap (about 40%), not silently skipped. Each exclusion cites a bullet ID.
- Candidates for real reuse: Compute Optimizer (3-2), NAT Gateway (3-4), and RDS in 2-2 (19%, borderline).
- 3-1 has only 8 questions, so a single repeat trips the cap. Note this or add a minimum-N rule.
- The Teacher proposes and the Lead Dev records; the plan should not say "written by the Teacher".

## P3 O8: approve
- The facts are correct.
- **Ruling:** remove `tf.004.8a` from gl-21 (no HCP content; "Terraform is not required"). Keep it on ul-21 as **partial**: sign-up, a remote-backend block and notes, but it stops before AWS credentials and never creates infrastructure through HCP.
- `tf.004.8a` is not in the SAA registry; check how the Coverage tab counts Terraform lab coverage instead.
- The all-labs title comparison must normalise benign differences; gl-20 and gl-03 are worth a look.

## P4 drill UI: approve
- The facts are correct.
- Start here's summary carries IDs only, so a catalog fetch is needed (the Lead Dev confirmed this).
- A stem preview is acceptable, as long as no cut stem reads as a different question.
- Putting the question above the grid adds a scroll after each answer (a study-loop cost; a "Next drill" control is out of scope).
- `slice.spec.ts` is one loose smoke test, so new tests carry the real coverage.

## P5 regional NAT gateway: approve option 1
- Record a revisit trigger (an exam guide update, or exam questions that include it).
- Optionally log the S01 "single AZ" sentence as a known zonal simplification.

## Master plan: concerns (folded in)
- The order is correct.
- State the P-label and phase-number mapping once.
- P2 needs a Teacher ruling.
- Add the coverage-doc refresh and the demo-drill decision to P1's phase.

**Overall:** P3, P4 and P5 approve. P1, P2 and the master plan approve once the edits above are made; they have been made.
