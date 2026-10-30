/**
 * Vendor logo URLs via logo.dev. Only used when NEXT_PUBLIC_LOGO_DEV_TOKEN is
 * set; otherwise returns '' so self-hosted instances never call logo.dev.
 */
export const LOGO_DEV_TOKEN = process.env.NEXT_PUBLIC_LOGO_DEV_TOKEN ?? '';

export function logoDevUrl(domain: string | undefined | null, extraQuery = ''): string {
  if (!LOGO_DEV_TOKEN || !domain) return '';
  return `https://img.logo.dev/${domain}?token=${LOGO_DEV_TOKEN}${extraQuery}`;
}
