"""Plan and optionally create large GPU Hugging Face endpoint commands.

This script is intentionally safe by default: it prints commands and cost notes.
Actual paid endpoint creation requires:

  1. Passing --create
  2. Setting FOCUS_APPROVE_PAID_GPU=YES
  3. Having the Hugging Face CLI installed and authenticated

It does not print tokens.
"""
from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
from pathlib import Path
from typing import Any

CONFIG_PATH = Path(__file__).resolve().parent / "config" / "large_gpu_endpoint_profiles.json"


def load_profiles() -> dict[str, Any]:
    return json.loads(CONFIG_PATH.read_text(encoding="utf-8-sig"))


def endpoint_command(name: str, spec: dict[str, Any]) -> list[str]:
    # HF CLI syntax per current hf-cli help / skill docs.
    return [
        "hf", "endpoints", "deploy", name,
        "--repo", spec["repo"],
        "--framework", spec.get("engine", "vllm"),
        "--accelerator", "gpu",
        "--instance-type", spec["instance_type"],
        "--instance-size", spec["instance_size"],
        "--region", spec.get("region", "us-east-1"),
        "--vendor", spec.get("vendor", "aws"),
        "--min-replica", str(spec.get("min_replica", 0)),
        "--max-replica", str(spec.get("max_replica", 1)),
        "--scale-to-zero-timeout", str(spec.get("scale_to_zero_timeout_minutes", 15)),
    ]


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Plan/create Focus large GPU Hugging Face endpoints.")
    parser.add_argument("--endpoint", choices=["all"], default=None, help="Use 'all' to plan all endpoints, or omit with --name.")
    parser.add_argument("--name", help="Endpoint profile name to plan/create.")
    parser.add_argument("--create", action="store_true", help="Create paid endpoint using hf CLI. Requires FOCUS_APPROVE_PAID_GPU=YES.")
    args = parser.parse_args(argv)

    profiles = load_profiles()
    endpoints = profiles["endpoints"]
    if args.endpoint == "all":
        selected = list(endpoints)
    elif args.name:
        if args.name not in endpoints:
            raise SystemExit(f"Unknown endpoint {args.name}. Options: {', '.join(endpoints)}")
        selected = [args.name]
    else:
        selected = list(endpoints)

    plan = []
    for name in selected:
        spec = endpoints[name]
        cmd = endpoint_command(name, spec)
        plan.append({
            "name": name,
            "repo": spec["repo"],
            "purpose": spec["purpose"],
            "hourly_estimate_usd": spec["hourly_estimate_usd"],
            "scale_to_zero_timeout_minutes": spec["scale_to_zero_timeout_minutes"],
            "command": cmd,
        })

    print(json.dumps({
        "approval_rule": profiles["approval_rule"],
        "pricing_source": profiles["source_pricing_checked"],
        "selected": plan,
    }, indent=2))

    if not args.create:
        return 0
    if os.getenv("FOCUS_APPROVE_PAID_GPU") != "YES":
        raise SystemExit("Refusing paid endpoint creation. Set FOCUS_APPROVE_PAID_GPU=YES after approving exact model/instance/cost.")
    if not shutil.which("hf"):
        raise SystemExit("hf CLI is not installed. Install/authenticate Hugging Face CLI before creating endpoints.")
    for item in plan:
        subprocess.run(item["command"], check=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
