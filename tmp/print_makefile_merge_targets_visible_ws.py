from __future__ import annotations

from pathlib import Path

lines = Path("Makefile").read_text(encoding="utf-8").splitlines()

# Find merge-gh-dry-run:
needle = "merge-gh-dry-run:"
idx = None
for i, line in enumerate(lines):
    if line.strip() == needle:
        idx = i
        break

if idx is None:
    raise SystemExit(f"Not found: {needle}")

start = max(0, idx - 5)
end = min(len(lines), idx + 12)

for i in range(start, end):
    raw = lines[i]
    # show leading whitespace explicitly
    visible = raw.replace("\t", "\\t")
    print(f"{i+1}:{visible}")
