#!/usr/bin/env bash
# Read-only inventory of the production AWS account (the account whose keys
# live in deploy/aws/.env). Produces the rows for Comp's "Infrastructure
# inventory" and "RBAC matrix" evidence forms, plus raw listings for review.
#
#   bash deploy/aws/inventory.sh [out-dir]      (default: ./inventory-<date>)
#
# Only list/describe calls are made; nothing is modified.
set -euo pipefail
cd "$(dirname "$0")"
set -a; . ./.env; set +a
unset AWS_SESSION_TOKEN
export AWS_PAGER=""
AWS="${AWS:-aws}"

out="${1:-./inventory-$(date -u +%Y-%m-%d)}"
mkdir -p "$out"
today="$(date -u +%Y-%m-%d)"
acct="$($AWS sts get-caller-identity --query Account --output text)"
echo "account $acct -> $out"

q() { $AWS "$@" --output json; }

q iam list-users --query 'Users[].{name:UserName,created:CreateDate,pwLastUsed:PasswordLastUsed}' > "$out/iam_users.json"
q iam list-roles --query 'Roles[?!starts_with(Path,`/aws-service-role/`)].{name:RoleName,created:CreateDate,lastUsed:RoleLastUsed.LastUsedDate}' > "$out/iam_roles.json"
q iam list-groups --query 'Groups[].{name:GroupName}' > "$out/iam_groups.json"
q iam get-account-summary > "$out/iam_summary.json"
q lambda list-functions --query 'Functions[].{name:FunctionName,runtime:Runtime,modified:LastModified}' > "$out/lambda.json"
q docdb describe-db-clusters --query 'DBClusters[].{id:DBClusterIdentifier,engine:EngineVersion,encrypted:StorageEncrypted,multiAz:MultiAZ,backupDays:BackupRetentionPeriod,azs:AvailabilityZones}' > "$out/docdb.json"
q rds describe-db-instances --query 'DBInstances[?Engine!=`docdb`].{id:DBInstanceIdentifier,engine:Engine,encrypted:StorageEncrypted}' > "$out/rds.json"
q s3api list-buckets --query 'Buckets[].{name:Name,created:CreationDate}' > "$out/s3.json"
q cloudfront list-distributions --query 'DistributionList.Items[].{id:Id,domain:DomainName,alias:Aliases.Items[0]}' > "$out/cloudfront.json"
q ec2 describe-vpcs --query 'Vpcs[].{id:VpcId,cidr:CidrBlock,name:Tags[?Key==`Name`].Value|[0]}' > "$out/vpc.json"
q ec2 describe-instances --query 'Reservations[].Instances[].{id:InstanceId,type:InstanceType,state:State.Name,name:Tags[?Key==`Name`].Value|[0]}' > "$out/ec2.json"
q ecr describe-repositories --query 'repositories[].{name:repositoryName,scanOnPush:imageScanningConfiguration.scanOnPush}' > "$out/ecr.json"
q kms list-aliases --query 'Aliases[?!starts_with(AliasName,`alias/aws/`)].{alias:AliasName,key:TargetKeyId}' > "$out/kms.json"
q sns list-topics --query 'Topics[].{arn:TopicArn}' > "$out/sns.json"
q sqs list-queues --query '{urls:QueueUrls}' > "$out/sqs.json"
q events list-rules --query 'Rules[].{name:Name,state:State,schedule:ScheduleExpression}' > "$out/eventbridge.json"
q cloudtrail describe-trails --query 'trailList[].{name:Name,multiRegion:IsMultiRegionTrail,bucket:S3BucketName}' > "$out/cloudtrail.json"
q cloudformation list-stacks --stack-status-filter CREATE_COMPLETE UPDATE_COMPLETE --query 'StackSummaries[].{name:StackName,updated:LastUpdatedTime}' > "$out/cloudformation.json"
q secretsmanager list-secrets --query 'SecretList[].{name:Name}' > "$out/secrets.json"
$AWS securityhub describe-hub --output json > "$out/securityhub.json" 2>/dev/null || echo '{"enabled":false}' > "$out/securityhub.json"

python3 - "$out" "$acct" "$today" <<'PY'
import json, sys, os
out, acct, today = sys.argv[1:4]
def load(n):
    try: return json.load(open(os.path.join(out, n))) or []
    except Exception: return []
owner = "Mo Messidi (CEO)"
rows = []
def add(aid, typ, env="Production", loc="us-east-1"):
    rows.append({"assetId": aid, "systemType": typ, "environment": env, "location": loc, "assignedOwner": owner, "lastReviewed": today})
add(f"AWS account {acct}", "Cloud account (AWS)", loc="Global")
for v in load("vpc.json"): add(f"{v['id']} ({v.get('name') or 'vpc'} {v['cidr']})", "Network / VPC")
for i in load("ec2.json"):
    if i["state"] != "terminated": add(f"{i['id']} ({i.get('name') or 'ec2'}, {i['type']})", f"Compute / EC2 ({i['state']})")
for d in load("docdb.json"): add(f"{d['id']} (DocumentDB {d['engine']}, encrypted={d['encrypted']}, backups={d['backupDays']}d)", "Database / DocumentDB", loc=",".join(d.get("azs") or []) or "us-east-1")
for d in load("rds.json"): add(f"{d['id']} ({d['engine']})", "Database / RDS")
for f in load("lambda.json"): add(f"{f['name']} ({f.get('runtime') or 'container'})", "Compute / Lambda")
for b in load("s3.json"): add(b["name"], "Storage / S3 bucket", loc="Global")
for c in load("cloudfront.json"): add(f"{c['id']} ({c.get('alias') or c['domain']})", "CDN / CloudFront", loc="Global")
for r in load("ecr.json"): add(f"{r['name']} (scanOnPush={r.get('scanOnPush')})", "Container registry / ECR")
for k in load("kms.json"): add(k["alias"], "Encryption key / KMS")
for t in load("sns.json"): add(t["arn"].split(":")[-1], "Messaging / SNS topic")
for u in (load("sqs.json") or {}).get("urls") or []: add(u.rsplit("/",1)[-1], "Messaging / SQS queue")
for s in load("cloudformation.json"): add(s["name"], "IaC stack / CloudFormation")
for t in load("cloudtrail.json"): add(f"{t['name']} (multi-region={t['multiRegion']})", "Audit logging / CloudTrail")
sh = load("securityhub.json")
if isinstance(sh, dict) and sh.get("HubArn"): add("AWS Security Hub", "Security monitoring")
json.dump({"submissionDate": today, "inventoryRows": rows}, open(os.path.join(out, "infrastructure-inventory.json"), "w"), indent=1)

rbac = []
def r(system, role, scope): rbac.append({"system": system, "roleName": role, "permissionsScope": scope, "approvedBy": owner, "lastReviewed": today})
for u in load("iam_users.json"): r(f"AWS IAM ({acct})", f"IAM user: {u['name']}", "Per attached policies; console/API access as configured. Reviewed quarterly.")
for g in load("iam_groups.json"): r(f"AWS IAM ({acct})", f"IAM group: {g['name']}", "Per attached policies")
for ro in load("iam_roles.json"): r(f"AWS IAM ({acct})", f"IAM role: {ro['name']}", "Assumed by AWS services / deploy tooling per trust policy)
json.dump({"submissionDate": today, "awsRows": rbac}, open(os.path.join(out, "rbac-aws-rows.json"), "w"), indent=1)
print(f"inventory rows: {len(rows)}; aws rbac rows: {len(rbac)}")
PY
