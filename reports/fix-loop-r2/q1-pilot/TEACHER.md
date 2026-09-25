# Q1 pilot: Teacher pedagogy review (SAA task 1.1)

Date: 2026-09-25. Role: Teacher Agent (read-only). Scope: the 19 files `content/questions/q-saa-1-1-*.json` at commit `c565163`, the 33 `cite-saa-1-1-*` citation files, `content/lessons/lesson-1-1.json`, and the earlier lesson `a0-lab-safety.json`. Method and targets come from "Phase 4: Q1" of `.cursor/plans/lead_dev_fix_loop_round2_20260926.plan.md`. Author notes: `impl.md`.

No files other than this report were written.

## Checks run

| Check | Result |
|---|---|
| `backend\.venv\Scripts\python.exe scripts\content_lint.py` | **PASS** (questions 429: aws 310, tf 119; labs 21 + 21; lessons 23), exit 0 |
| File name matches `id`, for all 19 | yes |
| `selectCount` equals key length, for all 19 | yes |
| Every MR stem says "(Select TWO.)" | yes (8/8) |
| Letter references in rationales ("Option C", "(a)", "A and B") | 0 |
| Every citation ID resolves to a file in `content/citations/` | yes (33/33); each URL and title matches the topic it is cited for |
| Difficulty values | `applied` 17, `foundation` 2 (the bank uses only these two values) |
| Doc spot-checks (WebFetch, 2026-09-25) | Control Tower "landing zone in less than an hour", three control kinds, and Account Factory: confirmed. Identity Center with AD: the AD Connector must be in the management account (or the delegated admin account), Simple AD is not supported, and no passwords are synchronized: confirmed |

Full AWS fact-checking belongs to the AWS Architect under the plan. I found no factual errors in the claims I read or spot-checked.

## Per-question review

Teach-before-test ("TbT") is **No** for every item, because lesson 1.1 has no teaching text (see CR-draft T1). Following the task rules, this does not block a question. It is a lesson gap.

| ID | Objective fit | TbT | Difficulty | Rationale quality | Verdict | Notes |
|---|---|---|---|---|---|---|
| k01-mc | Good (K01: controls across accounts) | No | applied, right | Strong. Covers the key and all 3 distractors; explains why the root user matters | **approve** | The stem's "even ... the root user" points toward an SCP, but the real exam uses that cue too, so it is fair. |
| k01-mr | Good | No | applied, right | Strong; all 3 distractors covered | **approve** | The management-account group distractor also fails the "sign in once with the corporate IdP" requirement. The rationale could say so, but it is fine as written. |
| k02-mc | Good (K02) | No (a0 names Identity Center only in passing) | applied, right | Strong. The "12 separate trusts" reason is precise | **approve** | |
| k03-mc | Acceptable (K03 framed as Region isolation plus AZ failure) | No | foundation, right | Good; all 3 distractors covered | **approve** | Author doubt 4: I agree with the framing. Small wording nit: "never leave the country where its chosen Region is located" is fine. |
| k04-mc | Good (K04 least privilege) | Partial (a0 and GL-01 explain permissions boundaries) | applied, right | Strong. The "boundary only caps" reason teaches well | **approve** | |
| k04-mr | Good | No | applied, but plays easier | Accurate | **concerns** | Two distractors are not plausible. "GuardDuty removes unused permissions" is a feature that does not exist, and "an AdministratorAccess boundary that follows usage" is self-evidently wrong. PowerUserAccess is plainly broader. A student can reach the key by elimination without knowing Access Analyzer or last-accessed data. Replace one or two of them with real tools that do not answer the question, such as a Trusted Advisor check, an AWS Config rule that flags admin policies, or Access Analyzer *external access* findings. |
| k05-mc | Good (K05) | Partial (a0 lists K05 but only covers safety rules) | foundation, right | Good. The last sentence ("you do not configure security access for processes that RDS manages") answers a slightly different point than the distractor, which is about configuring replication | **approve** | Author doubt 2: I agree that leaving OS patching out was right. The key is the longest choice (91 vs 85), which is within the 35% target. Optional: end the rationale with "RDS sets up and runs synchronous replication to the standby itself." |
| s01-mc | Good (S01 root + MFA) | Partial (a0: "never root access keys") | applied, right | Strong | **approve** | Minor: the stem does not say where the nightly script runs. If it runs off AWS, "move the script to an IAM role" needs IAM Roles Anywhere or similar. Suggest adding "on an EC2 instance". The key stays the only defensible answer either way. |
| s01-mr | Good | No | applied, right | Strong; the password-policy correction teaches well | **approve** (minor) | Author doubt 5: the pair is defensible. The Deny policy covers "MFA before API calls" and Identity Center covers "no long-lived keys", and no other pair works. For a self-contained choice, add "with MFA required at sign-in" to the Identity Center choice. "Users inherit root MFA" is a weak distractor, but it tests a real misconception. |
| s02-mc | Good (S02) | No | applied, right | Strong. Nested groups and group-as-Principal are correct and useful | **approve** | |
| s02-mr | Good | No | applied, right | Good | **concerns** | The stem says the apps "each run under their own IAM role", which implies the roles are already in use on the instances. That makes the keyed choice "attach each role through an instance profile" look like something already done, and a careful student may look elsewhere. Reword to "each has its own IAM role, but the instances currently read access keys from a config file", or similar. |
| s03-mc | Good (S03 STS, cross-account) | Partial (GL-03 touches AssumeRole) | applied, right | Strong; explains the confused deputy clearly | **approve** | |
| s03-mr | Good | Partial (GL-03) | applied, right | Strong. "Both sides are required" is the core teaching point | **approve** | |
| s04-mc | Good (S04 Control Tower) | Partial (exercise de-multi-account names Control Tower and SCPs) | applied, right | Strong; claims confirmed against the doc | **approve** | The key is the shortest choice, which is good against length cues. |
| s04-mr | Good (S04 SCPs, org trail) | Partial | applied, right | Strong. The "SCP on the management account does nothing" point is exam-relevant | **approve** | |
| s05-mc | Good (S05 resource policies) | Partial (GL-03 mentions a bucket policy) | applied, right | Strong | **approve** | |
| s05-mr | Good | No | applied, right | Strong | **approve** | |
| s06-mc | Good (S06: federate a directory with IAM roles) | No (exercise de-federation has no SAML or AD FS text) | applied, right | Strong | **approve** | Author doubt 1: fair, not a trick. Identity Center is not offered, the stem says "single AWS account", and the objective wording is "federate ... with IAM roles". Each distractor fails a stated constraint. |
| s06-mr | Good | No | applied, right | Accurate; the Identity Center AD claims are confirmed | **concerns** | (1) The keyed choice says "using **that directory** as its identity source". That dangling reference ties it to another choice, which is a pairing cue, and it is ambiguous (which directory?). Say "an AWS Directory Service directory" instead. (2) Author doubt 6: Simple AD is closed to new customers, so it is a dated distractor. Replace it with a current one, such as an IAM SAML provider in each of the 15 accounts (valid but fails "manage all accounts from one place"), which would need a matching stem constraint, or a Cognito identity pool. |

Tally: **16 approve, 3 concerns** (k04-mr, s02-mr, s06-mr), plus the batch-level issue below. No factual errors found. Every question has exactly one defensible key once the wording fixes above are made.

### Batch-level fairness issue: repeated distractor archetypes

Taken one at a time, each distractor is plausible. Across the batch, the same wrong ideas come back so often that a student can learn "this option type is always wrong" instead of the concept:

| Distractor archetype | Questions | Count |
|---|---|---|
| IAM user / long-term access keys | k01-mr, k02-mc, k04-mc, s01-mc, s03-mc, s03-mr, s05-mc, s06-mc | 8 |
| Permissions boundary as the fix | k01-mc, k04-mc, k04-mr, s04-mr, s05-mc, s05-mr | 6 |
| Cognito for workforce sign-in | k02-mc, s06-mc, s06-mr | 3 |
| SCP that "grants" | k01-mr, s05-mc, s05-mr | 3 |
| IAM group containing a role or instance | s02-mr, s03-mr, s05-mr | 3 |

"IAM user with access keys" in 8 of 19 items is the same generic safety-mistake pattern that Q1 set out to remove. In the real exam, the wrong answers are usually *correct technology used for the wrong constraint*, such as a cross-Region replica, a delegated admin, or RAM sharing.

## Draft change requests (for Lead Dev to record in `docs/change-requests.md`)

**CR-draft T1: Lesson 1.1 has no teaching content (High, content)**
- Where: `content/lessons/lesson-1-1.json` `bodyMarkdown`.
- Problem: each of the 11 bullets repeats only the objective text followed by a generic "Tradeoffs" or "Applied practice" paragraph. None of the concepts the 19 drills test are taught. The lesson citation (`cite-1-1`, the IAM introduction) is marked "MCP re-check pending".
- Needed, per bullet (short, cited, same `cite-saa-1-1-*` files):
  - K01: SCPs set maximum permissions, never grant, apply to member root users, do not affect the management account, and are inherited by OUs. Cross-account roles.
  - K02: Identity Center (identity sources, permission sets, access portal) vs per-account IAM SAML vs Cognito (app users).
  - K03: Region isolation and data residency; AZs; Multi-AZ vs cross-Region replica; Local Zones.
  - K04: least privilege; AWS managed vs customer managed vs inline policies; Access Analyzer policy generation; last accessed information.
  - K05: shared responsibility, with the RDS example (security groups and DB users vs hardware and replication).
  - S01: root user practices (no access keys, MFA, root-only tasks); `aws:MultiFactorAuthPresent`; the password policy has no MFA option.
  - S02: groups (no nesting, not a Principal, users only); instance profiles; managed vs inline policies.
  - S03: both sides of AssumeRole; external ID and the confused deputy problem.
  - S04: Control Tower (landing zone, controls, Account Factory); organization trail.
  - S05: identity plus resource policy for cross-account access; S3, Lambda and SQS resource policies.
  - S06: IAM SAML provider plus roles (AD FS), AD Connector vs AWS Managed Microsoft AD vs Simple AD, and Identity Center with an AD source.
- Content-affecting: yes. Teacher validation is needed before and after.

**CR-draft T2: Exercise `de-federation` does not teach federation mechanics (Medium, content)**
- `content/exercises/de-federation.json` (S06) never mentions SAML, AD FS, AD Connector or Identity Center. Add the decision points that s06-mc and s06-mr test.

**CR-draft T3: Fix wording in four pilot questions (Low, content)**
- k04-mr: replace the implausible GuardDuty and "boundary follows usage" distractors with real, plausible tools.
- s02-mr: reword the stem so the roles are not already attached.
- s06-mr: remove "that directory"; replace the Simple AD distractor.
- s01-mc (optional): say where the script runs. s01-mr (optional): add "with MFA required" to the Identity Center choice. k05-mc (optional): tighten the last rationale sentence.

**CR-draft T4: Lesson 1.1 `drillIds` list only the 11 MC items (Low, content)**
- The 8 MR drills (`q-saa-1-1-*-mr`) are not linked from the lesson. Add them, or record why they are left out.

## Method changes recommended for the remaining batches

1. **Cap distractor archetypes per batch.** Add a rule: no single wrong-answer archetype (IAM user/keys, "boundary fixes it", "SCP grants", root user, group holds a role) in more than about 15% of a batch's items. Prefer distractors that are *real, working features that miss one stated constraint*.
2. **Plausibility check per distractor.** Reject distractors that describe a feature that does not exist or that contradict themselves (k04-mr). The Student's sample should record "eliminated without domain knowledge" as a fairness failure.
3. **No cross-choice references.** Each choice must stand alone: no "that directory" or "the same role" pointing at another choice. This is lintable with a small phrase list.
4. **Stem-state check.** The stem must not describe as already done anything a key asks you to do (s02-mr).
5. **Retired or closed services** (Simple AD, and later items such as CodeCommit or Cloud9 for new customers) should not be used as distractors unless the stem is about migration away from them.
6. **Teach-before-test gate.** Before drafting a batch, confirm the lesson for that task actually teaches the tested concepts. Every SAA lesson I have seen follows the same boilerplate template as 1.1. Otherwise every batch will fail teach-before-test. Suggest a lesson-rewrite work item per task in step with the question batches (lesson first, then drills).
7. **Keep what worked:** varied openings, key positions and lengths, per-distractor rationales naming content rather than letters, one citation per claim, and the author's "where I was unsure" list. The unsure list made this review fast and should be kept for every batch.
8. **Difficulty.** Two levels are enough for now. Mark an item `foundation` only when it tests recall of a single fact (k03-mc and k05-mc are correct examples).

## Overall

Question quality is a large improvement. The items are exam-realistic, the rationales are complete and plain, the IDs, counts and citations are consistent, and the lint passes. The open items are: 3 questions that need small wording or distractor fixes, a batch-wide pattern of repeated distractors, and a lesson 1.1 that teaches none of the tested material (T1).

Overall: concerns
