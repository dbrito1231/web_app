# Teacher review — R1 / R2 (post-fix)

Read-only check of current `content/labs/gl-17.json` and `content/labs/gl-08.json` after Lead Dev edits. No content, code, or git changes. AWS and Terraform not called.

## Scope

Re-check only the failed items from the prior Teacher/AWS review:

- **R1** `gl-17`: CSV newline + `name,value` columns; s09 Athena drops before bucket deletes; `teardown.orderedDeletesPowerShell` drops before S3 deletes.
- **R2** `gl-08`: `user-data.sh` written LF/no BOM via `UTF8Encoding $false` and `` `n ``; still `python3 -m http.server 80` and `file://user-data.sh`; no `Set-Content` in that step.

## R1

**Verdict: Pass**

### CSV write — real newline, columns match table

s06 now writes with `UTF8Encoding $false` and PowerShell `` `n `` inside double quotes (real LF), not a literal `\n` in single quotes. Header/columns are `name,value`, matching the CREATE EXTERNAL TABLE columns.

Quoted (s06):

> Run `$utf8 = New-Object System.Text.UTF8Encoding $false; [IO.File]::WriteAllText("$pwd\gl17.csv", "name,value`nfoo,1`n", $utf8)`.

Quoted (s07 CREATE EXTERNAL TABLE):

> Run `aws athena start-query-execution --query-string "CREATE EXTERNAL TABLE IF NOT EXISTS gl17.sample (name string, value int) ROW FORMAT DELIMITED FIELDS TERMINATED BY ',' LOCATION 's3://$Bucket/data/' TBLPROPERTIES ('skip.header.line.count'='1')" --query-execution-context Database=gl17 --result-configuration OutputLocation=s3://$ResultsBucket/athena/`.

### s09 — drop table and database before buckets

s09 runs both Athena drops via `aws athena start-query-execution`. s10/s11 empty and delete buckets afterward.

Quoted (s09):

> Run `aws athena start-query-execution --query-string 'DROP TABLE gl17.sample' --query-execution-context Database=gl17 --result-configuration OutputLocation=s3://$ResultsBucket/athena/`.
>
> Run `aws athena start-query-execution --query-string 'DROP DATABASE gl17' --result-configuration OutputLocation=s3://$ResultsBucket/athena/`.
>
> Success: table and database are gone. Do this before you delete the results bucket.

### teardown.orderedDeletesPowerShell — same order

Athena drops appear before any `aws s3 rm` / `delete-bucket`.

Quoted (`teardown.orderedDeletesPowerShell`):

> `aws athena start-query-execution --query-string 'DROP TABLE IF EXISTS gl17.sample' --query-execution-context Database=gl17 --result-configuration OutputLocation=s3://$ResultsBucket/athena/`
>
> `aws athena start-query-execution --query-string 'DROP DATABASE IF EXISTS gl17' --result-configuration OutputLocation=s3://$ResultsBucket/athena/`
>
> `aws s3 rm s3://$Bucket --recursive`
>
> `aws s3 rm s3://$ResultsBucket --recursive`
>
> `aws s3api delete-bucket --bucket $Bucket`
>
> `aws s3api delete-bucket --bucket $ResultsBucket`

## R2

**Verdict: Pass**

### user-data.sh — LF, no BOM; bash server; file://

s08 writes with `UTF8Encoding $false` and `` `n ``, content remains bash + `python3 -m http.server 80`, and run-instances still uses `file://user-data.sh`. No `Set-Content` in this step.

Quoted (s08):

> Run `$utf8 = New-Object System.Text.UTF8Encoding $false; [IO.File]::WriteAllText("$pwd\user-data.sh", "#!/bin/bash`npython3 -m http.server 80`n", $utf8)`. This writes LF line endings and no BOM, so the shebang works on Linux.
>
> Run `$InstanceId = aws ec2 run-instances --image-id $AmiId --instance-type t3.micro --subnet-id $SubnetPub --security-group-ids $SgId --tag-specifications "ResourceType=instance,Tags=[{Key=LabId,Value=gl-08}]" --user-data file://user-data.sh --query "Instances[0].InstanceId" --output text`.

`Set-Content` is absent from s08 (and from the lab file for this write path).
