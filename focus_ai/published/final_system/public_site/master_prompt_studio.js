const ENGINE_PROFILES = {
  research: {
    label: 'Research Engine',
    focus: 'verified research, synthesis, constraints, and next-best actions'
  },
  claims: {
    label: 'Claims Engine',
    focus: 'claim extraction, verification paths, evidence priorities, and rebuttal logic'
  },
  writing: {
    label: 'Writing Engine',
    focus: 'clear writing, structured drafts, and conversion-grade messaging'
  },
  geometry: {
    label: 'Geometry Engine',
    focus: 'layout logic, dimensional framing, and spatial design structure'
  },
  construction: {
    label: 'Construction Engine',
    focus: 'execution planning, sequencing, dependencies, and field risk'
  },
  compliance: {
    label: 'Compliance Engine',
    focus: 'guardrails, approvals, risk notes, and safe execution steps'
  },
  frequency: {
    label: 'Frequency Engine',
    focus: 'cadence design, attention management, and execution rhythm'
  },
  marketing: {
    label: 'Marketing Engine',
    focus: 'offer framing, channel strategy, message architecture, and KPIs'
  },
  ai_twin: {
    label: 'AI Twin Video Engine',
    focus: 'avatar strategy, scene prompts, voiceover direction, and distribution cutdowns'
  },
  publish: {
    label: 'Publishing Engine',
    focus: 'release packaging, launch surfaces, repo readiness, and handoff'
  },
  automation: {
    label: 'Automation Engine',
    focus: 'workflow routing, webhook handoff, and system continuation'
  }
};

function pickPrimaryEngine(task) {
  const text = task.toLowerCase();
  if (/claim|fact check|evidence|verify/.test(text)) return 'claims';
  if (/geometry|floor|plan|layout|sacred/.test(text)) return 'geometry';
  if (/build|construction|timeline|estimate|scope|bid/.test(text)) return 'construction';
  if (/compliance|legal|policy|payroll|insurance|license/.test(text)) return 'compliance';
  if (/cadence|focus|routine|habit|schedule/.test(text)) return 'frequency';
  if (/market|campaign|funnel|launch|offer|shop|sales/.test(text)) return 'marketing';
  if (/video|avatar|ai twin|voiceover|scene|reel|short-form/.test(text)) return 'ai_twin';
  if (/publish|release|book|library|deploy live/.test(text)) return 'publish';
  if (/automate|workflow|make|replit|connector|api|trigger/.test(text)) return 'automation';
  if (/research|analyze|investigate|study/.test(text)) return 'research';
  return 'writing';
}

function buildSequence(task, primary) {
  const text = task.toLowerCase();
  let sequence;

  if (/full system|master machine|power house|merge apps|combine apps/.test(text)) {
    sequence = ['research', 'claims', 'writing', 'geometry', 'construction', 'compliance', 'marketing', 'publish', 'automation'];
  } else {
    const defaults = {
      research: ['research', 'writing', 'automation'],
      claims: ['research', 'claims', 'writing', 'automation'],
      writing: ['research', 'writing', 'automation'],
      geometry: ['research', 'geometry', 'construction', 'automation'],
      construction: ['research', 'geometry', 'construction', 'writing', 'automation'],
      compliance: ['research', 'claims', 'compliance', 'automation'],
      frequency: ['research', 'frequency', 'automation'],
      marketing: ['research', 'writing', 'marketing', 'publish', 'automation'],
      ai_twin: ['research', 'writing', 'ai_twin', 'marketing', 'automation'],
      publish: ['research', 'writing', 'publish', 'automation'],
      automation: ['research', 'writing', 'automation']
    };
    sequence = defaults[primary] || defaults.writing;
  }

  if (/video|avatar|ai twin|voiceover|scene|reel|short-form/.test(text) && !sequence.includes('ai_twin')) {
    sequence.splice(Math.max(sequence.length - 1, 1), 0, 'ai_twin');
  }

  return [...new Set(sequence)];
}

function connectorTargets(sequence) {
  const targets = ['Local prompt compiler', 'OpenAI reasoning core (if configured)'];
  if (sequence.includes('automation')) {
    targets.push('Make automation webhook');
    targets.push('Replit remote runner');
  }
  if (sequence.includes('publish')) {
    targets.push('GitHub publishing surface');
  }
  if (sequence.includes('ai_twin')) {
    targets.push('AI twin video stack');
  }
  return targets;
}

function actionChecklist(task, primary) {
  return [
    `Normalize the request around the ${ENGINE_PROFILES[primary].label}.`,
    'Expand the task into deliverables, risks, connectors, and the strongest next actions.',
    'Generate a reusable prompt packet instead of a one-off completion.',
    `Keep the output practical for "${task.trim() || 'the user task'}".`
  ];
}

function twinStack() {
  return [
    'Avatar performance brief for HeyGen, Tavus, or a local recording workflow',
    'Scene prompts for Runway, Sora, or image-to-video tools',
    'Edit and caption pass for CapCut or DaVinci Resolve'
  ];
}

function compilePacket(task) {
  const cleanedTask = task.trim();
  const primary = pickPrimaryEngine(cleanedTask || 'general writing support');
  const sequence = buildSequence(cleanedTask, primary);
  const connectors = connectorTargets(sequence);
  const includesTwin = sequence.includes('ai_twin');
  const checklist = actionChecklist(cleanedTask, primary);

  const masterPrompt = [
    'You are FOCUS MASTER AI, a high-quality execution machine.',
    '',
    `User task: ${cleanedTask || 'Turn a rough task into a refined execution brief.'}`,
    `Primary engine: ${ENGINE_PROFILES[primary].label}`,
    `Primary focus: ${ENGINE_PROFILES[primary].focus}`,
    `Engine chain: ${sequence.map((key) => ENGINE_PROFILES[key].label).join(' -> ')}`,
    '',
    'Required deliverables:',
    '- premium execution-ready brief',
    '- stronger prompt packet',
    '- automation-ready next actions',
    includesTwin ? '- AI twin storyboard and distribution guidance' : '- optional AI twin extension when useful',
    '',
    'Experience goals:',
    '- Keep the output high signal and immediately usable.',
    '- Prefer free or low-cost tools and repeatable workflows.',
    '- Preserve spiritual clarity without losing business precision.',
    '',
    'Connector context:',
    ...connectors.map((item) => `- ${item}`),
    '',
    'Execution checklist:',
    ...checklist.map((item) => `- ${item}`)
  ].join('\n');

  return {
    task: cleanedTask,
    primary,
    sequence,
    connectors,
    includesTwin,
    checklist,
    masterPrompt
  };
}

function renderPacket(packet) {
  const header = [
    '# FOCUS MASTER AI :: Prompt Packet',
    '',
    `Task: ${packet.task || 'Turn the next task into a stronger execution packet.'}`,
    `Primary engine: ${ENGINE_PROFILES[packet.primary].label}`,
    `Engine chain: ${packet.sequence.map((key) => ENGINE_PROFILES[key].label).join(' -> ')}`,
    ''
  ];

  const connectorBlock = [
    '## Connectors',
    ...packet.connectors.map((item) => `- ${item}`),
    ''
  ];

  const twinBlock = packet.includesTwin
    ? [
        '## AI Twin Stack',
        ...twinStack().map((item) => `- ${item}`),
        ''
      ]
    : [];

  return [
    ...header,
    '## Master Prompt',
    packet.masterPrompt,
    '',
    '## Action Checklist',
    ...packet.checklist.map((item) => `- ${item}`),
    '',
    ...connectorBlock,
    ...twinBlock,
    '## Immediate Next Move',
    '- Paste the master prompt into your preferred AI engine or keep refining it for your current workflow.'
  ].join('\n');
}

function wirePromptStudio() {
  const input = document.getElementById('studio-task');
  const output = document.getElementById('studio-output');
  const summary = document.getElementById('studio-summary');
  const generate = document.getElementById('studio-generate');
  const copy = document.getElementById('studio-copy');
  const download = document.getElementById('studio-download');

  if (!input || !output || !summary || !generate || !copy || !download) {
    return;
  }

  function compileAndRender() {
    const packet = compilePacket(input.value);
    output.textContent = renderPacket(packet);
    summary.innerHTML = `
      <strong>${ENGINE_PROFILES[packet.primary].label}</strong>
      <span>Engine chain: ${packet.sequence.map((key) => ENGINE_PROFILES[key].label).join(' -> ')}</span>
      <span>AI twin layer: ${packet.includesTwin ? 'included' : 'optional'}</span>
    `;
  }

  generate.addEventListener('click', compileAndRender);

  copy.addEventListener('click', async () => {
    if (!output.textContent.trim()) {
      compileAndRender();
    }
    await navigator.clipboard.writeText(output.textContent);
    const original = copy.textContent;
    copy.textContent = 'Copied';
    setTimeout(() => {
      copy.textContent = original;
    }, 1400);
  });

  download.addEventListener('click', () => {
    if (!output.textContent.trim()) {
      compileAndRender();
    }
    const blob = new Blob([output.textContent], { type: 'text/markdown;charset=utf-8' });
    const href = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = href;
    link.download = 'focus-master-prompt-packet.md';
    document.body.appendChild(link);
    link.click();
    link.remove();
    URL.revokeObjectURL(href);
  });

  compileAndRender();
}

document.addEventListener('DOMContentLoaded', wirePromptStudio);
