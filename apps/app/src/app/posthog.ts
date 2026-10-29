import type { Properties } from 'posthog-js';
import type { PostHog } from 'posthog-node';

let posthogInstance: PostHog | null = null;

async function getPostHogClient(): Promise<PostHog | null> {
  if (posthogInstance) {
    return posthogInstance;
  }

  const apiKey = process.env.NEXT_PUBLIC_POSTHOG_KEY;
  const apiHost = process.env.NEXT_PUBLIC_POSTHOG_HOST;

  if (apiKey && apiHost) {
    const { PostHog } = await import('posthog-node');
    posthogInstance = new PostHog(apiKey, {
      flushAt: 1,
      flushInterval: 0,
    });
    return posthogInstance;
  }

  return null;
}

export { getPostHogClient };

export async function track(distinctId: string, eventName: string, properties?: Properties) {
  const client = await getPostHogClient();
  if (!client) return;

  client.capture({
    distinctId,
    event: eventName,
    properties,
  });
}

export async function identify(distinctId: string, properties?: Properties) {
  const client = await getPostHogClient();
  if (!client) return;

  client.identify({
    distinctId,
    properties,
  });
}

/**
 * Flags that upstream gates behind PostHog. A self-hosted instance has no
 * PostHog, so every flag would read `false` and hide shipped features
 * (trust portal nav, questionnaire pages 404, ISMS tab, timeline, ...).
 * When SELF_HOSTED / NEXT_PUBLIC_SELF_HOSTED is "true" we enable them all,
 * minus anything explicitly disabled via SELF_HOSTED_DISABLED_FLAGS.
 */
const SELF_HOSTED_DEFAULT_FLAGS: Record<string, boolean> = {
  'ai-vendor-questionnaire': true,
  'is-trust-nda-enabled': false, // DI keeps its existing trust center (trust.dealintelligence.io)
  'is-web-automations-enabled': false, // needs Browserbase + enterprise API
  'is-timeline-enabled': true,
  'is-isms-enabled': true,
  'is-ai-policy-assistant-enabled': true,
};

export function isSelfHosted(): boolean {
  return (
    process.env.SELF_HOSTED === 'true' ||
    process.env.NEXT_PUBLIC_SELF_HOSTED === 'true'
  );
}

export function getSelfHostedFeatureFlags(): Record<string, boolean> {
  const disabled = new Set(
    (process.env.SELF_HOSTED_DISABLED_FLAGS ?? '')
      .split(',')
      .map((s) => s.trim())
      .filter(Boolean),
  );
  const enabled = new Set(
    (process.env.SELF_HOSTED_ENABLED_FLAGS ?? '')
      .split(',')
      .map((s) => s.trim())
      .filter(Boolean),
  );
  const flags: Record<string, boolean> = {};
  for (const [key, value] of Object.entries(SELF_HOSTED_DEFAULT_FLAGS)) {
    flags[key] = enabled.has(key) ? true : disabled.has(key) ? false : value;
  }
  for (const key of enabled) flags[key] = true;
  return flags;
}

export async function getFeatureFlags(
  distinctId: string,
  options?: { groups?: Record<string, string> },
) {
  if (isSelfHosted()) return getSelfHostedFeatureFlags();

  const client = await getPostHogClient();
  if (!client) return {};

  const flags = await client.getAllFlags(distinctId, {
    groups: options?.groups,
  });
  return flags;
}
