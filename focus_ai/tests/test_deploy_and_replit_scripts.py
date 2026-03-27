import shutil
import stat
import importlib.util
from pathlib import Path
import subprocess
import sys

DEPLOY_INFINITYFREE_PATH = Path("focus_ai/scripts/deploy_infinityfree.py")
DEPLOY_INFINITYFREE_SPEC = importlib.util.spec_from_file_location(
    "deploy_infinityfree", DEPLOY_INFINITYFREE_PATH
)
assert DEPLOY_INFINITYFREE_SPEC and DEPLOY_INFINITYFREE_SPEC.loader
deploy_infinityfree = importlib.util.module_from_spec(DEPLOY_INFINITYFREE_SPEC)
DEPLOY_INFINITYFREE_SPEC.loader.exec_module(deploy_infinityfree)


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
    assert result.returncode in {0, 1}
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


def test_connect_and_login_retries_before_success(monkeypatch):
    attempts = {"count": 0}

    class FakeFTP:
        def __init__(self, host, timeout=30):
            self.host = host
            self.timeout = timeout

        def set_pasv(self, _enabled):
            return None

        def login(self, user, passwd):
            attempts["count"] += 1
            if attempts["count"] < 3:
                raise Exception("530 Login authentication failed")

        def quit(self):
            return None

        def close(self):
            return None

    monkeypatch.setattr(deploy_infinityfree.time, "sleep", lambda _seconds: None)
    ftp = deploy_infinityfree._connect_and_login(
        "example.com",
        "user",
        "pass",
        retries=3,
        retry_delay=0,
        ftp_factory=FakeFTP,
    )
    assert isinstance(ftp, FakeFTP)
    assert attempts["count"] == 3


def test_deploy_infinityfree_non_strict_skips_failed_login(monkeypatch, tmp_path, capsys):
    public_dir = tmp_path / "published" / "public_site"
    public_dir.mkdir(parents=True)
    (public_dir / "index.html").write_text("<html></html>", encoding="utf-8")

    class FailingFTP:
        def __init__(self, host, timeout=30):
            self.host = host
            self.timeout = timeout

        def set_pasv(self, _enabled):
            return None

        def login(self, user, passwd):
            raise Exception("530 Login authentication failed")

        def quit(self):
            return None

        def close(self):
            return None

        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc, tb):
            return False

    monkeypatch.setattr(deploy_infinityfree, "PUBLIC", public_dir)
    monkeypatch.setattr(deploy_infinityfree, "FTP", FailingFTP)
    monkeypatch.setattr(deploy_infinityfree.time, "sleep", lambda _seconds: None)
    monkeypatch.setenv("INFINITYFREE_FTP_HOST", "example.com")
    monkeypatch.setenv("INFINITYFREE_FTP_USER", "user")
    monkeypatch.setenv("INFINITYFREE_FTP_PASS", "pass")
    monkeypatch.setenv("INFINITYFREE_REMOTE_DIR", "htdocs")
    monkeypatch.setenv("INFINITYFREE_LOGIN_RETRIES", "2")
    monkeypatch.delenv("INFINITYFREE_STRICT", raising=False)

    result = deploy_infinityfree.main()
    output = capsys.readouterr().out

    assert result == 0
    assert "InfinityFree deploy skipped because INFINITYFREE_STRICT is disabled." in output
