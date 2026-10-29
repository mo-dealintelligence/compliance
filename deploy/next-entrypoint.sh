#!/bin/sh
# Next.js standalone server entrypoint for Lambda / containers.
# /tmp is the only writable path on Lambda; .next/cache is symlinked there.
set -e
mkdir -p /tmp/next-cache
exec node "${NEXT_APP_DIR:-apps/app}/server.js"
