# Fix-loop gate — AWS Architect (round-final)

Workspace: `C:\Users\dbadmin\Desktop\GitServ\ccna\web_app`  
Evidence: current lab JSON + `scripts/scan_lab_placeholders.py` only. No AWS API calls.

---

## Gate checklist

### GL-08 user-data is bash `python3` not PowerShell — **Gone**

`content/labs/gl-08.json` run-instances step:

> `--user-data \"#!/bin/bash\npython3 -m http.server 80\"`

No PowerShell payload in `--user-data`.

### GL-05 NACL protocol `6` port `22` not protocol `-1` — **Gone**

`content/labs/gl-05.json`:

> `aws ec2 create-network-acl-entry --network-acl-id $CustomNaclId --ingress --rule-number 100 --protocol 6 --rule-action deny --cidr-block 0.0.0.0/0 --port-range From=22,To=22`

### GL-17 `CREATE EXTERNAL TABLE` before `SELECT` — **Gone**

`content/labs/gl-17.json` s07 then s08:

> `CREATE EXTERNAL TABLE IF NOT EXISTS gl17.sample (line string) ROW FORMAT DELIMITED FIELDS TERMINATED BY ',' LOCATION 's3://$ResultsBucket/sample/'`

> `SELECT * FROM gl17.sample LIMIT 10`

DDL precedes SELECT in step order.

### GL-07 volume AZ is `$Az` — **Gone**

`content/labs/gl-07.json`:

> `$Az = aws ec2 describe-instances --instance-ids $InstanceId --query Reservations[0].Instances[0].Placement.AvailabilityZone --output text`

> `$VolumeId = aws ec2 create-volume --availability-zone $Az --size 8 --volume-type gp3 ...`

### GL-18 `network-configuration file://network.json` — **Gone**

`content/labs/gl-18.json`:

> `... | Set-Content -Encoding ascii network.json`. Run `aws ecs run-task --cluster workbook-gl18 --launch-type FARGATE --task-definition $TaskDef --network-configuration file://network.json`.

### GL-19 subnet list comma-joined — **Gone**

`content/labs/gl-19.json`:

> `$SubnetList = (($Subnets -split ' +') | Where-Object { $_ }) -join ','`. Run `aws eks create-cluster --name workbook-gl19 --role-arn $EksRoleArn --resources-vpc-config subnetIds=$SubnetList ...`

### UL-05 tag `ul-05` not `gl-05` — **Gone**

`content/labs/ul-05.json` LabId references use `ul-05`:

> `All resources tagged LabId=ul-05 where supported.`

> `Key=LabId,Values=ul-05`

`gl-05` appears only as `pairId` / “paired guided lab” pointer, not as a LabId tag value.

### `scan_lab_placeholders.py` no bare `pass` for unset vars — **Gone**

`scripts/scan_lab_placeholders.py` has **no** `pass` statement. Unassigned teardown `$var` refs append errors:

> `errors.append(f"{lab_id}: teardown uses ${var} but the file never assigns it")`

---

## Summary

| Item | Verdict |
|------|---------|
| GL-08 user-data bash/python3 | Gone |
| GL-05 NACL protocol 6 / port 22 | Gone |
| GL-17 CREATE EXTERNAL TABLE before SELECT | Gone |
| GL-07 volume AZ `$Az` | Gone |
| GL-18 file://network.json | Gone |
| GL-19 comma-joined subnets | Gone |
| UL-05 LabId=ul-05 | Gone |
| scan unset-var bare pass | Gone |

---

## New issues (Low+)

- **Low — GL-17 s07 leftover DDL bullet:** After the concrete `CREATE EXTERNAL TABLE` command, s07 still included a second instruction for `s3://$Bucket/data/` with different columns. **Lead Dev follow-up:** that second bullet is removed. The remaining `CREATE EXTERNAL TABLE` uses `name string, value int` and `LOCATION 's3://$Bucket/data/'`, matching the CSV uploaded in s06.
