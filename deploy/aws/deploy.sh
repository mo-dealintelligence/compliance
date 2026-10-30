#!/usr/bin/env bash
# Deal Intelligence self-hosted Comp — deployment driver (single Serverless stack).
#
#   deploy/aws/deploy.sh infra            # phase 1: network, nat, db, buckets, ecr, codebuild, zone, certs
#   deploy/aws/deploy.sh delegate         # print/apply the NS delegation for compliance.dealintelligence.io (prod zone)
#   deploy/aws/deploy.sh build [tag]      # zip repo -> S3 -> CodeBuild builds+pushes images (+migrate/seed)
#   deploy/aws/deploy.sh migrate [tag]    # CodeBuild run that only migrates (+SEED=true seeds)
#   deploy/aws/deploy.sh functions [tag]  # phase 2: lambdas, function urls, cloudfront, dns
#
# Credentials: run with the di-compliance account. From the management
# account, export COMP_ACCOUNT_ID and the script assumes
# OrganizationAccountAccessRole for you.
set -euo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT="$(cd "$HERE/../.." && pwd)"
export AWS_DEFAULT_REGION="${AWS_DEFAULT_REGION:-us-east-1}"
STAGE="${STAGE:-prod}"
STACK="comp-${STAGE}"
cmd="${1:-}"; tag="${2:-$(git -C "$ROOT" rev-parse --short HEAD)}"

assume_role() {
  [ -z "${COMP_ACCOUNT_ID:-}" ] && return 0
  local current; current="$(aws sts get-caller-identity --query Account --output text)"
  [ "$current" = "$COMP_ACCOUNT_ID" ] && return 0
  local creds
  creds="$(aws sts assume-role --role-arn "arn:aws:iam::${COMP_ACCOUNT_ID}:role/OrganizationAccountAccessRole" \
           --role-session-name comp-deploy --duration-seconds 3600 --query 'Credentials' --output json)"
  export AWS_ACCESS_KEY_ID="$(echo "$creds" | python3 -c 'import json,sys; print(json.load(sys.stdin)["AccessKeyId"])')"
  export AWS_SECRET_ACCESS_KEY="$(echo "$creds" | python3 -c 'import json,sys; print(json.load(sys.stdin)["SecretAccessKey"])')"
  export AWS_SESSION_TOKEN="$(echo "$creds" | python3 -c 'import json,sys; print(json.load(sys.stdin)["SessionToken"])')"
}

out() { aws cloudformation describe-stacks --stack-name "$STACK" --query "Stacks[0].Outputs[?OutputKey=='$1'].OutputValue" --output text; }

sls() { (cd "$HERE" && npm install --silent --no-audit --no-fund >/dev/null && npx serverless "$@"); }

infra() {
  assume_role
  sls deploy --stage "$STAGE" --param="phase=infra"
  echo "Name servers for compliance.dealintelligence.io: $(out HostedZoneNameServers)"
}

delegate() {
  # Runs with PROD (management) credentials: adds the NS record in dealintelligence.io.
  local ns; ns="$(COMP_ACCOUNT_ID="$COMP_ACCOUNT_ID" bash -c 'source "'"$HERE"'/deploy.sh" __ns')"
  local zone="${PROD_ZONE_ID:?set PROD_ZONE_ID (dealintelligence.io hosted zone in the prod account)}"
  local rrs; rrs="$(echo "$ns" | tr ',' '\n' | sed 's/.*/{"Value":"&."}/' | paste -sd, -)"
  aws route53 change-resource-record-sets --hosted-zone-id "$zone" --change-batch \
    "{\"Changes\":[{\"Action\":\"UPSERT\",\"ResourceRecordSet\":{\"Name\":\"compliance.dealintelligence.io\",\"Type\":\"NS\",\"TTL\":300,\"ResourceRecords\":[${rrs}]}}]}"
  echo "delegated compliance.dealintelligence.io -> $ns"
}

upload_source() {
  local bucket; bucket="$(out SourceBucket)"
  local zip; zip="$(mktemp -d)/source.zip"
  git -C "$ROOT" archive --format=zip -o "$zip" HEAD
  aws s3 cp "$zip" "s3://$bucket/source.zip" --only-show-errors
}

run_build() { # $1 = env overrides json array
  local project; project="$(out BuildProject)"
  local id
  id="$(aws codebuild start-build --project-name "$project" --environment-variables-override "$1" --query 'build.id' --output text)"
  echo "CodeBuild: $id"
  while :; do
    local status; status="$(aws codebuild batch-get-builds --ids "$id" --query 'builds[0].buildStatus' --output text)"
    [ "$status" = "IN_PROGRESS" ] || { echo "status: $status"; [ "$status" = "SUCCEEDED" ]; return; }
    sleep 20
  done
}

build() {
  assume_role; upload_source
  run_build "[{\"name\":\"IMAGE_TAG\",\"value\":\"$tag\"},{\"name\":\"RUN_MIGRATIONS\",\"value\":\"${RUN_MIGRATIONS:-true}\"},{\"name\":\"SEED\",\"value\":\"${SEED:-false}\"}]"
}

migrate() {
  assume_role; upload_source
  run_build "[{\"name\":\"IMAGE_TAG\",\"value\":\"$tag\"},{\"name\":\"TARGETS\",\"value\":\"migrator\"},{\"name\":\"RUN_MIGRATIONS\",\"value\":\"true\"},{\"name\":\"SEED\",\"value\":\"${SEED:-false}\"}]"
}

functions() {
  assume_role
  sls deploy --stage "$STAGE" --param="phase=all" --param="imageTag=$tag"
}

case "$cmd" in
  infra) infra ;;
  delegate) delegate ;;
  __ns) assume_role; out HostedZoneNameServers ;;
  build) build ;;
  migrate) migrate ;;
  functions) functions ;;
  *) sed -n 2,12p "$0"; exit 1 ;;
esac
