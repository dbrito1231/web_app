# UI journey — `/labs` + 13-lab paper walk

**URL:** http://127.0.0.1:5173/labs  
**Tool:** UI structure from `reports/evidence/ui/labs.md`; step detail from lab JSON (paper walk — no AWS CLI executed).

## Labs tab (UI)

- GL / UL pairs in one accordion; GL-01 shows **0/N steps**, **LIVE AWS**, cost estimate visible before reveal.
- Checkpoint buttons would POST progress — Gate 0: **403 Forbidden** (same CSRF issue as drills).
- UL-01 acceptance criteria visible without reveal: mentions **GL-03 bucket** and permissions boundary tied to GL-01 deny pattern (EV-STUDENT-210).

## Paper walk (13 labs)

| Lab | Title | Paper outcome | Blocker / note |
|-----|-------|---------------|----------------|
| GL-01 | Identity, budget, preflight | Would attempt after A0 | Step s06 **permissions boundary** — term not taught in 23 lessons (STUDENT-202) |
| GL-02 | Private S3 data controls | Runnable on paper | Clear teardown order |
| GL-03 | IAM role, STS, bucket | Runnable | Needed before UL-01 but not sequenced in UI |
| GL-05 | VPC segmentation | Stuck at s10 NACL | Bullet says deny SSH but command uses `protocol -1` (STUDENT-208) |
| GL-06 | NAT gateway | OK with cost gate | Good hourly warning |
| GL-08 | ALB | Stuck at s08 user-data | PowerShell wrapper on AL2023 AMI (STUDENT-208) |
| GL-10 | Queue and event path | Long but coherent | Many moving parts for week-2 student |
| GL-17 | Athena tiny file | Stuck s07–s08 | DDL for `gl17.sample` not spelled out (STUDENT-208) |
| GL-20 | Terraform workflow | OK on paper | Steps s03+ repeat generic preflight boilerplate |
| GL-21 | ElastiCache + HCP | OK | Hourly cost gate present |
| UL-01 | Challenge: identity | Blocked on criteria | Requires GL-03 bucket + boundary jargon (STUDENT-201) |
| UL-05 | Challenge: VPC | Depends GL-05 | Would inherit NACL confusion |
| UL-20 | Challenge: Terraform | Mirrors GL-20 | Fixture path `lab-fixtures/gl-20` referenced |

## Design exercise (student attempt)

**ID:** `de-multi-account` — *Control Tower and SCP strategy* (`content/exercises/de-multi-account.json`)

**My ADR sketch (not provisioned):**

1. **Requirement:** Multi-account guardrails without org admin in a personal account.
2. **Design:** Document AWS Control Tower landing zone + SCPs denying `root` usage and unapproved regions; use separate OUs for sandbox vs prod; IAM Identity Center for human access (cite AWS Control Tower overview).
3. **Security:** SCPs as guardrails, not authorization; least-privilege permission sets; no keys in git.
4. **Cost:** Control Tower baseline ~$0 for management features; member accounts still bill; state **not provisioned** — personal account cannot safely stand up org-wide tower same-day.
5. **Why no live lab:** Exercise `constraint_reason` matches — org-level services unavailable in disposable personal lab.

Self-score against rubric: ~8/10 (mapping + security + cost + citation; diagram notes verbal only).

## Evidence

EV-STUDENT-202, EV-STUDENT-210, EV-STUDENT-233, EV-STUDENT-234
