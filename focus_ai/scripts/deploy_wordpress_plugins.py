#!/usr/bin/env python3
"""Deploy local WordPress plugins to InfinityFree over FTP.

This script is strict by default and fails when credentials or plugin directories
are missing so deployments cannot appear successful without live updates.
"""

from __future__ import annotations

import os
from ftplib import FTP, error_perm
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PLUGINS_ROOT = ROOT / "wordpress_plugins"
REMOTE_BASE = "thefocuscorp.com/htdocs/wp-content/plugins"


def _mkdirs(ftp: FTP, path: str) -> None:
    current = ""
    for part in [p for p in path.strip("/").split("/") if p]:
        current = f"{current}/{part}" if current else part
        try:
            ftp.mkd(current)
        except error_perm as exc:
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
    host = os.getenv("INFINITYFREE_FTP_HOST")
    user = os.getenv("INFINITYFREE_FTP_USER")
    password = os.getenv("INFINITYFREE_FTP_PASS")
    remote_base = os.getenv("INFINITYFREE_WORDPRESS_PLUGINS_REMOTE_DIR", REMOTE_BASE)
    require_plugins = os.getenv("FOCUS_REQUIRE_WORDPRESS_PLUGINS", "1").strip().lower() not in {
        "0",
        "false",
        "no",
    }

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
        print("Strict deploy mode requires live credentials for every run.")
        return 1

    if not PLUGINS_ROOT.exists():
        if require_plugins:
            print(f"Missing plugin root: {PLUGINS_ROOT}")
            print("Create plugin directories or set FOCUS_REQUIRE_WORDPRESS_PLUGINS=0.")
            return 1
        print("No local plugins directory found; plugin deploy skipped by configuration.")
        return 0

    plugin_dirs = sorted([p for p in PLUGINS_ROOT.iterdir() if p.is_dir()])
    if not plugin_dirs:
        if require_plugins:
            print(f"No plugin directories found under {PLUGINS_ROOT}.")
            print("Add at least one plugin folder or set FOCUS_REQUIRE_WORDPRESS_PLUGINS=0.")
            return 1
        print("No plugin directories found; plugin deploy skipped by configuration.")
        return 0

    with FTP(host, timeout=30) as ftp:
        ftp.login(user=user, passwd=password)

        total_files = 0
        total_dirs = 0
        for plugin_dir in plugin_dirs:
            remote_dir = f"{remote_base.rstrip('/')}/{plugin_dir.name}"
            files, dirs = _upload_dir(ftp, plugin_dir, remote_dir)
            total_files += files
            total_dirs += dirs
            print(f"Uploaded plugin '{plugin_dir.name}' -> {remote_dir} ({files} files, {dirs} dirs)")

    print(f"Uploaded {len(plugin_dirs)} plugin(s), {total_files} files and {total_dirs} directories total.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
