from __future__ import annotations

from pathlib import Path

text = Path("Makefile").read_text(encoding="utf-8").splitlines()

target = "merge-gh-dry-run:"
idx = None
for i, line in enumerate(text):
    if line.strip() == target:
        idx = i
        break

if idx is None:
    raise SystemExit("Target not found: merge-gh-dry-run:")

start = max(0, idx - 5)
end = min(len(text), idx + 20)

for i in range(start, end):
    print(f"{i+1}:{text[i]}")
