# Coverage and metrics

Curriculum coverage registry, readiness formulas, MCP validation, and baseline audit. Spec version 1. Implements REQ-P30–P35, REQ-P15. Access date: 2026-09-23.

Primary sources:

- Supplied PDF: `solutions-architect-associate-03.pdf` (SAA-C03 exam guide, copyright 2026 Amazon Web Services). 30 physical pages; printed pages 1–26 map to physical pages 5–30 (add 4).
- Coverage contract: `C:\Users\dbadmin\Downloads\cursor_saa_c03_exam_objectives_coverage.md`
- Terraform Associate (004): [exam content list](https://developer.hashicorp.com/terraform/tutorials/certification-004/associate-review-004). Objectives 1a–1c through 8a–8d (37 lettered). Weights, item count, and passing score stay `unpublished`. Cover both wordings of 4f and 4h.

Local tracking IDs such as `SAA-1.1-K01` are project IDs, not AWS-issued.

## Discrepancy log (2026-09-23)

REQ-C01. PDF is authoritative for which bullets exist.

| Item | Disposition |
| --- | --- |
| Online edition lists AWS AppSync (twice), Amazon Kendra, AWS Audit Manager; supplied PDF does not | Record as `edition_variance`; teach at awareness level; exclude from service denominator |
| `SAA-2.2-K02` examples list AMS with Comprehend / Polly | Preserve PDF wording; do not teach Comprehend or Polly as AMS components; add flagged current-docs note when authored |
| Guide names Amazon Quick, Amazon SageMaker AI | Keep guide names; add cited current-status note when branding differs |
| Amazon Redshift listed in two PDF categories | Preserve both placements; dedupe for unique-service counts |

## MCP validation (authors/reviewers, not the app)

REQ-C10. AWS items: AWS Knowledge MCP Server (`search_documentation` / `read_documentation`). Store official URL and accessed date.

REQ-C11. Terraform items: Terraform MCP Server **registry/docs tools only**. No HCP workspace create/update/delete/run. Store registry or HashiCorp URL and accessed date.

REQ-C12. If PDF and MCP disagree: keep PDF wording, flag a note, log the discrepancy. Phase 3, 4, and 6 content tasks do not start if these servers are missing.

## Stable identifiers

Examples: `SAA-1.1-K01`, `tf.004.4f`, `lesson.m6.workflow`, `q.m6.014`, `lab.gl07`, `lab.ul07`, `DE-*`.

## Registry row fields

`objective_id`, `domain`, `task`, `ks`, `source_text`, `lesson_refs`, `drill_refs`, `guided_refs`, `unguided_refs`, `exercise_refs`, `practice_mode`, `constraint_reason`, `validation_refs`, `status` (`missing` \| `planned` \| `partial` \| `implemented_unverified` \| `verified`), `gap`, `owner`, `next_action`.

## Curriculum coverage formulas (workbook, not learner)

Half-up whole percents:

- Verified atomic = verified / 189 × 100
- Domain coverage against 32 / 43 / 50 / 64
- Weighted guide coverage = 0.30×D1 + 0.26×D2 + 0.24×D3 + 0.20×D4
- Task and K/S counts separate; live vs design-exercise separate; planned vs verified separate
- Service awareness uses its own denominator (Redshift deduped; `edition_variance` excluded)
- None of these is a pass probability or scaled score

## Learner metrics

- Lesson completion = read / in scope (exposure, not mastery)
- Drill completion = distinct attempted ids / in scope
- Accuracy = correct first-attempt exam-mode / first-attempt exam-mode (“no attempts” if denominator 0)
- Lab completion = all checkpoints self-reported; cleanup recorded separately
- Mastery “not assessed” until attempts exist

## Readiness formula (locked)

Not a pass probability. Integer display. Caption: weighted summary of this workbook’s practice, not a prediction.

```
readiness = round(100 * (0.70 * weightedFirstAttemptAccuracy + 0.20 * objectiveCoverage + 0.10 * recentAccuracy))
```

- AWS withheld until ≥40 first-attempt exam-mode items and ≥5 in each of 4 domains; else “insufficient evidence” plus missing counts.
- Terraform withheld until ≥30 first-attempt exam-mode items and ≥2 in each of 8 groups.
- Recent accuracy: last 14 days if those 14 days have ≥10 items; else the 0.10 weight moves onto first-attempt accuracy.
- AWS domain weights in the formula: 30/26/24/20, renormalized across domains with attempts.
- Terraform: equal group weights; state that HashiCorp publishes none.
- Objective coverage in the formula = fraction of atomic AWS bullets (or Terraform lettered objectives) with at least one first-attempt item. Not lessons read. Not curriculum coverage.
- Assisted attempts excluded. No partial-credit path.
- Confidence: `low` just above threshold; `medium` at ≥80 AWS or ≥60 Terraform items with every domain/group represented. Never “likely to pass.”
- Trend vs score stored 7 days earlier, in percentage points. If either side was insufficient evidence, say that instead of a delta.

## Mock exam

50 items, 15/13/12/10 by domain. Raw score out of 50 and by domain. Never 100–1000 scaled; never compared to 720.

## 14-task rollup

Statuses as of 2026-10-07 (Phase 3), from `content/coverage/saa_registry.json`. Domain weights are official; bullet counts are project coverage units.

| Task | Domain | Weight | K | S | Total | Status |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| 1.1 | 1 | 30% | 5 | 6 | 11 | verified |
| 1.2 | 1 | 30% | 6 | 4 | 10 | verified |
| 1.3 | 1 | 30% | 4 | 7 | 11 | verified |
| 2.1 | 2 | 26% | 16 | 7 | 23 | verified |
| 2.2 | 2 | 26% | 12 | 8 | 20 | implemented_unverified (CR-0024) |
| 3.1 | 3 | 24% | 3 | 2 | 5 | implemented_unverified (CR-0024) |
| 3.2 | 3 | 24% | 6 | 4 | 10 | implemented_unverified (CR-0024) |
| 3.3 | 3 | 24% | 8 | 5 | 13 | implemented_unverified (CR-0024) |
| 3.4 | 3 | 24% | 4 | 4 | 8 | implemented_unverified (CR-0024) |
| 3.5 | 3 | 24% | 7 | 7 | 14 | implemented_unverified (CR-0024) |
| 4.1 | 4 | 20% | 11 | 10 | 21 | verified |
| 4.2 | 4 | 20% | 9 | 6 | 15 | verified |
| 4.3 | 4 | 20% | 9 | 5 | 14 | verified |
| 4.4 | 4 | 20% | 7 | 7 | 14 | verified |
| **Sum** | | | **107** | **82** | **189** | |

Domain totals: D1=32, D2=43, D3=50, D4=64.

## Terraform Associate (004) outline

Letter groups (37 lettered). Separate readiness and bank from SAA.

| Group | Letters (count) | Bank floor |
| --- | --- | ---: |
| 1 | 1a–1c (3) | ≥3 each / ≥9 group contribution toward 111 |
| 2 | 2a–2d (4) | ≥3 each |
| 3 | 3a–3g (7) | ≥3 each |
| 4 | 4a–4h (8) | ≥3 each; cover both 4f and 4h wordings |
| 5 | 5a–5d (4) | ≥3 each |
| 6 | 6a–6d (4) | ≥3 each |
| 7 | 7a–7c (3) | ≥3 each |
| 8 | 8a–8d (4) | ≥3 each; HCP no-charge only |

Overall Terraform bank floor: ≥111 items.

## Service awareness map (in-scope from PDF)

Status for every named service: `missing` awareness content. Deduped Redshift counts once. `edition_variance` (AppSync, Kendra, Audit Manager) excluded from denominator.

Categories (PDF pp. 16–22): Analytics; Application Integration; Business Applications; Cloud Financial Management; Compute; Containers; Database; Developer Tools (in-scope subset per PDF); Front-End Web and Mobile; Machine Learning; Management and Governance; Media Services; Migration and Transfer; Networking and Content Delivery; Security, Identity, and Compliance; Serverless; Storage.

Out-of-scope tooling/guardrail services (PDF pp. 22–25) must not inflate the SAA service denominator (MWAA, Sumerian, Managed Blockchain, Lightsail, RDS on VMware, CDK/Code* family, IoT all, Braket, Ground Station, etc. — full list in coverage contract).

## Gap report (Phase 3, 2026-10-07)

`verified` means **reviewed on paper**: the lesson and drills for the row were reviewed by a technical reviewer, the Teacher and a blind Student, with official citations, and the task's distractor-type audit passes. It does not mean tested, exam-ready, or run in AWS. Labs are never run against AWS by agents (decision D5), so the 15 verified `live_aws` rows carry "paper review only; not run in AWS (D5)" in `gap`. The Teacher spot-checked 18 of the 119 verified rows, not every row (`reports/open-items/phase3/`). `scripts/registry_verify.py` re-checks every row (read-only by default; `--write` applies).

| Gap | Severity | Notes |
| --- | --- | --- |
| 70 rows unverified: tasks 2.2, 3.1, 3.2, 3.3, 3.4, 3.5 | medium | Real distractor reuse in the task's questions (CR-0024). Each row's `gap` names the audit result; re-run `registry_verify.py --write` after CR-0024 closes |
| Demo drills `q-a0-*` | closed | Removed from the drill_refs of `SAA-1.1-K04` and `K05` |
| Lab prices unfinished (RDS, EBS, ...) | medium | Fill from official pages before verified |
| Terraform 37 lettered objectives | tracked outside this registry | Mapped by lessons tf-g1 to tf-g8, not by `saa_registry.json` |

Verified atomic coverage: **119 / 189 (63%)**. Domain coverage: D1 32/32 (100%), D2 23/43 (53%), D3 0/50 (0%), D4 64/64 (100%). Weighted guide coverage: **64%** (0.30x100 + 0.26x53 + 0.24x0 + 0.20x100). Neither figure is a pass probability.

## Proposed mappings (planning only)

| Module | Objectives | Proposed labs | Proposed drills |
| --- | --- | --- | --- |
| A0 | Safety, shared responsibility, MFA, budgets, tags (`SAA-1.1-K05`, `SAA-1.1-S01`, Domain 4 cost tools) | GL-01 | ≥20 MC/MR |
| A1 | Domain 1 (32) | GL-01–04 | ≥36 domain share of AWS bank |
| A2 | Domain 2 (43) | GL-05–11 | ≥48 |
| A3 | Domain 3 (50) | GL-07–19 selective | ≥56 |
| A4 | Domain 4 (64) | Cost-focused steps + DE-* | ≥70 |
| T1–T4 | tf.004.* | GL-20–21 | ≥111; ≥20/module |

Skill bullets without disposable live services → `design_exercise` with rubric (see `docs/labs-and-safety.md`).

## Budget decisions (locked)

- $10 is a warning, not a retain/stop rule (confirmed 2026-09-23).
- Learner accepted spend above $10 for hands-on labs.
- Alert-only budget; no budget actions.
- Expensive services remain in labs the learner runs; agents never create them.

## 189-row registry

The source of truth is `content/coverage/saa_registry.json` (count must remain exactly 189; `content_lint.py` checks it). The Phase-0 skeleton table that was here listed every row as `missing` and has been removed because it contradicted the registry. Row fields are listed under "Registry row fields".
