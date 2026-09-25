# Fix-loop round 5 (round-4b): AWS Solutions Architect re-review of lesson 1.1, the 19 questions, and de-federation

Reviewer: Senior AWS Solutions Architect (read-only). Date: 2026-09-25.
Scope: commit `f7b6f98` (change log `reports/fix-loop-r2/amendment-2/impl-F8.md`):
- `content/lessons/lesson-1-1.json`;
- all 19 `content/questions/q-saa-1-1-*.json` (8 replaced distractors, the s02-mr stem);
- `content/exercises/de-federation.json`;
- 6 new citations.

Method:
- I read `git show f7b6f98` (word diff), then dumped all 19 questions (stem, choices, key, rationale).
- I checked every changed or added statement against live `docs.aws.amazon.com` pages with WebFetch on 2026-09-25. No AWS docs MCP was available.
- I ran `python scripts\content_lint.py` (read-only): **PASS** (429 questions; labs 21+21; lessons 23).
- No AWS calls were made. No file other than this report was written.

Pages fetched this round:
- Identity Center: instance types; account instances; external IdP identity source; Microsoft AD identity source;
- IAM: root user best practices; Access Analyzer findings; Access Analyzer policy generation; the confused deputy problem;
- CloudTrail: creating an organization trail;
- Organizations: delegated administrator;
- S3: Object Ownership; ACL overview;
- Cognito: user pools;
- DataSync: what is DataSync.

## 1. Verdict table: round-4 items

| ID | Sev (R4) | What changed | Verdict | Evidence | Doc URL |
|---|---|---|---|---|---|
| AWS-R4-001 | Medium | S04: "It covers every account in the organization, not selected OUs, and any account that later joins the organization is added to the trail automatically." | **Gone** | The doc says organization trails "log events for the management account and all member accounts in the organization". It also says: "If an AWS account is added to an organization, the organization trail ... [is] added ... and logging starts ... automatically." | https://docs.aws.amazon.com/awscloudtrail/latest/userguide/creating-trail-organization.html |
| AWS-R4-002 | Medium | K02: identity sources are now listed as "SAML 2.0, with users and groups provisioned by SCIM; Identity Center's own directory; or Active Directory, either self-managed through AD Connector or AWS Managed Microsoft AD". | **Gone** | The doc says Identity Center connects external IdPs "through the ... SAML 2.0 and ... SCIM protocols". It also connects "a self-managed directory in Active Directory ... or a directory in AWS Managed Microsoft AD". | https://docs.aws.amazon.com/singlesignon/latest/userguide/manage-your-identity-source-idp.html ; https://docs.aws.amazon.com/singlesignon/latest/userguide/manage-your-identity-source-ad.html |
| AWS-R4-003 | Low | K04: new unused access findings bullet, and the exam tip now names them. | **Gone** | The doc lists unused roles, "Unused IAM user access keys and passwords", and unused permissions "used by a role". It adds: "There are charges for unused access findings". | https://docs.aws.amazon.com/IAM/latest/UserGuide/access-analyzer-findings.html |
| AWS-R4-004 | Low | K04: policy generation now covers users or roles, up to 90 days, action-level vs service-level output, and the data event and `iam:PassRole` exclusions. | **Gone** | The doc says "IAM entity (user or role)" and "a time period of up to 90 days". It gives action-level output "for some AWS services" and service-level output otherwise. It says: "Data events not available". It also says `iam:PassRole` "is not tracked by CloudTrail". | https://docs.aws.amazon.com/IAM/latest/UserGuide/access-analyzer-policy-generation.html |
| AWS-R4-005 | Low | K01: "attach only to IAM users, groups, or roles (boundaries to users or roles), and neither can be attached to the root user". | **Gone** | Boundaries apply to "IAM entities (users or roles)". Neither policy type can be attached to the root user. | https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies_boundaries.html |
| AWS-R4-006 | Low | S01: root MFA is now required on all account types, and central root access management is recommended for organizations. | **Gone** | The doc says: "All AWS account types (standalone, management, and member accounts) require MFA to be configured for their root user". It also says: "we recommend removing root user credentials from member accounts". | https://docs.aws.amazon.com/IAM/latest/UserGuide/root-user-best-practices.html |
| AWS-R4-007 | Low | S03: the attacker is now "another customer of the same third party". | **Gone** | This matches the doc's cross-account scenario (steps 3–4) and its line "Even if another customer supplies Example Corp with your ARN...". | https://docs.aws.amazon.com/IAM/latest/UserGuide/confused-deputy.html |
| AWS-R4-008 | Medium | s02-mr stem: the keys are now "an IAM user's long-term access keys". | **Gone** | The doc says a role "does not have standard long-term credentials, such as a password or access keys". The stem no longer says otherwise. Key (a, c) is unchanged and still correct. | https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles.html |
| AWS-R4-009 | Low | de-federation: (1) "for each option" wording in the constraint and in r7; (2) the scenario now says "move users into AWS Managed Microsoft AD with no on-premises trust"; (3) a new constraint on the organization instance; plus a K02 clause. | **Gone** | See §4. The constraint "AWS Organizations enabled, with this account as the management account" matches the doc. A standalone account can create an organization instance, and an organization instance is "enabled in the AWS Organizations management account". | https://docs.aws.amazon.com/singlesignon/latest/userguide/identity-center-instances.html |

Round-4 optional nits, still open (non-blocking, not re-raised):
- k04-mr (d) still says "Turn on the ... check".
- s06-mr (e) still says "an AWS Directory Service directory".

## 2. Lesson 1.1: changed or added statements

**All 11 changed or added statements are accurate and current.** Nothing new is wrong.

| # | Section | Statement (abridged) | Verdict | Doc URL |
|---|---|---|---|---|
| 1 | K01 | Identity policies attach to users, groups, and roles; boundaries attach to users or roles; neither attaches to root. | Accurate | https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies_boundaries.html |
| 2 | K02 | Identity sources: SAML 2.0 + SCIM; the Identity Center directory; AD via AD Connector or AWS Managed Microsoft AD. | Accurate | https://docs.aws.amazon.com/singlesignon/latest/userguide/manage-your-identity-source-idp.html |
| 3 | K02 | Permission sets per account need an organization instance, enabled in the Organizations management account. | Accurate. The account instances page says: "Account instances do not support permission sets and therefore do not support access to AWS accounts." | https://docs.aws.amazon.com/singlesignon/latest/userguide/account-instances-identity-center.html |
| 4 | K04 | Policy generation: user or role; up to 90 days; action-level or service-level output; data events and PassRole not captured. | Accurate. "Data events ... not captured" is a fair summary of "does not identify action-level activity for data events". | https://docs.aws.amazon.com/IAM/latest/UserGuide/access-analyzer-policy-generation.html |
| 5 | K04 | Unused access findings: a paid analyzer that continuously flags unused roles, keys and passwords, and unused permissions on roles. | Accurate ("continuously monitors all IAM roles and users") | https://docs.aws.amazon.com/IAM/latest/UserGuide/access-analyzer-findings.html |
| 6 | K04 | The Trusted Advisor IAM Access Key Rotation check flags keys not rotated in 90 days; rotation does not shrink permissions. | Accurate (verified in R4) | https://docs.aws.amazon.com/awssupport/latest/user/security-checks.html#iam-access-key-rotation |
| 7 | K04 tip | "Shrink permissions based on evidence" means policy generation, unused access findings, or last accessed information. | Accurate | as 4–5 |
| 8 | S01 | Root MFA is required on standalone, management, and member accounts; in an organization, centrally manage root access and remove member root credentials. | Accurate | https://docs.aws.amazon.com/IAM/latest/UserGuide/root-user-best-practices.html |
| 9 | S03 | Confused deputy: another customer of the same third party supplies your ARN. | Accurate | https://docs.aws.amazon.com/IAM/latest/UserGuide/confused-deputy.html |
| 10 | S04 | The organization trail covers every account, not selected OUs, and adds joining accounts automatically. | Accurate. Opt-in Region nuances are out of scope. | https://docs.aws.amazon.com/awscloudtrail/latest/userguide/creating-trail-organization.html |
| 11 | S06 | The AD Connector "must be in the management or a delegated administrator account". | Accurate. The doc allows the management account, or the delegated admin account if one exists. | https://docs.aws.amazon.com/singlesignon/latest/userguide/manage-your-identity-source-ad.html |

The 9 `*italic*` to `**bold**` or plain-text changes are formatting only and change no facts.

## 3. Questions

### 3a. The 8 replaced distractors

| Question | Choice | Real feature, correctly described? | Wrong for the stated reason? | Second defensible answer? | Verdict | Doc URL |
|---|---|---|---|---|---|---|
| k01-mc | b: resource-based policy on every new resource denying other Regions | Yes | Yes. It is per-resource ongoing effort, and it cannot stop a resource being created in a disallowed Region. | No. SCP (c) is the only preventive, org-wide control that binds root. | **Approve** | https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_evaluation-logic.html |
| k01-mr | b: delegated administrator "alone" lets the security account read everything | Yes. The doc says delegated admin gives "some administrative permissions for that service, as well as permissions for Organizations read-only actions". | Yes | No. Note: an AWS Config delegated admin with an org aggregator can collect configurations. But "since that alone" plus a general-purpose scanner keeps (b) wrong, and (a) + (d) remain the unique pair. | **Approve** | https://docs.aws.amazon.com/organizations/latest/userguide/orgs_integrate_delegated_admin.html |
| k02-mc | d: Identity Center account instance, "without enabling AWS Organizations" | Partly. See **AWS-R5-001**. | Yes, it fails. But the rationale gives a **false reason**: it says an account instance "supports only the single account it runs in". In fact, account instances support no AWS account access at all. The choice text also says "without enabling AWS Organizations" when the stem says the 12 accounts are already "in one organization". | No | **Concerns** (AWS-R5-001) | https://docs.aws.amazon.com/singlesignon/latest/userguide/account-instances-identity-center.html |
| s01-mc | d: external access findings to "monitor" root, keep the root key | Yes. External access findings cover resource-based policies shared outside the zone of trust. | Yes. They do not monitor root activity, and the key stays. | No | **Approve** | https://docs.aws.amazon.com/IAM/latest/UserGuide/access-analyzer-findings.html |
| s03-mr | a: trust policy on the development role naming the production role | Yes. This is a common misconception about trust-policy placement. | Yes. A trust policy belongs on the assumed role, and this gives no `sts:AssumeRole` grant. | No. (b) + (d) are the unique pair. | **Approve** (nit: every role already has a trust policy, so "edit" is more precise than "add") | https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_terms-and-concepts.html |
| s05-mc | b: DataSync copy into account B | Yes. DataSync transfers "between AWS storage services", including S3. | Yes. It does not let the role read the original bucket, and the stem asks what to add so the existing request succeeds. | No | **Approve** | https://docs.aws.amazon.com/datasync/latest/userguide/what-is-datasync.html |
| s05-mc | c: bucket ACL granting read to account B | Yes. ACLs grant to an AWS account or a predefined group, and are disabled by default under Bucket owner enforced. | Yes, but the rationale's lead reason is weak. See **AWS-R5-002**: account B's role already has the identity-based half, so "account rather than role" is not why this fails. The decisive fact is missing: bucket-level READ "allows grantee to list the objects in the bucket" only (s3:ListBucket), not s3:GetObject. | No. ACLs are off by default, and a bucket READ grant never gives GetObject. | **Approve with nit** (AWS-R5-002) | https://docs.aws.amazon.com/AmazonS3/latest/userguide/acl-overview.html ; https://docs.aws.amazon.com/AmazonS3/latest/userguide/about-object-ownership.html |
| s06-mc | c: Cognito user pool as a SAML SP for AD FS, used for console sign-in | Yes. User pools accept SAML 2.0 assertions and act as an OIDC IdP "from the perspective of your app". | Yes. They sign users into your application, not the Management Console. | No | **Approve** | https://docs.aws.amazon.com/cognito/latest/developerguide/cognito-user-identity-pools.html |

### 3b. s02-mr and the keys of all 19 questions

- **s02-mr stem:** accurate now ("an IAM user's long-term access keys"). Key (a, c) is still the single best pair: instance profile + one customer managed policy.
- **All 19 keys re-checked:** each is correct and the single best answer.
  - k01-mc c; k01-mr a,d; k02-mc a; k03-mc d; k04-mc b; k04-mr b,e; k05-mc c;
  - s01-mc a; s01-mr c,e; s02-mc d; s02-mr a,c; s03-mc c; s03-mr b,d;
  - s04-mc a; s04-mr a,e; s05-mc d; s05-mr b,c; s06-mc b; s06-mr d,e.
- `correctAnswerIds` and `selectCount` are unchanged from R4.
- The new lesson text agrees with every key. For example, the S01 mandatory root MFA text supports s01-mc (a), and the S04 org trail text supports s04-mr (a).
- The s03-mc rationale ("on behalf of any customer who knows the ARN") is consistent with the corrected S03 lesson text.

## 4. de-federation accuracy

**Verdict: approve.**
- **(1) "For each option" wording (constraint and r7):** correct. AD Connector and per-account AD FS SAML both keep passwords on premises, and only AWS Managed Microsoft AD adds DCs in AWS. The wording no longer implies one option each.
- **(2) Scenario option "move users into AWS Managed Microsoft AD with no on-premises trust":** it now differs clearly from "connect ... AWS Managed Microsoft AD to IAM Identity Center" (trust or pass-through).
- **(3) Organization-instance constraint:** accurate.
  - "Account instances do not support permission sets and therefore do not support access to AWS accounts."
  - An organization instance is "An instance of IAM Identity Center that you enable in the AWS Organizations management account".
  - A standalone account can create an organization instance. That makes it the management account of a new organization, which matches "AWS Organizations enabled, with this account as the management account".
- The lesson K02 clause is consistent with the exercise.

Doc URLs:
- https://docs.aws.amazon.com/singlesignon/latest/userguide/identity-center-instances.html
- https://docs.aws.amazon.com/singlesignon/latest/userguide/account-instances-identity-center.html
- https://docs.aws.amazon.com/singlesignon/latest/userguide/manage-your-identity-source-ad.html

## 5. New issues

| ID | Severity | Location | Problem | Exact fix | Doc URL |
|---|---|---|---|---|---|
| AWS-R5-001 | Medium | `q-saa-1-1-k02-mc`, choice d and rationale | The rationale says an account instance "supports only the single account it runs in". That implies it can assign permission sets to its own account, which is false: "Account instances do not support permission sets and therefore do not support access to AWS accounts." This contradicts lesson K02 and the de-federation constraint. The choice says "without enabling AWS Organizations", but the stem already has 12 accounts "in one organization", so the choice is internally inconsistent. The key is unaffected. | **Choice d:** replace with "Enable an account instance of IAM Identity Center in one member account, connect the IdP to it, and assign permission sets from there". **Rationale:** replace the last sentence with "An account instance of Identity Center supports only applications in the account where it is created; it does not support permission sets, so it cannot give access to any AWS account, not even its own. Assigning permission sets across the 12 accounts and giving users one access portal to all of them requires an organization instance, enabled in the AWS Organizations management account." | https://docs.aws.amazon.com/singlesignon/latest/userguide/account-instances-identity-center.html |
| AWS-R5-002 | Low | `q-saa-1-1-s05-mc`, rationale for the bucket ACL distractor | The lead reason ("grants access to the whole AWS account rather than to the specific role's ARN") does not explain the failure. Account B's role already has the identity-based half, and ACL grants to an account are designed to be delegated onward. The decisive facts are that ACLs are disabled by default and that bucket-level READ allows listing only. | Replace the ACL sentence with "A bucket ACL is not the fix: new buckets default to Bucket owner enforced, which disables ACLs entirely, and even where ACLs are enabled, READ on a bucket only lets the grantee list the objects (s3:ListBucket), not read them (s3:GetObject). A bucket policy that names the role's ARN is the supported way to grant this access." Also add a citation for the ACL overview page (optional). | https://docs.aws.amazon.com/AmazonS3/latest/userguide/acl-overview.html |

Optional nit (non-blocking): in the s03-mr (a) choice text, "add a trust policy to" could read "edit the trust policy of", because every role already has exactly one trust policy. The rationale is correct as written.

Both fixes are content changes and need the AGENTS.md flow: a plan, then Teacher validation, then re-review. Neither changes a key.

## Overall: concerns

This is one Medium item (AWS-R5-001, rationale accuracy in k02-mc). All nine round-4 items are **Gone**. The lesson changes, the s02-mr stem, 6 of the 8 new distractors, and de-federation are accurate. Once AWS-R5-001 is fixed (and ideally AWS-R5-002), I expect to approve without another full review. A targeted check of those two files is enough.
