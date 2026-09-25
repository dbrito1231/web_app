# Amendment 2, batch F12: round-5 Teacher/AWS fixes to lesson 1.1 and its 19 questions

Batch F12 per `.cursor/plans/lead_dev_fix_loop_round2_20260926.plan.md` ("Amendment 2"), closing the items in `reports/fix-loop-r2/round-5/TEACHER.md` and `reports/fix-loop-r2/round-4b/AWS-lesson-pilot.md`. Files touched: `content/lessons/lesson-1-1.json`; `content/questions/q-saa-1-1-{k01-mc,k01-mr,k02-mc,s01-mc,s01-mr,s03-mr,s05-mc,s05-mr,s06-mc}.json`; new citations `content/citations/cite-saa-1-1-{s3-acl-permissions,idc-account-instances}.json`. No other files edited (`backend/workbook/content_loader.py` and `scripts/content_lint.py` show as modified in `git status` from other agents' concurrent work, not from this batch).

`python scripts\content_lint.py`: **PASS** (429 questions: aws 310, tf 119; labs 21+21; lessons 23).

## 1. TEACHER-R5-001 — "IAM group as the fix" over the 3/19 cap

### Distractor-type count, before

| Question / choice | Text (abridged) |
|---|---|
| k01-mr(e) | "Create an IAM group with the ReadOnlyAccess managed policy... add each auditor's IAM user" |
| s02-mc(b) | "Create a parent IAM group that contains the three team groups" (kept — objective is groups) |
| s02-mr(e) | "Add the EC2 instances to an IAM group..." (kept — objective is groups) |
| s03-mr(e) | "Add the development account's release role to an IAM group in the production account" |
| s05-mr(e) | "Create an IAM group in account A, add account B's role to it, and attach the needed permissions" |

Count: **5/19 (26%)**, over the ≤3 cap.

### Fix

- **q-saa-1-1-k01-mr(e)**, before → after:
  - Before: "Create an IAM group with the ReadOnlyAccess managed policy in the management account and add each auditor's IAM user to it"
  - After: "Create an organization trail in the management account and give the auditors direct read access to its S3 log bucket, instead of connecting IAM Identity Center to the corporate IdP"
  - Rationale tail replaced with: an organization trail only centralizes API logs; it does not authenticate people or grant resource access, and reading a log bucket is not sign-in through the corporate IdP, so it fails the auditors'-access requirement even though it is a real, correctly described feature.
  - Added citation `cite-saa-1-1-org-trail` (existing file, `creating-trail-organization.html`).
- **q-saa-1-1-s05-mr(e)**, before → after:
  - Before: "Create an IAM group in account A, add account B's role to it, and attach the needed permissions"
  - After: "Create a role in account A that trusts account B's role, and have the account B role call sts:AssumeRole on it before invoking the function and sending the messages"
  - Rationale tail replaced with: this is a common cross-account pattern, but the stem explicitly rules it out ("without assuming a role in account A"), and the account B role's own identity-based policy already reaches the function/queue directly once the two resource-based policies (the actual key) are in place.
  - Citations: dropped `cite-saa-1-1-groups` (no longer relevant), added `cite-saa-1-1-xacct-tutorial`.

### Distractor-type count, after

Only `s02-mc(b)`, `s02-mr(e)`, `s03-mr(e)` remain (all three where IAM groups are the tested objective, per the instruction to keep s02-mc/s02-mr). **3/19 (16%)** — within the ≤3 cap. Verified with a script scanning every non-key choice for "IAM group".

## 2. TEACHER-R5-002 / AWS-R5-002 — s05-mc ACL rationale

- **Before:** "A bucket ACL, even where still enabled, grants access to the whole AWS account rather than to the specific role's ARN, and new S3 buckets default to the Bucket owner enforced setting, which disables ACLs entirely; a bucket policy is the supported way to scope resource-based access to one caller's ARN."
- **After:** "A bucket ACL granting READ to account B's AWS account is not the fix: on a bucket, READ allows the grantee only to list the objects (s3:ListBucket), not to read their data (s3:GetObject), so it would not satisfy this request even if it were the only problem; new S3 buckets also default to the Bucket owner enforced setting, which disables ACLs entirely and means AWS access-management policies, not ACLs, control access. A bucket policy is the supported way to scope resource-based access to one caller's ARN."
- Doc URL: https://docs.aws.amazon.com/AmazonS3/latest/userguide/acl-overview.html — fetched 2026-09-26. Confirmed table: "READ | When granted on a bucket: Allows grantee to list the objects in the bucket | When granted on an object: Allows grantee to read the object data and its metadata" and the ACL→policy mapping "READ [bucket] → s3:ListBucket, s3:ListBucketVersions, s3:ListBucketMultipartUploads" vs. "READ [object] → s3:GetObject, s3:GetObjectVersion".
- New citation `cite-saa-1-1-s3-acl-permissions` added (added to the question and to the lesson).
- **Lesson S05** gained one new sentence after the resource-based-policy services list: "Amazon S3 also has an older, separate mechanism, the **bucket ACL**: even when enabled, a bucket-level READ grant allows the grantee only to list the objects (`s3:ListBucket`), not to read them (`s3:GetObject`), and new buckets default to **Bucket owner enforced**, which disables ACLs entirely — a bucket policy is the modern, supported way to grant this kind of cross-account access."

## 3. TEACHER-R5-005 / AWS-R5-001 — k02-mc choice d + rationale

- **Choice d before:** "Enable IAM Identity Center as an account instance, without enabling AWS Organizations, and assign permission sets from there" (internally inconsistent — stem already has the 12 accounts "in one organization").
- **Choice d after:** "Enable an account instance of IAM Identity Center in one of the 12 member accounts and assign permission sets from there" (length padded slightly, see §7, to keep the key non-longest).
- **Rationale tail before:** "An account instance of Identity Center supports only the single account it runs in; assigning permission sets across the other 11 accounts and giving users one access portal to all of them requires an organization instance, enabled in the AWS Organizations management account." (false: account instances support **no** permission sets/account access at all, not even their own account).
- **Rationale tail after:** "Account instances support only application assignments; multi-account permissions and portal access to AWS accounts need an organization instance."
- Doc URL: https://docs.aws.amazon.com/singlesignon/latest/userguide/account-instances-identity-center.html — fetched 2026-09-26. Quote: "Account instances do not support permission sets and therefore do not support access to AWS accounts." Also: "Account instances are bound to a single AWS account and are used only to manage user and group access for supported applications in the same account."
- New citation `cite-saa-1-1-idc-account-instances` added (question + lesson).

## 4. TEACHER-R5-003 — delegated administrator, never explained in the lesson

Added to lesson **S04**, right after the existing sentence "...only the management account (or a delegated administrator) can [stop/delete/change the org trail].":

> "Registering a delegated administrator gives a member account admin rights for one specific service plus read-only Organizations actions; it grants no general IAM access to other accounts."

Doc URL: https://docs.aws.amazon.com/organizations/latest/userguide/orgs_integrate_delegated_admin.html — re-fetched 2026-09-26. Quote: "By registering a member account as a delegated administrator for an AWS service you enable that account to have some administrative permissions for that service, as well as permissions for Organizations read-only actions." (read-only action list: `DescribeAccount`, `ListAccounts`, etc. — no IAM/resource-read permissions in other accounts.) Uses the existing citation `cite-saa-1-1-org-delegated-admin`, already on the lesson's list.

## 5. TEACHER-R5-004 — k01-mc rationale, resource-based-policy distractor

- **Before:** "Resource-based policies would have to be added to every new resource individually as it is created, which is exactly the ongoing administrative burden the design is trying to avoid, and they still do not stop an administrator or the root user from creating a resource in a disallowed Region in the first place."
- **After:** "Resource-based policies control access to a resource that already exists, not where a resource can be created, and many resource types, including EC2 instances and RDS DB instances, do not support them at all; even where a service does support them, a policy would have to be added to every new resource individually as it is created, which is exactly the ongoing administrative burden the design is trying to avoid, and it still would not stop an administrator or the root user from creating a resource in a disallowed Region in the first place."
- Doc URL: https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies_identity-vs-resource.html — re-fetched 2026-09-26. Quote: "Resource-based policies are attached to a resource. For example, you can attach resource-based policies to Amazon S3 buckets, Amazon SQS queues, VPC endpoints, AWS Key Management Service encryption keys, Amazon DynamoDB tables and streams, and AWS Sign-In resources." — EC2 instances and RDS DB instances are absent from every AWS list of resource-based-policy-capable services. Reused existing citation `cite-saa-1-1-identity-vs-resource` (already on the question).

## 6. TEACHER-R5-006 — s01-mc choice d

- **Before:** "Turn on IAM Access Analyzer external access findings to monitor the root user's activity, and leave the backup script using the root access key" (wrong for both findings, self-evidently wrong, 143-char length outlier).
- **After:** "Move the script to an IAM role, delete the root access key, and set the account password policy to require MFA."
- **Rationale tail before:** "External access findings flag resource-based policies that share access with a principal outside your account or organization; they do not monitor root user API activity, and turning them on does not remove the root access key that the backup script still uses."
- **Rationale tail after:** "Moving the script to a role and deleting the root access key correctly fixes the access-key finding, but setting the account password policy to require MFA does not fix the other finding: the IAM password policy controls password length, complexity, expiration, and reuse, has no MFA setting, and does not apply to the root user, so the root user still has no MFA device registered."
- Doc URL: https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_passwords_account-policy.html — fetched 2026-09-26. Quote: "The IAM password policy does not apply to the AWS account root user password or IAM user access keys." Password-policy options list (length, character mix, expiration, reuse) has no MFA setting.
- Citations: dropped `cite-saa-1-1-aa-external` (no longer referenced), added `cite-saa-1-1-pw-policy` (existing file, already used on `q-saa-1-1-s01-mr`).

## 7. TEACHER-R5-007 — imperative choices fixed to noun phrases

| Question / choice | Before | After |
|---|---|---|
| s05-mc(b) | "Use AWS DataSync to copy the bucket's objects into a bucket in account B" | "An AWS DataSync task that copies the bucket's objects into a bucket in account B" |
| s05-mc(c) | "Add a bucket ACL that grants read access to account B's AWS account" | "A bucket ACL that grants read access to account B's AWS account" |
| s06-mc(c) | "Create an Amazon Cognito user pool configured as a SAML service provider for AD FS, and use it for console sign-in" | "An Amazon Cognito user pool configured as a SAML service provider for AD FS, used for console sign-in" |

## 8. TEACHER-R5-008 — s06-mc's two Cognito distractors

- **Choice (a) before:** "An Amazon Cognito identity pool that accepts AD FS assertions and exchanges them for IAM role credentials."
- **Choice (a) after:** "An AD Connector directory pointing to the on-premises Active Directory, without connecting IAM Identity Center or any SAML provider to it."
- **Rationale sentence before:** "A Cognito identity pool issues AWS credentials to users of your web or mobile app; it does not provide single sign-on to the AWS Management Console."
- **Rationale sentence after:** "AD Connector is a directory gateway that redirects authentication requests straight through to the existing on-premises Active Directory without caching anything in the cloud; on its own it does not sign users into the AWS Management Console or map AD groups to permissions, so this single AWS account still needs a federation front end such as the IAM SAML provider above to reach the console."
- Doc URL: https://docs.aws.amazon.com/directoryservice/latest/admin-guide/directory_ad_connector.html — re-fetched 2026-09-26. Quote: "AD Connector is a directory gateway with which you can redirect directory requests to your on-premises Microsoft Active Directory without caching any information in the cloud." Console access is listed as a benefit achieved "through IAM role-based access" — i.e., via a federation front end, not from AD Connector alone. Reused existing citation `cite-saa-1-1-ad-connector` (added to this question).
- Choice (c), the remaining Cognito distractor (user pool as SAML SP), is unchanged in substance (only reworded to a noun phrase, §7).

## 9. Optional nits (all applied)

- **s03-mr(a):** "In development, add a trust policy to the engineers' role..." → "In development, edit the trust policy of the engineers' role...". Rationale updated to match: "...every role already has exactly one trust policy, and editing the one on the development-side role does not grant it permission to call sts:AssumeRole...".
- **Lesson K02:** "with users and groups provisioned by SCIM" → "with users and groups usually provisioned by SCIM".
- **s01-mr(e):** "Move developers to IAM Identity Center so that..." → "Move developers to IAM Identity Center, with MFA required, so that...".

## Verification

Ran a scratch script (`verify_f12.py`) over all 19 `q-saa-1-1-*.json` files after edits:

- **Distractor-type recount ("IAM group"):** 3/19 (16%) — down from 5/19 (26%). List: `s02-mc(b)`, `s02-mr(e)`, `s03-mr(e)`.
- **Longest-is-key (11 MC questions):** 1/11 (9.1%) — unchanged from round 5 (the one case, `k05-mc`, is untouched by this batch and was already the state before). `k02-mc`'s new choice `d` was initially a two-way tie with the key at 118 chars; padded to 120 chars ("in one of the 12 member accounts") so the key (`a`, 118 chars) is no longer tied-longest.
- **Letter references** (`choice (a)`, `option b`, `answer d`, etc.) across every stem/choice/rationale: **0 found**.
- **Single-asterisk spans** in the 19 questions and in `lesson-1-1.json`'s `bodyMarkdown`: **0 found** (the lesson's one `##` heading line is pre-existing, outside this batch's scope, and is a level-2 title, not body content, so the "only `###`/`####`" rule reads as applying to the body sections, consistent with round-4/5 practice).
- **Teach-before-test:** every new/changed distractor concept is already covered in `lesson-1-1.json`: AD Connector alone (S06), organization trail (S04), cross-account role trust + `sts:AssumeRole` (S03), bucket ACL READ = list-only (new S05 sentence), account instances not supporting permission sets (K02 + new citation), IAM password policy having no MFA setting (S01).
- **Citation resolution:** every `citationId` referenced by the 19 questions and the lesson resolves to a file in `content/citations/` (61 files total, 2 new).
- `selectCount` matches `correctAnswerIds` length on all 19 questions; no `correctAnswerIds` changed in this batch.
- `python scripts\content_lint.py`: **PASS**.

## Files changed

- `content/lessons/lesson-1-1.json` (K02 SCIM wording; S04 delegated-admin sentence; S05 ACL sentence; 2 new citationIds)
- `content/questions/q-saa-1-1-k01-mc.json` (rationale only)
- `content/questions/q-saa-1-1-k01-mr.json` (choice e, rationale, citationIds)
- `content/questions/q-saa-1-1-k02-mc.json` (choice d, rationale, citationIds)
- `content/questions/q-saa-1-1-s01-mc.json` (choice d, rationale, citationIds)
- `content/questions/q-saa-1-1-s01-mr.json` (choice e wording nit)
- `content/questions/q-saa-1-1-s03-mr.json` (choice a + rationale wording nit)
- `content/questions/q-saa-1-1-s05-mc.json` (choices b/c wording, rationale, citationIds)
- `content/questions/q-saa-1-1-s05-mr.json` (choice e, rationale, citationIds)
- `content/questions/q-saa-1-1-s06-mc.json` (choices a/c, rationale, citationIds)
- `content/citations/cite-saa-1-1-s3-acl-permissions.json` (new)
- `content/citations/cite-saa-1-1-idc-account-instances.json` (new)

No keys (`correctAnswerIds`), `selectCount`, question/lesson IDs, or `objectiveIds` were changed. All edits kept `mcpStatus: "verified"` and `reviewedOn: "2026-09-26"` as they were already on the pre-existing 19 files.

**Status:** implementation done, pending Teacher and AWS re-validation per the Amendment-2/AGENTS.md content-impact flow.
