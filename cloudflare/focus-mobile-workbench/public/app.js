const STORAGE_KEY = "focus-mobile-workbench-state";

const state = {
  sessionReady: false,
  stacks: [],
  bridges: [],
  templates: [],
  providers: [],
  selectedStackId: "",
  selectedBridgeIds: [],
  selectedProvider: "fallback",
  currentRun: null,
};

function byId(id) {
  return document.getElementById(id);
}

async function api(path, options = {}) {
  const response = await fetch(path, {
    credentials: "same-origin",
    headers: {
      "content-type": "application/json",
      ...(options.headers || {}),
    },
    ...options,
  });

  const data = await response.json().catch(() => ({}));
  if (!response.ok || data.ok === false) {
    throw new Error(data.error || `Request failed with status ${response.status}`);
  }
  return data;
}

function saveState() {
  const payload = {
    selectedStackId: state.selectedStackId,
    selectedBridgeIds: state.selectedBridgeIds,
    selectedProvider: state.selectedProvider,
    mission: byId("mission-input").value,
    documentText: byId("document-input").value,
  };
  localStorage.setItem(STORAGE_KEY, JSON.stringify(payload));
}

function restoreState() {
  try {
    const raw = localStorage.getItem(STORAGE_KEY);
    if (!raw) return;
    const payload = JSON.parse(raw);
    state.selectedStackId = payload.selectedStackId || state.selectedStackId;
    state.selectedBridgeIds = Array.isArray(payload.selectedBridgeIds) ? payload.selectedBridgeIds : [];
    state.selectedProvider = payload.selectedProvider || state.selectedProvider;
    byId("mission-input").value = payload.mission || "";
    byId("document-input").value = payload.documentText || "";
  } catch (_error) {
    localStorage.removeItem(STORAGE_KEY);
  }
}

function runtimeChipText() {
  const configured = state.providers.filter((provider) => provider.configured).length;
  return configured
    ? `${configured} provider${configured === 1 ? "" : "s"} ready`
    : "Fallback planner only";
}

function setLoginState(ready) {
  state.sessionReady = ready;
  byId("login-panel").classList.toggle("hidden", ready);
  byId("workspace").classList.toggle("hidden", !ready);
}

function selectedStack() {
  return state.stacks.find((stack) => stack.id === state.selectedStackId) || state.stacks[0];
}

function selectedProviderRecord() {
  return state.providers.find((provider) => provider.id === state.selectedProvider);
}

function updateMetrics() {
  byId("metric-stacks").textContent = String(state.stacks.length);
  byId("metric-bridges").textContent = String(state.bridges.length);
  byId("metric-providers").textContent = String(state.providers.filter((provider) => provider.configured).length);
  byId("runtime-chip").textContent = runtimeChipText();
}

function renderStacks() {
  const root = byId("stack-list");
  root.innerHTML = state.stacks
    .map(
      (stack) => `
        <button class="stack-card ${stack.id === state.selectedStackId ? "active" : ""}" type="button" data-stack-id="${stack.id}">
          <strong>${stack.label}</strong>
          <span>${stack.objective}</span>
        </button>
      `
    )
    .join("");

  root.querySelectorAll("[data-stack-id]").forEach((button) => {
    button.addEventListener("click", () => {
      state.selectedStackId = button.dataset.stackId;
      renderStacks();
      saveState();
    });
  });
}

function renderBridges() {
  const root = byId("bridge-list");
  root.innerHTML = state.bridges
    .map(
      (bridge) => `
        <button class="bridge-card ${state.selectedBridgeIds.includes(bridge.id) ? "active" : ""}" type="button" data-bridge-id="${bridge.id}">
          <strong>${bridge.label}</strong>
          <span>${bridge.role}</span>
        </button>
      `
    )
    .join("");

  root.querySelectorAll("[data-bridge-id]").forEach((button) => {
    button.addEventListener("click", () => {
      const id = button.dataset.bridgeId;
      if (state.selectedBridgeIds.includes(id)) {
        state.selectedBridgeIds = state.selectedBridgeIds.filter((value) => value !== id);
      } else {
        state.selectedBridgeIds = [...state.selectedBridgeIds, id];
      }
      renderBridges();
      saveState();
    });
  });
}

function renderTemplates() {
  const root = byId("template-list");
  root.innerHTML = state.templates
    .map(
      (template) => `
        <button class="template-card" type="button" data-template-id="${template.id}">
          <strong>${template.label}</strong>
          <span>${template.content.split("\n").slice(0, 3).join(" ").trim()}</span>
        </button>
      `
    )
    .join("");

  const templateSelect = byId("template-select");
  templateSelect.innerHTML = ['<option value="">Choose a template</option>']
    .concat(
      state.templates.map((template) => `<option value="${template.id}">${template.label}</option>`)
    )
    .join("");

  root.querySelectorAll("[data-template-id]").forEach((button) => {
    button.addEventListener("click", () => insertTemplate(button.dataset.templateId));
  });
}

function renderProviderSelect() {
  const select = byId("provider-select");
  select.innerHTML = state.providers
    .map(
      (provider) =>
        `<option value="${provider.id}" ${!provider.configured ? "disabled" : ""}>${provider.label}${provider.configured ? "" : " (not configured)"}</option>`
    )
    .join("");

  if (!state.providers.find((provider) => provider.id === state.selectedProvider && provider.configured)) {
    const liveProvider = state.providers.find((provider) => provider.configured && provider.id !== "fallback");
    state.selectedProvider = liveProvider?.id || "fallback";
  }

  select.value = state.selectedProvider;
}

function renderRunMeta(run) {
  const root = byId("run-meta");
  if (!run) {
    root.innerHTML = `
      <article><span>Status</span><strong>Idle</strong></article>
      <article><span>Provider</span><strong>Not selected</strong></article>
      <article><span>Model</span><strong>n/a</strong></article>
    `;
    return;
  }

  root.innerHTML = `
    <article><span>Status</span><strong>${run.mode === "live" ? "Completed" : "Planned"}</strong></article>
    <article><span>Provider</span><strong>${run.provider}</strong></article>
    <article><span>Model</span><strong>${run.model}</strong></article>
  `;
}

function setOutput(text) {
  byId("output-panel").textContent = text;
}

function buildRunText(run) {
  return [
    `# ${run.stack.label}`,
    "",
    `Run ID: ${run.id}`,
    `Created: ${run.createdAt}`,
    `Mode: ${run.mode}`,
    `Provider: ${run.provider}`,
    `Model: ${run.model}`,
    "",
    run.output,
  ].join("\n");
}

function insertTemplate(templateId = byId("template-select").value) {
  const template = state.templates.find((entry) => entry.id === templateId);
  if (!template) return;
  const editor = byId("document-input");
  const prefix = editor.value.trim() ? `${editor.value.trim()}\n\n` : "";
  editor.value = `${prefix}${template.content}`.trim();
  saveState();
}

async function loadStatus() {
  const payload = await api("/api/status", { method: "GET" });
  state.stacks = payload.stacks || [];
  state.bridges = payload.toolBridges || [];
  state.templates = payload.templates || [];
  state.providers = payload.providers || [];

  if (!state.selectedStackId) {
    state.selectedStackId = state.stacks[0]?.id || "";
  }
  if (!state.selectedBridgeIds.length) {
    state.selectedBridgeIds = state.bridges.slice(0, 3).map((bridge) => bridge.id);
  }

  updateMetrics();
  renderStacks();
  renderBridges();
  renderTemplates();
  renderProviderSelect();
}

async function login() {
  const password = byId("login-password").value;
  const message = byId("login-message");
  message.textContent = "Unlocking workbench…";

  try {
    await api("/api/session", {
      method: "POST",
      body: JSON.stringify({ password }),
    });
    setLoginState(true);
    await loadStatus();
    renderRunMeta(null);
    setOutput("Choose a stack, frame the mission, and run the workbench.");
    message.textContent = "";
  } catch (error) {
    message.textContent = error.message;
  }
}

async function logout() {
  await api("/api/session", { method: "DELETE" }).catch(() => {});
  setLoginState(false);
  byId("login-password").value = "";
  byId("login-message").textContent = "Workbench locked.";
}

async function runMission() {
  const mission = byId("mission-input").value.trim();
  const documentText = byId("document-input").value.trim();
  if (!mission) {
    setOutput("Add a mission before running the workbench.");
    return;
  }

  const runButton = byId("run-button");
  const previous = runButton.textContent;
  runButton.disabled = true;
  runButton.textContent = "Running…";
  setOutput("Running the selected stack. This panel will update when the mission completes.");

  try {
    const payload = await api("/api/run", {
      method: "POST",
      body: JSON.stringify({
        stackId: state.selectedStackId,
        provider: state.selectedProvider,
        toolIds: state.selectedBridgeIds,
        prompt: mission,
        documentText,
      }),
    });
    state.currentRun = payload.run;
    renderRunMeta(payload.run);
    setOutput(buildRunText(payload.run));
    saveState();
  } catch (error) {
    setOutput(`Run failed.\n\n${error.message}`);
  } finally {
    runButton.disabled = false;
    runButton.textContent = previous;
  }
}

async function boot() {
  restoreState();

  byId("login-button").addEventListener("click", login);
  byId("login-password").addEventListener("keydown", (event) => {
    if (event.key === "Enter") {
      login();
    }
  });
  byId("logout-button").addEventListener("click", logout);
  byId("refresh-button").addEventListener("click", loadStatus);
  byId("run-button").addEventListener("click", runMission);
  byId("insert-template").addEventListener("click", () => insertTemplate());
  byId("provider-select").addEventListener("change", (event) => {
    state.selectedProvider = event.target.value;
    saveState();
  });
  byId("mission-input").addEventListener("input", saveState);
  byId("document-input").addEventListener("input", saveState);

  byId("copy-button").addEventListener("click", async () => {
    await navigator.clipboard.writeText(byId("output-panel").textContent);
  });

  byId("download-button").addEventListener("click", () => {
    const blob = new Blob([byId("output-panel").textContent], { type: "text/markdown" });
    const link = document.createElement("a");
    link.href = URL.createObjectURL(blob);
    link.download = "focus-mobile-workbench-run.md";
    link.click();
    URL.revokeObjectURL(link.href);
  });

  try {
    await loadStatus();
    setLoginState(true);
    renderRunMeta(null);
    setOutput("Choose a stack, frame the mission, and run the workbench.");
  } catch (_error) {
    setLoginState(false);
  }
}

boot();
