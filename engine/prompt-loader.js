const fs = require('fs');
const path = require('path');

function loadEngineConfig(filePath = path.join(__dirname, 'stages.json')) {
  const raw = fs.readFileSync(filePath, 'utf8');
  const parsed = JSON.parse(raw);

  validateEngineConfig(parsed);
  return parsed;
}

function validateEngineConfig(config) {
  if (!config || typeof config !== 'object') {
    throw new Error('Invalid engine config: expected object.');
  }

  if (!Array.isArray(config.stages)) {
    throw new Error('Invalid engine config: stages must be an array.');
  }

  if (config.stages.length !== 11) {
    throw new Error(`Invalid engine config: expected 11 stages, found ${config.stages.length}.`);
  }

  for (const stage of config.stages) {
    if (typeof stage.id !== 'number' || !stage.name || !stage.purpose) {
      throw new Error(`Invalid stage definition: ${JSON.stringify(stage)}`);
    }
  }
}

function buildDailyBrief({ mission, outcomes, constraints, tasks }) {
  const config = loadEngineConfig();

  const header = [
    `# ${config.engineName} :: THE EYE OF FOCUS`,
    '',
    `**Base Mode:** ${config.baseMode.name}`,
    `**Directive:** ${config.baseMode.directive}`,
    '',
    '## Mission',
    mission || 'Define the mission for this session.',
    '',
    '## Desired Outcomes',
    outcomes || '- Outcome 1\n- Outcome 2',
    '',
    '## Constraints',
    constraints || '- Time\n- Scope\n- Dependencies',
    '',
    '## Tasks',
    tasks || '- Build\n- Verify\n- Deliver',
    '',
    '## 11-Stage Execution Sequence'
  ];

  const stageLines = config.stages.flatMap((stage) => [
    `### Stage ${stage.id}: ${stage.name}`,
    `- Purpose: ${stage.purpose}`,
    `- Expected Output: ${stage.output}`,
    ''
  ]);

  return [...header, ...stageLines].join('\n');
}

module.exports = {
  loadEngineConfig,
  validateEngineConfig,
  buildDailyBrief
};

if (require.main === module) {
  const brief = buildDailyBrief({
    mission: 'Launch focused development session with sacred geometry-based cognition.',
    outcomes: '- Clean implementation\n- Verified behavior\n- Organized delivery',
    constraints: '- Keep scope focused\n- Maintain modular structure',
    tasks: '- Load engine\n- Execute planned coding tasks\n- Publish output'
  });

  console.log(brief);
}
