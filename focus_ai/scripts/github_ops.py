#!/usr/bin/env python3
"""GitHub operations helper for merging PRs and running the Focus AI engine live."""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def run_cmd(cmd: list[str], *, cwd: Path | None = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        cmd,
        cwd=cwd or ROOT,
        check=False,
        text=True,
        capture_output=True,
    )


def require_gh() -> None:
    if shutil.which("gh"):
        return
    raise SystemExit(
        "GitHub CLI (gh) is not installed. Install it and authenticate with: gh auth login"
    )


def ensure_gh_auth() -> None:
    check = run_cmd(["gh", "auth", "status"])
    if check.returncode == 0:
        return
    raise SystemExit(
        "GitHub CLI is not authenticated. Run `gh auth login` (or set GH_TOKEN) and retry."
    )


def print_403_help(stderr: str) -> None:
    if "403" not in stderr:
        return
    print(
        "\nDetected HTTP 403 while contacting GitHub. Common fixes:\n"
        "1) Ensure GH_TOKEN has repo permissions (or refresh `gh auth login`).\n"
        "2) Route traffic through your approved outbound tunnel/proxy, e.g.:\n"
        "   export HTTPS_PROXY=http://<proxy-host>:<proxy-port>\n"
        "   export HTTP_PROXY=http://<proxy-host>:<proxy-port>\n"
        "3) If your org requires SSH/VPN, connect first and rerun the command.\n",
        file=sys.stderr,
    )


def merge_all_prs(repo: str | None, merge_method: str) -> int:
    require_gh()
    ensure_gh_auth()

    cmd = ["gh", "pr", "list", "--state", "open", "--json", "number,title,baseRefName,headRefName"]
    if repo:
        cmd.extend(["--repo", repo])

    listed = run_cmd(cmd)
    if listed.returncode != 0:
        print(listed.stderr.strip() or listed.stdout.strip(), file=sys.stderr)
        print_403_help(listed.stderr)
        return listed.returncode

    prs = json.loads(listed.stdout)
    if not prs:
        print("No open pull requests found.")
        return 0

    print(f"Found {len(prs)} open pull request(s).")
    failed = 0
    for pr in prs:
        number = pr["number"]
        title = pr["title"]
        print(f"Merging PR #{number}: {title}")

        merge_cmd = ["gh", "pr", "merge", str(number), f"--{merge_method}", "--delete-branch"]
        if repo:
            merge_cmd.extend(["--repo", repo])

        merged = run_cmd(merge_cmd)
        if merged.returncode != 0:
            failed += 1
            print(merged.stderr.strip() or merged.stdout.strip(), file=sys.stderr)
            print_403_help(merged.stderr)
            continue

        print(merged.stdout.strip() or f"PR #{number} merged.")

    if failed:
        print(f"Completed with {failed} merge failure(s).", file=sys.stderr)
        return 1

    print("All open pull requests merged successfully.")
    return 0


def run_live_pipeline(include_deploy: bool) -> int:
    commands = [
        [sys.executable, str(ROOT / "focus_ai" / "scripts" / "engine.py")],
        [sys.executable, str(ROOT / "focus_ai" / "scripts" / "publish_ebooks.py")],
        [sys.executable, str(ROOT / "focus_ai" / "scripts" / "build_public_site.py")],
    ]

    if include_deploy:
        commands.append([sys.executable, str(ROOT / "focus_ai" / "scripts" / "deploy_infinityfree.py")])

    for cmd in commands:
        print(f"Running: {' '.join(cmd)}")
        proc = subprocess.run(cmd, cwd=ROOT, check=False)
        if proc.returncode != 0:
            return proc.returncode

    print("Focus AI engine pipeline run complete.")
    return 0


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Merge GitHub PRs and run Focus AI live pipeline commands."
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    merge = subparsers.add_parser("merge-prs", help="Merge all currently open pull requests.")
    merge.add_argument("--repo", help="Optional owner/repo override for GitHub CLI.")
    merge.add_argument(
        "--method",
        choices=["merge", "squash", "rebase"],
        default="merge",
        help="Merge strategy (default: merge).",
    )

    live = subparsers.add_parser(
        "go-live", help="Run engine, publish eBooks, and build public site."
    )
    live.add_argument(
        "--deploy",
        action="store_true",
        help="Also run InfinityFree deployment after build.",
    )

    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.command == "merge-prs":
        return merge_all_prs(repo=args.repo, merge_method=args.method)
    if args.command == "go-live":
        return run_live_pipeline(include_deploy=args.deploy)
    raise SystemExit("Unknown command")


if __name__ == "__main__":
    raise SystemExit(main())
