# Fix-loop r2 — AWS Architect (round-1)

Workspace: `C:\Users\dbadmin\Desktop\GitServ\ccna\web_app`  
Read-only review of current content files. No AWS API calls, no Terraform apply/plan/destroy, no servers, no Playwright.

## Scope

Re-check:

- **R1** — `content/labs/gl-17.json` (Athena DDL / query / cleanup)
- **R2** — `content/labs/gl-08.json` (user-data LF vs PowerShell CRLF)
- **R6** — `content/lessons/lesson-4-2.json`, `lesson-4-3.json`, `lesson-4-4.json` (per-bullet official AWS citations)

---

## R1

**Verdict: Fail**

### Evidence

CSV uploaded in `content/labs/gl-17.json` s06:

> `Run `'name,value\\nfoo,1' | Out-File -Encoding ascii gl17.csv`.`

> `Run `aws s3 cp gl17.csv s3://$Bucket/data/gl17.csv`.`

CREATE EXTERNAL TABLE in s07 matches those columns, location, and skip-header:

> `Run `aws athena start-query-execution --query-string \"CREATE EXTERNAL TABLE IF NOT EXISTS gl17.sample (name string, value int) ROW FORMAT DELIMITED FIELDS TERMINATED BY ',' LOCATION 's3://$Bucket/data/' TBLPROPERTIES ('skip.header.line.count'='1')\" --query-execution-context Database=gl17 --result-configuration OutputLocation=s3://$ResultsBucket/athena/`.`

No second conflicting DDL bullet in this file (single CREATE EXTERNAL TABLE in s07).

Later query in s08 uses the table (and therefore those columns via `SELECT *`):

> `Run `aws athena start-query-execution --query-string 'SELECT * FROM gl17.sample LIMIT 10' --query-execution-context Database=gl17 --result-configuration OutputLocation=s3://$ResultsBucket/athena/`.`

Cleanup drops the table only (s09):

> `Run `DROP TABLE gl17.sample`.`

There is **no** `DROP DATABASE` (or `DROP DATABASE gl17`) anywhere in `steps` or in `teardown.orderedDeletesPowerShell` (that list only empties/deletes the two S3 buckets).

### What is still wrong

- Cleanup must drop **both** the table and the database; database drop is missing.
- s09’s bare `DROP TABLE gl17.sample` is also not wrapped in `aws athena start-query-execution` (unlike create/query steps), so the documented cleanup command is incomplete for the CLI path this lab teaches.

---

## R2

**Verdict: Fail**

### Evidence

`content/labs/gl-08.json` s08 (“Launch target instance”):

> `Run `@'` then a new line `#!/bin/bash` then a new line `python3 -m http.server 80` then a new line `'@ | Set-Content -Encoding ascii user-data.sh`.`

> `Run `$InstanceId = aws ec2 run-instances ... --user-data file://user-data.sh ...`.`

Content intent is correct: bash + `python3 -m http.server 80`, file `user-data.sh`, passed as `file://user-data.sh`.

The write path **still uses `Set-Content`**. On Windows PowerShell, `Set-Content` / `Out-File` typically emit CRLF, so the shebang becomes `#!/bin/bash\r` and fails on Linux EC2 user-data. The required LF-safe pattern (for example `[IO.File]::WriteAllText` with `` `n `` and no BOM) is not present.

### What is still wrong

- Replace `Set-Content` with an explicit LF write (no BOM).
- Keep bash `python3 -m http.server` → `user-data.sh` → `file://user-data.sh`.

---

## R6

**Verdict: Fail**

### Evidence

Each of lessons 4.2 / 4.3 / 4.4 points every knowledge bullet at **one shared lesson citation**, not a per-bullet official doc for that bullet’s topic.

Lesson bottoms + citation records:

| Lesson | Shared URL in body | `content/citations/` |
| --- | --- | --- |
| `lesson-4-2.json` | `https://aws.amazon.com/ec2/pricing/` | `cite-4-2.json` → same URL |
| `lesson-4-3.json` | `https://aws.amazon.com/rds/pricing/` | `cite-4-3.json` → same URL |
| `lesson-4-4.json` | `https://aws.amazon.com/vpc/pricing/` | `cite-4-4.json` → same URL |

Repeated per-bullet sentence (example from every Knowledge section):

> `Use this lesson's citation link at the bottom before you lab.`

### Sample (≥6 bullets) — topic vs shared cite

1. **SAA-4.2-K02** (Cost Explorer, Budgets, CUR) → shared `aws.amazon.com/ec2/pricing/`  
   Wrong for this bullet. Official docs for these tools include e.g.  
   `https://docs.aws.amazon.com/cost-management/latest/userguide/ce-what-is.html`,  
   `https://docs.aws.amazon.com/cost-management/latest/userguide/budgets-managing-costs.html`.

2. **SAA-4.2-K04** (Spot, Reserved Instances, Savings Plans) → same EC2 pricing page for the whole lesson  
   Purchasing-options docs are separate, e.g.  
   `https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/instance-purchasing-options.html`,  
   `https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/using-spot-instances.html`.  
   Shared lesson sentence fails the per-bullet rule even where pricing is loosely related.

3. **SAA-4.2-K06** (AWS Outposts) → same `ec2/pricing/`  
   Not an Outposts doc.

4. **SAA-4.3-K03** (Caching strategies) → shared `aws.amazon.com/rds/pricing/`  
   Wrong. Caching guidance lives under ElastiCache docs, e.g.  
   `https://docs.aws.amazon.com/AmazonElastiCache/latest/dg/elasticache-use-cases.html`.

5. **SAA-4.3-K06** (Database connections and proxies) → same RDS pricing page  
   Wrong. Official proxy doc:  
   `https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/rds-proxy.html`.

6. **SAA-4.4-K03** (Load balancing / ALB) → shared `aws.amazon.com/vpc/pricing/`  
   Wrong for ALB. ELB billing/usage docs:  
   `https://docs.aws.amazon.com/elasticloadbalancing/latest/userguide/load-balancer-billing-usage-reports.html`.

7. **SAA-4.4-K04** (NAT gateways vs NAT instance costs) → same VPC pricing URL for every bullet  
   NAT-specific docs exist, e.g.  
   `https://docs.aws.amazon.com/vpc/latest/userguide/nat-gateway-pricing.html`,  
   `https://docs.aws.amazon.com/vpc/latest/userguide/vpc-nat-comparison.html`.  
   Still fails because the lesson uses one shared citation sentence, not a per-bullet cite.

### What is still wrong

- Knowledge bullets that tell the learner to “use this lesson's citation link” must instead cite the **correct official AWS doc for that bullet’s topic**.
- One pricing page per lesson (`cite-4-2` / `cite-4-3` / `cite-4-4`) is not enough.

---

## New issues (Low+)

| Severity | Item | Note |
| --- | --- | --- |
| Medium | GL-08 ALB subnets | s09 `create-load-balancer --subnets $SubnetPub` uses a **single** subnet; internet-facing ALBs require subnets in **at least two AZs**. Lab will fail at ALB create unless a second subnet is added. |
| Low | GL-17 s09 CLI form | `DROP TABLE` is not an `aws athena start-query-execution` call (inconsistent with s07/s08). |
| Low | GL-17 teardown catalog | `teardown.orderedDeletesPowerShell` never drops Athena/Glue table or database; only S3. |
| Low | Lessons 4.2–4.4 body | Every Knowledge bullet reuses identical Tradeoffs boilerplate; Skills have no per-bullet citations at all. |

---

## Summary

| ID | Item | Verdict |
| --- | --- | --- |
| R1 | GL-17 Athena DDL / query / cleanup | **Fail** |
| R2 | GL-08 user-data LF write | **Fail** |
| R6 | Lessons 4.2 / 4.3 / 4.4 per-bullet cites | **Fail** |
