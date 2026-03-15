import subprocess


def test_visual_verification_passes():
    result = subprocess.run(
        ["python3", "focus_ai/scripts/verify_visuals.py"],
        capture_output=True,
        text=True,
        check=True,
    )
    assert "passed" in result.stdout.lower()
