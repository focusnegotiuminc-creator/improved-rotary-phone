#!/usr/bin/env python3
from __future__ import annotations

import json
import os
import stat
import sys
from html import escape
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from site_catalog import BOOK_BY_SOURCE, BOOK_CATALOG

ROOT = Path(__file__).resolve().parents[1]
EBOOKS = ROOT / "ebooks"
OUT = ROOT / "published" / "ebooks"
CONFIG = ROOT / "config" / "business_os.json"
BOOK_BUNDLE_URL = os.getenv(
    "FOCUS_BOOK_BUNDLE_URL",
    "https://buy.stripe.com/bJe7sKh2B6ZQ8bP4II5os02",
)


def _format_currency(value: float) -> str:
    return f"${value:,.2f}"


def load_contact() -> tuple[str, str]:
    data = json.loads(CONFIG.read_text(encoding="utf-8"))
    contact = data["portal"]["primary_contact"]
    phone = "".join(char for char in contact["phone"] if char.isdigit())
    return contact["name"], phone


def md_to_html(markdown: str) -> str:
    lines = markdown.splitlines()
    html: list[str] = []
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
        elif line.startswith("### "):
            if in_list:
                html.append("</ul>")
                in_list = False
            html.append(f"<h3>{escape(line[4:])}</h3>")
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


def shell_css() -> str:
    return """
    :root {
      --bg-900: #050812;
      --bg-850: #0a1222;
      --bg-800: #101a31;
      --panel: rgba(8, 16, 31, 0.82);
      --ink: #f6f8ff;
      --muted: #c1cbe3;
      --gold: #f2c96d;
      --sky: #7cc8ff;
      --ember: #ff9b68;
      --line: rgba(124, 200, 255, 0.2);
      --shadow: 0 28px 70px rgba(2, 8, 24, 0.45);
    }
    * { box-sizing: border-box; }
    body {
      margin: 0;
      color: var(--ink);
      font-family: "Manrope", "Segoe UI", sans-serif;
      background:
        radial-gradient(920px 520px at 14% 8%, rgba(62, 228, 214, 0.14), transparent 60%),
        radial-gradient(760px 460px at 90% 10%, rgba(242, 201, 109, 0.14), transparent 56%),
        linear-gradient(160deg, var(--bg-900), var(--bg-850) 50%, var(--bg-800) 100%);
    }
    main { max-width: 1080px; margin: 0 auto; padding: 2rem 1rem 4rem; }
    a { color: var(--sky); text-decoration: none; }
    h1, h2, h3 { margin: 0; font-family: "Cormorant Garamond", Georgia, serif; color: var(--gold); line-height: 1.05; }
    p, li { line-height: 1.72; color: var(--muted); }
    .eyebrow {
      margin: 0;
      color: var(--gold);
      letter-spacing: 0.16em;
      text-transform: uppercase;
      font-size: 0.74rem;
      font-weight: 700;
    }
    .hero, .card, .book-card {
      border: 1px solid var(--line);
      border-radius: 28px;
      padding: 1.2rem 1.25rem;
      margin-bottom: 1rem;
      background: linear-gradient(155deg, rgba(9, 18, 36, 0.84), rgba(15, 30, 58, 0.72));
      box-shadow: var(--shadow);
    }
    .hero {
      display: grid;
      gap: 0.85rem;
    }
    .cta-row, .meta-row, .catalog-grid {
      display: flex;
      flex-wrap: wrap;
      gap: 0.75rem;
    }
    .catalog-grid {
      display: grid;
      grid-template-columns: repeat(2, minmax(0, 1fr));
      gap: 1rem;
    }
    .btn {
      display: inline-flex;
      align-items: center;
      justify-content: center;
      min-height: 46px;
      padding: 0.82rem 1.05rem;
      border-radius: 999px;
      background: linear-gradient(120deg, var(--gold), #ffd999 52%, var(--ember));
      color: #1b1420;
      font-weight: 800;
    }
    .btn.secondary {
      background: rgba(6, 13, 26, 0.54);
      color: var(--ink);
      border: 1px solid rgba(124, 200, 255, 0.22);
    }
    .meta-row span {
      display: inline-flex;
      align-items: center;
      min-height: 34px;
      padding: 0.28rem 0.8rem;
      border-radius: 999px;
      border: 1px solid rgba(124, 200, 255, 0.18);
      background: rgba(6, 13, 26, 0.58);
      font-size: 0.88rem;
    }
    .price { color: #fff0c1; }
    article.card h1 { margin-top: 1rem; }
    article.card h2, article.card h3 { margin-top: 1.25rem; }
    @media (max-width: 780px) {
      .catalog-grid { grid-template-columns: 1fr; }
      .cta-row, .meta-row { flex-direction: column; }
      .btn { width: 100%; }
    }
    """.strip()


def wrap_page(title: str, hero_html: str, body_html: str) -> str:
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>{escape(title)}</title>
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@500;600;700&family=Manrope:wght@400;500;600;700;800&display=swap" rel="stylesheet" />
  <style>{shell_css()}</style>
</head>
<body>
  <main>
    {hero_html}
    <article class="card">{body_html}</article>
  </main>
</body>
</html>
"""


def safe_write_text(path: Path, contents: str) -> None:
    if path.exists():
        os.chmod(path, 0o644)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(contents, encoding="utf-8")


def build() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    markdown_files = sorted(EBOOKS.glob("*.md"))
    if not markdown_files:
        print("No ebook markdown files found.")
        return 1

    contact_name, phone = load_contact()
    links = []
    for md in markdown_files:
        meta = BOOK_BY_SOURCE.get(md.name, {
            "slug": md.stem,
            "title": md.stem.replace("_", " ").title(),
            "tag": "Focus AI title",
            "summary": "Published from the Focus AI library.",
            "price_usd": 14.99,
        })
        slug = meta["slug"]
        title = meta["title"]
        html_name = f"{slug}.html"
        pdf_href = f"pdfs/{slug}.pdf"
        hero_html = f"""
<section class="hero">
  <p class="eyebrow">{escape(meta['tag'])}</p>
  <h1>{escape(title)}</h1>
  <p>{escape(meta['summary'])}</p>
  <div class="meta-row">
    <span class="price">{_format_currency(float(meta['price_usd']))}</span>
    <span>Direct route {phone}</span>
    <span>Published Focus AI library</span>
  </div>
  <div class="cta-row">
    <a class="btn" href="../books.html">Back to book sales page</a>
    <a class="btn secondary" href="{pdf_href}">Download PDF</a>
    <a class="btn secondary" href="tel:{phone}">Call {phone}</a>
  </div>
  <p><a href="index.html">Back to eBook library</a> · <a href="../products.html">View live offers</a> · <a href="../index.html">Return to TheFocusCorp.com</a></p>
</section>
""".strip()
        body_html = md_to_html(md.read_text(encoding="utf-8"))
        page = wrap_page(title, hero_html, body_html)
        safe_write_text(OUT / html_name, page)
        links.append((meta, html_name))

    cards = []
    for meta, href in links:
        cards.append(
            f"""
<article class="book-card">
  <p class="eyebrow">{escape(meta['tag'])}</p>
  <h2>{escape(meta['title'])}</h2>
  <p>{escape(meta['summary'])}</p>
  <div class="meta-row">
    <span class="price">{_format_currency(float(meta['price_usd']))}</span>
    <span>PDF + web edition</span>
  </div>
  <div class="cta-row">
    <a class="btn" href="{href}">Read online</a>
    <a class="btn secondary" href="pdfs/{meta['slug']}.pdf">Download PDF</a>
  </div>
</article>
""".strip()
        )

    index_html = f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Focus AI eBook Library</title>
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@500;600;700&family=Manrope:wght@400;500;600;700;800&display=swap" rel="stylesheet" />
  <style>{shell_css()}</style>
</head>
<body>
  <main>
    <section class="hero">
      <p class="eyebrow">Published eBook library</p>
      <h1>Read the Focus AI library online or download printable PDFs.</h1>
      <p>The book storefront now includes visible pricing, downloadable PDFs, and direct routing into the higher-value Focus AI offer ladder.</p>
      <div class="meta-row">
        <span>{len(BOOK_CATALOG)} current titles</span>
        <span>Call or text {phone}</span>
        <span>Primary route: {escape(contact_name)}</span>
      </div>
      <div class="cta-row">
        <a class="btn" href="../books.html">Open books sales page</a>
        <a class="btn secondary" href="{BOOK_BUNDLE_URL}">Buy the bundle</a>
        <a class="btn secondary" href="../products.html">Browse live offers</a>
      </div>
      <p><a href="../index.html">Return to home</a> · <a href="../services.html">See services</a> · <a href="../command/">Open command platform</a></p>
    </section>
    <section class="catalog-grid">{''.join(cards)}</section>
  </main>
</body>
</html>
"""
    safe_write_text(OUT / "index.html", index_html)
    print(f"Published {len(markdown_files)} eBooks to {OUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(build())
