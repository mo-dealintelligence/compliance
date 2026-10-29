/**
 * URL helpers. Every value is overridable through env so a self-hosted
 * instance never falls back to the upstream vendor's domains.
 */
function fromEnv(...keys: string[]): string | undefined {
  for (const key of keys) {
    const value = process.env[key]?.trim();
    if (value) return value.replace(/\/$/, '');
  }
  return undefined;
}

export function getAppUrl() {
  const configured = fromEnv('NEXT_PUBLIC_APP_URL', 'NEXT_PUBLIC_BETTER_AUTH_URL', 'BETTER_AUTH_URL');
  if (configured) return configured;

  if (process.env.VERCEL_ENV === 'preview' && process.env.VERCEL_URL) {
    return `https://${process.env.VERCEL_URL}`;
  }

  return 'http://localhost:3000';
}

export function getEmailUrl() {
  return fromEnv('NEXT_PUBLIC_WEBSITE_URL', 'WEBSITE_URL') ?? getAppUrl();
}

export function getWebsiteUrl() {
  return fromEnv('NEXT_PUBLIC_WEBSITE_URL', 'WEBSITE_URL') ?? getAppUrl();
}

export function getCdnUrl() {
  return fromEnv('NEXT_PUBLIC_CDN_URL', 'CDN_URL') ?? `${getAppUrl()}/static`;
}
