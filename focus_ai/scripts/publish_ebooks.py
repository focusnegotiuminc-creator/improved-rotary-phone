#!/usr/bin/env python3
import os
import stat
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EBOOKS = ROOT / "ebooks"
OUT = ROOT / "published" / "ebooks"
BOOK_BUNDLE_URL = os.getenv(
    "FOCUS_BOOK_BUNDLE_URL",
    "https://buy.stripe.com/bJe7sKh2B6ZQ8bP4II5os02",
)


def md_to_html(markdown: str) -> str:
    lines = markdown.splitlines()
    html = []
    in_list = False

    for raw in lines:
        line = raw.rstrip()
        if not line:
            if in_list:
                html.append("</ul>")
                in_list = False
            continue

        if line.startswith("# "):
            if in_list:
                html.append("</ul>")
                in_list = False
            html.append(f"<h1>{escape(line[2:])}</h1>")
        elif line.startswith("## "):
            if in_list:
                html.append("</ul>")
                in_list = False
            html.append(f"<h2>{escape(line[3:])}</h2>")
        elif line.startswith("- "):
            if not in_list:
                html.append("<ul>")
                in_list = True
            html.append(f"<li>{escape(line[2:])}</li>")
        elif line[:2].isdigit() and line[1:3] == ". ":
            if not in_list:
                html.append("<ul>")
                in_list = True
            html.append(f"<li>{escape(line[3:])}</li>")
        else:
            if in_list:
                html.append("</ul>")
                in_list = False
            html.append(f"<p>{escape(line)}</p>")

    if in_list:
        html.append("</ul>")

    return "\n".join(html)


def wrap_page(title: str, body_html: str) -> str:
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>{escape(title)}</title>
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@500;600;700&family=Space+Grotesk:wght@400;500;700&display=swap" rel="stylesheet" />
  <style>
    :root {{
      --bg-900: #050812;
      --bg-800: #09142a;
      --panel: rgba(10, 20, 38, 0.78);
      --ink: #f6f8ff;
      --muted: #c1cbe3;
      --gold: #f2c96d;
      --sky: #7cc8ff;
      --line: rgba(124, 200, 255, 0.22);
    }}
    body {{
      margin: 0;
      font-family: "Space Grotesk", "Segoe UI", sans-serif;
      background:
        radial-gradient(920px 520px at 14% 8%, rgba(62, 228, 214, 0.14), transparent 60%),
        radial-gradient(760px 460px at 90% 10%, rgba(242, 201, 109, 0.14), transparent 56%),
        linear-gradient(160deg, var(--bg-900), var(--bg-800) 50%, #071426 100%);
      color: var(--ink);
    }}
    main {{ max-width: 920px; margin: 0 auto; padding: 2rem 1rem 4rem; }}
    a {{ color: var(--sky); }}
    h1, h2 {{ font-family: "Cormorant Garamond", Georgia, serif; color: var(--gold); line-height: 1.08; }}
    p, li {{ line-height: 1.72; color: var(--muted); }}
    .nav {{ margin-bottom: 1.5rem; }}
    .hero {{
      border: 1px solid var(--line);
      border-radius: 24px;
      padding: 1.2rem 1.25rem;
      margin-bottom: 1rem;
      background: linear-gradient(155deg, rgba(9, 18, 36, 0.84), rgba(15, 30, 58, 0.72));
    }}
    .card {{
      background: linear-gradient(155deg, rgba(9, 18, 36, 0.84), rgba(15, 30, 58, 0.72));
      border: 1px solid var(--line);
      padding: 1.15rem;
      border-radius: 24px;
    }}
  </style>
</head>
<body>
  <main>
    <section class="hero">
      <p class="nav"><a href="index.html">Back to eBook library</a> · <a href="../products.html">View live offers</a> · <a href="../index.html">Return to TheFocusCorp.com</a></p>
      <h1>{escape(title)}</h1>
      <p>Published from the Focus AI library for direct reading, sharing, and storefront delivery.</p>
    </section>
    <article class="card">{body_html}</article>
  </main>
</body>
</html>
"""


def safe_write_text(path: Path, contents: str) -> None:
    if path.exists():
        os.chmod(path, stat.S_IWRITE)
    path.write_text(contents, encoding="utf-8")


def build() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    markdown_files = sorted(EBOOKS.glob("*.md"))
    if not markdown_files:
        print("No ebook markdown files found.")
        return 1

    links = []
    for md in markdown_files:
        title = md.stem.replace("_", " ").title()
        html_name = f"{md.stem}.html"
        body_html = md_to_html(md.read_text(encoding="utf-8"))
        page = wrap_page(title, body_html)
        safe_write_text(OUT / html_name, page)
        links.append((title, html_name))

    index_items = "\n".join(
        f'<li><a href="{href}">{escape(title)}</a></li>' for title, href in links
    )
    index_html = f"""<!doctype html>
<html lang="en"><head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Focus AI eBook Library</title>
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@500;600;700&family=Space+Grotesk:wght@400;500;700&display=swap" rel="stylesheet" />
  <style>
    :root {{
      --bg-900: #050812;
      --bg-800: #09142a;
      --panel: rgba(10, 20, 38, 0.78);
      --ink: #f6f8ff;
      --muted: #c1cbe3;
      --gold: #f2c96d;
      --sky: #7cc8ff;
      --line: rgba(124, 200, 255, 0.22);
    }}
    body {{
      margin: 0;
      font-family: "Space Grotesk", "Segoe UI", sans-serif;
      background:
        radial-gradient(920px 520px at 14% 8%, rgba(62, 228, 214, 0.14), transparent 60%),
        radial-gradient(760px 460px at 90% 10%, rgba(242, 201, 109, 0.14), transparent 56%),
        linear-gradient(160deg, var(--bg-900), var(--bg-800) 50%, #071426 100%);
      color: var(--ink);
    }}
    main {{ max-width: 980px; margin: 0 auto; padding: 3rem 1rem 4rem; }}
    h1, h2 {{ font-family: "Cormorant Garamond", Georgia, serif; color: var(--gold); }}
    p, li {{ color: var(--muted); line-height: 1.7; }}
    .hero, .panel {{
      background: linear-gradient(155deg, rgba(9, 18, 36, 0.84), rgba(15, 30, 58, 0.72));
      border: 1px solid var(--line);
      border-radius: 24px;
      padding: 1rem 1.25rem;
      margin-bottom: 1rem;
    }}
    a {{ color: var(--sky); }}
    li {{ margin: .6rem 0; }}
  </style>
</head><body>
  <main>
    <section class="hero">
      <h1>Published eBook Library</h1>
      <p>These files are generated from <code>focus_ai/ebooks/*.md</code> and styled as storefront-ready reading pages for TheFocusCorp.com.</p>
      <p><a href="../index.html">Return to home</a> · <a href="../products.html">Browse live offers</a></p>
    </section>
    <section class="panel">
      <p><strong>Want the full library plus launch assets?</strong></p>
      <p><a href="{BOOK_BUNDLE_URL}">Buy the Focus AI eBook Bundle for $49</a></p>
      <p><a href="../products.html">View the live product ladder</a></p>
    </section>
    <section class="panel"><ul>{index_items}</ul></section>
  </main>
</body></html>
"""
    safe_write_text(OUT / "index.html", index_html)
    print(f"Published {len(markdown_files)} eBooks to {OUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(build())
