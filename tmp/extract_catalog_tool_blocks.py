from __future__ import annotations

import re
from pathlib import Path

PATH = Path("cloudflare/focus-mobile-workbench/src/catalog.js")
c = PATH.read_text(encoding="utf-8")

def extract_block(tool_id: str, window_fallback: int = 6000) -> str:
    target = f'id: "{tool_id}"'
    i = c.find(target)
    if i == -1:
        return f"NOT_FOUND {tool_id}"

    # Best-effort: slice around the match. This avoids trying to parse JS AST in a small helper.
    start = max(0, i - 800)
    end = min(len(c), i + window_fallback)
    return c[start:end]

def main() -> None:
    for tool_id in ["github_workspace", "artifact_archive"]:
        print(f"---{tool_id.upper()}---")
        print(extract_block(tool_id))

if __name__ == "__main__":
    main()
