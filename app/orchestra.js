const ORCHESTRA_STORAGE_KEY = 'focus-ai-model-orchestra-state';
const DEFAULT_OUTPUT = 'Generate the routing plan to populate this panel.';

const PROVIDER_REGISTRY = {
  openai: {
    name: 'OpenAI',
    label: 'Primary orchestration lane',
    specialties: ['brief compilation', 'code reasoning', 'workflow packaging']
  },
  anthropic: {
    name: 'Anthropic',
    label: 'Secondary reasoning lane',
    specialties: ['long-context review', 'policy-aware critique', 'coverage checks']
  },
  local: {
    name: 'Local Workers',
    label: 'On-device utilities',
    specialties: ['deterministic transforms', 'file outputs', 'bounded automations']
  },
  memory: {
    name: 'Memory Fabric',
    label: 'Persistence + recall',
    specialties: ['session continuity', 'artifact recall', 'operator handoff']
  }
};

const WORKLOAD_PROFILES = {
  'Code generation and debugging': {
    preferredLead: 'openai',
    outcome: 'ship validated source changes with reproducible QA',
    lanes: [
      'normalize the coding mission and break it into bounded implementation slices',
      'run a second-pass reasoning review against regressions and missing tests',
      'delegate deterministic compile, build, and file operations locally',
      'store QA evidence and next-step notes in the continuity layer'
    ]
  },
  'Research and synthesis': {
    preferredLead: 'anthropic',
    outcome: 'deliver a high-coverage synthesis packet with clear decisions',
    lanes: [
      'frame the research question and the exact decision it supports',
      'expand the context window and compare the strongest evidence sources',
      'use local workers for extraction, note cleanup, and structured transforms',
      'capture the final synthesis and unresolved questions for the next round'
    ]
  },
  'Product and storefront execution': {
    preferredLead: 'openai',
    outcome: 'refresh the product surface and verify the live conversion path',
    lanes: [
      'translate the mission into a storefront or product-experience brief',
      'review hierarchy, messaging, and policy-sensitive user flows',
      'use local workers for build steps, asset movement, and repeatable validation',
      'preserve publish notes, live URLs, and rollback details'
    ]
  },
  'Content publishing and book operations': {
    preferredLead: 'openai',
    outcome: 'publish content cleanly with pricing, assets, and distribution aligned',
    lanes: [
      'assemble the publishing brief and exact content deliverables',
      'review structure, clarity, and continuity across long-form material',
      'generate deterministic exports, PDFs, indexes, and package outputs locally',
      'record the publishing state, asset paths, and next campaign actions'
    ]
  },
  'Operations and automation mapping': {
    preferredLead: 'anthropic',
    outcome: 'map a stable operating system with explicit routing and checkpoints',
    lanes: [
      'normalize the operational problem into reusable workflows',
      'audit the routing plan for hidden complexity and missing controls',
      'delegate bounded automations and structured transforms to local workers',
      'persist the operating map and handoff steps for the next operator'
    ]
  }
};

const POLICY_PROFILES = {
  'Balanced admin control': {
    summary: 'Balanced between creative range and operator review.',
    rules: [
      'Require explicit operator approval before publish, deploy, or irreversible changes.',
      'Keep model outputs traceable by lane so decisions can be reviewed later.',
      'Preserve a memory record of inputs, outputs, and next actions.'
    ],
    features: [
      ['Provider registry', 'Register OpenAI, Anthropic, local workers, and memory adapters in one switchboard.'],
      ['Router policies', 'Assign synthesis, build, review, and publish responsibilities without ambiguity.'],
      ['Session state', 'Persist mission, artifacts, outputs, and decisions across working sessions.'],
      ['Admin controls', 'Expose approvals, execution boundaries, audit logs, and emergency stop hooks.']
    ]
  },
  'Research heavy': {
    summary: 'Prioritize long-context comparison, source tracking, and synthesis depth.',
    rules: [
      'Escalate ambiguous evidence to a second review lane before conclusion.',
      'Capture source provenance and keep the output tied to explicit evidence packets.',
      'Use local workers only for extraction and formatting, not for final judgment calls.'
    ],
    features: [
      ['Evidence map', 'Track source coverage, confidence, and contradictions in one research ledger.'],
      ['Dual review lane', 'Use a second reasoning pass whenever the decision carries real weight.'],
      ['Structured exports', 'Format notes, briefs, and references into deterministic deliverables.'],
      ['Memory discipline', 'Save citations, decisions, and open questions for reuse.']
    ]
  },
  'Build heavy': {
    summary: 'Bias toward implementation speed, verification, and bounded automation.',
    rules: [
      'Keep code-edit permissions explicit by lane and confirm deployment intent before release.',
      'Require compile or runtime verification before marking a build lane complete.',
      'Write concise handoff notes so the next operator can continue without re-discovery.'
    ],
    features: [
      ['Execution queue', 'Track tasks by ownership, verification state, and deployment readiness.'],
      ['Verification hooks', 'Attach test, compile, and browser evidence directly to the run summary.'],
      ['Artifact packaging', 'Bundle outputs, manifests, and release notes through local workers.'],
      ['Operator checkpoint', 'Keep one final human approval gate before any live release.']
    ]
  },
  'Publishing heavy': {
    summary: 'Favor asset readiness, pricing clarity, and distribution continuity.',
    rules: [
      'Validate book, product, or content metadata before final publish actions.',
      'Keep download assets and public pages in sync to avoid stale storefront states.',
      'Preserve the final publish summary with links, prices, and delivery notes.'
    ],
    features: [
      ['Catalog manager', 'Coordinate offers, pricing, assets, and live routes from one registry.'],
      ['Export engine', 'Generate PDFs, landing pages, and distribution packages in repeatable steps.'],
      ['Launch review', 'Check sales pages, phone routing, and mobile UX before calling it complete.'],
      ['Continuity log', 'Store live links, inventory state, and follow-up actions for the next campaign.']
    ]
  }
};

const FIELD_IDS = ['mesh-mission', 'mesh-workload', 'mesh-policy', 'mesh-providers'];

function providerCards() {
  return Array.from(document.querySelectorAll('.provider-card'));
}

function selectedProviderKeys() {
  return providerCards()
    .filter((card) => card.classList.contains('active'))
    .map((card) => card.dataset.provider);
}

function providerNames(keys) {
  return keys.map((key) => PROVIDER_REGISTRY[key]?.name || key);
}

function syncProvidersInput() {
  document.getElementById('mesh-providers').value = providerNames(selectedProviderKeys()).join(', ');
}

function applyProviderSelection(keys) {
  const normalized = Array.from(new Set(keys.filter((key) => PROVIDER_REGISTRY[key])));
  const finalKeys = normalized.length ? normalized : ['openai'];
  providerCards().forEach((card) => {
    card.classList.toggle('active', finalKeys.includes(card.dataset.provider));
  });
  syncProvidersInput();
}

function getState() {
  return {
    mission: document.getElementById('mesh-mission').value.trim(),
    workload: document.getElementById('mesh-workload').value,
    policy: document.getElementById('mesh-policy').value,
    providers: selectedProviderKeys()
  };
}

function saveState() {
  localStorage.setItem(ORCHESTRA_STORAGE_KEY, JSON.stringify(getState()));
}

function restoreState() {
  const raw = localStorage.getItem(ORCHESTRA_STORAGE_KEY);
  if (!raw) {
    syncProvidersInput();
    return;
  }

  try {
    const state = JSON.parse(raw);
    FIELD_IDS.forEach((id) => {
      const key = id.replace('mesh-', '');
      const element = document.getElementById(id);
      if (typeof state[key] === 'string') {
        element.value = state[key];
      }
    });
    applyProviderSelection(Array.isArray(state.providers) ? state.providers : []);
  } catch (_error) {
    localStorage.removeItem(ORCHESTRA_STORAGE_KEY);
    syncProvidersInput();
  }
}

function providerFor(keys, preferred) {
  return keys.includes(preferred) ? preferred : keys[0];
}

function secondaryReviewer(keys, lead) {
  const preferred = ['anthropic', 'openai', 'memory', 'local'];
  return preferred.find((key) => keys.includes(key) && key !== lead) || lead;
}

function executionLane(keys, lead) {
  if (keys.includes('local')) {
    return 'local';
  }
  return secondaryReviewer(keys, lead);
}

function memoryLane(keys, lead) {
  if (keys.includes('memory')) {
    return 'memory';
  }
  return secondaryReviewer(keys, lead);
}

function renderSummary(state, lead, reviewer, executor) {
  const summary = document.getElementById('mesh-summary');
  summary.innerHTML = `
    <article>
      <span>Lead lane</span>
      <strong>${PROVIDER_REGISTRY[lead].name}</strong>
    </article>
    <article>
      <span>Review lane</span>
      <strong>${PROVIDER_REGISTRY[reviewer].name}</strong>
    </article>
    <article>
      <span>Execution posture</span>
      <strong>${state.policy}</strong>
    </article>
    <article>
      <span>Active providers</span>
      <strong>${state.providers.length}</strong>
    </article>
    <article>
      <span>Workload</span>
      <strong>${state.workload}</strong>
    </article>
    <article>
      <span>Utility lane</span>
      <strong>${PROVIDER_REGISTRY[executor].name}</strong>
    </article>
  `;
}

function renderLanes(state, lead, reviewer, executor, memory) {
  const profile = WORKLOAD_PROFILES[state.workload];
  const lanes = [
    {
      title: 'Lane 1 · Intake and task normalization',
      body: `${PROVIDER_REGISTRY[lead].name} prepares the primary brief and ${profile.lanes[0]}.`
    },
    {
      title: 'Lane 2 · Review and synthesis',
      body: `${PROVIDER_REGISTRY[reviewer].name} pressure-tests the mission, ${profile.lanes[1]}, and applies the ${state.policy.toLowerCase()} profile.`
    },
    {
      title: 'Lane 3 · Execution and transforms',
      body: `${PROVIDER_REGISTRY[executor].name} handles bounded execution, ${profile.lanes[2]}, and packages the working artifacts.`
    },
    {
      title: 'Lane 4 · Continuity and publish readiness',
      body: `${PROVIDER_REGISTRY[memory].name} ${profile.lanes[3]} while preserving operator visibility.`
    }
  ];

  document.getElementById('mesh-lanes').innerHTML = lanes
    .map((lane) => `<li><strong>${lane.title}</strong>${lane.body}</li>`)
    .join('');
}

function renderFeatures(state) {
  const profile = POLICY_PROFILES[state.policy];
  document.getElementById('mesh-features').innerHTML = profile.features
    .map(([title, body]) => `<li><strong>${title}</strong>${body}</li>`)
    .join('');
}

function renderViewportDiagnostics() {
  document.body.dataset.viewportWidth = String(window.innerWidth);
  document.body.dataset.clientWidth = String(document.documentElement.clientWidth);
  document.body.dataset.scrollWidth = String(document.documentElement.scrollWidth);
  document.body.dataset.overflowDelta = String(
    document.documentElement.scrollWidth - document.documentElement.clientWidth
  );
}

function buildPlan(state, lead, reviewer, executor, memory) {
  const workloadProfile = WORKLOAD_PROFILES[state.workload];
  const policyProfile = POLICY_PROFILES[state.policy];
  const providers = providerNames(state.providers);
  const timestamp = new Date().toLocaleString();

  const lines = [
    '# FOCUS AI MODEL ORCHESTRA :: ROUTING PLAN',
    '',
    `Generated: ${timestamp}`,
    '',
    '## Mission',
    state.mission || 'Define the mission for this orchestration run before execution starts.',
    '',
    '## Active Provider Mesh',
    ...providers.map((name) => `- ${name}`),
    '',
    '## Control Posture',
    `- Workload: ${state.workload}`,
    `- Policy profile: ${state.policy}`,
    `- Lead lane: ${PROVIDER_REGISTRY[lead].name}`,
    `- Review lane: ${PROVIDER_REGISTRY[reviewer].name}`,
    `- Execution lane: ${PROVIDER_REGISTRY[executor].name}`,
    `- Continuity lane: ${PROVIDER_REGISTRY[memory].name}`,
    '',
    '## Operator Goal',
    `- Outcome target: ${workloadProfile.outcome}.`,
    `- Policy summary: ${policyProfile.summary}`,
    '',
    '## Routing Lanes',
    `1. Intake: ${PROVIDER_REGISTRY[lead].name} frames the mission and ${workloadProfile.lanes[0]}.`,
    `2. Review: ${PROVIDER_REGISTRY[reviewer].name} ${workloadProfile.lanes[1]}.`,
    `3. Execution: ${PROVIDER_REGISTRY[executor].name} ${workloadProfile.lanes[2]}.`,
    `4. Continuity: ${PROVIDER_REGISTRY[memory].name} ${workloadProfile.lanes[3]}.`,
    '',
    '## Policy Rules',
    ...policyProfile.rules.map((rule) => `- ${rule}`),
    '',
    '## Provider Assignments',
    ...state.providers.map((key) => {
      const provider = PROVIDER_REGISTRY[key];
      return `- ${provider.name}: ${provider.specialties.join(', ')}.`;
    }),
    '',
    '## UI Build Priorities',
    ...policyProfile.features.map(([title, body]) => `- ${title}: ${body}`),
    '',
    '## Admin Reminder',
    '- This platform is for controlled multi-model orchestration, not an unrestricted autonomous surface.',
    '- Keep approvals explicit before publish, deployment, credential changes, or external system actions.',
    '- Preserve the session memory so the next operator can continue without re-discovery.',
    '',
    '## Next Build Moves',
    '- Finish the provider registry and adapter configuration surface.',
    '- Connect this UI to a real orchestration backend and event log.',
    '- Attach artifact history, prompt packets, and QA evidence to each run.'
  ];

  return lines.join('\n');
}

function regenerateOutput() {
  const state = getState();
  const workload = WORKLOAD_PROFILES[state.workload];
  const lead = providerFor(state.providers, workload.preferredLead);
  const reviewer = secondaryReviewer(state.providers, lead);
  const executor = executionLane(state.providers, lead);
  const memory = memoryLane(state.providers, lead);

  renderSummary(state, lead, reviewer, executor);
  renderLanes(state, lead, reviewer, executor, memory);
  renderFeatures(state);
  document.getElementById('mesh-output').textContent = buildPlan(state, lead, reviewer, executor, memory);
  saveState();
}

function syncFromProviderInput() {
  const raw = document.getElementById('mesh-providers').value;
  const matched = Object.entries(PROVIDER_REGISTRY)
    .filter(([, provider]) => raw.toLowerCase().includes(provider.name.toLowerCase()))
    .map(([key]) => key);
  applyProviderSelection(matched);
  saveState();
}

function attachEvents() {
  providerCards().forEach((card) => {
    card.addEventListener('click', () => {
      const active = card.classList.contains('active');
      const selected = selectedProviderKeys();
      if (active && selected.length === 1) {
        return;
      }
      card.classList.toggle('active');
      syncProvidersInput();
      saveState();
    });
  });

  FIELD_IDS.forEach((id) => {
    const element = document.getElementById(id);
    const eventName = element.tagName === 'SELECT' ? 'change' : 'input';
    element.addEventListener(eventName, () => {
      if (id === 'mesh-providers') {
        syncFromProviderInput();
      } else {
        saveState();
      }
    });
  });

  document.getElementById('mesh-providers').addEventListener('blur', syncFromProviderInput);
  document.getElementById('mesh-generate').addEventListener('click', regenerateOutput);
  document.getElementById('mesh-copy').addEventListener('click', async () => {
    const button = document.getElementById('mesh-copy');
    await navigator.clipboard.writeText(document.getElementById('mesh-output').textContent);
    const previous = button.textContent;
    button.textContent = 'Copied Plan';
    window.setTimeout(() => {
      button.textContent = previous;
    }, 1400);
  });
}

function hydrate() {
  restoreState();
  attachEvents();
  renderFeatures({ policy: document.getElementById('mesh-policy').value });
  regenerateOutput();
  renderViewportDiagnostics();
}

window.addEventListener('resize', renderViewportDiagnostics);
hydrate();
