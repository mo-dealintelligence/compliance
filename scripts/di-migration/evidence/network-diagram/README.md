# Network flow diagrams — di-backend-api production

| File | Audience |
|---|---|
| `di-backend-network-internal-2026-11-01.png` | Engineering, auditor. Every system and every connection. |
| `di-backend-network-customer-2026-11-01.png` | Customers. Customer systems are the only outside parties; no operator path. |

Drawn to the usual network-flow-diagram conventions (PCI DSS 1.2.3/1.2.4 style):

- Trust boundaries are dashed boxes: Internet, AWS account, VPC, each subnet with its CIDR.
- Entry points are separate nodes, one per interface: web app (browser, Netlify-hosted),
  REST API clients, MCP clients. All three enter through CloudFront + the self-managed WAF.
- Arrows are connections, drawn from the side that opens the connection, labelled with
  protocol and port. Solid = application traffic. Dashed = administrative access
  (operator → SSM → bastion → DocumentDB).
- Outside systems are labelled by name and the protocol used to reach them (customer CRMs and Slack via the NAT).
- Version, date, and owner are in the header.

No authentication detail is on the diagram (that belongs in the data-flow diagram and the
access-control policy). The `documentdb-proxy` Lambda is not drawn — it is scheduled for
removal.

Source: `make_network_diagram.py` (writes the `.svg` and dated `.png`). Icons are the
official AWS Architecture Icons, vendored in `aws-icons/`.

The WAF and the NAT are self-managed rather than the AWS managed services — an
application WAF (origin verification, shared rate limiting, header rules) in front of
the Lambdas, and a t3.micro NAT instance instead of a NAT Gateway. In policy text say
"self-managed WAF" and "NAT instance", never "AWS WAF" or "NAT Gateway".

Facts as of 2026-11-01 from `serverless.yml` (CIDRs), DNS, and
`di-backend-api/docs/infra-edge-review-2026-11-01.md`. Fargate tasks run in the public
subnet; their calls
back to the API go through CloudFront like any other client.
