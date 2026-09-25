# Citation sample re-check (Phase 6)

Date: 2026-09-24  
Method: **AWS Knowledge MCP** (`aws___search_documentation`, `aws___read_documentation`, `aws___get_regional_availability`) and **Terraform registry MCP** via Docker gateway (`get_latest_provider_version`, `search_providers`, `get_provider_details`).  
Not used: AWS API MCP / any provisioning tools (plan §9). Live AWS lab commands remain **unexecuted**.

## AWS Knowledge MCP samples

| Claim (workbook) | MCP evidence | Result |
| --- | --- | --- |
| Do not use root for everyday tasks; MFA; no root access keys | `read_documentation` → https://docs.aws.amazon.com/IAM/latest/UserGuide/root-user-best-practices.html — “Don't create access keys for the root user”; create admin for everyday tasks | **Confirmed** |
| IAM best-practice reinforce | `search_documentation` “IAM root user best practices…” → https://aws.amazon.com/iam/resources/best-practices/ | **Confirmed** |
| S3 Block Public Access on by default for new buckets | `search_documentation` → Block Public Access settings / console help | **Confirmed** |
| NAT Gateway ~$0.045/hour + data processing; partial hour = full hour | `search_documentation` → https://aws.amazon.com/vpc/pricing/ (example rate $0.045/hour in cited region example) | **Confirmed** (learner must re-read live pricing for their region) |
| EKS standard support $0.10/cluster-hour; extended $0.60 | `search_documentation` → https://aws.amazon.com/eks/pricing/ | **Confirmed** |
| Lab default region `us-east-1` has EKS, EC2, Lambda | `get_regional_availability` products filter exact names → all `isAvailableIn` | **Confirmed** |
| SAA-C03 domains 30/26/24/20; MC/MR; scaled pass 720; 50 scored + 15 unscored | `read_documentation` → official exam guide HTML | **Confirmed** (matches plan baseline) |

## Terraform registry MCP samples

| Claim (workbook) | MCP evidence | Result |
| --- | --- | --- |
| Pin `hashicorp/aws` 6.x; fixture uses `~> 6.0` | `get_latest_provider_version` namespace=`hashicorp` name=`aws` → **6.66.0** | **Confirmed** (6.x; matches prior local validate) |
| `aws_s3_bucket` is current provider resource | `search_providers` + `get_provider_details` doc id `13748781` on provider **6.66.0** | **Confirmed** |
| `aws_iam_role` is current provider resource | `search_providers` + `get_provider_details` doc id `13748255` on provider **6.66.0** | **Confirmed** |

## Citation file updates

- All `content/citations/cite-*.json` notes refreshed `accessed: 2026-09-24` with MCP sample-pass note.
- Added `content/citations/cite-tf-aws-provider.json` for registry pin evidence.

## Remaining (intentionally open)

- Full 429-question bank is still `mcpStatus: pending_recheck` except where unmarked; Phase 6 gate is **sample** re-check, not per-item MCP polish.
- Curriculum registry stays `implemented_unverified` until human review maps each of 189 bullets to MCP-backed stems (plan: verified only with evidence).
- Edition variance (AppSync / Kendra / Audit Manager vs supplied PDF) unchanged; PDF remains authoritative.
- Agents did **not** call AWS APIs, CLI, or credentialed Terraform.
