import { CloudflareConnector, validateCloudflareEnv, type CloudflareEnv } from './cloudflare';

export type ConnectorName = 'cloudflare' | 'github' | 'googleDrive' | 'vercel' | 'gmail' | 'calendar';
export interface ConnectorStatus { name: ConnectorName; configured: boolean; health: 'ready' | 'missing-config' | 'unknown'; message: string }

export function buildConnectorRegistry(env: CloudflareEnv): ConnectorStatus[] {
  return [
    { name: 'cloudflare', configured: validateCloudflareEnv(env).some((c) => c.state === 'pass'), health: env.CLOUDFLARE_API_TOKEN ? 'ready' : 'missing-config', message: 'Cloudflare Workers/Pages primary deployment connector' },
    { name: 'github', configured: Boolean(env.GITHUB_TOKEN), health: env.GITHUB_TOKEN ? 'ready' : 'missing-config', message: 'GitHub source and review connector' },
    { name: 'googleDrive', configured: Boolean(env.GOOGLE_DRIVE_CLIENT_ID), health: env.GOOGLE_DRIVE_CLIENT_ID ? 'ready' : 'missing-config', message: 'Google Drive import connector' },
    { name: 'vercel', configured: Boolean(env.VERCEL_TOKEN), health: env.VERCEL_TOKEN ? 'ready' : 'missing-config', message: 'Vercel fallback deployment connector' },
    { name: 'gmail', configured: Boolean(env.GMAIL_CLIENT_ID), health: env.GMAIL_CLIENT_ID ? 'ready' : 'missing-config', message: 'Gmail automation connector' },
    { name: 'calendar', configured: Boolean(env.GOOGLE_CALENDAR_CLIENT_ID), health: env.GOOGLE_CALENDAR_CLIENT_ID ? 'ready' : 'missing-config', message: 'Calendar scheduling connector' },
  ];
}

export function createCloudflareConnector(env: CloudflareEnv) { return new CloudflareConnector(env); }
