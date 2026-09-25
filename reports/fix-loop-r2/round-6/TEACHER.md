# Fix-loop round 6: Teacher targeted re-check of F12 (commit `04cb6fb`)

Saved by Lead Dev from the Teacher's reply (AGENTS.md: the Teacher does not write files).

## Items

| Item | Verdict | Evidence |
|---|---|---|
| TEACHER-R5-001 (IAM group over cap) | Gone | 3/19 (s02-mc, s02-mr, s03-mr), by the Teacher's own script. k01-mr(e) is now the org-trail distractor; s05-mr(e) is the role-in-account-A distractor |
| TEACHER-R5-002 / AWS-R5-002 (s05-mc ACL) | Gone | Rationale leads with "READ allows the grantee only to list the objects (s3:ListBucket), not to read their data (s3:GetObject)". Confirmed on the ACL overview page. Bucket-owner-enforced default stated correctly |
| TEACHER-R5-003 (delegated admin not taught) | Gone | S04 sentence matches the Organizations doc |
| TEACHER-R5-004 (k01-mc resource policy) | Gone | "many resource types, including EC2 instances and RDS DB instances, do not support them at all" |
| TEACHER-R5-005 / AWS-R5-001 (k02-mc) | Gone | Choice d and rationale now match "Account instances do not support permission sets and therefore do not support access to AWS accounts" |
| TEACHER-R5-006 (s01-mc d) | Gone | Password policy "has no MFA setting, and does not apply to the root user", confirmed verbatim |
| TEACHER-R5-007 (imperative choices) | Gone | Noun phrases now |
| TEACHER-R5-008 (s06-mc double Cognito) | Gone | (a) is now AD Connector without Identity Center or SAML |
| Optional nits (3) | Applied | |

The four new facts were verified live on docs.aws.amazon.com: S3 ACL READ semantics, account instances, delegated administrator scope, password policy vs MFA.

## Batch acceptance (re-run)

- longest-is-key 1/11 (9.1%);
- key positions balanced;
- unique 6-word openings;
- 0 letter references;
- 0 single-asterisk spans (the `invoices/*` hit in k04-mc is ARN text, a false positive);
- every citation resolves;
- `selectCount` matches;
- teach-before-test satisfied for every new distractor;
- `drillIds` lists all 19;
- `content_lint.py` PASS.

## New issues

None.

**Lesson 1.1 + task 1.1 questions: close.** Overall: approve.
