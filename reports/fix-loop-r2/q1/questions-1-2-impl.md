# Q1 implementation — SAA task 1.2 (lesson fix + 16-question rewrite)

Scope: `content/lessons/lesson-1-2.json` (AWS-L12-001 fix + two small doc-verified additions), the 16 `content/questions/q-saa-1-2-*.json` files (full rewrite from placeholder stubs), and 3 new citation files. Follows Amendment 3 of `.cursor/plans/lead_dev_fix_loop_round2_20260926.plan.md`, modeled on the approved pilot `content/questions/q-saa-1-1-*.json`.

## 1. Lesson fix (AWS-L12-001)

**Before (K01):** "...can automatically rotate a supported secret on a schedule **using a Lambda function it manages**. An application makes a runtime call..."

**After (K01):** "...can automatically rotate a supported secret on a schedule. Secrets Manager invokes a Lambda rotation function to do this — for a handful of native database integrations (managed rotation) that function is created and run for you; for everything else, Secrets Manager deploys and invokes a rotation function in your own account, and you pay the normal Lambda charge for it. An application makes a runtime call..."

Verified against `https://docs.aws.amazon.com/secretsmanager/latest/userguide/intro.html` ("Pricing" section: "When you turn on automatic rotation (except managed rotation), Secrets Manager uses an AWS Lambda function to rotate the secret, and you are charged for the rotation function...") via the AWS Documentation MCP (`search_documentation` / `read_documentation`). Matches the exact fix specified in `reports/fix-loop-r2/q1/lesson-1-2-AWS.md`.

**Two small additions** (teach-before-test, both doc-verified) needed to support new question distractors:
- K02: added "Unlike a gateway endpoint, an interface endpoint is billed per endpoint-hour plus a per-GB data processing charge." — verified via `docs.aws.amazon.com/vpc/latest/userguide/vpc-billing-usage-reports.html` and AWS PrivateLink pricing search results (endpoint-hour + per-GB).
- S04: added "Direct Connect is billed through port-hour capacity charges for the connection plus data transfer out, not the per-connection-hour model that Site-to-Site VPN uses." — verified via `docs.aws.amazon.com/directconnect/latest/PricingGuide/full.html` ("Capacity (port-hour) charges", "Data transfer out (DTO)").

New citations added: `cite-saa-1-2-vpc-endpoint-billing`, `cite-saa-1-2-direct-connect-pricing`, plus `cite-saa-1-2-iam-role-ec2` (IAM roles for EC2, used by K01/K04 questions). Lesson `citationIds` and `drillIds` updated (`drillIds` now lists all 16 questions, including the 6 MR variants that were missing).

## 2. Question rewrite — metrics

- **Distractor-type table** (bucket = question count in which the bucket appears at least once; max allowed 3):

| Distractor type | Questions | Count |
|---|---|---|
| missing-capability (feature/service can't do what's claimed) | k01-mc, k02-mr, k03-mc | 3 |
| wrong-mechanism-cost (NAT/interface endpoint misused or costly) | k02-mc, k02-mr, s04-mc | 3 |
| contradicts-requirement | k02-mc, s01-mc, s02-mr | 3 |
| still-insecure-practice (still hardcoded / long-term creds) | k01-mc, k04-mc, s03-mr | 3 |
| wrong-threat-type (Shield vs injection/credential gap) | k06-mc, s03-mc, s03-mr | 3 |
| wrong-service-scope (Macie/Cognito/GuardDuty mixed up) | k05-mc, k05-mr | 2 |
| wrong-population (workforce vs app users vs per-user) | k04-mc, s03-mc, s03-mr | 3 |
| wrong-subnet-type | s02-mc, s02-mr | 2 |
| misunderstands-mechanism | k03-mc, s01-mr | 2 |
| wrong-service-attribution | k05-mr | 1 |
| wrong-default-assumption | k03-mc | 1 |
| wrong-credential-type | k04-mc | 1 |
| cant-inspect-content | k06-mc | 1 |
| wrong-layer-insufficient (SG/NACL can't create a route) | s01-mc | 1 |
| overcorrection-breaks-function | s01-mr | 1 |
| irrelevant-to-goal | s01-mr | 1 |
| fails-strict-requirement | s02-mc | 1 |
| wrong-control-for-goal | s02-mc | 1 |
| unnecessary-exposure | s02-mr | 1 |
| timeline-mismatch | s04-mc | 1 |
| wrong-scope-for-goal | s04-mc | 1 |
| false-default-claim | s04-mr | 1 |
| reversed-comparison | s04-mr | 1 |
| attribute-swap | s04-mr | 1 |

No type exceeds 3 of the 16 questions.

- **Longest-choice-is-key rate (MC, 10 questions):** 3/10 = 30% (≤ 35% target). Longest choice is the key on k04-mc, k05-mc, s01-mc only.
- **MC key-letter distribution (10 questions):** a=3, b=2, c=2, d=3.
- **MR key-position distribution (6 questions × 2 keys = 12 slots):** a=2, b=3, c=2, d=3, e=2.
- **Stem 6-word openings:** all 16 unique (verified programmatically, no collisions).
- **Letter references in rationale:** 0 (verified with a regex scan for "choice/option/answer <letter>" and "letter X" patterns; every rationale explains distractors by content).
- **Objective text pasted into stem or choices:** 0 (verified by checking each question's stem/choices against the exact `SAA-1.2-*` objective `text` field).
- **Citations / verification fields:** all 16 questions have non-empty `citationIds`, `mcpStatus: "verified"`, `reviewedOn: "2026-09-26"`.
- **Teach-before-test:** every concept named in a distractor's rationale (Secrets Manager, Parameter Store, IAM roles/instance profiles, gateway vs. interface endpoints + their cost model, endpoint policies, security groups vs. NACLs (stateful/stateless, default-allow NACL), Cognito user pool vs. identity pool, GuardDuty vs. Macie vs. Cognito scope, Shield Standard/Advanced vs. WAF, NAT gateway/route tables/public-private-isolated subnets, IAM Identity Center, Site-to-Site VPN vs. Direct Connect including the two pricing facts added above) is present in `lesson-1-2.json`'s `bodyMarkdown` — verified by a keyword-presence scan against the lesson text.
- **`scripts\content_lint.py`:** PASS (`questions 429 aws 310 tf 119`, `lessons 23`, module-level MC key-balance check unaffected — top key for module A1 is `d` at 56/190 = 29.5%, well under the 45% ceiling).

## 3. Per-question summary

| Question | Objective | Tests | Key | Doc URL(s) |
|---|---|---|---|---|
| q-saa-1-2-k01-mc | K01 | Secrets Manager rotation vs. Parameter Store's lack of rotation vs. still-hardcoded alternatives | a (Secrets Manager + rotation) | secretsmanager/.../intro.html |
| q-saa-1-2-k02-mc | K02 | Gateway endpoint (S3, free, route-table) vs. NAT gateway/interface endpoint cost vs. making the subnet public | b (gateway endpoint) | vpc/.../privatelink/concepts.html; vpc/.../vpc-nat-gateway.html |
| q-saa-1-2-k02-mr | K02 | Gateway endpoint scope (S3/DynamoDB only) vs. interface endpoint for other services vs. endpoint-policy attachment point | a, e | vpc/.../privatelink/concepts.html |
| q-saa-1-2-k03-mc | K03 | NACL numbered deny at subnet level vs. security groups' allow-only limitation vs. default-NACL behavior | c (NACL deny rule) | vpc/.../vpc-network-acls.html; vpc/.../vpc-security-groups.html |
| q-saa-1-2-k04-mc | K04 | Cognito user pool + identity pool for per-end-user temporary AWS credentials vs. long-term keys vs. EC2 role population mismatch | d (user pool + identity pool) | cognito/.../what-is-amazon-cognito.html; IAM/.../id_credentials_temp.html |
| q-saa-1-2-k05-mc | K05 | GuardDuty's data sources/use case vs. Macie's S3-only scope vs. Cognito vs. WAF | a (GuardDuty) | guardduty/.../what-is-guardduty.html; macie/.../what-is-macie.html |
| q-saa-1-2-k05-mr | K05 | Macie's S3 inventory + PII discovery capabilities vs. GuardDuty/Cognito/WAF capabilities misattributed to Macie | c, e | macie/.../what-is-macie.html; guardduty/.../what-is-guardduty.html |
| q-saa-1-2-k06-mc | K06 | WAF managed rule group for SQL injection vs. Shield Standard/Advanced (DDoS-only) vs. NACL's inability to inspect content | d (WAF) | waf/.../what-is-aws-waf.html; waf/.../ddos-overview.html |
| q-saa-1-2-s01-mc | S01 | NAT gateway for one-way private-subnet outbound access vs. SG/NACL's inability to create a route vs. an internet gateway making the subnet public | c (NAT gateway) | vpc/.../vpc-nat-gateway.html |
| q-saa-1-2-s01-mr | S01 | Tightening the security group + adding a custom NACL for defense in depth vs. overcorrections that break connectivity | a, d | vpc/.../vpc-security-groups.html; vpc/.../vpc-network-acls.html |
| q-saa-1-2-s02-mc | S02 | Isolated subnet (no route in or out) vs. private-with-NAT (still has outbound) vs. public subnet vs. NACL-as-route-substitute | a (isolated subnet) | vpc/.../configure-subnets.html |
| q-saa-1-2-s02-mr | S02 | Public subnet for an internet-facing load balancer + isolated subnet for the database vs. wrong placements | b, d | vpc/.../configure-subnets.html |
| q-saa-1-2-s03-mc | S03 | Secrets Manager for a hard-coded-credential gap specifically, vs. WAF/Shield/IAM Identity Center addressing different layers | d (Secrets Manager) | secretsmanager/.../intro.html; waf/.../what-is-aws-waf.html |
| q-saa-1-2-s03-mr | S03 | WAF (SQL injection) + Secrets Manager (hard-coded password) as the two matching fixes vs. Shield/IAM Identity Center/AMI-baking mismatches | a, d | waf/.../what-is-aws-waf.html; secretsmanager/.../intro.html |
| q-saa-1-2-s04-mc | S04 | Site-to-Site VPN for a fast, internet-path encrypted connection vs. Direct Connect's longer provisioning vs. PrivateLink/NAT gateway scope mismatch | b (Site-to-Site VPN) | vpn/.../VPC_VPN.html; directconnect/.../Welcome.html |
| q-saa-1-2-s04-mr | S04 | VPN's two-tunnel redundancy + VPN-over-Direct-Connect-public-VIF vs. reversed bandwidth claim, false DX-encrypts-by-default claim, and DX/VPN billing-model swap | b, d | vpn/.../VPC_VPN.html; directconnect/.../PricingGuide/full.html |

## 4. Verification method

Two scratch scripts were run (not committed, per instructions to keep helper scripts in the scratchpad):
- `build_q12.py` — generated all 16 question files with `json.dump(..., indent=2, ensure_ascii=True)` via `backend\.venv\Scripts\python.exe`.
- `verify_q12.py` — checked: id/type/module/objectiveIds/selectCount preservation; unique 6-word stem openings and "(Select TWO.)" on all MR stems; 4/5 choice counts; zero letter-reference patterns in rationale; zero pasted objective text; citation/verification fields present; MC key distribution and longest-is-key rate; MR key-position distribution; no choice-refers-to-choice phrasing; teach-before-test keyword coverage against the lesson body.

Result: `ALL CHECKS PASS`. `scripts\content_lint.py` also PASS after the changes.
