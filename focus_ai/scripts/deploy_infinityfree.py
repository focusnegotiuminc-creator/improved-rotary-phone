#!/usr/bin/env python3
"""Deploy focus_ai/published/public_site to InfinityFree over FTP.

Required env vars:
- INFINITYFREE_FTP_HOST
- INFINITYFREE_FTP_USER
- INFINITYFREE_FTP_PASS
Optional:
- INFINITYFREE_REMOTE_DIR (default: htdocs)
"""

from __future__ import annotations

import os
from ftplib import FTP, error_perm
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PUBLIC = ROOT / "published" / "public_site"


def _mkdirs(ftp: FTP, path: str) -> None:
    current = ""
    for part in [p for p in path.strip("/").split("/") if p]:
        current = f"{current}/{part}" if current else part
        try:
            ftp.mkd(current)
        except error_perm as exc:
            # 550 often means "already exists" on shared FTP hosts.
            if not str(exc).startswith("550"):
                raise


def _upload_dir(ftp: FTP, local_dir: Path, remote_dir: str) -> tuple[int, int]:
    files = 0
    dirs = 0
    _mkdirs(ftp, remote_dir)

    for path in sorted(local_dir.rglob("*")):
        rel = path.relative_to(local_dir).as_posix()
        remote_path = f"{remote_dir.rstrip('/')}/{rel}"
        if path.is_dir():
            _mkdirs(ftp, remote_path)
            dirs += 1
            continue

        parent = remote_path.rsplit("/", 1)[0]
        _mkdirs(ftp, parent)
        with path.open("rb") as fh:
            ftp.storbinary(f"STOR {remote_path}", fh)
        files += 1

    return files, dirs


def main() -> int:
    if not PUBLIC.exists():
        print("Missing public site bundle. Run: make public-build")
        return 1

    host = os.getenv("INFINITYFREE_FTP_HOST")
    user = os.getenv("INFINITYFREE_FTP_USER")
    password = os.getenv("INFINITYFREE_FTP_PASS")
    remote_dir = os.getenv("INFINITYFREE_REMOTE_DIR", "htdocs")

    missing = [
        name
        for name, value in {
            "INFINITYFREE_FTP_HOST": host,
            "INFINITYFREE_FTP_USER": user,
            "INFINITYFREE_FTP_PASS": password,
        }.items()
        if not value
    ]
    if missing:
        print("Missing required env vars:")
        for name in missing:
            print(f"- {name}")
        return 1

    with FTP(host, timeout=30) as ftp:
        ftp.login(user=user, passwd=password)
        files, dirs = _upload_dir(ftp, PUBLIC, remote_dir)
        print(f"Uploaded {files} files ({dirs} directories) to {host}:{remote_dir}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
