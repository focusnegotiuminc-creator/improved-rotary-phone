"""Safe Hugging Face pull helper for the Focus Private AI Engine.

Default behavior pulls lightweight metadata/config/tokenizer files only.
Use --weights intentionally when the machine has enough disk/GPU resources.
Tokens are read from HF_TOKEN or local HF auth; never printed.
"""
from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any

REGISTRY_PATH = Path(__file__).resolve().parent / "config" / "hf_model_registry.json"


def load_registry(path: Path = REGISTRY_PATH) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def selected_model_ids(registry: dict[str, Any], profile: str | None, model: str | None) -> list[str]:
    models = registry["models"]
    if model:
        if model in models:
            return [model]
        matches = [key for key, spec in models.items() if spec["repo_id"] == model]
        if matches:
            return matches
        raise SystemExit(f"Unknown model key or repo_id: {model}")
    profile_name = profile or "starter_local"
    if profile_name not in registry["profiles"]:
        raise SystemExit(f"Unknown profile: {profile_name}. Available: {', '.join(registry['profiles'])}")
    return list(registry["profiles"][profile_name]["models"])


def run_hf_download(repo_id: str, local_dir: Path, patterns: list[str], dry_run: bool) -> None:
    cmd = [
        "hf",
        "download",
        repo_id,
        "--local-dir",
        str(local_dir),
    ]
    for pattern in patterns:
        cmd.extend(["--include", pattern])
    if dry_run:
        cmd.append("--dry-run")
    subprocess.run(cmd, check=True)


def snapshot_download(repo_id: str, local_dir: Path, patterns: list[str], dry_run: bool) -> None:
    if dry_run:
        print(json.dumps({"dry_run": True, "repo_id": repo_id, "local_dir": str(local_dir), "allow_patterns": patterns}, indent=2))
        return
    try:
        from huggingface_hub import snapshot_download as hf_snapshot_download
    except Exception:
        if shutil.which("hf"):
            run_hf_download(repo_id, local_dir, patterns, dry_run=False)
            return
        raise SystemExit(
            "huggingface_hub and hf CLI are not installed. Run:\n"
            "  python -m pip install -r requirements-ai-engine.txt\n"
            "or install the Hugging Face CLI, then retry."
        )
    token = os.getenv("HF_TOKEN") or None
    hf_snapshot_download(
        repo_id=repo_id,
        local_dir=str(local_dir),
        allow_patterns=patterns,
        token=token,
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Pull Hugging Face model metadata or weights for Focus Private AI Engine.")
    parser.add_argument("--profile", default="starter_local", help="Registry profile to pull. Default: starter_local")
    parser.add_argument("--model", help="Single registry key or HF repo_id to pull instead of a profile.")
    parser.add_argument("--weights", action="store_true", help="Pull weight files too. Default pulls metadata/config/tokenizer only.")
    parser.add_argument("--dry-run", action="store_true", help="Show what would be pulled without downloading.")
    parser.add_argument("--download-root", help="Override download root.")
    args = parser.parse_args(argv)

    registry = load_registry()
    root = Path(args.download_root or registry.get("download_root") or "D:/TheFocusFiles/Models/huggingface")
    root.mkdir(parents=True, exist_ok=True)
    keys = selected_model_ids(registry, args.profile, args.model)

    plan: list[dict[str, Any]] = []
    for key in keys:
        spec = registry["models"][key]
        repo_id = spec["repo_id"]
        patterns = spec["weights_allow_patterns"] if args.weights else spec["default_allow_patterns"]
        local_dir = root / repo_id.replace("/", "__")
        plan.append({"key": key, "repo_id": repo_id, "local_dir": str(local_dir), "patterns": patterns, "weights": args.weights})

    print(json.dumps({"download_plan": plan, "token_source": registry["policy"]["hf_token_source"]}, indent=2))
    for item in plan:
        snapshot_download(item["repo_id"], Path(item["local_dir"]), item["patterns"], dry_run=args.dry_run)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
