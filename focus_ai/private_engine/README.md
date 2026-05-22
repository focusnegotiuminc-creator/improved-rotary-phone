# Focus Private AI Engine

This package is the executable starter layer for a Focus-owned AI command center.

It is designed for:

- Hugging Face model/code pulling.
- Local/open-model and endpoint model routing.
- OpenAI-like builder lane + Claude-like critic lane debate.
- Business-aware routing for Focus Negotium Inc, Focus Records LLC, Royal Lee Construction Solutions LLC, Flux & Crave, The Focus Corporation, and partner lanes.
- Human approval before high-impact external actions.

## Key files

- `config/hf_model_registry.json` — recommended Hugging Face models and download profiles.
- `config/agent_board.json` — multi-agent board definition.
- `hf_pull.py` — safe model metadata/weights pull helper.
- `orchestrator.py` — prompt/debate/run packet generator with optional OpenAI-compatible endpoint support.

## Important boundary

This is not a stolen or guardrail-stripped copy of OpenAI or Claude. It is a Focus-owned orchestration layer that can use open models and provider APIs in separate lanes.
