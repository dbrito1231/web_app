# Agent 2 — Teacher evaluation report

**Date:** 2026-09-25  
**Role:** Teacher (read-only correctness)  
**Scope baseline:** `reports/evidence/intended-design.md`, stratified sample `reports/evidence/sample.md` (429/429 questions), inventory (23 lessons, 42 labs, 60 exercises)  
**Checks run (read-only):** `content_lint.py` PASS, `scan_lab_placeholders.py` PASS, content scan heuristics, MCP AWS Budgets + Terraform AWS provider docs, HashiCorp CLI `plan -refresh-only` reference  
**Not run:** Live AWS lab execution, credentialed `terraform apply`, UI click-through (see Agent 3 evidence under `reports/evidence/ui/`)

---

## Evaluation Scope

| Area | Coverage | Method |
| --- | --- | --- |
| Lessons (23) | All files in `content/lessons/` | Full read of structure, `drillIds`, citations, lab/exercise links; body spot-check all SAA + all 8 Terraform lesson files |
| Exam drills (429) | Full bank IDs in `sample.md` | Template/heuristic triage + stratified deep read (A0, SAA 1.1–4.4, TF 004 groups, HCP extras) |
| Design exercises (60) | 18+ stratified (`de-*` topical + `de-saa-*` per domain) | JSON rubric/scenario/constraints review |
| Guided labs GL-01…GL-21 | All 21 | Full read GL-01,02,06,10,12,20,21; spot-check remainder via scan + CR-0005 regression targets |
| Unguided labs UL-01…UL-21 | All 21 | Preflight/criteria/teardown spot-check (UL-01,02 pattern); scan flags |
| Terraform | Lessons T1–T4, GL-20/21, `lab-fixtures/gl-20` | Fixture HCL + lab steps; validate PASS per preflight evidence |
| Citations / MCP | All questions + citation files | `mcpStatus` census; sample MCP recheck for Budgets + S3 public access block |

**CR-0005 post-implementation:** Teacher re-review completed here. Verdict: **concerns (partial regression fix)** — automated placeholder scan PASS and many former blockers are fixed, but exam navigation, drill bank pedagogy, and a few lab content mismatches remain (details below). Do **not** treat CR-0005 as fully closed from a learning-quality perspective until follow-up CRs land.

---

## Confirmed Issues

### F-01 — Lesson drill ID dot/hyphen mismatch (regression of CR-0001 pattern)

- **Severity:** High  
- **Category:** content-error / navigation  
- **Location:** `content/lessons/lesson-1-2.json` through `lesson-4-4.json` (20 lessons); contrast `lesson-1-1.json`  
- **Evidence:** EV-TEACHER-003, EV-TEACHER-004  
- **Description:** Twenty SAA lesson files list `drillIds` with dots in the lesson segment (`q-saa-3.2-k02-mc`). Question files on disk use hyphens (`q-saa-3-2-k02-mc`). Lesson 1-1 was fixed under CR-0001; the same defect persists elsewhere.  
- **Impact:** Lesson-linked drills may 404 or fail to load wherever the UI/API resolves drills strictly from `drillIds`. Learners studying from lessons miss the intended MC bank.  
- **Reproduction/Validation:** Open any affected lesson JSON `drillIds` entry and compare to `content/questions/` filename.  
- **Recommended Improvement:** Bulk-replace dot lesson segments with hyphens in all `drillIds` (mirror CR-0001). Add lint rule: every `drillIds` entry must match an existing question file.  
- **Confidence:** High  

**Draft CR (Lead Dev to record):**

- Raised by: Teacher  
- Date: 2026-09-25  
- Type: content-error  
- Where: `content/lessons/lesson-1-2.json` … `lesson-4-4.json`  
- Problem: Dot vs hyphen drill ID mismatch (20 lessons).  
- Suggested fix: Hyphenate all `drillIds`; extend content lint.  
- Affects learning content: yes  
- Status: open  

---

### F-02 — Template MC bank teaches test-taking heuristics, not exam skills

- **Severity:** High  
- **Category:** content-quality / pedagogy  
- **Location:** ~227 MC files with stem prefix `Which statement best reflects this exam objective` + ~74 `mc2` variants; e.g. `q-saa-1-1-k01-mc`, `q-saa-2-1-k08-mc`, `q-tf-004-3e-mc2`  
- **Evidence:** EV-TEACHER-001, EV-TEACHER-002, EV-TEACHER-020 (contrast)  
- **Description:** Most knowledge MC items share one stem template, identical wrong-answer distractors (root user, skip teardown, budgets delete resources), and correct answer “Apply the objective directly: &lt;objective text&gt;”. The `heuristic_longest_correct` scan hit (380) is largely explained by this pattern. Rationales repeat the same four lines.  
- **Impact:** Drills measure pattern recognition, not SAA/Terraform judgment. Weak objectives (e.g. container migration SAA-2.1-K08) receive no scenario depth.  
- **Reproduction/Validation:** Grep `Which statement best reflects` under `content/questions/`; open any `-kNN-mc.json`.  
- **Recommended Improvement:** Replace template bank per objective with scenario-based stems, plausible service-specific distractors, and `citationIds` linked to lesson citations. Keep shared safety distractors only where relevant.  
- **Confidence:** High  

**Draft CR:**

- Raised by: Teacher  
- Date: 2026-09-25  
- Type: content-update  
- Where: SAA + TF primary MC files (`*-mc.json`, most `*-mc2.json`)  
- Problem: Template drill bank; 380 longest-correct heuristic hits.  
- Suggested fix: Phased rewrite by module; add generator guardrails in `scripts/gen_all_content.py`.  
- Affects learning content: yes  
- Status: open  

---

### F-03 — GL-20 step s03 contradicts lab intent

- **Severity:** Medium  
- **Category:** content-error  
- **Location:** `content/labs/gl-20.json` step `s03`  
- **Evidence:** EV-TEACHER-009, EV-TEACHER-010  
- **Description:** Step title is “Confirm AWS CLI v2” but bullet says “This lab focuses on Terraform; **Terraform is not required unless a step says so**” — copied from AWS-only labs while subsequent steps require `terraform init/plan/apply/destroy`.  
- **Impact:** Confuses learners on a capstone Terraform workflow lab.  
- **Reproduction/Validation:** Read GL-20 `s03` vs `s06`–`s13`.  
- **Recommended Improvement:** Replace bullet with “Confirm Terraform CLI (`terraform version`) meets fixture `required_version`.”  
- **Confidence:** High  

**Draft CR:** content-error, `gl-20.json` s03, open.

---

### F-04 — GL-21 title promises HCP; lab content is AWS ElastiCache only

- **Severity:** Medium  
- **Category:** content-error / objective mapping  
- **Location:** `content/labs/gl-21.json` title vs body; `lesson-tf-g8.json` maps `tf.004.8a–d` + `gl-21`  
- **Evidence:** EV-TEACHER-011, EV-TEACHER-020  
- **Description:** Title: “ElastiCache then **HCP as allowed**”. Steps and body cover Redis ElastiCache create/delete only. No HCP Terraform workspace steps. Lesson T4 and `q-tf-004-8-extra-*` drills cover HCP conceptually elsewhere.  
- **Impact:** Objective `tf.004.8a–d` hands-on path is unclear; title over-promises.  
- **Reproduction/Validation:** Search `gl-21.json` for HCP/terraform cloud steps (none).  
- **Recommended Improvement:** Either rename lab to ElastiCache-only and retarget lesson link, or add optional HCP no-charge module aligned with `q-tf-004-8-extra-00` rules.  
- **Confidence:** High  

**Draft CR:** content-error, GL-21 + lesson-tf-g8 linkage, open.

---

### F-05 — Unguided labs lack `beforeYouStart` preflight

- **Severity:** Medium  
- **Category:** content-gap (safety UX)  
- **Location:** `content/labs/ul-01.json` … `ul-21.json`  
- **Evidence:** EV-TEACHER-001, EV-TEACHER-012  
- **Description:** Content scan flags 21× `missing_beforeYouStart`. All guided labs include profile/region/STS/cost preflight. Unguided labs jump to scenario/criteria with no mirrored preflight block.  
- **Impact:** UL learners may skip profile, region, or cost acknowledgment before live AWS work (especially hourly UL-06–09, 14, 18–21).  
- **Reproduction/Validation:** Compare `gl-06` vs `ul-06` JSON top matter.  
- **Recommended Improvement:** Duplicate GL preflight strings on each UL or inherit from paired GL via UI; at minimum add `beforeYouStart` to UL JSON.  
- **Confidence:** High  

**Draft CR:** content-update, all `ul-*.json`, open.

---

### F-06 — Lessons omit links to design exercises and most labs

- **Severity:** Medium  
- **Category:** content-navigation  
- **Location:** SAA lessons `lesson-1-1` … `lesson-4-4` (`labIds`: [], `exerciseIds`: [])  
- **Evidence:** EV-TEACHER-014  
- **Description:** Lesson bodies tell learners to “complete the mapped guided/unguided lab or design exercise” but JSON arrays are empty. Sixty design exercises exist; labs are reachable from Labs tab only.  
- **Impact:** Coverage/lesson flow does not connect reading → practice artifacts; learners must discover labs/exercises indirectly.  
- **Reproduction/Validation:** Inspect lesson JSON arrays vs `content/exercises/` and lab objective maps.  
- **Recommended Improvement:** Populate `labIds` / `exerciseIds` from coverage registry; or soften lesson copy if intentional.  
- **Confidence:** High  

**Draft CR:** content-update, lesson JSON + coverage mapping, open.

---

### F-07 — Wrong citation URL reused for unrelated SAA bullets

- **Severity:** Low  
- **Category:** content-error  
- **Location:** SAA lesson bodies, e.g. `lesson-1-1.json` SAA-1.1-K03 (Regions/AZ)  
- **Evidence:** EV-TEACHER-015  
- **Description:** Multiple knowledge bullets cite the IAM introduction URL regardless of topic (global infrastructure, shared responsibility, etc.).  
- **Impact:** Misleading study pointers; undermines “cite official docs” exercise constraints.  
- **Reproduction/Validation:** Read any SAA lesson Knowledge section tradeoff lines.  
- **Recommended Improvement:** Map each bullet to a primary AWS doc (EC2 global infra, Well-Architected, etc.); update `cite-*` files.  
- **Confidence:** High  

**Draft CR:** content-update, `content/lessons/` + `content/citations/`, open.

---

## Probable Concerns

### P-01 — MR drill bank is generic and mostly absent from lesson `drillIds`

- **Severity:** Medium  
- **Category:** content-quality  
- **Location:** ~150+ `*-mr.json` files; lessons include at most one MR (Terraform groups only)  
- **Evidence:** EV-TEACHER-021  
- **Description:** Many MR items reuse “Design against the stated requirement / Validate with official documentation” as correct pair, with the same safety wrong answers. SAA lessons list MC drills only—MR variants exist in the bank but are not lesson-linked.  
- **Impact:** Weaker multi-select practice; uneven lesson vs Exam drills tab experience.  
- **Reproduction/Validation:** Sample `q-saa-1-1-k01-mr.json`; compare lesson `drillIds` length to question count per objective.  
- **Recommended Improvement:** Objective-specific MR scenarios; add second MR to lesson drill lists where objectives warrant.  
- **Confidence:** Medium-High  

---

### P-02 — Labs depend on learner-authored sidecar files without templates

- **Severity:** Medium  
- **Category:** lab-usability  
- **Location:** GL-01,02,03,09–12,16,18,19 ( `file://` references); e.g. GL-10 `gl10-trust.json`, `gl10-queue-policy.json`, `function.zip`  
- **Evidence:** EV-TEACHER-013  
- **Description:** Steps say “Save … json” but repo provides no `lab-fixtures` or `content/labs/assets/` templates. GL-02/03 describe policy content inline (better). GL-10 Lambda/SQS policy path is high-friction.  
- **Impact:** Advanced labs stall on JSON authoring errors; uneven compared to GL-06 style (commands only).  
- **Reproduction/Validation:** Glob repo for `gl10*` (none).  
- **Recommended Improvement:** Add minimal committed templates under `lab-fixtures/` or inline heredoc instructions per GL-01 pattern.  
- **Confidence:** Medium  

---

### P-03 — Shared s12–s15 lab step boilerplate

- **Severity:** Low  
- **Category:** content-quality  
- **Location:** All guided labs  
- **Evidence:** EV-TEACHER-007, EV-TEACHER-008  
- **Description:** Cost checkpoint / order deletes / bill later steps repeat with only minor edits. Some mention EC2 “stopping” on non-EC2 labs.  
- **Impact:** Noise; minor confusion (ElastiCache lab mentions “stopping an instance”).  
- **Recommended Improvement:** Tailor checkpoint bullets to service billing model.  
- **Confidence:** Medium  

---

### P-04 — Design exercise scenarios are templated

- **Severity:** Low  
- **Category:** content-quality  
- **Location:** e.g. `de-multi-account.json`, `de-federation.json`  
- **Evidence:** EV-TEACHER-022  
- **Description:** Scenarios follow “You must design a solution addressing: &lt;title&gt;” with standard rubric—acceptable for design-only bullets but low engagement.  
- **Impact:** Meets coverage; limited realism vs exam case studies.  
- **Recommended Improvement:** Add 1–2 paragraph stakeholder constraints per exercise.  
- **Confidence:** Medium  

---

## Items Requiring Verification

| ID | Item | Why verification needed | Suggested check |
| --- | --- | --- | --- |
| V-01 | End-to-end runnable all 21 GL labs | AWS Architect paper review: GL-05/08/17 blockers (AWS-001–003); not all GL verified live | Live spot-runs after JSON fixes; see `03-senior-aws-solutions-architect.md` |
| V-02 | UL acceptance criteria vs GL prerequisites | UL-01 references GL-03 bucket and GL-01 budget | **Partially confirmed** — Student STUDENT-001 (GL-03 not in lessons); trace remaining UL deps |
| V-03 | UI lesson drill resolution for dotted IDs | Backend may normalize IDs | Exam drills tab from lesson view for `lesson-3-2` |
| V-04 | `q-a0-mc-001` / MR in coverage | A0 drills lack `mcpStatus` field | Confirm intentional; align with lint schema |
| V-05 | Budget distractor nuance | AWS Budgets *can* attach IAM deny actions (optional) | Ensure rewritten drills distinguish “default alert” vs “configured action” |
| V-06 | GL-21 default VPC ElastiCache | Uses default VPC subnets | Confirm account default VPC exists (legacy accounts) |

---

## Subjective Observations

- **Terraform track:** Terraform lesson files (`lesson-tf-g1`–`g8`) are concise and on-message; GL-20 fixture aligns with provider docs for public access block (EV-TEACHER-018). `-refresh-only` after OOB tag change matches HashiCorp CLI semantics (EV-TEACHER-019).  
- **Lab rewrite quality:** GL-06 and GL-02 teardown show meaningful CR-0005 improvement (EV-TEACHER-007, EV-TEACHER-008). Placeholder scan PASS (EV-TEACHER-006) supports “no generic Step N titles” at scale.  
- **Safety voice:** A0 lesson, lab preambles, and shared distractors consistently reinforce root/MFA/teardown/budget-warning semantics—aligned with intended design.  
- **Exam realism gap:** The workbook covers objective IDs well, but the MC bank will not prepare learners for scenario-heavy SAA item styles until F-02 is addressed.  
- **Citation hygiene:** `pending_recheck` on 427 question/citation records (EV-TEACHER-001) blocks claiming MCP-verified accuracy for the full bank; spot checks support Budgets and Terraform fixture only.

---

## Strengths

1. **Structural completeness:** 189 SAA tracking IDs + Terraform 004 objectives represented across lessons, labs, exercises, and drills (inventory PASS, EV-TEACHER-005).  
2. **Safety-first lab framing:** Guided labs embed cost acceptance, tagging, ordered teardown, and “budgets warn only” messaging (EV-TEACHER-007, EV-TEACHER-016, EV-TEACHER-017).  
3. **CR-0005 lab engineering:** Runnable CLI sequences replace outline placeholders; versioned S3 teardown and NAT/VPC labs are exam-relevant (EV-TEACHER-006, EV-TEACHER-007, EV-TEACHER-008).  
4. **Unguided lab maturity:** UL-01 shows real IAM scenario/criteria/teardown vs early CR-0004 placeholders (EV-TEACHER-012 sample).  
5. **HCP policy clarity:** Extra TF drills (`q-tf-004-8-extra-00`) state no-charge HCP rule explicitly (EV-TEACHER-020).  
6. **Tooling:** Content lint and lab placeholder scan provide regression gates for future Teacher reviews (EV-TEACHER-005, EV-TEACHER-006).  
7. **GL-20 Terraform lab:** Covers init/fmt/validate/plan/apply/state/refresh-only/destroy with variableized bucket suffix (EV-TEACHER-009)— suitable capstone for T3.

---

## Summary verdict

| Dimension | Rating | Notes |
| --- | --- | --- |
| Curriculum coverage | Strong | Breadth matches plan |
| Lab runnable content (post CR-0005) | Improved; verify live | Scan PASS; spot checks good |
| Exam drill pedagogy | Weak | Template bank F-02 |
| Lesson ↔ drill linkage | Broken on 20 lessons | F-01 |
| MCP / citation freshness | Not complete | pending_recheck dominant |
| Teacher CR-0005 validation | **Concerns** | Fix major lab defects; residual F-03–F-07 |

**Recommended next actions for Lead Developer (plans required):** (1) F-01 drill ID sweep, (2) UL preflight F-05, (3) GL-20/21 lab text fixes F-03/F-04, (4) phased drill rewrite F-02, (5) lesson–exercise–lab linking F-06.

*Teacher did not write `docs/change-requests.md` per evaluation charter; draft CR blocks above are for Lead Dev transcription.*

## Post-discussion status

| Finding | Final status | XF cluster |
|---------|--------------|------------|
| F-01 | Confirmed High | XF-010 |
| F-02 | Confirmed High | XF-003 |
| F-03 | Confirmed Medium | — |
| F-04 | Confirmed Medium | — |
| F-05 | Confirmed Medium | — |
| F-06 | Confirmed Medium | — |
| F-07 | Confirmed Low | — |
| P-01–P-04 | Likely Low–Medium | — |
| V-01 (CR-0005 live) | Needs Verification | XF-005 |
