import { brand } from '@trycompai/utils/brand';
import { logoDevUrl } from '@/lib/logo-dev';

const brandHost = new URL(brand.websiteUrl).hostname;

export interface AutomationExample {
  title: string;
  prompt: string;
  url: string;
}

export const AUTOMATION_EXAMPLES: AutomationExample[] = [
  {
    title: 'Check if I have dependabot enabled in my GitHub repository',
    prompt: 'Check if I have dependabot enabled in my GitHub repository',
    url: logoDevUrl('github.com'),
  },
  {
    title: 'Check if I have branch protection enabled for the main branch in my GitHub repository',
    prompt: 'Check if I have branch protection enabled for the main branch in my GitHub repository',
    url: logoDevUrl('github.com'),
  },
  {
    title: 'Check if my website has a privacy policy',
    prompt: 'Check if my website has a privacy policy',
    url: logoDevUrl(brandHost),
  },
  {
    title: 'Give me a list of failed deployments in my Vercel project',
    prompt: 'Give me a list of failed deployments in my Vercel project',
    url: logoDevUrl('vercel.com'),
  },
  {
    title: 'Check that DDoS protection is enabled for my Cloudflare project',
    prompt: 'Check that DDoS protection is enabled for my Cloudflare project',
    url: logoDevUrl('cloudflare.com'),
  },
];
