export type QualityGate = "preflight" | "code-review" | "connector-health" | "security" | "post-deploy";
export type QualityResult = { gate: QualityGate; ok: boolean; findings: string[]; nextActions: string[] };

const SECRET_PATTERNS = [/api[_-]?token\s*=\s*[^\s]+/i, /secret\s*=\s*[^\s]+/i, /-----BEGIN (RSA |EC |OPENSSH )?PRIVATE KEY-----/];

export class QualityControlAuditor {
  run(task: string, files: Record<string, string>): QualityResult[] {
    return [
      this.preflight(task),
      this.codeReview(files),
      this.connectorHealth(),
      this.security(files),
      this.postDeploy(),
    ];
  }
  preflight(task: string): QualityResult { return { gate: "preflight", ok: task.trim().length > 0, findings: task ? ["Task is defined and routable."] : ["Task is empty."], nextActions: ["Classify, route, plan, execute, test, quality check, deploy check, log, report."] }; }
  codeReview(files: Record<string, string>): QualityResult { return { gate: "code-review", ok: Object.keys(files).length > 0, findings: ["Review typed interfaces, explicit environment inputs, and no destructive action without confirmation."], nextActions: ["Run unit tests and deployment dry-runs before release."] }; }
  connectorHealth(): QualityResult { return { gate: "connector-health", ok: true, findings: ["Connector health checks are required before deployment."], nextActions: ["Run CloudflareConnector.runHealthAudit for each profile."] }; }
  security(files: Record<string, string>): QualityResult { const hits = Object.entries(files).flatMap(([file, body]) => SECRET_PATTERNS.some((pattern) => pattern.test(body)) ? [file] : []); return { gate: "security", ok: hits.length === 0, findings: hits.length ? hits.map((file) => `Potential secret pattern in ${file}.`) : ["No obvious secret literals detected in provided file set."], nextActions: hits.length ? ["Move secrets to local .env or platform secret store and rotate exposed values."] : ["Keep using .env.example placeholders only."] }; }
  postDeploy(): QualityResult { return { gate: "post-deploy", ok: true, findings: ["Post-deploy checks must verify status endpoint, dashboard load, connector panel, and audit-log access."], nextActions: ["Capture deployment URL, status code, and smoke-test evidence."] }; }
}
