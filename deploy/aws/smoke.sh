#!/usr/bin/env bash
# Post-deploy smoke test: hits the three public hostnames and reports status.
# The first request after idle wakes Aurora (0 ACU) and cold-starts the Lambda,
# so each probe allows up to 120 s and retries once.
set -u
ROOT="${ROOT_DOMAIN:-dealintelligence.io}"
probe() { # name url expected-substring
  local name=$1 url=$2 want=$3 code body
  for attempt in 1 2; do
    body=$(curl -s --max-time 120 -w '\n%{http_code} %{time_total}' "$url")
    code=$(tail -1 <<<"$body"); body=$(sed '$d' <<<"$body")
    if [[ "$code" == 200* && "$body" == *"$want"* ]]; then
      printf '  ok   %-8s %s (%s)\n' "$name" "$url" "$code"; return 0
    fi
    [ $attempt = 1 ] && sleep 5
  done
  printf '  FAIL %-8s %s -> %s\n       %s\n' "$name" "$url" "$code" "${body:0:200}"; return 1
}
rc=0
probe api    "https://api.compliance.$ROOT/v1/health"   '"ok"' || rc=1
probe app    "https://compliance.$ROOT/api/health"      'ok'       || rc=1
probe portal "https://portal.compliance.$ROOT/"         '<html'    || rc=1
probe login  "https://compliance.$ROOT/auth"            '<html'    || rc=1
exit $rc
