# Network diagram — di-backend-api production

Two versions, same facts:

| File | Source | Use |
|---|---|---|
| `di-backend-network-designed-2026-11-01.png` | `make_network_diagram.py` → `di-backend-network-designed.svg` | The presentable one, in the house style of the 2025 Data Flow Diagram. CloudFront and the NAT instance are drawn **on** the account boundary: everything in crosses CloudFront, everything out crosses the NAT. |
| `di-backend-network-2026-11-01.png` | `di-backend-network.mmd` (Mermaid) | Dense engineering view; quick to edit, renders with `mmdc -i di-backend-network.mmd -o out.png -b white -w 2400`. |

Facts verified read-only against account 164482277879 on 2026-11-01, from
`di-backend-api/docs/infra-edge-review-2026-11-01.md` and
`docs/auth-hardening-2026-11-01.md`.

## What changed from the 2026-10-31 version
- **Edge protection added** (what Mo calls "the WAF, done the way we did the NAT" — built in
  code rather than bought as a managed service): `X-Origin-Verify` header checked by
  `OriginVerifyMiddleware`, so a direct hit on the app Lambda function URL gets 403; rate
  limiting moved out of per-Lambda memory into DocumentDB (`rate_limits`, TTL), keyed by
  credential then IP, fail-open; security headers and log redaction. **There is no AWS WAF**
  in the account or in `serverless.yml` — deliberately (no paid serverless.yml resources).
- **API auth**: `X-Internal-Key` header replaces the master key in URL paths (the URL now
  carries the placeholder `__master__`); PropelAuth bearer for app users, PropelAuth API keys
  for MCP and the `/v1/li` customer routes; tenant taken from the token; 112 routes
  authenticated; `/v1/webhook-hubspot` and the duplicate `app.py` removed.
- **Fargate egress corrected**: tasks run in the public subnet with their own public IP, so job
  egress does **not** pass through the NAT (finding A of the infra edge review). The previous
  diagram implied it did.
- CloudFront shown serving both `api.` and `mcp.` (the old one named only `mcp.`).
- Function URL authorizers shown per function: app origin-verified, mcp bearer,
  batchOrchestrator and documentdb-proxy SigV4.
- Bastion shown as a task definition with no instance running.
- Security Hub and AWS Config dropped from the picture: Config is not in use, and Security Hub
  is being retired in favour of the monthly configuration-check Lambda (decision D12,
  2026-10-31). Logging is CloudTrail multi-region with log-file validation, VPC flow logs and
  CloudWatch Logs at 90 days.

## Regenerating
```
python3 make_network_diagram.py      # svg + png, no arguments
```
