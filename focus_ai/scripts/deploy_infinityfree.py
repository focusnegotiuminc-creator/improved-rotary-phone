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
import time
from ftplib import FTP, error_perm
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PUBLIC = ROOT / "published" / "public_site"
DEFAULT_REMOTE_DIR_CANDIDATES = [
    "thefocuscorp.com/htdocs",
    "htdocs",
    "domains/thefocuscorp.com/public_html",
]
DEFAULT_REMOTE_REMOVE_PATHS = [
    "command",
    "machine.html",
    "master_prompt_studio.js",
    "data/business_os.json",
    "data/stages.json",
]
DEFAULT_LOGIN_RETRIES = 3
DEFAULT_LOGIN_RETRY_DELAY = 2.0


def _parse_remote_dir_candidates(raw: str | None) -> list[str]:
    if not raw:
        return list(DEFAULT_REMOTE_DIR_CANDIDATES)
    parsed = [item.strip().strip("/") for item in raw.split(",") if item.strip()]
    return parsed or list(DEFAULT_REMOTE_DIR_CANDIDATES)


def _parse_remove_paths(raw: str | None) -> list[str]:
    if raw is None:
        return list(DEFAULT_REMOTE_REMOVE_PATHS)
    parsed = [item.strip().strip("/") for item in raw.split(",") if item.strip()]
    return parsed


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


def _strict_mode() -> bool:
    return os.getenv("INFINITYFREE_STRICT", "0").strip().lower() in {
        "1",
        "true",
        "yes",
        "on",
    }


def _close_quietly(ftp: FTP) -> None:
    try:
        ftp.quit()
    except Exception:
        try:
            ftp.close()
        except Exception:
            pass


def _connect_and_login(
    host: str,
    user: str,
    password: str,
    *,
    retries: int = DEFAULT_LOGIN_RETRIES,
    retry_delay: float = DEFAULT_LOGIN_RETRY_DELAY,
    ftp_factory=FTP,
) -> FTP:
    attempts = max(1, retries)
    last_exc: Exception | None = None

    for attempt in range(1, attempts + 1):
        ftp = ftp_factory(host, timeout=30)
        ftp.set_pasv(True)
        try:
            ftp.login(user=user, passwd=password)
            return ftp
        except Exception as exc:  # noqa: BLE001
            last_exc = exc
            _close_quietly(ftp)
            if attempt >= attempts:
                raise
            print(
                f"FTP login attempt {attempt} failed: {exc}. "
                f"Retrying in {retry_delay * attempt:.1f}s..."
            )
            time.sleep(max(0.0, retry_delay) * attempt)

    assert last_exc is not None
    raise last_exc


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


def _list_dir(ftp: FTP, remote_dir: str) -> list[str]:
    start_dir = ftp.pwd()
    try:
        ftp.cwd(remote_dir)
        names = ftp.nlst()
    finally:
        try:
            ftp.cwd(start_dir)
        except error_perm:
            pass

    cleaned: list[str] = []
    for name in names:
        stripped = name.strip().strip("/")
        if not stripped or stripped.endswith("/.") or stripped.endswith("/..") or stripped in {".", ".."}:
            continue
        if "/" in stripped:
            cleaned.append(stripped)
        else:
            cleaned.append(f"{remote_dir.strip('/')}/{stripped}".strip("/"))
    return cleaned


def _delete_remote_path(ftp: FTP, remote_path: str) -> bool:
    normalized = remote_path.strip().strip("/")
    if not normalized:
        return False

    if _path_exists(ftp, normalized):
        for child in _list_dir(ftp, normalized):
            if child == normalized:
                continue
            _delete_remote_path(ftp, child)
        ftp.rmd(normalized)
        return True

    try:
        ftp.delete(normalized)
        return True
    except error_perm as exc:
        if str(exc).startswith("550"):
            return False
        raise


def _cleanup_remote_paths(ftp: FTP, remote_dir: str, relative_paths: list[str]) -> int:
    removed = 0
    for rel_path in relative_paths:
        target = f"{remote_dir.rstrip('/')}/{rel_path.strip('/')}".strip("/")
        if _delete_remote_path(ftp, target):
            removed += 1
            print(f"Removed legacy remote path: {target}")
    return removed


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
    remote_remove_paths = _parse_remove_paths(os.getenv("INFINITYFREE_REMOVE_PATHS"))
    retry_count = int(os.getenv("INFINITYFREE_LOGIN_RETRIES", str(DEFAULT_LOGIN_RETRIES)))
    retry_delay = float(
        os.getenv("INFINITYFREE_LOGIN_RETRY_DELAY", str(DEFAULT_LOGIN_RETRY_DELAY))
    )

    strict = _strict_mode()
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
        if strict:
            return 1
        print("InfinityFree deploy skipped (non-strict mode).")
        return 0

    last_error: Exception | None = None
    passwords = [secret for secret in [password, password_alt] if secret]
    for ftp_host in _host_candidates(host):
        for passwd in passwords:
            try:
                with _connect_and_login(
                    ftp_host,
                    user,
                    passwd,
                    retries=retry_count,
                    retry_delay=retry_delay,
                    ftp_factory=FTP,
                ) as ftp:
                    remote_dir = _resolve_remote_dir(ftp, remote_dir_setting, remote_dir_candidates)
                    if remote_dir_setting.strip().lower() in {"", "auto", "suggested"}:
                        print(f"Auto-selected remote deploy directory: {remote_dir}")
                    removed = _cleanup_remote_paths(ftp, remote_dir, remote_remove_paths)
                    files, dirs = _upload_dir(ftp, PUBLIC, remote_dir)
                    print(
                        f"Uploaded {files} files ({dirs} directories) to {ftp_host}:{remote_dir}"
                    )
                    if removed:
                        print(f"Removed {removed} legacy remote paths from {remote_dir}")
                    return 0
            except Exception as exc:  # noqa: BLE001
                last_error = exc
                print(f"Failed host {ftp_host} with provided credential set: {exc}")

    if last_error is not None:
        print(f"InfinityFree deploy failed: {last_error}")
        if strict:
            return 1
        print("InfinityFree deploy skipped because INFINITYFREE_STRICT is disabled.")
        return 0

    return 1


if __name__ == "__main__":
    raise SystemExit(main())
