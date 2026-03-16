#!/usr/bin/env python3
from pathlib import Path
import shutil

ROOT = Path(__file__).resolve().parents[1]
PUBLISHED = ROOT / "published" / "ebooks"
SITE = ROOT / "site"
PUBLIC = ROOT / "published" / "public_site"


def copy_tree(src: Path, dst: Path) -> None:
    if not src.exists():
        return
    dst.mkdir(parents=True, exist_ok=True)
    for item in src.iterdir():
        target = dst / item.name
        if item.is_dir():
            shutil.copytree(item, target, dirs_exist_ok=True)
        else:
            shutil.copy2(item, target)


def build() -> int:
    if not PUBLISHED.exists():
        print("Missing published ebooks. Run publish_ebooks.py first.")
        return 1

    if PUBLIC.exists():
        shutil.rmtree(PUBLIC)
    PUBLIC.mkdir(parents=True, exist_ok=True)

    copy_tree(PUBLISHED, PUBLIC / "ebooks")

    preview_html = SITE / "visual_preview.html"
    preview_css = SITE / "visual_preview.css"
    if preview_html.exists():
        shutil.copy2(preview_html, PUBLIC / "index.html")
    if preview_css.exists():
        shutil.copy2(preview_css, PUBLIC / "visual_preview.css")

    # Add simple landing links for public visitors.
    landing = PUBLIC / "landing.html"
    landing.write_text(
        """<!doctype html>
<html lang=\"en\"><head>
  <meta charset=\"utf-8\" />
  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\" />
  <title>Focus AI Public Launch</title>
  <style>
    body { font-family: Inter, Arial, sans-serif; margin: 0; background: #0c1024; color: #ecf0ff; }
    main { max-width: 900px; margin: 0 auto; padding: 3rem 1rem; }
    a { color: #9de6ff; }
    .card { border: 1px solid #2b356d; border-radius: 12px; padding: 1rem 1.25rem; background: #171d3f; }
  </style>
</head><body>
  <main>
    <h1>Focus AI Public Launch</h1>
    <div class=\"card\">
      <p><a href=\"index.html\">View visual preview homepage</a></p>
      <p><a href=\"ebooks/index.html\">View published eBook library</a></p>
    </div>
  </main>
</body></html>
""",
        encoding="utf-8",
    )

    print(f"Built public site at {PUBLIC}")
    return 0


if __name__ == "__main__":
    raise SystemExit(build())
