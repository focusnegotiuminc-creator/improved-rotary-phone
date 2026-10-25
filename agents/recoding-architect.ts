export const masterOsAgents = [
  "Master OS Command Router", "Universal Business Builder", "Recoding Architect", "Connector Engineer", "Deployment Commander", "Automation Operator", "Memory & Knowledge Librarian", "Quality Control Auditor", "Focus Negotium Inc Automation Agent", "Focus Records LLC Automation Agent", "Flux & Crave Automation Agent", "Real Estate / Container Development Agent", "Music Release Agent", "Investor Package Agent", "Grants/Funding Agent",
] as const;

export type WorkflowStage = "INPUT" | "CLASSIFY" | "ROUTE" | "PLAN" | "EXECUTE" | "TEST" | "QUALITY CHECK" | "DEPLOY CHECK" | "LOG" | "REPORT";
export const masterOsWorkflow: WorkflowStage[] = ["INPUT", "CLASSIFY", "ROUTE", "PLAN", "EXECUTE", "TEST", "QUALITY CHECK", "DEPLOY CHECK", "LOG", "REPORT"];

export function routeTask(input: string) {
  const lowered = input.toLowerCase();
  const agent = lowered.includes("deploy") ? "Deployment Commander" : lowered.includes("cloudflare") ? "Connector Engineer" : lowered.includes("audit") || lowered.includes("quality") ? "Quality Control Auditor" : "Master OS Command Router";
  return { agent, workflow: masterOsWorkflow, requiresConfirmation: /deploy|delete|destroy|publish|send|payment/i.test(input) };
}
