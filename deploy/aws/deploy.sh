#!/usr/bin/env bash
# Deal Intelligence self-hosted Comp — deployment driver.
#
#   deploy/aws/deploy.sh infra            # create/update shared CloudFormation stack
#   deploy/aws/deploy.sh build [tag]      # zip repo -> S3 -> CodeBuild builds+pushes images
#   deploy/aws/deploy.sh migrate [tag]    # CodeBuild run that only migrates (+SEED=true seeds)
#   deploy/aws/deploy.sh functions [tag]  # sls deploy api/app/portal from ECR images
#   deploy/aws/deploy.sh all [tag]        # infra -> build (+migrate) -> functions
#
# Needs: aws cli v2, node (for serverless), git. Credentials from the usual
# AWS env/profile. Region defaults to us-east-1.
set -euo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT="$(cd "$HERE/../.." && pwd)"
export AWS_DEFAULT_REGION="${AWS_DEFAULT_REGION:-us-east-1}"
PROJECT="${PROJECT:-comp}"
STACK="${PROJECT}-infra"
STAGE="${STAGE:-prod}"
cmd="${1:-}"; tag="${2:-$(git -C "$ROOT" rev-parse --short HEAD)}"

out() { aws cloudformation describe-stacks --stack-name "$STACK" --query "Stacks[0].Outputs[?OutputKey=='$1'].OutputValue" --output text; }

infra() {
  aws cloudformation deploy \
    --stack-name "$STACK" --template-file "$HERE/infra.yml" \
    --capabilities CAPABILITY_NAMED_IAM \
    --parameter-overrides "Project=$PROJECT" \
    --no-fail-on-empty-changeset
  aws cloudformation describe-stacks --stack-name "$STACK" --query 'Stacks[0].Outputs' --output table
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
  id="$(aws codebuild start-build --project-name "$project" \
        --environment-variables-override "$1" --query 'build.id' --output text)"
  echo "CodeBuild: $id"
  while :; do
    local status; status="$(aws codebuild batch-get-builds --ids "$id" --query 'builds[0].buildStatus' --output text)"
    [ "$status" = "IN_PROGRESS" ] || { echo "status: $status"; [ "$status" = "SUCCEEDED" ]; return; }
    sleep 20
  done
}

build() {
  upload_source
  run_build "[{\"name\":\"IMAGE_TAG\",\"value\":\"$tag\"},{\"name\":\"RUN_MIGRATIONS\",\"value\":\"${RUN_MIGRATIONS:-true}\"},{\"name\":\"SEED\",\"value\":\"${SEED:-false}\"}]"
}

migrate() {
  upload_source
  run_build "[{\"name\":\"IMAGE_TAG\",\"value\":\"$tag\"},{\"name\":\"TARGETS\",\"value\":\"migrator\"},{\"name\":\"RUN_MIGRATIONS\",\"value\":\"true\"},{\"name\":\"SEED\",\"value\":\"${SEED:-false}\"}]"
}

functions() {
  : "${HOSTED_ZONE_ID:?set HOSTED_ZONE_ID (Route 53 zone for dealintelligence.io)}"
  cd "$HERE" && npm install --silent --no-audit --no-fund
  for svc in api app portal; do
    echo "==> sls deploy $svc ($tag)"
    (cd "$HERE/$svc" && npx serverless deploy --stage "$STAGE" \
        --param="imageTag=$tag" --param="hostedZoneId=$HOSTED_ZONE_ID")
  done
}

case "$cmd" in
  infra) infra ;;
  build) build ;;
  migrate) migrate ;;
  functions) functions ;;
  all) infra; build; functions ;;
  *) sed -n 2,12p "$0"; exit 1 ;;
esac
