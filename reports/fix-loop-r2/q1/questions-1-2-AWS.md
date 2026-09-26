# AWS Solutions Architect review — task 1.2 questions (16 rewritten, commit a324a5a)

Reviewer: Senior AWS Solutions Architect role (read-only). Date: 2026-09-26.
Scope: the 16 files `content/questions/q-saa-1-2-*.json`, the lesson 1.2 changes in the same commit (`content/lessons/lesson-1-2.json` K01 rotation wording + K02/S04 pricing additions), the 3 new citation files, and the author notes `reports/fix-loop-r2/q1/questions-1-2-impl.md`. Quality bar: the approved pilot `content/questions/q-saa-1-1-*.json` (`reports/fix-loop-r2/q1-pilot/AWS.md`) and the lesson-1-2 fact-check in `reports/fix-loop-r2/q1/lesson-1-2-AWS.md`.

Method:
- Solved each question cold against the stated constraints before checking the listed key.
- Verified every load-bearing claim (Secrets Manager rotation billing/ownership, Parameter Store's lack of rotation, gateway vs. interface endpoint scope/cost, VPC endpoint policy attachment point, security group vs. NACL statefulness, Cognito user pool vs. identity pool, GuardDuty vs. Macie scope, WAF vs. Shield Standard/Advanced scope, isolated/private/public subnet definitions, NAT gateway subnet requirement, Site-to-Site VPN vs. Direct Connect mechanics/billing) via the AWS Documentation MCP (`search_documentation`).
- All 17 `citationIds` referenced across the 16 files (14 pre-existing + `cite-saa-1-2-vpc-endpoint-billing`, `cite-saa-1-2-direct-connect-pricing`, `cite-saa-1-2-iam-role-ec2`) resolve to existing files under `content/citations/`, each pointing to a `docs.aws.amazon.com` URL that supports the claim it's cited for.
- No AWS calls were made, no files other than this report were written.

## Per-question results

| ID | Key correct | Rating | Issues / notes | Doc URL |
|---|---|---|---|---|
| q-saa-1-2-k01-mc | y (a) | Exam-realistic and correct | Secrets Manager + rotation is the only choice that both removes the hardcoded credential and gets code-change-free rotation. Parameter Store correctly ruled out for having no built-in rotation. AMI-baking and image-pull-restriction distractors are well-built (still hardcoded, still no rotation). | secretsmanager/latest/userguide/intro.html |
| q-saa-1-2-k02-mc | y (b) | Exam-realistic and correct | Gateway endpoint is verified "free of charge" for S3/DynamoDB (AWS docs: "provides reliable connectivity... free of charge"). NAT gateway requires a public subnet (verified) and is billed hourly — correctly ruled out on cost. Interface endpoint correctly ruled out on cost (endpoint-hour + per-GB), consistent with the new lesson K02 sentence. | vpc/latest/privatelink/gateway-endpoints.html; vpc/latest/userguide/vpc-billing-usage-reports.html |
| q-saa-1-2-k02-mr | y (b, e) | Exam-realistic and correct | Gateway endpoints are S3/DynamoDB only (verified); Kinesis Data Streams correctly requires an interface endpoint. Endpoint policies attach to the VPC endpoint itself, not a Lambda execution role — verified against multiple AWS "VPC endpoint policy" pages, all describing the policy as attached to the endpoint. | vpc/latest/privatelink/vpc-endpoints-ddb.html |
| q-saa-1-2-k03-mc | y (c) | Exam-realistic and correct | NACL numbered deny at subnet level is the only option that blocks one instance's IP for every other instance without touching security groups. Distractor (d), "security group removal changes statefulness," is a good misunderstands-mechanism trap — statefulness is a property of the SG mechanism itself, not something toggled off. | vpc/latest/userguide/vpc-network-acls.html |
| q-saa-1-2-k04-mc | y (d) | Exam-realistic and correct | Cognito user pool (auth) + identity pool (STS credential vending) is the standard exam pattern for per-end-user temporary AWS credentials. JWT-direct-to-S3 distractor (c) is a good misunderstands-mechanism trap: S3 does not accept a Cognito JWT. | cognito/latest/developerguide/what-is-amazon-cognito.html |
| q-saa-1-2-k05-mc | y (a) | Exam-realistic and correct | GuardDuty's CloudTrail/VPC-flow-log/DNS analysis is the documented mechanism for exactly this scenario (unrecognized temporary credentials + cryptomining-like traffic). Macie, Cognito, WAF are all clearly out of scope for account/network threat detection. | guardduty/latest/ug/what-is-guardduty.html |
| q-saa-1-2-k05-mr | y (c, e) | Exam-realistic and correct | Both Macie capabilities (public-bucket inventory + PII pattern matching) are correctly attributed and match the lesson text verbatim in spirit. Distractors correctly misattribute GuardDuty, Cognito, and WAF capabilities to Macie. | macie/latest/user/what-is-macie.html |
| q-saa-1-2-k06-mc | y (d) | Exam-realistic and correct | WAF managed rule group is the only content-inspecting control among the four; Shield Standard/Advanced are DDoS-focused (network/transport or volumetric layer-7), and a NACL cannot inspect payload content. Clean single-best-answer question. | waf/latest/developerguide/what-is-aws-waf.html |
| q-saa-1-2-s01-mc | y (c) | Exam-realistic and correct | NAT gateway in a public subnet with the private subnet's route pointing to it is the textbook one-way-outbound pattern. SG/NACL distractors correctly note that a resource- or subnet-level allow rule cannot create a route where none exists — this is an accurate and non-trivial distinction. | vpc/latest/userguide/vpc-nat-gateway.html |
| q-saa-1-2-s01-mr | y (a, d) | Exam-realistic and correct | Tightened security group + custom NACL is standard defense-in-depth without a subnet redesign. "Remove the route table" and "disable the default NACL" distractors are correctly identified as breaking connectivity rather than adding a layer, and NAT-gateway relocation correctly does nothing for east-west traffic. | vpc/latest/userguide/vpc-security-groups.html |
| q-saa-1-2-s02-mc | y (a) | Exam-realistic and correct | "Isolated subnet" (no route to an IGW or NAT gateway) is verified AWS terminology (VPC User Guide "Subnet types": "A subnet with no routes to destinations outside its VPC"). This is the only listed design with zero internet path, matching the strict no-outbound requirement. The NACL distractor (d) correctly notes the route table, not the NACL, determines whether a path exists at all. | vpc/latest/userguide/configure-subnets.html |
| q-saa-1-2-s02-mr | y (b, d) | Exam-realistic and correct | Public subnet for the load balancer + isolated subnet for the database is the correct pairing for the stated two-sided requirement. All three distractors are clear misplacements. | vpc/latest/userguide/configure-subnets.html |
| q-saa-1-2-s03-mc | y (d) | Exam-realistic and correct | Secrets Manager is the only choice that touches credential storage at all; WAF, Shield Advanced, and IAM Identity Center are all real services addressing genuinely different layers, which is a good exam-realistic distractor set (not strawmen). | secretsmanager/latest/userguide/intro.html |
| q-saa-1-2-s03-mr | y (a, c) | Exam-realistic and correct | WAF (content) + Secrets Manager (credential) correctly map one-to-one onto the two stated gaps. Shield Standard, IAM Identity Center, and AMI-baking are all correctly ruled out for reasons specific to what each gap actually needs. | waf/latest/developerguide/what-is-aws-waf.html |
| q-saa-1-2-s04-mc | y (b) | Exam-realistic and correct | Site-to-Site VPN is quick to provision and runs over the internet, fitting a two-day deadline with tolerated variable latency; Direct Connect's longer provisioning (colocation/partner) correctly rules it out for the timeline. Interface endpoint and NAT gateway distractors are correctly identified as not providing site-to-site connectivity at all. | vpn/latest/s2svpn/VPC_VPN.html; directconnect/latest/UserGuide/Welcome.html |
| q-saa-1-2-s04-mr | y (b, d) | Exam-realistic and correct | Two-tunnel redundancy and VPN-over-DX-public-VIF are both accurate standalone and combined-use facts. The three false statements (DX encrypts by default, VPN has more consistent bandwidth/latency than DX, DX billed per connection-hour like VPN) are each a clean, verified reversal of a real fact — matches the lesson's S04 pricing/mechanics sentence added in this same commit. | directconnect/latest/PricingGuide/full.html |

## Lesson 1.2 change verification

- **K01 rotation wording (AWS-L12-001 fix):** the new sentence ("Secrets Manager invokes a Lambda rotation function to do this — for a handful of native database integrations (managed rotation) that function is created and run for you; for everything else, Secrets Manager deploys and invokes a rotation function in your own account, and you pay the normal Lambda charge for it") is accurate and matches the fix specified in the earlier `lesson-1-2-AWS.md` review. Confirmed again against `secretsmanager/latest/userguide/intro.html`.
- **K02 addition** ("Unlike a gateway endpoint, an interface endpoint is billed per endpoint-hour plus a per-GB data processing charge."): accurate, matches `vpc-billing-usage-reports.html` and PrivateLink pricing.
- **S04 addition** ("Direct Connect is billed through port-hour capacity charges for the connection plus data transfer out, not the per-connection-hour model that Site-to-Site VPN uses."): accurate, matches `directconnect/latest/PricingGuide/full.html`.
- `drillIds` now lists all 16 questions (previously missing the 6 MR variants) — confirmed against the lesson file's current `drillIds` array.
- All 3 new citation files (`cite-saa-1-2-vpc-endpoint-billing`, `cite-saa-1-2-direct-connect-pricing`, `cite-saa-1-2-iam-role-ec2`) exist, point to live `docs.aws.amazon.com` URLs, and their `note` fields accurately describe the claim each supports.

## Summary metrics

- Key correct: **16/16**. No MC item has a second defensible answer under its stated constraints; every MR key set is exact and complete.
- Rated "exam-realistic and correct": **16/16 = 100%** (target ≥ 95%).
- Factual errors found: **0**. Every checked claim — including the two new lesson-body pricing sentences these questions depend on — matches current AWS documentation.
- Every question tests its mapped `objectiveIds` (`content/objectives/saa_c03.json`, SAA-1.2-K01…S04), and none leans on an untaught concept: the impl notes' teach-before-test keyword scan is consistent with what this review found in the lesson body.
- Citations: all 17 referenced `citationIds` resolve to existing files with `docs.aws.amazon.com` URLs.

## Required fixes

None. No factual errors, ambiguous keys, or unsupported citations were found.

## Recommended (non-blocking) improvements

1. **q-saa-1-2-s04-mc (optional):** the stem's "tolerate the variable latency of a connection that runs over the public internet" is a slightly stronger tell than the pilot's subtlest items — a harder version could drop the latency-tolerance clue and let the two-day deadline alone drive the key. Not required; the current version is still exam-realistic.
2. **q-saa-1-2-k02-mc / k02-mr (optional):** consider a future citation split so `cite-saa-1-2-privatelink` and `cite-saa-1-2-vpc-endpoint-billing` aren't both cited for the same cost claim in k02-mc when only the billing citation is strictly needed for that sentence — purely a citation-hygiene nit, not a factual issue.

Any of these edits would require re-review under the freeze rule.

## Overall: approve
