#!/usr/bin/env python3
"""Run the full local deployment path without GitHub Actions."""

from __future__ import annotations

import argparse
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def _candidate_env_files() -> list[Path]:
    home = Path.home()
    return [
        ROOT / ".secrets" / "focus_master.env",
        ROOT.parent / ".secrets" / "focus_master.env",
        ROOT.parent / "GitHub" / "Focus--Master" / ".secrets" / "focus_master.env",
        home / "OneDrive" / "Documents" / "GitHub" / "Focus--Master" / ".secrets" / "focus_master.env",
    ]


DEFAULT_ENV_FILE = next((path for path in _candidate_env_files() if path.exists()), _candidate_env_files()[0])
BROKEN_PROXY_VALUES = {"http://127.0.0.1:9", "https://127.0.0.1:9"}
PROXY_ENV_NAMES = [
    "HTTP_PROXY",
    "HTTPS_PROXY",
    "ALL_PROXY",
    "GIT_HTTP_PROXY",
    "GIT_HTTPS_PROXY",
    "http_proxy",
    "https_proxy",
    "all_proxy",
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Publish, build, deploy, and verify the live site from the local machine."
    )
    parser.add_argument(
        "--env-file",
        default=str(DEFAULT_ENV_FILE),
        help="Optional env file with deploy credentials and live verification settings.",
    )
    parser.add_argument(
        "--include-replit",
        action="store_true",
        help="Also trigger deploy_replit.py before FTP deployment when configured.",
    )
    parser.add_argument(
        "--skip-verify",
        action="store_true",
        help="Skip verify_live_app.py after deployment.",
    )
    parser.add_argument(
        "--ftp-host",
        help="Override INFINITYFREE_FTP_HOST for this run without editing the env file.",
    )
    return parser.parse_args()


def load_env_file(path: Path) -> None:
    if not path.exists():
        return
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        if value:
            os.environ.setdefault(key.strip(), value.strip().strip("'").strip('"'))


def sanitize_known_broken_proxy_env() -> None:
    cleared: list[str] = []
    for name in PROXY_ENV_NAMES:
        value = os.environ.get(name, "").strip().rstrip("/")
        if value in BROKEN_PROXY_VALUES:
            os.environ.pop(name, None)
            cleared.append(name)
    if cleared:
        print(f"Cleared broken local proxy env vars for deploy: {', '.join(sorted(set(cleared)))}")


def run_step(label: str, script_path: Path) -> int:
    print(f"==> {label}")
    proc = subprocess.run(
        [sys.executable, str(script_path)],
        cwd=ROOT,
        text=True,
        check=False,
    )
    return proc.returncode


def main() -> int:
    args = parse_args()
    env_file = Path(args.env_file)
    sanitize_known_broken_proxy_env()
    if args.ftp_host:
        os.environ["INFINITYFREE_FTP_HOST"] = args.ftp_host
    load_env_file(env_file)
    if env_file.exists():
        print(f"Loaded env file: {env_file}")
    else:
        print(f"Env file not found, using current environment: {env_file}")

    steps: list[tuple[str, Path]] = [
        ("Publish eBooks", ROOT / "focus_ai" / "scripts" / "publish_ebooks.py"),
        ("Build public site", ROOT / "focus_ai" / "scripts" / "build_public_site.py"),
    ]
    if args.include_replit:
        steps.append(("Trigger Replit deploy", ROOT / "focus_ai" / "scripts" / "deploy_replit.py"))
    steps.append(("Deploy to InfinityFree", ROOT / "focus_ai" / "scripts" / "deploy_infinityfree.py"))
    if not args.skip_verify:
        steps.append(("Verify live endpoints", ROOT / "focus_ai" / "scripts" / "verify_live_app.py"))

    for label, script_path in steps:
        code = run_step(label, script_path)
        if code != 0:
            print(f"Step failed: {label}")
            return code

    print("Local live deployment completed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
