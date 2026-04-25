const PRIVATE_STORAGE_KEY = 'focus-private-operations-console-state';
const DEFAULT_OUTPUT = 'Generate the private runbook to populate this panel.';

const BUSINESS_PROFILES = {
  'focus-negotium': {
    name: 'Focus Negotium Inc',
    role: 'Parent company',
    lanes: [
      'Holdings, entity support, governance coordination, and executive operating design',
      'Real estate development, property operations, and portfolio planning',
      'Websites, Stripe storefronts, client portals, and commercial infrastructure'
    ]
  },
  'focus-records': {
    name: 'Focus Records LLC',
    role: 'Affiliate media company',
    lanes: [
      'Release planning, rollout calendars, and catalog packaging',
      'Cover art direction, Firefly-ready campaign boards, and promo systems',
      'Beat-store planning, licensing pages, and media-commerce positioning'
    ]
  },
  'royal-lee-construction': {
    name: 'Royal Lee Construction Solutions LLC',
    role: 'Affiliate construction company',
    lanes: [
      'Sacred-geometry concept studies and presentation-grade owner packets',
      'Development planning, site logic, and preconstruction scope framing',
      'Renovation strategy, owner representation, and build coordination prep'
    ]
  }
};

const WORKFLOW_PROFILES = {
  'Website Design and Deployment': {
    outcome: 'ship a polished customer-facing website update with verified routing and mobile behavior',
    steps: [
      'Audit the current page structure, pricing, and routing.',
      'Write or revise the public copy and sector-specific service details.',
      'Build, verify, and deploy the updated site with rollback awareness.'
    ]
  },
  'Storefront and Stripe Offers': {
    outcome: 'align pricing, offer copy, Stripe links, and the storefront hierarchy',
    steps: [
      'Verify the product ladder and the service ladder are saying the same thing.',
      'Update checkout links, CTA copy, and offer packaging.',
      'Validate customer-facing pages, prices, and payment routing.'
    ]
  },
  'Real Estate Development Packet': {
    outcome: 'assemble a decision-ready property or development packet',
    steps: [
      'Clarify site context, ownership goals, and decision horizon.',
      'Package concept studies, notes, assumptions, and next-stage deliverables.',
      'Prepare an owner-facing summary that can move into review or execution.'
    ]
  },
  'Property Management Setup': {
    outcome: 'stand up a usable management workflow with clear routing and reporting',
    steps: [
      'Map communications, maintenance flow, records, and owner updates.',
      'Design the intake, vendor, and document structure.',
      'Prepare rollout notes and a handoff sequence for day-one use.'
    ]
  },
  'Release Campaign and Media Packaging': {
    outcome: 'ship a cohesive media package with launch direction and branded assets',
    steps: [
      'Define the release story, audience, and visual direction.',
      'Package campaign assets, rollout notes, and storefront language.',
      'Prepare the catalog or licensing pathway for launch.'
    ]
  },
  'Client Intake and Service Routing': {
    outcome: 'normalize a client request into a clean service path and execution brief',
    steps: [
      'Clarify the lead, budget, need, and best-fit company lane.',
      'Translate the conversation into a service recommendation and scoped next step.',
      'Prepare the booking, follow-up, and delivery handoff.'
    ]
  }
};

const INTEGRATION_DETAILS = {
  github: 'Branch work, releases, deployments, and implementation tracking.',
  stripe: 'Secure checkout links, pricing ladders, and product or service payment routing.',
  adobe: 'Creative direction, PDF packets, visual studies, and production-ready branded assets.',
  figma: 'Layout planning, interface references, and design-system translation.',
  airtable: 'Structured operating data, client records, and service inventory.',
  media: 'Campaign resizing, video prep, and future beat-catalog packaging.'
};

function businessCards() {
  return Array.from(document.querySelectorAll('.business-card'));
}

function integrationCards() {
  return Array.from(document.querySelectorAll('.integration-card'));
}

function selectedBusiness() {
  return businessCards().find((card) => card.classList.contains('active'))?.dataset.business || 'focus-negotium';
}

function selectedIntegrations() {
  return integrationCards()
    .filter((card) => card.classList.contains('active'))
    .map((card) => card.dataset.integration);
}

function getState() {
  return {
    business: selectedBusiness(),
    integrations: selectedIntegrations(),
    workflow: document.getElementById('workflow').value,
    mission: document.getElementById('mission').value.trim(),
    deliverables: document.getElementById('deliverables').value.trim(),
    constraints: document.getElementById('constraints').value.trim(),
    context: document.getElementById('context').value.trim()
  };
}

function saveState() {
  localStorage.setItem(PRIVATE_STORAGE_KEY, JSON.stringify(getState()));
}

function applyBusinessSelection(businessKey) {
  businessCards().forEach((card) => {
    card.classList.toggle('active', card.dataset.business === businessKey);
  });
}

function applyIntegrationSelection(keys) {
  const selected = new Set(keys);
  integrationCards().forEach((card) => {
    card.classList.toggle('active', selected.has(card.dataset.integration));
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
    ['workflow', 'mission', 'deliverables', 'constraints', 'context'].forEach((id) => {
      if (typeof state[id] === 'string') {
        document.getElementById(id).value = state[id];
      }
    });
  } catch (_error) {
    localStorage.removeItem(PRIVATE_STORAGE_KEY);
  }
}

function lines(value, fallback) {
  const parsed = value
    .split('\n')
    .map((line) => line.trim())
    .filter(Boolean);
  return parsed.length ? parsed : fallback;
}

function updateSummary(state) {
  const business = BUSINESS_PROFILES[state.business];
  const integrations = state.integrations.length ? state.integrations : ['github'];
  const deliverables = lines(state.deliverables, []);
  const constraints = lines(state.constraints, []);

  document.getElementById('summary-grid').innerHTML = `
    <article>
      <span>Business lane</span>
      <strong>${business.name}</strong>
    </article>
    <article>
      <span>Workflow</span>
      <strong>${state.workflow}</strong>
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
    <article>
      <span>Execution posture</span>
      <strong>Private / operator reviewed</strong>
    </article>
  `;
}

function buildRunbook() {
  const state = getState();
  const business = BUSINESS_PROFILES[state.business];
  const workflow = WORKFLOW_PROFILES[state.workflow];
  const deliverables = lines(state.deliverables, ['Define the first deliverable before execution starts.']);
  const constraints = lines(state.constraints, ['Protect live quality, keep the workflow reviewable, and preserve rollback safety.']);
  const context = lines(state.context, ['Attach source files, live URLs, or notes before execution.']);
  const integrations = state.integrations.length ? state.integrations : ['github'];
  const timestamp = new Date().toLocaleString();

  const linesOut = [
    '# FOCUS PRIVATE OPERATIONS CONSOLE :: RUNBOOK',
    '',
    `Generated: ${timestamp}`,
    '',
    '## Mission',
    state.mission || 'Define the mission for this private run before execution begins.',
    '',
    '## Business Lane',
    `- ${business.name} (${business.role})`,
    ...business.lanes.map((lane) => `- ${lane}`),
    '',
    '## Workflow Type',
    `- ${state.workflow}`,
    `- Target outcome: ${workflow.outcome}`,
    '',
    '## Deliverables',
    ...deliverables.map((item) => `- ${item}`),
    '',
    '## Constraints',
    ...constraints.map((item) => `- ${item}`),
    '',
    '## Source Context',
    ...context.map((item) => `- ${item}`),
    '',
    '## Integration Lanes',
    ...integrations.map((key) => `- ${key}: ${INTEGRATION_DETAILS[key]}`),
    '',
    '## Execution Sequence',
    ...workflow.steps.map((step, index) => `${index + 1}. ${step}`),
    '',
    '## Operator Checks',
    '- Confirm the selected business lane matches the public-facing company or the internal project owner.',
    '- Confirm any public site work remains customer-facing and does not expose internal systems.',
    '- Confirm pricing, routing, and storefront links before publish or deploy.',
    '- Capture the final output, live checks, and next actions before closing the run.',
    '',
    '## Handoff Note',
    'Use this runbook as the input packet for the next private execution tool, code workspace, or operator session.'
  ];

  updateSummary(state);
  return linesOut.join('\n');
}

function renderRunbook() {
  const output = buildRunbook();
  document.getElementById('output').textContent = output;
  saveState();
}

function bindCards() {
  businessCards().forEach((card) => {
    card.addEventListener('click', () => {
      applyBusinessSelection(card.dataset.business);
      renderRunbook();
    });
  });

  integrationCards().forEach((card) => {
    card.addEventListener('click', () => {
      card.classList.toggle('active');
      renderRunbook();
    });
  });
}

function bindInputs() {
  ['workflow', 'mission', 'deliverables', 'constraints', 'context'].forEach((id) => {
    document.getElementById(id).addEventListener('input', renderRunbook);
    document.getElementById(id).addEventListener('change', renderRunbook);
  });

  document.getElementById('generate').addEventListener('click', renderRunbook);
  document.getElementById('reset').addEventListener('click', () => {
    localStorage.removeItem(PRIVATE_STORAGE_KEY);
    document.getElementById('workflow').value = 'Website Design and Deployment';
    document.getElementById('mission').value = '';
    document.getElementById('deliverables').value = '';
    document.getElementById('constraints').value = '';
    document.getElementById('context').value = '';
    applyBusinessSelection('focus-negotium');
    applyIntegrationSelection(['github', 'stripe', 'adobe']);
    document.getElementById('output').textContent = DEFAULT_OUTPUT;
    updateSummary(getState());
  });

  document.getElementById('copy').addEventListener('click', async () => {
    await navigator.clipboard.writeText(document.getElementById('output').textContent);
  });

  document.getElementById('download').addEventListener('click', () => {
    const blob = new Blob([document.getElementById('output').textContent], { type: 'text/markdown' });
    const link = document.createElement('a');
    link.href = URL.createObjectURL(blob);
    link.download = 'focus-private-runbook.md';
    link.click();
    URL.revokeObjectURL(link.href);
  });
}

restoreState();
applyBusinessSelection(selectedBusiness());
if (!selectedIntegrations().length) {
  applyIntegrationSelection(['github', 'stripe', 'adobe']);
}
bindCards();
bindInputs();
updateSummary(getState());
