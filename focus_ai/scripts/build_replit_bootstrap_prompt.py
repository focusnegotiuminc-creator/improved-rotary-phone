#!/usr/bin/env python3
"""Build a single Replit-shell command block for GitHub + Replit + InfinityFree go-live runs."""

from __future__ import annotations

import argparse

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Generate a copy/paste shell block for Replit that sets GitHub/Replit/InfinityFree "
            "environment variables and runs merge + go-live commands."
        )
    )
    parser.add_argument(
        "--repos",
        default="",
        help="Comma-separated owner/repo values to merge before go-live (example: org/a,org/b).",
    )
    parser.add_argument(
        "--default-repo",
        default="",
        help="Optional owner/repo value used when only one repo is needed.",
    )
    return parser.parse_args()


def _merge_commands(repos_csv: str, default_repo: str) -> str:
    repos = [repo.strip() for repo in repos_csv.split(",") if repo.strip()]
    if not repos and default_repo.strip():
        repos = [default_repo.strip()]

    if not repos:
        return "python3 focus_ai/scripts/github_ops.py merge-prs"

    merge_lines = [
        f'python3 focus_ai/scripts/github_ops.py merge-prs --repo "{repo}" || exit 1'
        for repo in repos
    ]
    return "\n".join(merge_lines)


def main() -> int:
    args = parse_args()
    merges = _merge_commands(args.repos, args.default_repo)

    lines = [
        "# Paste this entire block into the Replit Shell or Replit AI chat command panel.",
        "# IMPORTANT: GitHub personal access tokens are created manually in GitHub Settings.",
        "export GITHUB_TOKEN='REPLACE_WITH_NEW_GITHUB_TOKEN'",
        'export GH_TOKEN="$GITHUB_TOKEN"',
        "export GITHUB_REPOS='REPLACE_WITH_OWNER_REPO_LIST'",
        "",
        "export REPLIT_DEPLOY_HOOK_URL='REPLACE_WITH_REPLIT_DEPLOY_HOOK_URL'",
        "export REPLIT_DEPLOY_TOKEN='REPLACE_WITH_REPLIT_DEPLOY_TOKEN'",
        "",
        "export INFINITYFREE_FTP_HOST='REPLACE_WITH_INFINITYFREE_FTP_HOST'",
        "export INFINITYFREE_FTP_USER='REPLACE_WITH_INFINITYFREE_FTP_USER'",
        "export INFINITYFREE_FTP_PASS='REPLACE_WITH_INFINITYFREE_FTP_PASSWORD'",
        "export INFINITYFREE_REMOTE_DIR='htdocs'",
        "",
        merges,
        "python3 focus_ai/scripts/github_ops.py go-live --deploy",
    ]
    script = "\n".join(lines)

    print(script)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
