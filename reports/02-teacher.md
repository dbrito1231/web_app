# Agent 2 — Teacher evaluation report

**Date:** 2026-09-25  
**Role:** Teacher (read-only correctness) | **Pass:** run-2 strict  
**Scope:** `reports/evidence/intended-design.md`, `reports/evidence/sample.md` (429 questions), 23 lessons / 42 labs / 60 exercises  
**Checks (read-only):** `content_lint.py` PASS, `scan_lab_placeholders.py` PASS, full lesson/GL/exercise review, 70 TF validations, 26 Terraform doc lookups (see `reports/evidence/TEACHER/evidence-log.md`)  
**Paper-feedback mode:** Gate 0 CSRF save failure — UI scoring **Needs Verification** (`reports/evidence/gate0-save-failure.md`)  
**Terraform accuracy:** Teacher is primary owner for TF Associate 004 claims this pass (MCP + WebFetch + fixture review).

---

## Evaluation Scope

| Area | Coverage | Method |
| --- | --- | --- |
| Lessons (23) | All `content/lessons/*.json` | Objective count vs body; `drillIds` resolution (`lesson-drillids-run2.md`); TF T1–T8 sequence |
| Exam drills | 429 IDs in `sample.md` | Heuristic triage + 70 TF deep validations (TF-VALID-001–070) |
| SAA objectives | 189 bullets | `content/objectives/saa_c03.json` + `content/coverage/saa_registry.json` matrix |
| TF objectives | 37 bullets | `content/objectives/terraform_004.json` + full TF bank (119) |
| Design exercises (60) | All `content/exercises/*.json` | Rubric/scenario/constraints (EV-TEACHER-270) |
| Guided labs GL-01–21 | All 21 | Objective IDs + step review; GL-20 fixture + provider docs |
| Unguided UL-01–21 | Spot + scan flags | Preflight gap vs GL |
| Citations / MCP | Sample + TF fixture | 26 Terraform lookups logged; 427 questions `pending_recheck` |

### Coverage matrix (summary)

Registry (`saa_registry.json`) is the authoritative lesson → drill → lab → exercise map:

- **SAA 189/189** rows include `lesson_refs` and `drill_refs`; **47** include guided lab refs; **70** include design exercise refs.
- **Lesson JSON** for SAA modules often has **empty** `labIds` / `exerciseIds` while registry is populated (navigation disconnect — F-206).
- **Terraform 37/37** objectives appear in lessons T1–T8 and/or TF drills; **GL-20** covers workflow/state; **GL-21** covers cache but not HCP hands-on despite title.

Detailed evidence: EV-TEACHER-268, EV-TEACHER-224–246, EV-TEACHER-247–267.

---

## Confirmed Issues

### F-201 — Lesson drill ID dot/hyphen mismatch (13 lessons)

- **Prior:** [TEACHER F-01 (run-1)](reports/archive/run-1/02-teacher.md) — re-verified; **13** lessons with missing drill files per `lesson-drillids-run2.md` (not 20).

- **Severity:** High  
- **Category:** content-error / navigation  
- **Location:** `content/lessons/lesson-1-2.json` … `lesson-4-4.json` (13 lessons); contrast `lesson-1-1.json`, all `lesson-tf-g*.json`  
- **Evidence:** EV-TEACHER-203, EV-TEACHER-204, EV-TEACHER-226–238  
- **Description:** SAA lesson `drillIds` use dot lesson segments (`q-saa-3.2-k02-mc`); question files use hyphens (`q-saa-3-2-k02-mc`). Lesson 1-1 and Terraform lessons are hyphen-correct.  
- **Impact:** Lesson-linked drills may 404 or fail strict ID resolution; learners miss intended MC bank from lesson view.  
- **Reproduction / Validation:** Compare `lesson-3-2.json` `drillIds` to `content/questions/` filenames; run `reports/evidence/lesson-drillids-run2.md` audit.  
- **Recommended Improvement:** Bulk hyphenate `drillIds` (mirror CR-0001); add lint rule: every `drillIds` entry must exist on disk.  
- **Confidence:** Confirmed  

---

### F-202 — Template MC bank teaches test-taking heuristics, not exam skills

- **Prior:** [TEACHER F-02 (run-1)](reports/archive/run-1/02-teacher.md)

- **Severity:** High  
- **Category:** content-quality / pedagogy  
- **Location:** ~227 SAA MC + 37 TF primary `-mc` files with stem prefix `Which statement best reflects this exam objective`; e.g. `q-saa-1-1-k01-mc`, `q-tf-004-1a-mc`  
- **Evidence:** EV-TEACHER-201, EV-TEACHER-202, TF-VALID-001/004/007 pattern, EV-TEACHER-220  
- **Description:** Shared stem, “Apply the objective directly…” correct choice, and identical safety distractors; rationales repeat four lines. Scan `heuristic_longest_correct` ≈380.  
- **Impact:** Drills reward pattern recognition, not SAA/Terraform judgment; weak scenario depth on hard bullets.  
- **Reproduction / Validation:** Grep `Which statement best reflects` under `content/questions/`; open any `-kNN-mc.json`.  
- **Recommended Improvement:** Phased rewrite per module with scenario stems, plausible distractors, and citation links; generator guardrails in `scripts/gen_all_content.py`.  
- **Confidence:** Confirmed  

---

### F-203 — GL-20 step s03 contradicts lab intent

- **Prior:** [TEACHER F-03 (run-1)](reports/archive/run-1/02-teacher.md)

- **Severity:** Medium  
- **Category:** content-error  
- **Location:** `content/labs/gl-20.json` step `s03`  
- **Evidence:** EV-TEACHER-209, EV-TEACHER-210, EV-TEACHER-266  
- **Description:** Step title references AWS CLI v2 but bullet states Terraform is not required while later steps require full Terraform workflow.  
- **Impact:** Confuses learners on capstone Terraform lab.  
- **Reproduction / Validation:** Read GL-20 `s03` vs `s06`–`s13` and `lab-fixtures/gl-20/main.tf`.  
- **Recommended Improvement:** Replace bullet with Terraform CLI version check against fixture `required_version`.  
- **Confidence:** Confirmed  

---

### F-204 — GL-21 title promises HCP; lab is ElastiCache only

- **Prior:** [TEACHER F-04 (run-1)](reports/archive/run-1/02-teacher.md)

- **Severity:** Medium  
- **Category:** content-error / objective mapping  
- **Location:** `content/labs/gl-21.json`; `lesson-tf-g8.json`  
- **Evidence:** EV-TEACHER-211, EV-TEACHER-246, EV-TEACHER-267, EV-TEACHER-301  
- **Description:** Title references HCP; steps cover Redis ElastiCache create/delete only. HCP objectives taught in lessons/extras, not this lab.  
- **Impact:** Hands-on path for tf.004.8a–d unclear; title over-promises.  
- **Reproduction / Validation:** Search `gl-21.json` for HCP/Terraform Cloud workspace steps (none).  
- **Recommended Improvement:** Rename to ElastiCache-only or add optional no-charge HCP module aligned with `q-tf-004-8-extra-00`.  
- **Confidence:** Confirmed  

---

### F-205 — Unguided labs lack `beforeYouStart` preflight

- **Prior:** [TEACHER F-05 (run-1)](reports/archive/run-1/02-teacher.md)

- **Severity:** Medium  
- **Category:** content-gap (safety UX)  
- **Location:** `content/labs/ul-01.json` … `ul-21.json`  
- **Evidence:** EV-TEACHER-201, EV-TEACHER-212  
- **Description:** Content scan: 21× `missing_beforeYouStart`. Guided labs include profile/region/cost preflight.  
- **Impact:** UL learners may skip cost/profile acknowledgment before hourly AWS work.  
- **Reproduction / Validation:** Compare `gl-06.json` vs `ul-06.json` top matter.  
- **Recommended Improvement:** Add `beforeYouStart` to each UL or inherit from paired GL in UI.  
- **Confidence:** Confirmed  

---

### F-206 — Lessons omit links to design exercises and most labs

- **Prior:** [TEACHER F-06 (run-1)](reports/archive/run-1/02-teacher.md)

- **Severity:** Medium  
- **Category:** content-navigation  
- **Location:** SAA lessons `lesson-1-1` … `lesson-4-4`  
- **Evidence:** EV-TEACHER-214, EV-TEACHER-268, EV-TEACHER-225  
- **Description:** Lesson copy references mapped labs/exercises but JSON `labIds` / `exerciseIds` empty while registry lists refs.  
- **Impact:** Coverage flow does not connect reading → practice from lesson tab.  
- **Reproduction / Validation:** Inspect lesson JSON vs `saa_registry.json` row for SAA-1.1-K01.  
- **Recommended Improvement:** Populate arrays from registry or soften lesson copy.  
- **Confidence:** Confirmed  

---

### F-207 — Wrong citation URL reused for unrelated SAA bullets

- **Prior:** [TEACHER F-07 (run-1)](reports/archive/run-1/02-teacher.md)

- **Severity:** Low  
- **Category:** content-error  
- **Location:** SAA lesson bodies, e.g. `lesson-1-1.json` SAA-1.1-K03  
- **Evidence:** EV-TEACHER-215  
- **Description:** IAM intro URL repeated on non-IAM bullets (Regions/AZ, shared responsibility, etc.).  
- **Impact:** Misleading study pointers.  
- **Reproduction / Validation:** Read Knowledge section tradeoff lines in any SAA lesson.  
- **Recommended Improvement:** Per-bullet primary AWS doc URLs; update `cite-*` files.  
- **Confidence:** Confirmed  

---

## Probable Concerns

### TEACHER-208 — MR drill bank generic and under-linked in lessons

- **Severity:** Medium  
- **Category:** content-quality  
- **Location:** ~150+ `*-mr.json`; SAA lesson `drillIds` mostly MC-only  
- **Evidence:** EV-TEACHER-221  
- **Description:** MR items reuse generic “Design against requirement / Validate with docs” pairs; MR exists in bank but rarely in lesson lists.  
- **Impact:** Weaker multi-select practice from lesson path.  
- **Reproduction / Validation:** Open `q-saa-1-1-k01-mr.json`; compare lesson `drillIds` to available `-mr` files per objective.  
- **Recommended Improvement:** Objective-specific MR scenarios; add MR to lesson drill lists where warranted.  
- **Confidence:** Likely  

---

### TEACHER-209 — Labs depend on learner-authored sidecar files without templates

- **Severity:** Medium  
- **Category:** lab-usability  
- **Location:** GL-10 and others with `file://` references  
- **Evidence:** EV-TEACHER-213, EV-TEACHER-256  
- **Description:** Steps reference local JSON/zip not committed under `lab-fixtures/` or `content/labs/assets/`.  
- **Impact:** Advanced labs stall on authoring errors.  
- **Reproduction / Validation:** Glob repo for `gl10-trust.json` (none).  
- **Recommended Improvement:** Commit minimal templates or inline heredocs per GL-01 pattern.  
- **Confidence:** Likely  

---

### TEACHER-210 — Shared s12–s15 lab step boilerplate

- **Severity:** Low  
- **Category:** content-quality  
- **Location:** All guided labs  
- **Evidence:** EV-TEACHER-207, EV-TEACHER-208  
- **Description:** Cost/teardown checkpoints repeat; occasional wrong service wording (e.g. “stop instance” on non-EC2 labs).  
- **Impact:** Noise; minor confusion.  
- **Reproduction / Validation:** Diff GL-21 vs GL-07 checkpoint bullets.  
- **Recommended Improvement:** Tailor checkpoint text to service billing model.  
- **Confidence:** Likely  

---

### TEACHER-211 — Design exercise scenarios are templated

- **Severity:** Low  
- **Category:** content-quality  
- **Location:** All 60 `de-*.json`  
- **Evidence:** EV-TEACHER-222, EV-TEACHER-270  
- **Description:** “You must design a solution addressing: &lt;title&gt;” pattern; rubrics adequate, engagement low.  
- **Impact:** Coverage met; limited exam case-study realism.  
- **Reproduction / Validation:** Open `de-multi-account.json`.  
- **Recommended Improvement:** Add stakeholder constraints per exercise.  
- **Confidence:** Subjective Observation  

---

## Items Requiring Verification

### TEACHER-212 — Live UI drill/lab scoring (Gate 0)

- **Severity:** High  
- **Category:** app-integration / grading  
- **Location:** Exam tab `q-a0-mc-001`; Labs GL-01 checkpoint  
- **Evidence:** EV-TEACHER-271, `reports/evidence/gate0-save-failure.md`  
- **Description:** POST `/api/attempts` and lab checkpoints return 403 CSRF; UI shows `Forbidden`. Paper-feedback mode: keys graded from JSON only.  
- **Impact:** Cannot confirm end-user feedback, progress persistence, or rationale display this pass.  
- **Reproduction / Validation:** Re-run Gate 0 after `CSRF_TRUSTED_ORIGINS` fix; click Check answers and GL checkpoint.  
- **Recommended Improvement:** Lead Dev fix (FULLSTACK/PYTHON CRs); Teacher re-validates scoring copy after green Gate 0.  
- **Confidence:** Needs Verification  

---

### TEACHER-213 — End-to-end runnable all 21 GL labs

- **Severity:** Medium  
- **Category:** lab-runnable  
- **Location:** GL-05, GL-08, GL-17 (among others)  
- **Evidence:** EV-TEACHER-251, EV-TEACHER-254, EV-TEACHER-263; AWS agent paper review  
- **Description:** Placeholder scan PASS but AWS Solutions Architect flagged blockers on subset.  
- **Impact:** Live lab success uncertain for full GL catalog.  
- **Reproduction / Validation:** Live spot-runs after JSON fixes.  
- **Recommended Improvement:** Close AWS-201–003 class issues; Teacher spot-check teardown.  
- **Confidence:** Needs Verification  

---

### TEACHER-214 — Backend drill ID normalization

- **Severity:** Medium  
- **Category:** app-behavior  
- **Location:** Lesson drill resolution API  
- **Evidence:** EV-TEACHER-203, EV-TEACHER-226  
- **Description:** If API normalizes dots→hyphens, lesson view might work while strict file audit still fails.  
- **Impact:** F-201 severity for learners depends on UI path.  
- **Reproduction / Validation:** Open lesson 3-2 in UI with Gate 0 fixed; trace API question fetch.  
- **Recommended Improvement:** Fix content regardless; add integration test for lesson drillIds.  
- **Confidence:** Needs Verification  

---

### TEACHER-215 — Budget distractor nuance in rewrites

- **Severity:** Low  
- **Category:** content-accuracy  
- **Location:** Template distractor D across MC bank  
- **Evidence:** EV-TEACHER-216, EV-TEACHER-217  
- **Description:** Optional Budget *actions* can attach IAM denies; default remains alert-only.  
- **Impact:** Future rewrites must not over-correct to “always false.”  
- **Reproduction / Validation:** AWS Budgets managing costs doc via MCP.  
- **Recommended Improvement:** Rewrite distractor to “default alert does not delete resources.”  
- **Confidence:** Likely  

---

## Subjective Observations

- **Terraform track:** Fixture GL-20 matches provider docs for split S3 public access block (EV-TEACHER-300, EV-TEACHER-218). CLI `-refresh-only` semantics align with lab OOB tag exercise (EV-TEACHER-306, EV-TEACHER-219). Teacher owns TF accuracy until MCP recheck clears `pending_recheck`.  
- **TF drills:** Objective mapping is correct on all 70 sampled TF items; primary `-mc` stems suffer same template issue as SAA (37/119 template-class); `mc2`, `mr`, and `8-extra-*` items are stronger (EV-TEACHER-220, TF-VALID table).  
- **CR-0005 labs:** GL-06/GL-02 show meaningful runnable improvement (EV-TEACHER-207, EV-TEACHER-208); placeholder scan PASS supports scale quality.  
- **Exam realism:** Objective ID coverage is strong; scenario-heavy SAA item styles still blocked on F-202.  
- **Round A alignment:** Drill IDs (13 lessons), template MC, GL-20/21 text, and Gate 0 paper mode consistent with `reports/discussion/round-a/TEACHER.md`.

---

## Strengths

1. **Structural completeness:** 189 SAA + 37 TF objectives represented across lessons, labs, exercises, drills (EV-TEACHER-205, EV-TEACHER-268).  
2. **Safety-first framing:** A0, GL preambles, shared distractors reinforce MFA/teardown/budget-warning (EV-TEACHER-216, EV-TEACHER-217).  
3. **GL-20 capstone:** End-to-end Terraform workflow with variableized bucket and state refresh drill (EV-TEACHER-209, EV-TEACHER-323).  
4. **Exercise rubrics:** 60/60 design exercises include scoring rubrics (EV-TEACHER-270).  
5. **TF lesson linkage:** Terraform lessons resolve drills correctly unlike 13 SAA lessons (EV-TEACHER-239–246).  
6. **Tooling gates:** `content_lint.py` and lab placeholder scan provide regression hooks (EV-TEACHER-205, EV-TEACHER-206).  
7. **HCP policy clarity:** `q-tf-004-8-extra-00` states no-charge HCP rule (EV-TEACHER-220).

---

## Draft change requests (Teacher)

| CR draft | Type | Where | Problem | Suggested fix | Learning content |
| --- | --- | --- | --- | --- | --- |
| CR-T-201 | content-error | `lesson-1-2` … `lesson-4-4` `drillIds` | 13 lessons dot/hyphen mismatch | Hyphenate all; lint existence check | yes |
| CR-T-202 | content-update | SAA + TF `-mc` bank | Template stems / heuristic bank | Phased scenario rewrite | yes |
| CR-T-203 | content-error | `gl-20.json` s03 | Terraform disclaimer on TF lab | Terraform version bullet | yes |
| CR-T-204 | content-error | `gl-21.json`, `lesson-tf-g8` | HCP title vs ElastiCache body | Rename or add HCP optional lab | yes |
| CR-T-205 | content-update | `ul-*.json` | Missing `beforeYouStart` | Mirror GL preflight | yes |
| CR-T-206 | content-navigation | SAA lesson JSON | Empty lab/exercise arrays | Sync from `saa_registry.json` | yes |
| CR-T-207 | content-update | `content/lessons`, `cite-*` | Wrong repeated IAM URLs | Per-bullet doc map | yes |

*Teacher did not write `docs/change-requests.md`; Lead Developer records after approved plan.*

---

## Summary verdict

| Dimension | Rating | Notes |
| --- | --- | --- |
| Curriculum coverage | Strong | Registry complete |
| Lab content (post CR-0005) | Improved | Scan PASS; live GL subset unverified |
| Exam drill pedagogy | Weak | F-202 template bank |
| Lesson ↔ drill linkage | Broken on **13** SAA lessons | F-201 |
| Terraform technical accuracy | Good (spot-checked) | Fixture + 26 doc lookups; MCP recheck pending |
| UI scoring feedback | Unverified | Gate 0 paper mode |

**Recommended Lead Developer order:** F-201 → Gate 0 CSRF → F-205/F-203/F-204 → F-206 → phased F-202.

---

## Post-discussion status

| Finding ID | Final status | XF / notes |
|---|---|---|
| F-201 | Confirmed High | **13** lessons; XF-210; Round B count refined |
| F-202 | Confirmed High | Template MC bank; XF-203 |
| F-203 | Confirmed Medium | GL-20 s03 copy |
| F-204 | Confirmed Medium | GL-21 / fixture alignment |
| F-205 | Confirmed Medium | UL preflight gap |
| TEACHER-212 | Needs Verification | UI scoring blocked by Gate 0 CSRF |
