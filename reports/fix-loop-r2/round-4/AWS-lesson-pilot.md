# Fix-loop round 4: AWS Solutions Architect review of lesson 1.1, the pilot fixes, and de-federation

Reviewer: Senior AWS Solutions Architect (read-only). Date: 2026-09-25.
Scope: commit `448e17d` (change log `reports/fix-loop-r2/amendment-2/impl-F7.md`):
- `content/lessons/lesson-1-1.json` (bodyMarkdown);
- `content/questions/q-saa-1-1-{k04-mr,s02-mr,s06-mr}.json`;
- `content/exercises/de-federation.json`;
- the 4 new citations.

Method:
- I read the whole lesson and split it into atomic technical statements.
- I checked each statement against live `docs.aws.amazon.com` pages with WebFetch on 2026-09-25. No AWS docs MCP was available.
- Where round-1 pilot checks already covered a page (`reports/fix-loop-r2/q1-pilot/AWS.md`), I re-fetched it only if the lesson words the claim differently.
- No AWS calls were made. No file other than this report was written.

Pages fetched this round:
- SCPs, permissions boundaries, and Access Analyzer policy generation and findings;
- last accessed information;
- Identity Center identity sources: overview, external IdP, and AD;
- Identity Center instance types;
- the organization trail;
- root user best practices;
- the MFA self-manage example policy;
- Simple AD;
- Lambda cross-account access;
- Control Tower;
- Local Zones;
- the third-party external ID page;
- Trusted Advisor security checks (IAM Access Key Rotation).

## 1. Lesson 1.1: statement-by-statement findings (problems only)

**Statements verified: 98.** 90 are accurate and current as written. The 8 below need a change: 2 are Medium and 6 are Low. None of them affects a question key.

| # | Section | Lesson statement (abridged) | Problem | Severity | Doc URL |
|---|---|---|---|---|---|
| L1 | S04 | "Accounts placed under a covered OU are picked up automatically." | **Wrong.** An organization trail is not scoped to OUs. It "logs events for the management account and all member accounts in the organization". "If an AWS account is added to an organization, the organization trail ... [is] added to that AWS account, and logging starts ... automatically." The OU wording mixes up the trail with SCP inheritance, and a student may believe accounts outside some OU escape the trail. | Medium (AWS-R4-001) | https://docs.aws.amazon.com/awscloudtrail/latest/userguide/creating-trail-organization.html |
| L2 | K02 | Identity Center identity source: "an external IdP over SAML/OIDC, Identity Center's own directory, or AWS Managed Microsoft AD" | **Wrong protocol and an incomplete list.** Identity Center connects external IdPs "through ... SAML 2.0 and ... SCIM". OIDC is not a way to connect an identity source. The AD option is "a self-managed directory in Active Directory or ... AWS Managed Microsoft AD", and self-managed AD is reached through AD Connector. Leaving out AD Connector here also contradicts S06. | Medium (AWS-R4-002) | https://docs.aws.amazon.com/singlesignon/latest/userguide/manage-your-identity-source-idp.html ; https://docs.aws.amazon.com/singlesignon/latest/userguide/manage-your-identity-source.html |
| L3 | K04 exam tip | "'shrink permissions based on evidence' means Access Analyzer policy generation or last accessed information" | **Misleading by omission (currency).** Access Analyzer **unused access findings** exist to do exactly this. They report unused roles, unused access keys and passwords, and "Unused permissions – service-level and action-level permissions that weren't used by a role". The lesson presents Access Analyzer only as external access findings, and the exam tip is an exclusive "means X or Y". On the real exam, "IAM Access Analyzer unused access" can be the correct answer. The lesson line "external access findings ... say nothing about whether a role's own permissions are oversized" is correct. | Low (AWS-R4-003) | https://docs.aws.amazon.com/IAM/latest/UserGuide/access-analyzer-findings.html |
| L4 | K04 | Policy generation "reads a role's CloudTrail activity over a chosen period and drafts a policy containing only the actions actually used" | **Imprecise.** It works for IAM users as well as roles, and the period is up to 90 days. Action-level output exists only "for some AWS services". For other services it gives service-level output and prompts you to add actions. It does not identify data events, and it does not track `iam:PassRole`. | Low (AWS-R4-004) | https://docs.aws.amazon.com/IAM/latest/UserGuide/access-analyzer-policy-generation.html |
| L5 | K01 | Identity-based policies and boundaries "apply only to the specific users, roles, or member accounts they are set on" | **Imprecise.** Neither policy type is set on an account. Boundaries attach to "IAM entities (users or roles)", and identity-based policies attach to users, groups, and roles. The real reason they cannot bind the root user is that you cannot attach either policy type to the root user. An SCP "restricts permissions for IAM users and roles in member accounts, including the member account's root user". | Low (AWS-R4-005) | https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies_boundaries.html ; https://docs.aws.amazon.com/organizations/latest/userguide/orgs_manage_policies_scps.html |
| L6 | S01 | "Register MFA on the root user ..." (the only root-hardening guidance given) | **Currency.** MFA on the root user is now mandatory: "All AWS account types (standalone, management, and member accounts) require MFA to be configured for their root user", with a 35-day grace period. For Organizations, AWS now recommends **centrally managing root access** and removing member-account root credentials. Neither fact is mentioned. | Low (AWS-R4-006) | https://docs.aws.amazon.com/IAM/latest/UserGuide/root-user-best-practices.html |
| L7 | S03 | "without it, anyone who learns the role's ARN could ask the third party to assume it on their behalf" | **Imprecise.** The confused deputy is *another customer of the same third party*. That customer supplies your role ARN, and the third party's service uses its own trusted principal to act on it. The external ID is generated by the third party and is not a secret. An arbitrary outsider cannot use the role simply by knowing the ARN. | Low (AWS-R4-007) | https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_common-scenarios_third-party.html ; https://docs.aws.amazon.com/IAM/latest/UserGuide/confused-deputy.html |
| L8 | K02 / S06 | "assign permission sets to groups per account"; Identity Center as the multi-account answer | **Missing prerequisite (minor).** Permission sets and the access portal for AWS accounts need an **organization instance**, which is enabled in the Organizations management account. An account instance has "Multi-account permissions: No" and "AWS access portal ... to your AWS accounts: No". The lesson is not wrong for the multi-account case, but add one clause, because the de-federation exercise asks students to consider Identity Center for a single standalone account (see E2). | Low (folded into AWS-R4-009) | https://docs.aws.amazon.com/singlesignon/latest/userguide/identity-center-instances.html |

Spot-checked and verified, with notes (no change needed):
- SCPs never grant permissions; they never apply to the management account; they do apply to member-account root users.
- The Region-lock pattern uses `NotAction`.
- A boundary is an intersection that only narrows; an `AdministratorAccess` boundary restricts nothing. Nuance: resource-based policies granting to an IAM user ARN are not limited by a boundary's implicit deny, but the lesson only claims the identity-policy intersection, which is correct.
- The SAML provider must be in the role's own account.
- Cognito is for application users.
- Regions do not replicate automatically.
- RDS Multi-AZ is a synchronous standby; a cross-Region read replica is asynchronous.
- `BoolIfExists` + `aws:MultiFactorAuthPresent` + `sts:GetSessionToken` all match the example policy. "Every action except MFA setup" is a fair simplification: the NotAction list also includes `iam:GetUser` and `sts:GetSessionToken`.
- The password policy has no MFA setting.
- Groups hold only users, cannot be nested, and cannot be a Principal.
- The instance profile gives rotated credentials from metadata.
- Cross-account AssumeRole needs both sides.
- Control Tower orchestrates Organizations, Service Catalog, and Identity Center (landing zone in under an hour; preventive, detective, and proactive controls; Account Factory).
- Member accounts cannot change an organization trail; only the management account or a delegated administrator can.
- Lambda supports `add-permission` and `put-resource-policy`. AWS now recommends `put-resource-policy`, and the lesson lists both.
- AD Connector does not cache in the cloud.
- AWS Managed Microsoft AD deploys two domain controllers and supports trusts.
- Simple AD is Samba 4 based, is "no longer open to new customers", and has no trusts.
- The Identity Center AD directory lives in the management account or the delegated admin account, and authentication is pass-through with no password sync.

## 2. Pilot fixes: per-question table

| ID | Key | Single best answer set? | Distractors real, plausible, clearly wrong? | Facts | Verdict | Doc URL |
|---|---|---|---|---|---|---|
| k04-mr | b, e | Yes | Yes. Each wrong choice is now a real feature from the same problem space. (a) PowerUserAccess widens permissions. (c) An external access analyzer is real and plausible, but it looks at sharing outside the zone of trust, not usage; deleting roles would also be wrong. (d) The Trusted Advisor IAM Access Key Rotation check is real ("not been rotated in the last 90 days"; Yellow above 90 days, Red above 2 years), but it concerns credentials, not permission scope. This fixes both round-3 complaints (the GuardDuty non-feature and the self-evident boundary). | Correct. Optional nit: Trusted Advisor checks are refreshed, not "turned on". "Review the ... check" would be more precise. | **Approve** | https://docs.aws.amazon.com/IAM/latest/UserGuide/access-analyzer-findings.html ; https://docs.aws.amazon.com/awssupport/latest/user/security-checks.html#iam-access-key-rotation |
| s02-mr | a, c | Yes | Yes, unchanged: baked AMI keys, inline copies, and an IAM group of instances. | **Error in the new stem:** "read long-term access keys **for that role** from a config file". IAM roles have no long-term credentials; "a role does not have standard long-term credentials, such as a password or access keys". The keys can only belong to an IAM user. This teaches a false fact, and it goes against the lesson's own S02/S01 text. | **Concerns** (AWS-R4-008) | https://docs.aws.amazon.com/IAM/latest/UserGuide/root-user-best-practices.html ; https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles.html |
| s06-mr | d, e | Yes. The added "set up and managed from one central place rather than once per account" cleanly rules out (a). | Yes, and better than before. (a) Per-account AD FS SAML is a real and strong distractor that meets two of the three constraints but fails "one central place". (b) Cognito is for app users. (c) Managed AD deploys domain controllers in the VPC. Replacing Simple AD removes the retired-service distractor and resolves my round-1 note. | Correct: AD Connector (no caching, no DCs in AWS); Identity Center with the AD directory in the management account; pass-through, "No password information is synchronized". Optional: choice e "an AWS Directory Service directory" is generic and could be read as Managed AD. It still pairs only with d, so the key stays unique; "using the AD Connector as its identity source" would be tighter. | **Approve** | https://docs.aws.amazon.com/singlesignon/latest/userguide/manage-your-identity-source-ad.html ; https://docs.aws.amazon.com/directoryservice/latest/admin-guide/directory_ad_connector.html |

## 3. de-federation exercise verdict

**Verdict: approve with minor concerns.** The scenario and the new rubric items r6 and r7 now target SAA-1.1-S06 correctly: SAML/AD FS versus Identity Center, and AD Connector versus Managed AD versus per-account SAML. None of the requirements states a false fact. Two wording issues could mislead a student, or make grading against r7 inconsistent:

- **E1.** The constraint says "state **which one** keeps passwords on premises and **which one** runs domain controllers in AWS", which implies one option each. In fact:
  - AD Connector and per-account AD FS SAML both keep passwords on premises.
  - AWS Managed Microsoft AD with a trust to the on-premises forest also authenticates on-premises users against on-premises DCs ("can work with users ... from any domain connected through an AD trust"). Only the AWS-hosted *DCs* differ.
  - The scenario's "or run a fully AWS-hosted directory" also overlaps with AWS Managed Microsoft AD without saying how it differs (users migrated into AWS, no trust).
- **E2.** The single-account case offers IAM Identity Center as an equal alternative. To give AWS account access through permission sets, Identity Center needs an **organization instance**, meaning the account must enable AWS Organizations and become its management account. An account instance cannot assign AWS account access. Students should be asked to state this.

## 4. New issues

| ID | Severity | Location | Exact fix | Doc URL |
|---|---|---|---|---|
| AWS-R4-001 | Medium | lesson-1-1 S04, organization trail paragraph | Replace "Accounts placed under a covered OU are picked up automatically." with "It covers every account in the organization, not selected OUs, and any account that later joins the organization is added to the trail automatically." | https://docs.aws.amazon.com/awscloudtrail/latest/userguide/creating-trail-organization.html |
| AWS-R4-002 | Medium | lesson-1-1 K02, Identity Center bullet | Replace "(an external IdP over SAML/OIDC, Identity Center's own directory, or AWS Managed Microsoft AD)" with "(an external IdP over SAML 2.0, with users and groups provisioned by SCIM; Identity Center's own directory; or Active Directory, either self-managed through AD Connector or AWS Managed Microsoft AD)". | https://docs.aws.amazon.com/singlesignon/latest/userguide/manage-your-identity-source-idp.html |
| AWS-R4-003 | Low | lesson-1-1 K04, bullets and exam tip | Add a bullet: "**Access Analyzer unused access findings** (a paid analyzer) continuously flag unused roles, unused access keys and passwords, and unused service- and action-level permissions on roles." Change the exam tip to "... means Access Analyzer policy generation, unused access findings, or last accessed information — not a permissions boundary ... and not external access findings ...". | https://docs.aws.amazon.com/IAM/latest/UserGuide/access-analyzer-findings.html |
| AWS-R4-004 | Low | lesson-1-1 K04, policy generation bullet | Change it to "reads an IAM user's or role's CloudTrail activity over a period of up to 90 days and drafts a policy from what was used (action-level for supported services, service-level otherwise; data events and `iam:PassRole` are not captured), for you to review and attach." | https://docs.aws.amazon.com/IAM/latest/UserGuide/access-analyzer-policy-generation.html |
| AWS-R4-005 | Low | lesson-1-1 K01, first paragraph | Replace "since those apply only to the specific users, roles, or member accounts they are set on" with "since those attach only to IAM users, groups, or roles (boundaries to users or roles), and neither can be attached to the root user". | https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies_boundaries.html |
| AWS-R4-006 | Low | lesson-1-1 S01, first paragraph | After "Register **MFA** on the root user", add "(AWS now requires root MFA on standalone, management, and member accounts); in an organization, AWS recommends centrally managing root access and removing member-account root credentials altogether". | https://docs.aws.amazon.com/IAM/latest/UserGuide/root-user-best-practices.html |
| AWS-R4-007 | Low | lesson-1-1 S03, external ID sentence | Replace "without it, anyone who learns the role's ARN could ask the third party to assume it on their behalf" with "without it, another customer of the same third party could give it your role ARN, and the third party's service would access your account on that customer's behalf". | https://docs.aws.amazon.com/IAM/latest/UserGuide/confused-deputy.html |
| AWS-R4-008 | Medium | q-saa-1-1-s02-mr stem | Replace "each have their own IAM role defined, but the instances currently read long-term access keys for that role from a config file on disk to reach one DynamoDB table" with "each have their own IAM role defined, but the instances still read an IAM user's long-term access keys from a config file on disk to reach one DynamoDB table". Key (a, c) and rationale are unchanged. | https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles.html |
| AWS-R4-009 | Low | de-federation constraints (and one clause in lesson K02) | (1) Change the constraint to "... and state, for each option, whether passwords stay on premises and whether it runs domain controllers in AWS". Change r7 to match ("for each option"). (2) In the scenario, change "or run a fully AWS-hosted directory" to "or move users into AWS Managed Microsoft AD with no on-premises trust". (3) Add the constraint "If IAM Identity Center is chosen for the single-account case, state that assigning AWS account access requires an organization instance (AWS Organizations enabled, with this account as the management account)". In lesson K02, add "(requires an organization instance enabled in the Organizations management account)" after "assign **permission sets** to groups per account". | https://docs.aws.amazon.com/singlesignon/latest/userguide/identity-center-instances.html ; https://docs.aws.amazon.com/singlesignon/latest/userguide/manage-your-identity-source-ad.html |

Optional nits (non-blocking):
- **k04-mr (d):** "Turn on the ... check" → "Review the ... check".
- **s06-mr (e):** "an AWS Directory Service directory" → "the AD Connector".

All edits are content changes and need the AGENTS.md flow: a plan, Teacher validation, and re-review.

## Overall: concerns
