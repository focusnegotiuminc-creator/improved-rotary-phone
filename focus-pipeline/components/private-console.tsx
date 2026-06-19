"use client";

import { useState, useEffect, useCallback } from "react";
import { cn } from "@/lib/cn";
import { ShieldCheck, Copy, Download, RotateCcw } from "lucide-react";

const BUSINESS_PROFILES = {
  "focus-negotium": {
    name: "Focus Negotium Inc",
    role: "Parent company",
    lanes: [
      "Holdings, entity support, governance coordination, and executive operating design",
      "Real estate development, property operations, and portfolio planning",
      "Websites, Stripe storefronts, client portals, and commercial infrastructure",
    ],
  },
  "focus-records": {
    name: "Focus Records LLC",
    role: "Affiliate media company",
    lanes: [
      "Release planning, rollout calendars, and catalog packaging",
      "Cover art direction, Firefly-ready campaign boards, and promo systems",
      "Beat-store planning, licensing pages, and media-commerce positioning",
    ],
  },
  "royal-lee-construction": {
    name: "Royal Lee Construction Solutions LLC",
    role: "Affiliate construction company",
    lanes: [
      "Sacred-geometry concept studies and presentation-grade owner packets",
      "Development planning, site logic, and preconstruction scope framing",
      "Renovation strategy, owner representation, and build coordination prep",
    ],
  },
} as const;

const WORKFLOW_PROFILES = {
  "Website Design and Deployment": {
    outcome: "ship a polished customer-facing website update with verified routing and mobile behavior",
    steps: [
      "Audit the current page structure, pricing, and routing.",
      "Write or revise the public copy and sector-specific service details.",
      "Build, verify, and deploy the updated site with rollback awareness.",
    ],
  },
  "Storefront and Stripe Offers": {
    outcome: "align pricing, offer copy, Stripe links, and the storefront hierarchy",
    steps: [
      "Verify the product ladder and the service ladder are saying the same thing.",
      "Update checkout links, CTA copy, and offer packaging.",
      "Validate customer-facing pages, prices, and payment routing.",
    ],
  },
  "Real Estate Development Packet": {
    outcome: "assemble a decision-ready property or development packet",
    steps: [
      "Clarify site context, ownership goals, and decision horizon.",
      "Package concept studies, notes, assumptions, and next-stage deliverables.",
      "Prepare an owner-facing summary that can move into review or execution.",
    ],
  },
  "Property Management Setup": {
    outcome: "stand up a usable management workflow with clear routing and reporting",
    steps: [
      "Map communications, maintenance flow, records, and owner updates.",
      "Design the intake, vendor, and document structure.",
      "Prepare rollout notes and a handoff sequence for day-one use.",
    ],
  },
  "Release Campaign and Media Packaging": {
    outcome: "ship a cohesive media package with launch direction and branded assets",
    steps: [
      "Define the release story, audience, and visual direction.",
      "Package campaign assets, rollout notes, and storefront language.",
      "Prepare the catalog or licensing pathway for launch.",
    ],
  },
  "Client Intake and Service Routing": {
    outcome: "normalize a client request into a clean service path and execution brief",
    steps: [
      "Clarify the lead, budget, need, and best-fit company lane.",
      "Translate the conversation into a service recommendation and scoped next step.",
      "Prepare the booking, follow-up, and delivery handoff.",
    ],
  },
} as const;

const INTEGRATIONS = {
  github: "Branch work, releases, deployments, and implementation tracking.",
  stripe: "Secure checkout links, pricing ladders, and product or service payment routing.",
  adobe: "Creative direction, PDF packets, visual studies, and production-ready branded assets.",
  figma: "Layout planning, interface references, and design-system translation.",
  airtable: "Structured operating data, client records, and service inventory.",
  media: "Campaign resizing, video prep, and future beat-catalog packaging.",
} as const;

type BusinessKey = keyof typeof BUSINESS_PROFILES;
type WorkflowKey = keyof typeof WORKFLOW_PROFILES;
type IntegrationKey = keyof typeof INTEGRATIONS;

const STORAGE_KEY = "focus-private-console-state";
const DEFAULT_OUTPUT = "Generate the private runbook to populate this panel.";

function lines(value: string, fallback: string[]): string[] {
  const parsed = value.split("\n").map((l) => l.trim()).filter(Boolean);
  return parsed.length ? parsed : fallback;
}

interface SummaryItem { label: string; value: string }

function SummaryCard({ label, value }: SummaryItem) {
  return (
    <div className="rounded-[var(--radius-sm)] border border-[var(--border)] bg-[var(--background)] p-3">
      <p className="text-[10px] font-medium uppercase tracking-wider text-[var(--muted)]">{label}</p>
      <p className="mt-0.5 text-sm font-medium text-foreground">{value}</p>
    </div>
  );
}

export function PrivateConsole() {
  const [business, setBusiness] = useState<BusinessKey>("focus-negotium");
  const [enabledIntegrations, setEnabledIntegrations] = useState<Set<IntegrationKey>>(
    new Set(["github", "stripe", "adobe"])
  );
  const [workflow, setWorkflow] = useState<WorkflowKey>("Website Design and Deployment");
  const [mission, setMission] = useState("");
  const [deliverables, setDeliverables] = useState("");
  const [constraints, setConstraints] = useState("");
  const [context, setContext] = useState("");
  const [output, setOutput] = useState(DEFAULT_OUTPUT);
  const [summaryItems, setSummaryItems] = useState<SummaryItem[]>([]);
  const [copied, setCopied] = useState(false);

  // Restore state from localStorage
  useEffect(() => {
    try {
      const raw = localStorage.getItem(STORAGE_KEY);
      if (!raw) return;
      const s = JSON.parse(raw);
      if (s.business && s.business in BUSINESS_PROFILES) setBusiness(s.business);
      if (Array.isArray(s.integrations)) setEnabledIntegrations(new Set(s.integrations));
      if (s.workflow && s.workflow in WORKFLOW_PROFILES) setWorkflow(s.workflow);
      if (typeof s.mission === "string") setMission(s.mission);
      if (typeof s.deliverables === "string") setDeliverables(s.deliverables);
      if (typeof s.constraints === "string") setConstraints(s.constraints);
      if (typeof s.context === "string") setContext(s.context);
    } catch {
      localStorage.removeItem(STORAGE_KEY);
    }
  }, []);

  const saveState = useCallback(() => {
    localStorage.setItem(
      STORAGE_KEY,
      JSON.stringify({
        business,
        integrations: [...enabledIntegrations],
        workflow,
        mission,
        deliverables,
        constraints,
        context,
      })
    );
  }, [business, enabledIntegrations, workflow, mission, deliverables, constraints, context]);

  const buildRunbook = useCallback(() => {
    const biz = BUSINESS_PROFILES[business];
    const wf = WORKFLOW_PROFILES[workflow];
    const delivs = lines(deliverables, ["Define the first deliverable before execution starts."]);
    const cons = lines(constraints, ["Protect live quality, keep the workflow reviewable, and preserve rollback safety."]);
    const ctx = lines(context, ["Attach source files, live URLs, or notes before execution."]);
    const intgs = enabledIntegrations.size ? [...enabledIntegrations] : (["github"] as IntegrationKey[]);
    const timestamp = new Date().toLocaleString();

    setSummaryItems([
      { label: "Business lane", value: biz.name },
      { label: "Workflow", value: workflow },
      { label: "Integrations", value: `${intgs.length} enabled` },
      { label: "Deliverables", value: `${delivs.filter((d) => d !== delivs[0] || deliverables.trim()).length} listed` },
      { label: "Constraints", value: `${cons.filter((c) => c !== cons[0] || constraints.trim()).length} tracked` },
      { label: "Execution posture", value: "Private / operator reviewed" },
    ]);

    const runbookLines = [
      "# FOCUS PRIVATE OPERATIONS CONSOLE :: RUNBOOK",
      "",
      `Generated: ${timestamp}`,
      "",
      "## Mission",
      mission || "Define the mission for this private run before execution begins.",
      "",
      "## Business Lane",
      `- ${biz.name} (${biz.role})`,
      ...biz.lanes.map((l) => `- ${l}`),
      "",
      "## Workflow Type",
      `- ${workflow}`,
      `- Target outcome: ${wf.outcome}`,
      "",
      "## Deliverables",
      ...delivs.map((d) => `- ${d}`),
      "",
      "## Constraints",
      ...cons.map((c) => `- ${c}`),
      "",
      "## Source Context",
      ...ctx.map((c) => `- ${c}`),
      "",
      "## Integration Lanes",
      ...intgs.map((k) => `- ${k}: ${INTEGRATIONS[k as IntegrationKey]}`),
      "",
      "## Execution Sequence",
      ...wf.steps.map((s, i) => `${i + 1}. ${s}`),
      "",
      "## Operator Checks",
      "- Confirm the selected business lane matches the public-facing company or the internal project owner.",
      "- Confirm any public site work remains customer-facing and does not expose internal systems.",
      "- Confirm pricing, routing, and storefront links before publish or deploy.",
      "- Capture the final output, live checks, and next actions before closing the run.",
      "",
      "## Handoff Note",
      "Use this runbook as the input packet for the next private execution tool, code workspace, or operator session.",
    ];

    setOutput(runbookLines.join("\n"));
    saveState();
  }, [business, workflow, mission, deliverables, constraints, context, enabledIntegrations, saveState]);

  // Auto-rebuild when inputs change
  useEffect(() => {
    if (mission || deliverables || constraints || context) buildRunbook();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [business, workflow, enabledIntegrations]);

  const toggleIntegration = (key: IntegrationKey) => {
    setEnabledIntegrations((prev) => {
      const next = new Set(prev);
      next.has(key) ? next.delete(key) : next.add(key);
      return next;
    });
  };

  const reset = () => {
    localStorage.removeItem(STORAGE_KEY);
    setBusiness("focus-negotium");
    setEnabledIntegrations(new Set(["github", "stripe", "adobe"]));
    setWorkflow("Website Design and Deployment");
    setMission("");
    setDeliverables("");
    setConstraints("");
    setContext("");
    setOutput(DEFAULT_OUTPUT);
    setSummaryItems([]);
  };

  const copyRunbook = async () => {
    await navigator.clipboard.writeText(output);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const downloadRunbook = () => {
    const blob = new Blob([output], { type: "text/markdown" });
    const link = document.createElement("a");
    link.href = URL.createObjectURL(blob);
    link.download = "focus-private-runbook.md";
    link.click();
    URL.revokeObjectURL(link.href);
  };

  return (
    <div className="flex flex-col gap-6">
      {/* Header */}
      <div className="flex flex-col gap-1">
        <div className="flex items-center gap-2">
          <ShieldCheck className="h-4 w-4 text-[var(--gold)]" />
          <p className="text-xs font-medium uppercase tracking-widest text-[var(--muted)]">
            Private Operations Console
          </p>
        </div>
        <h1 className="font-serif text-3xl font-semibold tracking-tight text-balance">
          Internal Runbook Builder
        </h1>
        <p className="text-sm text-[var(--muted)] max-w-xl leading-relaxed">
          Frame internal missions, select the business lane and integrations, then generate a
          private execution runbook ready to hand off to any execution tool or operator session.
        </p>
      </div>

      {/* Business lane selector */}
      <section className="rounded-[var(--radius)] border border-[var(--border)] bg-[var(--surface)] p-5">
        <div className="mb-3">
          <p className="text-xs font-medium uppercase tracking-widest text-[var(--muted)]">
            Business Routing
          </p>
          <h2 className="font-medium text-foreground">Choose the Company Lane</h2>
        </div>
        <div className="grid grid-cols-1 gap-2 sm:grid-cols-3">
          {(Object.entries(BUSINESS_PROFILES) as [BusinessKey, typeof BUSINESS_PROFILES[BusinessKey]][]).map(
            ([key, biz]) => (
              <button
                key={key}
                onClick={() => setBusiness(key)}
                className={cn(
                  "rounded-[var(--radius-sm)] border p-4 text-left transition-all cursor-pointer",
                  business === key
                    ? "border-[var(--border-gold)] bg-[var(--gold-dim)]"
                    : "border-[var(--border)] bg-[var(--background)] hover:bg-[var(--surface-elevated)]"
                )}
              >
                <p className="text-[10px] font-medium uppercase tracking-widest text-[var(--muted)] mb-1">
                  {biz.role}
                </p>
                <h3
                  className={cn(
                    "font-medium text-sm mb-1",
                    business === key ? "text-[var(--gold)]" : "text-foreground"
                  )}
                >
                  {biz.name}
                </h3>
                <ul className="flex flex-col gap-0.5">
                  {biz.lanes.map((lane) => (
                    <li key={lane} className="text-xs text-[var(--muted)] leading-relaxed line-clamp-1">
                      {lane}
                    </li>
                  ))}
                </ul>
              </button>
            )
          )}
        </div>
      </section>

      {/* Integration selector */}
      <section className="rounded-[var(--radius)] border border-[var(--border)] bg-[var(--surface)] p-5">
        <div className="mb-3">
          <p className="text-xs font-medium uppercase tracking-widest text-[var(--muted)]">
            Integration Registry
          </p>
          <h2 className="font-medium text-foreground">Toggle Allowed Integrations</h2>
        </div>
        <div className="grid grid-cols-2 gap-2 sm:grid-cols-3">
          {(Object.entries(INTEGRATIONS) as [IntegrationKey, string][]).map(([key, desc]) => (
            <button
              key={key}
              onClick={() => toggleIntegration(key)}
              className={cn(
                "rounded-[var(--radius-sm)] border p-3 text-left transition-all cursor-pointer",
                enabledIntegrations.has(key)
                  ? "border-[var(--border-gold)] bg-[var(--gold-dim)]"
                  : "border-[var(--border)] bg-[var(--background)] hover:bg-[var(--surface-elevated)]"
              )}
            >
              <p
                className={cn(
                  "text-xs font-medium mb-0.5 capitalize",
                  enabledIntegrations.has(key) ? "text-[var(--gold)]" : "text-foreground"
                )}
              >
                {key}
              </p>
              <p className="text-[11px] text-[var(--muted)] leading-relaxed line-clamp-2">{desc}</p>
            </button>
          ))}
        </div>
      </section>

      {/* Mission builder + Runbook output */}
      <div className="grid grid-cols-1 gap-4 lg:grid-cols-2">
        {/* Mission builder */}
        <section className="rounded-[var(--radius)] border border-[var(--border)] bg-[var(--surface)] p-5 flex flex-col gap-3">
          <div>
            <p className="text-xs font-medium uppercase tracking-widest text-[var(--muted)]">
              Mission Builder
            </p>
            <h2 className="font-medium text-foreground">Frame the Internal Run</h2>
          </div>

          <div className="flex flex-col gap-1">
            <label className="text-xs text-[var(--muted)]">Workflow type</label>
            <select
              value={workflow}
              onChange={(e) => setWorkflow(e.target.value as WorkflowKey)}
              className="rounded-lg border border-[var(--border)] bg-[var(--background)] px-3 py-2 text-sm text-foreground focus:border-[var(--blue)] focus:outline-none"
            >
              {Object.keys(WORKFLOW_PROFILES).map((wf) => (
                <option key={wf} value={wf}>{wf}</option>
              ))}
            </select>
          </div>

          {[
            { id: "mission", label: "Mission", value: mission, set: setMission, placeholder: "What needs to get done in this run?" },
            { id: "deliverables", label: "Deliverables", value: deliverables, set: setDeliverables, placeholder: "List the exact outputs you want. One line per deliverable." },
            { id: "constraints", label: "Constraints", value: constraints, set: setConstraints, placeholder: "List the boundaries, quality requirements, and things we cannot break." },
            { id: "context", label: "Source assets or context", value: context, set: setContext, placeholder: "List files, URLs, live pages, campaign references, drawings, or customer details." },
          ].map(({ id, label, value, set, placeholder }) => (
            <div key={id} className="flex flex-col gap-1">
              <label className="text-xs text-[var(--muted)]">{label}</label>
              <textarea
                value={value}
                onChange={(e) => set(e.target.value)}
                rows={3}
                placeholder={placeholder}
                className="resize-none rounded-lg border border-[var(--border)] bg-[var(--background)] px-3 py-2.5 text-sm text-foreground placeholder:text-[var(--muted)] focus:border-[var(--blue)] focus:outline-none leading-relaxed"
              />
            </div>
          ))}

          <div className="flex gap-2">
            <button
              onClick={buildRunbook}
              className="flex flex-1 items-center justify-center gap-2 rounded-lg bg-[var(--gold)] px-4 py-2.5 text-sm font-medium text-[var(--background)] hover:brightness-110 transition-all"
            >
              Generate Private Runbook
            </button>
            <button
              onClick={reset}
              className="flex items-center gap-1.5 rounded-lg border border-[var(--border)] bg-[var(--background)] px-3 py-2.5 text-sm text-[var(--muted)] hover:text-foreground transition-colors"
            >
              <RotateCcw className="h-3.5 w-3.5" />
              Reset
            </button>
          </div>
        </section>

        {/* Runbook output */}
        <section className="rounded-[var(--radius)] border border-[var(--border)] bg-[var(--surface)] p-5 flex flex-col gap-3">
          <div>
            <p className="text-xs font-medium uppercase tracking-widest text-[var(--muted)]">
              Generated Runbook
            </p>
            <h2 className="font-medium text-foreground">Copy into Execution Environment</h2>
          </div>

          {summaryItems.length > 0 && (
            <div className="grid grid-cols-2 gap-2">
              {summaryItems.map((item) => (
                <SummaryCard key={item.label} label={item.label} value={item.value} />
              ))}
            </div>
          )}

          {/* Terminal output */}
          <div className="relative rounded-[var(--radius-sm)] border border-[var(--border)] bg-[rgba(4,10,22,0.95)] overflow-hidden flex-1">
            <div className="flex items-center justify-between border-b border-[var(--border)] px-4 py-2">
              <div className="flex items-center gap-2">
                <div className="flex gap-1.5">
                  <span className="h-2.5 w-2.5 rounded-full bg-[rgba(248,113,113,0.6)]" />
                  <span className="h-2.5 w-2.5 rounded-full bg-[rgba(242,201,109,0.6)]" />
                  <span className="h-2.5 w-2.5 rounded-full bg-[rgba(74,222,128,0.6)]" />
                </div>
                <span className="text-xs font-mono text-[var(--muted)]">focus-private :: runbook</span>
              </div>
              <div className="flex gap-2">
                <button
                  onClick={copyRunbook}
                  disabled={output === DEFAULT_OUTPUT}
                  className="flex items-center gap-1 rounded px-2 py-1 text-xs text-[var(--muted)] hover:text-foreground hover:bg-[var(--surface)] transition-colors disabled:opacity-30"
                >
                  <Copy className="h-3 w-3" />
                  {copied ? "Copied!" : "Copy"}
                </button>
                <button
                  onClick={downloadRunbook}
                  disabled={output === DEFAULT_OUTPUT}
                  className="flex items-center gap-1 rounded px-2 py-1 text-xs text-[var(--muted)] hover:text-foreground hover:bg-[var(--surface)] transition-colors disabled:opacity-30"
                >
                  <Download className="h-3 w-3" />
                  Save
                </button>
              </div>
            </div>
            <pre className="terminal overflow-auto p-4 text-[var(--foreground)] min-h-[360px] max-h-[480px] text-sm">
              {output}
            </pre>
          </div>
        </section>
      </div>
    </div>
  );
}
