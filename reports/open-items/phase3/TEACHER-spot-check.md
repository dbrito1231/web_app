# Phase 3 Teacher spot-check (pre-write), 2026-10-07

Saved by Lead Dev (the Teacher writes no files). Scope: 18 of the 119 proposed-verified rows, not every row.

Rows checked (all approved except the two noted): SAA-1.1-K01, K02, K03, K04, K05, S01, S02, S04; SAA-2.1-K01, K02, K03, S01, S02; SAA-4.1-K01, K02, K03, S01; SAA-4.2-S06. Mix: live_aws (1.1-S01, 1.1-S02, 2.1-S01, 4.2-S06), design_exercise (1.1-S04, 2.1-S02, 4.1-S01), single-drill rows (1.1-K02, K03, K05; 2.1-K01, K03; 4.1-K01, K03). Domain 3 has no proposed-verified rows.

Verdict: **approve, conditional on TEACHER-P3-001.**

| ID | Finding | Disposition |
| --- | --- | --- |
| TEACHER-P3-001 | Coverage tab caption and "verified with evidence" label overclaim for paper-reviewed rows; no "not a pass probability" text on the tab | Fixed in `CoverageTab.tsx` in the same change set as `--write` |
| TEACHER-P3-002 | 1.1-S04: Control Tower gets one mention in the lesson, while the drill turns on it | Follow-up (not blocking) |
| TEACHER-P3-003 | 1.1-K05: one foundation-level drill left after the demo drills are removed | Follow-up: add a second drill |
| TEACHER-P3-004 | 4.2-S06: lesson never names Compute Optimizer or percentile sizing; mc is solvable by "next size up" | Follow-up: content improvement |
| TEACHER-P3-005 | Docs must not imply the Teacher read every row | Done: gap report says 18 of 119 were spot-checked |
