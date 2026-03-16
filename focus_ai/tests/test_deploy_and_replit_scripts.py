import shutil
from pathlib import Path
import subprocess


def test_deploy_infinityfree_requires_env_vars():
    result = subprocess.run(
        ["python3", "focus_ai/scripts/deploy_infinityfree.py"],
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 1
    assert "Missing required env vars" in result.stdout or "Missing public site bundle" in result.stdout


def test_replit_export_builds_bundle():
    result = subprocess.run(
        ["python3", "focus_ai/scripts/export_replit_bundle.py"],
        capture_output=True,
        text=True,
        check=True,
    )
    assert "Exported Replit bundle" in result.stdout
    bundle = Path("focus_ai/published/replit_bundle")
    assert bundle.exists()
    shutil.rmtree(bundle)
