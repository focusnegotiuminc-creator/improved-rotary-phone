declare const process: { env: Record<string, string | undefined> };
type Env = Record<string, string | undefined>;

export type CloudflareCheck = {
  name: string;
  ok: boolean;
  status: "pass" | "fail" | "missing" | "unsupported";
  message: string;
  data?: unknown;
};

export type CloudflareAudit = {
  generatedAt: string;
  profile: string;
  checks: CloudflareCheck[];
  missingData: string[];
};

const API = "https://api.cloudflare.com/client/v4";

export class CloudflareConnector {
  constructor(private readonly env: Env = process.env, private readonly fetcher: typeof fetch = fetch) {}

  private headers(): Record<string, string> {
    const token = this.env.CLOUDFLARE_API_TOKEN;
    return token ? { Authorization: `Bearer ${token}`, "Content-Type": "application/json" } : { "Content-Type": "application/json" };
  }

  private async get(path: string): Promise<CloudflareCheck> {
    if (!this.env.CLOUDFLARE_API_TOKEN) return { name: path, ok: false, status: "missing", message: "CLOUDFLARE_API_TOKEN is not set." };
    try {
      const res = await this.fetcher(`${API}${path}`, { headers: this.headers() });
      const data = await res.json().catch(() => undefined);
      return { name: path, ok: res.ok, status: res.ok ? "pass" : "fail", message: res.ok ? "Cloudflare API check passed." : `Cloudflare API returned ${res.status}.`, data };
    } catch (error) {
      return { name: path, ok: false, status: "fail", message: error instanceof Error ? error.message : String(error) };
    }
  }

  verifyToken() { return this.get("/user/tokens/verify"); }
  lookupAccount(accountId = this.env.CLOUDFLARE_ACCOUNT_ID) { return accountId ? this.get(`/accounts/${accountId}`) : Promise.resolve(missing("account", "CLOUDFLARE_ACCOUNT_ID")); }
  lookupZone(zoneId = this.env.CLOUDFLARE_ZONE_ID) { return zoneId ? this.get(`/zones/${zoneId}`) : Promise.resolve(missing("zone", "CLOUDFLARE_ZONE_ID")); }
  checkWorkersSubdomain(accountId = this.env.CLOUDFLARE_ACCOUNT_ID) { return accountId ? this.get(`/accounts/${accountId}/workers/subdomain`) : Promise.resolve(missing("workers-subdomain", "CLOUDFLARE_ACCOUNT_ID")); }
  checkPagesProject(accountId = this.env.CLOUDFLARE_ACCOUNT_ID, project = this.env.CLOUDFLARE_PROJECT_NAME) { return accountId && project ? this.get(`/accounts/${accountId}/pages/projects/${project}`) : Promise.resolve(missing("pages-project", "CLOUDFLARE_ACCOUNT_ID and CLOUDFLARE_PROJECT_NAME")); }
  checkKvNamespace(accountId = this.env.CLOUDFLARE_ACCOUNT_ID, namespace = this.env.CLOUDFLARE_KV_NAMESPACE_ID) { return accountId && namespace ? this.get(`/accounts/${accountId}/storage/kv/namespaces/${namespace}`) : Promise.resolve(missing("kv-namespace", "CLOUDFLARE_ACCOUNT_ID and CLOUDFLARE_KV_NAMESPACE_ID")); }
  checkD1Database(accountId = this.env.CLOUDFLARE_ACCOUNT_ID, database = this.env.CLOUDFLARE_D1_DATABASE_ID) { return accountId && database ? this.get(`/accounts/${accountId}/d1/database/${database}`) : Promise.resolve(missing("d1-database", "CLOUDFLARE_ACCOUNT_ID and CLOUDFLARE_D1_DATABASE_ID")); }
  checkR2Bucket(accountId = this.env.CLOUDFLARE_ACCOUNT_ID, bucket = this.env.CLOUDFLARE_R2_BUCKET) { return accountId && bucket ? this.get(`/accounts/${accountId}/r2/buckets/${bucket}`) : Promise.resolve(missing("r2-bucket", "CLOUDFLARE_ACCOUNT_ID and CLOUDFLARE_R2_BUCKET")); }
  checkDeploymentStatus(accountId = this.env.CLOUDFLARE_ACCOUNT_ID, project = this.env.CLOUDFLARE_PROJECT_NAME) { return accountId && project ? this.get(`/accounts/${accountId}/pages/projects/${project}/deployments`) : Promise.resolve(missing("deployment-status", "CLOUDFLARE_ACCOUNT_ID and CLOUDFLARE_PROJECT_NAME")); }
  fetchAuditLogs(accountId = this.env.CLOUDFLARE_ACCOUNT_ID) { return accountId ? this.get(`/accounts/${accountId}/audit_logs`) : Promise.resolve(missing("audit-logs", "CLOUDFLARE_ACCOUNT_ID")); }

  async runHealthAudit(profile = "default"): Promise<CloudflareAudit> {
    const checks = await Promise.all([this.verifyToken(), this.lookupAccount(), this.lookupZone(), this.checkWorkersSubdomain(), this.checkPagesProject(), this.checkKvNamespace(), this.checkD1Database(), this.checkR2Bucket(), this.checkDeploymentStatus(), this.fetchAuditLogs()]);
    return { generatedAt: new Date().toISOString(), profile, checks, missingData: checks.filter((c) => c.status === "missing" || c.name.includes("audit_logs") && !c.ok).map((c) => `${c.name}: ${c.message}`) };
  }
}

function missing(name: string, envName: string): CloudflareCheck { return { name, ok: false, status: "missing", message: `${envName} is required for this check.` }; }
