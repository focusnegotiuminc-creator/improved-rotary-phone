export const masterOsAgents = [
  'Master OS Command Router','Universal Business Builder','Recoding Architect','Connector Engineer','Deployment Commander','Automation Operator','Memory & Knowledge Librarian','Quality Control Auditor','Focus Negotium Inc Automation Agent','Focus Records LLC Automation Agent','Flux & Crave Automation Agent','Real Estate / Container Development Agent','Music Release Agent','Investor Package Agent','Grants/Funding Agent',
] as const;

export function routeMasterOsTask(input: string) {
  const lower = input.toLowerCase();
  const assigned = masterOsAgents.filter((agent) => lower.includes(agent.toLowerCase().split(' ')[0]) || agent === 'Quality Control Auditor');
  return { workflow: 'INPUT → CLASSIFY → ROUTE → PLAN → EXECUTE → TEST → QUALITY CHECK → DEPLOY CHECK → LOG → REPORT', assignedAgents: assigned.length ? assigned : ['Master OS Command Router','Quality Control Auditor'], requiresConfirmation: /deploy|delete|destroy|purge|production/i.test(input) };
}
