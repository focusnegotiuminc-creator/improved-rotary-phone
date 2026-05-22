from focus_ai.private_engine.orchestrator import create_run
from focus_ai.private_engine.hf_pull import load_registry, selected_model_ids


def test_focus_engine_routes_flux_and_requires_post_approval():
    run = create_run('Post a Flux & Crave launch campaign after the coder and critic review it')
    assert run.lane == 'Flux & Crave'
    assert run.approval_required is True
    assert any(stage['agent_id'] == 'focus-critic' for stage in run.stages)


def test_hf_registry_starter_profile_has_coder_and_embedding():
    registry = load_registry()
    selected = selected_model_ids(registry, 'starter_local', None)
    assert 'open_coder_primary' in selected
    assert 'embedding_light' in selected
    assert registry['models']['open_coder_primary']['repo_id'].startswith('Qwen/')
