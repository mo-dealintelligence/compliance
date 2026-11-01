# Network flow diagrams — di-backend-api production

| File | Audience |
|---|---|
| `di-backend-network-internal-2026-11-01.png` | Engineering, auditor. Every system and every connection. |
| `di-backend-network-customer-2026-11-01.png` | Customers. Their systems and the identity provider are the only outside parties; no data vendors. |

Nodes are systems. Arrows are connections, drawn from the side that opens the
connection, labelled with protocol and port. Nothing else is on the page.

Source: `make_network_diagram.py` (writes the `.svg` and dated `.png`). Icons are the
official AWS Architecture Icons, vendored in `aws-icons/`.

The WAF and the NAT are self-managed rather than the AWS managed services — an
application WAF (origin verification, shared rate limiting, header rules) in front of
the Lambdas, and a t3.micro NAT instance instead of a NAT Gateway. In policy text say
"self-managed WAF" and "NAT instance", never "AWS WAF" or "NAT Gateway".

Facts as of 2026-11-01 from `di-backend-api/docs/infra-edge-review-2026-11-01.md` and
`auth-hardening-2026-11-01.md`. Fargate tasks run in the public subnet and reach the
internet on their own public IP, not through the NAT; the diagram draws it that way.

A dense Mermaid version for quick edits: `di-backend-network.mmd`.
