# Teacher evidence log (workbook evaluation 2026-09-25)

| ID | Date | Source | Summary |
| --- | --- | --- | --- |
| EV-TEACHER-001 | 2026-09-25 | `reports/evidence/content-scan.md`, `content-scan.json` | Scan: 721 findings; 380 `heuristic_longest_correct`; 21 `missing_beforeYouStart` (all UL); mcpStatus pending_recheck 427 / verified 0. |
| EV-TEACHER-002 | 2026-09-25 | `content/questions/q-saa-1-1-k01-mc.json` | Template MC stem + “Apply the objective directly…” correct choice; shared distractors B–D. |
| EV-TEACHER-003 | 2026-09-25 | `content/lessons/lesson-1-2.json` | `drillIds` use dots (`q-saa-1.2-k01-mc`); question files use hyphens (`q-saa-1-2-k01-mc`). |
| EV-TEACHER-004 | 2026-09-25 | `content/lessons/lesson-1-1.json` | Contrast: lesson 1-1 `drillIds` correctly hyphenated (post CR-0001). |
| EV-TEACHER-005 | 2026-09-25 | `reports/evidence/lint-output.txt` | `python scripts/content_lint.py` → PASS (429 questions, 42 labs, 23 lessons). |
| EV-TEACHER-006 | 2026-09-25 | `reports/evidence/scan-lab-placeholders-output.txt` | `scripts/scan_lab_placeholders.py` → PASS 41 labs scanned. |
| EV-TEACHER-007 | 2026-09-25 | `content/labs/gl-06.json` | Post–CR-0005: runnable VPC/NAT/EIP commands, IGW present, ordered teardown. |
| EV-TEACHER-008 | 2026-09-25 | `content/labs/gl-02.json` | Versioned-bucket teardown includes delete markers loop (addresses prior CR-0005 note). |
| EV-TEACHER-009 | 2026-09-25 | `content/labs/gl-20.json`, `lab-fixtures/gl-20/main.tf` | GL-20 includes `-var bucket_suffix`, OOB tag + `terraform plan -refresh-only`; fixture uses `aws_s3_bucket` + `aws_s3_bucket_public_access_block`. |
| EV-TEACHER-010 | 2026-09-25 | `content/labs/gl-20.json` s03 | Boilerplate bullet: “Terraform is not required unless a step says so” on a Terraform-primary lab. |
| EV-TEACHER-011 | 2026-09-25 | `content/labs/gl-21.json` | Title references HCP; body/steps are ElastiCache-only (no HCP steps). |
| EV-TEACHER-012 | 2026-09-25 | `content/labs/ul-01.json` … `ul-21.json` | No `beforeYouStart` on any unguided lab; guided GL-01–GL-21 all have 3-line preflight. |
| EV-TEACHER-013 | 2026-09-25 | `content/labs/gl-10.json` | Steps reference `file://gl10-trust.json`, `gl10-queue-policy.json`, `function.zip`; no committed lab artifacts under repo. |
| EV-TEACHER-014 | 2026-09-25 | `content/lessons/*.json` | All SAA exam lessons (`lesson-1-2` … `lesson-4-4`) have empty `labIds` and `exerciseIds`; 60 design exercises exist under `content/exercises/`. |
| EV-TEACHER-015 | 2026-09-25 | `content/lessons/lesson-1-1.json` body | SAA-1.1-K03 (Regions/AZ) cites IAM intro URL for every knowledge bullet. |
| EV-TEACHER-016 | 2026-09-25 | AWS Knowledge MCP `aws___read_documentation` | Budgets doc: default is alerts/notifications; optional budget *actions* can apply IAM policies—workbook distractor “deletes resources” remains false. URL: https://docs.aws.amazon.com/cost-management/latest/userguide/budgets-managing-costs.html |
| EV-TEACHER-017 | 2026-09-25 | AWS Knowledge MCP `aws___search_documentation` | Budget alerts lag; notifications do not inherently stop spend without configured actions. |
| EV-TEACHER-018 | 2026-09-25 | Terraform MCP `search_providers` + `get_provider_details` | Provider doc id 9242525: separate `aws_s3_bucket_public_access_block` matches GL-20 fixture pattern. |
| EV-TEACHER-019 | 2026-09-25 | HashiCorp `terraform plan` docs (WebFetch) | `-refresh-only` mode refreshes state without apply; supports GL-20 OOB tag drift step. |
| EV-TEACHER-020 | 2026-09-25 | `content/questions/q-tf-004-8-extra-00-mc.json` | Contrast: HCP extra drill has scenario-specific stem/rationale (not template bank). |
| EV-TEACHER-021 | 2026-09-25 | `content/questions/q-saa-1-1-k01-mr.json` | MR items use generic “Design against requirement / Validate with docs” pattern (~150+ MR files). |
| EV-TEACHER-022 | 2026-09-25 | `content/exercises/de-multi-account.json`, `de-federation.json`, `de-direct-connect.json` | Stratified design exercises: rubric + constraints present; scenarios templated but exam-appropriate for non-lab bullets. |
| EV-TEACHER-023 | 2026-09-25 | `docs/change-requests.md` CR-0005 | Status done; Teacher post-implementation re-review performed in this evaluation (see `reports/02-teacher.md`). |
