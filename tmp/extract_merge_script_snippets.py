from __future__ import annotations

from pathlib import Path

p = Path("focus_ai/scripts/merge_github_repositories.py")
c = p.read_text(encoding="utf-8")

patterns = [
    "DEFAULT_MERGE_ROOT",
    "AUTO_BRANCH",
    "--owner",
    "--repos",
    "--dry-run",
    "def main",
    "if __name__",
    "git clone",
    "git remote",
    "checkout",
    "merge",
    "merged_repositories",
    "clone",
    "remote_name",
]

for pat in patterns:
    i = c.find(pat)
    if i == -1:
        continue
    start = max(0, i - 500)
    end = min(len(c), i + 2000)
    print(f"\n===== {pat} @ {i} =====\n")
    print(c[start:end])
