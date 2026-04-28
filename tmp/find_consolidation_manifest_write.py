from __future__ import annotations

from pathlib import Path

p = Path("scripts/build_master_archive.py")
c = p.read_text(encoding="utf-8").splitlines()

# Find the first line that defines consolidation_manifest = {
idx = None
for i, line in enumerate(c):
    if "consolidation_manifest" in line and "=" in line and "{" in line:
        idx = i
        break

if idx is None:
    print("NOT_FOUND: consolidation_manifest assignment block")
    raise SystemExit(0)

print(f"FOUND consolidation_manifest assignment at line ~{idx+1}")

# Look forward for likely output paths/writes until we hit a blank/function end.
# We specifically want lines that construct a filename/path and then write it.
candidates = []
for j in range(idx, min(len(c), idx + 400)):
    line = c[j]
    if any(k in line for k in [
        "manifests_dir",
        "write_text",
        "open(",
        "json.dump",
        "Path(",
        "consolidation_manifest",
        "storage_sync_report",
        "repo_inventory",
    ]):
        candidates.append((j + 1, line))

print("\n--- Relevant lines near consolidation_manifest ---")
for ln, line in candidates:
    print(f"{ln}: {line}")

# Also find any explicit occurrences of ".json" with consolidation_manifest
print("\n--- consolidation_manifest.*.json occurrences ---")
for i, line in enumerate(c):
    if "consolidation_manifest" in line and ".json" in line:
        print(f"{i+1}: {line}")
