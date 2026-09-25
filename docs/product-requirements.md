# Product requirements

Workbook: AWS Solutions Architect + Terraform Lab Workbook. Spec version 1. Access date for certification baselines: 2026-09-23.

Owning plan: [`.cursor/plans/aws_terraform_workbook_92c3d04f.plan.md`](../.cursor/plans/aws_terraform_workbook_92c3d04f.plan.md). Approved for implementation 2026-09-23. Phase 0 writes specs only; application code starts in Phase 1.

**KISS rule:** if a feature does not teach an exam bullet, protect the learner from a surprise AWS bill, or score/store progress, do not build it.

## Scope

REQ-P01. Local single-user learning app. React UI + Django on `127.0.0.1` + SQLite file on this PC. No hosting, no login, no cloud database, no LLM API, no browser terminal, no AWS API calls from the app.

REQ-P02. Teaches the supplied SAA-C03 exam guide at the level of all 189 atomic objective bullets, plus Terraform Associate (004) lettered objectives 1a–8d (37 lettered).

REQ-P03. Learner runs AWS CLI and Terraform in their own terminal. The app never receives credentials or account IDs.

REQ-P04. Agents never create, change, start, stop, tag, or delete anything in AWS. Agents never run credentialed Terraform apply/destroy/plan. Agents never operate HCP workspaces. See REQ-P99.

REQ-P05. Coverage reports “coverage of the supplied guide,” never “all possible exam questions.”

REQ-P06. Windows 11. Lab commands are PowerShell first. Show bash only where syntax differs.

REQ-P07. Learning path unlock: A0 → A1 → A2 → A3 → A4, then T1 → T2 → T3 → T4. AWS modules and labs first; Terraform reuses the A0/A1 IAM/S3 baseline.

REQ-P08. Direct Connect, Outposts, Snow, Wavelength, VMware Cloud on AWS, Shield Advanced, and CloudHSM stay in lessons and design exercises. Not created live.

REQ-P09. HCP Terraform: no-charge hands-on only. Otherwise docs, drills, and a design exercise. Never connect AWS credentials to HCP on a paid path.

## Drill bank and assessment

REQ-P10. At least 210 AWS items and 111 Terraform items (321+), at least 20 questions per module.

REQ-P11. Formats are multiple choice (one of four) and multiple response (prompt states how many) only. No matching, ordering, or drag-and-drop.

REQ-P12. Mock exam: 50 items, domain allocation 15/13/12/10. Raw score only. Never a scaled score. Never equate 720 with 72%. Never convert practice accuracy into a scaled score.

REQ-P13. Scoring is all-or-nothing in practice and exam modes. Rationale after submit. First attempt is the first exam-mode submit for a question id. Reveal or hint before submit marks `assisted` and drops first-attempt accuracy.

REQ-P14. Shuffle choice order per attempt; store presented order; stem and correct choice ids stay stable. If a question changes, give it a new id.

REQ-P15. Every exam-style item has at least one atomic objective id, one official citation, and a rationale. AWS items validated via AWS Knowledge MCP; Terraform items via Terraform MCP registry/docs only. MCP is not part of the running app.

REQ-P16. Difficulty mix guideline inside a module: about 30% foundation, 50% applied, 20% tradeoff (not lint-enforced).

## Labs

REQ-P20. Twenty-one guided and twenty-one unguided lab pairs. Each guided lab has at least 15 execution steps. Each unguided lab has at least 15 acceptance criteria.

REQ-P21. Every lab has teardown commands, verification commands, and a Stop charges panel visible from the first create step. Unguided teardown is available without opening the gated solution.

REQ-P22. $10 is a warning, not a stop. Alert-only budget thresholds: actual $2/$5/$8, forecast $5/$8. Alerts do not stop spend (~8–12 hour lag).

REQ-P23. Hourly labs GL-06, GL-07, GL-08, GL-09, GL-14, GL-18, GL-19, GL-21 require typing `I ACCEPT THE COST RISK` before create/apply steps.

REQ-P24. Default region `us-east-1`. Tags: `Workbook=aws-tf-lab`, `LabId`, `CreatedAt`, `ExpiresAt` same calendar day.

REQ-P25. Destructive commands print account, region, and resource id, then require the learner to type the account id. Kill switch is a GL-01 PowerShell snippet the learner runs; not a product feature and not agent-executed.

REQ-P26. Free Tier is never assumed. Named CLI profile or Identity Center session. No keys in git or the app. No root keys. State gitignored.

REQ-P27. Stopping an instance is not teardown. Complete requires every verification box checked (self-reported). Lab evidence status is `not-started` | `self-reported` | `unresolved`, never shown as “verified in AWS.”

## Coverage and readiness

REQ-P30. Exactly 189 SAA atomic IDs in the coverage registry. Knowledge bullets need lesson + assessment. Skill bullets need lab step or labeled design exercise with rubric.

REQ-P31. Separate AWS and Terraform readiness scores using the formula in `docs/coverage-and-metrics.md`. Never show a pass probability. Insufficient evidence until thresholds are met.

REQ-P32. Progress vs curriculum coverage stay separate. Mastery shows “not assessed” before attempts exist. Zero verified curriculum coverage means the workbook is unverified, not that the learner knows nothing.

REQ-P33. All 189 IDs start `missing`. No contract checkbox is satisfied until Phase 6 evidence. Status values: `missing` | `planned` | `partial` | `implemented_unverified` | `verified`.

REQ-P34. Every content item has `practice_mode` of `live_aws`, `local_validation`, `design_exercise`, or `concept_review`, plus `constraint_reason` when live execution was rejected.

REQ-P35. Purchasing bullets are analysis only: never buy a Savings Plan, Reserved Instance, subscription, or hardware as an exercise.

## UI and delivery

REQ-P40. Visual chrome is defined only in [`.cursor/plans/ccna_layout_replica_160c046c.plan.md`](../.cursor/plans/ccna_layout_replica_160c046c.plan.md). Four tabs only: Labs, Exam drills, Coverage, Start here. Phase 1 implements that layout. Phase 0 does not build UI.

REQ-P41. Functional surfaces (labs, MC/MR, coverage registry, cost/teardown, export/import, readiness) render inside those four tabs. Do not invent a different shell.

REQ-P42. Accessibility: visible focus, skip link, labeled controls, WCAG 2.2 AA, keyboard path, no information by color alone, 375px and 1280px, copy button plus `<pre>`.

REQ-P43. Follow `prefers-color-scheme` and `prefers-reduced-motion`. No theme toggle.

REQ-P44. Clean install success: `npm ci`, `npm run dev`, and `npm run build` succeed on Node 24; Django scoring and SQLite persistence work on Python 3.13 latest micro + Django 6.1.1.

## Data and security

REQ-P50. Content in git; learner records in SQLite (`backend/db.sqlite3`, gitignored). React bundle does not embed answer keys.

REQ-P51. Export `workbook-progress.json` with `schemaVersion: 1`. Import validates, rejects unknown future versions, replace or abort. Corrupt file does not change the database. Reset requires typing `RESET`.

REQ-P52. Threat model: Markdown without raw HTML; size-capped schema-checked imports; `rel="noopener noreferrer"`; no CLI output uploaded; CSRF on; lockfiles committed; state and `db.sqlite3` never in git. Public hosting needs a new ADR.

REQ-P53. Settings copy (Start here tab) states that another local process could call the Django port, and that answer keys exist in content files and SQLite.

## Orchestrator loop

REQ-P60. Orchestrator / implementer loop with path locks. No required model name or slug. Orchestrator is read-only except `docs/status.md`. Implementer never touches AWS.

REQ-P61. Specs in `docs/` (five files) before application code. Every behavior traces to a REQ id. Wrong spec → update markdown first, then stop for review.

## Out of scope

REQ-P90. Multi-user accounts, public hosting, AWS calls from the app or agents, leaked exam items, numeric chance of passing, Django REST framework unless a later ADR, matching/ordering/DND, live agent Terraform apply, HCP workspace ops by agents, LLM API, browser terminal, required model slug, AWS API MCP or any provisioning MCP.

## Agent AWS isolation

REQ-P99. Orchestrator, implementer, and any subagent must not call AWS APIs, AWS CLI, or Console; must not inventory or clean up the learner account; must not use AWS API MCP or any provisioning MCP. Allowed: write files; `terraform fmt` / `terraform validate` without credentials; AWS Knowledge MCP docs; Terraform MCP registry/docs only. Live lab commands stay labeled **unexecuted** until the learner reports that they ran them.
