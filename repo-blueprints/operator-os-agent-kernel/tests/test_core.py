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


def test_render_prompt_preserves_human_final_approval():
    prompt = OperatorOSKernel().render_prompt("Build repo scaffold")
    assert "human final approval" in prompt.lower()
