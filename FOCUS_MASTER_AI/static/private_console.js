const PRIVATE_STORAGE_KEY = "focus-private-operations-console-state";
const DEFAULT_OUTPUT = "Generate the private runbook to populate this panel.";

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
};

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
  "Sacred Geometry Book Research and Publishing": {
    outcome: "research, verify, outline, draft, and package a source-disciplined nonfiction book project",
    steps: [
      "Build the research database and reliability-ranked evidence set.",
      "Extract claims, verify them, and design the manuscript structure.",
      "Draft, diagram, audit, and assemble the final publication package.",
    ],
  },
  "Executive Planning and Prioritization": {
    outcome: "produce a tightly prioritized command plan with sequencing, timing, and follow-up",
    steps: [
      "Capture all relevant tasks, deadlines, dependencies, and priorities.",
      "Convert raw work into a structured execution plan.",
      "Package the plan into an operator-ready command brief.",
    ],
  },
};

const INTEGRATION_DETAILS = {
  github: "Branch work, releases, deployments, and implementation tracking.",
  stripe: "Secure checkout links, pricing ladders, and product or service payment routing.",
  adobe: "Creative direction, PDF packets, visual studies, and production-ready branded assets.",
  figma: "Layout planning, interface references, and design-system translation.",
  airtable: "Structured operating data, client records, and service inventory.",
  media: "Campaign resizing, video prep, and future beat-catalog packaging.",
};

function businessCards() {
  return Array.from(document.querySelectorAll(".business-card"));
}

function integrationCards() {
  return Array.from(document.querySelectorAll(".integration-card"));
}

function selectedBusiness() {
  return businessCards().find((card) => card.classList.contains("active"))?.dataset.business || "focus-negotium";
}

function selectedIntegrations() {
  return integrationCards()
    .filter((card) => card.classList.contains("active"))
    .map((card) => card.dataset.integration);
}

function getState() {
  return {
    business: selectedBusiness(),
    integrations: selectedIntegrations(),
    workflow: document.getElementById("workflow").value,
    stackId: document.getElementById("stack-id").value,
    preferredProvider: document.getElementById("preferred-provider").value,
    mission: document.getElementById("mission").value.trim(),
    deliverables: document.getElementById("deliverables").value.trim(),
    constraints: document.getElementById("constraints").value.trim(),
    context: document.getElementById("context").value.trim(),
    executeAutomation: document.getElementById("execute-automation").checked,
  };
}

function saveState() {
  localStorage.setItem(PRIVATE_STORAGE_KEY, JSON.stringify(getState()));
}

function applyBusinessSelection(businessKey) {
  businessCards().forEach((card) => {
    card.classList.toggle("active", card.dataset.business === businessKey);
  });
}

function applyIntegrationSelection(keys) {
  const selected = new Set(keys);
  integrationCards().forEach((card) => {
    card.classList.toggle("active", selected.has(card.dataset.integration));
  });
}

function restoreState() {
  const raw = localStorage.getItem(PRIVATE_STORAGE_KEY);
  if (!raw) {
    return;
  }

  try {
    const state = JSON.parse(raw);
    if (state.business) {
      applyBusinessSelection(state.business);
    }
    if (Array.isArray(state.integrations)) {
      applyIntegrationSelection(state.integrations);
    }
    if (typeof state.stackId === "string") {
      document.getElementById("stack-id").value = state.stackId;
    }
    if (typeof state.preferredProvider === "string") {
      document.getElementById("preferred-provider").value = state.preferredProvider;
    }
    if (typeof state.executeAutomation === "boolean") {
      document.getElementById("execute-automation").checked = state.executeAutomation;
    }
    ["workflow", "mission", "deliverables", "constraints", "context"].forEach((id) => {
      if (typeof state[id] === "string") {
        document.getElementById(id).value = state[id];
      }
    });
  } catch (_error) {
    localStorage.removeItem(PRIVATE_STORAGE_KEY);
  }
}

function lines(value, fallback) {
  const parsed = value
    .split("\n")
    .map((line) => line.trim())
    .filter(Boolean);
  return parsed.length ? parsed : fallback;
}

function updateSummary(state) {
  const business = BUSINESS_PROFILES[state.business];
  const integrations = state.integrations.length ? state.integrations : ["github"];
  const deliverables = lines(state.deliverables, []);
  const constraints = lines(state.constraints, []);

  document.getElementById("summary-grid").innerHTML = `
    <article>
      <span>Business lane</span>
      <strong>${business.name}</strong>
    </article>
    <article>
      <span>Workflow</span>
      <strong>${state.workflow}</strong>
    </article>
    <article>
      <span>Preferred provider</span>
      <strong>${state.preferredProvider || "Auto route"}</strong>
    </article>
    <article>
      <span>Workflow stack</span>
      <strong>${state.stackId || "Auto-select"}</strong>
    </article>
    <article>
      <span>Integrations</span>
      <strong>${integrations.length} enabled</strong>
    </article>
    <article>
      <span>Deliverables</span>
      <strong>${deliverables.length || 0} listed</strong>
    </article>
    <article>
      <span>Constraints</span>
      <strong>${constraints.length || 0} tracked</strong>
    </article>
  `;
}

function renderRunMetadata(run) {
  const metadata = document.getElementById("run-metadata");
  if (!run) {
    metadata.innerHTML = "";
    return;
  }

  const engineCount = Array.isArray(run.results) ? run.results.length : 0;
  const summaryMeta = run.final_summary_meta || {};
  metadata.innerHTML = `
    <article>
      <span>Run ID</span>
      <strong>${run.id}</strong>
    </article>
    <article>
      <span>Status</span>
      <strong>${run.status}</strong>
    </article>
    <article>
      <span>Engine count</span>
      <strong>${engineCount}</strong>
    </article>
    <article>
      <span>Summary provider</span>
      <strong>${summaryMeta.provider || "n/a"} / ${summaryMeta.mode || "n/a"}</strong>
    </article>
    <article>
      <span>Created</span>
      <strong>${new Date(run.created_at).toLocaleString()}</strong>
    </article>
    <article>
      <span>Automation</span>
      <strong>${run.execute_automation ? "Enabled" : "Review only"}</strong>
    </article>
    <article>
      <span>Workflow stack</span>
      <strong>${run.workflow_stack?.label || run.workflow_stack?.id || "n/a"}</strong>
    </article>
    <article>
      <span>Artifacts</span>
      <strong>${(run.artifacts || []).length}</strong>
    </article>
  `;
}

function buildRunbook() {
  const state = getState();
  const business = BUSINESS_PROFILES[state.business];
  const workflow = WORKFLOW_PROFILES[state.workflow];
  const deliverables = lines(state.deliverables, ["Define the first deliverable before execution starts."]);
  const constraints = lines(state.constraints, [
    "Protect live quality, keep the workflow reviewable, and preserve rollback safety.",
  ]);
  const context = lines(state.context, ["Attach source files, live URLs, or notes before execution."]);
  const integrations = state.integrations.length ? state.integrations : ["github"];
  const timestamp = new Date().toLocaleString();

  const linesOut = [
    "# FOCUS PRIVATE OPERATIONS CONSOLE :: RUNBOOK",
    "",
    `Generated: ${timestamp}`,
    "",
    "## Mission",
    state.mission || "Define the mission for this private run before execution begins.",
    "",
    "## Business Lane",
    `- ${business.name} (${business.role})`,
    ...business.lanes.map((lane) => `- ${lane}`),
    "",
    "## Workflow Type",
    `- ${state.workflow}`,
    `- Target outcome: ${workflow.outcome}`,
    "",
    "## Preferred Provider",
    `- ${state.preferredProvider || "Auto route across configured providers"}`,
    `- Stack preference: ${state.stackId || "Auto-select best stack"}`,
    "",
    "## Deliverables",
    ...deliverables.map((item) => `- ${item}`),
    "",
    "## Constraints",
    ...constraints.map((item) => `- ${item}`),
    "",
    "## Source Context",
    ...context.map((item) => `- ${item}`),
    "",
    "## Integration Lanes",
    ...integrations.map((key) => `- ${key}: ${INTEGRATION_DETAILS[key]}`),
    "",
    "## Execution Sequence",
    ...workflow.steps.map((step, index) => `${index + 1}. ${step}`),
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

  updateSummary(state);
  return linesOut.join("\n");
}

function renderRunbook() {
  const output = buildRunbook();
  document.getElementById("output").textContent = output;
  renderRunMetadata(null);
  saveState();
}

function payloadForRun() {
  const state = getState();
  return {
    business: state.business,
    workflow: state.workflow,
    stack_id: state.stackId || null,
    preferred_provider: state.preferredProvider || null,
    mission: state.mission,
    deliverables: lines(state.deliverables, []),
    constraints: lines(state.constraints, []),
    context: lines(state.context, []),
    integrations: state.integrations,
    execute_automation: state.executeAutomation,
  };
}

function outputForRun(run) {
  const sequence = (run.engine_sequence || []).join(", ");
  const engineBlocks = (run.results || [])
    .map((result) => {
      const execution = result.model_execution || {};
      return [
        `## ${result.label}`,
        `Provider: ${execution.provider || "fallback"}`,
        `Model: ${execution.model || "templated-fallback"}`,
        `Mode: ${execution.mode || "fallback"}`,
        "",
        result.output || "",
      ].join("\n");
    })
    .join("\n\n");
  const toolRuns = (run.tool_runs || []).map((tool) => `- ${tool.label}: ${tool.status}`).join("\n");

  return [
    `# ${run.workflow} :: ${run.status}`,
    "",
    `Run ID: ${run.id}`,
    `Business: ${run.business}`,
    `Stack: ${run.workflow_stack?.label || run.workflow_stack?.id || "n/a"}`,
    `Sequence: ${sequence}`,
    "",
    "## Final Summary",
    run.final_summary || "No final summary was generated.",
    "",
    "## Tool Runs",
    toolRuns || "No tool runs recorded.",
    "",
    "## Engine Outputs",
    engineBlocks || "No engine outputs recorded.",
  ].join("\n");
}

async function fetchJson(url, options = {}) {
  const response = await fetch(url, options);
  const data = await response.json();
  if (!response.ok || data.ok === false) {
    throw new Error(data.error || `Request failed with status ${response.status}`);
  }
  return data;
}

function renderProviderStatus(runtime) {
  const providerList = document.getElementById("provider-status");
  const providers = runtime.providers || [];
  providerList.innerHTML = providers
    .map(
      (provider) => `
      <li>
        <strong>${provider.provider} / ${provider.default_model}</strong>
        <span>${provider.message}</span>
      </li>
    `
    )
    .join("");

  const runtimeSummary = document.getElementById("runtime-summary");
  const connectors = runtime.connectors || { ready_count: 0, total: 0, attention_count: 0 };
  const jobs = runtime.jobs || { active_count: 0 };
  runtimeSummary.innerHTML = `
    <article>
      <span>Configured providers</span>
      <strong>${providers.filter((item) => item.configured).length}</strong>
    </article>
    <article>
      <span>Connectors ready</span>
      <strong>${connectors.ready_count}/${connectors.total}</strong>
    </article>
    <article>
      <span>Connector attention</span>
      <strong>${connectors.attention_count}</strong>
    </article>
    <article>
      <span>Recent runs</span>
      <strong>${(runtime.recent_runs || []).length}</strong>
    </article>
    <article>
      <span>Active jobs</span>
      <strong>${jobs.active_count || 0}</strong>
    </article>
  `;
}

function renderRecentRuns(runs) {
  const list = document.getElementById("recent-runs");
  if (!runs.length) {
    list.innerHTML = "<li><strong>No runs yet.</strong><span>Launch the first mission to populate this panel.</span></li>";
    return;
  }

  list.innerHTML = runs
    .map(
      (run) => `
      <li>
        <strong>${run.workflow}</strong>
        <span>${run.status} / ${new Date(run.created_at).toLocaleString()}</span>
        <div class="button-row">
          <button class="secondary run-detail" data-run-id="${run.id}" type="button">View run</button>
        </div>
      </li>
    `
    )
    .join("");

  document.querySelectorAll(".run-detail").forEach((button) => {
    button.addEventListener("click", async () => {
      await loadRun(button.dataset.runId);
    });
  });
}

function renderStackOptions(stacks) {
  const select = document.getElementById("stack-id");
  const current = select.value;
  select.innerHTML = ['<option value="">Auto-select best stack</option>']
    .concat((stacks || []).map((stack) => `<option value="${stack.id}">${stack.label}</option>`))
    .join("");
  if (current) {
    select.value = current;
  }
}

function renderArtifacts(artifacts) {
  const list = document.getElementById("artifact-list");
  if (!artifacts || !artifacts.length) {
    list.innerHTML = "<li><strong>No artifacts yet.</strong><span>Launch or queue a run to generate stored outputs.</span></li>";
    return;
  }

  list.innerHTML = artifacts
    .map(
      (artifact) => `
      <li>
        <strong>${artifact.name}</strong>
        <span>${artifact.kind} / ${artifact.filename}</span>
      </li>
    `
    )
    .join("");
}

async function refreshRuntime() {
  const payload = await fetchJson("/v1/private/runtime");
  renderProviderStatus(payload.runtime);
  renderRecentRuns(payload.runtime.recent_runs || []);
  renderStackOptions(payload.runtime.stacks || []);
}

async function loadRun(runId) {
  const payload = await fetchJson(`/v1/private/runs/${runId}`);
  document.getElementById("output").textContent = outputForRun(payload.run);
  renderRunMetadata(payload.run);
  renderArtifacts(payload.run.artifacts || []);
}

async function launchRun() {
  const payload = payloadForRun();
  if (!payload.mission) {
    document.getElementById("output").textContent = "Mission is required before launching the private engine.";
    return;
  }

  const launchButton = document.getElementById("launch");
  const previousLabel = launchButton.textContent;
  launchButton.disabled = true;
  launchButton.textContent = "Running private engine...";
  document.getElementById("output").textContent = "Executing private engine sequence. This panel will populate when the run completes.";

  try {
    const response = await fetchJson("/v1/private/runs", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });
    const run = response.run;
    document.getElementById("output").textContent = outputForRun(run);
    renderRunMetadata(run);
    renderArtifacts(run.artifacts || []);
    await refreshRuntime();
  } catch (error) {
    document.getElementById("output").textContent = `Private engine run failed.\n\n${error.message}`;
    renderRunMetadata(null);
    renderArtifacts([]);
  } finally {
    launchButton.disabled = false;
    launchButton.textContent = previousLabel;
  }
}

async function queueRun() {
  const payload = payloadForRun();
  if (!payload.mission) {
    document.getElementById("output").textContent = "Mission is required before queueing the private engine.";
    return;
  }

  const queueButton = document.getElementById("queue");
  const previousLabel = queueButton.textContent;
  queueButton.disabled = true;
  queueButton.textContent = "Queueing...";
  document.getElementById("output").textContent = "Queueing background run. The console will refresh status and load the result when it finishes.";

  try {
    const response = await fetchJson("/v1/private/jobs", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });
    renderRunMetadata(response.run);
    renderArtifacts(response.run.artifacts || []);
    await refreshRuntime();
    await waitForRunCompletion(response.run.id);
  } catch (error) {
    document.getElementById("output").textContent = `Background run failed to queue.\n\n${error.message}`;
  } finally {
    queueButton.disabled = false;
    queueButton.textContent = previousLabel;
  }
}

async function waitForRunCompletion(runId) {
  const deadline = Date.now() + 45000;
  while (Date.now() < deadline) {
    const payload = await fetchJson(`/v1/private/runs/${runId}`);
    if (payload.run.status === "completed") {
      document.getElementById("output").textContent = outputForRun(payload.run);
      renderRunMetadata(payload.run);
      renderArtifacts(payload.run.artifacts || []);
      await refreshRuntime();
      return;
    }
    await new Promise((resolve) => setTimeout(resolve, 1200));
  }
  document.getElementById("output").textContent = `Run ${runId} is still processing. Refresh the runtime panel or open the run again in a moment.`;
}

function bindCards() {
  businessCards().forEach((card) => {
    card.addEventListener("click", () => {
      applyBusinessSelection(card.dataset.business);
      renderRunbook();
    });
  });

  integrationCards().forEach((card) => {
    card.addEventListener("click", () => {
      card.classList.toggle("active");
      renderRunbook();
    });
  });
}

function bindInputs() {
  ["workflow", "stack-id", "preferred-provider", "mission", "deliverables", "constraints", "context"].forEach((id) => {
    document.getElementById(id).addEventListener("input", renderRunbook);
    document.getElementById(id).addEventListener("change", renderRunbook);
  });
  document.getElementById("execute-automation").addEventListener("change", renderRunbook);

  document.getElementById("generate").addEventListener("click", renderRunbook);
  document.getElementById("launch").addEventListener("click", launchRun);
  document.getElementById("queue").addEventListener("click", queueRun);
  document.getElementById("reset").addEventListener("click", () => {
    localStorage.removeItem(PRIVATE_STORAGE_KEY);
    document.getElementById("workflow").value = "Website Design and Deployment";
    document.getElementById("stack-id").value = "";
    document.getElementById("preferred-provider").value = "";
    document.getElementById("mission").value = "";
    document.getElementById("deliverables").value = "";
    document.getElementById("constraints").value = "";
    document.getElementById("context").value = "";
    document.getElementById("execute-automation").checked = true;
    applyBusinessSelection("focus-negotium");
    applyIntegrationSelection(["github", "stripe", "adobe"]);
    document.getElementById("output").textContent = DEFAULT_OUTPUT;
    renderRunMetadata(null);
    renderArtifacts([]);
    updateSummary(getState());
  });

  document.getElementById("copy").addEventListener("click", async () => {
    await navigator.clipboard.writeText(document.getElementById("output").textContent);
  });

  document.getElementById("download").addEventListener("click", () => {
    const blob = new Blob([document.getElementById("output").textContent], { type: "text/markdown" });
    const link = document.createElement("a");
    link.href = URL.createObjectURL(blob);
    link.download = "focus-private-runbook.md";
    link.click();
    URL.revokeObjectURL(link.href);
  });
}

restoreState();
applyBusinessSelection(selectedBusiness());
if (!selectedIntegrations().length) {
  applyIntegrationSelection(["github", "stripe", "adobe"]);
}
bindCards();
bindInputs();
updateSummary(getState());
renderArtifacts([]);
refreshRuntime().catch((error) => {
  document.getElementById("provider-status").innerHTML = `<li><strong>Runtime load failed.</strong><span>${error.message}</span></li>`;
});
