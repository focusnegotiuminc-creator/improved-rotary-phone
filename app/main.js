const ENGINE_CONFIG = {
  engineName: '11-Stage AI Engine',
  baseMode: {
    name: 'Sacred Geometry Foundation',
    directive:
      'All outputs should preserve harmony, coherence, recursion-awareness, and practical execution grounded in sacred geometry framing.'
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

const STORAGE_KEY = 'focus-eye-of-focus-state';

function splitLines(value, fallback) {
  const lines = value
    .split('\n')
    .map((line) => line.trim())
    .filter(Boolean);
  return lines.length ? lines : fallback;
}

function saveState() {
  const state = {
    mission: document.getElementById('mission').value,
    outcomes: document.getElementById('outcomes').value,
    constraints: document.getElementById('constraints').value,
    tasks: document.getElementById('tasks').value
  };
  localStorage.setItem(STORAGE_KEY, JSON.stringify(state));
}

function restoreState() {
  const raw = localStorage.getItem(STORAGE_KEY);
  if (!raw) {
    return;
  }

  try {
    const state = JSON.parse(raw);
    ['mission', 'outcomes', 'constraints', 'tasks'].forEach((key) => {
      if (typeof state[key] === 'string') {
        document.getElementById(key).value = state[key];
      }
    });
  } catch (_error) {
    localStorage.removeItem(STORAGE_KEY);
  }
}

function appliedFocus(stageId, state) {
  const outcomes = splitLines(state.outcomes, ['Ship one meaningful result']);
  const constraints = splitLines(state.constraints, ['Protect time, quality, and clarity']);
  const tasks = splitLines(state.tasks, ['Define the next concrete task']);

  switch (stageId) {
    case 1:
      return `Lock the mission to "${state.mission || "today's primary objective"}" and define success in practical terms.`;
    case 2:
      return `Load the most relevant context from current outcomes (${outcomes[0]}) and current constraints (${constraints[0]}).`;
    case 3:
      return `Watch for recurring friction across the active task cluster, starting with ${tasks[0]}.`;
    case 4:
      return 'Choose the simplest architecture that still supports execution, review, and handoff.';
    case 5:
      return 'Assemble a reusable prompt or operating brief instead of a one-off burst of effort.';
    case 6:
      return `Sequence the work into checkpoints around ${tasks.slice(0, 2).join(' and ')}.`;
    case 7:
      return 'Build the highest-value artifact first, then integrate it into the existing system.';
    case 8:
      return 'Check behavior, links, language, and real-world usability before calling the work finished.';
    case 9:
      return 'Refine only the areas that materially improve clarity, quality, or conversion.';
    case 10:
      return 'Prepare the result for publication, deployment, or handoff with version confidence.';
    case 11:
      return 'Capture the next actions and preserve continuity for the next session.';
    default:
      return 'Apply disciplined execution.';
  }
}

function buildBrief() {
  const state = {
    mission: document.getElementById('mission').value.trim(),
    outcomes: document.getElementById('outcomes').value.trim(),
    constraints: document.getElementById('constraints').value.trim(),
    tasks: document.getElementById('tasks').value.trim()
  };
  const outcomes = splitLines(state.outcomes, ['Ship one clear result']);
  const constraints = splitLines(state.constraints, ['Protect quality and do not create hidden risk']);
  const tasks = splitLines(state.tasks, ['Choose the next concrete task']);
  const timestamp = new Date().toLocaleString();

  const lines = [
    '# THE EYE OF FOCUS :: DAILY COMMAND BRIEF',
    '',
    `Generated: ${timestamp}`,
    '',
    '## Operating Frame',
    `- Engine: ${ENGINE_CONFIG.engineName}`,
    `Base Mode: ${ENGINE_CONFIG.baseMode.name}`,
    `Directive: ${ENGINE_CONFIG.baseMode.directive}`,
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
    lines.push(`- Applied focus: ${appliedFocus(stage.id, state)}`);
    lines.push(`- Output target: ${stage.output}`);
    lines.push('');
  });

  lines.push('## Master Operator Prompt');
  lines.push(
    `Operate as ${ENGINE_CONFIG.engineName} under the ${ENGINE_CONFIG.baseMode.name}. Use the mission, outcomes, constraints, and task cluster above to execute with clarity, sequence, and measurable completion.`
  );
  lines.push('');
  lines.push('## Carry Forward');
  lines.push('- Preserve the strongest decisions.');
  lines.push('- Record unresolved blockers.');
  lines.push('- Name the very next concrete move for the next session.');

  return lines.join('\n');
}

document.getElementById('generate').addEventListener('click', () => {
  saveState();
  const output = buildBrief();
  document.getElementById('output').textContent = output;
});

document.getElementById('copy').addEventListener('click', async () => {
  const text = document.getElementById('output').textContent;
  if (!text.trim()) {
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

['mission', 'outcomes', 'constraints', 'tasks'].forEach((id) => {
  document.getElementById(id).addEventListener('input', saveState);
});

restoreState();
