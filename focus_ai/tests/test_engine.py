from pathlib import Path
import subprocess
import sys


def test_engine_runs_all_stages():
    result = subprocess.run(
        [sys.executable, "focus_ai/scripts/engine.py"],
        capture_output=True,
        text=True,
        check=True,
    )
    assert "Ran all 11 stages" in result.stdout
    assert Path("focus_ai/docs/engine_run.log").exists()


def test_engine_accepts_codex_thread_uri():
    result = subprocess.run(
        [
            sys.executable,
            "focus_ai/scripts/engine.py",
            "--stage",
            "1",
            "--thread-uri",
            "codex://threads/019cf3b1-7a75-7123-b3b7-a2b631c0934b",
        ],
        capture_output=True,
        text=True,
        check=True,
    )
    assert "Thread: codex://threads/019cf3b1-7a75-7123-b3b7-a2b631c0934b" in result.stdout


def test_engine_rejects_invalid_thread_uri():
    result = subprocess.run(
        [
            sys.executable,
            "focus_ai/scripts/engine.py",
            "--thread-uri",
            "https://example.com/thread",
        ],
        capture_output=True,
        text=True,
    )
    assert result.returncode != 0
    assert "Thread URI must match" in result.stderr
