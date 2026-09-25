# Lab commands extract

| Lab | Step | Command |
|---|---|---|
| gl-01 | s02 | `aws sts get-caller-identity` |
| gl-01 | s03 | `aws --version` |
| gl-01 | s05 | `aws iam create-user --user-name workbook-gl01 --tags Key=Workbook,Value=aws-tf-lab Key=LabId,Value=gl-01 Key=CreatedAt,Value=$CreatedAt Key=ExpiresAt,Value=$ExpiresAt` |
| gl-01 | s05 | `aws iam create-access-key` |
| gl-01 | s06 | `aws iam create-policy --policy-name gl01-boundary --policy-document file://gl01-boundary.json --tags Key=Workbook,Value=aws-tf-lab Key=LabId,Value=gl-01 Key=CreatedAt,Value=$CreatedAt Key=ExpiresAt,Value=$ExpiresAt` |
| gl-01 | s07 | `aws iam put-user-permissions-boundary --user-name workbook-gl01 --permissions-boundary $BoundaryArn` |
| gl-01 | s07 | `aws iam get-user --user-name workbook-gl01` |
| gl-01 | s08 | `aws iam create-virtual-mfa-device --virtual-mfa-device-name workbook-gl01 --outfile "$env:TEMP\gl01-mfa.png" --bootstrap-method QRCodePNG` |
| gl-01 | s09 | `aws iam enable-mfa-device --user-name workbook-gl01 --serial-number <SerialNumber Arn> --authentication-code1 <current code> --authentication-code2 <next code>` |
| gl-01 | s09 | `aws iam list-mfa-devices --user-name workbook-gl01` |
| gl-01 | s10 | `aws budgets create-budget --account-id $AccountId --budget file://gl01-budget.json` |
| gl-01 | s10 | `aws budgets describe-budget --account-id $AccountId --budget-name workbook-gl01` |
| gl-01 | s11 | `aws budgets create-notification --account-id $AccountId --budget-name workbook-gl01 --notification NotificationType=ACTUAL,ComparisonOperator=GREATER_THAN,Threshold=<amount>,ThresholdType=ABSOLUTE_VALUE --subscribers SubscriptionType=EMAIL,Address=<your-email>` |
| gl-01 | s11 | `aws budgets describe-notifications-for-budget` |
| gl-01 | s12 | `aws iam list-access-keys --user-name workbook-gl01` |
| gl-01 | s12 | `aws iam delete-access-key` |
| gl-01 | s14 | `aws iam get-user --user-name workbook-gl01` |
| gl-01 | s14 | `aws budgets describe-budget --account-id $AccountId --budget-name workbook-gl01` |
| gl-02 | s02 | `aws sts get-caller-identity` |
| gl-02 | s03 | `aws --version` |
| gl-02 | s03 | `Terraform is not required unless a step says so.` |
| gl-02 | s06 | `aws s3api create-bucket --bucket $Bucket --region us-east-1 --tagging "TagSet=[{Key=Workbook,Value=aws-tf-lab},{Key=LabId,Value=gl-02},{Key=CreatedAt,Value=$CreatedAt},{Key=ExpiresAt,Value=$ExpiresAt}]"` |
| gl-02 | s06 | `aws s3api head-bucket --bucket $Bucket` |
| gl-02 | s07 | `aws s3api put-public-access-block --bucket $Bucket --public-access-block-configuration BlockPublicAcls=true,IgnorePublicAcls=true,BlockPublicPolicy=true,RestrictPublicBuckets=true` |
| gl-02 | s08 | `aws s3api put-bucket-versioning --bucket $Bucket --versioning-configuration Status=Enabled` |
| gl-02 | s08 | `aws s3api put-bucket-lifecycle-configuration --bucket $Bucket --lifecycle-configuration file://lifecycle.json` |
| gl-02 | s09 | `aws s3 cp gl02.txt s3://$Bucket/lab/gl02.txt` |
| gl-02 | s10 | `aws s3api put-bucket-policy --bucket $Bucket --policy file://gl02-policy.json` |
| gl-02 | s11 | `aws s3 cp gl02.txt s3://$Bucket/lab/gl02-copy.txt` |
| gl-02 | s14 | `aws resourcegroupstaggingapi get-resources --tag-filters Key=LabId,Values=gl-02` |
| gl-03 | s02 | `aws sts get-caller-identity` |
| gl-03 | s03 | `aws --version` |
| gl-03 | s03 | `Terraform is not required unless a step says so.` |
| gl-03 | s06 | `aws s3api create-bucket --bucket $Bucket --region us-east-1` |
| gl-03 | s06 | `aws s3api put-bucket-tagging --bucket $Bucket --tagging "TagSet=[{Key=Workbook,Value=aws-tf-lab},{Key=LabId,Value=gl-03},{Key=CreatedAt,Value=$CreatedAt},{Key=ExpiresAt,Value=$ExpiresAt}]"` |
| gl-03 | s06 | `aws s3 cp gl03.txt s3://$Bucket/readme.txt` |
| gl-03 | s07 | `aws iam create-role --role-name workbook-gl03-role --assume-role-policy-document file://gl03-trust.json --tags Key=Workbook,Value=aws-tf-lab Key=LabId,Value=gl-03 Key=CreatedAt,Value=$CreatedAt Key=ExpiresAt,Value=$ExpiresAt` |
| gl-03 | s07 | `aws iam get-role --role-name workbook-gl03-role --query Role.Arn --output text` |
| gl-03 | s08 | `aws iam put-role-policy --role-name workbook-gl03-role --policy-name gl03-read --policy-document file://gl03-s3read.json` |
| gl-03 | s09 | `aws sts assume-role --role-arn $RoleArn --role-session-name gl03-lab | ConvertFrom-Json` |
| gl-03 | s10 | `aws s3 cp s3://$Bucket/readme.txt -` |
| gl-03 | s11 | `aws s3 cp gl03.txt s3://$Bucket/denied.txt` |
| gl-03 | s14 | `aws resourcegroupstaggingapi get-resources --tag-filters Key=LabId,Values=gl-03` |
| gl-04 | s02 | `aws sts get-caller-identity` |
| gl-04 | s03 | `aws --version` |
| gl-04 | s03 | `Terraform is not required unless a step says so.` |
| gl-04 | s06 | `aws kms create-key --description 'workbook gl-04' --tags Key=Workbook,Value=aws-tf-lab Key=LabId,Value=gl-04 Key=CreatedAt,Value=$CreatedAt Key=ExpiresAt,Value=$ExpiresAt` |
| gl-04 | s06 | `aws kms create-alias --alias-name alias/workbook-gl04 --target-key-id $KeyId` |
| gl-04 | s07 | `aws s3api create-bucket --bucket $Bucket --region us-east-1` |
| gl-04 | s07 | `aws s3api put-bucket-tagging --bucket $Bucket --tagging "TagSet=[{Key=LabId,Value=gl-04},{Key=Workbook,Value=aws-tf-lab}]"` |
| gl-04 | s08 | `aws s3 cp gl04.txt s3://$Bucket/secret.txt --sse aws:kms --sse-kms-key-id $KeyId` |
| gl-04 | s09 | `aws s3 cp s3://$Bucket/secret.txt -` |
| gl-04 | s10 | `aws kms schedule-key-deletion --key-id $KeyId --pending-window-in-days 7` |
| gl-04 | s11 | `aws kms list-aliases --query "Aliases[?AliasName=='alias/workbook-gl04']"` |
| gl-04 | s14 | `aws resourcegroupstaggingapi get-resources --tag-filters Key=LabId,Values=gl-04` |
| gl-05 | s02 | `aws sts get-caller-identity` |
| gl-05 | s03 | `aws --version` |
| gl-05 | s03 | `Terraform is not required unless a step says so.` |
| gl-05 | s06 | `aws ec2 create-vpc --cidr-block 10.50.0.0/16 --query Vpc.VpcId --output text --tag-specifications "ResourceType=vpc,Tags=[{Key=Name,Value=workbook-gl05},{Key=LabId,Value=gl-05},{Key=Workbook,Value=aws-tf-lab}]"` |
| gl-05 | s06 | `aws ec2 modify-vpc-attribute --vpc-id $VpcId --enable-dns-hostnames '{"Value":true}'` |
| gl-05 | s07 | `aws ec2 create-subnet --vpc-id $VpcId --cidr-block 10.50.1.0/24 --availability-zone us-east-1a --query Subnet.SubnetId --output text --tag-specifications "ResourceType=subnet,Tags=[{Key=LabId,Value=gl-05}]"` |
| gl-05 | s07 | `aws ec2 create-subnet --vpc-id $VpcId --cidr-block 10.50.2.0/24 --availability-zone us-east-1b --query Subnet.SubnetId --output text --tag-specifications "ResourceType=subnet,Tags=[{Key=LabId,Value=gl-05}]"` |
| gl-05 | s08 | `aws ec2 create-internet-gateway --query InternetGateway.InternetGatewayId --output text --tag-specifications "ResourceType=internet-gateway,Tags=[{Key=LabId,Value=gl-05}]"` |
| gl-05 | s08 | `aws ec2 attach-internet-gateway --internet-gateway-id $IgwId --vpc-id $VpcId` |
| gl-05 | s08 | `aws ec2 create-route-table --vpc-id $VpcId --query RouteTable.RouteTableId --output text --tag-specifications "ResourceType=route-table,Tags=[{Key=LabId,Value=gl-05}]"` |
| gl-05 | s08 | `aws ec2 create-route --route-table-id $PublicRouteTableId --destination-cidr-block 0.0.0.0/0 --gateway-id $IgwId` |
| gl-05 | s08 | `aws ec2 associate-route-table --route-table-id $PublicRouteTableId --subnet-id $SubnetPub --query AssociationId --output text` |
| gl-05 | s09 | `aws ec2 create-route-table --vpc-id $VpcId --query RouteTable.RouteTableId --output text --tag-specifications "ResourceType=route-table,Tags=[{Key=LabId,Value=gl-05}]"` |
| gl-05 | s09 | `aws ec2 associate-route-table --route-table-id $PrivateRouteTableId --subnet-id $SubnetPriv --query AssociationId --output text` |
| gl-05 | s09 | `aws ec2 create-vpc-endpoint --vpc-id $VpcId --service-name com.amazonaws.us-east-1.s3 --route-table-ids $PrivateRouteTableId --query VpcEndpoint.VpcEndpointId --output text --tag-specifications "ResourceType=vpc-endpoint,Tags=[{Key=LabId,Value=gl-05}]"` |
| gl-05 | s10 | `aws ec2 create-security-group --group-name workbook-gl05 --description "gl05" --vpc-id $VpcId --query GroupId --output text --tag-specifications "ResourceType=security-group,Tags=[{Key=LabId,Value=gl-05}]"` |
| gl-05 | s10 | `aws ec2 authorize-security-group-ingress --group-id $SgId --protocol tcp --port 22 --cidr 203.0.113.0/32` |
| gl-05 | s10 | `aws ec2 create-network-acl --vpc-id $VpcId --query NetworkAcl.NetworkAclId --output text --tag-specifications "ResourceType=network-acl,Tags=[{Key=LabId,Value=gl-05}]"` |
| gl-05 | s10 | `aws ec2 create-network-acl-entry --network-acl-id $CustomNaclId --ingress --rule-number 100 --protocol -1 --rule-action deny --cidr-block 0.0.0.0/0 --port-range From=22,To=22` |
| gl-05 | s10 | `aws ec2 describe-network-acls --filters Name=association.subnet-id,Values=$SubnetPriv --query 'NetworkAcls[0].Associations[0].NetworkAclAssociationId' --output text` |
| gl-05 | s10 | `aws ec2 describe-network-acls --filters Name=vpc-id,Values=$VpcId Name=default,Values=true --query 'NetworkAcls[0].NetworkAclId' --output text` |
| gl-05 | s10 | `aws ec2 replace-network-acl-association --association-id $NaclAssocId --network-acl-id $CustomNaclId` |
| gl-05 | s11 | `aws ec2 describe-nat-gateways --filter Name=vpc-id,Values=$VpcId --query NatGateways` |
| gl-05 | s14 | `aws resourcegroupstaggingapi get-resources --tag-filters Key=LabId,Values=gl-05` |
| gl-06 | s02 | `aws sts get-caller-identity` |
| gl-06 | s03 | `aws --version` |
| gl-06 | s03 | `Terraform is not required unless a step says so.` |
| gl-06 | s06 | `aws ec2 create-vpc --cidr-block 10.60.0.0/16 --query Vpc.VpcId --output text --tag-specifications "ResourceType=vpc,Tags=[{Key=LabId,Value=gl-06}]"` |
| gl-06 | s06 | `aws ec2 create-subnet --vpc-id $VpcId --cidr-block 10.60.1.0/24 --availability-zone us-east-1a --query Subnet.SubnetId --output text` |
| gl-06 | s06 | `aws ec2 create-subnet --vpc-id $VpcId --cidr-block 10.60.2.0/24 --availability-zone us-east-1b --query Subnet.SubnetId --output text` |
| gl-06 | s07 | `aws ec2 create-internet-gateway --query InternetGateway.InternetGatewayId --output text --tag-specifications "ResourceType=internet-gateway,Tags=[{Key=LabId,Value=gl-06}]"` |
| gl-06 | s07 | `aws ec2 attach-internet-gateway --internet-gateway-id $IgwId --vpc-id $VpcId` |
| gl-06 | s07 | `aws ec2 create-route-table --vpc-id $VpcId --query RouteTable.RouteTableId --output text` |
| gl-06 | s07 | `aws ec2 create-route --route-table-id $PublicRouteTableId --destination-cidr-block 0.0.0.0/0 --gateway-id $IgwId` |
| gl-06 | s07 | `aws ec2 associate-route-table --route-table-id $PublicRouteTableId --subnet-id $SubnetPub --query AssociationId --output text` |
| gl-06 | s07 | `aws ec2 create-route-table --vpc-id $VpcId --query RouteTable.RouteTableId --output text` |
| gl-06 | s07 | `aws ec2 associate-route-table --route-table-id $PrivateRouteTableId --subnet-id $SubnetPriv --query AssociationId --output text` |
| gl-06 | s08 | `aws ec2 allocate-address --domain vpc --query AllocationId --output text --tag-specifications "ResourceType=elastic-ip,Tags=[{Key=LabId,Value=gl-06}]"` |
| gl-06 | s09 | `aws ec2 create-nat-gateway --subnet-id $SubnetPub --allocation-id $AllocationId --query NatGateway.NatGatewayId --output text --tag-specifications "ResourceType=natgateway,Tags=[{Key=LabId,Value=gl-06}]"` |
| gl-06 | s09 | `aws ec2 wait nat-gateway-available --nat-gateway-ids $NatGatewayId` |
| gl-06 | s10 | `aws ec2 create-route --route-table-id $PrivateRouteTableId --destination-cidr-block 0.0.0.0/0 --nat-gateway-id $NatGatewayId` |
| gl-06 | s11 | `aws ec2 delete-nat-gateway --nat-gateway-id $NatGatewayId` |
| gl-06 | s11 | `aws ec2 wait nat-gateway-deleted --nat-gateway-ids $NatGatewayId` |
| gl-06 | s11 | `aws ec2 release-address --allocation-id $AllocationId` |
| gl-06 | s14 | `aws resourcegroupstaggingapi get-resources --tag-filters Key=LabId,Values=gl-06` |
| gl-07 | s02 | `aws sts get-caller-identity` |
| gl-07 | s03 | `aws --version` |
| gl-07 | s03 | `Terraform is not required unless a step says so.` |
| gl-07 | s06 | `aws ec2 describe-vpcs --filters Name=isDefault,Values=true --query "Vpcs[0].VpcId" --output text` |
| gl-07 | s06 | `aws ec2 describe-subnets --filters Name=vpc-id,Values=$VpcId Name=default-for-az,Values=true --query "Subnets[0].SubnetId" --output text` |
| gl-07 | s07 | `aws ssm get-parameters --names /aws/service/ami-amazon-linux-latest/al2023-ami-kernel-default-x86_64 --query "Parameters[0].Value" --output text` |
| gl-07 | s07 | `aws ec2 run-instances --image-id $AmiId --instance-type t3.micro --subnet-id $SubnetId --tag-specifications "ResourceType=instance,Tags=[{Key=LabId,Value=gl-07},{Key=Workbook,Value=aws-tf-lab}]" --query "Instances[0].InstanceId" --output text` |
| gl-07 | s07 | `aws ec2 wait instance-running --instance-ids $InstanceId` |
| gl-07 | s08 | `aws ec2 create-volume --availability-zone us-east-1a --size 8 --volume-type gp3 --query VolumeId --output text --tag-specifications "ResourceType=volume,Tags=[{Key=LabId,Value=gl-07}]"` |
| gl-07 | s08 | `aws ec2 wait volume-available --volume-ids $VolumeId` |
| gl-07 | s08 | `aws ec2 describe-instances --instance-ids $InstanceId --query Reservations[0].Instances[0].Placement.AvailabilityZone --output text` |
| gl-07 | s08 | `aws ec2 attach-volume --volume-id $VolumeId --instance-id $InstanceId --device /dev/sdf` |
| gl-07 | s09 | `aws ec2 create-snapshot --volume-id $VolumeId --description "gl07 lab" --query SnapshotId --output text --tag-specifications "ResourceType=snapshot,Tags=[{Key=LabId,Value=gl-07}]"` |
| gl-07 | s09 | `aws ec2 wait snapshot-completed --snapshot-ids $SnapshotId` |
| gl-07 | s10 | `aws ec2 terminate-instances --instance-ids $InstanceId` |
| gl-07 | s10 | `aws ec2 wait instance-terminated --instance-ids $InstanceId` |
| gl-07 | s11 | `aws ec2 detach-volume --volume-id $VolumeId` |
| gl-07 | s11 | `aws ec2 wait volume-available --volume-ids $VolumeId` |
| gl-07 | s11 | `aws ec2 delete-volume --volume-id $VolumeId` |
| gl-07 | s14 | `aws resourcegroupstaggingapi get-resources --tag-filters Key=LabId,Values=gl-07` |
| gl-08 | s02 | `aws sts get-caller-identity` |
| gl-08 | s03 | `aws --version` |
| gl-08 | s03 | `Terraform is not required unless a step says so.` |
| gl-08 | s06 | `aws ec2 create-vpc --cidr-block 10.80.0.0/16 --query Vpc.VpcId --output text --tag-specifications "ResourceType=vpc,Tags=[{Key=LabId,Value=gl-08}]"` |
| gl-08 | s06 | `aws ec2 create-subnet --vpc-id $VpcId --cidr-block 10.80.1.0/24 --availability-zone us-east-1a --query Subnet.SubnetId --output text` |
| gl-08 | s06 | `aws ec2 create-internet-gateway --query InternetGateway.InternetGatewayId --output text --tag-specifications "ResourceType=internet-gateway,Tags=[{Key=LabId,Value=gl-08}]"` |
| gl-08 | s06 | `aws ec2 attach-internet-gateway --internet-gateway-id $IgwId --vpc-id $VpcId` |
| gl-08 | s06 | `aws ec2 create-route-table --vpc-id $VpcId --query RouteTable.RouteTableId --output text` |
| gl-08 | s06 | `aws ec2 create-route --route-table-id $PublicRouteTableId --destination-cidr-block 0.0.0.0/0 --gateway-id $IgwId` |
| gl-08 | s06 | `aws ec2 associate-route-table --route-table-id $PublicRouteTableId --subnet-id $SubnetPub --query AssociationId --output text` |
| gl-08 | s07 | `aws ec2 create-security-group --group-name workbook-gl08 --description gl08 --vpc-id $VpcId --query GroupId --output text --tag-specifications "ResourceType=security-group,Tags=[{Key=LabId,Value=gl-08}]"` |
| gl-08 | s07 | `aws ec2 authorize-security-group-ingress --group-id $SgId --protocol tcp --port 80 --cidr 0.0.0.0/0` |
| gl-08 | s08 | `aws ssm get-parameters --names /aws/service/ami-amazon-linux-latest/al2023-ami-kernel-default-x86_64 --query "Parameters[0].Value" --output text` |
| gl-08 | s08 | `aws ec2 run-instances --image-id $AmiId --instance-type t3.micro --subnet-id $SubnetPub --security-group-ids $SgId --tag-specifications "ResourceType=instance,Tags=[{Key=LabId,Value=gl-08}]" --user-data "<powershell>python -m http.server 80</powershell>" --query "Instances[0].InstanceId" --output text` |
| gl-08 | s08 | `aws ec2 wait instance-running --instance-ids $InstanceId` |
| gl-08 | s09 | `aws elbv2 create-load-balancer --name workbook-gl08 --subnets $SubnetPub --security-groups $SgId --query "LoadBalancers[0].LoadBalancerArn" --output text --tags Key=LabId,Value=gl-08 Key=Workbook,Value=aws-tf-lab` |
| gl-08 | s09 | `aws elbv2 create-target-group --name workbook-gl08-tg --protocol HTTP --port 80 --vpc-id $VpcId --target-type instance --query "TargetGroups[0].TargetGroupArn" --output text` |
| gl-08 | s09 | `aws elbv2 register-targets --target-group-arn $TargetGroupArn --targets Id=$InstanceId` |
| gl-08 | s09 | `aws elbv2 create-listener --load-balancer-arn $AlbArn --protocol HTTP --port 80 --default-actions Type=forward,TargetGroupArn=$TargetGroupArn` |
| gl-08 | s10 | `aws elbv2 describe-load-balancers --load-balancer-arns $AlbArn --query 'LoadBalancers[0].DNSName' --output text` |
| gl-08 | s14 | `aws resourcegroupstaggingapi get-resources --tag-filters Key=LabId,Values=gl-08` |
| gl-09 | s02 | `aws sts get-caller-identity` |
| gl-09 | s03 | `aws --version` |
| gl-09 | s03 | `Terraform is not required unless a step says so.` |
| gl-09 | s06 | `aws ec2 describe-vpcs --filters Name=isDefault,Values=true --query "Vpcs[0].VpcId" --output text` |
| gl-09 | s06 | `aws ec2 describe-subnets --filters Name=vpc-id,Values=$VpcId --query "Subnets[0].SubnetId" --output text` |
| gl-09 | s07 | `aws ssm get-parameters --names /aws/service/ami-amazon-linux-latest/al2023-ami-kernel-default-x86_64 --query "Parameters[0].Value" --output text` |
| gl-09 | s07 | `aws ec2 create-launch-template --launch-template-name workbook-gl09 --launch-template-data file://gl09-lt.json --query LaunchTemplate.LaunchTemplateId --output text` |
| gl-09 | s08 | `aws autoscaling create-auto-scaling-group --auto-scaling-group-name $AsgName --launch-template LaunchTemplateId=$LaunchTemplateId,Version=1 --min-size 1 --max-size 1 --desired-capacity 1 --vpc-zone-identifier $SubnetId --tags Key=LabId,Value=gl-09,PropagateAtLaunch=true Key=Workbook,Value=aws-tf-lab,PropagateAtLaunch=true` |
| gl-09 | s09 | `aws autoscaling update-auto-scaling-group --auto-scaling-group-name $AsgName --min-size 0 --max-size 0 --desired-capacity 0` |
| gl-09 | s10 | `aws autoscaling delete-auto-scaling-group --auto-scaling-group-name $AsgName --force-delete` |
| gl-09 | s11 | `aws ec2 delete-launch-template --launch-template-id $LaunchTemplateId` |
| gl-09 | s14 | `aws resourcegroupstaggingapi get-resources --tag-filters Key=LabId,Values=gl-09` |
| gl-10 | s02 | `aws sts get-caller-identity` |
| gl-10 | s03 | `aws --version` |
| gl-10 | s03 | `Terraform is not required unless a step says so.` |
| gl-10 | s06 | `aws iam create-role --role-name workbook-gl10-lambda --assume-role-policy-document file://gl10-trust.json --tags Key=Workbook,Value=aws-tf-lab Key=LabId,Value=gl-10 Key=CreatedAt,Value=$CreatedAt Key=ExpiresAt,Value=$ExpiresAt` |
| gl-10 | s06 | `aws iam attach-role-policy --role-name workbook-gl10-lambda --policy-arn arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole` |
| gl-10 | s06 | `aws iam get-role --role-name workbook-gl10-lambda --query Role.Arn --output text` |
| gl-10 | s07 | `aws sns create-topic --name workbook-gl10 --tags Key=Workbook,Value=aws-tf-lab Key=LabId,Value=gl-10 Key=CreatedAt,Value=$CreatedAt Key=ExpiresAt,Value=$ExpiresAt --query TopicArn --output text` |
| gl-10 | s07 | `aws sqs create-queue --queue-name workbook-gl10 --attributes MessageRetentionPeriod=86400 --tags LabId=gl-10,Workbook=aws-tf-lab --query QueueUrl --output text` |
| gl-10 | s07 | `aws sqs get-queue-attributes --queue-url $QueueUrl --attribute-names QueueArn --query Attributes.QueueArn --output text` |
| gl-10 | s08 | `aws sns subscribe --topic-arn $TopicArn --protocol sqs --notification-endpoint $QueueArn` |
| gl-10 | s08 | `aws sqs set-queue-attributes --queue-url $QueueUrl --attributes Policy=file://gl10-queue-policy.json` |
| gl-10 | s09 | `aws lambda create-function --function-name workbook-gl10 --runtime python3.12 --role $LambdaRoleArn --handler lambda_function.lambda_handler --zip-file fileb://function.zip --tags Key=Workbook,Value=aws-tf-lab Key=LabId,Value=gl-10 Key=CreatedAt,Value=$CreatedAt Key=ExpiresAt,Value=$ExpiresAt --query FunctionArn --output text` |
| gl-10 | s10 | `aws sns subscribe --topic-arn $TopicArn --protocol lambda --notification-endpoint $FunctionArn` |
| gl-10 | s10 | `aws lambda add-permission --function-name workbook-gl10 --statement-id sns-gl10 --action lambda:InvokeFunction --principal sns.amazonaws.com --source-arn $TopicArn` |
| gl-10 | s11 | `aws sns publish --topic-arn $TopicArn --message '{"test":"gl10"}'` |
| gl-10 | s11 | `aws logs tail /aws/lambda/workbook-gl10 --since 5m` |
| gl-10 | s14 | `aws resourcegroupstaggingapi get-resources --tag-filters Key=LabId,Values=gl-10` |
| gl-11 | s02 | `aws sts get-caller-identity` |
| gl-11 | s03 | `aws --version` |
| gl-11 | s03 | `Terraform is not required unless a step says so.` |
| gl-11 | s06 | `aws iam create-role --role-name workbook-gl11-lambda --assume-role-policy-document file://gl11-trust.json --tags Key=Workbook,Value=aws-tf-lab Key=LabId,Value=gl-11 Key=CreatedAt,Value=$CreatedAt Key=ExpiresAt,Value=$ExpiresAt` |
| gl-11 | s06 | `aws iam attach-role-policy --role-name workbook-gl11-lambda --policy-arn arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole` |
| gl-11 | s06 | `aws iam get-role --role-name workbook-gl11-lambda --query Role.Arn --output text` |
| gl-11 | s06 | `aws lambda create-function --function-name workbook-gl11 --runtime python3.12 --role $LambdaRoleArn --handler lambda_function.lambda_handler --zip-file fileb://function.zip --tags Key=Workbook,Value=aws-tf-lab Key=LabId,Value=gl-11 Key=CreatedAt,Value=$CreatedAt Key=ExpiresAt,Value=$ExpiresAt --query FunctionArn --output text` |
| gl-11 | s07 | `aws apigatewayv2 create-api --name workbook-gl11 --protocol-type HTTP --tags LabId=gl-11,Workbook=aws-tf-lab --query ApiId --output text` |
| gl-11 | s07 | `aws apigatewayv2 create-integration --api-id $ApiId --integration-type AWS_PROXY --integration-uri $FunctionArn --payload-format-version 2.0 --query IntegrationId --output text` |
| gl-11 | s07 | `aws apigatewayv2 create-route --api-id $ApiId --route-key 'GET /hello' --target integrations/$IntegrationId` |
| gl-11 | s08 | `aws apigatewayv2 create-stage --api-id $ApiId --stage-name prod --auto-deploy` |
| gl-11 | s08 | `aws lambda add-permission --function-name workbook-gl11 --statement-id apigw --action lambda:InvokeFunction --principal apigateway.amazonaws.com --source-arn arn:aws:execute-api:us-east-1:$AccountId:$ApiId/*/*` |
| gl-11 | s09 | `aws apigatewayv2 get-apis --query "Items[?ApiId=='$ApiId'].ApiEndpoint" --output text` |
| gl-11 | s10 | `aws apigatewayv2 get-routes --api-id $ApiId` |
| gl-11 | s14 | `aws resourcegroupstaggingapi get-resources --tag-filters Key=LabId,Values=gl-11` |
| gl-12 | s02 | `aws sts get-caller-identity` |
| gl-12 | s03 | `aws --version` |
| gl-12 | s03 | `Terraform is not required unless a step says so.` |
| gl-12 | s06 | `aws iam create-role --role-name workbook-gl12-sfn --assume-role-policy-document file://gl12-trust.json --tags Key=Workbook,Value=aws-tf-lab Key=LabId,Value=gl-12 Key=CreatedAt,Value=$CreatedAt Key=ExpiresAt,Value=$ExpiresAt` |
| gl-12 | s06 | `aws iam put-role-policy --role-name workbook-gl12-sfn --policy-name gl12-log --policy-document file://gl12-log-policy.json` |
| gl-12 | s06 | `aws iam get-role --role-name workbook-gl12-sfn --query Role.Arn --output text` |
| gl-12 | s07 | `aws stepfunctions create-state-machine --name workbook-gl12 --definition file://gl12.asl.json --role-arn $SfnRoleArn --tags Key=Workbook,Value=aws-tf-lab Key=LabId,Value=gl-12 Key=CreatedAt,Value=$CreatedAt Key=ExpiresAt,Value=$ExpiresAt --query stateMachineArn --output text` |
| gl-12 | s08 | `aws stepfunctions start-execution --state-machine-arn $SmArn --input '{}' --query executionArn --output text` |
| gl-12 | s08 | `aws stepfunctions describe-execution --execution-arn $ExecArn` |
| gl-12 | s09 | `aws stepfunctions list-executions --state-machine-arn $SmArn --max-results 1` |
| gl-12 | s14 | `aws resourcegroupstaggingapi get-resources --tag-filters Key=LabId,Values=gl-12` |
| gl-13 | s02 | `aws sts get-caller-identity` |
| gl-13 | s03 | `aws --version` |
| gl-13 | s03 | `Terraform is not required unless a step says so.` |
| gl-13 | s06 | `aws dynamodb create-table --table-name workbook-gl13 --attribute-definitions AttributeName=pk,AttributeType=S --key-schema AttributeName=pk,KeyType=HASH --billing-mode PAY_PER_REQUEST --tags Key=Workbook,Value=aws-tf-lab Key=LabId,Value=gl-13 Key=CreatedAt,Value=$CreatedAt Key=ExpiresAt,Value=$ExpiresAt` |
| gl-13 | s06 | `aws dynamodb wait table-exists --table-name workbook-gl13` |
| gl-13 | s07 | `aws dynamodb put-item --table-name workbook-gl13 --item '{"pk":{"S":"item1"},"data":{"S":"alpha"}}'` |
| gl-13 | s07 | `aws dynamodb put-item --table-name workbook-gl13 --item '{"pk":{"S":"item2"},"data":{"S":"beta"}}'` |
| gl-13 | s08 | `aws dynamodb get-item --table-name workbook-gl13 --key '{"pk":{"S":"item1"}}'` |
| gl-13 | s08 | `aws dynamodb scan --table-name workbook-gl13 --select COUNT` |
| gl-13 | s09 | `aws dynamodb update-item --table-name workbook-gl13 --key '{"pk":{"S":"item1"}}' --update-expression 'SET data = :v' --expression-attribute-values '{":v":{"S":"gamma"}}'` |
| gl-13 | s10 | `aws dynamodb delete-item --table-name workbook-gl13 --key '{"pk":{"S":"item2"}}'` |
| gl-13 | s11 | `aws dynamodb delete-table --table-name workbook-gl13` |
| gl-13 | s11 | `aws dynamodb wait table-not-exists --table-name workbook-gl13` |
| gl-13 | s14 | `aws resourcegroupstaggingapi get-resources --tag-filters Key=LabId,Values=gl-13` |
| gl-14 | s02 | `aws sts get-caller-identity` |
| gl-14 | s03 | `aws --version` |
| gl-14 | s03 | `Terraform is not required unless a step says so.` |
| gl-14 | s06 | `aws ec2 describe-vpcs --filters Name=isDefault,Values=true --query "Vpcs[0].VpcId" --output text` |
| gl-14 | s06 | `aws ec2 describe-subnets --filters Name=vpc-id,Values=$VpcId --query "Subnets[0:2].SubnetId" --output text` |
| gl-14 | s06 | `aws rds create-db-subnet-group --db-subnet-group-name $SubnetGroup --db-subnet-group-description gl14 --subnet-ids $Subnets --tags Key=LabId,Value=gl-14 Key=Workbook,Value=aws-tf-lab` |
| gl-14 | s07 | `aws rds create-db-instance --db-instance-identifier $DbId --db-instance-class db.t3.micro --engine postgres --master-username labadmin --master-user-password 'TempGl14Pass!' --allocated-storage 20 --backup-retention-period 1 --no-multi-az --no-publicly-accessible --db-subnet-group-name $SubnetGroup --tags Key=LabId,Value=gl-14 Key=Workbook,Value=aws-tf-lab` |
| gl-14 | s07 | `aws rds wait db-instance-available --db-instance-identifier $DbId` |
| gl-14 | s08 | `aws rds describe-db-instances --db-instance-identifier $DbId` |
| gl-14 | s09 | `aws rds delete-db-instance --db-instance-identifier $DbId --skip-final-snapshot` |
| gl-14 | s09 | `aws rds wait db-instance-deleted --db-instance-identifier $DbId` |
| gl-14 | s10 | `aws rds delete-db-subnet-group --db-subnet-group-name $SubnetGroup` |
| gl-14 | s14 | `aws resourcegroupstaggingapi get-resources --tag-filters Key=LabId,Values=gl-14` |
| gl-15 | s02 | `aws sts get-caller-identity` |
| gl-15 | s03 | `aws --version` |
| gl-15 | s03 | `Terraform is not required unless a step says so.` |
| gl-15 | s06 | `aws s3api create-bucket --bucket $Bucket --region us-east-1` |
| gl-15 | s06 | `aws s3api put-bucket-tagging --bucket $Bucket --tagging "TagSet=[{Key=LabId,Value=gl-15},{Key=Workbook,Value=aws-tf-lab}]"` |
| gl-15 | s07 | `aws cloudtrail create-trail --name workbook-gl15 --s3-bucket-name $Bucket --is-multi-region-trail` |
| gl-15 | s07 | `aws cloudtrail start-logging --name workbook-gl15` |
| gl-15 | s08 | `aws sts get-caller-identity` |
| gl-15 | s09 | `aws cloudwatch put-metric-alarm --alarm-name workbook-gl15 --metric-name CPUUtilization --namespace AWS/EC2 --statistic Average --period 300 --threshold 80 --comparison-operator GreaterThanThreshold --evaluation-periods 1 --datapoints-to-alarm 1 --dimensions Name=InstanceId,Value=i-0123456789abcdef0 --alarm-actions []` |
| gl-15 | s10 | `aws cloudtrail stop-logging --name workbook-gl15` |
| gl-15 | s11 | `aws cloudtrail delete-trail --name workbook-gl15` |
| gl-15 | s14 | `aws resourcegroupstaggingapi get-resources --tag-filters Key=LabId,Values=gl-15` |
| gl-16 | s02 | `aws sts get-caller-identity` |
| gl-16 | s03 | `aws --version` |
| gl-16 | s03 | `Terraform is not required unless a step says so.` |
| gl-16 | s06 | `aws ec2 create-vpc --cidr-block 10.160.0.0/16 --query Vpc.VpcId --output text --tag-specifications "ResourceType=vpc,Tags=[{Key=LabId,Value=gl-16}]"` |
| gl-16 | s07 | `aws route53 create-hosted-zone --name workbook.gl16.local --vpc VPCRegion=us-east-1,VPCId=$VpcId --caller-reference gl16-$(Get-Random) --hosted-zone-config Comment=gl16,PrivateZone=true --query HostedZone.Id --output text` |
| gl-16 | s08 | `aws route53 change-resource-record-sets --hosted-zone-id $ZoneId --change-batch file://gl16-record.json` |
| gl-16 | s09 | `aws route53 list-resource-record-sets --hosted-zone-id $ZoneId` |
| gl-16 | s11 | `aws route53 delete-hosted-zone --id $ZoneId` |
| gl-16 | s11 | `aws ec2 delete-vpc --vpc-id $VpcId` |
| gl-16 | s14 | `aws resourcegroupstaggingapi get-resources --tag-filters Key=LabId,Values=gl-16` |
| gl-17 | s02 | `aws sts get-caller-identity` |
| gl-17 | s03 | `aws --version` |
| gl-17 | s03 | `Terraform is not required unless a step says so.` |
| gl-17 | s06 | `aws s3api create-bucket --bucket $Bucket --region us-east-1` |
| gl-17 | s06 | `aws s3api create-bucket --bucket $ResultsBucket --region us-east-1` |
| gl-17 | s06 | `aws s3 cp gl17.csv s3://$Bucket/data/gl17.csv` |
| gl-17 | s07 | `aws athena start-query-execution --query-string 'CREATE DATABASE IF NOT EXISTS gl17' --result-configuration OutputLocation=s3://$ResultsBucket/athena/` |
| gl-17 | s08 | `aws athena start-query-execution --query-string 'SELECT * FROM gl17.sample LIMIT 10' --query-execution-context Database=gl17 --result-configuration OutputLocation=s3://$ResultsBucket/athena/` |
| gl-17 | s10 | `aws s3 rm s3://$Bucket --recursive` |
| gl-17 | s10 | `aws s3 rm s3://$ResultsBucket --recursive` |
| gl-17 | s11 | `aws s3api delete-bucket --bucket $Bucket` |
| gl-17 | s11 | `aws s3api delete-bucket --bucket $ResultsBucket` |
| gl-17 | s14 | `aws resourcegroupstaggingapi get-resources --tag-filters Key=LabId,Values=gl-17` |
| gl-18 | s02 | `aws sts get-caller-identity` |
| gl-18 | s03 | `aws --version` |
| gl-18 | s03 | `Terraform is not required unless a step says so.` |
| gl-18 | s06 | `aws ecs create-cluster --cluster-name workbook-gl18 --tags Key=Workbook,Value=aws-tf-lab Key=LabId,Value=gl-18 Key=CreatedAt,Value=$CreatedAt Key=ExpiresAt,Value=$ExpiresAt` |
| gl-18 | s06 | `aws iam create-role --role-name workbook-gl18-task --assume-role-policy-document file://gl18-trust.json` |
| gl-18 | s06 | `aws iam attach-role-policy --role-name workbook-gl18-task --policy-arn arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy` |
| gl-18 | s06 | `aws iam get-role --role-name workbook-gl18-task --query Role.Arn --output text` |
| gl-18 | s07 | `aws ecs register-task-definition --cli-input-json file://gl18-task.json` |
| gl-18 | s07 | `aws ecs describe-task-definition --task-definition workbook-gl18 --query taskDefinition.taskDefinitionArn --output text` |
| gl-18 | s08 | `aws ecs run-task --cluster workbook-gl18 --launch-type FARGATE --task-definition $TaskDef --network-configuration awsvpcConfiguration={subnets=[$SubnetId],assignPublicIp=ENABLED}` |
| gl-18 | s10 | `aws ecs deregister-task-definition --task-definition $TaskDef` |
| gl-18 | s11 | `aws ecs delete-cluster --cluster workbook-gl18` |
| gl-18 | s14 | `aws resourcegroupstaggingapi get-resources --tag-filters Key=LabId,Values=gl-18` |
| gl-19 | s02 | `aws sts get-caller-identity` |
| gl-19 | s03 | `aws --version` |
| gl-19 | s03 | `Terraform is not required unless a step says so.` |
| gl-19 | s06 | `aws iam create-role --role-name workbook-gl19-eks --assume-role-policy-document file://gl19-eks-trust.json --tags Key=Workbook,Value=aws-tf-lab Key=LabId,Value=gl-19 Key=CreatedAt,Value=$CreatedAt Key=ExpiresAt,Value=$ExpiresAt` |
| gl-19 | s06 | `aws iam attach-role-policy --role-name workbook-gl19-eks --policy-arn arn:aws:iam::aws:policy/AmazonEKSClusterPolicy` |
| gl-19 | s06 | `aws iam get-role --role-name workbook-gl19-eks --query Role.Arn --output text` |
| gl-19 | s07 | `aws ec2 describe-vpcs --filters Name=isDefault,Values=true --query "Vpcs[0].VpcId" --output text` |
| gl-19 | s07 | `aws ec2 describe-subnets --filters Name=vpc-id,Values=$VpcId --query "Subnets[0:2].SubnetId" --output text` |
| gl-19 | s07 | `aws eks create-cluster --name workbook-gl19 --role-arn $EksRoleArn --resources-vpc-config subnetIds=$Subnets --tags LabId=gl-19,Workbook=aws-tf-lab` |
| gl-19 | s07 | `aws eks wait cluster-active --name workbook-gl19` |
| gl-19 | s08 | `aws eks describe-cluster --name workbook-gl19` |
| gl-19 | s09 | `aws eks delete-cluster --name workbook-gl19` |
| gl-19 | s09 | `aws eks wait cluster-deleted --name workbook-gl19` |
| gl-19 | s10 | `aws iam detach-role-policy --role-name workbook-gl19-eks --policy-arn arn:aws:iam::aws:policy/AmazonEKSClusterPolicy` |
| gl-19 | s10 | `aws iam delete-role --role-name workbook-gl19-eks` |
| gl-19 | s14 | `aws resourcegroupstaggingapi get-resources --tag-filters Key=LabId,Values=gl-19` |
| gl-20 | s02 | `aws sts get-caller-identity` |
| gl-20 | s03 | `aws --version` |
| gl-20 | s03 | `Terraform is not required unless a step says so.` |
| gl-20 | s07 | `terraform init` |
| gl-20 | s08 | `terraform fmt` |
| gl-20 | s08 | `terraform validate` |
| gl-20 | s09 | `terraform plan -var bucket_suffix=$Suffix -out gl20.tfplan` |
| gl-20 | s09 | `terraform apply gl20.tfplan` |
| gl-20 | s09 | `terraform output -raw bucket_name` |
| gl-20 | s10 | `terraform state list` |
| gl-20 | s11 | `aws s3api put-bucket-tagging --bucket $Bucket --tagging "TagSet=[{Key=OOB,Value=manual},{Key=LabId,Value=gl-20}]"` |
| gl-20 | s11 | `terraform plan -refresh-only -var bucket_suffix=$Suffix` |
| gl-20 | s13 | `terraform destroy -var bucket_suffix=$Suffix` |
| gl-20 | s13 | `terraform local state artifacts from disk; state stays gitignored.` |
| gl-20 | s14 | `aws s3api head-bucket.` |
| gl-20 | s14 | `aws resourcegroupstaggingapi get-resources --tag-filters Key=LabId,Values=gl-20 returns an empty ResourceTagMappingList in $env:AWS_REGION` |
| gl-21 | s02 | `aws sts get-caller-identity` |
| gl-21 | s03 | `aws --version` |
| gl-21 | s03 | `Terraform is not required unless a step says so.` |
| gl-21 | s06 | `aws ec2 describe-vpcs --filters Name=isDefault,Values=true --query "Vpcs[0].VpcId" --output text` |
| gl-21 | s06 | `aws ec2 describe-subnets --filters Name=vpc-id,Values=$VpcId --query "Subnets[0:2].SubnetId" --output text` |
| gl-21 | s06 | `aws elasticache create-cache-subnet-group --cache-subnet-group-name workbook-gl21 --cache-subnet-group-description gl21 --subnet-ids $Subnets` |
| gl-21 | s07 | `aws elasticache create-cache-cluster --cache-cluster-id workbook-gl21 --engine redis --cache-node-type cache.t3.micro --num-cache-nodes 1 --cache-subnet-group-name workbook-gl21 --tags Key=LabId,Value=gl-21 Key=Workbook,Value=aws-tf-lab` |
| gl-21 | s07 | `aws elasticache wait cache-cluster-available --cache-cluster-id workbook-gl21` |
| gl-21 | s08 | `aws elasticache describe-cache-clusters --cache-cluster-id workbook-gl21 --show-cache-node-info` |
| gl-21 | s09 | `aws elasticache delete-cache-cluster --cache-cluster-id workbook-gl21` |
| gl-21 | s09 | `aws elasticache wait cache-cluster-deleted --cache-cluster-id workbook-gl21` |
| gl-21 | s10 | `aws elasticache delete-cache-subnet-group --cache-subnet-group-name workbook-gl21` |
| gl-21 | s14 | `aws resourcegroupstaggingapi get-resources --tag-filters Key=LabId,Values=gl-21` |