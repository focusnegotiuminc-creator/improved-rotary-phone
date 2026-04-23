#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "site"
CONFIG = ROOT / "config" / "business_os.json"

REQUIRED_FILES = [
    SITE / "homepage_copy.md",
    SITE / "change_log.md",
    SITE / "visual_preview.html",
    SITE / "visual_preview.css",
]

CATALOG = json.loads(CONFIG.read_text(encoding="utf-8"))
CONTACT = CATALOG["portal"]["primary_contact"]
PHONE_RAW = CONTACT["phone"]
PHONE_DISPLAY = CONTACT.get("phone_display", PHONE_RAW)
CONTACT_NAME = CONTACT["name"]

REQUIRED_TOKENS = {
    SITE / "homepage_copy.md": ["vertical luminous silhouette", CONTACT_NAME],
    SITE / "visual_preview.html": ["Abstract vertical alignment energy visual", CONTACT_NAME],
    SITE / "change_log.md": [CONTACT_NAME],
}

PHONE_TOKEN_FILES = {
    SITE / "homepage_copy.md",
    SITE / "visual_preview.html",
    SITE / "change_log.md",
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
        if file in PHONE_TOKEN_FILES and PHONE_RAW not in text and PHONE_DISPLAY not in text:
            errors.append(
                f"{file}: missing phone token '{PHONE_RAW}' or display token '{PHONE_DISPLAY}'"
            )

    if errors:
        print("Verification errors:")
        for error in errors:
            print(f"- {error}")
        return 1

    print("Visual/content verification passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
