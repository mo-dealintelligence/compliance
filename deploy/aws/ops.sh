#!/usr/bin/env bash
# Operator helpers for the self-hosted Comp workers.
#
#   deploy/aws/ops.sh run-status <app|api> <runId> <COMPLETED|FAILED> [error message]
#       Resolve a background run that died with the worker (e.g. the onboarding
#       run shown in "Setting up your organization").
#   deploy/aws/ops.sh run-task <app|api> <taskId> [json payload]
#       Fire a scheduled task now (same event EventBridge sends).
set -euo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
if [ -f "$HERE/.env" ]; then set -a; . "$HERE/.env"; set +a; fi
unset AWS_SESSION_TOKEN
STAGE="${STAGE:-prod}"
assume_role() {
  [ -z "${COMP_ACCOUNT_ID:-}" ] && return 0
  [ "$(aws sts get-caller-identity --query Account --output text)" = "$COMP_ACCOUNT_ID" ] && return 0
  local c; c="$(aws sts assume-role --role-arn "arn:aws:iam::${COMP_ACCOUNT_ID}:role/OrganizationAccountAccessRole" --role-session-name comp-ops --query Credentials --output json)"
  export AWS_ACCESS_KEY_ID="$(python3 -c 'import json,sys; print(json.load(sys.stdin)["AccessKeyId"])' <<<"$c")"
  export AWS_SECRET_ACCESS_KEY="$(python3 -c 'import json,sys; print(json.load(sys.stdin)["SecretAccessKey"])' <<<"$c")"
  export AWS_SESSION_TOKEN="$(python3 -c 'import json,sys; print(json.load(sys.stdin)["SessionToken"])' <<<"$c")"
}
invoke() { # fn payload
  local out; out="$(mktemp)"
  aws lambda invoke --function-name "comp-${STAGE}-$1" --payload "$2" --cli-binary-format raw-in-base64-out "$out" >/dev/null 2>&1 \
    || aws lambda invoke --function-name "comp-${STAGE}-$1" --payload "$2" "$out" >/dev/null
  cat "$out"; echo
}
assume_role
case "${1:-}" in
  run-status)
    fn="${2:?app|api}Worker"; payload="$(python3 -c 'import json,sys; print(json.dumps({"source":"admin","action":"set-run-status","runId":sys.argv[1],"status":sys.argv[2],**({"error":sys.argv[3]} if len(sys.argv)>3 else {})}))' "$3" "$4" "${5:-}")"
    invoke "$fn" "$payload" ;;
  run-task)
    fn="${2:?app|api}Worker"; payload="$(python3 -c 'import json,sys; print(json.dumps({"source":"schedule","taskId":sys.argv[1],"payload":json.loads(sys.argv[2]) if len(sys.argv)>2 and sys.argv[2] else {}}))' "$3" "${4:-}")"
    invoke "$fn" "$payload" ;;
  *) sed -n 2,9p "$0"; exit 1 ;;
esac
