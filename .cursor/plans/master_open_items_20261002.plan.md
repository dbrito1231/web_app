# Master plan: open items after the Q1 rewrite (2026-10-02)

Author: Lead Developer. Status: **approved by the user 2026-10-04 (recommended option).** Each phase also needs its own approval: approving this master plan approves the order and the process, not every phase's option.

**Naming:** the plan files are called P1–P5 (by topic). The phases are numbered 1–5 in the order they run. Phase 1 runs plan P2, Phase 2 runs P3, Phase 3 runs P1, and Phases 4 and 5 run P4 and P5.

Source: the "Still open (true list)" in `reports/fix-loop/issue-register.md` (final reconciliation, 2026-10-01).

## Phases (in execution order)

| Phase | Plan | Item | Recommended option | Size | Learning content |
|---|---|---|---|---|---|
| 1 | P2 `p2_audit_terms_scope_20261002.plan.md` | `distractor_type_audit` FAILs on 9 closed SAA tasks | Per-task subject terms with a looser cap (Teacher proposes, Lead Dev records), plus an exam split | Small | No content; **Teacher ruling required** |
| 2 | P3 `p3_o8_lab_titles_20261002.plan.md` | O8: the sidebar still shows the old GL-07 and GL-21 titles; `tf.004.8a` on GL-21 | Fix the 2 nav strings, Teacher ruling on the objective, Student check | Small | Yes |
| 3 | P1 `p1_coverage_registry_verify_20261002.plan.md` | R6 / ISS-070: 189 registry rows say `implemented_unverified`; Coverage tab shows 0/189 verified | Evidence-based flip by script, after a Teacher spot-check; demo drills removed; stale `coverage-and-metrics.md` refreshed | Medium | Yes |
| 4 | P4 `p4_drill_list_ui_20261002.plan.md` | N4 raw drill IDs on Start here; N9 long card grid above the question | Stem preview labels; question shown above the grid | Small–medium | UI only (Teacher and Student check) |
| 5 | P5 `p5_regional_nat_gateway_20261002.plan.md` | Optional regional NAT gateway note in 4.4 | Close as won't-do (both reviewers advised against it) | Tiny | No (if option 1) |

### Why this order

- **Phase 1 (audit scope)** is self-contained and makes every later check trustworthy.
- **Phase 2 (O8)** may change a lab's objectives, which feed the coverage registry, so it runs before Phase 3.
- **Phase 3 (registry)** then verifies against final data.
- **Phase 4 (UI)** is independent.
- **Phase 5** is a decision only.

## Process (same for every phase)

1. **Before:** for every phase except plain decisions (plans P1, P2, P3, P4, and P5 if option 2 or 3), the Teacher validates the plan, as AGENTS.md requires. The verdict is recorded in `reports/open-items/<phase>-TEACHER-plan.md`.
2. **You approve** the phase plan and choose an option.
3. **Implement.** The Lead Dev writes, or Sonnet subagents do (at most 3 at a time, no git). Every check runs before and after, and the full outputs are diffed.
4. **After:** the Teacher re-validates content-affecting phases. A second role closes each register item (the reporter plus one other).
5. **Close:** update the register, `docs/status.md` and HANDOFF, and commit and push straight to `main` (your 2026-10-01 decision).
6. Stop after each phase and report. The next phase starts on your GO.

## Definition of done (each phase)

`manage.py test workbook`, `content_lint.py`, `npm run build` and the phase's own tests pass; the register item is closed by two roles; the status docs are updated.

## Not in scope

- The recorded length and key-set tells on closed tasks 1-2, 3-1, 3-3 and 3-5. You decided on 2026-09-28 to leave 3-1 and 3-5 closed.
- PY-R5 scanner trade-offs: a formal won't-fix needs only your yes or no, and no plan.
- Lab cosmetics (UL-21 dash encoding, UL-02 echo quirk) and the STUDENT-R6 note. Say so if you want any of these added as a phase.

## Teacher pre-validation (2026-10-02)

Done for all five plans (`reports/open-items/TEACHER-plans.md`). P3, P4 and P5 were approved. P1 and P2 had concerns, now folded in. The master plan had three edits (naming, P2 Teacher ruling, P1 files), now made. CRs logged: CR-0022 (stale coverage doc, P1) and CR-0023 (gl-21 objective and sidebar titles, P3).

## Decisions needed from you

1. Approve this master plan and its phase order?
2. For each phase: the recommended option, or another?

## Progress

| Phase | Plan | Status |
|---|---|---|
| 1 | P2 audit scope | **Closed 2026-10-04** (`69487ff`); Teacher close; the real reuse is logged as CR-0024 |
| 2 | P3 O8 lab titles | **Closed 2026-10-04**; Student and Teacher close; CR-0023 done; follow-up CR-0025 |

| 3 | P1 registry | **Closed 2026-10-07**; 119/189 verified on paper, 70 held back by CR-0024; Teacher pre/post; CR-0022 done; follow-up CR-0026 |
| 4 | P4 drill UI | **Closed 2026-10-07**; Teacher post-check approve; follow-up CR-0027 |
| 5 | P5 regional NAT gateway | **Closed 2026-10-07: won't-do**, recorded in the register |
