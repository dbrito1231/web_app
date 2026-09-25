# Amendment 2, batch F7: lesson 1.1 rewrite, Q1-T3 question fixes, Q1-T2 exercise fix

Batch F7 per `.cursor/plans/lead_dev_fix_loop_round2_20260926.plan.md` ("Amendment 2"). Files touched: `content/lessons/lesson-1-1.json`; `content/questions/q-saa-1-1-{k04-mr,s02-mr,s06-mr}.json`; `content/exercises/de-federation.json`; new citations `content/citations/cite-saa-1-1-{policy-eval,org-overview,aa-external,ta-keys}.json`. No other files edited. `python scripts\content_lint.py` PASS (429 questions: aws 310, tf 119; labs 21+21; lessons 23).

## 1. Lesson 1.1 outline (T1, L1)

Replaces the boilerplate "Tradeoffs / Applied practice" paragraphs with real teaching, one section per objective, ~2,300 words, using only headings (`###`), bullets, bold and inline code (checked against `frontend/src/utils/markdown.tsx`, which does not render tables or `[text](url)` links — so no markdown tables or link syntax were used; comparisons are written as bullet lists instead).

| Objective | Section | Concepts taught | Prepares for |
|---|---|---|---|
| SAA-1.1-K01 | Access controls across multiple accounts | SCPs set a ceiling, never grant; OU inheritance covers root; SCPs never apply to the management account; Region-lock pattern with `NotAction` exemptions | k01-mc, k01-mr, s04-mc, s04-mr |
| SAA-1.1-K02 | Federated access and identity services | IAM Identity Center (one trust, permission sets, access portal) vs per-account IAM SAML vs Cognito (app users, not workforce) | k02-mc, s06-mc, s06-mr |
| SAA-1.1-K03 | AWS global infrastructure | Region isolation/no auto-replication, AZ independence, Multi-AZ vs cross-Region replica, Local Zone is one location | k03-mc |
| SAA-1.1-K04 | Least privilege | Customer vs AWS managed policies, permissions boundaries (intersection, only narrows), Access Analyzer policy generation, last accessed information, external access findings (different feature) | k04-mc, k04-mr |
| SAA-1.1-K05 | Shared responsibility model | AWS vs customer scope; RDS example (hardware/replication vs security groups/DB users) | k05-mc |
| SAA-1.1-S01 | Securing IAM users and root | No root access keys, root MFA, `aws:MultiFactorAuthPresent` deny pattern, `sts:GetSessionToken`, password policy has no MFA option, roles/Identity Center replace long-lived keys | s01-mc, s01-mr |
| SAA-1.1-S02 | Authorization model: users/groups/roles/policies | Groups hold only users, no nesting, not a Principal; managed vs inline; EC2 instance profiles vs baked-in keys | s02-mc, s02-mr |
| SAA-1.1-S03 | RBAC: STS, role switching, cross-account | Both sides of `AssumeRole` (trust policy + calling identity policy); external ID and the confused deputy problem | s03-mc, s03-mr |
| SAA-1.1-S04 | Multi-account security strategy | Control Tower (landing zone, controls, Account Factory) vs hand-built Organizations; organization trail (member accounts can't stop it); OU-level SCPs vs management-account SCPs (no-op) | s04-mc, s04-mr |
| SAA-1.1-S05 | Resource policies | Identity-based + resource-based both required; S3 bucket policy, Lambda resource policy, SQS queue policy; SCP/boundary cannot grant | s05-mc, s05-mr |
| SAA-1.1-S06 | Federating a directory service with IAM roles | Single-account AD FS + IAM SAML provider; multi-account comparison of AD Connector, AWS Managed Microsoft AD, per-account SAML, Simple AD (retired); IAM Identity Center with AD Connector as identity source | s06-mc, s06-mr |

`drillIds` now lists all 19 `q-saa-1-1-*` questions (previously only the 11 MC items; the 8 MR variants were missing) — closes T4.

`citationIds` expanded from `["cite-1-1"]` to include every `cite-saa-1-1-*` file the lesson draws a claim from (36 IDs total), plus 4 new citations created for facts the existing question citations didn't cover:
- `cite-saa-1-1-policy-eval` — IAM policy evaluation logic (boundary = intersection; SCP = intersection; explicit deny always wins)
- `cite-saa-1-1-org-overview` — What is AWS Organizations? (consolidate/group accounts, apply policies)
- `cite-saa-1-1-aa-external` — IAM Access Analyzer findings (external access = resources shared outside the zone of trust, distinct from unused-access/last-accessed rightsizing)
- `cite-saa-1-1-ta-keys` — AWS Trusted Advisor security checks, IAM Access Key Rotation check (flags un-rotated keys after 90 days; does not evaluate a role's permissions)

All four were fetched live from `docs.aws.amazon.com` on 2026-09-26 and checked against the lesson text before writing it.

## 2. Question fixes (Q1-T3)

### q-saa-1-1-k04-mr
- **Before:** distractor (c) "Enable Amazon GuardDuty in every Region so that it removes permissions from roles once it detects that they are unused" — GuardDuty has no such feature. Distractor (d) "Set AdministratorAccess as the permissions boundary on every role so that the boundary follows actual usage" — self-evidently wrong (a boundary never "follows usage"), eliminable without any domain knowledge.
- **After:** (c) "Turn on an IAM Access Analyzer external access analyzer for the account and remove every role that appears in its findings" — a real, current feature that answers a different question (external/cross-account sharing, not usage-based rightsizing). (d) "Turn on the AWS Trusted Advisor IAM Access Key Rotation check and rotate the credentials it flags" — a real Trusted Advisor check that does IAM hygiene but never touches a role's permission set.
- Rationale rewritten to explain both new distractors by what they actually do; added `citationIds` `cite-saa-1-1-aa-external` and `cite-saa-1-1-ta-keys`; kept `mcpStatus: verified`, set `reviewedOn: 2026-09-26`.

### q-saa-1-1-s02-mr
- **Before stem:** "...each run under their own IAM role and all need the same read and write access..." — implied the roles were already attached to the instances, which made keyed choice (a) "attach each application's IAM role to its instances through an instance profile" look like something already done.
- **After stem:** "...each have their own IAM role defined, but the instances currently read long-term access keys for that role from a config file on disk to reach one DynamoDB table..." — the role exists but is not yet attached, and the instances currently use stored keys instead, so choice (a) is a real pending step. Choices, key, and rationale unchanged (they were already correct); `reviewedOn` set to 2026-09-26.

### q-saa-1-1-s06-mr
- **Before choice (e):** "IAM Identity Center using **that directory** as its identity source, with permission sets per account" — a dangling cross-choice reference (ambiguous which directory, and a pairing cue). **Before choice (a):** "A Simple AD directory that is populated with copies of the employee accounts" — Simple AD is closed to new customers, a dated distractor.
- **After choice (e):** "IAM Identity Center using an AWS Directory Service directory as its identity source, with permission sets per account" — stands alone. **After choice (a):** "An IAM SAML identity provider for AD FS, created separately in each of the 15 accounts, with IAM roles mapped from AD groups in every account" — a current, plausible federation approach that keeps passwords on premises and adds no AWS domain controllers, but fails the "managed from one central place" requirement (which was added to the stem to make that the clear, single reason it's wrong).
- Stem also gained "...set up and managed from one central place rather than once per account..." so the new per-account-SAML distractor has exactly one flaw and isn't a second defensible answer.
- Rationale rewritten: explains AD Connector + Identity Center (kept), explains why per-account SAML fails (15 separate trusts instead of one), explains Cognito (kept), and — per the AWS reviewer's suggestion — adds that AWS Managed Microsoft AD is itself a directory hosted in AWS, so standing it up deploys domain controllers into your VPC and breaks "no domain controllers in AWS" even with a two-way trust.
- `citationIds` updated: dropped `cite-saa-1-1-simple-ad` (no longer referenced), kept `cite-saa-1-1-saml` (now used for the new distractor).

All three: `mcpStatus: "verified"`, `reviewedOn: "2026-09-26"`.

## 3. Exercise fix (Q1-T2)

`content/exercises/de-federation.json` previously had a generic scenario ("You must design a solution addressing: Directory federation with IAM roles...") that never named SAML, AD FS, AD Connector, AWS Managed Microsoft AD, or IAM Identity Center, so it did not teach or test the S06 decision points s06-mc/s06-mr assume.

**Scenario:** rewritten to require a single design record covering (1) a single-account case — choose between SAML 2.0 federation via AD FS and IAM Identity Center for console access with no IAM users — and (2) a multi-account case — compare AD Connector, AWS Managed Microsoft AD, and per-account SAML as the federation mechanism, and decide whether/how IAM Identity Center is used.

**Constraints:** added three new constraints naming the SAML/AD FS vs Identity Center decision, the AD Connector vs AWS Managed Microsoft AD vs per-account SAML comparison (with which one keeps passwords on premises and which one runs domain controllers in AWS), and whether/what Identity Center's identity source is.

**Rubric:** added `r6` (SAML/AD FS vs Identity Center choice justified, single-account case, 2 points) and `r7` (AD Connector vs AWS Managed Microsoft AD vs per-account SAML compared, multi-account case, naming the passwords/domain-controller tradeoff, 2 points). `objectiveIds` (`SAA-1.1-S06`), `id`, `title`, and the other rubric items (`r1`–`r5`) are unchanged.

## Doc URLs used (fetched 2026-09-26)

- https://docs.aws.amazon.com/organizations/latest/userguide/orgs_manage_policies_scps.html (SCPs)
- https://docs.aws.amazon.com/organizations/latest/userguide/orgs_introduction.html (What is AWS Organizations?) — new citation
- https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_evaluation-logic.html (policy evaluation logic: boundary/SCP intersection, explicit deny wins) — new citation
- https://docs.aws.amazon.com/IAM/latest/UserGuide/access-analyzer-findings.html (Access Analyzer external/internal/unused access findings) — new citation
- https://docs.aws.amazon.com/awssupport/latest/user/security-checks.html#iam-access-key-rotation (Trusted Advisor IAM Access Key Rotation check) — new citation
- https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies_boundaries.html (permissions boundaries)
- https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies_last-accessed.html (last accessed information)
- https://docs.aws.amazon.com/IAM/latest/UserGuide/access-analyzer-policy-generation.html (policy generation)
- https://docs.aws.amazon.com/singlesignon/latest/userguide/what-is.html, .../permissionsetsconcept.html, .../manage-your-identity-source-ad.html (IAM Identity Center)
- https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_providers_saml.html (SAML federation)
- https://docs.aws.amazon.com/cognito/latest/developerguide/what-is-amazon-cognito.html (Cognito)
- https://docs.aws.amazon.com/directoryservice/latest/admin-guide/directory_ad_connector.html (AD Connector)
- https://docs.aws.amazon.com/directoryservice/latest/admin-guide/directory_microsoft_ad.html (AWS Managed Microsoft AD)
- https://docs.aws.amazon.com/directoryservice/latest/admin-guide/directory_simple_ad.html (Simple AD)
- https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/using-regions-availability-zones.html (Regions/AZs)
- https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/Concepts.MultiAZSingleStandby.html, .../UsingWithRDS.html, .../USER_UpgradeDBInstance.Maintenance.html (RDS)
- https://docs.aws.amazon.com/IAM/latest/UserGuide/root-user-best-practices.html, .../best-practices.html (root/IAM best practices)
- https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_examples_aws_my-sec-creds-self-manage.html (MFA deny policy)
- https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_passwords_account-policy.html (password policy)
- https://docs.aws.amazon.com/IAM/latest/UserGuide/id_groups.html (IAM groups)
- https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies_managed-vs-inline.html (managed vs inline)
- https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_use_switch-role-ec2.html (EC2 instance role)
- https://docs.aws.amazon.com/IAM/latest/UserGuide/tutorial_cross-account-with-roles.html, .../id_roles_common-scenarios_third-party.html (cross-account roles, external ID)
- https://docs.aws.amazon.com/controltower/latest/userguide/what-is-control-tower.html (Control Tower)
- https://docs.aws.amazon.com/awscloudtrail/latest/userguide/creating-trail-organization.html (organization trail)
- https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies_identity-vs-resource.html, .../AmazonS3/latest/userguide/example-walkthroughs-managing-access-example2.html, .../lambda/latest/dg/permissions-function-cross-account.html, .../AWSSimpleQueueService/latest/SQSDeveloperGuide/sqs-basic-examples-of-sqs-policies.html (resource policies)

## Checks run

- `backend\.venv\Scripts\python.exe scripts\content_lint.py` → `questions 429 aws 310 tf 119`, `labs 21 + 21`, `lessons 23`, `PASS`.
- All `lesson-1-1.json` `citationIds` resolve to files in `content/citations/`.
- All `lesson-1-1.json` `drillIds` resolve to files in `content/questions/` and cover the full 19-file `q-saa-1-1-*` set with no extras missing.
- `lesson-1-1.json` `bodyMarkdown` contains no `|` table syntax, no `[text](url)` links, and no numbered-list lines — the renderer (`frontend/src/utils/markdown.tsx`) does not support any of these, only `#`/`##`/`###`/`####` headings, `- ` bullets, `**bold**`, and `` `code` ``.
- The three fixed question files parse as valid JSON and were saved with `json.dumps(data, indent=2, ensure_ascii=True) + "\n"`.

## Not done in this batch (out of scope for F7)

- Teacher's other T3 "optional" nits on s01-mc, s01-mr, k05-mc, s04-mr were not applied — Amendment 2 scoped this batch to k04-mr, s02-mr, and s06-mr only.
- Re-validation by Teacher/AWS/Student after implementation (required by AGENTS.md and the plan) is a separate step for the orchestrator to request.
