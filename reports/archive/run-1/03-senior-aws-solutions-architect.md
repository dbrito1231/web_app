# Senior AWS Solutions Architect Evaluation

**Role:** Agent 3 — Senior AWS Solutions Architect  
**Repository:** `C:\Users\dbadmin\Desktop\GitServ\ccna\web_app`  
**Date:** 2026-09-25  
**Evidence log:** `reports/evidence/AWS/evidence-log.md`

## Evaluation Scope

| Area | Scope |
|---|---|
| Labs | All **42** (`gl-01`–`gl-21`, `ul-01`–`ul-21`); CLI from `reports/evidence/lab-commands.md` (316 rows, guided labs) plus per-lab JSON teardown |
| SAA lessons | **16** exam-path lessons: `a0-lab-safety`, `lesson-1-1` … `lesson-4-4` (full read) |
| Sampled questions | **429** IDs in `reports/evidence/sample.md`; AWS accuracy spot-check on template-heavy SAA MC items (e.g. `q-saa-1-3-s02-mc`, `q-saa-2-1-k09-mc`) and objective-linked labs |
| CR-0005 | Verified claimed fixes: GL-02 LocationConstraint, UL-02 Macie teardown, `scan_lab_placeholders.py` PASS |
| Out of scope | Terraform Associate lesson accuracy (Teacher primary); live AWS execution |

## Executive Summary

Post–CR-0005, guided labs are **materially more runnable** than the pre-rewrite baseline: real `aws` commands replace placeholders, GL-02 S3 region guidance is correct, and UL-02 Macie teardown uses `update-macie-session --status PAUSED`. **`scan_lab_placeholders.py` PASS (41 labs, gl-01 excluded) confirms absence of placeholder patterns but does not enforce teardown variable symmetry** — a deeper scan still shows unguided teardown scripts and copy-paste VPC meg-scripts referencing variables learners never set in JSON.

**Confirmed high-impact lab defects:** GL-08 ships PowerShell-flavored user data on an Amazon Linux 2023 AMI (ALB health check fails); GL-05 NACL rule semantics deny all ingress rather than restricting SSH; GL-17 omits the Athena DDL needed for the stated SELECT.

**Cost/safety posture:** Sixteen labs flag `hourly: true` with UI cost-risk gates on guided hourly labs — appropriate. Forgotten-24h estimates for NAT/ALB/RDS/EKS paths are directionally plausible but not pricing-validated here.

Counts: **5 Confirmed** issues, **4 Likely**, **3 Needs Verification**, **2 Informational** strengths/observations.

## CR-0005 verification

| Claim | Verdict | Evidence |
|---|---|---|
| GL-02: remove invalid `LocationConstraint=us-east-1`; use expandable `$CreatedAt` tags | **Fixed / correct** | `content/labs/gl-02.json` s06 + bullet L75; MCP EV-AWS-050 |
| UL-02: Macie teardown uses `update-macie-session --status PAUSED` not `disable-macie` | **Fixed / correct** | `ul-02.json` teardown L66; MCP EV-AWS-054 |
| Teardown variable symmetry via `scan_lab_placeholders.py` PASS | **Partially verified** | EV-AWS-043 PASS; EV-AWS-044 shows var check is no-op (`pass`). Extended scan: 16 labs with teardown vars not declared in steps (unguided + meg-scripts) |
| Runnable commands end-to-end | **Improved, not universal** | GL-17 DDL gap; GL-08 user data; GL-19 subnetIds format |

## Strengths

- **Lab safety framing:** Consistent preflight (`sts get-caller-identity`, non-root), cost checkpoints, and `resourcegroupstaggingapi` verification by `LabId`.
- **GL-02 / GL-03 S3 + IAM patterns:** Private bucket, block public access, TLS policy, and assume-role read/write denial lab align with SAA 1.3 skills.
- **Hourly lab gating:** Guided labs gl-06–09, gl-14, gl-18–19, gl-21 require explicit UI cost-risk acceptance before create steps.
- **CR-0005 placeholder purge:** No `{{Key=` tag syntax or literal `` `aws ...` `` ellipses in scanned labs (EV-AWS-043).

## Confirmed Issues

### AWS-001

**Severity:** High  
**Category:** lab-command  
**Location:** `content/labs/gl-08.json` step s08  
**Evidence:** EV-AWS-008, EV-AWS-052  
**Description:** `run-instances` passes `--user-data "<powershell>python -m http.server 80</powershell>"` while the AMI is Amazon Linux 2023 (`al2023-ami-kernel-default-x86_64`). Amazon Linux expects cloud-init/bash user data, not a PowerShell wrapper.  
**Impact:** Instance bootstrapping does not start HTTP on port 80; ALB target stays unhealthy; learner cannot complete validation; hourly ALB/EC2 charges accrue while debugging.  
**Reproduction / Validation:** Compare step s08 user-data with [EC2 user data for Linux](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/user-data.html) (MCP EV-AWS-052). No AWS CLI run.  
**Recommended Improvement:** Replace user data with bash cloud-init, e.g. `#!/bin/bash` + `python3 -m http.server 80` or `yum install -y python3` as needed.  
**Confidence:** Confirmed  
**Related:** GL-08 pair ul-08

---

### AWS-002

**Severity:** High  
**Category:** lab-command  
**Location:** `content/labs/gl-05.json` step s10  
**Evidence:** EV-AWS-005, EV-AWS-051  
**Description:** NACL ingress rule uses `--protocol -1` (all protocols) with `--rule-action deny` and CIDR `0.0.0.0/0`. AWS documents that protocol `-1` applies to all ports regardless of `--port-range`; the lab text implies denying SSH (port 22) only.  
**Impact:** Private subnet NACL blocks all ingress, breaking the intended VPC exercise and teaching incorrect NACL semantics for SAA networking.  
**Reproduction / Validation:** [CreateNetworkAclEntry](https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_CreateNetworkAclEntry.html) Protocol parameter (MCP EV-AWS-051).  
**Recommended Improvement:** Use `--protocol tcp --port-range From=22,To=22` (and matching egress/ephemeral rules as needed for stateless NACL education).  
**Confidence:** Confirmed  
**Related:** ul-05 teardown copies VPC pattern (AWS-010)

---

### AWS-003

**Severity:** High  
**Category:** lab-sequence  
**Location:** `content/labs/gl-17.json` steps s07–s08  
**Evidence:** EV-AWS-017  
**Description:** Step s07 instructs "Run DDL for external table" without a complete CLI/query string; s08 runs `SELECT * FROM gl17.sample` against database `gl17`. No prior step creates table `sample`.  
**Impact:** Learner cannot pass validation; Athena lab objectives (SAA 3.5) not practised.  
**Reproduction / Validation:** Read JSON steps; no Glue/Athena create-table command present.  
**Recommended Improvement:** Add full `CREATE EXTERNAL TABLE gl17.sample (...)` DDL (CLI or saved `.sql`) referencing `s3://$Bucket/data/`.  
**Confidence:** Confirmed  
**Related:** ul-17

---

### AWS-004

**Severity:** Medium  
**Category:** content-accuracy  
**Location:** `content/labs/gl-07.json` title/body; `content/labs/ul-07.json` acceptance criteria  
**Evidence:** EV-AWS-007, EV-AWS-028  
**Description:** GL-07 is titled "EC2, EBS, and **EFS**" but steps cover only EC2, attach gp3 volume, and snapshot. UL-07 requires creating/mounting/deleting EFS.  
**Impact:** Guided lab does not prepare learners for unguided EFS requirements; objective gap for SAA storage architecture.  
**Reproduction / Validation:** Grep `gl-07.json` for EFS APIs — none. UL-07 criteria lines 18–25 require EFS.  
**Recommended Improvement:** Either add a minimal EFS create/mount/delete segment to GL-07 or retitle GL-07 and map EFS only to UL-07 with a prerequisite note.  
**Confidence:** Confirmed  
**Related:** ul-07

---

### AWS-005

**Severity:** Medium  
**Category:** lab-sequence  
**Location:** `scripts/scan_lab_placeholders.py`; multiple lab teardown blocks  
**Evidence:** EV-AWS-043, EV-AWS-044, EV-AWS-026–029  
**Description:** CR-0005 cites `scan_lab_placeholders.py` PASS as teardown hygiene signal, but the script's teardown variable symmetry check is explicitly disabled (`pass` at L66). Unguided labs (e.g. ul-05, ul-06, ul-08) and guided meg-teardowns (gl-06, gl-08) reference `$VpcId`, `$EndpointId`, `$AlbArn`, etc., without declaring them in JSON steps — relying on `if ($Var)` or learner notes.  
**Impact:** Stop-charges panel may no-op or fail silently; leftover ENIs/VPC/NAT/ALB continue billing — contradicts CR-0005 "end-to-end teardown" goal.  
**Reproduction / Validation:** Run extended var scan (`reports/evidence/AWS/_var_scan.py` output); compare with scan script L54–66.  
**Recommended Improvement:** Enable strict var symmetry for guided labs; for unguided labs, seed teardown with account-derived lookups or document required `$env:` replay commands. Trim gl-06/gl-08 teardown to resources each lab creates.  
**Confidence:** Confirmed  
**Related:** CR-0005 acceptance criteria

---

## Probable Concerns

### AWS-006

**Severity:** Medium  
**Category:** lab-command  
**Location:** `content/labs/gl-19.json` step s07; `ul-19.json` teardown  
**Evidence:** EV-AWS-019, EV-AWS-053  
**Description:** `eks create-cluster` uses `--resources-vpc-config subnetIds=$Subnets` where `$Subnets` comes from `--query "Subnets[0:2].SubnetId" --output text` (space-separated). AWS CLI examples use comma-separated subnet IDs in one parameter value.  
**Impact:** Cluster create may fail or parse only one subnet; EKS control plane hourly charges if partial create succeeds.  
**Reproduction / Validation:** [EKS create-cluster CLI example](https://docs.aws.amazon.com/cli/latest/userguide/cli_eks_code_examples.html) (MCP EV-AWS-053).  
**Recommended Improvement:** Set `$SubnetList = (subnets -join ',')` or use JSON `--cli-input-json`.  
**Confidence:** Likely  
**Related:** ul-19

---

### AWS-007

**Severity:** Medium  
**Category:** lab-command  
**Location:** `content/labs/gl-18.json` step s08  
**Evidence:** EV-AWS-018  
**Description:** Fargate `run-task` uses inline `network-configuration awsvpcConfiguration={subnets=[$SubnetId],assignPublicIp=ENABLED}` which is brittle in PowerShell AWS CLI v2 parsing.  
**Impact:** Task run fails until learner reformats to JSON or quoted shorthand.  
**Reproduction / Validation:** Code read; ECS CLI typically expects structured JSON for networkConfiguration on Windows.  
**Recommended Improvement:** Provide `file://network.json` or documented PowerShell-escaped JSON.  
**Confidence:** Likely  
**Related:** ul-18

---

### AWS-008

**Severity:** Low  
**Category:** lab-command  
**Location:** `content/labs/gl-07.json` step s08  
**Evidence:** EV-AWS-007  
**Description:** EBS volume created in fixed `us-east-1a` while instance AZ comes from default VPC subnet (may be `1b`, `1c`, …). Step mentions correction but default command fails first.  
**Impact:** Friction and failed attach for learners who skip the conditional bullet.  
**Recommended Improvement:** Create volume in `$Az` after instance launch.  
**Confidence:** Likely  
**Related:** —

---

### AWS-009

**Severity:** Low  
**Category:** consistency  
**Location:** `content/labs/ul-05.json` teardown verification  
**Evidence:** EV-AWS-056  
**Description:** Verification includes `LabId,Values=gl-05` instead of `ul-05`.  
**Impact:** False confidence if learner only checks wrong tag filter.  
**Recommended Improvement:** Change verification to `ul-05`.  
**Confidence:** Likely  
**Related:** ul-05

---

## Recommendations (non-defect)

### AWS-010

**Severity:** Informational  
**Category:** lab-cost  
**Location:** Hourly labs per `reports/evidence/inventory.md`  
**Evidence:** EV-AWS-006, EV-AWS-008, EV-AWS-014, EV-AWS-021  
**Description:** Forgotten-24h estimates (e.g. gl-08 `$0.96`, gl-06 NAT path) are reasonable order-of-magnitude but were not reconciled to current us-east-1 list prices.  
**Impact:** Learners may under/over-plan budget; not a correctness bug.  
**Recommended Improvement:** Add footnote linking AWS Pricing Calculator assumptions (ALB LCU hours, NAT hourly, RDS micro).  
**Confidence:** Needs Verification  
**Related:** —

---

### AWS-011

**Severity:** Informational  
**Category:** drill-key  
**Location:** Sampled SAA questions (template stems)  
**Evidence:** EV-AWS-049, `reports/evidence/content-scan.md`  
**Description:** Many SAA MC items reuse "Which statement best reflects this exam objective" with option A repeating the objective text. AWS facts in rationales (Budgets do not stop spend) are correct but exam realism is low.  
**Impact:** Weak certification transfer; not an AWS factual error.  
**Recommended Improvement:** Teacher/content pass to replace template stems with scenario-based AWS architecture questions.  
**Confidence:** Subjective Observation  
**Related:** Teacher domain

---

## Items Requiring Verification

| ID | Topic | What would settle it |
|---|---|---|
| AWS-010 | Lab cost estimates vs public pricing | Pricing Calculator or AWS Pricing API snapshot dated 2026-09-25 |
| AWS-007 | ECS run-task PowerShell quoting | Controlled CLI run in sandbox (out of eval scope) |
| AWS-006 | EKS subnetIds with space-separated `$Subnets` | Single cluster create attempt with documented variable format |

## SAA lesson notes (AWS accuracy)

Sixteen SAA lessons follow a **uniform boilerplate** ("Choose the simplest control…", KMS link repeated per bullet). Few service-specific AWS claims appear beyond generic tradeoffs and official URLs — **low risk of AWS factual error**, but **high risk of insufficient depth** for exam preparation (pedagogy: Teacher). Lesson warnings correctly state root-user avoidance and that budget alerts do not stop spend (consistent with GL-01 lab).

## Lab corpus summary

| Verdict | Guided (gl) | Unguided (ul) |
|---|---|---|
| Runnable with minor fixes | gl-01–04, gl-09–16, gl-20–21 | Most ul teardowns OK if learner tracked IDs |
| Blocking command/sequence issues | gl-05, gl-08, gl-17 | ul-07 EFS gap vs gl-07 |
| Teardown/template hygiene | gl-06, gl-08 meg-script | ul-05–09 var dependencies |

## Finding index

| ID | Severity | Confidence | Category |
|---|---|---|---|
| AWS-001 | High | Confirmed | lab-command |
| AWS-002 | High | Confirmed | lab-command |
| AWS-003 | High | Confirmed | lab-sequence |
| AWS-004 | Medium | Confirmed | content-accuracy |
| AWS-005 | Medium | Confirmed | lab-sequence |
| AWS-006 | Medium | Likely | lab-command |
| AWS-007 | Medium | Likely | lab-command |
| AWS-008 | Low | Likely | lab-command |
| AWS-009 | Low | Likely | consistency |
| AWS-010 | Informational | Needs Verification | lab-cost |
| AWS-011 | Informational | Subjective Observation | drill-key |

## Post-discussion status

| Finding | Final status | XF cluster |
|---------|--------------|------------|
| AWS-001 | Confirmed High | XF-011 |
| AWS-002 | Confirmed High | XF-011 |
| AWS-003 | Confirmed High | XF-011 |
| AWS-004 | Confirmed Medium | XF-011 |
| AWS-005 | Confirmed Medium | XF-005 |
| AWS-006–009 | Likely Low–Medium | — |
| AWS-010–011 | Needs Verification / Subjective | — |
