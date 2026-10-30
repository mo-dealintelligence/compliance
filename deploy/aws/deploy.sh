#!/usr/bin/env bash
# Deal Intelligence self-hosted Comp — deployment driver (single Serverless stack).
#
#   deploy/aws/deploy.sh infra            # phase 1: network, nat, db, buckets, ecr, codebuild, zone, certs
#   deploy/aws/deploy.sh delegate         # print/apply the NS delegation for compliance.dealintelligence.io (prod zone)
#   deploy/aws/deploy.sh build [tag]      # zip repo -> S3 -> CodeBuild builds+pushes images (+migrate/seed)
#   deploy/aws/deploy.sh migrate [tag]    # CodeBuild run that only migrates (+SEED=true seeds)
#   deploy/aws/deploy.sh functions [tag]  # phase 2: lambdas, function urls, cloudfront, dns
#   deploy/aws/deploy.sh bootstrap        # all of the above in order; re-runnable (DR / fresh account)
#   deploy/aws/deploy.sh restore <snapshot-id>  # bootstrap, but the database comes from a snapshot
#   deploy/aws/deploy.sh snapshot         # take a manual cluster snapshot now (comp-db-<date>)
#
# Credentials: run with the di-compliance account. From the management
# account, export COMP_ACCOUNT_ID and the script assumes
# OrganizationAccountAccessRole for you.
set -euo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT="$(cd "$HERE/../.." && pwd)"
# Load deploy/aws/.env when present; a stale session token from an earlier
# assume-role would otherwise break the long-term keys.
if [ -f "$HERE/.env" ]; then set -a; . "$HERE/.env"; set +a; fi
unset AWS_SESSION_TOKEN
export AWS_DEFAULT_REGION="${AWS_DEFAULT_REGION:-us-east-1}"
STAGE="${STAGE:-prod}"
STACK="comp-${STAGE}"
cmd="${1:-}"; tag="$(git -C "$ROOT" rev-parse --short HEAD)"
case "$cmd" in build|migrate|functions) tag="${2:-$tag}" ;; esac

assume_role() {
  [ -z "${COMP_ACCOUNT_ID:-}" ] && return 0
  local current; current="$(aws sts get-caller-identity --query Account --output text)"
  [ "$current" = "$COMP_ACCOUNT_ID" ] && return 0
  unset AWS_SESSION_TOKEN
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
  sls deploy --stage "$STAGE" --param="phase=infra" --param="dbSnapshot=${DB_SNAPSHOT:-}"
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
  sls deploy --stage "$STAGE" --param="phase=all" --param="imageTag=$tag" --param="dbSnapshot=${DB_SNAPSHOT:-}"
}

snapshot() {
  assume_role
  local id="${STACK}-db-$(date -u +%Y%m%d-%H%M)"
  aws rds create-db-cluster-snapshot --db-cluster-identifier "${STACK%-*}-db" --db-cluster-snapshot-identifier "$id" --query 'DBClusterSnapshot.Status' --output text
  echo "snapshot $id"
}

# Full build-out in order. Every step is idempotent, so a failed run is simply
# re-run. Credentials: prod keys from .env; the script assumes the compliance
# role where needed and uses the prod keys for the NS delegation.
bootstrap() {
  local backup="${SECRETS_BACKUP:-$HOME/di-run-logs/comp-deploy/secrets-backup.json}"
  echo "### 1/6 infra"; infra
  echo "### 2/6 delegate"; (unset COMP_ACCOUNT_ID; delegate) || echo "delegation skipped/failed (set PROD_ZONE_ID); certs will wait"
  echo "### 3/6 secrets"
  assume_role
  if [ "$(aws secretsmanager get-secret-value --secret-id comp/env/api --query SecretString --output text)" = "{}" ]; then
    if [ -f "$backup" ]; then bash "$HERE/secrets.sh" restore "$backup"
    else bash "$HERE/secrets.sh" init; fi
  else echo "secrets already present"; fi
  echo "### 4/6 build + migrate$( [ -n "${DB_SNAPSHOT:-}" ] || echo ' + seed')"
  if [ -n "${DB_SNAPSHOT:-}" ]; then SEED=false build; else SEED=true build; fi
  echo "### 5/6 functions"; functions
  echo "### 6/6 smoke"; bash "$HERE/smoke.sh" || echo "smoke test failed (cold start?) — rerun deploy/aws/smoke.sh"
  bash "$HERE/secrets.sh" backup "$backup" >/dev/null && echo "secrets backed up to $backup"
}

case "$cmd" in
  infra) infra ;;
  delegate) delegate ;;
  __ns) assume_role; out HostedZoneNameServers ;;
  build) build ;;
  migrate) migrate ;;
  functions) functions ;;
  bootstrap) bootstrap ;;
  restore) DB_SNAPSHOT="${2:?snapshot id}" bootstrap ;;
  snapshot) snapshot ;;
  *) sed -n 2,15p "$0"; exit 1 ;;
esac
