from __future__ import annotations

from pathlib import Path

lines = Path("scripts/build_master_archive.py").read_text(encoding="utf-8").splitlines()

# Based on earlier output: consolidation_manifest definition is around line 354 (1-based).
start = 345
end = 430

for i in range(start, min(end, len(lines))):
    print(f"{i+1}: {lines[i]}")
