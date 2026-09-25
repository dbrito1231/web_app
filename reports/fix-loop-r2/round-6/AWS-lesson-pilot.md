# Fix-loop round 6: AWS Solutions Architect targeted re-check of lesson 1.1 and its 19 questions

Reviewer: Senior AWS Solutions Architect (read-only). Date: 2026-09-25/26.
Scope: commit `04cb6fb` (change log `reports/fix-loop-r2/amendment-2/impl-F12.md`), the fix for round-5 items in `reports/fix-loop-r2/round-4b/AWS-lesson-pilot.md` and `reports/fix-loop-r2/round-5/TEACHER.md`.

Method:
- Read `git show 04cb6fb` (full diff) and the current state of `content/lessons/lesson-1-1.json` and all 10 changed `content/questions/q-saa-1-1-*.json` files.
- Verified every changed/added statement against live `docs.aws.amazon.com` pages with WebFetch on 2026-09-26 (no AWS docs MCP available). No AWS calls were made. No file other than this report was written.
- Ran `python scripts\content_lint.py` (read-only): **PASS** (429 questions: aws 310, tf 119; labs 21+21; lessons 23).
- Confirmed the two new citation files (`cite-saa-1-1-s3-acl-permissions`, `cite-saa-1-1-idc-account-instances`) cite the exact URLs I independently fetched.

## 1. Verdict on the round-5 carry-over items

| ID | What was required | Verdict | Evidence |
|---|---|---|---|
| AWS-R5-001 | k02-mc choice d must not be internally inconsistent, and its rationale must not claim an account instance "supports only the single account it runs in" | **Gone** | Choice d now reads "Enable an account instance of IAM Identity Center in one of the 12 member accounts and assign permission sets from there" (no more "without enabling AWS Organizations"). Rationale now reads "Account instances support only application assignments; multi-account permissions and portal access to AWS accounts need an organization instance." This matches: "Account instances do not support permission sets and therefore do not support access to AWS accounts." |
| AWS-R5-002 | s05-mc ACL rationale must give the decisive S3 fact (bucket READ = list-only) instead of the weak "account vs. role" reasoning | **Gone** | Rationale now reads "...on a bucket, READ allows the grantee only to list the objects (s3:ListBucket), not to read their data (s3:GetObject)... new S3 buckets also default to Bucket owner enforced, which disables ACLs entirely..." This matches the ACL-overview permission table and the ACL→policy-action mapping table exactly. |

Both are confirmed **Gone**.

## 2. Changed/added statements and their doc URLs

| # | Location | Statement (abridged) | Doc URL | Verdict |
|---|---|---|---|---|
| 1 | Lesson K02 | "usually provisioned by SCIM" (wording nit, no factual change) | https://docs.aws.amazon.com/singlesignon/latest/userguide/manage-your-identity-source-idp.html | Accurate |
| 2 | Lesson S04 | Delegated administrator "gives a member account admin rights for one specific service plus read-only Organizations actions; it grants no general IAM access to other accounts." | https://docs.aws.amazon.com/organizations/latest/userguide/orgs_integrate_delegated_admin.html | Accurate. Doc: "you enable that account to have some administrative permissions for that service, as well as permissions for Organizations read-only actions." The read-only action list (`DescribeAccount`, `ListAccounts`, etc.) grants no IAM/resource access in other accounts. |
| 3 | Lesson S05 | New sentence: bucket ACL, even enabled, gives READ = list only (`s3:ListBucket`), not `s3:GetObject`; Bucket owner enforced (default on new buckets) disables ACLs entirely. | https://docs.aws.amazon.com/AmazonS3/latest/userguide/acl-overview.html | Accurate. Confirmed against the permissions table and the ACL→policy-action mapping table. |
| 4 | k01-mc rationale | Resource-based policies "control access to a resource that already exists, not where a resource can be created, and many resource types, including EC2 instances and RDS DB instances, do not support them at all." | https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies_identity-vs-resource.html | Accurate. The doc's supported-service list ("S3 buckets, SQS queues, VPC endpoints, KMS keys, DynamoDB tables and streams, and AWS Sign-In resources") does not include EC2 or RDS. |
| 5 | k01-mr(e) | New distractor: "Create an organization trail... and give the auditors direct read access to its S3 log bucket, instead of connecting IAM Identity Center to the corporate IdP." | https://docs.aws.amazon.com/awscloudtrail/latest/userguide/creating-trail-organization.html (re-used, verified round 4/5) | Accurate and correctly wrong: a log bucket read grant is not SSO through the corporate IdP. |
| 6 | k02-mc choice d + rationale | See §1 (AWS-R5-001). | https://docs.aws.amazon.com/singlesignon/latest/userguide/account-instances-identity-center.html | Accurate |
| 7 | s01-mc choice d + rationale | "the IAM password policy controls password length, complexity, expiration, and reuse, has no MFA setting, and does not apply to the root user" | https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_passwords_account-policy.html | Accurate. Doc: "The IAM password policy does not apply to the AWS account root user password or IAM user access keys." The custom-policy option list has no MFA setting. |
| 8 | s01-mr(e) | "Move developers to IAM Identity Center, with MFA required..." (wording nit) | https://docs.aws.amazon.com/singlesignon/latest/userguide/... (Identity Center overview, verified prior rounds) | Accurate |
| 9 | s03-mr(a) + rationale | "edit the trust policy of the engineers' role" (wording nit); rationale: "every role already has exactly one trust policy" | https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_terms-and-concepts.html (re-used) | Accurate |
| 10 | s05-mc choices b/c (noun-phrase wording) + rationale | See §1 (AWS-R5-002) and the DataSync distractor (unchanged in substance). | https://docs.aws.amazon.com/datasync/latest/userguide/what-is-datasync.html ; https://docs.aws.amazon.com/AmazonS3/latest/userguide/acl-overview.html | Accurate |
| 11 | s05-mr(e) | New distractor: "Create a role in account A that trusts account B's role, and have the account B role call sts:AssumeRole on it..." | https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_use.html (cross-account tutorial, re-used) | Accurate and correctly wrong: the stem explicitly rules out assuming a role in account A, and the account B role's own identity-based policy already reaches the resources once the two resource-based policies are added. |
| 12 | s06-mc choice a + rationale | "An AD Connector directory pointing to the on-premises Active Directory, without connecting IAM Identity Center or any SAML provider to it." Rationale: AD Connector "redirects authentication requests straight through to the existing on-premises Active Directory without caching anything in the cloud; on its own it does not sign users into the AWS Management Console..." | https://docs.aws.amazon.com/directoryservice/latest/admin-guide/directory_ad_connector.html | Accurate. Doc: "AD Connector is a directory gateway with which you can redirect directory requests to your on-premises Microsoft Active Directory without caching any information in the cloud." Console access is listed as a benefit reached "through IAM role-based access" (i.e., needs a federation front end), consistent with the choice excluding IAM Identity Center/SAML. |
| 13 | s06-mc choice c (noun-phrase wording only) | No factual change from round 5 (already approved). | https://docs.aws.amazon.com/cognito/latest/developerguide/cognito-user-identity-pools.html | Accurate |

## 3. Keys of all 19 `q-saa-1-1-1-*` questions

Round 5 verified all 19 keys as correct and the single best answer, and confirmed `correctAnswerIds`/`selectCount` were unchanged there. This round's diff (commit `04cb6fb`) touches choice text and rationale only — no `correctAnswerIds` or `selectCount` field is present in the diff for any of the 10 changed files, which I confirmed by re-reading every changed file in full:

- k01-mc: key **c** unchanged, still correct (SCP binds root/admins org-wide, least ongoing effort).
- k01-mr: key **a, d** unchanged. The new distractor (e) is a plausible-sounding, clearly wrong third option — not a second defensible answer, since an org trail is not authentication/SSO.
- k02-mc: key **a** unchanged, still correct and still the single best answer. New choice d is a real feature (account instance) that genuinely cannot do what the stem needs (permission sets), so it is not a second defensible answer.
- s01-mc: key **a** unchanged. New choice d (role + delete key + password-policy MFA requirement) is a partial fix dressed as a full fix — the rationale correctly explains the gap (no MFA option in the password policy, doesn't touch root) — not a second defensible answer.
- s01-mr: key **c, e** unchanged (wording nit only on e).
- s03-mr: key **b, d** unchanged (wording nit only on a).
- s05-mc: key **d** unchanged. Choice c (ACL) remains wrong for the corrected, decisive reason (list-only + ACLs disabled by default); choice b (DataSync) remains wrong (copies data, doesn't grant read on the original bucket). Neither is a second defensible answer.
- s05-mr: key **b, c** unchanged. New distractor e (role-in-A + AssumeRole) is a real, common cross-account pattern but is explicitly excluded by the stem's "without assuming a role in account A" — correctly wrong, not a second defensible answer.
- s06-mc: key **b** unchanged. New choice a (AD Connector alone) and unchanged choice c (Cognito user pool) are both correctly wrong for stated reasons; neither reaches the console without a federation front end (SAML/Identity Center), so neither is a second defensible answer.

All other 10 of the 19 questions (k03-mc, k04-mc, k04-mr, k05-mc, s02-mc, s02-mr, s03-mc, s04-mc, s04-mr, s06-mr) are untouched by this commit; their keys were already verified in round 5 and nothing in this diff affects them.

## 4. New issues

None found. No AWS-R6-### items are raised.

## 5. Closure line

**Lesson 1.1 + task 1.1 questions: close**

## Overall: approve

Both carry-over items (AWS-R5-001, AWS-R5-002) are confirmed gone. Every changed or added statement in commit `04cb6fb` — the S04 delegated-administrator sentence, the S05 ACL sentence, the K02 wording nit, the new/changed distractors (k01-mr(e), s05-mr(e), s01-mc(d), s06-mc(a)), and every changed rationale — checks out against current official AWS documentation. All 19 keys remain correct and the single best (or exact) answer, with no new distractor rising to a second defensible answer. `python scripts\content_lint.py` passes.
