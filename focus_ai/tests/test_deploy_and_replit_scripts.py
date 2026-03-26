import shutil
import stat
from pathlib import Path
import subprocess
import sys


def _on_rm_error(func, path, _exc_info):
    Path(path).chmod(stat.S_IWRITE)
    func(path)


def test_deploy_infinityfree_requires_env_vars():
    result = subprocess.run(
        [sys.executable, "focus_ai/scripts/deploy_infinityfree.py"],
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 1
    assert "Missing required env vars" in result.stdout or "Missing public site bundle" in result.stdout


def test_replit_export_builds_bundle():
    result = subprocess.run(
        [sys.executable, "focus_ai/scripts/export_replit_bundle.py"],
        capture_output=True,
        text=True,
        check=True,
    )
    assert "Exported Replit bundle" in result.stdout
    bundle = Path("focus_ai/published/replit_bundle")
    assert bundle.exists()
    shutil.rmtree(bundle, onerror=_on_rm_error)


def test_deploy_replit_skips_without_hook():
    result = subprocess.run(
        [sys.executable, "focus_ai/scripts/deploy_replit.py"],
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0
    assert "Missing REPLIT_DEPLOY_HOOK_URL" in result.stdout
