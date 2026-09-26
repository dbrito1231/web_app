# AWS Solutions Architect review — lesson 1.2 (rewrite, commit d97b9c0)

Reviewer: Senior AWS Solutions Architect role (read-only).
Scope: `content/lessons/lesson-1-2.json` `bodyMarkdown` (all 10 sections, K01–K06 + S01–S04), against `content/objectives/saa_c03.json` `SAA-1.2-*` bullets, and the 14 `citationIds` files. Quality bar: approved `content/lessons/lesson-1-1.json`.

## 1. Fact-check findings

| # | Location | Problem | Exact fix | Doc URL | Severity |
|---|---|---|---|---|---|
| AWS-L12-001 | K01, sentence: "can automatically rotate a supported secret on a schedule using a Lambda function it manages" | Overstates AWS ownership of the rotation Lambda. Per AWS docs, when you turn on rotation (outside the separate "managed rotation" feature for a small set of native database integrations), **Secrets Manager invokes a Lambda function that is deployed and billed in your own account** — either one you author or one created from an AWS-supplied template — not a function "AWS manages" for you generically. "It manages" is only accurate for the distinct managed-rotation path (e.g., some RDS/Redshift/DocumentDB secrets), which the lesson does not name. | Replace with: "…can automatically rotate a supported secret on a schedule. Secrets Manager invokes a Lambda rotation function to do this — for a handful of native database integrations (managed rotation) that function is created and run for you; for everything else, Secrets Manager deploys and invokes a rotation function in your own account, and you pay the normal Lambda charge for it." | https://docs.aws.amazon.com/secretsmanager/latest/userguide/intro.html (see "Pricing" section: "Secrets Manager uses an AWS Lambda function to rotate the secret, and you are charged for the rotation function") | Medium |

No other statement in the ten sections (K01–K06, S01–S04) was found to be factually wrong, outdated, or misleading. The remaining claims I specifically checked against docs — Parameter Store's `SecureString`/no-rotation behavior, gateway vs. interface endpoints, security-group/NACL statefulness and the documented DNS-filtering exception, GuardDuty's foundational data sources, WAF's protected resource types, Shield Standard/Advanced scope, and Direct Connect/Site-to-Site VPN mechanics — all matched current AWS documentation. Two items are borderline-imprecise but not wrong enough to log as separate findings:

- K05/K06's GuardDuty protection-plan list ("Amazon S3, Amazon EKS, Amazon RDS, and AWS Lambda") and WAF's protectable-resource list ("CloudFront…, an Application Load Balancer, an API Gateway REST API, an AppSync GraphQL API, or a Cognito user pool") are both accurate but non-exhaustive (GuardDuty also has EC2 Runtime Monitoring and Malware Protection for EBS/S3/Backup; WAF also protects App Runner, Amplify, Verified Access, and Bedrock AgentCore Gateway). The lesson never claims either list is exhaustive, so this is not logged as a defect — flagging only for awareness.
- S04's Site-to-Site VPN description omits that dynamic BGP routing is the norm for the customer-gateway/virtual-private-gateway or transit-gateway session; the lesson only says "two tunnels per connection for redundancy," which is correct but a routing-mode detail is left out. Not required by the SAA-1.2-S04 bullet text, so not logged.

**Statements verified:** 46 distinct factual claims verified across the ten sections, using the 14 cited pages plus 3 additional lookups (AWS WAF protected-resource list, AWS Shield Standard/Advanced coverage and protected-resources policy, and the Parameter Store vs. Secrets Manager vs. AppConfig comparison table) via the AWS Documentation MCP (`search_documentation` / `read_documentation`).

## 2. Coverage review

All ten `SAA-1.2-*` objective bullets get a dedicated, correctly labeled section (K01–K06, S01–S04), matching the lesson-1-1 pattern of one `###` heading per objective ID plus an "Exam tip" callout. Objective-bullet text vs. section content:

- **K01** (config/credential security) — covers Secrets Manager, Parameter Store, and the IAM-role alternative. Correct contrast, only the AWS-L12-001 nuance above.
- **K02** (service endpoints) — gateway vs. interface/PrivateLink endpoints correctly contrasted (S3/DynamoDB only, route-table vs. ENI, cost, endpoint policies).
- **K03** (ports/protocols/traffic control) — security groups vs. NACLs correctly contrasted (stateful/resource vs. stateless/subnet, numbered rules, default-allow NACL, DNS/DHCP/metadata exception). Matches AWS docs exactly, including the specific documented DNS-filtering exception.
- **K04** (secure application access) — IAM roles, Cognito user pools vs. identity pools, API Gateway authorizers, and the IAM Identity Center hand-off to task 1.1 are all correctly scoped and none overlap incorrectly.
- **K05** (security services) — Cognito vs. GuardDuty vs. Macie contrasted correctly: GuardDuty's data sources and account/network scope vs. Macie's S3-only sensitive-data/misconfiguration scope. This is one of the "commonly confused services" triads named in the task and it is handled well.
- **K06** (external threat vectors) — DDoS/Shield and SQL injection–XSS/WAF pairing is correct, including Shield Standard (free, automatic, L3/4) vs. Shield Advanced (paid, broader resource list, cost protection, SRT) — matches the "Shield Advanced protections are only enabled for resources you explicitly specify" doc, though the lesson doesn't state the opt-in requirement explicitly (minor, not required by the bullet).
- **S01–S04** — VPC security-component design, segmentation strategy (public/private/isolated subnets), integrating multiple security services, and VPN vs. Direct Connect are all present, each with a closing exam tip that maps the scenario language to the right service, consistent with the S01–S06 pattern in lesson 1.1.

Commonly confused pairs named in the review task:
- Security groups vs. NACLs — correct, matches lesson-1-1's own SG explanation with no drift.
- WAF vs. Shield vs. Firewall Manager — WAF vs. Shield is covered and correct; **Firewall Manager is not mentioned**, but Firewall Manager is not named in any `SAA-1.2-*` bullet text (it appears only inside the AWS WAF doc's title, not the exam objective), so this is not a gap against the objective bullets.
- GuardDuty vs. Inspector vs. Macie — GuardDuty vs. Macie is covered and correct; **Inspector is not mentioned**, and Inspector likewise is not named in the `SAA-1.2-K05` bullet text (`text` lists only "Amazon Cognito, Amazon GuardDuty, Amazon Macie" as examples), so this is not a gap against the objective, only a note for anyone drilling the broader "detective services" triad.
- Secrets Manager vs. Parameter Store — covered and correct (see AWS-L12-001 nuance).
- VPN vs. Direct Connect — covered and correct, including the combined-use case (VPN over a Direct Connect public VIF, or VPN as failover).
- VPC endpoints (gateway vs. interface) — covered and correct.

Exam tips: all seven exam-tip callouts correctly restate the section's core discriminator in "if the scenario says X, answer Y" form, consistent with lesson-1-1's tip style, and none contain an incorrect mapping.

## 3. Citation check

All 14 `citationIds` in `content/lessons/lesson-1-2.json` resolve to existing files under `content/citations/`:

`cite-saa-1-2-secrets-manager`, `cite-saa-1-2-parameter-store`, `cite-saa-1-2-privatelink`, `cite-saa-1-2-security-groups`, `cite-saa-1-2-nacl`, `cite-saa-1-2-nat-gateway`, `cite-saa-1-2-subnets`, `cite-saa-1-2-cognito`, `cite-saa-1-2-guardduty`, `cite-saa-1-2-macie`, `cite-saa-1-2-waf`, `cite-saa-1-2-shield`, `cite-saa-1-2-vpn`, `cite-saa-1-2-direct-connect`.

Each citation's `url` is a live, correctly scoped official AWS doc page (docs.aws.amazon.com) matching its `note` field's claim area, and each page does support the claims made in the corresponding lesson section (spot-checked all 14 during this review). No dead, mismatched, or unofficial (non-`docs.aws.amazon.com`) citation found.

## Overall: approve

One medium-severity precision fix (AWS-L12-001, Secrets Manager rotation Lambda ownership) should be applied, but nothing in the lesson is wrong enough, or misaligned enough with the `SAA-1.2-*` objective bullets, to block approval. Coverage, contrasts, and exam tips meet the lesson-1-1 quality bar.
