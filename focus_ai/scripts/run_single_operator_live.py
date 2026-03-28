#!/usr/bin/env python3
"""Run a strict single-operator live workflow for Focus companies.

This pipeline is fail-fast and intended for one private operator managing
Focus Records LLC, Royal Lee Construction Solutions LLC, and Focus Negotium Inc.
"""

from __future__ import annotations

import argparse
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DEFAULT_ENV_FILE = ROOT / ".secrets" / "focus_master.env"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run full strict operator workflow: AI engine -> build -> deploy -> verify"
    )
    parser.add_argument(
        "--env-file",
        default=str(DEFAULT_ENV_FILE),
        help="Optional env file for deployment and integration credentials.",
    )
    parser.add_argument(
        "--thread-uri",
        default="",
        help="Optional codex thread URI for workflow run log annotation.",
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
        os.environ.setdefault(key.strip(), value.strip().strip("'").strip('"'))


def run_step(label: str, cmd: list[str]) -> None:
    print(f"==> {label}")
    result = subprocess.run(cmd, cwd=ROOT, text=True, check=False)
    if result.returncode != 0:
        raise SystemExit(f"Step failed ({label}) with exit code {result.returncode}")


def main() -> int:
    args = parse_args()
    env_file = Path(args.env_file)
    load_env_file(env_file)

    if env_file.exists():
        print(f"Loaded env file: {env_file}")
    else:
        print(f"Env file not found, using current environment: {env_file}")

    operator_mode = os.getenv("FOCUS_OPERATOR_MODE", "single_owner").strip().lower()
    if operator_mode != "single_owner":
        raise SystemExit(
            "FOCUS_OPERATOR_MODE must be 'single_owner' for this workflow. "
            "Set FOCUS_OPERATOR_MODE=single_owner and retry."
        )

    engine_cmd = [sys.executable, "focus_ai/scripts/engine.py"]
    if args.thread_uri.strip():
        engine_cmd.extend(["--thread-uri", args.thread_uri.strip()])

    run_step("Run full 11-stage AI engine", engine_cmd)
    run_step("Publish eBooks", [sys.executable, "focus_ai/scripts/publish_ebooks.py"])
    run_step("Build public site", [sys.executable, "focus_ai/scripts/build_public_site.py"])
    run_step("Trigger Replit deploy", [sys.executable, "focus_ai/scripts/deploy_replit.py"])
    run_step("Deploy to InfinityFree", [sys.executable, "focus_ai/scripts/deploy_infinityfree.py"])
    run_step("Deploy WordPress theme", [sys.executable, "focus_ai/scripts/deploy_wordpress_theme.py"])
    run_step("Deploy WordPress plugins", [sys.executable, "focus_ai/scripts/deploy_wordpress_plugins.py"])
    run_step("Verify live endpoints", [sys.executable, "focus_ai/scripts/verify_live_app.py"])

    print("Single-operator strict live workflow completed successfully.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
