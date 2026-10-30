import { withSentryConfig } from '@sentry/nextjs';
import path from 'path';
import './src/env.mjs';

const isStandalone = process.env.NEXT_OUTPUT_STANDALONE === 'true';

const config = {
  experimental: {
    serverActions: {
      // Behind CloudFront -> Lambda URL the forwarded host is the function URL;
      // list the public hostnames so server actions pass Next's origin check.
      allowedOrigins:
        process.env.NODE_ENV === 'production'
          ? Array.from(
              new Set(
                [
                  process.env.NEXT_PUBLIC_PORTAL_URL,
                  process.env.NEXT_PUBLIC_BETTER_AUTH_URL,
                  process.env.NEXT_PUBLIC_APP_URL,
                  ...(process.env.SERVER_ACTIONS_ALLOWED_ORIGINS ?? '').split(','),
                ]
                  .filter(Boolean)
                  .map((v) => (v as string).trim().replace(/^https?:\/\//, '').replace(/\/.*$/, '')),
              ),
            )
          : undefined,
    },
  },
  transpilePackages: [
    '@trycompai/auth',
    '@trycompai/db',
    '@trycompai/design-system',
    '@carbon/icons-react',
    '@trycompai/company',
  ],
  images: {
    // Disable the public optimizer endpoint (GH-083). Dynamic avatars, logos,
    // and signed uploads load directly in the browser without a server proxy.
    unoptimized: true,
  },
  async rewrites() {
    if (!process.env.NEXT_PUBLIC_POSTHOG_KEY) return [];
    return [
      {
        source: '/ingest/static/:path*',
        destination: 'https://us-assets.i.posthog.com/static/:path*',
      },
      {
        source: '/ingest/:path*',
        destination: 'https://us.i.posthog.com/:path*',
      },
      {
        source: '/ingest/decide',
        destination: 'https://us.i.posthog.com/decide',
      },
    ];
  },
  async headers() {
    return [
      {
        source: '/:path*',
        has: [
          {
            type: 'header',
            key: 'Next-Action',
          },
        ],
        headers: [
          {
            key: 'Cache-Control',
            value: 'no-cache, no-store, must-revalidate',
          },
          {
            key: 'Pragma',
            value: 'no-cache',
          },
          {
            key: 'Expires',
            value: '0',
          },
        ],
      },
    ];
  },
  skipTrailingSlashRedirect: true,
  outputFileTracingRoot: path.join(__dirname, '../../'),
  ...(isStandalone
    ? {
        output: 'standalone' as const,
      }
    : {}),
};

export default withSentryConfig(config, {
  org: process.env.SENTRY_ORG,
  project: process.env.SENTRY_PROJECT,

  // Only print logs for uploading source maps in CI
  silent: !process.env.CI,

  // Upload a larger set of source maps for prettier stack traces
  widenClientFileUpload: true,

  // Route browser requests to Sentry through a Next.js rewrite to circumvent ad-blockers.
  tunnelRoute: '/monitoring',

  webpack: {
    // Automatically tree-shake Sentry logger statements to reduce bundle size
    treeshake: {
      removeDebugLogging: true,
    },
  },
});
