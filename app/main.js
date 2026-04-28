/**
 * @typedef {Object} Stage
 * @property {number} id
 * @property {string} name
 * @property {string} purpose
 * @property {string} output
 */

const ENGINE_CONFIG = {
  engineName: '11-Stage AI Engine',
  baseMode: {
    name: 'Sacred Geometry Foundation',
    directive:
      'Preserve harmony, coherence, recursion-awareness, and practical execution grounded in sacred geometry framing.'
  },
  stages: [
    { id: 1, name: 'Intent Alignment', purpose: 'Define mission and success criteria.', output: 'Mission statement' },
    { id: 2, name: 'Context Loading', purpose: 'Load history, constraints, and references.', output: 'Context map' },
    { id: 3, name: 'Pattern Recognition', purpose: 'Identify motifs and friction points.', output: 'Pattern summary' },
    { id: 4, name: 'Architecture Framing', purpose: 'Choose modular structure.', output: 'Architecture plan' },
    { id: 5, name: 'Prompt Engine Assembly', purpose: 'Build stage-aware prompt stack.', output: 'Prompt protocol' },
    { id: 6, name: 'Execution Planning', purpose: 'Set milestones and checkpoints.', output: 'Execution map' },
    { id: 7, name: 'Build & Integrate', purpose: 'Implement and integrate.', output: 'Working build' },
    { id: 8, name: 'Verification & QA', purpose: 'Validate behavior with checks.', output: 'QA report' },
    { id: 9, name: 'Refinement Loop', purpose: 'Improve quality and speed.', output: 'Refinement log' },
    { id: 10, name: 'Deployment & Distribution', purpose: 'Release with version integrity.', output: 'Release summary' },
    { id: 11, name: 'Daily Command Mode', purpose: 'Track continuity and next actions.', output: 'Daily protocol' }
  ]
};

const STORAGE_KEY = 'focus-eye-of-focus-platform-state';
const FIELD_IDS = ['mission', 'outcomes', 'constraints', 'tasks', 'lens', 'surface'];
const PRESETS = {
  launch: {
    mission: 'Ship the next live Focus AI release with cleaner routing, verified build quality, and a premium user-facing presentation.',
    outcomes: [
      'Update the highest-impact experience first.',
      'Run validation and deployment checks.',
      'Capture a clean changelog and next actions.'
    ].join('\n'),
    constraints: [
      'Do not break the live site while upgrading it.',
      'Preserve operator-safe workflows and clear rollback paths.',
      'Keep language customer-facing and decisive.'
    ].join('\n'),
    tasks: [
      'Refresh the public-facing UI.',
      'Run build, verification, and deployment commands.',
      'Document what changed and what remains.'
    ].join('\n'),
    lens: 'Launch orchestration',
    surface: 'Codex + GitHub + live site'
  },
  build: {
    mission: 'Implement the next engineering milestone cleanly and move it toward production readiness.',
    outcomes: [
      'Fix the highest-value code path.',
      'Run tests and targeted verification.',
      'Preserve code quality and maintainability.'
    ].join('\n'),
    constraints: [
      'Avoid regressions in unrelated flows.',
      'Respect existing architecture and user edits.',
      'Leave a clear handoff trail.'
    ].join('\n'),
    tasks: [
      'Patch source files.',
      'Run compile checks and tests.',
      'Summarize the result with file references.'
    ].join('\n'),
    lens: 'Engineering execution',
    surface: 'Local repo + validation suite'
  },
  storefront: {
    mission: 'Strengthen the storefront so the story, routing, and conversion path feel like one system.',
    outcomes: [
      'Improve first-impression hierarchy.',
      'Surface the right CTA and contact routing.',
      'Keep the offer ladder easy to scan.'
    ].join('\n'),
    constraints: [
      'Avoid generic card-grid design.',
      'Keep the visual language premium and readable.',
      'Protect mobile usability.'
    ].join('\n'),
    tasks: [
      'Refresh homepage hierarchy.',
      'Check live links and contact details.',
      'Rebuild public output and verify visually.'
    ].join('\n'),
    lens: 'Storefront conversion',
    surface: 'Static site + live deploy'
  },
  content: {
    mission: 'Produce clear content assets that can publish cleanly and support the larger system.',
    outcomes: [
      'Write conversion-ready copy.',
      'Preserve brand tone and structure.',
      'Prepare the next publish or campaign handoff.'
    ].join('\n'),
    constraints: [
      'No filler language.',
      'Keep the copy modular and reusable.',
      'Tie every section to an action or proof point.'
    ].join('\n'),
    tasks: [
      'Write the core content block.',
      'Refine the offer or CTA flow.',
      'Package the result for publishing.'
    ].join('\n'),
    lens: 'Content production',
    surface: 'Documents + publishing flow'
  }
};

function splitLines(value, fallback) {
  const lines = value
    .split('\n')
    .map((line) => line.trim())
    .filter(Boolean);
  return lines.length ? lines : fallback;
}

function getState() {
  return {
    mission: document.getElementById('mission').value.trim(),
    outcomes: document.getElementById('outcomes').value.trim(),
    constraints: document.getElementById('constraints').value.trim(),
    tasks: document.getElementById('tasks').value.trim(),
    lens: document.getElementById('lens').value.trim(),
    surface: document.getElementById('surface').value.trim()
  };
}

function saveState() {
  localStorage.setItem(STORAGE_KEY, JSON.stringify(getState()));
}

function restoreState() {
  const raw = localStorage.getItem(STORAGE_KEY);
  if (!raw) {
    return;
  }

  try {
    const state = JSON.parse(raw);
    FIELD_IDS.forEach((key) => {
      if (typeof state[key] === 'string') {
        document.getElementById(key).value = state[key];
      }
    });
  } catch (_error) {
    localStorage.removeItem(STORAGE_KEY);
  }
}

function appliedFocus(stageId, state, outcomes, constraints, tasks) {
  switch (stageId) {
    case 1:
      return `Lock the mission to "${state.mission || "today's primary objective"}" and define what completion actually looks like.`;
    case 2:
      return `Load the strongest context from the current outcomes (${outcomes[0]}) and hard constraints (${constraints[0]}).`;
    case 3:
      return `Watch for recurring friction across the active task cluster, starting with ${tasks[0]}.`;
    case 4:
      return `Choose the simplest structure that serves the ${state.lens || 'current operating lens'} cleanly.`;
    case 5:
      return 'Assemble one reusable brief instead of scattering guidance across multiple one-off prompts.';
    case 6:
      return `Sequence the work into checkpoints around ${tasks.slice(0, 2).join(' and ')}.`;
    case 7:
      return 'Build the highest-value artifact first, then integrate it into the surrounding system.';
    case 8:
      return 'Check behavior, links, language, and real-world usability before calling the work finished.';
    case 9:
      return 'Refine only the changes that materially improve clarity, trust, conversion, or speed.';
    case 10:
      return `Prepare the result for release through ${state.surface || 'the chosen delivery surface'} with version confidence.`;
    case 11:
      return 'Capture the next actions and preserve continuity for the next operator session.';
    default:
      return 'Apply disciplined execution.';
  }
}

/**
 * Render the stage rail based on engine config.
 * @param {boolean} activePreset 
 */
function renderStageRail(activePreset) {
  const rail = document.getElementById('stage-list');
  rail.innerHTML = '';
  ENGINE_CONFIG.stages.forEach((stage) => {
    const item = document.createElement('li');
    if (activePreset) {
      item.classList.add('active');
    }
    item.innerHTML = `
      <div>
        <span class="stage-index">${stage.id}</span>
        <span class="stage-name">${stage.name}</span>
      </div>
      <div class="stage-purpose">${stage.purpose}</div>
    `;
    rail.appendChild(item);
  });
}

function updateSummary(state) {
  const outcomes = splitLines(state.outcomes, []);
  const constraints = splitLines(state.constraints, []);
  const tasks = splitLines(state.tasks, []);

  document.getElementById('mission-state').textContent = state.mission ? 'Locked' : 'Not set';
  document.getElementById('outcome-count').textContent = String(outcomes.length);
  document.getElementById('task-count').textContent = String(tasks.length);
  document.getElementById('surface-state').textContent = state.surface || 'Not set';

  document.getElementById('session-summary').innerHTML = `
    <article>
      <span>Focus Lens</span>
      <strong>${state.lens || 'Not set'}</strong>
    </article>
    <article>
      <span>Constraints</span>
      <strong>${constraints.length} tracked</strong>
    </article>
    <article>
      <span>Session State</span>
      <strong>${state.mission ? 'Ready to generate' : 'Awaiting mission'}</strong>
    </article>
  `;
}

function buildBrief() {
  const state = getState();
  const outcomes = splitLines(state.outcomes, ['Ship one clear result']);
  const constraints = splitLines(state.constraints, ['Protect quality and avoid hidden risk']);
  const tasks = splitLines(state.tasks, ['Choose the next concrete task']);
  const timestamp = new Date().toLocaleString();

  const lines = [
    '# THE EYE OF FOCUS :: COMMAND PLATFORM BRIEF',
    '',
    `Generated: ${timestamp}`,
    '',
    '## Operating Frame',
    `- Engine: ${ENGINE_CONFIG.engineName}`,
    `- Base Mode: ${ENGINE_CONFIG.baseMode.name}`,
    `- Directive: ${ENGINE_CONFIG.baseMode.directive}`,
    `- Focus Lens: ${state.lens || 'Not set'}`,
    `- Delivery Surface: ${state.surface || 'Not set'}`,
    '',
    '## Mission',
    state.mission || 'Define the mission before work begins.',
    '',
    '## Outcome Stack',
    ...outcomes.map((item) => `- ${item}`),
    '',
    '## Constraints',
    ...constraints.map((item) => `- ${item}`),
    '',
    '## Task Cluster',
    ...tasks.map((item) => `- ${item}`),
    '',
    '## 11 Stages'
  ];

  ENGINE_CONFIG.stages.forEach((stage) => {
    lines.push(`### Stage ${stage.id}: ${stage.name}`);
    lines.push(`- Purpose: ${stage.purpose}`);
    lines.push(`- Applied focus: ${appliedFocus(stage.id, state, outcomes, constraints, tasks)}`);
    lines.push(`- Output target: ${stage.output}`);
    lines.push('');
  });

  lines.push('## Master Operator Prompt');
  lines.push(
    `Operate as ${ENGINE_CONFIG.engineName} under the ${ENGINE_CONFIG.baseMode.name}. Use the mission, outcomes, constraints, task cluster, focus lens, and delivery surface above to execute with clarity, sequence, and measurable completion.`
  );
  lines.push('');
  lines.push('## Carry Forward');
  lines.push('- Preserve the strongest decisions.');
  lines.push('- Record unresolved blockers.');
  lines.push('- Name the next concrete move for the next session.');

  return lines.join('\n');
}

function markGeneratedStages() {
  document.querySelectorAll('#stage-list li').forEach((item) => {
    item.classList.remove('active');
    item.classList.add('complete');
  });
}

function applyPreset(name) {
  const preset = PRESETS[name];
  if (!preset) {
    return;
  }

  FIELD_IDS.forEach((id) => {
    if (typeof preset[id] === 'string') {
      document.getElementById(id).value = preset[id];
    }
  });

  document.querySelectorAll('.preset-button').forEach((button) => {
    button.classList.toggle('active', button.dataset.preset === name);
  });

  saveState();
  updateSummary(getState());
  renderStageRail(true);
}

function resetSession() {
  FIELD_IDS.forEach((id) => {
    const element = document.getElementById(id);
    if (element.tagName === 'SELECT') {
      element.selectedIndex = 0;
    } else if (id === 'surface') {
      element.value = 'Codex + GitHub + live site';
    } else {
      element.value = '';
    }
  });
  document.getElementById('output').textContent = 'Generate the brief to populate the 11-stage packet.';
  document.querySelectorAll('.preset-button').forEach((button) => button.classList.remove('active'));
  renderStageRail(false);
  updateSummary(getState());
  saveState();
}

function downloadBrief() {
  const text = document.getElementById('output').textContent.trim();
  if (!text) {
    return;
  }

  const blob = new Blob([text], { type: 'text/markdown;charset=utf-8' });
  const url = URL.createObjectURL(blob);
  const link = document.createElement('a');
  link.href = url;
  link.download = 'focus-ai-command-brief.md';
  document.body.appendChild(link);
  link.click();
  link.remove();
  URL.revokeObjectURL(url);
}

document.getElementById('generate').addEventListener('click', () => {
  saveState();
  const state = getState();
  document.getElementById('output').textContent = buildBrief();
  updateSummary(state);
  markGeneratedStages();
});

document.getElementById('copy').addEventListener('click', async () => {
  const text = document.getElementById('output').textContent.trim();
  if (!text) {
    return;
  }

  await navigator.clipboard.writeText(text);
  const button = document.getElementById('copy');
  const original = button.textContent;
  button.textContent = 'Copied';
  setTimeout(() => {
    button.textContent = original;
  }, 1400);
});

document.getElementById('download').addEventListener('click', downloadBrief);
document.getElementById('reset').addEventListener('click', resetSession);

document.querySelectorAll('.preset-button').forEach((button) => {
  button.addEventListener('click', () => applyPreset(button.dataset.preset));
});

FIELD_IDS.forEach((id) => {
  document.getElementById(id).addEventListener('input', () => {
    saveState();
    updateSummary(getState());
  });
  document.getElementById(id).addEventListener('change', () => {
    saveState();
    updateSummary(getState());
  });
});

renderStageRail(false);
restoreState();
updateSummary(getState());
