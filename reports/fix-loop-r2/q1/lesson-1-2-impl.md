# Lesson 1.2 rewrite — implementation notes

Scope: `content/lessons/lesson-1-2.json` (`bodyMarkdown` and `citationIds` only; `title`, `module`, `objectiveIds`, `drillIds`, `labIds`, `exerciseIds` unchanged) plus 14 new citation files `content/citations/cite-saa-1-2-*.json`. Questions were not touched.

## Section outline (objective → section)

| Objective | Section heading | Core concepts taught |
|---|---|---|
| SAA-1.2-K01 | K01 — Application configuration and credentials security | AWS Secrets Manager (rotation, credential-shaped secrets) vs Systems Manager Parameter Store (`SecureString`, no rotation, general config) vs IAM roles (no stored credential at all) |
| SAA-1.2-K02 | K02 — AWS service endpoints | VPC gateway endpoints (S3/DynamoDB only, route-table based, free) vs interface endpoints / AWS PrivateLink (ENI, private DNS, endpoint policies) |
| SAA-1.2-K03 | K03 — Control ports, protocols, and network traffic on AWS | Security groups (stateful, resource-level, allow-only) vs network ACLs (stateless, subnet-level, numbered allow/deny rules, default-allow NACL) |
| SAA-1.2-K04 | K04 — Secure application access | IAM roles for resource-to-resource calls; Cognito user pools (JWTs) + identity pools (STS credentials) for app end users; API Gateway authorizers; IAM Identity Center reserved for workforce access |
| SAA-1.2-K05 | K05 — Security services with appropriate use cases | Cognito (app identity) vs GuardDuty (account/network threat detection: CloudTrail, VPC flow logs, DNS logs, protection plans) vs Macie (S3-scoped sensitive-data and bucket-misconfiguration discovery) |
| SAA-1.2-K06 | K06 — Threat vectors external to AWS | DDoS (layer 3/4/7) countered by Shield Standard (automatic, free) / Shield Advanced (paid, broader coverage, cost protection, SRT); SQL injection/XSS countered by AWS WAF web ACL rules and managed rule groups; Shield+WAF combined for L7 DDoS |
| SAA-1.2-S01 | S01 — Designing VPC architectures with security components | Security groups, route tables (public vs NAT route), network ACLs, NAT gateways — each control mapped to the layer it operates at |
| SAA-1.2-S02 | S02 — Determining network segmentation strategies | Public subnet (route to IGW) vs private subnet (route to NAT gateway) vs isolated/VPN-only subnets; three-tier design example |
| SAA-1.2-S03 | S03 — Integrating AWS services to secure applications | Layered design combining Shield, WAF, IAM Identity Center, and Secrets Manager, each covering a distinct attack surface |
| SAA-1.2-S04 | S04 — Securing external network connections to and from the AWS Cloud | Site-to-Site VPN (IPsec, customer gateway + virtual private/transit gateway, over the internet, fast to provision) vs Direct Connect (dedicated fiber, bypasses the internet, consistent bandwidth); the two combined |

Word count: 2,317 (in the 1,200–2,500 target range). Markdown uses only `##`/`###` headings, `- ` bullets, `**bold**`, and backticks — no tables, links, numbered lists, or single-asterisk italics (verified: 0 single-asterisk spans).

## Concepts drawn from each current (placeholder) question id

The existing `q-saa-1-2-*` files are all still the generic "Apply the objective directly" placeholders scheduled for a later question rewrite, so they carry no real distractor content yet. Their objective bindings were used only to confirm which K/S bullet each drill id maps to, which the lesson's `drillIds` list already reflected and was left unchanged:

- `q-saa-1-2-k01-mc` → K01 (credentials/config security)
- `q-saa-1-2-k02-mc`, `q-saa-1-2-k02-mr` → K02 (service endpoints)
- `q-saa-1-2-k03-mc` → K03 (ports/protocols/traffic control)
- `q-saa-1-2-k04-mc` → K04 (secure application access)
- `q-saa-1-2-k05-mc`, `q-saa-1-2-k05-mr` → K05 (security services: Cognito/GuardDuty/Macie)
- `q-saa-1-2-k06-mc` → K06 (external threat vectors: DDoS, SQL injection)
- `q-saa-1-2-s01-mc`, `q-saa-1-2-s01-mr` → S01 (VPC security component design)
- `q-saa-1-2-s02-mc`, `q-saa-1-2-s02-mr` → S02 (network segmentation)
- `q-saa-1-2-s03-mc`, `q-saa-1-2-s03-mr` → S03 (integrating security services)
- `q-saa-1-2-s04-mc`, `q-saa-1-2-s04-mr` → S04 (external connections: VPN/Direct Connect)

## Doc URLs fetched and cited

- https://docs.aws.amazon.com/secretsmanager/latest/userguide/intro.html (`cite-saa-1-2-secrets-manager`)
- https://docs.aws.amazon.com/systems-manager/latest/userguide/systems-manager-parameter-store.html (`cite-saa-1-2-parameter-store`)
- https://docs.aws.amazon.com/vpc/latest/privatelink/concepts.html (`cite-saa-1-2-privatelink`)
- https://docs.aws.amazon.com/vpc/latest/userguide/vpc-security-groups.html (`cite-saa-1-2-security-groups`)
- https://docs.aws.amazon.com/vpc/latest/userguide/vpc-network-acls.html (`cite-saa-1-2-nacl`)
- https://docs.aws.amazon.com/vpc/latest/userguide/vpc-nat-gateway.html (`cite-saa-1-2-nat-gateway`)
- https://docs.aws.amazon.com/vpc/latest/userguide/configure-subnets.html (`cite-saa-1-2-subnets`)
- https://docs.aws.amazon.com/cognito/latest/developerguide/what-is-amazon-cognito.html (`cite-saa-1-2-cognito`)
- https://docs.aws.amazon.com/guardduty/latest/ug/what-is-guardduty.html (`cite-saa-1-2-guardduty`)
- https://docs.aws.amazon.com/macie/latest/user/what-is-macie.html (`cite-saa-1-2-macie`)
- https://docs.aws.amazon.com/waf/latest/developerguide/what-is-aws-waf.html (`cite-saa-1-2-waf`)
- https://docs.aws.amazon.com/waf/latest/developerguide/ddos-overview.html (`cite-saa-1-2-shield`)
- https://docs.aws.amazon.com/vpn/latest/s2svpn/VPC_VPN.html (`cite-saa-1-2-vpn`)
- https://docs.aws.amazon.com/directconnect/latest/UserGuide/Welcome.html (`cite-saa-1-2-direct-connect`)

All 14 fetched on 2026-09-26 via WebFetch against docs.aws.amazon.com and used to check every factual claim in the corresponding lesson section before writing it (stateful vs stateless behavior, gateway vs interface endpoints, Shield Standard vs Advanced coverage, GuardDuty data sources, Macie's S3 scope, Cognito user pool vs identity pool roles, VPN tunnel/gateway components, Direct Connect virtual interface types).

## Verification performed

- `json.load` round-trip; file rewritten with `json.dumps(data, indent=2, ensure_ascii=True) + "\n"`, UTF-8 text mode, via `backend\.venv\Scripts\python.exe`.
- 0 single-asterisk spans; no numbered lists, tables, or markdown links in `bodyMarkdown`.
- All 14 `citationIds` resolve to existing files under `content/citations/`.
- `python scripts\content_lint.py` → `PASS` (429 questions, 21+21 labs, 23 lessons).
