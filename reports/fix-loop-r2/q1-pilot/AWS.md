# Q1 pilot: AWS Solutions Architect review (SAA-C03 task 1.1)

Reviewer: Senior AWS Solutions Architect (read-only). Date: 2026-09-25.
Scope: the 19 files `content/questions/q-saa-1-1-*.json` from commit `c565163`, their citations `content/citations/cite-saa-1-1-*.json`, and the author notes `reports/fix-loop-r2/q1-pilot/impl.md`. Targets are from "Phase 4: Q1" in `.cursor/plans/lead_dev_fix_loop_round2_20260926.plan.md`.

Method:
- I read every stem, choice and rationale, and solved each question for the stated constraints before looking at the key.
- I checked the load-bearing claims against the live `docs.aws.amazon.com` pages with WebFetch: SCPs, the Region-deny example, root user best practices, IAM best practices, the MFA self-manage policy, IAM groups, last accessed information, SAML federation, Identity Center (what-is, permission sets, AD identity source), AD Connector, Simple AD, Control Tower, organization trails, Regions and zones, RDS security, RDS maintenance, third-party external ID, and Lambda cross-account access.
- All 33 citation files exist, and each points to a `docs.aws.amazon.com` URL. Every `citationId` resolves.
- No AWS calls were made, and no files other than this report were written.

## Per-question results

| ID | Key correct | Rating | Issues / notes | Doc URL (primary) |
|---|---|---|---|---|
| k01-mc | y (c) | Exam-realistic and correct | The SCP on the OUs is the only choice that binds member-account admins and the root user. Doc: "An SCP restricts permissions for IAM users and roles in member accounts, including the member account's root user." Citation substitution (doubt 3) is acceptable: the IAM example uses the same Deny + NotAction + `aws:RequestedRegion` pattern and names the same global-service exemptions. | https://docs.aws.amazon.com/organizations/latest/userguide/orgs_manage_policies_scps.html |
| k01-mr | y (a, d) | Exam-realistic and correct | Doc: when you assign a permission set, Identity Center "creates corresponding ... IAM roles in each account". "An SCP never grants" is verbatim from the docs. | https://docs.aws.amazon.com/singlesignon/latest/userguide/permissionsetsconcept.html |
| k02-mc | y (a) | Exam-realistic and correct | "only one certificate to manage" (Identity Center what-is) and "SAML IDPs used in a role trust policy must be in the same account that the role is in" (IAM SAML page) are both verified. The per-account SAML distractor is plausible but fails "one federation trust". | https://docs.aws.amazon.com/singlesignon/latest/userguide/what-is.html |
| k03-mc | y (d) | Exam-realistic and correct | Doubt 4: the framing (residency = Region isolation, and an AZ failure means Multi-AZ) fits K03. EC2 doc: "Regions are isolated from each other, and we don't automatically replicate resources across Regions." The same-AZ distractor is easy to rule out, which is acceptable for `foundation`. Optional: a cross-AZ self-managed option would be a stronger distractor. | https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/using-regions-availability-zones.html |
| k04-mc | y (b) | Exam-realistic and correct | The boundary distractor is well built: the effective permissions would be the intersection, which is read on every bucket. Doc: AWS managed policies "might not grant least-privilege permissions". | https://docs.aws.amazon.com/IAM/latest/UserGuide/best-practices.html |
| k04-mr | y (b, e) | Exam-realistic and correct | Minor nuance, not an error: action-level last accessed data covers management actions only, not data-plane events. The rationale wording matches the doc's own summary ("services and actions"). | https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies_last-accessed.html |
| k05-mc | y (c) | Exam-realistic and correct | Doubt 2: leaving out OS patching is right, because RDS optional OS updates are not applied automatically, so that responsibility is shared. RDS security page: "Use security groups to control what IP addresses or Amazon EC2 instances can connect" and "You don't have to configure security access for processes that Amazon RDS manages ... replicating data." Hardware maintenance appears as the `hardware-maintenance` action on the maintenance page. | https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/UsingWithRDS.html |
| s01-mc | y (a) | Exam-realistic and correct | The root best-practices page supports all three parts of the key. The distractors are standard anti-patterns; the item is realistic for SAA. | https://docs.aws.amazon.com/IAM/latest/UserGuide/root-user-best-practices.html |
| s01-mr | y (c, e) | Exam-realistic and correct | Doubt 5: the Identity Center MFA claim is supported by the IAM best-practices MFA section ("you can use the IAM Identity Center MFA capabilities ..."), not by `idc-what`, which never mentions MFA. The citation set already includes `iam-bp`, so this is OK. Suggestion: add "with MFA required at sign-in" to choice e so that e plainly meets the MFA part. The BoolIfExists and GetSessionToken statements match the example policy page. | https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_examples_aws_my-sec-creds-self-manage.html |
| s02-mc | y (d) | Exam-realistic and correct | "User groups can't be nested" and "groups relate to permissions, not authentication" are verbatim from the doc. The key is the doc's own "changes jobs" example. | https://docs.aws.amazon.com/IAM/latest/UserGuide/id_groups.html |
| s02-mr | y (a, c) | Exam-realistic and correct | Accurate. | https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_use_switch-role-ec2.html |
| s03-mc | y (c) | Exam-realistic and correct | Matches the doc: the external ID is generated by the third party, and its "primary function ... is to address and prevent the confused deputy problem". | https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_common-scenarios_third-party.html |
| s03-mr | y (b, d) | Exam-realistic and correct | Both halves of cross-account role access are required, so the answer set is exact. | https://docs.aws.amazon.com/IAM/latest/UserGuide/tutorial_cross-account-with-roles.html |
| s04-mc | y (a) | Exam-realistic and correct | Doc: Control Tower "orchestrates ... Organizations, Service Catalog, and IAM Identity Center, to build a landing zone in less than an hour". Preventive, detective and proactive controls, and Account Factory as a "configurable account template", are all verified. | https://docs.aws.amazon.com/controltower/latest/userguide/what-is-control-tower.html |
| s04-mr | y (a, e) | Exam-realistic and correct | The org trail claims are verbatim from the doc: member-account users cannot delete it, turn logging on or off, or change it, and new accounts are added automatically. "SCPs don't affect users or roles in the management account" is verified. Optional: "New accounts must be covered automatically" holds only if new accounts are created in, or moved to, those OUs. The rationale says so, but the stem could say "new accounts are placed in these OUs". | https://docs.aws.amazon.com/awscloudtrail/latest/userguide/creating-trail-organization.html |
| s05-mc | y (d) | Exam-realistic and correct | Classic cross-account S3 pattern with a correct rationale. | https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies_identity-vs-resource.html |
| s05-mr | y (b, c) | Exam-realistic and correct | Lambda doc: both `put-resource-policy` and `add-permission` are valid, as the rationale says. | https://docs.aws.amazon.com/lambda/latest/dg/permissions-function-cross-account.html |
| s06-mc | y (b) | Exam-realistic and correct | Doubt 1: leaving IAM Identity Center out is fair. There is a single account, S06 is literally "federate a directory service with IAM roles", and the key is the documented AD FS → IAM SAML provider → roles pattern ("map users or groups in your organization to the IAM roles"). Including Identity Center would make the item arguable. | https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_providers_saml.html |
| s06-mr | y (d, e) | Exam-realistic and correct | Doubt 6: every Simple AD claim is verified: "no longer open to new customers", no trust relationships, and "AWS IAM Identity Center" is on its does-not-support list. AD Connector works "without caching any information in the cloud", and Identity Center does "pass-through authentication" with "No password information is synchronized". Choice d ("in the management account") matches the doc; the delegated-admin account is also allowed, but that does not make d wrong. Suggestion: add to the rationale that Simple AD is itself a directory hosted in AWS, which fails "no domain controllers in AWS" and "passwords stay on premises". That is the stronger reason to reject it, and it stays valid even for students with older material. | https://docs.aws.amazon.com/directoryservice/latest/admin-guide/directory_ad_connector.html |

## Summary metrics

- Key correct: **19/19**. No MC item has a second defensible answer, and every MR key set is exact.
- Rated "exam-realistic and correct": **19/19 = 100%** (target ≥ 95%).
- Factual errors found: **0**. Every checked claim matches the current docs.
- Every question tests its mapped objective (`content/objectives/saa_c03.json`, SAA-1.1-K01…S06).

## Required fixes

None. No factual errors or ambiguous keys were found.

## Recommended (non-blocking) improvements

1. **s06-mr rationale:** add that Simple AD is a directory hosted in AWS, so it violates "no domain controllers in AWS" and "passwords stay on premises".
2. **s01-mr choice e:** add "with MFA required at sign-in" so that the choice meets the MFA requirement on its own wording.
3. **s04-mr stem:** say that new accounts are created in those OUs, so that "covered automatically" does not depend on the rationale.
4. **k03-mc (optional):** replace the same-AZ EC2 distractor with a harder one, for example self-managed MySQL replication across two AZs with asynchronous replication (fails "no committed transactions lost").
5. **k04-mr (optional):** note that action-level last accessed data covers management actions.

Any of these edits would require re-review under the freeze rule.

## Overall: approve
