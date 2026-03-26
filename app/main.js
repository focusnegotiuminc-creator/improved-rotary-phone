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

function buildBrief() {
  const mission = document.getElementById('mission').value.trim();
  const outcomes = document.getElementById('outcomes').value.trim();
  const constraints = document.getElementById('constraints').value.trim();
  const tasks = document.getElementById('tasks').value.trim();

  const lines = [
    `# ${ENGINE_CONFIG.engineName} :: THE EYE OF FOCUS`,
    '',
    `Base Mode: ${ENGINE_CONFIG.baseMode.name}`,
    `Directive: ${ENGINE_CONFIG.baseMode.directive}`,
    '',
    '## Mission',
    mission || 'Define mission',
    '',
    '## Outcomes',
    outcomes || '- Outcome 1',
    '',
    '## Constraints',
    constraints || '- Constraint 1',
    '',
    '## Tasks',
    tasks || '- Task 1',
    '',
    '## 11 Stages'
  ];

  ENGINE_CONFIG.stages.forEach((stage) => {
    lines.push(`### Stage ${stage.id}: ${stage.name}`);
    lines.push(`- Purpose: ${stage.purpose}`);
    lines.push(`- Output: ${stage.output}`);
    lines.push('');
  });

  return lines.join('\n');
}

document.getElementById('generate').addEventListener('click', () => {
  const output = buildBrief();
  document.getElementById('output').textContent = output;
});

document.getElementById('copy').addEventListener('click', async () => {
  const text = document.getElementById('output').textContent;
  if (!text.trim()) {
    return;
  }

  await navigator.clipboard.writeText(text);
});
