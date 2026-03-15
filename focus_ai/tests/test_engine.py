from pathlib import Path
import subprocess


def test_engine_runs_all_stages():
    result = subprocess.run(
        ["python3", "focus_ai/scripts/engine.py"],
        capture_output=True,
        text=True,
        check=True,
    )
    assert "Ran all 11 stages" in result.stdout
    assert Path("focus_ai/docs/engine_run.log").exists()
