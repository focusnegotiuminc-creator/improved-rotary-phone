#!/usr/bin/env python3
from pathlib import Path
from html import escape

ROOT = Path(__file__).resolve().parents[1]
EBOOKS = ROOT / "ebooks"
OUT = ROOT / "published" / "ebooks"


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
<html lang=\"en\">
<head>
  <meta charset=\"utf-8\" />
  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\" />
  <title>{escape(title)}</title>
  <style>
    body {{ font-family: Inter, Arial, sans-serif; margin: 0; background: #0d1023; color: #eef1ff; }}
    main {{ max-width: 900px; margin: 0 auto; padding: 2rem 1rem 4rem; }}
    a {{ color: #90e4ff; }}
    h1,h2 {{ color: #ffd882; }}
    p,li {{ line-height: 1.6; }}
    .nav {{ margin-bottom: 1.5rem; }}
    .card {{ background: #151933; border: 1px solid #2b356d; padding: 1rem; border-radius: 12px; }}
  </style>
</head>
<body>
  <main>
    <p class=\"nav\"><a href=\"index.html\">← Back to eBook library</a></p>
    <article class=\"card\">{body_html}</article>
  </main>
</body>
</html>
"""


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
        (OUT / html_name).write_text(page, encoding="utf-8")
        links.append((title, html_name))

    index_items = "\n".join(
        f'<li><a href="{href}">{escape(title)}</a></li>' for title, href in links
    )
    index_html = f"""<!doctype html>
<html lang=\"en\"><head>
  <meta charset=\"utf-8\" />
  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\" />
  <title>Focus AI eBook Library</title>
  <style>
    body {{ font-family: Inter, Arial, sans-serif; margin: 0; background: radial-gradient(circle at top, #1b1940, #07070f); color: #eef1ff; }}
    main {{ max-width: 900px; margin: 0 auto; padding: 3rem 1rem 4rem; }}
    h1 {{ color: #ffd882; }}
    .panel {{ background: #151933; border: 1px solid #2b356d; border-radius: 12px; padding: 1rem 1.25rem; }}
    a {{ color: #90e4ff; }}
    li {{ margin: .6rem 0; }}
  </style>
</head><body>
  <main>
    <h1>Published eBook Library</h1>
    <p>These files are locally published HTML outputs generated from <code>focus_ai/ebooks/*.md</code>.</p>
    <section class=\"panel\"><ul>{index_items}</ul></section>
  </main>
</body></html>
"""
    (OUT / "index.html").write_text(index_html, encoding="utf-8")
    print(f"Published {len(markdown_files)} eBooks to {OUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(build())
