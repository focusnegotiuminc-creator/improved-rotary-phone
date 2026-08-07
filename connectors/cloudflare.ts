export type CloudflareEnv = Record<string, string | undefined>;
export type CheckState = 'pass' | 'fail' | 'missing' | 'unknown';
export interface CloudflareCheck { name: string; state: CheckState; message: string; data?: unknown }

const API = 'https://api.cloudflare.com/client/v4';
const envKeys = ['CLOUDFLARE_API_TOKEN','CLOUDFLARE_ACCOUNT_ID','CLOUDFLARE_ZONE_ID','CLOUDFLARE_EMAIL','CLOUDFLARE_PROJECT_NAME','CLOUDFLARE_KV_NAMESPACE_ID','CLOUDFLARE_D1_DATABASE_ID','CLOUDFLARE_R2_BUCKET'] as const;

export function validateCloudflareEnv(env: CloudflareEnv): CloudflareCheck[] {
  return envKeys.map((key) => ({ name: key, state: env[key] ? 'pass' : 'missing', message: env[key] ? 'configured from environment' : 'missing from runtime environment' }));
}

export class CloudflareConnector {
  constructor(private env: CloudflareEnv, private fetcher: typeof fetch = fetch) {}
  private headers() { return { Authorization: `Bearer ${this.env.CLOUDFLARE_API_TOKEN ?? ''}`, 'Content-Type': 'application/json' }; }
  private async request(path: string): Promise<CloudflareCheck> {
    if (!this.env.CLOUDFLARE_API_TOKEN) return { name: path, state: 'missing', message: 'CLOUDFLARE_API_TOKEN is required' };
    try {
      const res = await this.fetcher(`${API}${path}`, { headers: this.headers() });
      const data = await res.json().catch(() => ({}));
      return { name: path, state: res.ok ? 'pass' : 'fail', message: res.ok ? 'Cloudflare API check succeeded' : `Cloudflare API returned ${res.status}`, data };
    } catch (error) {
      return { name: path, state: 'fail', message: error instanceof Error ? error.message : 'Unknown Cloudflare connector error' };
    }
  }
  verifyToken() { return this.request('/user/tokens/verify'); }
  lookupAccount() { return this.env.CLOUDFLARE_ACCOUNT_ID ? this.request(`/accounts/${this.env.CLOUDFLARE_ACCOUNT_ID}`) : Promise.resolve({ name: 'account', state: 'missing' as const, message: 'CLOUDFLARE_ACCOUNT_ID is required' }); }
  lookupZone() { return this.env.CLOUDFLARE_ZONE_ID ? this.request(`/zones/${this.env.CLOUDFLARE_ZONE_ID}`) : Promise.resolve({ name: 'zone', state: 'missing' as const, message: 'CLOUDFLARE_ZONE_ID is required' }); }
  checkWorkersSubdomain() { return this.env.CLOUDFLARE_ACCOUNT_ID ? this.request(`/accounts/${this.env.CLOUDFLARE_ACCOUNT_ID}/workers/subdomain`) : Promise.resolve({ name: 'workers', state: 'missing' as const, message: 'CLOUDFLARE_ACCOUNT_ID is required' }); }
  checkPagesProject() { return this.env.CLOUDFLARE_ACCOUNT_ID && this.env.CLOUDFLARE_PROJECT_NAME ? this.request(`/accounts/${this.env.CLOUDFLARE_ACCOUNT_ID}/pages/projects/${this.env.CLOUDFLARE_PROJECT_NAME}`) : Promise.resolve({ name: 'pages', state: 'missing' as const, message: 'CLOUDFLARE_ACCOUNT_ID and CLOUDFLARE_PROJECT_NAME are required' }); }
  checkKvNamespace() { return this.env.CLOUDFLARE_ACCOUNT_ID && this.env.CLOUDFLARE_KV_NAMESPACE_ID ? this.request(`/accounts/${this.env.CLOUDFLARE_ACCOUNT_ID}/storage/kv/namespaces/${this.env.CLOUDFLARE_KV_NAMESPACE_ID}`) : Promise.resolve({ name: 'kv', state: 'missing' as const, message: 'CLOUDFLARE_ACCOUNT_ID and CLOUDFLARE_KV_NAMESPACE_ID are required' }); }
  checkD1Database() { return this.env.CLOUDFLARE_ACCOUNT_ID && this.env.CLOUDFLARE_D1_DATABASE_ID ? this.request(`/accounts/${this.env.CLOUDFLARE_ACCOUNT_ID}/d1/database/${this.env.CLOUDFLARE_D1_DATABASE_ID}`) : Promise.resolve({ name: 'd1', state: 'missing' as const, message: 'CLOUDFLARE_ACCOUNT_ID and CLOUDFLARE_D1_DATABASE_ID are required' }); }
  checkR2Bucket() { return this.env.CLOUDFLARE_ACCOUNT_ID && this.env.CLOUDFLARE_R2_BUCKET ? this.request(`/accounts/${this.env.CLOUDFLARE_ACCOUNT_ID}/r2/buckets/${this.env.CLOUDFLARE_R2_BUCKET}`) : Promise.resolve({ name: 'r2', state: 'missing' as const, message: 'CLOUDFLARE_ACCOUNT_ID and CLOUDFLARE_R2_BUCKET are required' }); }
  checkDeploymentStatus() { return this.checkPagesProject(); }
  fetchAuditLogs() { return this.env.CLOUDFLARE_ACCOUNT_ID ? this.request(`/accounts/${this.env.CLOUDFLARE_ACCOUNT_ID}/audit_logs`) : Promise.resolve({ name: 'audit', state: 'missing' as const, message: 'CLOUDFLARE_ACCOUNT_ID and audit-log API permissions are required' }); }
  async healthCheck() { return Promise.all([this.verifyToken(), this.lookupAccount(), this.lookupZone(), this.checkWorkersSubdomain(), this.checkPagesProject(), this.checkKvNamespace(), this.checkD1Database(), this.checkR2Bucket(), this.checkDeploymentStatus(), this.fetchAuditLogs()]); }
}
