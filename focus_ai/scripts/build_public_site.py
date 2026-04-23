#!/usr/bin/env python3
from __future__ import annotations

import json
import os
import shutil
import stat
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = ROOT.parent
CONFIG = ROOT / "config" / "business_os.json"
PUBLISHED = ROOT / "published" / "ebooks"
SITE = ROOT / "site"
PUBLIC = ROOT / "published" / "public_site"
COMMAND_APP = REPO_ROOT / "app"
ENGINE_STAGES = REPO_ROOT / "engine" / "stages.json"
MASTER_PROMPT_SCRIPT = SITE / "master_prompt_studio.js"
RLC_OUTPUT = REPO_ROOT / "construction" / "rlc_office_pkg_extracted" / "output"
RLC_CHECKLIST = REPO_ROOT / "construction" / "rlc_bid_input_checklist.md"


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


def _format_phone_display(value: str) -> str:
    digits = "".join(char for char in value if char.isdigit())
    if len(digits) == 10:
        return f"({digits[:3]}) {digits[3:6]}-{digits[6:]}"
    return value


def _ebook_count() -> int:
    return len(list((ROOT / "ebooks").glob("*.md")))


def _rlc_bid_summary() -> dict[str, str]:
    if not RLC_OUTPUT.joinpath("bid_summary.json").exists():
        return {}
    data = json.loads(RLC_OUTPUT.joinpath("bid_summary.json").read_text(encoding="utf-8"))
    return {
        item["Label"]: _format_currency(float(item["Amount"]))
        for item in data
    }


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


def head_html(title: str) -> str:
    return f"""<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>{title}</title>
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@500;600;700&family=Space+Grotesk:wght@400;500;700&display=swap" rel="stylesheet" />
  <link rel="stylesheet" href="funnel.css" />
</head>"""


def nav_html() -> str:
    return (
        '<nav class="top-nav">'
        '<a href="index.html">Home</a>'
        '<a href="machine.html">Prompt Studio</a>'
        '<a href="command/">Command Center</a>'
        '<a href="rlc-office-package.html">RLC Package</a>'
        '<a href="business_os.html">Business OS</a>'
        '<a href="services.html">Services</a>'
        '<a href="products.html">Products</a>'
        '<a href="ebooks/index.html">Library</a>'
        '<a href="booking.html">Booking</a>'
        "</nav>"
    )


def render_company_cards(catalog: dict) -> str:
    accents = catalog["design_system"]["company_accents"]
    cards = []
    for company in catalog.get("companies", []):
        accent = accents.get(company["accent_key"], {})
        capabilities = "".join(f"<li>{item}</li>" for item in company.get("capabilities", []))
        cards.append(
            f"""
<article class="info-card" style="--accent:{accent.get('accent', '#7CC8FF')};">
  <p class="eyebrow">{accent.get('label', 'Business Unit')}</p>
  <h3>{company['name']}</h3>
  <p>{company['tagline']}</p>
  <ul class="detail-list">{capabilities}</ul>
</article>
""".strip()
        )
    return "\n".join(cards)


def render_offer_cards(catalog: dict) -> str:
    cards = []
    for offer in catalog.get("offers", []):
        cards.append(
            f"""
<article class="offer-card">
  <p class="eyebrow">{offer['title']}</p>
  <h3>{offer['title']}</h3>
  <p>{offer['summary']}</p>
  <p class="price">${offer['price_usd']:,} USD</p>
  <div class="button-row">
    <a class="btn" href="{offer['checkout_url']}">{offer['cta_label']}</a>
  </div>
</article>
""".strip()
        )
    return "\n".join(cards)


def render_track_cards(catalog: dict) -> str:
    return "\n".join(
        f"""
<article class="track-card">
  <p class="eyebrow">{track['title']}</p>
  <h3>{track['title']}</h3>
  <p>{track['summary']}</p>
</article>
""".strip()
        for track in catalog["portal"]["tracks"]
    )


def render_stage_cards(catalog: dict) -> str:
    return "\n".join(
        f"""
<article class="stage-card">
  <p class="eyebrow">{stage['label']}</p>
  <h3>{stage['label']}</h3>
  <p>{stage['description']}</p>
</article>
""".strip()
        for stage in catalog.get("workflow_stages", [])
    )


def render_automation_cards(catalog: dict) -> str:
    return "\n".join(
        f"""
<article class="stage-card">
  <p class="eyebrow">{item['title']}</p>
  <h3>{item['title']}</h3>
  <p>{item['summary']}</p>
</article>
""".strip()
        for item in catalog.get("automation_categories", [])
    )


def render_connector_cards(catalog: dict) -> str:
    return "\n".join(
        f"""
<article class="stage-card">
  <p class="eyebrow">{connector['category'].title()}</p>
  <h3>{connector['label']}</h3>
  <p>{connector['notes']}</p>
  <p class="small">Status: {connector.get('status', connector.get('mode', 'unknown'))}</p>
</article>
""".strip()
        for connector in catalog.get("connectors", [])
    )


def render_system_cards(catalog: dict) -> str:
    systems = [
        {
            "eyebrow": "Storefront + services",
            "title": "TheFocusCorp.com",
            "summary": "Sell the eBook library, route service inquiries, and move visitors through the live offer ladder.",
            "href": "products.html",
            "cta": "Browse offers",
        },
        {
            "eyebrow": "No-key prompt compiler",
            "title": "Master Prompt Studio",
            "summary": "Turn one rough task into a stronger execution packet with engine sequencing, connectors, and AI twin guidance.",
            "href": "machine.html",
            "cta": "Open the studio",
        },
        {
            "eyebrow": "Daily command app",
            "title": "The Eye of Focus",
            "summary": "Start the day with a reusable 11-stage command brief that carries the work cleanly into the next tool.",
            "href": "command/",
            "cta": "Enter command mode",
        },
    ]
    return "\n".join(
        f"""
<article class="feature-panel">
  <p class="eyebrow">{item['eyebrow']}</p>
  <h3>{item['title']}</h3>
  <p>{item['summary']}</p>
  <div class="button-row"><a class="btn secondary" href="{item['href']}">{item['cta']}</a></div>
</article>
""".strip()
        for item in systems
    )


def build_css(catalog: dict) -> str:
    colors = catalog["design_system"]["core"]["colors"]
    display = catalog["design_system"]["core"]["typography"]["display_family"]
    body = catalog["design_system"]["core"]["typography"]["body_family"]
    template = """
:root {
  --bg-900: __BG900__;
  --bg-800: __BG800__;
  --panel: __PANEL__;
  --ink: __INK__;
  --muted: __MUTED__;
  --gold: __GOLD__;
  --teal: __TEAL__;
  --sky: __SKY__;
  --ember: __EMBER__;
  --line: rgba(124, 200, 255, 0.24);
  --shadow: 0 24px 60px rgba(2, 8, 24, 0.45);
  --display: __DISPLAY__;
  --body: __BODY__;
}

* { box-sizing: border-box; }
html { scroll-behavior: smooth; }
body {
  margin: 0;
  color: var(--ink);
  font-family: var(--body);
  background:
    radial-gradient(900px 520px at 10% 2%, rgba(62, 228, 214, 0.12), transparent 60%),
    radial-gradient(760px 460px at 92% 4%, rgba(242, 201, 109, 0.14), transparent 55%),
    linear-gradient(165deg, var(--bg-900), var(--bg-800) 48%, #08172e 100%);
}
a { color: var(--sky); text-decoration: none; }
a:hover { text-decoration: underline; }
main { max-width: 1180px; margin: 0 auto; padding: 1.2rem clamp(1rem, 3vw, 2.2rem) 4rem; }
.top-nav { display: flex; flex-wrap: wrap; gap: 1rem; padding: 0.8rem 0 1.2rem; margin-bottom: 1rem; border-bottom: 1px solid rgba(122, 168, 255, 0.16); }
.top-nav a { color: var(--ink); opacity: 0.88; font-size: 0.96rem; }
h1,h2,h3 { margin: 0; font-family: var(--display); line-height: 1.05; }
h1 { font-size: clamp(2.4rem, 6vw, 4.8rem); }
h2 { font-size: clamp(1.8rem, 4vw, 3rem); }
h3 { font-size: clamp(1.35rem, 2.4vw, 1.9rem); }
p, li { color: var(--muted); line-height: 1.65; }
.hero-panel,.feature-panel,.offer-card,.info-card,.track-card,.stage-card { border: 1px solid var(--line); border-radius: 24px; background: linear-gradient(155deg, rgba(9, 18, 35, 0.84), rgba(15, 30, 58, 0.72)); box-shadow: var(--shadow); }
.hero-panel { display: grid; grid-template-columns: minmax(0, 1.15fr) minmax(260px, 0.85fr); gap: 1.2rem; padding: clamp(1.3rem, 4vw, 2.4rem); }
.poster,.feature-panel { display: grid; gap: 0.8rem; align-content: start; }
.eyebrow { margin: 0; color: var(--gold); letter-spacing: 0.14em; text-transform: uppercase; font-size: 0.78rem; font-weight: 700; }
.button-row { display: flex; flex-wrap: wrap; gap: 0.8rem; margin-top: 0.9rem; }
.btn { display: inline-flex; align-items: center; justify-content: center; min-height: 48px; padding: 0.82rem 1.15rem; border-radius: 999px; font-weight: 700; background: linear-gradient(120deg, var(--gold), #ffd98f 52%, var(--ember)); color: #1c1420; border: 1px solid transparent; cursor: pointer; }
.btn.secondary { background: rgba(8, 15, 31, 0.6); color: var(--ink); border-color: rgba(124, 200, 255, 0.32); }
.orbital-graphic { min-height: 300px; border-radius: 22px; background: radial-gradient(circle at center, rgba(242, 201, 109, 0.14), transparent 34%), repeating-conic-gradient(from 0deg, rgba(124, 200, 255, 0.08) 0deg 10deg, transparent 10deg 24deg), linear-gradient(145deg, rgba(11, 22, 46, 0.88), rgba(6, 13, 28, 0.92)); position: relative; }
.orbital-graphic::before,.orbital-graphic::after { content: ""; position: absolute; inset: 16%; border-radius: 50%; border: 1px solid rgba(242, 201, 109, 0.35); }
.orbital-graphic::after { inset: 28%; border-color: rgba(62, 228, 214, 0.4); }
.section-block { margin-top: 1.35rem; }
.grid-three,.offer-grid,.track-grid,.stage-grid,.detail-grid,.split-band { display: grid; gap: 1rem; }
.grid-three,.offer-grid,.track-grid { grid-template-columns: repeat(3, minmax(0, 1fr)); }
.stage-grid,.detail-grid,.split-band { grid-template-columns: repeat(2, minmax(0, 1fr)); }
.feature-panel,.offer-card,.info-card,.track-card,.stage-card { padding: 1.1rem; }
.info-card::before { content: ""; display: block; width: 4px; height: 36px; border-radius: 999px; background: var(--accent, var(--sky)); margin-bottom: 0.7rem; }
.detail-list,.kicker-list { margin: 0.8rem 0 0; padding-left: 1.1rem; }
.price { color: #ffe0a0; font-weight: 700; font-size: 1.08rem; }
.small { font-size: 0.93rem; opacity: 0.88; }
.status-chip { display: inline-flex; align-items: center; min-height: 28px; padding: 0.25rem 0.75rem; border-radius: 999px; background: rgba(62,228,214,0.12); color: var(--teal); font-size: 0.82rem; }
.metric-strip { display: flex; flex-wrap: wrap; gap: 0.75rem; margin-top: 0.9rem; }
.metric-strip span { display: inline-flex; align-items: center; min-height: 34px; padding: 0.25rem 0.8rem; border-radius: 999px; border: 1px solid rgba(124, 200, 255, 0.24); background: rgba(8, 15, 31, 0.5); color: var(--ink); font-size: 0.9rem; }
.section-copy { max-width: 66ch; margin: 0.55rem 0 0; }
.panel-stack { display: grid; gap: 1rem; }
.story-note { margin-top: 0.85rem; padding-left: 1rem; border-left: 3px solid rgba(242, 201, 109, 0.4); color: var(--ink); }
.support-list li + li { margin-top: 0.32rem; }
.studio-layout,.drawing-grid { display: grid; gap: 1rem; grid-template-columns: repeat(2, minmax(0, 1fr)); }
.studio-panel { min-height: 100%; }
.studio-label { display: block; color: var(--ink); font-weight: 700; }
.studio-input,.inline-form input { width: 100%; margin-top: 0.55rem; min-height: 240px; padding: 0.9rem 1rem; border-radius: 18px; border: 1px solid rgba(124, 200, 255, 0.24); background: rgba(8, 15, 31, 0.74); color: var(--ink); font: inherit; resize: vertical; }
.inline-form input { min-height: auto; }
.studio-actions { display: flex; flex-wrap: wrap; gap: 0.8rem; margin-top: 0.9rem; }
.studio-output { min-height: 520px; margin: 0; white-space: pre-wrap; background: rgba(6, 13, 27, 0.9); border: 1px solid rgba(124, 200, 255, 0.18); border-radius: 20px; padding: 1rem; color: #e9f1ff; font-family: "IBM Plex Mono", "SFMono-Regular", Consolas, monospace; line-height: 1.58; overflow-x: auto; }
.studio-summary { display: grid; gap: 0.3rem; margin-top: 0.9rem; padding: 0.85rem 1rem; border-radius: 18px; background: rgba(8, 15, 31, 0.5); border: 1px solid rgba(124, 200, 255, 0.18); }
.download-strip { display: flex; flex-wrap: wrap; gap: 0.8rem; margin-top: 0.9rem; }
.drawing-frame { padding: 1rem; border-radius: 24px; border: 1px solid var(--line); background: linear-gradient(155deg, rgba(9, 18, 35, 0.84), rgba(15, 30, 58, 0.72)); box-shadow: var(--shadow); }
.drawing-frame img { width: 100%; height: auto; display: block; border-radius: 18px; background: #ffffff; }
.drawing-frame figcaption { margin-top: 0.8rem; color: var(--muted); }
@media (max-width: 960px) { .hero-panel,.grid-three,.offer-grid,.track-grid,.stage-grid,.detail-grid,.split-band { grid-template-columns: 1fr; } }
@media (max-width: 960px) { .studio-layout,.drawing-grid { grid-template-columns: 1fr; } }
@media (max-width: 640px) { .button-row,.studio-actions,.download-strip { flex-direction: column; } .btn { width: 100%; } }
"""
    for key, value in {
        "__BG900__": colors["bg_900"],
        "__BG800__": colors["bg_800"],
        "__PANEL__": colors["panel"],
        "__INK__": colors["ink"],
        "__MUTED__": colors["muted"],
        "__GOLD__": colors["gold"],
        "__TEAL__": colors["teal"],
        "__SKY__": colors["sky"],
        "__EMBER__": colors["ember"],
        "__DISPLAY__": display,
        "__BODY__": body,
    }.items():
        template = template.replace(key, value)
    return template.strip() + "\n"


def render_square_panel(catalog: dict) -> str:
    square = catalog["portal"]["payment_processors"]["square"]
    buttons = []
    if square.get("payment_links_url"):
        buttons.append(f'<a class="btn secondary" href="{square["payment_links_url"]}">Pay with Square</a>')
    if square.get("buy_button_url"):
        buttons.append(f'<a class="btn secondary" href="{square["buy_button_url"]}">Square Buy Button</a>')
    if not buttons:
        buttons.append(f'<a class="btn secondary" href="{square["setup_url"]}">Square setup path</a>')
    return f"""
<section class="feature-panel">
  <p class="eyebrow">Square-ready payment path</p>
  <h2>Square support is now wired into the catalog and site build.</h2>
  <p>{square['summary']}</p>
  <p class="small">Status: {square['status']}</p>
  <div class="button-row">{''.join(buttons)}</div>
</section>
""".strip()


def build_pages(catalog: dict) -> dict[str, str]:
    contact = catalog["portal"]["primary_contact"]
    contact_phone_href = "".join(char for char in contact["phone"] if char.isdigit())
    contact_phone_display = contact.get("phone_display") or _format_phone_display(contact["phone"])
    ebook_count = _ebook_count()
    rlc_summary = _rlc_bid_summary()
    rlc_checklist = _rlc_checklist_items()
    hero = f"""
<section class="hero-panel">
  <div class="poster">
    <p class="eyebrow">{catalog['portal']['site_name']}</p>
    <h1>One operating system for revenue, sacred design, mobile delivery, and AI execution.</h1>
    <p>{catalog['portal']['visual_thesis']}</p>
    <p>Focus AI routes customers through Focus Records LLC, Royal Lee Construction Solutions LLC, and Focus Negotium Inc with one shared offer ladder, one shared routing contact, and one assistant control plane.</p>
    <div class="metric-strip">
      <span>Routing contact {contact['name']}</span>
      <span>Call or text {contact_phone_display}</span>
      <span>3 companies, 1 machine</span>
    </div>
    <div class="button-row">
      <a class="btn" href="products.html">Enter the revenue ladder</a>
      <a class="btn secondary" href="tel:{contact_phone_href}">Call {contact_phone_display}</a>
      <a class="btn secondary" href="business_os.html">See the full business OS</a>
      <a class="btn secondary" href="booking.html">Book with {contact['name']}</a>
    </div>
  </div>
  <section class="feature-panel signal-panel">
    <p class="eyebrow">Primary routing</p>
    <h2>{contact['name']}</h2>
    <p>Use the same routing line for services, product questions, construction scope reviews, and AI engine handoff planning.</p>
    <div class="button-row">
      <a class="btn secondary" href="tel:{contact_phone_href}">Call {contact_phone_display}</a>
      <a class="btn secondary" href="booking.html">Open booking</a>
    </div>
    <ul class="kicker-list support-list">
      <li>Creative planning and release support.</li>
      <li>Sacred-geometry design and build strategy.</li>
      <li>Automation, monetization, and premium offer routing.</li>
    </ul>
  </section>
</section>
""".strip()

    home_page = f"""<!doctype html>
<html lang="en">
{head_html("TheFocusCorp.com")}
<body><main>
  {nav_html()}
  {hero}
  <section class="section-block">
    <p class="eyebrow">Root storefront</p>
    <h2>The root homepage now carries the same sacred storefront language as the rest of the static launch.</h2>
    <p class="section-copy">TheFocusCorp.com now opens with the same visual system, contact routing, and offer hierarchy used across the public launch pages, so visitors are not stepping from an old WordPress shell into a different product world.</p>
    <div class="grid-three">{render_system_cards(catalog)}</div>
  </section>
  <section class="section-block">
    <div class="split-band">
      <section class="feature-panel">
        <p class="eyebrow">Royal Lee Construction</p>
        <h2>522 Vermont bid package is now part of the experience.</h2>
        <p>Surface the office package with cost summary, plan visuals, checklist context, and download-ready attachments.</p>
        <div class="button-row">
          <a class="btn" href="rlc-office-package.html">Open the RLC package</a>
          <a class="btn secondary" href="booking.html">Book with {contact['name']}</a>
        </div>
      </section>
      <section class="feature-panel">
        <p class="eyebrow">Primary routing</p>
        <h2>One direct line handles products, services, and engine handoff planning.</h2>
        <p>Call or text {contact['name']} at {contact_phone_display} to route service questions, book strategy time, or move straight into the premium offer ladder.</p>
        <div class="button-row">
          <a class="btn" href="tel:{contact_phone_href}">Call {contact_phone_display}</a>
          <a class="btn secondary" href="booking.html">Open booking</a>
        </div>
        <p class="story-note">Routing stays human-first while the automation layers prepare prompts, content, checkout surfaces, and delivery-ready assets behind the scenes.</p>
      </section>
    </div>
  </section>
  <section class="section-block">
    <p class="eyebrow">Three companies, one design core</p>
    <h2>Each company keeps its own promise while sharing one visual language and one conversion path.</h2>
    <p class="section-copy">This keeps the storefront coherent for visitors while preserving the depth needed for media, construction strategy, and monetization work.</p>
    <div class="grid-three">{render_company_cards(catalog)}</div>
  </section>
  <section class="section-block"><div class="track-grid">{render_track_cards(catalog)}</div></section>
</main></body></html>
"""

    products_page = f"""<!doctype html>
<html lang="en">
{head_html("Products and Offers")}
<body><main>
  {nav_html()}
  <section class="hero-panel">
    <div class="poster">
      <p class="eyebrow">Live revenue surface</p>
      <h1>The Focus AI ladder moves from insight to implementation to the full business engine.</h1>
      <p>Stripe payment links are live now, and Square-ready support has been added so the site can expose Square payment links or buy buttons as soon as live URLs are available.</p>
      <div class="button-row">
        <a class="btn" href="{catalog['offers'][0]['checkout_url']}">{catalog['offers'][0]['cta_label']}</a>
        <a class="btn secondary" href="ebooks/index.html">Browse the library</a>
        <a class="btn secondary" href="tel:{contact_phone_href}">Call {contact_phone_display}</a>
      </div>
    </div>
    <section class="feature-panel">
      <p class="eyebrow">Offer ladder</p>
      <p class="small">If you want a guided route instead of a direct checkout, call or text {contact['name']} at {contact_phone_display}.</p>
      <ul class="kicker-list">
        <li>$49 bundle for fast entry and proof of value.</li>
        <li>$299 blueprint pack for practical implementation depth.</li>
        <li>$5,000 business engine for the flagship operating-system offer.</li>
      </ul>
    </section>
  </section>
  <section class="section-block">
    <div class="offer-grid">{render_offer_cards(catalog)}</div>
  </section>
  <section class="split-band">
    <section class="feature-panel">
      <p class="eyebrow">What buyers unlock</p>
      <ul class="kicker-list">
        <li>Published content, prompts, and operating materials.</li>
        <li>Shared design direction across the portal, app, and campaigns.</li>
        <li>Assistant-ready structure for deployment, follow-up, and optimization.</li>
      </ul>
    </section>
    {render_square_panel(catalog)}
  </section>
</main></body></html>
"""

    machine_page = f"""<!doctype html>
<html lang="en">
{head_html("Master Prompt Studio")}
<body><main>
  {nav_html()}
  <section class="hero-panel">
    <div class="poster">
      <p class="eyebrow">No-key prompt compiler</p>
      <h1>Turn one rough task into a stronger execution packet.</h1>
      <p>This studio runs directly in the browser so the site stays useful even before every remote connector is fully configured.</p>
      <div class="metric-strip">
        <span>Engine sequencing</span>
        <span>Connector-aware output</span>
        <span>AI twin layer when relevant</span>
      </div>
      <div class="button-row">
        <a class="btn" href="command/">Use The Eye of Focus next</a>
        <a class="btn secondary" href="products.html">Return to live offers</a>
      </div>
    </div>
    <section class="feature-panel">
      <p class="eyebrow">What it creates</p>
      <ul class="kicker-list">
        <li>A primary engine recommendation based on the task itself.</li>
        <li>A deliberate engine chain instead of one flat completion.</li>
        <li>A reusable master prompt plus action checklist and connector targets.</li>
      </ul>
    </section>
  </section>
  <section class="section-block studio-layout">
    <section class="feature-panel studio-panel">
      <label class="studio-label" for="studio-task">Raw task</label>
      <textarea id="studio-task" class="studio-input">Take the next Focus task, refine the prompt, route the right engines, include AI twin video support when helpful, and prepare the cleanest next actions.</textarea>
      <div class="studio-actions">
        <button class="btn" id="studio-generate" type="button">Compile prompt packet</button>
        <button class="btn secondary" id="studio-copy" type="button">Copy packet</button>
        <button class="btn secondary" id="studio-download" type="button">Download Markdown</button>
      </div>
      <div class="studio-summary" id="studio-summary"></div>
    </section>
    <section class="feature-panel studio-panel">
      <p class="eyebrow">Compiled packet</p>
      <pre class="studio-output" id="studio-output"></pre>
    </section>
  </section>
  <script src="master_prompt_studio.js"></script>
</main></body></html>
"""

    rlc_page = f"""<!doctype html>
<html lang="en">
{head_html("RLC Office Package")}
<body><main>
  {nav_html()}
  <section class="hero-panel">
    <div class="poster">
      <p class="eyebrow">Royal Lee Construction Solutions LLC</p>
      <h1>522 Vermont office package with live visual and download-ready surfaces.</h1>
      <p>This page carries the current bid summary, drawing previews, checklist context, and attachment links into one cleaner front-end experience.</p>
      <div class="metric-strip">
        <span>Total bid {rlc_summary.get('Total Bid', '$0.00')}</span>
        <span>Materials {rlc_summary.get('Materials Total', '$0.00')}</span>
        <span>{_rlc_line_item_count()} takeoff lines</span>
      </div>
      <div class="download-strip">
        <a class="btn" href="rlc/bid_summary.json">Download bid summary</a>
        <a class="btn secondary" href="rlc/material_list.csv">Download material list</a>
        <a class="btn secondary" href="booking.html">Route through {contact['name']}</a>
      </div>
    </div>
    <section class="feature-panel">
      <p class="eyebrow">Package checklist</p>
      <ul class="kicker-list">{''.join(f'<li>{item}</li>' for item in rlc_checklist[:6])}</ul>
      <p class="small">Official insurance certificates and business-license documents still require issuer-provided updates before final delivery.</p>
    </section>
  </section>
  <section class="section-block drawing-grid">
    <figure class="drawing-frame">
      <img src="rlc/first_floor.svg" alt="First floor drawing preview" />
      <figcaption>First floor preview for the office package.</figcaption>
    </figure>
    <figure class="drawing-frame">
      <img src="rlc/second_floor.svg" alt="Second floor drawing preview" />
      <figcaption>Second floor preview for the office package.</figcaption>
    </figure>
  </section>
  <section class="section-block split-band">
    <section class="feature-panel">
      <p class="eyebrow">Bid structure</p>
      <ul class="kicker-list">
        <li>Labor: {rlc_summary.get('Labor (Reduced by 2/3)', '$0.00')}</li>
        <li>Insurance fee: {rlc_summary.get('Insurance Fee', '$0.00')}</li>
        <li>Subtotal: {rlc_summary.get('Subtotal', '$0.00')}</li>
        <li>Overhead: {rlc_summary.get('Overhead (8%)', '$0.00')}</li>
      </ul>
    </section>
    <section class="feature-panel">
      <p class="eyebrow">Attachments</p>
      <div class="download-strip">
        <a class="btn secondary" href="rlc/insurance_license_summary.md">Insurance summary</a>
        <a class="btn secondary" href="rlc/first_floor.svg">First floor SVG</a>
        <a class="btn secondary" href="rlc/second_floor.svg">Second floor SVG</a>
      </div>
    </section>
  </section>
</main></body></html>
"""

    return {
        "index.html": home_page,
        "machine.html": machine_page,
        "rlc-office-package.html": rlc_page,
        "landing.html": f"""<!doctype html>
<html lang="en">
{head_html("Focus AI Public Launch")}
<body><main>
  {nav_html()}
  {hero}
  <section class="section-block"><div class="track-grid">{render_track_cards(catalog)}</div></section>
  <section class="split-band">
    <section class="feature-panel">
      <p class="eyebrow">Current live offers</p>
      <h2>Revenue path first, backed by deeper systems.</h2>
      <p>The portal is wired for live Stripe checkout and a Square-ready payment path.</p>
      <div class="button-row">
        <a class="btn" href="products.html">Browse offers</a>
        <a class="btn secondary" href="ebooks/index.html">View eBook library</a>
      </div>
    </section>
    <section class="feature-panel">
      <p class="eyebrow">Human routing stays visible</p>
      <h2>The launch page keeps one direct contact line in view while the engine stack handles the heavier lift.</h2>
      <p>Call or text {contact['name']} at {contact_phone_display} if you want the fastest path into booking, construction review, or the premium system.</p>
      <div class="button-row">
        <a class="btn secondary" href="tel:{contact_phone_href}">Call {contact_phone_display}</a>
        <a class="btn secondary" href="booking.html">Open booking</a>
      </div>
      <p class="small">Automation stops before legal, payroll, or banking execution.</p>
      <ul class="kicker-list">
        <li>High-risk workflows create readiness packs instead of taking final action.</li>
        <li>Low-risk workflows stay eligible for content, site, and campaign automation.</li>
        <li>Connected apps remain available for operator-approved release steps.</li>
      </ul>
    </section>
  </section>
</main></body></html>
""",
        "business_os.html": f"""<!doctype html>
<html lang="en">
{head_html("Focus AI Business Operating System")}
<body><main>
  {nav_html()}
  <section class="hero-panel">
    <div class="poster">
      <p class="eyebrow">Full-precedence operating model</p>
      <h1>Equal priority for revenue, design system, mobile shipping, and back-office automation.</h1>
      <p>The public portal lives in <strong>focus_ai</strong>. The internal assistant control plane lives in <strong>FOCUS_MASTER_AI</strong>. They share one catalog, one workflow map, and one operator-safe readiness policy.</p>
      <div class="metric-strip">
        <span>Primary routing {contact_phone_display}</span>
        <span>Shared contact {contact['name']}</span>
        <span>Readiness-first automation</span>
      </div>
      <div class="button-row">
        <a class="btn" href="products.html">Go to offers</a>
        <a class="btn secondary" href="tel:{contact_phone_href}">Call {contact_phone_display}</a>
        <a class="btn secondary" href="data/business_os.json">View shared data</a>
      </div>
    </div>
    <div class="orbital-graphic" aria-hidden="true"></div>
  </section>
  <section class="section-block">
    <p class="eyebrow">Operating companies</p>
    <h2>One design core, three business accents.</h2>
    <div class="grid-three">{render_company_cards(catalog)}</div>
  </section>
  <section class="section-block">
    <p class="eyebrow">Workflow stages</p>
    <h2>From intake to daily command mode.</h2>
    <div class="stage-grid">{render_stage_cards(catalog)}</div>
  </section>
  <section class="section-block">
    <p class="eyebrow">Automation categories</p>
    <h2>Recurring business loops the assistant can prepare and route.</h2>
    <div class="stage-grid">{render_automation_cards(catalog)}</div>
  </section>
  <section class="section-block">
    <p class="eyebrow">Connected platforms</p>
    <h2>Shared interfaces for delivery, payments, design, security, and ops.</h2>
    <div class="detail-grid">{render_connector_cards(catalog)}</div>
  </section>
</main></body></html>
""",
        "booking.html": f"""<!doctype html>
<html lang="en">
{head_html(f"Book with {contact['name']}")}
<body><main>
  {nav_html()}
  <section class="hero-panel">
    <div class="poster">
      <p class="eyebrow">Primary routing</p>
      <h1>Book with {contact['name']}</h1>
      <p>{contact['name']} is the central routing contact for Focus Records LLC, Royal Lee Construction Solutions LLC, and Focus Negotium Inc.</p>
      <div class="metric-strip">
        <span>Call or text {contact_phone_display}</span>
        <span>Creative, construction, and AI routing</span>
      </div>
      <div class="button-row">
        <a class="btn" href="tel:{contact_phone_href}">Call {contact_phone_display}</a>
        <a class="btn secondary" href="products.html">Review offers first</a>
      </div>
    </div>
    <section class="feature-panel">
      <p class="eyebrow">Best use cases</p>
      <ul class="kicker-list">
        <li>Creative planning and release support</li>
        <li>Build and sacred-geometry design strategy</li>
        <li>Automation, monetization, and product architecture</li>
      </ul>
      <p class="small">Until a calendar platform is connected, call or text to claim the next available slot.</p>
    </section>
  </section>
</main></body></html>
""",
        "services.html": f"""<!doctype html>
<html lang="en">
{head_html("Services Across Three Companies")}
<body><main>
  {nav_html()}
  <section class="hero-panel">
    <div class="poster">
      <p class="eyebrow">Service routing</p>
      <h1>Choose the right company path without losing the shared system underneath.</h1>
      <p>Each company has a distinct customer promise while still benefiting from the same design language, offer structure, and assistant workflow foundation.</p>
      <div class="button-row">
        <a class="btn" href="tel:{contact_phone_href}">Call {contact_phone_display}</a>
        <a class="btn" href="booking.html">Route me through {contact['name']}</a>
        <a class="btn secondary" href="business_os.html">See the operating system</a>
      </div>
    </div>
    <section class="feature-panel">
      <p class="eyebrow">Shared contact line</p>
      <h2>{contact['name']}</h2>
      <p>Call or text {contact_phone_display} for the fastest route into media support, sacred-geometry construction planning, or business-engine implementation.</p>
      <ul class="kicker-list support-list">
        <li>Creative planning and release support.</li>
        <li>Construction strategy and package review.</li>
        <li>Automation, prompt systems, and monetization design.</li>
      </ul>
    </section>
  </section>
  <section class="section-block"><div class="grid-three">{render_company_cards(catalog)}</div></section>
</main></body></html>
""",
        "products.html": products_page,
        "funnel_landing.html": f"""<!doctype html>
<html lang="en">
{head_html("Free Download - Sacred Geometry Wealth Blueprint")}
<body><main>
  {nav_html()}
  <section class="hero-panel">
    <div class="poster">
      <p class="eyebrow">Lead capture</p>
      <h1>Start with a free blueprint. Move into the live offer ladder when ready.</h1>
      <p>Use this entry point to capture interest, route visitors into the bundle, and keep follow-up anchored to the same operating-system story.</p>
      <form class="inline-form" action="delivery.html" method="get">
        <input type="email" placeholder="you@example.com" aria-label="Email address" required />
        <button class="btn" type="submit">Download now</button>
      </form>
      <div class="button-row"><a class="btn secondary" href="products.html">Skip to offers</a></div>
    </div>
    <section class="feature-panel">
      <p class="eyebrow">Download includes</p>
      <ul class="kicker-list">
        <li>Golden Ratio layout principles</li>
        <li>Value-building design language</li>
        <li>AI-assisted architecture strategy</li>
      </ul>
    </section>
  </section>
</main></body></html>
""",
        "delivery.html": f"""<!doctype html>
<html lang="en">
{head_html("Your Blueprint Is Ready")}
<body><main>
  {nav_html()}
  <section class="hero-panel">
    <div class="poster">
      <p class="eyebrow">Delivery</p>
      <h1>Your blueprint is on the way.</h1>
      <p>Check your inbox, then move into the bundle if you want the full library and operating materials immediately.</p>
      <div class="button-row"><a class="btn" href="book_offer.html">Continue to the bundle</a></div>
    </div>
    <section class="feature-panel">
      <p class="eyebrow">Next step</p>
      <h2>{catalog['offers'][0]['title']}</h2>
      <p>{catalog['offers'][0]['summary']}</p>
    </section>
  </section>
</main></body></html>
""",
        "book_offer.html": f"""<!doctype html>
<html lang="en">
{head_html(catalog['offers'][0]['title'])}
<body><main>
  {nav_html()}
  <section class="hero-panel">
    <div class="poster">
      <p class="eyebrow">Entry offer</p>
      <h1>{catalog['offers'][0]['title']}</h1>
      <p>{catalog['offers'][0]['summary']}</p>
      <p class="price">${catalog['offers'][0]['price_usd']:,} USD</p>
      <div class="button-row">
        <a class="btn" href="{catalog['offers'][0]['checkout_url']}">{catalog['offers'][0]['cta_label']}</a>
        <a class="btn secondary" href="upsell.html">See the next offer</a>
      </div>
    </div>
    <section class="feature-panel">
      <p class="eyebrow">Why it matters</p>
      <ul class="kicker-list">
        <li>Instant access to the published library.</li>
        <li>Practical prompts and frameworks for focused execution.</li>
        <li>Clear next path into implementation-grade assets.</li>
      </ul>
    </section>
  </section>
</main></body></html>
""",
        "upsell.html": f"""<!doctype html>
<html lang="en">
{head_html(catalog['offers'][1]['title'])}
<body><main>
  {nav_html()}
  <section class="hero-panel">
    <div class="poster">
      <p class="eyebrow">Core implementation offer</p>
      <h1>{catalog['offers'][1]['title']}</h1>
      <p>{catalog['offers'][1]['summary']}</p>
      <p class="price">${catalog['offers'][1]['price_usd']:,} USD</p>
      <div class="button-row">
        <a class="btn" href="{catalog['offers'][1]['checkout_url']}">{catalog['offers'][1]['cta_label']}</a>
        <a class="btn secondary" href="high_ticket.html">See the premium system</a>
      </div>
    </div>
    <section class="feature-panel">
      <p class="eyebrow">Includes</p>
      <ul class="kicker-list">
        <li>Business workflow assets</li>
        <li>Implementation guides</li>
        <li>Better conversion and launch structure</li>
      </ul>
    </section>
  </section>
</main></body></html>
""",
        "high_ticket.html": f"""<!doctype html>
<html lang="en">
{head_html(catalog['offers'][2]['title'])}
<body><main>
  {nav_html()}
  <section class="hero-panel">
    <div class="poster">
      <p class="eyebrow">Flagship premium offer</p>
      <h1>{catalog['offers'][2]['title']}</h1>
      <p>{catalog['offers'][2]['summary']}</p>
      <p class="price">${catalog['offers'][2]['price_usd']:,} USD</p>
      <div class="button-row">
        <a class="btn" href="{catalog['offers'][2]['checkout_url']}">{catalog['offers'][2]['cta_label']}</a>
        <a class="btn secondary" href="email_automation.html">View follow-up campaign</a>
      </div>
    </div>
    <section class="feature-panel">
      <p class="eyebrow">Operating guardrail</p>
      <p>The business engine can coordinate prompts, design, content, and launch execution while stopping short of autonomous legal, payroll, or banking execution.</p>
    </section>
  </section>
</main></body></html>
""",
        "email_automation.html": f"""<!doctype html>
<html lang="en">
{head_html("Email Automation Sequence")}
<body><main>
  {nav_html()}
  <section class="hero-panel">
    <div class="poster">
      <p class="eyebrow">Follow-up campaign</p>
      <h1>Five email moments that move readers into the live offer ladder.</h1>
      <p>Use Mailchimp, ConvertKit, or the control-plane content workflow to stage these messages and keep the CTA progression consistent.</p>
    </div>
    <section class="feature-panel">
      <p class="eyebrow">Scale framing</p>
      <p>Weekly revenue goals depend on traffic, conversion, and follow-up discipline. This page presents a working conversion model, not a guarantee.</p>
    </section>
  </section>
  <section class="stage-grid">
    <article class="stage-card"><p class="eyebrow">Email 1</p><h3>Your blueprint is inside</h3><p>Deliver the lead magnet, then point to <a href="{catalog['offers'][0]['checkout_url']}">{catalog['offers'][0]['title']}</a>.</p></article>
    <article class="stage-card"><p class="eyebrow">Email 2</p><h3>Why most systems fail</h3><p>Frame the cost of confusion, then return to the library bundle.</p></article>
    <article class="stage-card"><p class="eyebrow">Email 3</p><h3>Architecture changes everything</h3><p>Promote <a href="{catalog['offers'][1]['checkout_url']}">{catalog['offers'][1]['title']}</a> for practical implementation depth.</p></article>
    <article class="stage-card"><p class="eyebrow">Email 4</p><h3>System over inspiration</h3><p>Move the reader from theory to operating materials with the blueprint pack.</p></article>
    <article class="stage-card"><p class="eyebrow">Email 5</p><h3>Ready for the full engine?</h3><p>Present <a href="{catalog['offers'][2]['checkout_url']}">{catalog['offers'][2]['title']}</a> as the flagship step.</p></article>
  </section>
</main></body></html>
""",
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

    print(f"Built public site at {PUBLIC}")
    return 0


if __name__ == "__main__":
    raise SystemExit(build())
