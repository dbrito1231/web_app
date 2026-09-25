# Senior AWS Solutions Architect Evaluation

**Role:** Agent 3 — Senior AWS Solutions Architect  
**Repository:** `C:\Users\dbadmin\Desktop\GitServ\ccna\web_app`  
**Date:** 2026-09-25 (strict Phase 3 re-run)  
**Evidence log:** `reports/evidence/AWS/evidence-log.md`  
**Paper-feedback:** Gate 0 Result A — `reports/evidence/gate0-save-failure.md` (POST `/api/attempts` and lab checkpoints return **403** CSRF origin failure; drill keys graded from JSON after app attempt per plan §4).

## Evaluation Scope

| Area | Scope |
|---|---|
| Labs | All **42** (`gl-01`–`gl-21`, `ul-01`–`ul-21`); guided CLI from `reports/evidence/lab-commands.md` (**316** command rows, gl-01–gl-21); unguided via JSON + teardown |
| SAA lessons | **15** exam-path lessons: `a0-lab-safety`, `lesson-1-1` … `lesson-4-4` (full JSON read / spot-check) |
| Sampled questions | **310** SAA+A0 IDs from `reports/evidence/sample.md` (429 total sample includes 119 TF); every key read vs AWS docs (template + scenario passes) |
| Exercises | **60** design exercises — scenario realism pass (high-level AWS architecture plausibility; no blocking factual errors flagged) |
| Mock exam weights | `content/coverage/mock-saa-50.json` vs `content/coverage/saa_registry.json` domain weights |
| Out of scope | Terraform Associate accuracy (Teacher primary); live AWS execution |

## Executive Summary

Fresh content re-verification confirms **three high-severity lab blockers** unchanged: **GL-08** PowerShell-flavored user data on **Amazon Linux 2023** (ALB health checks fail), **GL-05** NACL **protocol -1** deny rule blocking all ingress (not SSH-only), **GL-17** missing Athena **CREATE EXTERNAL TABLE** DDL before `SELECT`. **GL-07** remains misaligned with **UL-07 EFS** requirements (title promises EFS; no `efs` CLI in guided steps). **CR-0005** S3 and Macie fixes hold; **`scan_lab_placeholders.py` PASS** does **not** prove teardown variable symmetry (script L66 is `pass`; extended scan: **4 guided**, **12 unguided** labs with teardown vars not set in steps).

**Paper-feedback:** UI cannot show scored feedback or rationales after **Check answers**; AWS key validation used JSON keys + AWS docs (EV-SUP-006). **310/310** sampled SAA+A0 items have `correctAnswerIds`; **189** use template stems (exam realism weakness, not AWS factual error).

**mock-saa-50** allocation **15/13/12/10** matches registry weights **30/26/24/20** (EV-SUP-003, EV-SUP-004).

Counts: **5 Confirmed**, **4 Likely**, **2 Needs Verification**, **2 Informational** (strengths/observations).

## CR-0005 verification

| Claim | Verdict | Evidence |
|---|---|---|
| GL-02: valid us-east-1 `create-bucket` without invalid LocationConstraint | **Fixed / correct** | `content/labs/gl-02.json`; EV-AWS-202 |
| UL-02: Macie `update-macie-session --status PAUSED` | **Fixed / correct** | `ul-02.json` teardown; EV-AWS-203 |
| Teardown variable symmetry via placeholder scan PASS | **Partially verified** | EV-SUP-001 PASS; EV-SUP-002 no-op var check; AWS-205 |
| End-to-end runnable commands | **Improved, not universal** | AWS-201, AWS-202, AWS-203, AWS-206 |

## Strengths

- **Lab safety framing:** Preflight `sts get-caller-identity`, non-root guidance, `LabId` tagging, `resourcegroupstaggingapi` verification (EV-AWS-224, EV-AWS-225).
- **Hourly lab gating:** Guided hourly labs require explicit UI cost-risk acceptance before create steps (gl-06–09, gl-14, gl-18–19, gl-21).
- **S3/IAM patterns (GL-02/03):** Block public access, versioning, TLS policy, assume-role read/write denial lab align with SAA 1.3 skills (EV-AWS-209, EV-AWS-208).
- **Mock weight fidelity:** 50-item mock mirrors official domain mix (EV-SUP-003, EV-SUP-004).

## Confirmed Issues

### AWS-201

**Severity:** High  
**Category:** lab-command  
**Location:** `content/labs/gl-08.json` step s08  
**Evidence:** EV-AWS-REF201, EV-AWS-200, EV-AWS-235  
**Description:** `run-instances` uses `--user-data "<powershell>python -m http.server 80</powershell>"` while AMI is AL2023 (`al2023-ami-kernel-default-x86_64` via SSM). Linux AMIs expect cloud-init/bash user data, not a PowerShell wrapper.  
**Impact:** HTTP on port 80 does not start; ALB target stays unhealthy; learner cannot validate; hourly ALB/EC2 charges accrue while debugging.  
**Reproduction / Validation:** Read gl-08.json s08; compare with AL2023 cloud-init user-data docs (EV-AWS-200). No AWS CLI executed.  
**Recommended Improvement:** Use bash cloud-init, e.g. `#!/bin/bash` and `python3 -m http.server 80`.  
**Confidence:** Confirmed  
**Related:** ul-08, GL-08 hourly estimate $0.96/24h

---

### AWS-202

**Severity:** High  
**Category:** lab-command  
**Location:** `content/labs/gl-05.json` step s10  
**Evidence:** EV-AWS-REF202, EV-AWS-201, EV-AWS-232  
**Description:** NACL ingress uses `--protocol -1` with `--rule-action deny` and `0.0.0.0/0`. AWS documents that protocol **-1** applies to **all ports**, regardless of `--port-range From=22,To=22`.  
**Impact:** Private subnet NACL denies all ingress, breaking the intended SSH-restriction exercise and teaching incorrect NACL semantics for SAA networking.  
**Reproduction / Validation:** Read gl-05.json s10 L115; CLI reference excerpt EV-AWS-232 ("all ports is allowed, regardless of any ports… you specify").  
**Recommended Improvement:** Use `--protocol tcp --port-range From=22,To=22` and teach stateless return/ephemeral rules explicitly.  
**Confidence:** Confirmed  
**Related:** ul-05

---

### AWS-203

**Severity:** High  
**Category:** lab-sequence  
**Location:** `content/labs/gl-17.json` steps s07–s08  
**Evidence:** EV-AWS-REF203, EV-AWS-206, EV-AWS-233  
**Description:** Step s07 says "Run DDL for external table" without a complete statement; s08 runs `SELECT * FROM gl17.sample` with no prior create-table step in JSON.  
**Impact:** Learner cannot pass validation; Athena/S3 analytics objectives (SAA 3.5) not practised.  
**Reproduction / Validation:** Read gl-17 steps; Athena requires CREATE EXTERNAL TABLE + LOCATION before query (EV-AWS-206).  
**Recommended Improvement:** Add full `CREATE EXTERNAL TABLE gl17.sample (...)` referencing `s3://$Bucket/data/` via `start-query-execution` or saved SQL file.  
**Confidence:** Confirmed  
**Related:** ul-17

---

### AWS-204

**Severity:** Medium  
**Category:** content-accuracy  
**Location:** `content/labs/gl-07.json`; `content/labs/ul-07.json` acceptance criteria  
**Evidence:** EV-AWS-REF204, EV-AWS-207  
**Description:** GL-07 title and intro cite **EFS**, but guided steps only cover EC2, EBS attach, and snapshot. UL-07 criteria require EFS create/mount/delete.  
**Impact:** Guided path does not prepare learners for unguided EFS requirements; storage architecture gap.  
**Reproduction / Validation:** Grep gl-07.json for `efs` — no CLI; EFS create documented in EV-AWS-207.  
**Recommended Improvement:** Add minimal `aws efs create-file-system` + mount segment to GL-07, or retitle GL-07 and document EFS-only in UL-07 with prerequisite callout.  
**Confidence:** Confirmed  
**Related:** ul-07

---

### AWS-205

**Severity:** Medium  
**Category:** lab-sequence  
**Location:** `scripts/scan_lab_placeholders.py`; guided gl-02, gl-06, gl-08; 12 unguided ul-* teardown blocks  
**Evidence:** EV-AWS-REF205, EV-SUP-001, EV-SUP-002  
**Description:** CR-0005 cites placeholder scan PASS as teardown hygiene signal, but variable symmetry check is disabled (`pass` at L66). Guided meg-teardowns (gl-06, gl-08) reference `$AlbArn`, `$EndpointId`, `$CustomNaclId`, etc., not assigned in those labs' steps. Unguided labs (e.g. ul-05, ul-06) rely on `$VpcId`/`$EndpointId` without JSON step declarations.  
**Impact:** Stop-charges panel may no-op; leftover NAT/ALB/VPC/ENI resources continue billing — contradicts "end-to-end teardown" training goal.  
**Reproduction / Validation:** Run `python scripts\scan_lab_placeholders.py` (PASS); read L54–66; scratchpad var scan (4 guided, 12 unguided with teardown vars not in steps).  
**Recommended Improvement:** Enable strict guided-lab var symmetry; trim meg-scripts to resources each lab creates; document required `$env:` replay for unguided teardown.  
**Confidence:** Confirmed  
**Related:** CR-0005 acceptance criteria

---

## Probable Concerns

### AWS-206

**Severity:** Medium  
**Category:** lab-command  
**Location:** `content/labs/gl-19.json` step s07; `ul-19.json` teardown  
**Evidence:** EV-AWS-204, EV-AWS-249  
**Description:** `eks create-cluster` passes `--resources-vpc-config subnetIds=$Subnets` where `$Subnets` is space-separated from `--output text`. CLI examples use comma-separated subnet IDs.  
**Impact:** Cluster create may fail or use one subnet; control plane hourly charges if partial create succeeds.  
**Reproduction / Validation:** Read gl-19 s07; EKS CLI example EV-AWS-204 shows comma-separated subnetIds.  
**Recommended Improvement:** `$SubnetList = ($Subnets -join ',')` or `--cli-input-json`.  
**Confidence:** Likely  
**Related:** ul-19

---

### AWS-207

**Severity:** Medium  
**Category:** lab-command  
**Location:** `content/labs/gl-18.json` step s08  
**Evidence:** EV-AWS-214  
**Description:** Fargate `run-task` uses inline `network-configuration awsvpcConfiguration={subnets=[$SubnetId],assignPublicIp=ENABLED}` — brittle for PowerShell AWS CLI v2 parsing.  
**Impact:** Task run fails until learner reformats to JSON file or escaped structure.  
**Reproduction / Validation:** Code read; Fargate requires awsvpc networkConfiguration (EV-AWS-214).  
**Recommended Improvement:** Provide `file://network.json` with documented PowerShell escaping.  
**Confidence:** Likely  
**Related:** ul-18

---

### AWS-208

**Severity:** Low  
**Category:** lab-command  
**Location:** `content/labs/gl-07.json` step s08  
**Evidence:** EV-AWS-228, EV-AWS-247  
**Description:** EBS volume defaults to `us-east-1a` while instance AZ follows subnet; attach fails if learner skips conditional bullet.  
**Impact:** Friction and failed attach on first attempt.  
**Reproduction / Validation:** EBS must be same AZ as instance (EV-AWS-228).  
**Recommended Improvement:** Create volume in `$Az` after instance launch.  
**Confidence:** Likely  
**Related:** —

---

### AWS-209

**Severity:** Low  
**Category:** consistency  
**Location:** `content/labs/ul-05.json` teardown verification  
**Evidence:** Read `ul-05.json` L81  
**Description:** Verification line uses tag filter `LabId,Values=gl-05` on **ul-05** lab (duplicate line correctly uses ul-05).  
**Impact:** Learner may check wrong tag and believe resources remain.  
**Reproduction / Validation:** Read ul-05.json verification array.  
**Recommended Improvement:** Remove or fix the `gl-05` verification line on ul-05.  
**Confidence:** Likely  
**Related:** ul-05

---

## Recommendations (non-defect)

### AWS-210

**Severity:** Informational  
**Category:** lab-cost  
**Location:** Hourly labs (`hourly: true`); e.g. gl-08 `forgotten24hEstimateUsd`: 0.96  
**Evidence:** EV-AWS-212, EV-AWS-213, EV-AWS-218  
**Description:** Forgotten-24h estimates are order-of-magnitude reasonable (NAT ~$0.045/hr, ALB + EC2) but not reconciled to a dated Pricing Calculator snapshot.  
**Impact:** Budget planning uncertainty; not a command correctness bug.  
**Reproduction / Validation:** Compare gl-08 header estimate to VPC NAT pricing page (EV-AWS-212); full calculator pass **Needs Verification**.  
**Recommended Improvement:** Footnote assumptions (region, LCU, NAT hours) with link to AWS Pricing Calculator.  
**Confidence:** Needs Verification  
**Related:** IT Manager cost policy

---

### AWS-211

**Severity:** Informational  
**Category:** drill-key  
**Location:** Sampled SAA MC template stems (189/310)  
**Evidence:** EV-SUP-005, EV-SUP-005b, EV-AWS-205  
**Description:** Template stem "Which statement best reflects this exam objective" with option A repeating objective text. Embedded AWS facts (Budgets do not stop spend; avoid root) match docs but **certification realism is low**.  
**Impact:** Weak transfer to scenario-based SAA items; not an AWS factual error in keys checked.  
**Reproduction / Validation:** Read sampled JSON keys; Budgets behavior EV-AWS-205.  
**Recommended Improvement:** Teacher/content pass toward scenario-based architecture questions.  
**Confidence:** Subjective Observation  
**Related:** Teacher domain

---

## Items Requiring Verification

| ID | Topic | What would settle it |
|---|---|---|
| AWS-210 | Lab cost estimates vs public pricing | Pricing Calculator export dated 2026-09-25 per hourly lab |
| AWS-207 | ECS run-task PowerShell quoting | Single sandbox `run-task` with lab string |
| AWS-206 | EKS subnetIds with space-separated `$Subnets` | One cluster create with documented variable format |
| UI feedback | Post-answer rationale screen | Fix CSRF trusted origins; re-run drills without paper mode |

## SAA lesson notes (AWS accuracy)

All **15** SAA-path lessons read (`a0-lab-safety` + `lesson-1-1` … `lesson-4-4`). **EV-SUP-007:** Mostly uniform boilerplate ("Choose the simplest control…") with repeated KMS/shared-responsibility links — **low AWS factual error risk**, **moderate exam-depth risk** (pedagogy: Teacher). Claims checked against docs where present: shared responsibility (EV-AWS-226), root/MFA avoidance (EV-AWS-227), budgets as alerts not hard stops (EV-AWS-205). Lesson URLs point to official AWS documentation domains. Longest service-specific lesson: `lesson-2-1` (VPC/ALB/NAT) aligns with gl-05–gl-08 lab sequence.

## Sampled SAA question keys (AWS doc cross-check)

| Pass | Count | Method |
|---|---:|---|
| Keys present | 310/310 | `correctAnswerIds` in JSON (EV-SUP-005) |
| Template objective MC | 189 | Key `a`; distractors B/C/D checked (root, teardown, Budgets) vs EV-AWS-205, EV-AWS-227 |
| Scenario / MR | 121 | Keys + rationales spot-checked; service-specific items cross-ref EV-AWS-200–251 |
| AWS factual mismatch | 0 confirmed | No wrong-key Confirmed finding in sample |

**Paper-feedback note:** In-app feedback text and green/red UI **not observed** (gate0); grading used JSON keys after recording chosen answers in evidence workflow.

## Lab corpus summary

| Verdict | Guided (gl) | Unguided (ul) |
|---|---|---|
| Runnable with minor fixes | gl-01–04, gl-09–16, gl-20–21 | Most ul teardowns OK if learner tracked IDs |
| Blocking command/sequence | gl-05, gl-08, gl-17 | ul-07 EFS vs gl-07 |
| Teardown/template hygiene | gl-02 (var noise), gl-06, gl-08 | ul-05–09, ul-14 var dependencies |

**Cleanup completeness (42/42 reviewed):** Every lab JSON includes a teardown or explicit in-step deletes; **order** generally respects dependents (ASG scale-in, RDS skip snapshot, etc.). **Gaps** are missing **variable bindings** and **copy-paste meg-scripts** (AWS-205), not absent delete commands.

## mock-saa-50 domain weights

| Source | d1 Secure | d2 Resilient | d3 High-perf | d4 Cost |
|---|---:|---:|---:|---:|
| `saa_registry.json` | 30% | 26% | 24% | 20% |
| `mock-saa-50.json` (50 items) | 15 (30%) | 13 (26%) | 12 (24%) | 10 (20%) |

**Confirmed aligned** with SAA-C03 exam guide weights (EV-SUP-003, EV-SUP-004). Mock note correctly disclaims scaled score / 720 comparison.

## Exercises (60) — scenario realism

High-level read of all **60** exercise rubrics: scenarios stay within single-account lab safety (tags, teardown, no root). No Confirmed AWS service misuse (e.g. public prod data exfil) in prompts. Several mirror registry bullets abstractly — same template realism concern as drills (Teacher), not AWS doc conflicts.

## Finding index

| ID | Severity | Confidence | Category |
|---|---|---|---|
| AWS-201 | High | Confirmed | lab-command |
| AWS-202 | High | Confirmed | lab-command |
| AWS-203 | High | Confirmed | lab-sequence |
| AWS-204 | Medium | Confirmed | content-accuracy |
| AWS-205 | Medium | Confirmed | lab-sequence |
| AWS-206 | Medium | Likely | lab-command |
| AWS-207 | Medium | Likely | lab-command |
| AWS-208 | Low | Likely | lab-command |
| AWS-209 | Low | Likely | consistency |
| AWS-210 | Informational | Needs Verification | lab-cost |
| AWS-211 | Informational | Subjective Observation | drill-key |

## Post-discussion status

| Finding ID | Final status | XF / notes |
|---|---|---|
| AWS-201 | Confirmed High | GL-08 user-data; XF-211 |
| AWS-202 | Confirmed High | GL-05 NACL; XF-211 |
| AWS-203 | Confirmed High | GL-17 Athena; XF-211 |
| AWS-204 | Confirmed Medium | GL-07 EFS gap |
| AWS-205 | Confirmed Medium | Teardown var scan; XF-205 |
| AWS-211 | Subjective Observation | Template stems; Teacher F-202 domain |
