#!/usr/bin/env python3
from __future__ import annotations

import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
REPO_ROOT = ROOT.parents[1]
SCRIPT_DIR = REPO_ROOT / "focus_ai" / "scripts"
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from deploy_infinityfree import (  # noqa: E402
    _close_quietly,
    _connect_and_login,
    _delete_remote_path,
    _host_candidates,
    _list_dir,
    _mkdirs,
    _parse_remote_dir_candidates,
    _resolve_remote_dir,
    _upload_dir,
)

PUBLIC = ROOT / "dist"
DEFAULT_ENV_FILES = [
    REPO_ROOT / ".secrets" / "focus_master.env",
    REPO_ROOT / ".secrets" / "fluxcrave.env",
]


def load_env_file(path: Path) -> None:
    if not path.exists():
        return
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip()
        if key and key not in os.environ:
            os.environ[key] = value


def wipe_remote_dir(ftp, remote_dir: str) -> int:
    removed = 0
    for item in _list_dir(ftp, remote_dir):
        if _delete_remote_path(ftp, item):
            removed += 1
            print(f"Removed remote item: {item}")
    return removed


def main() -> int:
    for env_file in DEFAULT_ENV_FILES:
        load_env_file(env_file)

    if not PUBLIC.exists():
        print(f"Missing Flux & Crave build output: {PUBLIC}")
        return 1

    host = os.getenv("INFINITYFREE_FTP_HOST", "")
    user = os.getenv("INFINITYFREE_FTP_USER", "")
    password = os.getenv("INFINITYFREE_FTP_PASS", "")
    configured_remote = os.getenv("FLUXCRAVE_REMOTE_DIR", "fluxcrave.com/htdocs")
    candidates = _parse_remote_dir_candidates(
        os.getenv("FLUXCRAVE_REMOTE_DIR_CANDIDATES", "fluxcrave.com/htdocs,htdocs")
    )

    if not host or not user or not password:
        print("Missing InfinityFree FTP credentials in the loaded secret files.")
        return 1

    last_error: Exception | None = None
    ftp = None
    candidate_host = ""
    for candidate_host in _host_candidates(host):
        try:
            ftp = _connect_and_login(candidate_host, user, password)
            break
        except Exception as exc:  # noqa: BLE001
            last_error = exc
            ftp = None

    if ftp is None:
        print(f"Unable to connect to FTP: {last_error}")
        return 1

    try:
        remote_dir = _resolve_remote_dir(ftp, configured_remote, candidates)
        _mkdirs(ftp, remote_dir)
        removed = wipe_remote_dir(ftp, remote_dir)
        files, dirs = _upload_dir(ftp, PUBLIC, remote_dir)
        print(
            f"Flux & Crave deploy complete: {files} files, {dirs} dirs, "
            f"{removed} previous entries removed."
        )
        print(f"Remote target: {candidate_host}/{remote_dir}")
        return 0
    finally:
        _close_quietly(ftp)


if __name__ == "__main__":
    raise SystemExit(main())
