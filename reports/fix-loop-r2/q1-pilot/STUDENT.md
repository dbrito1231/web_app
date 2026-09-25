# STUDENT.md — College IT Student fairness review of Q1 pilot (SAA task 1.1)

Reviewer role: College IT Student (basic IT background, not an AWS expert, studying from this app).
Read-only review. No files edited, no servers started, no Reset/Import clicked.

## Lesson read first

Read lesson **1.1 — Secure access to AWS resources** at `/start` (lesson value `lesson-1-1`) before
answering any drill. The lesson lists the 5 knowledge bullets (K01–K05) and 6 skill bullets (S01–S06)
for task 1.1, each with a generic "Tradeoffs" or "Applied practice" paragraph, a citation to the IAM
user guide, and links to the drills, labs, and design exercises for the lesson.

## Per-question results

### q-saa-1-1-k01-mc
- **Scenario:** Retail group, 45 member accounts, legal requires workloads never leave eu-west-1/eu-central-1, must hold even for account admins and root.
- **My answer (recorded before submitting):** "Attach an SCP to the member accounts' OUs that denies requests where aws:RequestedRegion is not one of the two Regions." Reason: SCPs bind every principal in an account, including root, and apply org-wide with one policy — least ongoing effort and the only option that actually restricts root.
- **Result:** Correct (100%).
- **Fair:** Yes. All three distractors are individually wrong for a concrete, checkable reason (identity policy = per-principal upkeep and doesn't bind root; permissions boundary doesn't bind root or existing admins; CloudTrail+EventBridge is detective, not preventative), so only one answer is defensible. Not answerable from wording alone — you need to know how SCPs, identity policies, and permissions boundaries actually differ with respect to the root user.
- **Explanation useful:** Yes — it named the `NotAction` exemption for global services (IAM/CloudFront/Route 53), which is a detail I hadn't already known.

### q-saa-1-1-k02-mc
- **Scenario:** Insurance firm, 2,000 employees in an external SAML 2.0 IdP, 12 AWS accounts, needs one portal and one federation trust.
- **My answer:** "Enable IAM Identity Center, connect the IdP as its identity source, and assign groups to accounts with permission sets." Reason: only option matching "one trust" + "one portal" across 12 accounts.
- **Result:** Correct (100%).
- **Fair:** Yes. Cognito is a plausible-sounding trap for anyone who conflates "identity provider integration" with app auth; the explanation clarifies the distinction (Cognito = app/mobile users, not workforce console access). The "12 separate trusts" reasoning against per-account SAML providers is a specific, checkable fact, not vague reasoning.
- **Explanation useful:** Yes.

### q-saa-1-1-k04-mr
- **Scenario:** Fintech company's IAM roles still carry broad permissions after early growth; must shrink to actual usage based on evidence. Select TWO.
- **My answer:** "Use IAM Access Analyzer to generate a policy ... from CloudTrail activity" + "Review IAM last accessed information and remove unused services/actions." Reason: only two options that are evidence-based; the other three either widen access (PowerUserAccess, AdministratorAccess boundary) or misdescribe a service (GuardDuty does not edit IAM policies).
- **Result:** Correct (100%).
- **Fair:** Yes. Note: this `-mr` variant is not one of the 11 drills linked from the lesson page's "Drills for this lesson" list (the lesson links `q-saa-1-1-k04-mc` instead) — see "Confusing" below.
- **Explanation useful:** Yes, and it correctly matched the on-screen choices.

### q-saa-1-1-s02-mc
- **Scenario:** 60 developers across 3 teams, people rotate teams every few months, need least admin effort.
- **My answer:** "Create one IAM group per team with a managed policy attached, and move users between groups when they change teams." Reason: standard IAM group model; the other three are each broken by a specific IAM rule.
- **Result:** Correct (100%).
- **Fair:** Yes. Two of the four distractors are not just suboptimal but technically invalid (IAM groups cannot be nested; a group cannot be a resource-policy Principal), which the explanation confirms. This teaches real IAM limits, not just "best practice."
- **Explanation useful:** Yes.

### q-saa-1-1-s03-mr
- **Scenario:** Release engineers federate into a dev account, need short-lived access to a separate prod account, no identities may be created in prod. Select TWO.
- **My answer:** "In development, allow ... sts:AssumeRole on the production deployment role's ARN" + "In production, create a deployment role whose trust policy names the development account as a trusted principal." Reason: cross-account role assumption needs both halves — trust policy on the target role and an AssumeRole grant on the source side.
- **Result:** Correct (100%).
- **Fair:** Yes, and appropriately hard — a student who only remembers "you need a trust policy" but forgets the source-side AssumeRole grant (or vice versa) would miss one of the two required picks. The wrong options are each disqualified by a specific rule stated in the explanation (groups can't hold cross-account roles, VPC peering is network-only, IAM users violate the stated constraint).
- **Explanation useful:** Yes.

### q-saa-1-1-s05-mc
- **Scenario:** Account B role needs s3:GetObject on a bucket account A owns; identity policy already in place; requests still denied; no long-term credentials.
- **My answer:** "A bucket policy that allows s3:GetObject ... for the account B role's ARN." Reason: cross-account resource access needs both an identity-based policy (already present) and a resource-based policy on the resource-owning side.
- **Result:** Correct (100%).
- **Fair:** Yes. The SCP distractor is a good one for testing a common misconception (that SCPs can grant access) — the explanation directly corrects it ("An SCP never grants permissions").
- **Explanation useful:** Yes.

### q-saa-1-1-s06-mc
- **Scenario:** University runs AD FS in front of on-prem AD, single AWS account, IT staff need console access with AD credentials and AD-group-based permissions, no IAM users.
- **My answer:** "An IAM SAML identity provider for AD FS, plus IAM roles that trust it and are mapped from AD groups." Reason: this is the direct SAML 2.0 federation pattern; Cognito identity pools are for app/mobile credential exchange, not console SSO.
- **Result:** Correct (100%).
- **Fair:** Yes. The Cognito option is a realistic trap for someone who only pattern-matches "federation → Cognito"; the explanation states plainly that Cognito identity pools don't provide AWS Console SSO, which is worth knowing and not obvious from the option wording alone.
- **Explanation useful:** Yes.

## Fairness percentage

7 / 7 questions fair = **100%** (target ≥ 90%, met).

All seven were single-best-answer scenario questions with distractors that fail for specific, statable
reasons (a wrong service, a misapplied AWS mechanism, or a violated stated constraint) rather than
vague "less good" alternatives. None were answerable purely from wording tricks or elimination of
obviously silly options — each required knowing a specific fact about IAM/STS/Organizations mechanics.
All explanations matched the on-screen choices exactly and added at least one fact I did not already
know going in.

## Anything confusing

- **Drill-linking gap:** The lesson page's "Drills for this lesson" list for 1.1 shows only the `-mc`
  id for K04 (`q-saa-1-1-k04-mc`) and the `-mc` id for S03 (`q-saa-1-1-s03-mc`), but this review was
  asked to check `q-saa-1-1-k04-mr` and `q-saa-1-1-s03-mr` — different questions that exist and work
  correctly but are not reachable by clicking through from the lesson page itself (only from the Exam
  drills tab's full list, or a direct `?q=` link). A student following the lesson page's own links would
  never see these two `-mr` drills. This looks like a lesson↔drill link gap rather than a question
  quality problem, and I'm flagging it as a change request rather than working around it.
- **Generic lesson prose:** Every K-bullet on the lesson page repeats the identical "Tradeoffs..."
  paragraph verbatim, and every S-bullet repeats the identical "Applied practice..." paragraph verbatim.
  This is fine as scaffolding but doesn't teach the specific mechanics that the drills then test (e.g.
  nothing on the lesson page mentions that SCPs bind the root user, or that IAM groups can't nest) — the
  citation link is the only place a student is pointed to go deeper. Not a fairness problem for the
  drills themselves (each drill's own explanation was self-contained and taught the needed fact), just a
  gap between lesson depth and drill difficulty.
- **UI mechanic:** Finding a specific drill by id required using the Exam drills tab's full list (429
  items rendered on one page) rather than a direct single-question view — the `?q=` param only
  highlights/scrolls to the right card, it doesn't filter the list. Not a fairness issue, just slow to
  navigate as a student.

## Overall: approve
