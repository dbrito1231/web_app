# Fix-loop round 5: Teacher validation of batch F8 (commit `f7b6f98`)

Saved by Lead Dev from the Teacher's reply (AGENTS.md: the Teacher does not write files). Condensed; every verdict and issue row is kept.

**Lesson 1.1 + task 1.1 questions: not yet.** Overall: concerns. Two Medium items remain; both are small. After they are fixed and quickly re-checked, 1.1 can close without another full round.

## Checks

- `content_lint.py` PASS.
- Batch acceptance, all ✔:
  - longest-is-key 1/11 (9.1%);
  - key positions within ±10%;
  - every stem opening unique;
  - 0 objective text in choices;
  - 0 letter references;
  - 19/19 cited and verified, `selectCount` matching, and every rationale covering every distractor.
- Lesson 1.1 checks:
  - 0 single-asterisk spans;
  - renders with the markdown subset;
  - `drillIds` lists all 19;
  - all 43 `citationIds` resolve.
- Doc spot-checks: every new lesson bullet is correct (root MFA, policy generation, unused access findings, org trail, Identity Center sources and organization instance, K01 boundaries, S03 confused deputy).

## Round-4 items

R4-001, 002, 003, 004, 005, 006 and 008 are **Gone**. R4-007 is **Gone as scoped** (IAM user/keys 3/19, boundary 3/19). The recount found another type over the cap (R5-001).

## The 8 replaced distractors

| Q / choice | Verdict |
|---|---|
| k01-mc(b) resource policy on every resource | concerns, Low (R5-004) |
| k01-mr(b) delegated administrator | approve; teach gap (R5-003) |
| k02-mc(d) account instance of Identity Center | concerns (R5-005; same as AWS-R5-001) |
| s01-mc(d) Access Analyzer "monitor root" | concerns, Low (R5-006) |
| s03-mr(a) trust policy on the wrong role | approve |
| s05-mc(b) DataSync | approve |
| s05-mc(c) bucket ACL | concerns, **Medium** (R5-002; same as AWS-R5-002) |
| s06-mc(c) Cognito SAML | approve (R5-008) |

Teach-before-test: 17 Yes, 2 Partial (k01-mr, s05-mc), 0 No.

## New issues

| ID | Sev | File | Problem | Suggested fix |
|---|---|---|---|---|
| TEACHER-R5-001 | Medium | q-saa-1-1-k01-mr, s05-mr | "IAM group as the fix" appears in 5/19 questions, over the ≤3 cap | Replace s05-mr(e) with a role in account A that trusts account B (breaks "without assuming a role in account A"). Replace k01-mr(e) with, e.g., an organization trail offered as the auditors' access. Keep s02-mc and s02-mr, where groups are the objective |
| TEACHER-R5-002 | Medium | q-saa-1-1-s05-mc rationale | ACL distractor dismissed for reasons the stem doesn't state. The real one: a bucket ACL READ grant allows only listing (s3:ListBucket), not s3:GetObject | Lead with that fact; mention that ACLs are disabled by default (Bucket owner enforced), or state the default Object Ownership in the stem. Add one ACL line to lesson S05 |
| TEACHER-R5-003 | Low | lesson-1-1 K01 or S04 | Delegated administrator never explained | "Registering a delegated administrator gives a member account admin rights for one specific service plus read-only Organizations actions; it grants no general IAM access to other accounts." |
| TEACHER-R5-004 | Low | q-saa-1-1-k01-mc rationale | Resource-policy distractor's real flaws not stated | "Resource-based policies control access to a resource that already exists, not where resources can be created, and many resource types (EC2 instances, RDS DB instances) do not support them." |
| TEACHER-R5-005 | Low (Medium per AWS-R5-001) | q-saa-1-1-k02-mc choice d + rationale | An account instance gives no AWS-account access or permission sets at all; "without enabling AWS Organizations" conflicts with the stem | Choice: "Enable an account instance of IAM Identity Center in one member account and assign permission sets from there." Rationale: "Account instances support only application assignments; multi-account permissions and portal access to AWS accounts need an organization instance." |
| TEACHER-R5-006 | Low | q-saa-1-1-s01-mc choice d | Wrong for both findings, self-evidently wrong, and a 143-character length outlier | "Move the script to an IAM role, delete the root access key, and set the account password policy to require MFA." |
| TEACHER-R5-007 | Low | s05-mc(b,c); s06-mc(c) | Imperative choices where the others are noun phrases | "An AWS DataSync task that…", "A bucket ACL that…", "An Amazon Cognito user pool…" |
| TEACHER-R5-008 | Low | q-saa-1-1-s06-mc | Two Cognito distractors removed together by one rule | Replace (a) or (c), e.g. with AD Connector without Identity Center |

Optional nits: s01-mc "where the script runs"; s01-mr "with MFA required"; s03-mr(a) "edit the trust policy of" (AWS agrees); K02 "usually provisioned by SCIM".
