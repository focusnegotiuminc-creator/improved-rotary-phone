#!/usr/bin/env python3
from __future__ import annotations

import json
import os
import shutil
import stat
import sys
from io import StringIO
import csv
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
RewriteRule ^command(/.*)?$ - [R=404,L]
RewriteRule ^machine\\.html$ - [R=404,L]
RewriteRule ^master_prompt_studio\\.js$ - [R=404,L]
RewriteRule ^index\\.php$ - [L]
RewriteCond %{REQUEST_FILENAME} -f [OR]
RewriteCond %{REQUEST_FILENAME} -d
RewriteRule ^ - [L]
RewriteRule . /index.php [L]
</IfModule>
"""
HOLDING_DIAGRAM_PATH = "generated/corporate/holding_structure.svg"
FOCUS_RECORDS_POSTERS = [
    "generated/focus-records/release_identity_board.svg",
    "generated/focus-records/firefly_campaign_board.svg",
    "generated/focus-records/licensing_market_board.svg",
]
RLC_CONCEPT_STUDIES = [
    "generated/architecture/courtyard_residence_study.svg",
    "generated/architecture/hexagonal_estate_plan.svg",
    "generated/architecture/development_cluster_study.svg",
]


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
        ("services.html", "Services"),
        ("store.html", "Store"),
        ("books.html", "Books"),
        ("structure.html", "Structure"),
        ("focus-negotium.html", "Focus Negotium"),
        ("focus-records.html", "Focus Records"),
        ("royal-lee-construction.html", "Construction"),
        ("ebooks/index.html", "Library"),
        ("booking.html", "Booking"),
    ]
    items = "".join(f'<a href="{href}">{label}</a>' for href, label in links)
    return (
        '<header class="site-header">'
        '<div class="brand-lockup"><span class="brand-mark"></span><div>'
        '<p class="eyebrow">TheFocusCorp.com</p><strong>The Focus Corporation | Businesses, Services, and Store</strong>'
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


def _brand_poster_svg(title: str, subtitle: str, accent_a: str, accent_b: str, kicker: str) -> str:
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="1400" height="960" viewBox="0 0 1400 960" role="img" aria-labelledby="title desc">
  <title>{escape(title)}</title>
  <desc>{escape(subtitle)}</desc>
  <defs>
    <linearGradient id="bg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#08111f" />
      <stop offset="100%" stop-color="#111d33" />
    </linearGradient>
    <linearGradient id="beam" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="{accent_a}" stop-opacity="0" />
      <stop offset="50%" stop-color="{accent_a}" stop-opacity="0.9" />
      <stop offset="100%" stop-color="{accent_b}" stop-opacity="0" />
    </linearGradient>
  </defs>
  <rect width="1400" height="960" rx="40" fill="url(#bg)" />
  <circle cx="1090" cy="210" r="190" fill="{accent_a}" opacity="0.13" />
  <circle cx="1180" cy="660" r="250" fill="{accent_b}" opacity="0.12" />
  <circle cx="970" cy="470" r="260" fill="none" stroke="{accent_a}" stroke-opacity="0.18" stroke-width="2" />
  <circle cx="970" cy="470" r="190" fill="none" stroke="{accent_b}" stroke-opacity="0.2" stroke-width="2" />
  <circle cx="970" cy="470" r="118" fill="none" stroke="#f2c96d" stroke-opacity="0.32" stroke-width="2" />
  <path d="M170 260 H1230" stroke="url(#beam)" stroke-width="2" />
  <path d="M150 560 H1260" stroke="url(#beam)" stroke-width="1.5" opacity="0.75" />
  <path d="M760 110 L1180 820" stroke="{accent_a}" stroke-opacity="0.16" stroke-width="2" />
  <path d="M520 90 L1180 840" stroke="{accent_b}" stroke-opacity="0.16" stroke-width="2" />
  <rect x="96" y="96" width="1208" height="768" rx="28" fill="none" stroke="#7cc8ff" stroke-opacity="0.18" />
  <text x="140" y="178" fill="#f2c96d" font-family="Manrope, Arial, sans-serif" font-size="28" letter-spacing="8">{escape(kicker.upper())}</text>
  <text x="140" y="316" fill="#f6f8ff" font-family="Cormorant Garamond, Georgia, serif" font-size="88" font-weight="700">{escape(title)}</text>
  <text x="140" y="386" fill="#d5def0" font-family="Manrope, Arial, sans-serif" font-size="30">{escape(subtitle)}</text>
  <text x="140" y="770" fill="#eef4ff" font-family="Manrope, Arial, sans-serif" font-size="24">The Focus Corporation</text>
  <text x="140" y="814" fill="#b8c9e8" font-family="Manrope, Arial, sans-serif" font-size="20">Creative campaign concept board</text>
</svg>
""".strip()


def _architecture_study_svg(title: str, subtitle: str, figure_label: str, accent: str) -> str:
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="1600" height="1080" viewBox="0 0 1600 1080" role="img" aria-labelledby="title desc">
  <title>{escape(title)}</title>
  <desc>{escape(subtitle)}</desc>
  <rect width="1600" height="1080" fill="#f4efe4" />
  <rect x="72" y="72" width="1456" height="936" fill="none" stroke="#202226" stroke-width="3" />
  <g stroke="#c5b59a" stroke-width="1">
    <path d="M160 180 H1440" /><path d="M160 260 H1440" /><path d="M160 340 H1440" /><path d="M160 420 H1440" />
    <path d="M160 500 H1440" /><path d="M160 580 H1440" /><path d="M160 660 H1440" /><path d="M160 740 H1440" />
    <path d="M160 820 H1440" /><path d="M160 900 H1440" />
    <path d="M220 150 V930" /><path d="M360 150 V930" /><path d="M500 150 V930" /><path d="M640 150 V930" />
    <path d="M780 150 V930" /><path d="M920 150 V930" /><path d="M1060 150 V930" /><path d="M1200 150 V930" /><path d="M1340 150 V930" />
  </g>
  <g fill="none" stroke="#111" stroke-width="5">
    <path d="M310 290 L620 190 L930 290 L1040 505 L930 720 L620 820 L310 720 L200 505 Z" />
    <path d="M620 190 V820" />
    <path d="M310 290 L930 720" />
    <path d="M930 290 L310 720" />
    <rect x="560" y="420" width="120" height="170" rx="8" />
    <rect x="760" y="420" width="120" height="170" rx="8" />
    <path d="M1040 505 H1270" />
    <path d="M620 820 V930" />
    <path d="M620 930 H980" />
    <path d="M980 820 V930" />
    <circle cx="620" cy="505" r="208" stroke="{accent}" stroke-width="3" opacity="0.55" />
    <circle cx="620" cy="505" r="120" stroke="{accent}" stroke-width="3" opacity="0.55" />
  </g>
  <g font-family="Helvetica, Arial, sans-serif" fill="#202226">
    <text x="130" y="130" font-size="22">{escape(figure_label)}</text>
    <text x="130" y="188" font-size="48">{escape(title)}</text>
    <text x="130" y="232" font-size="22">{escape(subtitle)}</text>
    <text x="1120" y="230" font-size="20">N</text>
    <path d="M1110 310 L1135 250 L1160 310 Z" fill="#202226" />
    <path d="M1135 250 V360" stroke="#202226" stroke-width="3" />
    <text x="1120" y="404" font-size="18">North</text>
    <text x="1120" y="488" font-size="18">Concept use: residential / development planning</text>
    <text x="1120" y="522" font-size="18">Drafted by Reginald Hilton</text>
    <text x="1120" y="556" font-size="18">Verify field dimensions before fabrication</text>
    <text x="1120" y="720" font-size="18">Scale reference</text>
    <path d="M1110 750 H1400" stroke="#202226" stroke-width="3" />
    <path d="M1110 740 V760" stroke="#202226" stroke-width="3" />
    <path d="M1255 740 V760" stroke="#202226" stroke-width="3" />
    <path d="M1400 740 V760" stroke="#202226" stroke-width="3" />
    <text x="1110" y="785" font-size="16">0'</text>
    <text x="1242" y="785" font-size="16">20'</text>
    <text x="1382" y="785" font-size="16">40'</text>
  </g>
</svg>
""".strip()


def _holding_structure_svg() -> str:
    return """<svg xmlns="http://www.w3.org/2000/svg" width="1600" height="900" viewBox="0 0 1600 900" role="img" aria-labelledby="title desc">
  <title>Focus Negotium holding structure</title>
  <desc>Parent-company relationship between Focus Negotium Inc and its affiliate operating companies.</desc>
  <rect width="1600" height="900" fill="#08111f" />
  <rect x="110" y="92" width="1380" height="716" rx="34" fill="none" stroke="#7cc8ff" stroke-opacity="0.2" stroke-width="2" />
  <circle cx="800" cy="225" r="150" fill="#3ee4d6" opacity="0.12" />
  <circle cx="800" cy="225" r="108" fill="none" stroke="#f2c96d" stroke-opacity="0.42" stroke-width="2" />
  <path d="M800 348 V495" stroke="#f2c96d" stroke-width="4" stroke-linecap="round" />
  <path d="M520 495 H1080" stroke="#7cc8ff" stroke-width="4" stroke-linecap="round" />
  <path d="M520 495 V590" stroke="#7cc8ff" stroke-width="4" stroke-linecap="round" />
  <path d="M1080 495 V590" stroke="#7cc8ff" stroke-width="4" stroke-linecap="round" />
  <rect x="545" y="145" width="510" height="170" rx="28" fill="#0d1b33" stroke="#3ee4d6" stroke-opacity="0.4" />
  <rect x="210" y="590" width="500" height="165" rx="24" fill="#0d1b33" stroke="#7cc8ff" stroke-opacity="0.35" />
  <rect x="890" y="590" width="500" height="165" rx="24" fill="#0d1b33" stroke="#f2c96d" stroke-opacity="0.35" />
  <text x="800" y="188" text-anchor="middle" fill="#f2c96d" font-family="Manrope, Arial, sans-serif" font-size="26" letter-spacing="8">PARENT COMPANY</text>
  <text x="800" y="244" text-anchor="middle" fill="#f6f8ff" font-family="Cormorant Garamond, Georgia, serif" font-size="74" font-weight="700">Focus Negotium Inc</text>
  <text x="800" y="286" text-anchor="middle" fill="#d4dff2" font-family="Manrope, Arial, sans-serif" font-size="24">Real estate development, property management, business infrastructure, and executive operations</text>
  <text x="460" y="635" text-anchor="middle" fill="#f6f8ff" font-family="Cormorant Garamond, Georgia, serif" font-size="56" font-weight="700">Focus Records LLC</text>
  <text x="460" y="676" text-anchor="middle" fill="#d4dff2" font-family="Manrope, Arial, sans-serif" font-size="22">Affiliate media company</text>
  <text x="460" y="713" text-anchor="middle" fill="#d4dff2" font-family="Manrope, Arial, sans-serif" font-size="20">Release systems, visual campaigns, catalog packaging, licensing, and artist commerce</text>
  <text x="1140" y="635" text-anchor="middle" fill="#f6f8ff" font-family="Cormorant Garamond, Georgia, serif" font-size="50" font-weight="700">Royal Lee Construction Solutions LLC</text>
  <text x="1140" y="676" text-anchor="middle" fill="#d4dff2" font-family="Manrope, Arial, sans-serif" font-size="22">Affiliate construction company</text>
  <text x="1140" y="713" text-anchor="middle" fill="#d4dff2" font-family="Manrope, Arial, sans-serif" font-size="20">Sacred-geometry concept studies, development planning, preconstruction, and owner-facing strategy</text>
  <text x="800" y="844" text-anchor="middle" fill="#b6cae7" font-family="Manrope, Arial, sans-serif" font-size="18">One holding company, two affiliate operating companies, one coordinated public storefront</text>
</svg>
""".strip()


def generated_public_assets() -> dict[str, str]:
    return {
        HOLDING_DIAGRAM_PATH: _holding_structure_svg(),
        FOCUS_RECORDS_POSTERS[0]: _brand_poster_svg(
            "Release Identity Board",
            "Positioning, cover direction, and launch-world visual language for artists and branded drops.",
            "#7cc8ff",
            "#3ee4d6",
            "Focus Records LLC",
        ),
        FOCUS_RECORDS_POSTERS[1]: _brand_poster_svg(
            "Firefly Campaign Board",
            "Campaign art direction for promo stills, launch visuals, and social-first release sequencing.",
            "#f2c96d",
            "#7cc8ff",
            "Adobe-ready visual lane",
        ),
        FOCUS_RECORDS_POSTERS[2]: _brand_poster_svg(
            "Licensing Marketplace Board",
            "Beat-store, licensing, and digital catalog framing for future public product drops.",
            "#ff9b68",
            "#3ee4d6",
            "Commerce expansion",
        ),
        RLC_CONCEPT_STUDIES[0]: _architecture_study_svg(
            "Sanctuary Courtyard Residence",
            "A geometric courtyard home concept balancing circulation, light, and private retreat space.",
            "Concept Study A",
            "#b08a3b",
        ),
        RLC_CONCEPT_STUDIES[1]: _architecture_study_svg(
            "Hexagonal Estate Plan",
            "A sacred-geometry estate concept with radial zoning and owner-facing ceremonial arrival logic.",
            "Concept Study B",
            "#7c6a3a",
        ),
        RLC_CONCEPT_STUDIES[2]: _architecture_study_svg(
            "Development Cluster Study",
            "A multi-structure development concept study for shared amenities, circulation, and site hierarchy.",
            "Concept Study C",
            "#8b6b4c",
        ),
    }


def write_generated_assets() -> None:
    for relative_path, content in generated_public_assets().items():
        target = PUBLIC / relative_path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8")


def render_program_cards(company: dict) -> str:
    programs = company.get("programs", [])
    if not programs:
        return ""
    cards = "\n".join(
        f"""
<article class="feature-panel glow-card">
  <p class="eyebrow">Sector coverage</p>
  <h3>{escape(program['title'])}</h3>
  <p>{escape(program['summary'])}</p>
</article>
""".strip()
        for program in programs
    )
    return f"""
<section class="section-block">
  <p class="eyebrow">Where this company works best</p>
  <h2>High-level lanes that define the public offer.</h2>
  <div class="grid-three">{cards}</div>
</section>
""".strip()


def render_company_notes(company: dict) -> str:
    notes = company.get("notes", [])
    if not notes:
        return ""
    items = "".join(f"<li>{escape(note)}</li>" for note in notes)
    return f"""
<section class="section-block">
  <p class="eyebrow">Professional notes</p>
  <section class="feature-panel glow-card">
    <ul class="detail-list">{items}</ul>
  </section>
</section>
""".strip()


def render_focus_negotium_section() -> str:
    return f"""
<section class="section-block split-band">
  <figure class="drawing-frame">
    <img src="{HOLDING_DIAGRAM_PATH}" alt="Holding-company structure showing Focus Negotium Inc with affiliate companies Focus Records LLC and Royal Lee Construction Solutions LLC" />
    <figcaption>Focus Negotium Inc operates as the parent company, with affiliate media and construction companies supporting the larger portfolio.</figcaption>
  </figure>
  <section class="feature-panel glow-card">
    <p class="eyebrow">Corporate relationship</p>
    <h2>The holding-company lane keeps services organized without confusing the client path.</h2>
    <ul class="detail-list">
      <li>Focus Negotium Inc leads executive business services, development strategy, and portfolio operations.</li>
      <li>Focus Records LLC contracts for media, release, and branded campaign work as an affiliate company.</li>
      <li>Royal Lee Construction Solutions LLC contracts for sacred-geometry planning, concept studies, and construction strategy as an affiliate company.</li>
      <li>The public site keeps one shared storefront and one routing line while preserving distinct company pages.</li>
    </ul>
  </section>
</section>
""".strip()


def render_focus_records_section() -> str:
    figures = "\n".join(
        f"""
<figure class="drawing-frame">
  <img src="{path}" alt="Focus Records campaign concept board" />
  <figcaption>{caption}</figcaption>
</figure>
""".strip()
        for path, caption in [
            (FOCUS_RECORDS_POSTERS[0], "Release identity concept board for public launch positioning and cover-direction alignment."),
            (FOCUS_RECORDS_POSTERS[1], "Firefly-ready campaign board for promo visuals, social motion, and release-world atmosphere."),
            (FOCUS_RECORDS_POSTERS[2], "Licensing and beat-store concept board for future audio-product and catalog-commerce drops."),
        ]
    )
    return f"""
<section class="section-block">
  <p class="eyebrow">Campaign concept boards</p>
  <h2>Visual direction for release work, branded drops, and future music-product sales.</h2>
  <div class="grid-three">{figures}</div>
</section>
<section class="section-block split-band">
  <section class="feature-panel glow-card">
    <p class="eyebrow">Current delivery</p>
    <ul class="detail-list">
      <li>Launch pages, cover-direction systems, branded campaign assets, and release sequencing.</li>
      <li>Artist, founder, and product storytelling tuned for public-facing conversion and recognition.</li>
      <li>Catalog packaging that supports immediate release work and longer-term licensing value.</li>
    </ul>
  </section>
  <section class="feature-panel glow-card">
    <p class="eyebrow">Next commerce lane</p>
    <h2>Beat sales and licensing are being staged for public release.</h2>
    <p>The site is now ready to add Suno-adjacent beat products, producer packs, and licensing offers once the final catalog assets are ready for sale.</p>
  </section>
</section>
""".strip()


def render_rlc_section() -> str:
    gallery = "\n".join(
        f"""
<figure class="drawing-frame">
  <img src="{path}" alt="{alt}" />
  <figcaption>{caption}</figcaption>
</figure>
""".strip()
        for path, alt, caption in [
            ("rlc/first_floor.svg", "First floor office schematic", "Existing office-package schematic preserved inside the construction portfolio."),
            ("rlc/second_floor.svg", "Second floor office schematic", "Second-floor schematic from the existing package, ready for owner review."),
            (RLC_CONCEPT_STUDIES[0], "Sacred geometry residence concept study", "Concept Study A: a courtyard residence drafted by Reginald Hilton."),
            (RLC_CONCEPT_STUDIES[1], "Hexagonal estate concept study", "Concept Study B: an estate plan drafted by Reginald Hilton."),
            (RLC_CONCEPT_STUDIES[2], "Development cluster concept study", "Concept Study C: a development cluster drafted by Reginald Hilton."),
        ]
    )
    return f"""
<section class="section-block">
  <p class="eyebrow">Drafted concept studies</p>
  <h2>Presentation-grade sacred-geometry studies for homes, sites, and development work.</h2>
  <div class="drawing-grid">{gallery}</div>
</section>
<section class="section-block split-band">
  <section class="feature-panel glow-card">
    <p class="eyebrow">Presentation use</p>
    <ul class="detail-list">
      <li>Use concept studies to align ownership, development intent, and design direction before full drafting begins.</li>
      <li>Bring sacred geometry into the planning conversation without sacrificing buildability, scale logic, or budget framing.</li>
      <li>Move from concept studies into scope planning, owner representation, and contractor-facing package refinement.</li>
    </ul>
  </section>
  <section class="feature-panel glow-card">
    <p class="eyebrow">Important note</p>
    <p>These visuals are concept studies prepared for presentation and project development. Licensed professionals should verify field dimensions, structural loads, and permit requirements prior to fabrication or construction.</p>
    <div class="button-row"><a class="btn secondary" href="rlc-office-package.html">Open the RLC package</a></div>
  </section>
</section>
""".strip()


def render_company_extensions(company: dict) -> str:
    if company["id"] == "focus-negotium":
        return render_focus_negotium_section()
    if company["id"] == "focus-records":
        return render_focus_records_section()
    if company["id"] == "royal-lee-construction":
        return render_rlc_section()
    return ""


def render_offer_cards(catalog: dict) -> str:
    cards = []
    for offer in catalog.get("offers", []):
        cta = offer["cta_label"] if offer.get("checkout_url") else "Book to purchase"
        href = offer.get("checkout_url") or "booking.html"
        cards.append(
            f"""
<article class="offer-card glow-card">
  <p class="eyebrow">Offer ladder</p>
  <h3>{escape(offer['title'])}</h3>
  <p>{escape(offer['summary'])}</p>
  <div class="meta-row">
    <span class="price-pill">{_format_currency(float(offer['price_usd']))}</span>
    <span class="micro-note">Secure checkout path</span>
  </div>
  <div class="button-row">
    <a class="btn" href="{escape(href)}">{escape(cta)}</a>
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
  <p class="micro-note">{escape(company.get('relationship_note', ''))}</p>
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
  <p class="micro-note">{escape(company.get('relationship_note', ''))}</p>
  <div class="service-stack">{services}</div>
  <div class="button-row"><a class="btn secondary" href="{escape(company['slug'])}">Open company page</a></div>
</section>
""".strip()
        )
    return "\n".join(rows)


def render_system_cards() -> str:
    items = [
        {
            "eyebrow": "Storefront",
            "title": "Business-first homepage",
            "summary": "A clear public homepage that introduces the three companies, the store, and the service path without exposing internal tools.",
            "href": "index.html",
            "cta": "See the homepage",
        },
        {
            "eyebrow": "Store",
            "title": "Storefront and offers",
            "summary": "A customer-facing store for books, digital bundles, and higher-tier business offers.",
            "href": "store.html",
            "cta": "Open the store",
        },
        {
            "eyebrow": "Structure",
            "title": "Business structure",
            "summary": "Show how the companies, services, and customer journey fit together across one shared public experience.",
            "href": "structure.html",
            "cta": "See the structure",
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


def render_stripe_panel(catalog: dict) -> str:
    stripe = catalog["portal"]["payment_processors"]["stripe"]
    buttons = []
    for offer in catalog.get("offers", [])[:2]:
        if offer.get("checkout_url"):
            buttons.append(
                f'<a class="btn secondary" href="{escape(offer["checkout_url"])}">{escape(offer["title"])}</a>'
            )
    if not buttons:
        buttons.append('<a class="btn secondary" href="booking.html">Book to purchase</a>')
    return f"""
<section class="feature-panel glow-card">
  <p class="eyebrow">Stripe checkout</p>
  <h2>Public payments route through secure Stripe links instead of a separate storefront platform.</h2>
  <p>{escape(stripe['summary'])}</p>
  <p class="micro-note">Status: {escape(stripe['status'])}</p>
  <div class="button-row">{''.join(buttons)}</div>
</section>
""".strip()


def public_store_catalog(catalog: dict) -> dict:
    phone = _phone_digits(catalog["portal"]["primary_contact"]["phone"])
    return {
        "brand": catalog["portal"]["brand"],
        "site_name": catalog["portal"]["site_name"],
        "phone": phone,
        "companies": [
            {
                "name": company["name"],
                "slug": company["slug"],
                "headline": company["headline"],
                "description": company["description"],
                "relationship_note": company.get("relationship_note", ""),
                "programs": company.get("programs", []),
                "services": company["services"],
            }
            for company in COMPANY_PROFILES
        ],
        "books": [
            {
                "title": book["title"],
                "slug": book["slug"],
                "price_usd": book["price_usd"],
                "tag": book["tag"],
                "summary": book["summary"],
                "reading_url": f"ebooks/{book['slug']}.html",
                "pdf_url": f"ebooks/pdfs/{book['slug']}.pdf",
            }
            for book in BOOK_CATALOG
        ],
        "offers": [
            {
                "title": offer["title"],
                "price_usd": offer["price_usd"],
                "summary": offer["summary"],
                "checkout_url": offer["checkout_url"],
                "cta_label": offer["cta_label"],
            }
            for offer in catalog.get("offers", [])
        ],
    }


def build_stripe_csv(catalog: dict) -> str:
    buffer = StringIO()
    writer = csv.writer(buffer)
    writer.writerow(
        [
            "Slug",
            "Title",
            "Type",
            "Price USD",
            "Checkout URL",
            "Summary",
        ]
    )

    for offer in catalog.get("offers", []):
        writer.writerow(
            [
                offer["id"].replace("_", "-"),
                offer["title"],
                "Digital Offer",
                f"{float(offer['price_usd']):.2f}",
                offer.get("checkout_url", ""),
                offer["summary"],
            ]
        )

    return buffer.getvalue()


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
        "while still connecting back into the larger public storefront."
    )
    relationship_note = company.get("relationship_note", "This company sits inside the wider Focus Corporation public experience.")
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
          <span>{escape(company['eyebrow'])}</span>
          <span>Professional pricing and delivery structure</span>
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
        <p class="eyebrow">Shared structure note</p>
        <h2>This company is distinct, but it still sits inside one shared customer experience.</h2>
        <p>{escape(relationship_note)}</p>
      </section>
    </section>
    <section class="section-block">
      <p class="eyebrow">Services and standardized pricing</p>
      <h2>Choose the level of support that matches the decision in front of you.</h2>
      <div class="offer-grid">{services}</div>
    </section>
    {render_program_cards(company)}
    {render_company_extensions(company)}
    {render_company_notes(company)}
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
{head_html('TheFocusCorp.com', 'Businesses, services, books, and storefront structure across The Focus Corporation.')}
<body>
  <main>
    {nav_html()}
    <section class="hero-panel luminous-hero">
      <div class="poster panel-flow">
        <p class="eyebrow">The Focus Corporation</p>
        <h1>One holding company, two affiliate operating companies, and one clear path into books, services, development, and premium support.</h1>
        <p class="lede">TheFocusCorp.com is the public home of Focus Negotium Inc, Focus Records LLC, and Royal Lee Construction Solutions LLC, organized as a mobile-friendly corporate storefront with clearer routing into the right company, the right service, and the right next step.</p>
        <p>The experience stays elevated and easy to use so visitors can understand the structure quickly, review pricing, and move from first visit into a real engagement without confusion.</p>
        <div class="metric-strip">
          <span>Call or text {phone}</span>
          <span>{ebook_count} published books</span>
          <span>Parent company + 2 affiliates</span>
        </div>
        <div class="button-row">
          <a class="btn" href="store.html">Open the store</a>
          <a class="btn secondary" href="services.html">Explore services</a>
          <a class="btn secondary" href="structure.html">View the structure</a>
          <a class="btn secondary" href="tel:{phone}">Call {phone}</a>
        </div>
      </div>
      <section class="hero-visual-panel glow-card">{render_sacred_visual()}</section>
    </section>
    <section class="section-block">
      <p class="eyebrow">Holding company and affiliates</p>
      <h2>One public standard across corporate services, media work, and construction strategy.</h2>
      <p class="section-copy">The homepage carries the parent-company structure and the affiliate roles clearly so visitors can move into the right sector without losing the bigger picture.</p>
      <div class="grid-three">{render_company_cards(catalog)}</div>
    </section>
    <section class="section-block catalog-band">
      <section class="feature-panel glow-card">
        <p class="eyebrow">Storefront</p>
        <h2>The store now combines books, premium offers, and secure Stripe checkout in one place.</h2>
        <p>Use the storefront to present the books clearly, route buyers into the right service tier, and move qualified clients into deeper work without adding a second platform.</p>
        <div class="button-row">
          <a class="btn" href="store.html">Browse the store</a>
          <a class="btn secondary" href="ebooks/index.html">Open the library</a>
        </div>
      </section>
      <section class="feature-panel glow-card">
        <p class="eyebrow">Routing line</p>
        <h2>{escape(contact_name)}</h2>
        <p>For service routing, store questions, development planning, or help choosing the right package, call or text {phone}.</p>
        <div class="detail-list">
          <p><strong>Books</strong> Start with the book shelf and digital library.</p>
          <p><strong>Services</strong> Move into company-specific strategy, media work, development, or build planning.</p>
          <p><strong>Structure</strong> Review how the parent company and affiliates fit together.</p>
        </div>
      </section>
    </section>
    <section class="section-block">
      <p class="eyebrow">Service architecture</p>
      <h2>Reasonable global standardized pricing across every company path.</h2>
      <div class="detail-grid">{render_company_service_rows()}</div>
    </section>
    <section class="section-block">
      <p class="eyebrow">Public site structure</p>
      <h2>The homepage now points directly into the services, the store, and the holding-company structure.</h2>
      <div class="grid-three">{render_system_cards()}</div>
    </section>
  </main>
</body>
</html>
"""

    landing_page = f"""<!doctype html>
<html lang="en">
{head_html('The Focus Corporation Landing', 'Launch-facing page for the businesses, books, store, and services on TheFocusCorp.com.')}
<body>
  <main>
    {nav_html()}
    <section class="hero-panel luminous-hero">
      <div class="poster panel-flow">
        <p class="eyebrow">Launch page</p>
        <h1>Enter the brand without losing the practical next step.</h1>
        <p class="lede">This landing page keeps the sacred-geometry atmosphere while staying grounded in visible pricing, corporate structure, clear routing, and a business-first public experience.</p>
        <div class="metric-strip">
          <span>{phone}</span>
          <span>Books + services + holdings</span>
          <span>Mobile-first storefront</span>
        </div>
        <div class="button-row">
          <a class="btn" href="store.html">Enter the storefront</a>
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
{head_html('Services Across Three Companies', 'Company pages and service pricing across The Focus Corporation.')}
<body>
  <main>
    {nav_html()}
    <section class="hero-panel luminous-hero">
      <div class="poster panel-flow">
        <p class="eyebrow">Service routing</p>
        <h1>Choose the right company path without losing the larger corporate structure behind it.</h1>
        <p class="lede">Every service page keeps the same mobile behavior, visual discipline, and pricing clarity while still distinguishing the parent company from its affiliate operating companies.</p>
        <div class="button-row">
          <a class="btn" href="tel:{phone}">Call {phone}</a>
          <a class="btn secondary" href="booking.html">Book with {escape(contact_name)}</a>
          <a class="btn secondary" href="structure.html">See the structure</a>
        </div>
      </div>
      <section class="feature-panel glow-card">
        <p class="eyebrow">Shared route</p>
        <h2>{escape(contact_name)}</h2>
        <p>Use {phone} for corporate setup, development planning, media rollout, sacred-geometry build strategy, or storefront support.</p>
        <ul class="detail-list">
          <li>Focus Negotium Inc for holdings, business services, real estate, property operations, and websites.</li>
          <li>Focus Records LLC for release work, cover direction, campaign assets, and catalog packaging.</li>
          <li>Royal Lee Construction Solutions LLC for concept studies, development strategy, and preconstruction planning.</li>
        </ul>
      </section>
    </section>
    <section class="section-block">
      <p class="eyebrow">Company service matrix</p>
      <h2>Reasonable global standardized pricing with deeper company pages behind each sector.</h2>
      <div class="detail-grid">{render_company_service_rows()}</div>
    </section>
  </main>
</body>
</html>
"""

    products_page = f"""<!doctype html>
<html lang="en">
{head_html('The Focus Corporation Store', 'Books, digital collections, and premium offers on TheFocusCorp.com.')}
<body>
  <main>
    {nav_html()}
    <section class="hero-panel luminous-hero">
      <div class="poster panel-flow">
        <p class="eyebrow">Storefront</p>
        <h1>Move from books and digital products into premium service, development, and business support.</h1>
        <p class="lede">The store combines individual book pricing with Stripe-connected offers so customers can start small, purchase a structured package, or move directly into a premium buildout.</p>
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
          <li>{_format_currency(float(catalog['offers'][2]['price_usd']))} signature business buildout</li>
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
          <li>Digital resources, service routing, and clear package structure.</li>
          <li>One clear progression from knowledge product to custom implementation.</li>
        </ul>
      </section>
      {render_stripe_panel(catalog)}
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
      <h2>Current titles and prices.</h2>
      <div class="book-grid">{render_book_cards(phone)}</div>
    </section>
  </main>
</body>
</html>
"""

    business_os_page = f"""<!doctype html>
<html lang="en">
{head_html('Business Structure | The Focus Corporation', 'The public structure behind the businesses, services, and store on TheFocusCorp.com.')}
<body>
  <main>
    {nav_html()}
    <section class="hero-panel luminous-hero">
      <div class="poster panel-flow">
        <p class="eyebrow">Business structure</p>
        <h1>The structure behind the holding company, the affiliate companies, the services, and the storefront.</h1>
        <p class="lede">This page explains how Focus Negotium Inc holds the affiliate companies, how the public storefront is organized, and how customers can move from the first visit into the right book, service, development project, or premium package.</p>
        <div class="button-row">
          <a class="btn" href="services.html">Explore services</a>
          <a class="btn secondary" href="store.html">Open the store</a>
          <a class="btn secondary" href="tel:{phone}">Call {phone}</a>
        </div>
      </div>
      <section class="hero-visual-panel glow-card">{render_sacred_visual()}</section>
    </section>
    <section class="section-block">
      <p class="eyebrow">Company roles</p>
      <h2>The parent company leads the portfolio while the affiliates stay specialized.</h2>
      <div class="grid-three">{render_company_cards(catalog)}</div>
    </section>
    {render_focus_negotium_section()}
    <section class="section-block">
      <p class="eyebrow">Customer path</p>
      <h2>A simple public structure from first visit to paid engagement.</h2>
      <div class="stage-grid">
        <article class="stage-card glow-card"><p class="eyebrow">Step 1</p><h3>Discover the parent structure</h3><p>Visitors land on the homepage, understand the holding company, and see the affiliate sectors clearly.</p></article>
        <article class="stage-card glow-card"><p class="eyebrow">Step 2</p><h3>Browse the store</h3><p>The storefront presents books, premium offers, and secure Stripe checkout with visible pricing.</p></article>
        <article class="stage-card glow-card"><p class="eyebrow">Step 3</p><h3>Review sector services</h3><p>Each company page explains the service tiers, pricing, and the best use cases for that specific business lane.</p></article>
        <article class="stage-card glow-card"><p class="eyebrow">Step 4</p><h3>Route through one contact</h3><p>The shared routing line keeps the customer experience simple while the underlying company structure stays organized.</p></article>
      </div>
    </section>
    <section class="section-block">
      <p class="eyebrow">Store collections</p>
      <div class="grid-three">{render_system_cards()}</div>
    </section>
  </main>
</body>
</html>
"""

    booking_page = f"""<!doctype html>
<html lang="en">
{head_html(f'Book with {contact_name}', 'Book with the primary routing contact for services, storefront questions, and business guidance.')}
<body>
  <main>
    {nav_html()}
    <section class="hero-panel luminous-hero">
      <div class="poster panel-flow">
        <p class="eyebrow">Primary routing</p>
        <h1>Book with {escape(contact_name)}</h1>
        <p class="lede">Use one direct routing line for company selection, project framing, service clarity, development questions, and storefront support.</p>
        <div class="metric-strip">
          <span>Call or text {phone}</span>
          <span>Corporate, media, and construction routing</span>
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
          <li>Routing a live project into the right business or storefront path.</li>
        </ul>
      </section>
    </section>
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
{head_html('Email Follow-Up Sequence', 'Follow-up sequence for moving readers into the public store and service offers.')}
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
      <article class="stage-card glow-card"><p class="eyebrow">Email 5</p><h3>Ready for the signature buildout?</h3><p>Present the flagship buildout as the premium next step.</p></article>
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
        "store.html": products_page,
        "books.html": books_page,
        "business_os.html": business_os_page,
        "structure.html": business_os_page,
        "booking.html": booking_page,
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
    copy_tree(RLC_OUTPUT, PUBLIC / "rlc")
    write_generated_assets()

    (PUBLIC / "funnel.css").write_text(build_css(catalog), encoding="utf-8")

    data_dir = PUBLIC / "data"
    data_dir.mkdir(parents=True, exist_ok=True)
    public_catalog = public_store_catalog(catalog)
    (data_dir / "store_catalog.json").write_text(
        json.dumps(public_catalog, indent=2), encoding="utf-8"
    )
    (data_dir / "business_os.json").write_text(
        json.dumps(public_catalog, indent=2), encoding="utf-8"
    )

    stripe_dir = ROOT / "published" / "stripe"
    stripe_dir.mkdir(parents=True, exist_ok=True)
    (stripe_dir / "stripe_offer_catalog.csv").write_text(build_stripe_csv(catalog), encoding="utf-8")
    (stripe_dir / "README.txt").write_text(
        "Stripe-focused offer export generated from the public store catalog. "
        "Use stripe_offer_catalog.csv as the local manifest for secure checkout links and offer inventory.\n",
        encoding="utf-8",
    )

    pages = build_pages(catalog)
    for page_name, page_content in pages.items():
        (PUBLIC / page_name).write_text(page_content, encoding="utf-8")

    (PUBLIC / ".htaccess").write_text(ROOT_HTACCESS, encoding="utf-8")
    print(f"Built public site at {PUBLIC}")
    return 0


if __name__ == "__main__":
    raise SystemExit(build())
