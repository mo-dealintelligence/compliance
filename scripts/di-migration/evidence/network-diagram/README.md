# Production network diagram

`di-backend-network.mmd` is the source (Mermaid), drawn from the read-only
inventory produced by `deploy/aws/inventory.sh` (account 164482277879,
us-east-1). Regenerate after infrastructure changes and submit it as the
`network-diagram` evidence form:

    mmdc -i di-backend-network.mmd -o di-backend-network-$(date +%F).png -w 2200 -b white
    bun ../native-records.ts --network-diagram network-diagram/di-backend-network-$(date +%F).png
