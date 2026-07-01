from operator_os import CoordinateState, OperationMode, OperatorOSKernel


def test_coordinate_normalization():
    state = CoordinateState(eta=" Expanded ", theta=450, psi_phi=-90, mode=OperationMode.LOCAL).normalized()
    assert state.eta == "expanded"
    assert state.theta == 90
    assert state.psi_phi == 270


def test_loop_has_four_stages():
    kernel = OperatorOSKernel()
    results = kernel.run_cycle("Create a clean prompt scaffold")
    assert len(results) == 4
    assert results[-1].output.startswith("Resolution:")


def test_sensitive_credential_warning_triggers():
    kernel = OperatorOSKernel()
    result = kernel.global_consistency_check("Store a credential in the repository", CoordinateState(), {})
    assert result.warnings


def test_render_prompt_preserves_operator_rules():
    prompt = OperatorOSKernel().render_prompt("Build repo scaffold")
    assert "no secrets" in prompt.lower()
    assert "human final approval" in prompt.lower()
