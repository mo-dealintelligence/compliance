#!/usr/bin/env bash
# Manage the three env secrets (comp/env/api, comp/env/app, comp/env/portal).
#
#   deploy/aws/secrets.sh init   # build all three from infra outputs + random
#                                # secrets + values in $SECRETS_INPUT (json file)
#   deploy/aws/secrets.sh set api KEY value   # upsert one key
#   deploy/aws/secrets.sh show api            # print keys (values masked)
#
# SECRETS_INPUT is a JSON file you keep OUTSIDE the repo with third-party
# values: RESEND_API_KEY, AUTH_GOOGLE_ID, AUTH_GOOGLE_SECRET, OPENAI_API_KEY,
# LOGO_DEV_TOKEN (optional).
set -euo pipefail
export AWS_DEFAULT_REGION="${AWS_DEFAULT_REGION:-us-east-1}"
PROJECT="${PROJECT:-comp}"; STACK="${PROJECT}-infra"
ROOT_DOMAIN="dealintelligence.io"

out() { aws cloudformation describe-stacks --stack-name "$STACK" --query "Stacks[0].Outputs[?OutputKey=='$1'].OutputValue" --output text; }
rnd() { openssl rand -base64 32 | tr -d '\n'; }
get_secret() { aws secretsmanager get-secret-value --secret-id "$1" --query SecretString --output text; }
put_secret() { aws secretsmanager put-secret-value --secret-id "$1" --secret-string "$2" >/dev/null; }

init() {
  local input="${SECRETS_INPUT:?set SECRETS_INPUT=/path/to/input.json}"
  local db_host db_secret pw s3_secret
  db_host="$(out DbEndpoint)"; db_secret="$(out DbMasterSecretArn)"
  pw="$(get_secret "$db_secret" | python3 -c 'import json,sys,urllib.parse; print(urllib.parse.quote(json.load(sys.stdin)["password"], safe=""))')"
  s3_secret="$(get_secret "$(out AppUserKeySecret)")"
  local db_url="postgresql://comp:${pw}@${db_host}:5432/comp?sslmode=require"
  local bucket; bucket="$(out EvidenceBucket)"

  local auth_secret secret_key reval unsub internal svc_trigger svc_portal
  auth_secret="$(rnd)"; secret_key="$(rnd)"; reval="$(rnd)"; unsub="$(rnd)"
  internal="$(rnd)"; svc_trigger="$(rnd)"; svc_portal="$(rnd)"

  python3 - "$input" "$db_url" "$bucket" "$s3_secret" "$auth_secret" "$secret_key" "$reval" "$unsub" "$internal" "$svc_trigger" "$svc_portal" "$ROOT_DOMAIN" <<'EOF' > /tmp/comp-secrets.json
import json, sys
(inp, db_url, bucket, s3_json, auth_secret, secret_key, reval, unsub, internal,
 svc_trigger, svc_portal, root) = sys.argv[1:]
ext = json.load(open(inp)); s3 = json.loads(s3_json)
app_url, api_url, portal_url, trust_url = (f"https://{p}.{root}" for p in ("compliance","compliance-api","compliance-portal","trust"))
brand = {
  "NEXT_PUBLIC_BRAND_NAME": "Deal Intelligence",
  "NEXT_PUBLIC_BRAND_PRODUCT_NAME": "Deal Intelligence Compliance",
  "NEXT_PUBLIC_WEBSITE_URL": f"https://{root}",
  "NEXT_PUBLIC_SUPPORT_EMAIL": f"security@{root}",
  "NEXT_PUBLIC_TERMS_URL": f"https://{root}/terms",
  "NEXT_PUBLIC_PRIVACY_URL": f"https://{root}/privacy",
  "NEXT_PUBLIC_BRAND_LOGO_URL": f"https://{root}/logo.png",
}
shared = {
  "DATABASE_URL": db_url, "SELF_HOSTED": "true", "NODE_ENV": "production",
  "COOKIE_DOMAIN": f".{root}",
  "AUTH_TRUSTED_ORIGINS": ",".join([app_url, portal_url, api_url, trust_url]),
  "AUTH_TRUSTED_ORIGIN_SUFFIXES": root,
  "RESEND_API_KEY": ext.get("RESEND_API_KEY",""),
  "RESEND_DOMAIN": f"mail.{root}",
  "RESEND_FROM_SYSTEM": f"Deal Intelligence <noreply@mail.{root}>",
  "RESEND_FROM_DEFAULT": f"Deal Intelligence <hello@mail.{root}>",
  "RESEND_FROM_TRUST_PORTAL": f"Deal Intelligence <noreply@mail.{root}>",
  "UNSUBSCRIBE_SECRET": unsub, "INTERNAL_API_TOKEN": internal,
  "KV_BACKEND": "postgres",
  "APP_AWS_REGION": "us-east-1", "APP_AWS_BUCKET_NAME": bucket,
  "APP_AWS_ORG_ASSETS_BUCKET": bucket, "APP_AWS_QUESTIONNAIRE_UPLOAD_BUCKET": bucket,
  "APP_AWS_KNOWLEDGE_BASE_BUCKET": bucket,
  "APP_AWS_ACCESS_KEY_ID": s3["APP_AWS_ACCESS_KEY_ID"],
  "APP_AWS_SECRET_ACCESS_KEY": s3["APP_AWS_SECRET_ACCESS_KEY"],
  "OPENAI_API_KEY": ext.get("OPENAI_API_KEY",""),
  "NEXT_PUBLIC_APP_URL": app_url, "NEXT_PUBLIC_API_URL": api_url,
  "NEXT_PUBLIC_PORTAL_URL": portal_url, "NEXT_PUBLIC_TRUST_URL": trust_url,
  **brand,
}
api = {**shared,
  "BASE_URL": api_url, "BETTER_AUTH_URL": app_url, "PORTAL_URL": portal_url,
  "TRUST_APP_URL": trust_url, "SECRET_KEY": secret_key, "AUTH_SECRET": auth_secret,
  "AUTH_GOOGLE_ID": ext.get("AUTH_GOOGLE_ID",""), "AUTH_GOOGLE_SECRET": ext.get("AUTH_GOOGLE_SECRET",""),
  "SERVICE_TOKEN_TRIGGER": svc_trigger, "SERVICE_TOKEN_PORTAL": svc_portal,
  "NODE_EXTRA_CA_CERTS": "/usr/local/share/aws-rds-ca-bundle.pem",
}
app = {**shared,
  "AUTH_SECRET": auth_secret, "SECRET_KEY": secret_key, "REVALIDATION_SECRET": reval,
  "BETTER_AUTH_URL": app_url, "NEXT_PUBLIC_BETTER_AUTH_URL": app_url,
  "NEXT_PUBLIC_SELF_HOSTED": "true", "NEXT_PUBLIC_APP_ENV": "production",
  "SERVICE_TOKEN_TRIGGER": svc_trigger,
  "NEXT_PUBLIC_LOGO_DEV_TOKEN": ext.get("LOGO_DEV_TOKEN",""),
  "NEXT_OUTPUT_STANDALONE": "true",
}
portal = {**shared,
  "BETTER_AUTH_SECRET": auth_secret, "BETTER_AUTH_URL": portal_url,
  "NEXT_PUBLIC_BETTER_AUTH_URL": portal_url, "SERVICE_TOKEN_PORTAL": svc_portal,
}
json.dump({"api": api, "app": app, "portal": portal}, sys.stdout)
EOF
  for svc in api app portal; do
    put_secret "$PROJECT/env/$svc" "$(python3 -c "import json;print(json.dumps(json.load(open('/tmp/comp-secrets.json'))['$svc']))")"
    echo "wrote $PROJECT/env/$svc"
  done
  rm -f /tmp/comp-secrets.json
}

set_key() {
  local svc="$1" key="$2" value="$3"
  local cur; cur="$(get_secret "$PROJECT/env/$svc")"
  put_secret "$PROJECT/env/$svc" "$(python3 -c "import json,sys; d=json.loads(sys.argv[1]); d[sys.argv[2]]=sys.argv[3]; print(json.dumps(d))" "$cur" "$key" "$value")"
  echo "updated $svc.$key"
}

show() { get_secret "$PROJECT/env/$1" | python3 -c 'import json,sys; d=json.load(sys.stdin); [print(f"{k}={"*"*8 if any(t in k for t in ("SECRET","TOKEN","KEY","PASSWORD","DATABASE_URL")) else v}") for k,v in sorted(d.items())]'; }

case "${1:-}" in
  init) init ;;
  set) set_key "$2" "$3" "$4" ;;
  show) show "$2" ;;
  *) sed -n 2,13p "$0"; exit 1 ;;
esac
