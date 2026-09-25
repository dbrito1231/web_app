# Amendment 2, batch F8: round-4 lesson/pilot fixes and the 15% distractor rule

Batch F8 per `.cursor/plans/lead_dev_fix_loop_round2_20260926.plan.md` ("Amendment 2"), closing the items in `reports/fix-loop-r2/round-4/TEACHER.md` and `reports/fix-loop-r2/round-4/AWS-lesson-pilot.md`. Files touched: `content/lessons/lesson-1-1.json`; all 19 `content/questions/q-saa-1-1-*.json`; `content/exercises/de-federation.json`; new citations `content/citations/cite-saa-1-1-{idc-idp-source,idc-instances,aa-unused,confused-deputy,org-delegated-admin,s3-object-ownership}.json`. No other files edited.

`python scripts\content_lint.py`: **PASS** (429 questions: aws 310, tf 119; labs 21+21; lessons 23).

## 1. s02-mr stem fix (TEACHER-R4-001 / AWS-R4-008)

- **Before:** "...each have their own IAM role defined, but the instances currently read long-term access keys **for that role** from a config file on disk..." — IAM roles have no long-term credentials, so this taught a false fact.
- **After:** "...each have their own IAM role defined, but the instances currently read **an IAM user's** long-term access keys from a config file on disk..."
- Choices, key (`a`, `c`), `selectCount`, and rationale unchanged, as instructed.
- Doc URL: https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles.html

## 2. Lesson 1.1 fixes

| # | Section | Before | After | Doc URL |
|---|---|---|---|---|
| 1 | K01 | "...an identity-based policy or a permissions boundary cannot do, since those apply only to the specific users, roles, or member accounts they are set on." | "...since those attach only to IAM users, groups, or roles (boundaries to users or roles), and neither can be attached to the root user." | https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies_boundaries.html |
| 2 | K02 | "one place to connect a single identity source (an external IdP over SAML/OIDC, Identity Center's own directory, or AWS Managed Microsoft AD) and assign **permission sets** to groups per account." | "...(an external IdP over SAML 2.0, with users and groups provisioned by SCIM; Identity Center's own directory; or Active Directory, either self-managed through AD Connector or AWS Managed Microsoft AD) and assign **permission sets** to groups per account (this requires an organization instance, enabled in the AWS Organizations management account)." | https://docs.aws.amazon.com/singlesignon/latest/userguide/manage-your-identity-source-idp.html ; https://docs.aws.amazon.com/singlesignon/latest/userguide/identity-center-instances.html |
| 3 | K04 | Bullets ended at last accessed information + external access findings; exam tip: "means Access Analyzer policy generation or last accessed information". | Added bullet: "IAM Access Analyzer unused access findings (a paid analyzer) continuously flag unused roles, unused access keys and passwords, and unused service- and action-level permissions on roles." Added bullet: "AWS Trusted Advisor's IAM Access Key Rotation check flags access keys that have not been rotated in 90 days. Rotating a flagged key is credential hygiene — it never changes what a role or user may do..." Exam tip now lists unused access findings too. | https://docs.aws.amazon.com/IAM/latest/UserGuide/access-analyzer-findings.html ; https://docs.aws.amazon.com/awssupport/latest/user/security-checks.html#iam-access-key-rotation |
| 4 | K04 | "IAM Access Analyzer policy generation reads a role's CloudTrail activity over a chosen period and drafts a policy containing only the actions actually used..." | "...reads an IAM user's or role's CloudTrail activity over a period of up to 90 days and drafts a policy from what was used (action-level for supported services, service-level otherwise; data events and `iam:PassRole` are not captured)..." | https://docs.aws.amazon.com/IAM/latest/UserGuide/access-analyzer-policy-generation.html |
| 5 | S01 | "Register **MFA** on the root user, and require MFA for IAM users too:" | "...on the root user (AWS now requires root MFA on standalone, management, and member accounts; in an organization, AWS recommends centrally managing root access and removing member-account root credentials altogether), and require MFA for IAM users too:" | https://docs.aws.amazon.com/IAM/latest/UserGuide/root-user-best-practices.html |
| 6 | S03 | "...without it, anyone who learns the role's ARN could ask the third party to assume it on their behalf." | "...without it, another customer of the same third party could give it your role ARN, and the third party's service would access your account on that customer's behalf." | https://docs.aws.amazon.com/IAM/latest/UserGuide/confused-deputy.html |
| 7 | S04 | "Accounts placed under a covered OU are picked up automatically." | "It covers every account in the organization, not selected OUs, and any account that later joins the organization is added to the trail automatically." | https://docs.aws.amazon.com/awscloudtrail/latest/userguide/creating-trail-organization.html |
| 8 | S06 | "...(set up once, typically in the management or a delegated administrator account)..." | "...(set up once, which must be in the management or a delegated administrator account)..." | https://docs.aws.amazon.com/singlesignon/latest/userguide/manage-your-identity-source-ad.html |
| 9 | 9 places | Single-asterisk `*italic*` spans: "maximum" (x2), "between", "your own", "same", "the cloud", "what you put in the cloud", "and", "gateway" — the markdown renderer (`frontend/src/utils/markdown.tsx`) does not support single-asterisk emphasis, so these rendered as literal asterisks. | All 9 converted to `**bold**` (7) or plain text (2: "between", "and" — emphasis wasn't load-bearing there). | n/a (renderer capability, not a doc fact) |

`citationIds` grew from 37 to 41: added `cite-saa-1-1-idc-idp-source`, `cite-saa-1-1-idc-instances`, `cite-saa-1-1-aa-unused`, `cite-saa-1-1-confused-deputy` (all four new facts above), plus `cite-saa-1-1-org-delegated-admin` and `cite-saa-1-1-s3-object-ownership` (used by the new q-saa-1-1-k01-mr and q-saa-1-1-s05-mc distractors below, kept on the lesson's list for consistency with the rest of the citation set).

## 3. de-federation exercise fixes (AWS-R4-009, TEACHER-R4-008)

| Item | Before | After |
|---|---|---|
| E1 constraint | "...state **which one** keeps passwords on premises and **which one** runs domain controllers in AWS" (implies exactly one each; AD Connector and per-account SAML both keep passwords on-prem) | "...state, **for each option**, whether passwords stay on premises and whether it runs domain controllers in AWS" |
| r7 rubric | "...naming which keeps passwords on premises and which adds domain controllers in AWS" | "...stating for each option whether passwords stay on premises and whether it adds domain controllers in AWS" |
| Scenario overlap | "...connect an AD Connector or AWS Managed Microsoft AD to IAM Identity Center, or run a fully AWS-hosted directory" (overlapped with the AWS Managed Microsoft AD option already listed) | "...or move users into AWS Managed Microsoft AD with no on-premises trust" |
| E2 (single-account Identity Center) | Not required | New constraint: "If IAM Identity Center is chosen for the single-account case, state that assigning AWS account access requires an organization instance (AWS Organizations enabled, with this account as the management account)" |

Doc URLs: https://docs.aws.amazon.com/singlesignon/latest/userguide/identity-center-instances.html ; https://docs.aws.amazon.com/singlesignon/latest/userguide/manage-your-identity-source-ad.html

## 4. The 15% distractor rule (TEACHER-R4-007)

### Distractor-type counts, before

| Type | Occurrences (question, choice) | Count |
|---|---|---|
| IAM user / long-term access keys | k01-mr(b), k02-mc(d), k04-mc(c), s01-mc(d), s02-mr(b), s03-mc(a), s03-mr(a), s05-mc(c), s06-mc(c) | 9 / 19 (47%) |
| Permissions boundary as the fix | k01-mc(b), k04-mc(d), s04-mr(c), s05-mc(b), s05-mr(d) | 5 / 19 (26%) |

### Distractor-type counts, after

| Type | Occurrences (question, choice) | Count |
|---|---|---|
| IAM user / long-term access keys | k04-mc(c), s02-mr(b), s03-mc(a) | 3 / 19 (16%) |
| Permissions boundary as the fix | k04-mc(d), s04-mr(c), s05-mr(d) | 3 / 19 (16%) |

Kept per the plan's "most instructive wrong answer" rule: `k04-mc(c)` (IAM user + baked keys for a Lambda function — tests workload-identity least privilege directly), `s02-mr(b)` (keys baked into an AMI — the exact anti-pattern instance profiles replace), `s03-mc(a)` (IAM user handed to a third party — ties the confused-deputy question to why long-term keys are also the wrong shape there). Boundary kept at `k04-mc(d)`, `s04-mr(c)`, `s05-mr(d)` — each teaches a different reason a boundary can't do the job (never shrinks; misses root/new accounts; can't grant cross-account).

### Replacements (6 IAM-user + 2 boundary), each a real AWS feature that fails one stated requirement

| Question | Choice | Before | After | Why it's wrong (new rationale, condensed) | Doc URL |
|---|---|---|---|---|---|
| k01-mc | b | "Set a permissions boundary that allows only the two Regions on every IAM role that developers create in the member accounts" | "Add a resource-based policy to every new resource that denies requests from outside the two Regions" | Real per-resource mechanism, but it has to be added to every new resource as it's created — the ongoing effort the stem explicitly asks to minimize — and it still doesn't stop root or an admin from creating a resource in the wrong Region in the first place | https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_evaluation-logic.html |
| k01-mr | b | "Create an IAM user with access keys in each member account and store the 30 key pairs in the scanner's configuration" | "Register the security account as an AWS Organizations delegated administrator, since that alone lets it read resources in every member account" | Delegated administrator status registers a member account as administrator for one **compatible AWS service's** own organization-wide feature; it does not by itself grant the security account's role any IAM permission to read resources via a general-purpose scanner | https://docs.aws.amazon.com/organizations/latest/userguide/orgs_integrate_delegated_admin.html |
| k02-mc | d | "Create IAM users with console passwords and MFA in one central account and let them switch roles into the other accounts" | "Enable IAM Identity Center as an account instance, without enabling AWS Organizations, and assign permission sets from there" | An account instance supports only the single account it runs in; multi-account permission sets and the shared access portal require an organization instance, enabled in the Organizations management account | https://docs.aws.amazon.com/singlesignon/latest/userguide/identity-center-instances.html |
| s01-mc | d | "Create one shared IAM user with AdministratorAccess for the team and give the script that user's access keys" | "Turn on IAM Access Analyzer external access findings to monitor the root user's activity, and leave the backup script using the root access key" | External access findings flag resource-based policies shared outside the account/organization; they do not monitor root user API activity and don't remove the root key the script still uses | https://docs.aws.amazon.com/IAM/latest/UserGuide/access-analyzer-findings.html |
| s03-mr | a | "Create IAM users for the release engineers in the production account and require MFA on each user" | "In development, add a trust policy to the engineers' role that names the production deployment role as a trusted entity" | A trust policy belongs on the role being assumed (in production), not on the role doing the assuming (in development); this doesn't grant `sts:AssumeRole` and production still has no role trusting development | https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_terms-and-concepts.html |
| s05-mc | b | "A permissions boundary on account A's administrator role that includes s3:GetObject for the account B role" | "Use AWS DataSync to copy the bucket's objects into a bucket in account B" | DataSync copies data between locations; it doesn't grant account B's role permission to read the *original* bucket, which is what the role's identity-based policy already targets | https://docs.aws.amazon.com/datasync/latest/userguide/what-is-datasync.html |
| s05-mc | c | "A new IAM user in account A with S3 read access, created for the analytics team in account B" | "Add a bucket ACL that grants read access to account B's AWS account" | An ACL grants access to the whole AWS account, not to the specific role's ARN, and new S3 buckets default to Bucket owner enforced, which disables ACLs entirely | https://docs.aws.amazon.com/AmazonS3/latest/userguide/about-object-ownership.html |
| s06-mc | c | "IAM users whose names match the AD accounts, with a script that copies AD password changes into IAM" | "Create an Amazon Cognito user pool configured as a SAML service provider for AD FS, and use it for console sign-in" | A Cognito user pool authenticates users of your own application and issues its own tokens; configuring it as a SAML service provider still doesn't sign users into the AWS Management Console | https://docs.aws.amazon.com/cognito/latest/developerguide/cognito-user-identity-pools.html |

Every changed rationale explains the new distractor by name (no letter references), and every new claim above was checked live against `docs.aws.amazon.com` before writing it (delegated administrator, S3 Object Ownership defaults, and the confused-deputy mechanics were re-fetched in full; Identity Center instance types, Access Analyzer findings, and IAM trust-policy placement reuse facts already verified in the lesson's existing citations).

New distractor types introduced by the replacements above are each a singleton (1 occurrence), well under the 3-question cap: resource-policy-per-resource, delegated-admin-alone, account-instance-vs-org-instance, external-access-monitors-root, trust-policy-on-wrong-side, DataSync-copy, S3-ACL-account-level, Cognito-user-pool-for-console.

## 5. Checks

- **Distractor-type counts:** IAM user/keys 3/19 (16%); permissions boundary 3/19 (16%). Both ≤ 3, per the plan's cap.
- **Longest-is-key rate (MC only):** 1/11 = 9.1% (well under the 35% ceiling). MC questions: k01-mc, k02-mc, k03-mc, k04-mc, k05-mc, s01-mc, s02-mc, s03-mc, s04-mc, s05-mc, s06-mc.
- **Letter references in rationale:** 0 across all 19 questions (regex over `\(choice x\)` / `\bchoice x\b` patterns and bare `(a)`–`(e)` forms).
- **Single-asterisk spans in lesson-1-1:** 0 (was 9).
- **`selectCount` / key / objective IDs:** unchanged for all 19 questions — only `choices[].text` and `rationale` (and `citationIds` where a new fact needed one) were touched, plus the s02-mr stem.
- **`python scripts\content_lint.py`:** PASS (429 questions: aws 310, tf 119; labs 21+21; lessons 23).
- **`mcpStatus`/`reviewedOn`:** left as `"verified"` / `"2026-09-26"` on every touched question (facts re-verified above; no question's key changed).

## 6. Doc URLs used

- https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles.html (s02-mr stem)
- https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies_boundaries.html (K01)
- https://docs.aws.amazon.com/singlesignon/latest/userguide/manage-your-identity-source-idp.html (K02)
- https://docs.aws.amazon.com/singlesignon/latest/userguide/identity-center-instances.html (K02, de-federation, k02-mc)
- https://docs.aws.amazon.com/IAM/latest/UserGuide/access-analyzer-findings.html (K04, s01-mc)
- https://docs.aws.amazon.com/awssupport/latest/user/security-checks.html#iam-access-key-rotation (K04)
- https://docs.aws.amazon.com/IAM/latest/UserGuide/access-analyzer-policy-generation.html (K04)
- https://docs.aws.amazon.com/IAM/latest/UserGuide/root-user-best-practices.html (S01)
- https://docs.aws.amazon.com/IAM/latest/UserGuide/confused-deputy.html (S03)
- https://docs.aws.amazon.com/awscloudtrail/latest/userguide/creating-trail-organization.html (S04)
- https://docs.aws.amazon.com/singlesignon/latest/userguide/manage-your-identity-source-ad.html (S06, de-federation)
- https://docs.aws.amazon.com/organizations/latest/userguide/orgs_integrate_delegated_admin.html (k01-mr)
- https://docs.aws.amazon.com/AmazonS3/latest/userguide/about-object-ownership.html (s05-mc)
- https://docs.aws.amazon.com/datasync/latest/userguide/what-is-datasync.html (s05-mc)
- https://docs.aws.amazon.com/cognito/latest/developerguide/cognito-user-identity-pools.html (s06-mc)
- https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_terms-and-concepts.html (s03-mr)
- https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_evaluation-logic.html (k01-mc)

## Learning content affected

Yes: lesson, 19 questions, and one exercise. Per AGENTS.md, this batch needs Teacher (and, for the lesson accuracy items, AWS) re-validation before it is considered closed, per the round-4 reports' item verdicts.
