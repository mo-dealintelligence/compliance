/**
 * Hand-curated records that are not in the Humadroid export as data:
 * vendors (from the policies' sub-processor list + tooling), people, and the
 * auditor-view context answers (from the System Description).
 */
export const VENDORS = [
  {
    name: 'Amazon Web Services',
    website: 'https://aws.amazon.com',
    description:
      'Cloud hosting and encrypted storage for the Deal Intelligence platform (us-east-1): Lambda, Fargate, DocumentDB, S3, CloudFront, VPC. Sub-processor.',
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
    description:
      'Authentication and identity management for the Deal Intelligence web app (JWT, MFA, RBAC). Sub-processor.',
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
    description:
      'Source control, CI/CD (GitHub Actions), Dependabot, secret scanning and branch protection for all Deal Intelligence code.',
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
    description:
      'Email, calendar and document storage for Deal Intelligence LLC; identity provider for Google SSO.',
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
    description:
      'Transactional email delivery for the compliance platform (notifications, sign-in links).',
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
      "Deal Intelligence LLC (Delaware) is a business-to-business revenue data company. It surfaces verified competitor activity for revenue teams: named buyers at a customer's target accounts who have accepted outreach from named competitors, plus verified competitor-customer lists derived from DNS, certificate and SSO/tenant evidence. The company is founder-operated (single member LLC) with one go-to-market contractor, fully remote, with all infrastructure on AWS us-east-1.",
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
    answer:
      'Give B2B revenue teams a verified, daily view of competitive activity at the accounts they care about, so they can win net-new deals, protect renewals and revive closed-lost opportunities with facts rather than inference.',
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
    answer:
      'Amazon Web Services (hosting and storage), PropelAuth (authentication), GitHub (source control and CI/CD), Google Workspace (email and SSO).',
    tags: ['vendors'],
  },
  {
    question: 'Subservice Organizations',
    answer:
      'Amazon Web Services and PropelAuth are the two sub-processors (subservice organizations) that process customer data on behalf of Deal Intelligence. Customer-controlled integrations (Slack, Salesforce, HubSpot, Clay) are not subservice organizations.',
    tags: ['vendors'],
  },
  {
    question: 'How many employees do you have?',
    answer:
      'One full-time founder/CEO (Mo Messidi) and one go-to-market contractor (William Wickey).',
    tags: ['people'],
  },
  {
    question: 'Who are your C-Suite executives?',
    answer:
      'Mo Messidi, Chief Executive Officer and founder; also acts as Information Security Officer and System Owner.',
    tags: ['people'],
  },
  {
    question: 'Who will sign off on the final report?',
    answer: 'Mo Messidi, CEO.',
    tags: ['people'],
  },
];

/**
 * Risk register (Humadroid "Q4 Risks" snapshot, 2026-02-04, 6 items, all
 * Medium / requires treatment). Items 1-4 are transcribed from the snapshot
 * screenshots; 5-6 were cut off in the capture and are reconstructed from the
 * category summary (Technology Risk, Cybersecurity Risk) and the key risk
 * areas named in the Information Security Policy — REVIEW before publishing.
 */
export const RISKS = [
  {
    title: 'COMPLIANCE-001 Inadequate Incident Response Capacity',
    description:
      'With a single operator, detection and response to a security incident may be delayed, affecting the 48-hour customer notification commitment and SOC 2 CC7.3–CC7.5. Treatment: automated Security Hub / Lambda breach detection, documented Incident Response Procedure, AWS Support escalation path.',
    category: 'regulatory',
    likelihood: 'possible',
    impact: 'moderate',
    residualLikelihood: 'unlikely',
    residualImpact: 'moderate',
    treatmentStrategy: 'mitigate',
    status: 'open',
  },
  {
    title: 'COMPLIANCE_REGULATORY-001 Compliance Documentation Gaps',
    description:
      'Policies, procedures and evidence may drift out of date between annual reviews, creating gaps against GDPR/CCPA and SOC 2 requirements. Treatment: annual policy review cycle, quarterly evidence refresh, compliance platform reminders.',
    category: 'regulatory',
    likelihood: 'possible',
    impact: 'moderate',
    residualLikelihood: 'unlikely',
    residualImpact: 'minor',
    treatmentStrategy: 'mitigate',
    status: 'open',
  },
  {
    title: 'EXTERNAL_VENDOR-001 PropelAuth Service Disruption',
    description:
      'An outage or security incident at PropelAuth (authentication sub-processor) would block customer sign-in to the platform. Treatment: vendor assessment, monitoring of vendor status, documented fallback and communication plan.',
    category: 'vendor_management',
    likelihood: 'possible',
    impact: 'major',
    residualLikelihood: 'unlikely',
    residualImpact: 'moderate',
    treatmentStrategy: 'mitigate',
    status: 'open',
  },
  {
    title: 'OPERATIONAL_PEOPLE-001 Single Point of Failure - Solo Operator Dependency',
    description:
      'As a solo operator managing all aspects of the AI-powered market intelligence platform, illness, unavailability, or departure creates immediate operational continuity risks affecting SOC 2 compliance maintenance and customer service delivery. Score 32.0 (probability 4, impact 3: legal 3, financial 2, reputational 3). Treatment action (planned, due Dec 31): document all critical processes, establish emergency access procedures with a trusted third party, and create a knowledge transfer repository.',
    category: 'people',
    likelihood: 'likely',
    impact: 'moderate',
    residualLikelihood: 'possible',
    residualImpact: 'minor',
    treatmentStrategy: 'mitigate',
    status: 'open',
  },
  {
    title: 'TECHNOLOGY-001 Service Availability Disruption (reconstructed — review)',
    description:
      'Failure of AWS components (Lambda, Fargate, DocumentDB) or a deployment error could interrupt daily data delivery against the 99.9% uptime commitment. Treatment: multi-AZ deployment, CloudWatch alarms, DocumentDB backups (90 days), Business Continuity Plan and tested recovery.',
    category: 'technology',
    likelihood: 'possible',
    impact: 'moderate',
    residualLikelihood: 'unlikely',
    residualImpact: 'minor',
    treatmentStrategy: 'mitigate',
    status: 'open',
  },
  {
    title: 'CYBERSECURITY-001 Data Breach / Unauthorized Access (reconstructed — review)',
    description:
      'Unauthorized access to business contact information or customer account data through compromised credentials, misconfiguration or vulnerability. Treatment: MFA, least-privilege IAM and RBAC, VPC isolation, KMS encryption at rest and TLS in transit, Security Hub and CloudTrail monitoring, quarterly automated access reviews, Dependabot/ECR scanning.',
    category: 'technology',
    likelihood: 'possible',
    impact: 'severe',
    residualLikelihood: 'unlikely',
    residualImpact: 'moderate',
    treatmentStrategy: 'mitigate',
    status: 'open',
  },
] as const;
