# Focus--Master Merge Reference (Single-Operator Runtime)

## Purpose
This reference maps merged Focus--Master assets into the current local runtime so one operator can execute private company workflows end-to-end.

## Source Trees Referenced

### Core merged runtime
- `FOCUS_MASTER_AI/` (API server, orchestration, dispatcher, knowledge registry, operator console)
- `focus_ai/` (11-stage engine, prompts, build/deploy scripts, published outputs)

### Workflow + prompt system
- `focus_ai/published/final_system/system/sacred_ai_workflow.md`
- `focus_ai/published/final_system/system/stage_prompts.md`
- `focus_ai/scripts/engine.py`

### Strict live deployment path
- `focus_ai/scripts/run_single_operator_live.py`
- `focus_ai/scripts/deploy_replit.py`
- `focus_ai/scripts/deploy_infinityfree.py`
- `focus_ai/scripts/deploy_wordpress_theme.py`
- `focus_ai/scripts/deploy_wordpress_plugins.py`
- `focus_ai/scripts/verify_live_app.py`

## Company Routing (Single Owner)
- Focus Records LLC
- Royal Lee Construction Solutions LLC
- Focus Negotium Inc

## Standard Command (Single Owner)
```bash
FOCUS_OPERATOR_MODE=single_owner python3 focus_ai/scripts/run_single_operator_live.py
```

## Notes
- This flow is fail-fast and requires deployment credentials at runtime.
- Secret values remain outside git and should be loaded via `.secrets/focus_master.env` or environment variables.
