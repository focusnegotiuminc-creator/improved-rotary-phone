#!/usr/bin/env python3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "site"

REQUIRED_FILES = [
    SITE / "homepage_copy.md",
    SITE / "change_log.md",
    SITE / "visual_preview.html",
    SITE / "visual_preview.css",
]

REQUIRED_TOKENS = {
    SITE / "homepage_copy.md": ["2172576222", "vertical luminous silhouette"],
    SITE / "visual_preview.html": ["2172576222", "Abstract vertical alignment energy visual"],
    SITE / "change_log.md": ["2172576222"],
}


def main() -> int:
    missing = [str(f) for f in REQUIRED_FILES if not f.exists()]
    if missing:
        print("Missing files:")
        for item in missing:
            print(f"- {item}")
        return 1

    errors = []
    for file, tokens in REQUIRED_TOKENS.items():
        text = file.read_text(encoding="utf-8")
        for token in tokens:
            if token not in text:
                errors.append(f"{file}: missing token '{token}'")

    if errors:
        print("Verification errors:")
        for error in errors:
            print(f"- {error}")
        return 1

    print("Visual/content verification passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
