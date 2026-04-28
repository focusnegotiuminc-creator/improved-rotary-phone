from __future__ import annotations
from pathlib import Path

p = Path("scripts/build_master_archive.py")
c = p.read_text(encoding="utf-8")

tokens = [
    "REPO_MIRROR_EXPORT",
    "REPO_MIRROR_EXPORT =",
    "consolidation_manifest",
    "repo_inventory",
    "write_repo_inventory",
    "manifests_dir",
    "DRIVE_EXPORTS",
    "DESKTOP_ARCHIVE",
    "DESKTOP_ARCHIVE /",
    "bundle",
    "make_archive",
    "zip",
]

def show_around(token: str, window: int = 1200) -> None:
    i = c.find(token)
    if i == -1:
        print(f"\n--- NOT_FOUND {token} ---\n")
        return
    start = max(0, i - 600)
    end = min(len(c), i + window)
    print(f"\n--- AROUND {token} (idx={i}) ---\n")
    print(c[start:end])

for t in tokens:
    show_around(t)

print("\n--- DONE ---")
