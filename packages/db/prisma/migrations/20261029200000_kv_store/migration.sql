-- Generic key-value store with TTL (replaces Upstash Redis on self-hosted installs)
CREATE TABLE "kv_store" (
    "key" TEXT NOT NULL,
    "value" JSONB NOT NULL,
    "expires_at" TIMESTAMP(3),
    "updated_at" TIMESTAMP(3) NOT NULL,
    CONSTRAINT "kv_store_pkey" PRIMARY KEY ("key")
);
CREATE INDEX "kv_store_expires_at_idx" ON "kv_store"("expires_at");
