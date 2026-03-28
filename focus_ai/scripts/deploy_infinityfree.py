#!/usr/bin/env python3
"""Deploy focus_ai/published/public_site to InfinityFree over FTP.

Required env vars:
- INFINITYFREE_FTP_HOST
- INFINITYFREE_FTP_USER
- INFINITYFREE_FTP_PASS
Optional:
- INFINITYFREE_FTP_PASS_ALT
- INFINITYFREE_REMOTE_DIR (default: auto)
- INFINITYFREE_REMOTE_DIR_CANDIDATES (comma-separated)
"""

from __future__ import annotations

import os
from ftplib import FTP, error_perm
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PUBLIC = ROOT / "published" / "public_site"
DEFAULT_REMOTE_DIR_CANDIDATES = [
    "thefocuscorp.com/htdocs",
    "htdocs",
    "domains/thefocuscorp.com/public_html",
]


def _parse_remote_dir_candidates(raw: str | None) -> list[str]:
    if not raw:
        return list(DEFAULT_REMOTE_DIR_CANDIDATES)
    parsed = [item.strip().strip("/") for item in raw.split(",") if item.strip()]
    return parsed or list(DEFAULT_REMOTE_DIR_CANDIDATES)


def _host_candidates(raw_host: str | None) -> list[str]:
    if not raw_host:
        return []
    candidates: list[str] = []
    for candidate in [h.strip() for h in raw_host.split(",") if h.strip()]:
        if candidate not in candidates:
            candidates.append(candidate)
        if "." in candidate and not candidate.startswith("ftp."):
            ftp_candidate = f"ftp.{candidate}"
            if ftp_candidate not in candidates:
                candidates.append(ftp_candidate)
    return candidates


def _path_exists(ftp: FTP, remote_path: str) -> bool:
    start_dir = ftp.pwd()
    try:
        ftp.cwd(remote_path)
    except error_perm:
        return False
    finally:
        try:
            ftp.cwd(start_dir)
        except error_perm:
            pass
    return True


def _resolve_remote_dir(ftp: FTP, configured_remote_dir: str, candidates: list[str]) -> str:
    configured = configured_remote_dir.strip().strip("/")
    if configured and configured.lower() not in {"auto", "suggested"}:
        return configured

    for candidate in candidates:
        if _path_exists(ftp, candidate):
            return candidate

    return candidates[0]


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
    if not PUBLIC.exists():
        print("Missing public site bundle. Run: make public-build")
        return 1

    host = os.getenv("INFINITYFREE_FTP_HOST", "")
    user = os.getenv("INFINITYFREE_FTP_USER")
    password = os.getenv("INFINITYFREE_FTP_PASS")
    password_alt = os.getenv("INFINITYFREE_FTP_PASS_ALT")
    remote_dir_setting = os.getenv("INFINITYFREE_REMOTE_DIR", "auto")
    remote_dir_candidates = _parse_remote_dir_candidates(
        os.getenv("INFINITYFREE_REMOTE_DIR_CANDIDATES")
    )

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

    last_error: Exception | None = None
    passwords = [secret for secret in [password, password_alt] if secret]
    for ftp_host in _host_candidates(host):
        for passwd in passwords:
            try:
                with FTP(ftp_host, timeout=30) as ftp:
                    ftp.login(user=user, passwd=passwd)
                    remote_dir = _resolve_remote_dir(ftp, remote_dir_setting, remote_dir_candidates)
                    files, dirs = _upload_dir(ftp, PUBLIC, remote_dir)
                    print(f"Uploaded {files} files ({dirs} directories) to {ftp_host}:{remote_dir}")
                    return 0
            except Exception as exc:  # noqa: BLE001
                last_error = exc
                print(f"Failed host {ftp_host} with provided credential set: {exc}")

    if last_error is not None:
        raise last_error
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
