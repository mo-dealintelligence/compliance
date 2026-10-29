/**
 * Hand-curated records that are not in the Humadroid export as data:
 * vendors (from the policies' sub-processor list + tooling), people, and the
 * auditor-view context answers (from the System Description).
 */
export const VENDORS = [
  {
    name: 'Amazon Web Services',
    website: 'https://aws.amazon.com',
    description: 'Cloud hosting and encrypted storage for the Deal Intelligence platform (us-east-1): Lambda, Fargate, DocumentDB, S3, CloudFront, VPC. Sub-processor.',
    category: 'cloud',
    status: 'assessed',
    isSubProcessor: true,
    inherentProbability: 'possible',
    inherentImpact: 'severe',
    residualProbability: 'unlikely',
    residualImpact: 'moderate',
  },
  {
    name: 'PropelAuth',
    website: 'https://www.propelauth.com',
    description: 'Authentication and identity management for the Deal Intelligence web app (JWT, MFA, RBAC). Sub-processor.',
    category: 'software_as_a_service',
    status: 'assessed',
    isSubProcessor: true,
    inherentProbability: 'possible',
    inherentImpact: 'major',
    residualProbability: 'unlikely',
    residualImpact: 'minor',
  },
  {
    name: 'GitHub',
    website: 'https://github.com',
    description: 'Source control, CI/CD (GitHub Actions), Dependabot, secret scanning and branch protection for all Deal Intelligence code.',
    category: 'software_as_a_service',
    status: 'assessed',
    isSubProcessor: false,
    inherentProbability: 'possible',
    inherentImpact: 'major',
    residualProbability: 'unlikely',
    residualImpact: 'minor',
  },
  {
    name: 'Google Workspace',
    website: 'https://workspace.google.com',
    description: 'Email, calendar and document storage for Deal Intelligence LLC; identity provider for Google SSO.',
    category: 'software_as_a_service',
    status: 'assessed',
    isSubProcessor: false,
    inherentProbability: 'unlikely',
    inherentImpact: 'moderate',
    residualProbability: 'unlikely',
    residualImpact: 'minor',
  },
  {
    name: 'Resend',
    website: 'https://resend.com',
    description: 'Transactional email delivery for the compliance platform (notifications, sign-in links).',
    category: 'software_as_a_service',
    status: 'not_assessed',
    isSubProcessor: false,
    inherentProbability: 'unlikely',
    inherentImpact: 'minor',
  },
] as const;

export const PEOPLE = [
  { email: 'william@dealintelligence.io', roles: ['contractor'] }, // William Wickey, GTM contractor (1099) — confirm email before running
];

export const CONTEXT = [
  {
    question: 'Company Background & Overview of Operations',
    answer:
      'Deal Intelligence LLC (Delaware) is a business-to-business revenue data company. It surfaces verified competitor activity for revenue teams: named buyers at a customer\'s target accounts who have accepted outreach from named competitors, plus verified competitor-customer lists derived from DNS, certificate and SSO/tenant evidence. The company is founder-operated (single member LLC) with one go-to-market contractor, fully remote, with all infrastructure on AWS us-east-1.',
    tags: ['overview'],
  },
  {
    question: 'Types of Services Provided',
    answer:
      'Verified competitor activity events and competitor customer lists delivered through a REST API, an MCP server for Claude and other AI clients, Clay enrichment, Salesforce/HubSpot CRM writes, Slack notifications and webhooks. Events refresh daily, are named on both sides and carry a confidence score of 0.95 or higher.',
    tags: ['services'],
  },
  {
    question: 'Mission & Vision',
    answer: 'Give B2B revenue teams a verified, daily view of competitive activity at the accounts they care about, so they can win net-new deals, protect renewals and revive closed-lost opportunities with facts rather than inference.',
    tags: ['mission'],
  },
  {
    question: 'System Description',
    answer:
      'The in-scope system is the Deal Intelligence platform: AWS Lambda functions and Fargate containers (serverless, short-lived compute), Amazon DocumentDB with KMS encryption, S3, CloudFront, EventBridge schedules and private VPC subnets with no direct internet access, provisioned through CloudFormation (stack di-backend-api-prod) and deployed by GitHub Actions. Authentication is PropelAuth (JWT, MFA, RBAC) with company- and user-level data isolation. Monitoring uses CloudWatch (90-day retention), CloudTrail, Security Hub and multi-AZ deployment. The platform processes business contact information and competitor interaction data with a 24-month retention period for active leads. The compliance program itself is managed in a self-hosted GRC tool (Comp) outside the system boundary.',
    tags: ['system-description'],
  },
  {
    question: 'Critical Vendors',
    answer: 'Amazon Web Services (hosting and storage), PropelAuth (authentication), GitHub (source control and CI/CD), Google Workspace (email and SSO).',
    tags: ['vendors'],
  },
  {
    question: 'Subservice Organizations',
    answer: 'Amazon Web Services and PropelAuth are the two sub-processors (subservice organizations) that process customer data on behalf of Deal Intelligence. Customer-controlled integrations (Slack, Salesforce, HubSpot, Clay) are not subservice organizations.',
    tags: ['vendors'],
  },
  { question: 'How many employees do you have?', answer: 'One full-time founder/CEO (Mo Messidi) and one go-to-market contractor (William Wickey).', tags: ['people'] },
  { question: 'Who are your C-Suite executives?', answer: 'Mo Messidi, Chief Executive Officer and founder; also acts as Information Security Officer and System Owner.', tags: ['people'] },
  { question: 'Who will sign off on the final report?', answer: 'Mo Messidi, CEO.', tags: ['people'] },
];
