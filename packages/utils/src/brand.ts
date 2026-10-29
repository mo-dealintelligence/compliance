/**
 * Instance branding. Every value can be overridden through env so the same
 * build serves any operator; defaults are the Deal Intelligence fork.
 *
 * Client components read NEXT_PUBLIC_* at build time; server code reads the
 * same keys at runtime.
 */
function pick(...keys: string[]): string | undefined {
  for (const key of keys) {
    const value = process.env[key]?.trim();
    if (value) return value;
  }
  return undefined;
}

export const brand = {
  /** Short product/company name shown in titles, nav, and emails. */
  name: pick('NEXT_PUBLIC_BRAND_NAME', 'BRAND_NAME') ?? 'Deal Intelligence',
  /** Legal entity used in footers and NDA/PDF text. */
  legalName: pick('NEXT_PUBLIC_BRAND_LEGAL_NAME', 'BRAND_LEGAL_NAME') ?? 'Deal Intelligence LLC',
  /** Name of the compliance workspace itself (nav wordmark). */
  productName:
    pick('NEXT_PUBLIC_BRAND_PRODUCT_NAME', 'BRAND_PRODUCT_NAME') ?? 'Deal Intelligence Trust',
  websiteUrl: pick('NEXT_PUBLIC_WEBSITE_URL', 'WEBSITE_URL') ?? 'https://dealintelligence.io',
  supportEmail:
    pick('NEXT_PUBLIC_SUPPORT_EMAIL', 'SUPPORT_EMAIL') ?? 'security@dealintelligence.io',
  privacyEmail: pick('NEXT_PUBLIC_PRIVACY_EMAIL', 'PRIVACY_EMAIL') ?? 'privacy@dealintelligence.io',
  termsUrl: pick('NEXT_PUBLIC_TERMS_URL', 'TERMS_URL') ?? 'https://dealintelligence.io/terms',
  privacyUrl:
    pick('NEXT_PUBLIC_PRIVACY_URL', 'PRIVACY_URL') ?? 'https://dealintelligence.io/privacy',
  /** Absolute URL of a logo usable in emails and PDFs (must be publicly fetchable). */
  logoUrl:
    pick('NEXT_PUBLIC_BRAND_LOGO_URL', 'BRAND_LOGO_URL') ?? 'https://dealintelligence.io/logo.png',
  /** Postal address line for email footers (CAN-SPAM). */
  postalAddress:
    pick('NEXT_PUBLIC_BRAND_POSTAL_ADDRESS', 'BRAND_POSTAL_ADDRESS') ??
    'Deal Intelligence LLC, Long Beach, CA',
  appUrl:
    pick('NEXT_PUBLIC_APP_URL', 'NEXT_PUBLIC_BETTER_AUTH_URL', 'BETTER_AUTH_URL') ??
    'http://localhost:3000',
  portalUrl: pick('NEXT_PUBLIC_PORTAL_URL', 'PORTAL_URL') ?? 'http://localhost:3002',
  trustUrl: pick('NEXT_PUBLIC_TRUST_URL', 'TRUST_APP_URL') ?? 'http://localhost:3008',
} as const;

export type Brand = typeof brand;
