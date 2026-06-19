export type EngineKey =
  | "research"
  | "claims"
  | "writing"
  | "geometry"
  | "construction"
  | "compliance"
  | "frequency"
  | "marketing"
  | "ai_twin"
  | "publish"
  | "automation";

export interface EngineProfile {
  key: EngineKey;
  label: string;
  focus: string;
  deliverables: string[];
  icon: string;
}

export const ENGINE_PROFILES: Record<EngineKey, EngineProfile> = {
  research: {
    key: "research",
    label: "Research Engine",
    focus: "verified research, synthesis, constraints, and next-best actions",
    deliverables: ["source-aware findings summary", "key risks and assumptions", "recommended next actions"],
    icon: "🔬",
  },
  claims: {
    key: "claims",
    label: "Claims Engine",
    focus: "claim extraction, verification paths, evidence priorities, and rebuttal logic",
    deliverables: ["top claims list", "verification path per claim", "evidence gaps and confidence notes"],
    icon: "⚖️",
  },
  writing: {
    key: "writing",
    label: "Writing Engine",
    focus: "clear, conversion-grade writing, structured drafts, and deliverable polish",
    deliverables: ["high-quality draft output", "headline or framing options", "action checklist for the user"],
    icon: "✍️",
  },
  geometry: {
    key: "geometry",
    label: "Geometry Engine",
    focus: "layout logic, dimensions assumptions, spatial constraints, and visual structure",
    deliverables: ["spatial concept direction", "layout assumptions", "constraints and implementation notes"],
    icon: "📐",
  },
  construction: {
    key: "construction",
    label: "Construction Engine",
    focus: "execution planning, milestones, dependencies, field risk, and build sequencing",
    deliverables: ["build sequence", "dependency and risk register", "owner-facing summary"],
    icon: "🏗️",
  },
  compliance: {
    key: "compliance",
    label: "Compliance Engine",
    focus: "compliance guardrails, operational risks, approvals, and required review steps",
    deliverables: ["compliance watchouts", "required approvals", "safe execution checklist"],
    icon: "🛡️",
  },
  frequency: {
    key: "frequency",
    label: "Frequency Engine",
    focus: "cadence design, operational rhythm, attention management, and execution routines",
    deliverables: ["execution cadence", "daily or weekly ritual", "focus preservation rules"],
    icon: "📡",
  },
  marketing: {
    key: "marketing",
    label: "Marketing Engine",
    focus: "offer framing, channel strategy, message architecture, and KPI design",
    deliverables: ["channel plan", "message angle", "offer positioning and KPIs"],
    icon: "📣",
  },
  ai_twin: {
    key: "ai_twin",
    label: "AI Twin Video Engine",
    focus: "avatar strategy, video twin scripting, shot prompts, scene sequencing, and distribution cuts",
    deliverables: ["ai twin identity brief", "scene-by-scene video treatment", "voiceover and shot prompt stack"],
    icon: "🎬",
  },
  publish: {
    key: "publish",
    label: "Publishing Engine",
    focus: "release packaging, launch surfaces, repo readiness, and downstream publishing handoff",
    deliverables: ["release package summary", "publish checklist", "connector-ready handoff notes"],
    icon: "🚀",
  },
  automation: {
    key: "automation",
    label: "Automation Engine",
    focus: "connector routing, webhook handoff, remote execution, and ops-system continuation",
    deliverables: ["automation route plan", "connector handoff payload", "remote execution notes"],
    icon: "⚙️",
  },
};

export const ENGINE_SEQUENCES: Record<string, EngineKey[]> = {
  research: ["research", "writing", "automation"],
  claims: ["research", "claims", "writing", "automation"],
  writing: ["research", "writing", "automation"],
  geometry: ["research", "geometry", "construction", "automation"],
  construction: ["research", "geometry", "construction", "writing", "automation"],
  compliance: ["research", "claims", "compliance", "automation"],
  frequency: ["research", "frequency", "automation"],
  marketing: ["research", "writing", "marketing", "publish", "automation"],
  ai_twin: ["research", "writing", "ai_twin", "marketing", "automation"],
  publish: ["research", "writing", "publish", "automation"],
  automation: ["research", "writing", "automation"],
  full: ["research", "claims", "writing", "geometry", "construction", "compliance", "marketing", "publish", "automation"],
};

export type TaskStatus = "pending" | "running" | "completed" | "error";

export interface PipelineTask {
  id: string;
  task: string;
  engine: EngineKey;
  company_id?: string;
  execution_mode: "dry_run" | "live_ready";
  status: TaskStatus;
  output?: string;
  created_at: string;
  completed_at?: string;
  route?: string;
}

export const STATUS_COLORS: Record<TaskStatus, string> = {
  pending: "text-[var(--muted)]",
  running: "text-[var(--running)]",
  completed: "text-[var(--success)]",
  error: "text-[var(--error)]",
};

export const STATUS_BG: Record<TaskStatus, string> = {
  pending: "bg-[rgba(107,132,168,0.15)]",
  running: "bg-[rgba(96,165,250,0.15)]",
  completed: "bg-[rgba(74,222,128,0.12)]",
  error: "bg-[rgba(248,113,113,0.12)]",
};
