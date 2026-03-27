import subprocess
import sys


def test_visual_verification_passes():
    result = subprocess.run(
        [sys.executable, "focus_ai/scripts/verify_visuals.py"],
        capture_output=True,
        text=True,
        check=True,
    )
    assert "passed" in result.stdout.lower()
