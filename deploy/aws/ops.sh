#!/usr/bin/env bash
# Operator helpers for the self-hosted Comp workers.
#
#   deploy/aws/ops.sh run-status <app|api> <runId> <COMPLETED|FAILED> [error message]
#       Resolve a background run that died with the worker (e.g. the onboarding
#       run shown in "Setting up your organization").
#   deploy/aws/ops.sh run-task <app|api> <taskId> [json payload]
#       Fire a scheduled task now (same event EventBridge sends).
#   deploy/aws/ops.sh health [hours]
#       Read-only: Lambda error/invocation counts, EventBridge rule state and
#       recent worker log errors for the last N hours (default 24).
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
  health)
    hours="${2:-24}"; start="$(date -u -d "-${hours} hours" +%Y-%m-%dT%H:%M:%SZ 2>/dev/null || date -u -v-${hours}H +%Y-%m-%dT%H:%M:%SZ)"; end="$(date -u +%Y-%m-%dT%H:%M:%SZ)"
    echo "== Lambda invocations / errors (last ${hours}h)"
    for fn in api app portal apiWorker appWorker; do
      inv="$(aws cloudwatch get-metric-statistics --namespace AWS/Lambda --metric-name Invocations --dimensions Name=FunctionName,Value="comp-${STAGE}-${fn}" --start-time "$start" --end-time "$end" --period 86400 --statistics Sum --query 'sum(Datapoints[].Sum)' --output text)"
      err="$(aws cloudwatch get-metric-statistics --namespace AWS/Lambda --metric-name Errors --dimensions Name=FunctionName,Value="comp-${STAGE}-${fn}" --start-time "$start" --end-time "$end" --period 86400 --statistics Sum --query 'sum(Datapoints[].Sum)' --output text)"
      printf '  %-10s invocations=%-6s errors=%s\n' "$fn" "${inv/None/0}" "${err/None/0}"
    done
    echo "== EventBridge rules"
    aws events list-rules --name-prefix "comp-${STAGE}-" --query 'Rules[].[Name,State,ScheduleExpression]' --output text | sed 's/^/  /'
    echo "== Worker log errors (last ${hours}h)"
    for fn in apiWorker appWorker; do
      echo "  -- comp-${STAGE}-${fn}"
      aws logs filter-log-events --log-group-name "/aws/lambda/comp-${STAGE}-${fn}" --start-time "$(( $(date -u +%s) * 1000 - hours * 3600000 ))" --filter-pattern '?ERROR ?Error ?"Task timed out"' --query 'events[-15:].message' --output text 2>/dev/null | cut -c1-220 | sed 's/^/     /' || echo "     (no log group yet)"
    done ;;
  *) sed -n 2,12p "$0"; exit 1 ;;
esac
