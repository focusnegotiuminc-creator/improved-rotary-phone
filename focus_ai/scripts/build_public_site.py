#!/usr/bin/env python3
from __future__ import annotations

import json
import os
import shutil
import stat
import sys
from html import escape
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from site_catalog import BOOK_CATALOG, COMPANY_PROFILES

ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = ROOT.parent
CONFIG = ROOT / "config" / "business_os.json"
PUBLISHED = ROOT / "published" / "ebooks"
PUBLIC = ROOT / "published" / "public_site"
COMMAND_APP = REPO_ROOT / "app"
ENGINE_STAGES = REPO_ROOT / "engine" / "stages.json"
MASTER_PROMPT_SCRIPT = ROOT / "site" / "master_prompt_studio.js"
RLC_OUTPUT = REPO_ROOT / "construction" / "rlc_office_pkg_extracted" / "output"
RLC_CHECKLIST = REPO_ROOT / "construction" / "rlc_bid_input_checklist.md"
ROOT_HTACCESS = """DirectoryIndex index.html index.php
<IfModule mod_rewrite.c>
RewriteEngine On
RewriteBase /
RewriteRule ^index\\.php$ - [L]
RewriteCond %{REQUEST_FILENAME} -f [OR]
RewriteCond %{REQUEST_FILENAME} -d
RewriteRule ^ - [L]
RewriteRule . /index.php [L]
</IfModule>
"""


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


def _on_rm_error(func, path, _exc_info):
    os.chmod(path, stat.S_IWRITE)
    func(path)


def safe_rmtree(path: Path) -> None:
    if path.exists():
        shutil.rmtree(path, onerror=_on_rm_error)


def load_catalog() -> dict:
    data = json.loads(CONFIG.read_text(encoding="utf-8"))
    for offer in data.get("offers", []):
        env_name = offer.get("checkout_url_env", "")
        offer["checkout_url"] = os.getenv(env_name, "").strip() or offer.get("default_checkout_url", "")

    square = data.get("portal", {}).get("payment_processors", {}).get("square", {})
    if square:
        square["payment_links_url"] = (
            os.getenv(square.get("payment_links_url_env", ""), "").strip()
            or square.get("default_payment_links_url", "")
        )
        square["buy_button_url"] = (
            os.getenv(square.get("buy_button_url_env", ""), "").strip()
            or square.get("default_buy_button_url", "")
        )
    return data


def public_catalog(catalog: dict) -> dict:
    data = json.loads(json.dumps(catalog))
    for offer in data.get("offers", []):
        offer.pop("checkout_url_env", None)
    square = data.get("portal", {}).get("payment_processors", {}).get("square", {})
    square.pop("payment_links_url_env", None)
    square.pop("buy_button_url_env", None)
    for connector in data.get("connectors", []):
        connector.pop("env_keys", None)
        connector.pop("configured_keys", None)
    return data


def _format_currency(value: float) -> str:
    return f"${value:,.2f}"


def _phone_digits(value: str) -> str:
    return "".join(char for char in value if char.isdigit())


def _ebook_count() -> int:
    return len(list((ROOT / "ebooks").glob("*.md")))


def _rlc_bid_summary() -> dict[str, str]:
    target = RLC_OUTPUT / "bid_summary.json"
    if not target.exists():
        return {}
    data = json.loads(target.read_text(encoding="utf-8"))
    return {item["Label"]: _format_currency(float(item["Amount"])) for item in data}


def _rlc_line_item_count() -> int:
    csv_path = RLC_OUTPUT / "material_list.csv"
    if not csv_path.exists():
        return 0
    return max(0, len(csv_path.read_text(encoding="utf-8").splitlines()) - 1)


def _rlc_checklist_items() -> list[str]:
    if not RLC_CHECKLIST.exists():
        return []
    items: list[str] = []
    for raw_line in RLC_CHECKLIST.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line:
            continue
        if ". " in line and line.split(". ", 1)[0].isdigit():
            items.append(line.split(". ", 1)[1].strip())
    return items


def head_html(title: str, description: str) -> str:
    return f"""<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>{escape(title)}</title>
  <meta name="description" content="{escape(description)}" />
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@500;600;700&family=Manrope:wght@400;500;600;700;800&display=swap" rel="stylesheet" />
  <link rel="stylesheet" href="funnel.css" />
</head>"""


def nav_html() -> str:
    links = [
        ("index.html", "Home"),
        ("landing.html", "Landing"),
        ("services.html", "Services"),
        ("focus-records.html", "Focus Records"),
        ("royal-lee-construction.html", "RLC"),
        ("focus-negotium.html", "Focus Negotium"),
        ("books.html", "Books"),
        ("ebooks/index.html", "Library"),
        ("machine.html", "Prompt Studio"),
        ("command/", "Command"),
        ("booking.html", "Booking"),
    ]
    items = "".join(f'<a href="{href}">{label}</a>' for href, label in links)
    return (
        '<header class="site-header">'
        '<div class="brand-lockup"><span class="brand-mark"></span><div>'
        '<p class="eyebrow">TheFocusCorp.com</p><strong>Focus AI Sacred Operating System</strong>'
        f"</div></div><nav class=\"top-nav\">{items}</nav></header>"
    )


def render_sacred_visual() -> str:
    return """
<div class="sacred-visual" aria-hidden="true">
  <div class="orbital-ring ring-one"></div>
  <div class="orbital-ring ring-two"></div>
  <div class="orbital-ring ring-three"></div>
  <div class="sacred-grid"></div>
  <div class="sacred-core"></div>
  <span class="sacred-node node-a"></span>
  <span class="sacred-node node-b"></span>
  <span class="sacred-node node-c"></span>
  <span class="sacred-node node-d"></span>
  <div class="beam beam-left"></div>
  <div class="beam beam-right"></div>
</div>
""".strip()


def render_offer_cards(catalog: dict) -> str:
    cards = []
    for offer in catalog.get("offers", []):
        cards.append(
            f"""
<article class="offer-card glow-card">
  <p class="eyebrow">Offer ladder</p>
  <h3>{escape(offer['title'])}</h3>
  <p>{escape(offer['summary'])}</p>
  <div class="meta-row">
    <span class="price-pill">{_format_currency(float(offer['price_usd']))}</span>
    <span class="micro-note">Implementation-ready</span>
  </div>
  <div class="button-row">
    <a class="btn" href="{escape(offer['checkout_url'])}">{escape(offer['cta_label'])}</a>
  </div>
</article>
""".strip()
        )
    return "\n".join(cards)


def render_book_cards(phone: str, *, compact: bool = False) -> str:
    cards = []
    for book in BOOK_CATALOG:
        links = [
            f'<a class="btn" href="ebooks/{book["slug"]}.html">Read {escape(book["title"])} online</a>',
        ]
        if not compact:
            links.append(f'<a class="btn secondary" href="ebooks/pdfs/{book["slug"]}.pdf">Download PDF</a>')
            links.append(f'<a class="btn secondary" href="tel:{phone}">Call {phone}</a>')
        cards.append(
            f"""
<article class="book-card glow-card">
  <p class="eyebrow">{escape(book['tag'])}</p>
  <h3>{escape(book['title'])}</h3>
  <p>{escape(book['summary'])}</p>
  <div class="meta-row">
    <span class="price-pill">{_format_currency(float(book['price_usd']))}</span>
    <span class="micro-note">Digital edition</span>
  </div>
  <div class="button-row">{''.join(links)}</div>
</article>
""".strip()
        )
    return "\n".join(cards)


def render_company_cards(catalog: dict) -> str:
    accents = catalog["design_system"]["company_accents"]
    cards = []
    for company in COMPANY_PROFILES:
        accent = accents.get(company["id"], {})
        bullets = "".join(f"<li>{escape(item)}</li>" for item in company.get("proof_points", []))
        cards.append(
            f"""
<article class="info-card glow-card" style="--accent:{accent.get('accent', '#7CC8FF')};">
  <p class="eyebrow">{escape(company['eyebrow'])}</p>
  <h3>{escape(company['name'])}</h3>
  <p>{escape(company['description'])}</p>
  <ul class="detail-list">{bullets}</ul>
  <div class="button-row">
    <a class="btn secondary" href="{escape(company['slug'])}">Open {escape(company['name'])}</a>
  </div>
</article>
""".strip()
        )
    return "\n".join(cards)


def render_company_service_rows() -> str:
    rows = []
    for company in COMPANY_PROFILES:
        services = "".join(
            f"""
<div class="service-row">
  <div>
    <h3>{escape(service['title'])}</h3>
    <p>{escape(service['summary'])}</p>
  </div>
  <div class="service-price">{_format_currency(float(service['price_usd']))}</div>
</div>
""".strip()
            for service in company.get("services", [])
        )
        rows.append(
            f"""
<section class="service-cluster glow-card">
  <p class="eyebrow">{escape(company['name'])}</p>
  <h2>{escape(company['headline'])}</h2>
  <p class="section-copy">{escape(company['description'])}</p>
  <div class="service-stack">{services}</div>
  <div class="button-row"><a class="btn secondary" href="{escape(company['slug'])}">Open company page</a></div>
</section>
""".strip()
        )
    return "\n".join(rows)


def render_system_cards() -> str:
    items = [
        {
            "eyebrow": "Sacred storefront",
            "title": "Root experience",
            "summary": "A static-first homepage that immediately explains the offers, books, services, and routing across the three companies.",
            "href": "index.html",
            "cta": "See the root experience",
        },
        {
            "eyebrow": "Prompt activation",
            "title": "Master Prompt Studio",
            "summary": "Transform rough intent into a stronger multi-engine packet with platform-ready next steps.",
            "href": "machine.html",
            "cta": "Open prompt studio",
        },
        {
            "eyebrow": "Operator platform",
            "title": "The Eye of Focus",
            "summary": "Run the AI engine in a cleaner command environment with presets, stage logic, and export-ready briefs.",
            "href": "command/",
            "cta": "Enter command mode",
        },
    ]
    return "\n".join(
        f"""
<article class="feature-panel glow-card">
  <p class="eyebrow">{escape(item['eyebrow'])}</p>
  <h3>{escape(item['title'])}</h3>
  <p>{escape(item['summary'])}</p>
  <div class="button-row"><a class="btn secondary" href="{escape(item['href'])}">{escape(item['cta'])}</a></div>
</article>
""".strip()
        for item in items
    )


def render_track_cards(catalog: dict) -> str:
    return "\n".join(
        f"""
<article class="track-card glow-card">
  <p class="eyebrow">{escape(track['title'])}</p>
  <h3>{escape(track['title'])}</h3>
  <p>{escape(track['summary'])}</p>
</article>
""".strip()
        for track in catalog["portal"]["tracks"]
    )


def render_stage_cards(catalog: dict) -> str:
    return "\n".join(
        f"""
<article class="stage-card glow-card">
  <p class="eyebrow">{escape(stage['label'])}</p>
  <h3>{escape(stage['label'])}</h3>
  <p>{escape(stage['description'])}</p>
</article>
""".strip()
        for stage in catalog.get("workflow_stages", [])
    )


def render_connector_cards(catalog: dict) -> str:
    cards = []
    for connector in catalog.get("connectors", []):
        cards.append(
            f"""
<article class="stage-card glow-card">
  <p class="eyebrow">{escape(connector['category'].title())}</p>
  <h3>{escape(connector['label'])}</h3>
  <p>{escape(connector['notes'])}</p>
  <p class="micro-note">Status: {escape(connector.get('status', connector.get('mode', 'unknown')))}</p>
</article>
""".strip()
        )
    return "\n".join(cards)


def render_square_panel(catalog: dict) -> str:
    square = catalog["portal"]["payment_processors"]["square"]
    buttons = []
    if square.get("payment_links_url"):
        buttons.append(f'<a class="btn secondary" href="{escape(square["payment_links_url"])}">Square payment links</a>')
    if square.get("buy_button_url"):
        buttons.append(f'<a class="btn secondary" href="{escape(square["buy_button_url"])}">Square buy button</a>')
    if not buttons:
        buttons.append(f'<a class="btn secondary" href="{escape(square["setup_url"])}">Square setup path</a>')
    return f"""
<section class="feature-panel glow-card">
  <p class="eyebrow">Square-ready payments</p>
  <h2>Square support stays wired for direct checkout expansion.</h2>
  <p>{escape(square['summary'])}</p>
  <p class="micro-note">Status: {escape(square['status'])}</p>
  <div class="button-row">{''.join(buttons)}</div>
</section>
""".strip()


def render_company_page(company: dict, contact_name: str, phone: str) -> str:
    services = "\n".join(
        f"""
<article class="offer-card glow-card">
  <p class="eyebrow">Service architecture</p>
  <h3>{escape(service['title'])}</h3>
  <p>{escape(service['summary'])}</p>
  <div class="meta-row">
    <span class="price-pill">{_format_currency(float(service['price_usd']))}</span>
    <span class="micro-note">Standardized global rate</span>
  </div>
</article>
""".strip()
        for service in company["services"]
    )
    proof_points = "".join(f"<li>{escape(item)}</li>" for item in company["proof_points"])
    description = (
        f"{company['description']} This page carries the dedicated service structure, pricing, and routing "
        "while still connecting back into the larger Focus AI operating system."
    )
    return f"""<!doctype html>
<html lang="en">
{head_html(company['name'], description)}
<body>
  <main>
    {nav_html()}
    <section class="hero-panel luminous-hero">
      <div class="poster panel-flow">
        <p class="eyebrow">Dedicated company path</p>
        <h1>{escape(company['name'])}</h1>
        <p class="lede">{escape(company['headline'])}</p>
        <p>{escape(company['description'])}</p>
        <div class="metric-strip">
          <span>Direct route {phone}</span>
          <span>Akashic execution language</span>
          <span>Premium service architecture</span>
        </div>
        <div class="button-row">
          <a class="btn" href="tel:{phone}">Call {phone}</a>
          <a class="btn secondary" href="booking.html">Book with {escape(contact_name)}</a>
          <a class="btn secondary" href="services.html">See all services</a>
        </div>
      </div>
      <section class="feature-panel hero-visual-panel">{render_sacred_visual()}</section>
    </section>
    <section class="section-block split-band">
      <section class="feature-panel glow-card">
        <p class="eyebrow">Core proof points</p>
        <ul class="detail-list">{proof_points}</ul>
      </section>
      <section class="feature-panel glow-card">
        <p class="eyebrow">Shared operating note</p>
        <h2>This company is distinct, but it still lives inside one Focus AI system.</h2>
        <p>That means stronger routing, cleaner offers, reusable operating prompts, and a single customer-facing quality bar across every deliverable.</p>
      </section>
    </section>
    <section class="section-block">
      <p class="eyebrow">Services and standardized pricing</p>
      <h2>Choose the level of support that matches the decision in front of you.</h2>
      <div class="offer-grid">{services}</div>
    </section>
  </main>
</body>
</html>
"""


def build_css(catalog: dict) -> str:
    colors = catalog["design_system"]["core"]["colors"]
    return f"""
:root {{
  --bg-900: {colors['bg_900']};
  --bg-850: #081022;
  --bg-800: {colors['bg_800']};
  --panel: rgba(9, 18, 36, 0.76);
  --panel-strong: rgba(4, 10, 22, 0.9);
  --ink: {colors['ink']};
  --muted: {colors['muted']};
  --gold: {colors['gold']};
  --teal: {colors['teal']};
  --sky: {colors['sky']};
  --ember: {colors['ember']};
  --line: rgba(124, 200, 255, 0.2);
  --shadow: 0 28px 70px rgba(2, 8, 24, 0.45);
  --display: "Cormorant Garamond", Georgia, serif;
  --body: "Manrope", "Segoe UI", sans-serif;
}}
* {{ box-sizing: border-box; }}
html {{ scroll-behavior: smooth; }}
body {{
  margin: 0;
  min-height: 100vh;
  color: var(--ink);
  font-family: var(--body);
  background:
    radial-gradient(900px 620px at 8% 4%, rgba(62, 228, 214, 0.16), transparent 60%),
    radial-gradient(780px 460px at 92% 2%, rgba(242, 201, 109, 0.16), transparent 55%),
    radial-gradient(680px 420px at 50% 100%, rgba(255, 155, 104, 0.08), transparent 58%),
    linear-gradient(160deg, var(--bg-900), var(--bg-850) 44%, var(--bg-800) 100%);
  position: relative;
  overflow-x: hidden;
}}
body::before,
body::after {{
  content: "";
  position: fixed;
  inset: 0;
  pointer-events: none;
  z-index: -1;
}}
body::before {{
  background:
    repeating-radial-gradient(circle at center, transparent 0 38px, rgba(255,255,255,0.022) 38px 39px),
    linear-gradient(90deg, transparent, rgba(124, 200, 255, 0.04), transparent);
  mask-image: radial-gradient(circle at center, black 28%, transparent 88%);
  opacity: 0.9;
  animation: slowSpin 34s linear infinite;
}}
body::after {{
  background:
    linear-gradient(110deg, transparent 0%, rgba(242, 201, 109, 0.07) 44%, transparent 62%),
    linear-gradient(250deg, transparent 0%, rgba(62, 228, 214, 0.06) 42%, transparent 66%);
  animation: beamDrift 16s ease-in-out infinite alternate;
}}
a {{ color: var(--sky); text-decoration: none; }}
main {{ width: min(1220px, 94vw); margin: 0 auto; padding: 1rem 0 4rem; display: grid; gap: 1.2rem; }}
.site-header {{
  display: grid;
  grid-template-columns: minmax(220px, auto) minmax(0, 1fr);
  gap: 1rem;
  align-items: center;
  padding: 0.7rem 0 0.95rem;
  border-bottom: 1px solid rgba(124, 200, 255, 0.16);
}}
.brand-lockup {{ display: inline-flex; align-items: center; gap: 0.85rem; }}
.brand-mark {{
  width: 54px;
  height: 54px;
  border-radius: 50%;
  border: 1px solid rgba(242, 201, 109, 0.35);
  background:
    radial-gradient(circle at center, rgba(242, 201, 109, 0.2), transparent 40%),
    repeating-conic-gradient(from 0deg, rgba(124, 200, 255, 0.18) 0deg 18deg, transparent 18deg 36deg),
    rgba(7, 15, 29, 0.92);
  box-shadow: inset 0 0 28px rgba(124, 200, 255, 0.12);
}}
.top-nav {{ display: flex; flex-wrap: wrap; justify-content: flex-end; gap: 0.85rem; }}
.top-nav a {{
  padding: 0.62rem 0.95rem;
  border-radius: 999px;
  border: 1px solid rgba(124, 200, 255, 0.12);
  background: rgba(7, 15, 29, 0.42);
  color: var(--ink);
  font-size: 0.95rem;
}}
.eyebrow {{
  margin: 0;
  color: var(--gold);
  letter-spacing: 0.16em;
  text-transform: uppercase;
  font-size: 0.76rem;
  font-weight: 800;
}}
h1, h2, h3 {{ margin: 0; font-family: var(--display); line-height: 1.02; }}
h1 {{ font-size: clamp(2.7rem, 6vw, 5.8rem); }}
h2 {{ font-size: clamp(1.75rem, 3.8vw, 3.2rem); }}
h3 {{ font-size: clamp(1.2rem, 2.4vw, 1.85rem); }}
p, li {{ color: var(--muted); line-height: 1.72; }}
.lede {{ font-size: clamp(1.08rem, 2vw, 1.24rem); color: #eef4ff; max-width: 62ch; }}
.hero-panel,
.feature-panel,
.offer-card,
.info-card,
.track-card,
.stage-card,
.book-card,
.service-cluster {{
  border: 1px solid var(--line);
  border-radius: 30px;
  background: linear-gradient(152deg, rgba(9, 18, 36, 0.84), rgba(16, 30, 58, 0.72));
  box-shadow: var(--shadow);
}}
.glow-card {{ position: relative; overflow: hidden; }}
.glow-card::before {{
  content: "";
  position: absolute;
  inset: auto -14% 68% auto;
  width: 180px;
  height: 180px;
  border-radius: 50%;
  background: radial-gradient(circle, rgba(242, 201, 109, 0.16), transparent 68%);
  pointer-events: none;
}}
.hero-panel {{
  display: grid;
  grid-template-columns: minmax(0, 1.18fr) minmax(300px, 0.82fr);
  gap: 1rem;
  padding: clamp(1.2rem, 3vw, 2.4rem);
  align-items: stretch;
}}
.luminous-hero {{
  background:
    linear-gradient(145deg, rgba(9, 18, 36, 0.92), rgba(10, 28, 55, 0.74)),
    radial-gradient(circle at 12% 18%, rgba(62, 228, 214, 0.12), transparent 30%);
}}
.poster,
.feature-panel,
.hero-visual-panel {{ display: grid; gap: 0.85rem; align-content: start; }}
.hero-visual-panel {{ padding: 1rem; min-height: 100%; }}
.panel-flow {{ align-content: center; }}
.metric-strip,
.button-row,
.meta-row,
.download-strip {{ display: flex; flex-wrap: wrap; gap: 0.72rem; }}
.metric-strip span,
.micro-note,
.price-pill {{
  display: inline-flex;
  align-items: center;
  min-height: 34px;
  padding: 0.28rem 0.8rem;
  border-radius: 999px;
  border: 1px solid rgba(124, 200, 255, 0.2);
  background: rgba(6, 13, 26, 0.58);
  color: #eef4ff;
  font-size: 0.9rem;
}}
.price-pill {{ color: #fff0c1; border-color: rgba(242, 201, 109, 0.26); }}
.micro-note {{ font-size: 0.82rem; color: var(--muted); }}
.btn {{
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-height: 48px;
  padding: 0.82rem 1.15rem;
  border-radius: 999px;
  border: 1px solid transparent;
  background: linear-gradient(120deg, var(--gold), #ffd999 52%, var(--ember));
  color: #1b1420;
  font-weight: 800;
}}
.btn.secondary {{
  background: rgba(6, 13, 26, 0.54);
  color: var(--ink);
  border-color: rgba(124, 200, 255, 0.22);
}}
.section-block {{ display: grid; gap: 0.9rem; }}
.section-copy {{ max-width: 68ch; margin: 0; }}
.grid-three,
.offer-grid,
.track-grid,
.stage-grid,
.detail-grid,
.split-band,
.book-grid,
.drawing-grid {{ display: grid; gap: 1rem; }}
.grid-three,
.offer-grid,
.book-grid {{ grid-template-columns: repeat(3, minmax(0, 1fr)); }}
.track-grid {{ grid-template-columns: repeat(4, minmax(0, 1fr)); }}
.stage-grid,
.detail-grid,
.split-band,
.drawing-grid {{ grid-template-columns: repeat(2, minmax(0, 1fr)); }}
.feature-panel,
.offer-card,
.info-card,
.track-card,
.stage-card,
.book-card,
.service-cluster,
.drawing-frame {{ padding: 1.15rem; }}
.detail-list {{ margin: 0.35rem 0 0; padding-left: 1.15rem; }}
.detail-list li + li {{ margin-top: 0.38rem; }}
.info-card::after {{
  content: "";
  width: 56px;
  height: 4px;
  border-radius: 999px;
  display: block;
  margin-top: 0.4rem;
  background: var(--accent, var(--sky));
}}
.service-stack {{ display: grid; gap: 0.85rem; margin-top: 0.6rem; }}
.service-row {{
  display: grid;
  grid-template-columns: minmax(0, 1fr) auto;
  gap: 1rem;
  padding: 0.95rem 1rem;
  border-radius: 22px;
  border: 1px solid rgba(124, 200, 255, 0.14);
  background: rgba(6, 13, 26, 0.5);
}}
.service-price {{ color: #fff0c1; font-weight: 800; font-size: 1.05rem; }}
.catalog-band {{ display: grid; gap: 1rem; grid-template-columns: minmax(0, 1.1fr) minmax(280px, 0.9fr); }}
.sacred-visual {{
  position: relative;
  min-height: 360px;
  border-radius: 28px;
  background:
    radial-gradient(circle at center, rgba(242, 201, 109, 0.16), transparent 34%),
    linear-gradient(145deg, rgba(6, 13, 26, 0.92), rgba(11, 23, 42, 0.84));
  overflow: hidden;
}}
.sacred-grid,
.orbital-ring,
.sacred-core,
.beam,
.sacred-node {{ position: absolute; }}
.sacred-grid {{
  inset: 6%;
  border-radius: 28px;
  background:
    linear-gradient(rgba(124, 200, 255, 0.08) 1px, transparent 1px),
    linear-gradient(90deg, rgba(124, 200, 255, 0.08) 1px, transparent 1px);
  background-size: 52px 52px;
  mask-image: radial-gradient(circle at center, black 42%, transparent 82%);
}}
.orbital-ring {{
  border-radius: 50%;
  border: 1px solid rgba(242, 201, 109, 0.26);
  animation: slowSpin 26s linear infinite;
}}
.ring-one {{ inset: 8%; }}
.ring-two {{ inset: 18%; animation-direction: reverse; animation-duration: 18s; border-color: rgba(124, 200, 255, 0.28); }}
.ring-three {{ inset: 28%; animation-duration: 14s; border-color: rgba(62, 228, 214, 0.26); }}
.sacred-core {{
  width: 110px;
  height: 110px;
  left: 50%;
  top: 50%;
  translate: -50% -50%;
  border-radius: 50%;
  background: radial-gradient(circle, rgba(242, 201, 109, 0.96), rgba(255, 155, 104, 0.34) 45%, rgba(124, 200, 255, 0.08) 72%, transparent 75%);
  box-shadow: 0 0 50px rgba(242, 201, 109, 0.35);
  animation: pulseCore 6s ease-in-out infinite;
}}
.sacred-node {{ width: 14px; height: 14px; border-radius: 50%; background: rgba(124, 200, 255, 0.92); box-shadow: 0 0 16px rgba(124, 200, 255, 0.55); }}
.node-a {{ left: 50%; top: 8%; translate: -50% 0; }}
.node-b {{ left: 86%; top: 50%; translate: -50% -50%; }}
.node-c {{ left: 50%; top: 88%; translate: -50% -100%; }}
.node-d {{ left: 14%; top: 50%; translate: -50% -50%; }}
.beam {{
  width: 140%;
  height: 2px;
  left: -20%;
  top: 50%;
  background: linear-gradient(90deg, transparent, rgba(242, 201, 109, 0.3), transparent);
}}
.beam-right {{ rotate: 60deg; }}
.beam-left {{ rotate: -60deg; }}
.drawing-frame {{
  border-radius: 28px;
  border: 1px solid var(--line);
  background: linear-gradient(155deg, rgba(9, 18, 35, 0.84), rgba(15, 30, 58, 0.72));
  box-shadow: var(--shadow);
}}
.drawing-frame img {{ width: 100%; height: auto; display: block; border-radius: 20px; background: #ffffff; }}
.drawing-frame figcaption {{ margin-top: 0.8rem; color: var(--muted); }}
@keyframes slowSpin {{ from {{ transform: rotate(0deg); }} to {{ transform: rotate(360deg); }} }}
@keyframes pulseCore {{ 0%, 100% {{ transform: scale(1); opacity: 0.92; }} 50% {{ transform: scale(1.08); opacity: 1; }} }}
@keyframes beamDrift {{ from {{ transform: translateX(-3%); }} to {{ transform: translateX(3%); }} }}
@media (max-width: 1080px) {{
  .hero-panel,
  .grid-three,
  .offer-grid,
  .track-grid,
  .stage-grid,
  .detail-grid,
  .split-band,
  .catalog-band,
  .book-grid,
  .drawing-grid {{ grid-template-columns: 1fr; }}
  .site-header {{ grid-template-columns: 1fr; }}
  .top-nav {{ justify-content: flex-start; }}
}}
@media (max-width: 720px) {{
  main {{ width: min(94vw, 100%); }}
  .top-nav,
  .button-row,
  .metric-strip,
  .meta-row,
  .download-strip {{ flex-direction: column; }}
  .btn,
  .top-nav a {{ width: 100%; justify-content: center; }}
  .service-row {{ grid-template-columns: 1fr; }}
  .sacred-visual {{ min-height: 280px; }}
}}
""".strip() + "\n"


def build_pages(catalog: dict) -> dict[str, str]:
    contact = catalog["portal"]["primary_contact"]
    contact_name = contact["name"]
    phone = _phone_digits(contact["phone"])
    ebook_count = _ebook_count()
    rlc_summary = _rlc_bid_summary()
    rlc_checklist = _rlc_checklist_items()

    home_page = f"""<!doctype html>
<html lang="en">
{head_html('TheFocusCorp.com', 'Sacred geometry storefront for Focus AI, books, services, and the command platform.')}
<body>
  <main>
    {nav_html()}
    <section class="hero-panel luminous-hero">
      <div class="poster panel-flow">
        <p class="eyebrow">Sacred geometry storefront</p>
        <h1>An akashic operating system for books, services, launches, and AI execution.</h1>
        <p class="lede">TheFocusCorp.com now opens as one coherent sacred storefront: mobile-friendly, animation-aware, and structured to move visitors from curiosity into book sales, service routing, and the live command platform.</p>
        <p>Every part of the experience points back to one direct route, one premium quality bar, and one operating system shared across Focus Records LLC, Royal Lee Construction Solutions LLC, and Focus Negotium Inc.</p>
        <div class="metric-strip">
          <span>Call or text {phone}</span>
          <span>{ebook_count} published books</span>
          <span>3 companies under one system</span>
        </div>
        <div class="button-row">
          <a class="btn" href="books.html">Shop the books</a>
          <a class="btn secondary" href="services.html">Explore services</a>
          <a class="btn secondary" href="command/">Open command platform</a>
          <a class="btn secondary" href="tel:{phone}">Call {phone}</a>
        </div>
      </div>
      <section class="hero-visual-panel glow-card">{render_sacred_visual()}</section>
    </section>
    <section class="section-block">
      <p class="eyebrow">Three company paths</p>
      <h2>One visual language, three specialized businesses, and a direct service ladder.</h2>
      <p class="section-copy">The homepage now carries the complete company architecture instead of forcing visitors to piece it together from separate environments.</p>
      <div class="grid-three">{render_company_cards(catalog)}</div>
    </section>
    <section class="section-block catalog-band">
      <section class="feature-panel glow-card">
        <p class="eyebrow">Book storefront</p>
        <h2>Every core book now has a visible price, reading page, and printable PDF path.</h2>
        <p>Use the books to bring visitors into the Focus language quickly, then route them into the higher-ticket operating system offers when they are ready for implementation.</p>
        <div class="button-row">
          <a class="btn" href="books.html">Browse book sales page</a>
          <a class="btn secondary" href="ebooks/index.html">Open reading library</a>
        </div>
      </section>
      <section class="feature-panel glow-card">
        <p class="eyebrow">Routing line</p>
        <h2>{escape(contact_name)}</h2>
        <p>For guided service routing, custom builds, or help choosing the right offer, call or text {phone}.</p>
        <div class="detail-list">
          <p><strong>Books</strong> Start with the book shelf and the digital library.</p>
          <p><strong>Services</strong> Move into company-specific strategy or build work.</p>
          <p><strong>Platform</strong> Use the command environment to frame the next execution packet.</p>
        </div>
      </section>
    </section>
    <section class="section-block">
      <p class="eyebrow">Service architecture</p>
      <h2>Global standardized pricing across every company path.</h2>
      <div class="detail-grid">{render_company_service_rows()}</div>
    </section>
    <section class="section-block">
      <p class="eyebrow">Core systems</p>
      <h2>The root experience now points directly into the products, the platform, and the operational spine.</h2>
      <div class="grid-three">{render_system_cards()}</div>
    </section>
  </main>
</body>
</html>
"""

    landing_page = f"""<!doctype html>
<html lang="en">
{head_html('Focus AI Sacred Landing', 'Launch-facing page for sacred geometry books, offers, and services.')}
<body>
  <main>
    {nav_html()}
    <section class="hero-panel luminous-hero">
      <div class="poster panel-flow">
        <p class="eyebrow">Launch page</p>
        <h1>Enter the Focus field without losing the practical next step.</h1>
        <p class="lede">This landing page keeps the sacred-geometry atmosphere, but it is still grounded in direct offers, visible pricing, and clear routing.</p>
        <div class="metric-strip">
          <span>{phone}</span>
          <span>Books + services + platform</span>
          <span>Mobile-first storefront</span>
        </div>
        <div class="button-row">
          <a class="btn" href="products.html">Enter the offer ladder</a>
          <a class="btn secondary" href="books.html">See the books</a>
          <a class="btn secondary" href="tel:{phone}">Call {phone}</a>
        </div>
      </div>
      <section class="hero-visual-panel glow-card">{render_sacred_visual()}</section>
    </section>
    <section class="section-block">
      <div class="track-grid">{render_track_cards(catalog)}</div>
    </section>
  </main>
</body>
</html>
"""

    services_page = f"""<!doctype html>
<html lang="en">
{head_html('Focus AI Services', 'Company pages and service pricing across the Focus AI ecosystem.')}
<body>
  <main>
    {nav_html()}
    <section class="hero-panel luminous-hero">
      <div class="poster panel-flow">
        <p class="eyebrow">Service routing</p>
        <h1>Choose the right company path without losing the unified customer experience.</h1>
        <p class="lede">Every service page now reflects the same sacred storefront language, mobile behavior, and pricing discipline while preserving what makes each company distinct.</p>
        <div class="button-row">
          <a class="btn" href="tel:{phone}">Call {phone}</a>
          <a class="btn secondary" href="booking.html">Book with {escape(contact_name)}</a>
          <a class="btn secondary" href="focus-negotium.html">Open Focus Negotium</a>
        </div>
      </div>
      <section class="feature-panel glow-card">
        <p class="eyebrow">Shared route</p>
        <h2>{escape(contact_name)}</h2>
        <p>Use {phone} for creative campaigns, sacred-geometry build strategy, or premium operations architecture.</p>
        <ul class="detail-list">
          <li>Focus Records LLC for campaign and creative launch work.</li>
          <li>Royal Lee Construction Solutions LLC for build strategy and geometric planning.</li>
          <li>Focus Negotium Inc for offer systems, automation, and monetization design.</li>
        </ul>
      </section>
    </section>
    <section class="section-block">
      <p class="eyebrow">Company service matrix</p>
      <h2>Reasonable global standardized pricing with deeper company pages behind each path.</h2>
      <div class="detail-grid">{render_company_service_rows()}</div>
    </section>
  </main>
</body>
</html>
"""

    products_page = f"""<!doctype html>
<html lang="en">
{head_html('Focus AI Products and Offers', 'Books, bundle offers, and implementation products on TheFocusCorp.com.')}
<body>
  <main>
    {nav_html()}
    <section class="hero-panel luminous-hero">
      <div class="poster panel-flow">
        <p class="eyebrow">Live revenue ladder</p>
        <h1>Move from books and digital assets into blueprint-level implementation and the full business engine.</h1>
        <p class="lede">The store now combines individual book pricing with the larger Focus AI offer ladder, so customers can start small or move directly into a premium build.</p>
        <div class="button-row">
          <a class="btn" href="books.html">Shop books</a>
          <a class="btn secondary" href="ebooks/index.html">Read the library</a>
          <a class="btn secondary" href="tel:{phone}">Call {phone}</a>
        </div>
      </div>
      <section class="feature-panel glow-card">
        <p class="eyebrow">Offer ladder</p>
        <ul class="detail-list">
          <li>Individual books starting at {_format_currency(min(book['price_usd'] for book in BOOK_CATALOG))}</li>
          <li>{_format_currency(float(catalog['offers'][0]['price_usd']))} bundle entry offer</li>
          <li>{_format_currency(float(catalog['offers'][1]['price_usd']))} blueprint depth offer</li>
          <li>{_format_currency(float(catalog['offers'][2]['price_usd']))} flagship business engine</li>
        </ul>
      </section>
    </section>
    <section class="section-block">
      <p class="eyebrow">Featured books</p>
      <div class="book-grid">{render_book_cards(phone, compact=True)}</div>
    </section>
    <section class="section-block">
      <p class="eyebrow">Implementation offers</p>
      <div class="offer-grid">{render_offer_cards(catalog)}</div>
    </section>
    <section class="section-block split-band">
      <section class="feature-panel glow-card">
        <p class="eyebrow">What buyers unlock</p>
        <ul class="detail-list">
          <li>Published teachings, frameworks, and sacred-geometry language.</li>
          <li>Reusable system prompts, service routing, and operator structure.</li>
          <li>One clear progression from knowledge product to custom implementation.</li>
        </ul>
      </section>
      {render_square_panel(catalog)}
    </section>
  </main>
</body>
</html>
"""

    books_page = f"""<!doctype html>
<html lang="en">
{head_html('Focus Books', 'Complete book sales page with sacred geometry titles, pricing, and PDF access.')}
<body>
  <main>
    {nav_html()}
    <section class="hero-panel luminous-hero">
      <div class="poster panel-flow">
        <p class="eyebrow">Focus Books</p>
        <h1>A sacred-geometry book shelf with visible pricing, online reading, and printable editions.</h1>
        <p class="lede">Every current book is now available as a readable web page and as a generated PDF, with pricing displayed clearly and the larger bundle still visible for faster conversion.</p>
        <div class="button-row">
          <a class="btn" href="ebooks/index.html">Open full library</a>
          <a class="btn secondary" href="{escape(catalog['offers'][0]['checkout_url'])}">Buy the bundle</a>
          <a class="btn secondary" href="tel:{phone}">Call {phone}</a>
        </div>
      </div>
      <section class="feature-panel glow-card">
        <p class="eyebrow">Bundle signal</p>
        <h2>{escape(catalog['offers'][0]['title'])}</h2>
        <p>{escape(catalog['offers'][0]['summary'])}</p>
        <p class="price-pill">{_format_currency(float(catalog['offers'][0]['price_usd']))}</p>
      </section>
    </section>
    <section class="section-block">
      <p class="eyebrow">Book shelf</p>
      <h2>Current Focus AI titles and prices.</h2>
      <div class="book-grid">{render_book_cards(phone)}</div>
    </section>
  </main>
</body>
</html>
"""

    business_os_page = f"""<!doctype html>
<html lang="en">
{head_html('Focus AI Business Operating System', 'Workflow stages, connected platforms, and the operating-system spine behind the storefront.')}
<body>
  <main>
    {nav_html()}
    <section class="hero-panel luminous-hero">
      <div class="poster panel-flow">
        <p class="eyebrow">Business operating system</p>
        <h1>The operational spine behind the storefront, services, books, and AI engine.</h1>
        <p class="lede">The sacred experience is only useful if the execution system underneath it is clear. This page shows the stage flow, the platform surfaces, and the connectors that support delivery.</p>
        <div class="button-row">
          <a class="btn" href="command/">Open command platform</a>
          <a class="btn secondary" href="machine.html">Use prompt studio</a>
          <a class="btn secondary" href="tel:{phone}">Call {phone}</a>
        </div>
      </div>
      <section class="hero-visual-panel glow-card">{render_sacred_visual()}</section>
    </section>
    <section class="section-block">
      <p class="eyebrow">Workflow stages</p>
      <h2>Stage logic for how Focus AI moves from intake to verified release.</h2>
      <div class="stage-grid">{render_stage_cards(catalog)}</div>
    </section>
    <section class="section-block">
      <p class="eyebrow">Operating surfaces</p>
      <div class="grid-three">{render_system_cards()}</div>
    </section>
    <section class="section-block">
      <p class="eyebrow">Connected platforms</p>
      <div class="detail-grid">{render_connector_cards(catalog)}</div>
    </section>
  </main>
</body>
</html>
"""

    booking_page = f"""<!doctype html>
<html lang="en">
{head_html(f'Book with {contact_name}', 'Book with the primary Focus AI routing contact for services, builds, and product guidance.')}
<body>
  <main>
    {nav_html()}
    <section class="hero-panel luminous-hero">
      <div class="poster panel-flow">
        <p class="eyebrow">Primary routing</p>
        <h1>Book with {escape(contact_name)}</h1>
        <p class="lede">Use one direct routing line for company selection, project framing, service clarity, book questions, or AI-engine planning.</p>
        <div class="metric-strip">
          <span>Call or text {phone}</span>
          <span>Creative, construction, and AI routing</span>
        </div>
        <div class="button-row">
          <a class="btn" href="tel:{phone}">Call {phone}</a>
          <a class="btn secondary" href="services.html">Review services</a>
          <a class="btn secondary" href="books.html">Review books</a>
        </div>
      </div>
      <section class="feature-panel glow-card">
        <p class="eyebrow">Best use cases</p>
        <ul class="detail-list">
          <li>Choosing the right company and service tier.</li>
          <li>Moving from book interest into deeper implementation.</li>
          <li>Routing a live project into the command or build flow.</li>
        </ul>
      </section>
    </section>
  </main>
</body>
</html>
"""

    machine_page = f"""<!doctype html>
<html lang="en">
{head_html('Master Prompt Studio', 'Prompt compiler for translating rough intent into a stage-aware execution packet.')}
<body>
  <main>
    {nav_html()}
    <section class="hero-panel luminous-hero">
      <div class="poster panel-flow">
        <p class="eyebrow">Master Prompt Studio</p>
        <h1>Turn rough intent into a stronger execution packet before the build starts.</h1>
        <p class="lede">This studio stays browser-native so the prompt layer is always available, even before every remote connector is fully configured.</p>
        <div class="metric-strip">
          <span>Engine sequencing</span>
          <span>Connector-aware outputs</span>
          <span>Sacred execution framing</span>
        </div>
        <div class="button-row">
          <a class="btn" href="command/">Open command platform</a>
          <a class="btn secondary" href="products.html">Return to products</a>
        </div>
      </div>
      <section class="feature-panel glow-card">
        <p class="eyebrow">What it creates</p>
        <ul class="detail-list">
          <li>A primary engine recommendation based on the task itself.</li>
          <li>A deliberate engine chain instead of one flat response.</li>
          <li>A reusable master prompt plus action checklist and connector targets.</li>
        </ul>
      </section>
    </section>
    <section class="section-block split-band">
      <section class="feature-panel glow-card">
        <label class="eyebrow" for="studio-task">Raw task</label>
        <textarea id="studio-task" style="width:100%;min-height:240px;padding:1rem;border-radius:20px;border:1px solid rgba(124,200,255,0.18);background:rgba(6,13,26,0.58);color:var(--ink);font:inherit;">Take the next Focus task, refine the prompt, route the right engines, include AI twin support when helpful, and prepare the cleanest next actions.</textarea>
        <div class="button-row" style="margin-top:0.9rem;">
          <button class="btn" id="studio-generate" type="button">Compile prompt packet</button>
          <button class="btn secondary" id="studio-copy" type="button">Copy packet</button>
          <button class="btn secondary" id="studio-download" type="button">Download markdown</button>
        </div>
      </section>
      <section class="feature-panel glow-card">
        <p class="eyebrow">Compiled packet</p>
        <pre id="studio-output" style="margin:0;min-height:340px;padding:1rem;border-radius:20px;background:rgba(4,10,22,0.9);color:#edf4ff;overflow:auto;font-family:Consolas,monospace;white-space:pre-wrap;">Generate the packet to fill this panel.</pre>
      </section>
    </section>
    <script src="master_prompt_studio.js"></script>
  </main>
</body>
</html>
"""

    rlc_page = f"""<!doctype html>
<html lang="en">
{head_html('Royal Lee Construction Package', 'Live RLC office package with bid totals, drawing previews, and checklist context.')}
<body>
  <main>
    {nav_html()}
    <section class="hero-panel luminous-hero">
      <div class="poster panel-flow">
        <p class="eyebrow">Royal Lee Construction Solutions LLC</p>
        <h1>522 Vermont office package with live bid context and downloadable materials.</h1>
        <p class="lede">The construction package is now woven into the same sacred storefront rather than isolated as a separate artifact.</p>
        <div class="metric-strip">
          <span>Total bid {rlc_summary.get('Total Bid', '$0.00')}</span>
          <span>Materials {rlc_summary.get('Materials Total', '$0.00')}</span>
          <span>{_rlc_line_item_count()} takeoff lines</span>
        </div>
        <div class="button-row">
          <a class="btn" href="rlc/bid_summary.json">Download bid summary</a>
          <a class="btn secondary" href="rlc/material_list.csv">Download material list</a>
          <a class="btn secondary" href="royal-lee-construction.html">Open RLC services</a>
        </div>
      </div>
      <section class="feature-panel glow-card">
        <p class="eyebrow">Checklist context</p>
        <ul class="detail-list">{''.join(f'<li>{escape(item)}</li>' for item in rlc_checklist[:6])}</ul>
      </section>
    </section>
    <section class="drawing-grid">
      <figure class="drawing-frame">
        <img src="rlc/first_floor.svg" alt="First floor drawing preview" />
        <figcaption>First floor preview for the office package.</figcaption>
      </figure>
      <figure class="drawing-frame">
        <img src="rlc/second_floor.svg" alt="Second floor drawing preview" />
        <figcaption>Second floor preview for the office package.</figcaption>
      </figure>
    </section>
  </main>
</body>
</html>
"""

    email_automation = f"""<!doctype html>
<html lang="en">
{head_html('Email Automation Sequence', 'Follow-up sequence for moving readers into Focus AI offers.')}
<body>
  <main>
    {nav_html()}
    <section class="hero-panel luminous-hero">
      <div class="poster panel-flow">
        <p class="eyebrow">Follow-up sequence</p>
        <h1>Five email moments that move a reader into the live offer ladder.</h1>
        <p class="lede">This sequence is designed to lift a reader from a book, PDF, or free download into a more deliberate implementation path.</p>
      </div>
      <section class="feature-panel glow-card">
        <p class="eyebrow">Scale framing</p>
        <p>Weekly revenue depends on traffic, conversion, and disciplined follow-up. This sequence frames the motion, not a guaranteed result.</p>
      </section>
    </section>
    <section class="stage-grid">
      <article class="stage-card glow-card"><p class="eyebrow">Email 1</p><h3>Your blueprint is inside</h3><p>Deliver the lead magnet, then point to {escape(catalog['offers'][0]['title'])}.</p></article>
      <article class="stage-card glow-card"><p class="eyebrow">Email 2</p><h3>Why most systems fail</h3><p>Frame the cost of confusion, then return to the bundle.</p></article>
      <article class="stage-card glow-card"><p class="eyebrow">Email 3</p><h3>Architecture changes everything</h3><p>Move into the blueprint pack.</p></article>
      <article class="stage-card glow-card"><p class="eyebrow">Email 4</p><h3>System over inspiration</h3><p>Show the value of deeper operating materials.</p></article>
      <article class="stage-card glow-card"><p class="eyebrow">Email 5</p><h3>Ready for the full engine?</h3><p>Present the business engine as the flagship step.</p></article>
    </section>
  </main>
</body>
</html>
"""

    return {
        "index.html": home_page,
        "landing.html": landing_page,
        "services.html": services_page,
        "products.html": products_page,
        "books.html": books_page,
        "business_os.html": business_os_page,
        "booking.html": booking_page,
        "machine.html": machine_page,
        "rlc-office-package.html": rlc_page,
        "funnel_landing.html": landing_page,
        "delivery.html": books_page,
        "book_offer.html": products_page,
        "upsell.html": products_page,
        "high_ticket.html": business_os_page,
        "email_automation.html": email_automation,
        **{company["slug"]: render_company_page(company, contact_name, phone) for company in COMPANY_PROFILES},
    }


def build() -> int:
    if not PUBLISHED.exists():
        print("Missing published ebooks. Run publish_ebooks.py first.")
        return 1

    catalog = load_catalog()
    if PUBLIC.exists():
        safe_rmtree(PUBLIC)
    PUBLIC.mkdir(parents=True, exist_ok=True)

    copy_tree(PUBLISHED, PUBLIC / "ebooks")
    copy_tree(COMMAND_APP, PUBLIC / "command")
    copy_tree(RLC_OUTPUT, PUBLIC / "rlc")

    (PUBLIC / "funnel.css").write_text(build_css(catalog), encoding="utf-8")
    if MASTER_PROMPT_SCRIPT.exists():
        shutil.copy2(MASTER_PROMPT_SCRIPT, PUBLIC / "master_prompt_studio.js")

    data_dir = PUBLIC / "data"
    data_dir.mkdir(parents=True, exist_ok=True)
    (data_dir / "business_os.json").write_text(json.dumps(public_catalog(catalog), indent=2), encoding="utf-8")
    if ENGINE_STAGES.exists():
        shutil.copy2(ENGINE_STAGES, data_dir / "stages.json")

    pages = build_pages(catalog)
    for page_name, page_content in pages.items():
        (PUBLIC / page_name).write_text(page_content, encoding="utf-8")

    (PUBLIC / ".htaccess").write_text(ROOT_HTACCESS, encoding="utf-8")
    print(f"Built public site at {PUBLIC}")
    return 0


if __name__ == "__main__":
    raise SystemExit(build())
