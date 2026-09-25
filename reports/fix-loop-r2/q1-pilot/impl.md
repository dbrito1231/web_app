# Q1 pilot: SAA task 1.1 rewrite (Lead Dev implementation report)

Date: 2026-09-26. Scope: the 19 files `content/questions/q-saa-1-1-*.json` (11 MC, 8 MR) plus 33 new citation files `content/citations/cite-saa-1-1-*.json`. No other files were changed. No git commands were run.

Method: every stem, choice and rationale was rewritten from scratch. Each AWS claim was checked by fetching the cited page from `docs.aws.amazon.com` with WebFetch on 2026-09-26. `id`, `type`, `module` and `objectiveIds` were kept. Files were written with `json.dumps(indent=2, ensure_ascii=True) + "\n"`.

- Builder script: `scratchpad/q1_build.py`
- Metrics script: `scratchpad/q1_metrics.py`

## Checks

| Check | Result |
|---|---|
| `python scripts\content_lint.py` | PASS (429 questions; A1 MC key share is within the 45% rule) |
| `python manage.py test workbook` | OK (19 tests) |

## Q1 acceptance metrics (from `q1_metrics.py`)

| Metric | Target | Result |
|---|---|---|
| MC questions where the key is the longest choice (ties count) | ≤ 35% | **1/11 = 9%** (k05-mc) |
| MR questions where the keys are exactly the N longest choices (informational) | n/a | 1/8 |
| MC key positions | balanced | a 3, b 2, c 3, d 3 |
| MR key positions (16 keys) | balanced | a 3, b 3, c 3, d 3, e 4 |
| Largest number of stems sharing the same 6-word opening | 1 in batch | **1** (all 19 stems open differently) |
| Choices or stems that contain objective text, or the phrase "Apply the objective" | 0 | **0** |
| Rationales that refer to choices by letter ("A and B", "Option C", "(a)") | 0 | **0** |
| Questions with ≥ 1 valid `citationId`, `mcpStatus: verified` and `reviewedOn: 2026-09-26` | 19/19 | **19/19** |
| `selectCount` equals the key length, and every MR stem says "(Select TWO.)" | all | all |
| Choice counts | MC 4, MR 5–6 | MC 4, MR 5 |

Every rationale explains the key and names each distractor by its content.

Difficulty uses the existing vocabulary only: 17 `applied` and 2 `foundation` (k03-mc and k05-mc). The value `analysis` is not used anywhere in the bank, so I did not add it.

## Per question

Citation slugs are the `cite-saa-1-1-<slug>` files. The URLs are listed in the table at the end.

| ID | Objective | What it tests | Key | Citations |
|---|---|---|---|---|
| k01-mc | K01 multi-account access | Region restriction that also binds admins and the root user. The key is an SCP with `aws:RequestedRegion`. Distractors: an identity-based deny, a permissions boundary, and an org trail with an alert. | c | scp, deny-region, root-bp |
| k01-mr | K01 | Cross-account access for a machine and for humans. The keys are a cross-account role for the scanner and Identity Center permission sets for auditors. Distractors: IAM users with keys, an SCP that "grants", and an IAM group in the management account. | a, d | xacct-tutorial, idc-permsets, scp, iam-bp |
| k02-mc | K02 federation / Identity Center | Workforce SSO to 12 accounts through one trust. The key is Identity Center with the external IdP. Distractors: Cognito, 12 separate IAM SAML trusts, and IAM users. | a | idc-what, idc-permsets, saml, cognito, iam-bp |
| k03-mc | K03 global infrastructure | Data residency (Region isolation) plus surviving the loss of an AZ. The key is RDS Multi-AZ in one Region. Distractors: a cross-Region replica, a Local Zone, and a single AZ. | d | regions-azs, rds-multiaz |
| k04-mc | K04 least privilege | Scoping a Lambda role to one S3 prefix. Distractors: AmazonS3ReadOnlyAccess, IAM user keys, and a boundary on top of full access. | b | iam-bp, managed-inline, boundaries |
| k04-mr | K04 | Evidence-based right-sizing. The keys are Access Analyzer policy generation and last accessed information. Distractors: PowerUserAccess, GuardDuty, and an admin boundary. | b, e | aa-policygen, last-accessed, iam-bp, guardduty, boundaries |
| k05-mc | K05 shared responsibility | What the customer still owns on RDS: security groups and DB users. Distractors: physical infrastructure, hardware maintenance, and Multi-AZ replication. | c | rds-security, rds-maint, rds-multiaz |
| s01-mc | S01 root/IAM user best practices | A root access key used by a script, and no MFA. The key moves the script to a role, deletes the key and adds MFA. Distractors: rotate the root key, add MFA but keep the key, and a shared admin IAM user. | a | root-bp, iam-bp |
| s01-mr | S01 | Requiring MFA for API calls and ending long-lived keys. The keys are a Deny on `aws:MultiFactorAuthPresent` and Identity Center temporary credentials. Distractors: an MFA option in the password policy (it has none), key rotation, and "inherit" root MFA. | c, e | mfa-policy, pw-policy, iam-bp, idc-what |
| s02-mc | S02 users/groups/roles/policies | Team-based permissions with frequent moves. The key is one group per team with a managed policy. Distractors: inline policies per user, nested groups (not supported), and a group as a Principal (not allowed). | d | groups, managed-inline |
| s02-mr | S02 | Three apps that share one policy and store no credentials. The keys are an instance profile role and one customer managed policy. Distractors: keys in the AMI, inline copies, and EC2 instances in a group. | a, c | ec2-role, managed-inline, groups |
| s03-mc | S03 STS / cross-account | Third-party SaaS access and the confused deputy problem. The key is a role with an `sts:ExternalId` condition. Distractors: IAM user keys, a trust with no condition, and per-resource policies. | c | third-party |
| s03-mr | S03 | Dev-to-prod role switching. The keys are the trust policy in prod and `sts:AssumeRole` allowed in dev (both sides are required). Distractors: IAM users in prod, VPC peering, and a role in a group. | b, d | xacct-tutorial, identity-vs-resource, groups |
| s04-mc | S04 Control Tower / SCPs | A landing zone with guardrails and account vending. The key is Control Tower. Distractors: DIY Organizations with scripts, Service Catalog alone, and Identity Center. | a | control-tower, scp |
| s04-mr | S04 | A tamper-proof trail and a ban on IAM users and access keys for new accounts. The keys are an organization trail and an SCP on the OUs. Distractors: an SCP on the management account (no effect), boundaries, and trails owned by local admins. | a, e | org-trail, scp, boundaries |
| s05-mc | S05 resource policies | Cross-account S3 read when the identity policy already exists. The key is a bucket policy naming the role. Distractors: an SCP, a boundary, and a new IAM user. | d | identity-vs-resource, s3-xacct, scp, boundaries |
| s05-mr | S05 | Cross-account Lambda invoke and SQS send without AssumeRole. The keys are the Lambda resource-based policy and the SQS queue policy. Distractors: an SCP, a boundary on the execution role, and an IAM group. | b, c | lambda-xacct, sqs-policies, identity-vs-resource, scp, groups |
| s06-mc | S06 federate directory with IAM roles | AD FS to the console for one account, with AD groups mapped to roles. The key is an IAM SAML provider with roles. Distractors: a Cognito identity pool, IAM users with password sync, and replacing the forest with Managed Microsoft AD. | b | saml, cognito, managed-ad, iam-bp |
| s06-mr | S06 | On-prem AD for 15 accounts with no domain controllers in AWS. The keys are AD Connector and Identity Center with AD as the identity source. Distractors: Simple AD, a Cognito user pool, and Managed Microsoft AD. | d, e | ad-connector, idc-ad, simple-ad, managed-ad, cognito |

### Citation URLs (all accessed 2026-09-26)

| Slug | URL |
|---|---|
| scp | https://docs.aws.amazon.com/organizations/latest/userguide/orgs_manage_policies_scps.html |
| deny-region | https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_examples_aws_deny-requested-region.html |
| idc-what | https://docs.aws.amazon.com/singlesignon/latest/userguide/what-is.html |
| idc-permsets | https://docs.aws.amazon.com/singlesignon/latest/userguide/permissionsetsconcept.html |
| idc-ad | https://docs.aws.amazon.com/singlesignon/latest/userguide/manage-your-identity-source-ad.html |
| boundaries | https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies_boundaries.html |
| iam-bp | https://docs.aws.amazon.com/IAM/latest/UserGuide/best-practices.html |
| root-bp | https://docs.aws.amazon.com/IAM/latest/UserGuide/root-user-best-practices.html |
| aa-policygen | https://docs.aws.amazon.com/IAM/latest/UserGuide/access-analyzer-policy-generation.html |
| last-accessed | https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies_last-accessed.html |
| pw-policy | https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_passwords_account-policy.html |
| mfa-policy | https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_examples_aws_my-sec-creds-self-manage.html |
| groups | https://docs.aws.amazon.com/IAM/latest/UserGuide/id_groups.html |
| managed-inline | https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies_managed-vs-inline.html |
| ec2-role | https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_use_switch-role-ec2.html |
| third-party | https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_common-scenarios_third-party.html |
| xacct-tutorial | https://docs.aws.amazon.com/IAM/latest/UserGuide/tutorial_cross-account-with-roles.html |
| identity-vs-resource | https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies_identity-vs-resource.html |
| saml | https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_providers_saml.html |
| regions-azs | https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/using-regions-availability-zones.html |
| rds-multiaz | https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/Concepts.MultiAZSingleStandby.html |
| rds-security | https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/UsingWithRDS.html |
| rds-maint | https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_UpgradeDBInstance.Maintenance.html |
| control-tower | https://docs.aws.amazon.com/controltower/latest/userguide/what-is-control-tower.html |
| org-trail | https://docs.aws.amazon.com/awscloudtrail/latest/userguide/creating-trail-organization.html |
| s3-xacct | https://docs.aws.amazon.com/AmazonS3/latest/userguide/example-walkthroughs-managing-access-example2.html |
| lambda-xacct | https://docs.aws.amazon.com/lambda/latest/dg/permissions-function-cross-account.html |
| sqs-policies | https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/sqs-basic-examples-of-sqs-policies.html |
| ad-connector | https://docs.aws.amazon.com/directoryservice/latest/admin-guide/directory_ad_connector.html |
| simple-ad | https://docs.aws.amazon.com/directoryservice/latest/admin-guide/directory_simple_ad.html |
| managed-ad | https://docs.aws.amazon.com/directoryservice/latest/admin-guide/directory_microsoft_ad.html |
| cognito | https://docs.aws.amazon.com/cognito/latest/developerguide/what-is-amazon-cognito.html |
| guardduty | https://docs.aws.amazon.com/guardduty/latest/ug/what-is-guardduty.html |

## Where I was unsure (please focus Teacher and AWS review here)

1. **s06-mc (S06).** In the real world, IAM Identity Center with AD Connector would also let AD users reach a single account. I left Identity Center out of the choices on purpose, so the key (an IAM SAML provider plus roles, which matches "federate ... with IAM roles") is the only best answer. Teacher should confirm this is fair and not a trick.
2. **k05-mc (K05).** I avoided "OS patching" as a distractor. The RDS maintenance page says *optional* OS updates are not applied automatically, so the customer shares that decision. The distractors are hardware maintenance, infrastructure protection and Multi-AZ replication, which the docs attribute to AWS without that nuance.
3. **k01-mc (K01).** The Organizations SCP examples page now only links to a GitHub repo, and WebFetch could not read the general-examples subpage. So the Region-deny pattern is cited from the IAM example policy (the same `aws:RequestedRegion` + `NotAction` pattern). The SCP behaviour it relies on (applies to the member root user, inherited from OUs, never grants) is cited from the SCP page.
4. **k03-mc (K03).** K03 is general infrastructure knowledge, not access control. I framed it as data residency (Region isolation) plus surviving an AZ loss, so it still fits task 1.1. I did not use the "an AZ is one or more discrete data centers" wording, because the fetched pages did not state it.
5. **s01-mr (S01).** The Identity Center key relies on Identity Center's own MFA settings to satisfy "API calls only after MFA". The IAM best-practices page supports this, but it is less direct than the `aws:MultiFactorAuthPresent` key.
6. **Simple AD (s06-mr).** The docs now say Simple AD is closed to new customers. The distractor stays valid because Simple AD is also unsupported by Identity Center and cannot form trusts. It may confuse a student who studied from older material.
7. **Lesson `drillIds` text (N4).** Not touched. The question IDs are unchanged, so the links still resolve.
