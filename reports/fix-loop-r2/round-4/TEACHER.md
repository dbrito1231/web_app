# Fix-loop round 4: Teacher validation of Amendment 2 (F7 lesson and pilot fixes, F6 wrong-letter fix)

Saved by Lead Dev from the Teacher's reply (AGENTS.md: the Teacher does not write files). Condensed; the verdicts and every issue row are kept as given.

**Overall: concerns.** Lesson 1.1 now teaches the drills (18 Yes, 1 Partial, 0 No; the pilot had 0 Yes). The F6 letter fix is clean. T2 (de-federation) is resolved. What remains is a new factual error in the s02-mr stem, two lesson inaccuracies, and the pilot batch breaking the 15% distractor rule.

## Checks

- `content_lint.py`: PASS. It ran with the uncommitted F4 script in the working tree.
- Letter references across all 429 questions: 0, using a broader regex than F6's.
- F6 field isolation: only `rationale` changed in 185/185 files.
- F6 key consistency: 185/185.
- Lesson 1.1 `drillIds`: all 19.
- Markdown subset: 0 tables, links or numbered lists. 9 single-asterisk spans render as literal asterisks.
- Doc spot-checks: 10 facts. 8 confirmed, 1 inaccurate (Identity Center sources), 1 partly wrong (org trail "covered OU").

## Item verdicts

| Item | Verdict |
|---|---|
| Lesson 1.1: coverage | approve (T1 closed) |
| Lesson 1.1: accuracy | concerns (R4-002, R4-003, R4-005, R4-008) |
| Lesson 1.1: structure and length | approve |
| Lesson 1.1: markdown | concerns, Low (R4-004) |
| Lesson 1.1: `drillIds` | approve (T4 closed) |
| k04-mr | approve (resolved). Trusted Advisor check not taught (R4-006) |
| s02-mr | **concerns**: new factual error (R4-001) |
| s06-mr | approve (resolved) |
| Batch 15% distractor rule | **fails**: IAM user/keys 9/19 (47%), permissions boundary 5/19 (26%) (R4-007) |
| de-federation | approve (T2 resolved), wording nit (R4-008) |
| F6 interim fix (20 sampled + all 185 by script) | approve. Note: it replaces placeholder items; the Q1 rewrite still has to replace them |

## New issues

| ID | Sev | File | Problem | Suggested fix |
|---|---|---|---|---|
| TEACHER-R4-001 | Medium | q-saa-1-1-s02-mr (stem) | "read long-term access keys for that role": roles have no long-term keys | "...each have their own IAM role defined, but the instances currently read an IAM user's long-term access keys from a config file on disk..." |
| TEACHER-R4-002 | Medium | lesson-1-1 K02 | Identity Center sources: docs list SAML 2.0 (+SCIM), not OIDC. The AD option also covers self-managed AD via AD Connector | "...an external IdP over SAML 2.0 (users provisioned with SCIM), Identity Center's own directory, or Active Directory (AWS Managed Microsoft AD, or on-premises AD through AD Connector)..." |
| TEACHER-R4-003 | Low | lesson-1-1 S04 | Org trails aren't OU-scoped | "Accounts that join the organization are added to the trail automatically." |
| TEACHER-R4-004 | Low | lesson-1-1 (9 places) | `*italic*` renders as literal asterisks | Use `**…**` or plain text; optional lint rule |
| TEACHER-R4-005 | Low | lesson-1-1 S06 | "typically in the management or a delegated administrator account": it must be | "which must be" |
| TEACHER-R4-006 | Low | lesson-1-1 K04 | Trusted Advisor IAM Access Key Rotation check not taught | Add one bullet (credential hygiene, never changes what a role may do) |
| TEACHER-R4-007 | Medium | q-saa-1-1-* batch | 15% distractor rule broken (IAM user/keys 9/19, boundary 5/19) | Replace about 6 IAM-user and about 2 boundary distractors with real features that miss one constraint, or record a user-approved pilot exemption |
| TEACHER-R4-008 | Low (optional) | lesson-1-1 K01; de-federation | Boundaries can't be set on accounts; exercise options overlap | Remove "or member accounts"; reword "fully AWS-hosted directory" |

Carry-overs (optional): the s01-mc "where the script runs" nit; "with MFA required" for s01-mr; tightening the k05-mc rationale.

## May SAA task 1.2 start?

Yes, lesson first. Lesson 1.2 can be drafted now and sent to the Teacher before any 1.2 questions, on two conditions:
- apply the Amendment 2 rules from the start (15% cap, no single-asterisk markdown);
- fix R4-001 and R4-002 before 1.1 closes.
