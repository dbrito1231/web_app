# Teacher evidence log — run-2 strict pass (2026-09-25)

**Role:** Teacher (read-only) | **Timestamp:** 2026-09-25 run-2 strict pass | **Primary Terraform accuracy owner**

Paper-feedback mode: `reports/evidence/gate0-save-failure.md` (UI drill/lab scoring **Needs Verification**).

---

## Summary counts

| Metric | Count |
| --- | ---: |
| EV-TEACHER rows (this log) | 97 |
| TF-VALID rows (objective + rationale spot-check) | 70 |
| Terraform MCP / WebFetch doc lookups (EV-TEACHER-300–325) | 26 |
| Lessons sequence/objective reviewed | 23 |
| Guided labs (GL-01–GL-21) objective fit | 21 |
| Design exercise rubrics reviewed | 60 |

---

## Core automation and scan

| ID | Date | Source | Summary |
| --- | --- | --- | --- |
| EV-TEACHER-201 | 2026-09-25 run-2 | `reports/evidence/content-scan.json` | 721 scan findings; 380 `heuristic_longest_correct`; 21× `missing_beforeYouStart` (all UL); `mcpStatus` pending_recheck 427 / verified 0. |
| EV-TEACHER-202 | 2026-09-25 run-2 | `content/questions/q-saa-1-1-k01-mc.json` | Template MC stem + “Apply the objective directly…” correct choice; shared safety distractors. |
| EV-TEACHER-203 | 2026-09-25 run-2 | `reports/evidence/lesson-drillids-run2.md` | **13** SAA lessons with dot-segment `drillIds` vs hyphen question filenames (lesson-1-2 … lesson-4-4); a0 + lesson-1-1 + all TF lessons OK. |
| EV-TEACHER-204 | 2026-09-25 run-2 | `content/lessons/lesson-1-1.json` | Contrast: post CR-0001 hyphenated `drillIds` on lesson-1-1 only among SAA domain lessons. |
| EV-TEACHER-205 | 2026-09-25 run-2 | `python scripts/content_lint.py` | PASS — 429 questions, 42 labs, 23 lessons. |
| EV-TEACHER-206 | 2026-09-25 run-2 | `scripts/scan_lab_placeholders.py` | PASS — 41 labs scanned, no placeholder step titles. |
| EV-TEACHER-207 | 2026-09-25 run-2 | `content/labs/gl-06.json` | Runnable VPC/NAT/EIP sequence; ordered teardown present. |
| EV-TEACHER-208 | 2026-09-25 run-2 | `content/labs/gl-02.json` | Versioned S3 teardown includes delete-marker loop. |
| EV-TEACHER-209 | 2026-09-25 run-2 | `lab-fixtures/gl-20/main.tf`, GL-20 | Fixture: `aws_s3_bucket` + separate `aws_s3_bucket_public_access_block`; lab covers init/plan/apply/destroy and `-refresh-only`. |
| EV-TEACHER-210 | 2026-09-25 run-2 | `content/labs/gl-20.json` s03 | AWS-only boilerplate (“Terraform is not required…”) on Terraform-primary lab. |
| EV-TEACHER-211 | 2026-09-25 run-2 | `content/labs/gl-21.json` | Title promises HCP; steps are ElastiCache-only. |
| EV-TEACHER-212 | 2026-09-25 run-2 | `content/labs/ul-01.json` … `ul-21.json` | No `beforeYouStart` on any UL; all GL include preflight. |
| EV-TEACHER-213 | 2026-09-25 run-2 | `content/labs/gl-10.json` | `file://gl10-trust.json`, `function.zip` — no committed templates in repo. |
| EV-TEACHER-214 | 2026-09-25 run-2 | `content/lessons/lesson-1-2.json` … `lesson-4-4.json` | Empty `labIds` / `exerciseIds` despite lesson copy referencing mapped labs/exercises. |
| EV-TEACHER-215 | 2026-09-25 run-2 | `content/lessons/lesson-1-1.json` | Repeated IAM intro URL on non-IAM bullets (e.g. SAA-1.1-K03 Regions/AZ). |
| EV-TEACHER-216 | 2026-09-25 run-2 | AWS Knowledge MCP | Budgets: alerts/notifications default; optional actions — “deletes resources” distractor remains false. |
| EV-TEACHER-217 | 2026-09-25 run-2 | AWS Knowledge MCP | Budget notifications do not inherently stop spend without configured actions. |
| EV-TEACHER-218 | 2026-09-25 run-2 | Terraform MCP `SearchAwsProviderDocs` | `aws_s3_bucket_public_access_block` matches GL-20 fixture split-resource pattern. |
| EV-TEACHER-219 | 2026-09-25 run-2 | WebFetch HashiCorp CLI | `terraform plan -refresh-only` refreshes state without apply (GL-20 OOB tag step). |
| EV-TEACHER-220 | 2026-09-25 run-2 | `q-tf-004-8-extra-00-mc.json` | HCP extra drill: scenario-specific stem (contrast to template bank). |
| EV-TEACHER-221 | 2026-09-25 run-2 | `q-saa-1-1-k01-mr.json` | Generic MR pattern; SAA lessons mostly omit MR from `drillIds`. |
| EV-TEACHER-222 | 2026-09-25 run-2 | `content/exercises/de-*.json` (60/60) | All exercises include rubric criteria; scenarios templated but objective-linked. |
| EV-TEACHER-223 | 2026-09-25 run-2 | `docs/change-requests.md` CR-0005 | Teacher post-implementation verdict: learning-quality concerns remain (F-202, F-201, labs). |

---

## Lesson sequence / objective fit (23/23)

| ID | Date | Source | Summary |
| --- | --- | --- | --- |
| EV-TEACHER-224 | 2026-09-25 run-2 | `a0-lab-safety.json` | Tier A0; 1 objective; drillIds match disk; sequence fit: preflight before AWS labs. |
| EV-TEACHER-225 | 2026-09-25 run-2 | `lesson-1-1.json` | 11 objectives ↔ 11 drills; hyphen drillIds; empty lab/exercise arrays vs registry links. |
| EV-TEACHER-226 | 2026-09-25 run-2 | `lesson-1-2.json` | 10 objectives; **all 10 drillIds missing on disk** (dot segments). |
| EV-TEACHER-227 | 2026-09-25 run-2 | `lesson-1-3.json` | 11 objectives; 11/11 drill file mismatch. |
| EV-TEACHER-228 | 2026-09-25 run-2 | `lesson-2-1.json` | 23 objectives; 23/23 drill mismatch — largest broken lesson bank. |
| EV-TEACHER-229 | 2026-09-25 run-2 | `lesson-2-2.json` | 20 objectives; 20/20 drill mismatch. |
| EV-TEACHER-230 | 2026-09-25 run-2 | `lesson-3-1.json` | 5 objectives; 5/5 drill mismatch. |
| EV-TEACHER-231 | 2026-09-25 run-2 | `lesson-3-2.json` | 10 objectives; 10/10 drill mismatch. |
| EV-TEACHER-232 | 2026-09-25 run-2 | `lesson-3-3.json` | 13 objectives; 13/13 drill mismatch. |
| EV-TEACHER-233 | 2026-09-25 run-2 | `lesson-3-4.json` | 8 objectives; 8/8 drill mismatch. |
| EV-TEACHER-234 | 2026-09-25 run-2 | `lesson-3-5.json` | 14 objectives; 14/14 drill mismatch. |
| EV-TEACHER-235 | 2026-09-25 run-2 | `lesson-4-1.json` | 21 objectives; 21/21 drill mismatch. |
| EV-TEACHER-236 | 2026-09-25 run-2 | `lesson-4-2.json` | 15 objectives; 15/15 drill mismatch. |
| EV-TEACHER-237 | 2026-09-25 run-2 | `lesson-4-3.json` | 14 objectives; 14/14 drill mismatch. |
| EV-TEACHER-238 | 2026-09-25 run-2 | `lesson-4-4.json` | 14 objectives; 14/14 drill mismatch. |
| EV-TEACHER-239 | 2026-09-25 run-2 | `lesson-tf-g1.json` | T1 objectives 1a–1c; 4 drills; IDs resolve. |
| EV-TEACHER-240 | 2026-09-25 run-2 | `lesson-tf-g2.json` | T2 providers/state; 5 drills; IDs resolve. |
| EV-TEACHER-241 | 2026-09-25 run-2 | `lesson-tf-g3.json` | T3 workflow; 8 drills; links GL-20. |
| EV-TEACHER-242 | 2026-09-25 run-2 | `lesson-tf-g4.json` | T4 HCL language; 9 drills; IDs resolve. |
| EV-TEACHER-243 | 2026-09-25 run-2 | `lesson-tf-g5.json` | Modules group; 5 drills; IDs resolve. |
| EV-TEACHER-244 | 2026-09-25 run-2 | `lesson-tf-g6.json` | Backends/state; 5 drills; IDs resolve. |
| EV-TEACHER-245 | 2026-09-25 run-2 | `lesson-tf-g7.json` | Import/CLI; 4 drills; IDs resolve. |
| EV-TEACHER-246 | 2026-09-25 run-2 | `lesson-tf-g8.json` | HCP objectives 8a–8d; 5 drills + GL-21 link; lab title over-promises HCP hands-on. |

---

## Coverage matrix (registry → lesson → drill → lab)

| ID | Date | Source | Summary |
| --- | --- | --- | --- |
| EV-TEACHER-268 | 2026-09-25 run-2 | `content/objectives/saa_c03.json`, `terraform_004.json`, `content/coverage/saa_registry.json` | **SAA:** 189 registry rows — each has `lesson_refs` + `drill_refs`; 47 rows list guided labs; 70 list design exercises. **TF:** 37 objectives in `terraform_004.json`; lessons T1–T8 + 119 TF questions in bank. Lesson JSON `labIds`/`exerciseIds` often empty while registry populated → navigation gap (F-206). |
| EV-TEACHER-269 | 2026-09-25 run-2 | `reports/evidence/sample.md` | Stratified sample 429/429 question IDs includes full TF bank (119) and all lesson scopes noted in sample header. |

---

## Guided lab objective fit (21/21)

| ID | Date | Source | Summary |
| --- | --- | --- | --- |
| EV-TEACHER-247 | 2026-09-25 run-2 | `gl-01.json` | Identity/budget preflight; objectives align IAM + cost awareness. |
| EV-TEACHER-248 | 2026-09-25 run-2 | `gl-02.json` | S3 private/versioned controls; teardown complete. |
| EV-TEACHER-249 | 2026-09-25 run-2 | `gl-03.json` | IAM role + resource policy + STS. |
| EV-TEACHER-250 | 2026-09-25 run-2 | `gl-04.json` | CMK KMS lab matches encryption objectives. |
| EV-TEACHER-251 | 2026-09-25 run-2 | `gl-05.json` | VPC segmentation; AWS architect flagged runnable concerns (V-01). |
| EV-TEACHER-252 | 2026-09-25 run-2 | `gl-06.json` | NAT/EIP/VPC — strong exam alignment. |
| EV-TEACHER-253 | 2026-09-25 run-2 | `gl-07.json` | EC2/EBS/EFS storage trio. |
| EV-TEACHER-254 | 2026-09-25 run-2 | `gl-08.json` | ALB — paper review blocker candidate (V-01). |
| EV-TEACHER-255 | 2026-09-25 run-2 | `gl-09.json` | Auto Scaling group workflow. |
| EV-TEACHER-256 | 2026-09-25 run-2 | `gl-10.json` | SQS/Lambda event path; sidecar file friction (F-P02). |
| EV-TEACHER-257 | 2026-09-25 run-2 | `gl-11.json` | API Gateway + Lambda. |
| EV-TEACHER-258 | 2026-09-25 run-2 | `gl-12.json` | Step Functions orchestration. |
| EV-TEACHER-259 | 2026-09-25 run-2 | `gl-13.json` | DynamoDB table operations. |
| EV-TEACHER-260 | 2026-09-25 run-2 | `gl-14.json` | RDS single-AZ. |
| EV-TEACHER-261 | 2026-09-25 run-2 | `gl-15.json` | CloudWatch + CloudTrail observability. |
| EV-TEACHER-262 | 2026-09-25 run-2 | `gl-16.json` | Route 53 private DNS. |
| EV-TEACHER-263 | 2026-09-25 run-2 | `gl-17.json` | Athena tiny query — paper blocker candidate (V-01). |
| EV-TEACHER-264 | 2026-09-25 run-2 | `gl-18.json` | ECS Fargate. |
| EV-TEACHER-265 | 2026-09-25 run-2 | `gl-19.json` | EKS control plane lifecycle. |
| EV-TEACHER-266 | 2026-09-25 run-2 | `gl-20.json` | Terraform capstone; fixture validates; s03 text defect (F-203). |
| EV-TEACHER-267 | 2026-09-25 run-2 | `gl-21.json` | ElastiCache hands-on OK; HCP title mismatch (F-204). |

---

## Design exercises (60/60 rubrics)

| ID | Date | Source | Summary |
| --- | --- | --- | --- |
| EV-TEACHER-270 | 2026-09-25 run-2 | `content/exercises/*.json` (60 files) | Every exercise includes rubric/scoring criteria; 0 missing rubric; scenarios use short template but map to registry `exercise_refs`. |

---

## Paper feedback (Gate 0)

| ID | Date | Source | Summary |
| --- | --- | --- | --- |
| EV-TEACHER-271 | 2026-09-25 run-2 | `reports/evidence/gate0-save-failure.md` | POST `/api/attempts` and GL-01 checkpoint return 403 CSRF; UI shows `Forbidden` — **Cannot verify** live scoring feedback this pass. |

---

## Terraform MCP / WebFetch lookups (26)

| ID | Date | Source | Summary |
| --- | --- | --- | --- |
| EV-TEACHER-300 | 2026-09-25 run-2 | MCP `SearchAwsProviderDocs` | `aws_s3_bucket_public_access_block` — GL-20 fixture. |
| EV-TEACHER-301 | 2026-09-25 run-2 | MCP | `aws_elasticache_cluster` — GL-21 Redis lab. |
| EV-TEACHER-302 | 2026-09-25 run-2 | MCP | `aws_dynamodb_table` — GL-13. |
| EV-TEACHER-303 | 2026-09-25 run-2 | MCP | `aws_lambda_function` — GL-10/11. |
| EV-TEACHER-304 | 2026-09-25 run-2 | MCP | `aws_iam_role` — GL-03. |
| EV-TEACHER-305 | 2026-09-25 run-2 | MCP | `aws_s3_bucket` — GL-02/20. |
| EV-TEACHER-306 | 2026-09-25 run-2 | WebFetch | `terraform plan` / `-refresh-only`. |
| EV-TEACHER-307 | 2026-09-25 run-2 | WebFetch | `terraform init`. |
| EV-TEACHER-308 | 2026-09-25 run-2 | WebFetch | `terraform validate`. |
| EV-TEACHER-309 | 2026-09-25 run-2 | WebFetch | `terraform fmt`. |
| EV-TEACHER-310 | 2026-09-25 run-2 | WebFetch | State backends doc. |
| EV-TEACHER-311 | 2026-09-25 run-2 | WebFetch | `terraform apply`. |
| EV-TEACHER-312 | 2026-09-25 run-2 | WebFetch | `terraform destroy`. |
| EV-TEACHER-313 | 2026-09-25 run-2 | WebFetch | State locking. |
| EV-TEACHER-314 | 2026-09-25 run-2 | WebFetch | Modules overview. |
| EV-TEACHER-315 | 2026-09-25 run-2 | WebFetch | Import workflow. |
| EV-TEACHER-316 | 2026-09-25 run-2 | WebFetch | Input variables. |
| EV-TEACHER-317 | 2026-09-25 run-2 | WebFetch | Output values. |
| EV-TEACHER-318 | 2026-09-25 run-2 | WebFetch | Data sources. |
| EV-TEACHER-319 | 2026-09-25 run-2 | WebFetch | `terraform state list`. |
| EV-TEACHER-320 | 2026-09-25 run-2 | MCP | `aws_vpc` — GL-05/06. |
| EV-TEACHER-321 | 2026-09-25 run-2 | MCP | `aws_nat_gateway` — GL-06 depends_on pattern. |
| EV-TEACHER-322 | 2026-09-25 run-2 | MCP | `aws_kms_key` — GL-04. |
| EV-TEACHER-323 | 2026-09-25 run-2 | `lab-fixtures/gl-20/main.tf` | `required_version >= 1.12.0, < 1.17.0`; provider `hashicorp/aws ~> 6.0`. |
| EV-TEACHER-324 | 2026-09-25 run-2 | `content/citations/cite-tf-004.json` | Citation bundle present for TF lessons; question `mcpStatus` still pending_recheck. |
| EV-TEACHER-325 | 2026-09-25 run-2 | `q-tf-004-3d-mc2.json` (sample) | Plan-step drill aligns with EV-TEACHER-306 plan docs (conceptual). |

---

## TF-VALID — objective fit + rationale (70 items from `sample.md`)

Format: `ID | question | objective | stem class | objective fit | rationale quality`

| ID | Question | Objective | Stem | Fit | Rationale |
| --- | --- | --- | --- | --- | --- |
| TF-VALID-001 | q-tf-004-1a-mc | tf.004.1a | template | ok | generic 4-line |
| TF-VALID-002 | q-tf-004-1a-mc2 | tf.004.1a | scenario | ok | specific |
| TF-VALID-003 | q-tf-004-1a-mr | tf.004.1a | scenario | ok | specific |
| TF-VALID-004 | q-tf-004-1b-mc | tf.004.1b | template | ok | generic |
| TF-VALID-005 | q-tf-004-1b-mc2 | tf.004.1b | scenario | ok | specific |
| TF-VALID-006 | q-tf-004-1b-mr | tf.004.1b | scenario | ok | specific |
| TF-VALID-007 | q-tf-004-1c-mc | tf.004.1c | template | ok | generic |
| TF-VALID-008 | q-tf-004-1c-mc2 | tf.004.1c | scenario | ok | specific |
| TF-VALID-009 | q-tf-004-1c-mr | tf.004.1c | scenario | ok | specific |
| TF-VALID-010 | q-tf-004-2a-mc | tf.004.2a | template | ok | generic |
| TF-VALID-011 | q-tf-004-2a-mc2 | tf.004.2a | scenario | ok | specific |
| TF-VALID-012 | q-tf-004-2a-mr | tf.004.2a | scenario | ok | specific |
| TF-VALID-013 | q-tf-004-2b-mc | tf.004.2b | template | ok | generic |
| TF-VALID-014 | q-tf-004-2b-mc2 | tf.004.2b | scenario | ok | specific |
| TF-VALID-015 | q-tf-004-2b-mr | tf.004.2b | scenario | ok | specific |
| TF-VALID-016 | q-tf-004-2c-mc | tf.004.2c | template | ok | generic |
| TF-VALID-017 | q-tf-004-2c-mc2 | tf.004.2c | scenario | ok | specific |
| TF-VALID-018 | q-tf-004-2c-mr | tf.004.2c | scenario | ok | specific |
| TF-VALID-019 | q-tf-004-2d-mc | tf.004.2d | template | ok | generic |
| TF-VALID-020 | q-tf-004-2d-mc2 | tf.004.2d | scenario | ok | specific |
| TF-VALID-021 | q-tf-004-2d-mr | tf.004.2d | scenario | ok | specific |
| TF-VALID-022 | q-tf-004-3a-mc | tf.004.3a | template | ok | generic |
| TF-VALID-023 | q-tf-004-3a-mc2 | tf.004.3a | scenario | ok | specific |
| TF-VALID-024 | q-tf-004-3a-mr | tf.004.3a | scenario | ok | specific |
| TF-VALID-025 | q-tf-004-3b-mc | tf.004.3b | template | ok | generic |
| TF-VALID-026 | q-tf-004-3b-mc2 | tf.004.3b | scenario | ok | specific |
| TF-VALID-027 | q-tf-004-3b-mr | tf.004.3b | scenario | ok | specific |
| TF-VALID-028 | q-tf-004-3c-mc | tf.004.3c | template | ok | generic |
| TF-VALID-029 | q-tf-004-3c-mc2 | tf.004.3c | scenario | ok | specific |
| TF-VALID-030 | q-tf-004-3c-mr | tf.004.3c | scenario | ok | specific |
| TF-VALID-031 | q-tf-004-3d-mc | tf.004.3d | template | ok | generic |
| TF-VALID-032 | q-tf-004-3d-mc2 | tf.004.3d | scenario | ok | specific |
| TF-VALID-033 | q-tf-004-3d-mr | tf.004.3d | scenario | ok | specific |
| TF-VALID-034 | q-tf-004-3e-mc | tf.004.3e | template | ok | generic |
| TF-VALID-035 | q-tf-004-3e-mc2 | tf.004.3e | scenario | ok | specific |
| TF-VALID-036 | q-tf-004-3e-mr | tf.004.3e | scenario | ok | specific |
| TF-VALID-037 | q-tf-004-3f-mc | tf.004.3f | template | ok | generic |
| TF-VALID-038 | q-tf-004-3f-mc2 | tf.004.3f | scenario | ok | specific |
| TF-VALID-039 | q-tf-004-3f-mr | tf.004.3f | scenario | ok | specific |
| TF-VALID-040 | q-tf-004-3g-mc | tf.004.3g | template | ok | generic |
| TF-VALID-041 | q-tf-004-3g-mc2 | tf.004.3g | scenario | ok | specific |
| TF-VALID-042 | q-tf-004-3g-mr | tf.004.3g | scenario | ok | specific |
| TF-VALID-043 | q-tf-004-4a-mc | tf.004.4a | template | ok | generic |
| TF-VALID-044 | q-tf-004-4a-mc2 | tf.004.4a | scenario | ok | specific |
| TF-VALID-045 | q-tf-004-4a-mr | tf.004.4a | scenario | ok | specific |
| TF-VALID-046 | q-tf-004-4b-mc | tf.004.4b | template | ok | generic |
| TF-VALID-047 | q-tf-004-4b-mc2 | tf.004.4b | scenario | ok | specific |
| TF-VALID-048 | q-tf-004-4b-mr | tf.004.4b | scenario | ok | specific |
| TF-VALID-049 | q-tf-004-4c-mc | tf.004.4c | template | ok | generic |
| TF-VALID-050 | q-tf-004-4c-mc2 | tf.004.4c | scenario | ok | specific |
| TF-VALID-051 | q-tf-004-4c-mr | tf.004.4c | scenario | ok | specific |
| TF-VALID-052 | q-tf-004-4d-mc | tf.004.4d | template | ok | generic |
| TF-VALID-053 | q-tf-004-4d-mc2 | tf.004.4d | scenario | ok | specific |
| TF-VALID-054 | q-tf-004-4d-mr | tf.004.4d | scenario | ok | specific |
| TF-VALID-055 | q-tf-004-4e-mc | tf.004.4e | template | ok | generic |
| TF-VALID-056 | q-tf-004-4e-mc2 | tf.004.4e | scenario | ok | specific |
| TF-VALID-057 | q-tf-004-4e-mr | tf.004.4e | scenario | ok | specific |
| TF-VALID-058 | q-tf-004-4f-mc | tf.004.4f | template | ok | generic |
| TF-VALID-059 | q-tf-004-4f-mc2 | tf.004.4f | scenario | ok | specific |
| TF-VALID-060 | q-tf-004-4f-mr | tf.004.4f | scenario | ok | specific |
| TF-VALID-061 | q-tf-004-4g-mc | tf.004.4g | template | ok | generic |
| TF-VALID-062 | q-tf-004-4g-mc2 | tf.004.4g | scenario | ok | specific |
| TF-VALID-063 | q-tf-004-4g-mr | tf.004.4g | scenario | ok | specific |
| TF-VALID-064 | q-tf-004-4h-mc | tf.004.4h | template | ok | generic |
| TF-VALID-065 | q-tf-004-4h-mc2 | tf.004.4h | scenario | ok | specific |
| TF-VALID-066 | q-tf-004-4h-mr | tf.004.4h | scenario | ok | specific |
| TF-VALID-067 | q-tf-004-5a-mc | tf.004.5a | template | ok | generic |
| TF-VALID-068 | q-tf-004-5a-mc2 | tf.004.5a | scenario | ok | specific |
| TF-VALID-069 | q-tf-004-5a-mr | tf.004.5a | scenario | ok | specific |
| TF-VALID-070 | q-tf-004-5b-mc | tf.004.5b | template | ok | generic |

*Remaining 49 TF sample IDs (5b–8d + extras) follow the same pattern: objectiveIds match `terraform_004.json`; 37/119 primary `-mc` stems are template-class; mc2/mr/extra-00–07 generally scenario-class (EV-TEACHER-220).*
