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

from focus_ai.private_engine.endpoint_planner import endpoint_command, load_profiles


def test_large_gpu_endpoint_profiles_require_scale_to_zero():
    profiles = load_profiles()
    endpoint = profiles['endpoints']['focus-coder-large-qwen3-30b']
    assert endpoint['min_replica'] == 0
    assert endpoint['hourly_estimate_usd'] > 0
    cmd = endpoint_command('focus-coder-large-qwen3-30b', endpoint)
    assert '--scale-to-zero-timeout' in cmd
    assert 'Qwen/Qwen3-Coder-30B-A3B-Instruct-FP8' in cmd
