#!/usr/bin/env python3
from __future__ import annotations

import json
import os
import shutil
import stat
from html import escape
from pathlib import Path

from PIL import Image

try:
    import qrcode
except ImportError:  # pragma: no cover
    qrcode = None

ROOT = Path(__file__).resolve().parent
DIST = ROOT / "dist"
SOURCE = ROOT / "source"
SECRETS_DIR = ROOT.parents[1] / ".secrets"
SITE_CSS = ROOT / "site.css"
SITE_JS = ROOT / "site.js"

BASE_URL = "https://www.fluxcrave.com"

LOGO_WORDMARK_BOX = (150, 108, 430, 172)
QR_FALLBACK_BOX = (821, 609, 1008, 797)


def safe_rmtree(path: Path) -> None:
    def on_error(func, value, _exc) -> None:
        os.chmod(value, stat.S_IWRITE)
        func(value)

    if path.exists():
        shutil.rmtree(path, onerror=on_error)


def load_env_file(path: Path) -> None:
    if not path.exists():
        return
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip()
        if key and key not in os.environ:
            os.environ[key] = value


def load_env() -> dict[str, str]:
    load_env_file(SECRETS_DIR / "focus_master.env")
    load_env_file(SECRETS_DIR / "fluxcrave.env")
    data = {
        "domain": os.getenv("FLUXCRAVE_DOMAIN", "fluxcrave.com"),
        "www_domain": os.getenv("FLUXCRAVE_WWW_DOMAIN", "www.fluxcrave.com"),
        "name": os.getenv("FLUXCRAVE_SITE_NAME", "Flux & Crave"),
        "phone": os.getenv("FLUXCRAVE_PHONE", "5737193159"),
        "display_phone": os.getenv("FLUXCRAVE_DISPLAY_PHONE", "(573) 719-3159"),
        "address_line": os.getenv("FLUXCRAVE_ADDRESS_LINE", "3827 Highway MM"),
        "city_state_zip": os.getenv("FLUXCRAVE_CITY_STATE_ZIP", "Hannibal, MO 63401"),
        "order_url": os.getenv("FLUXCRAVE_ORDER_URL", ""),
    }
    data["address_full"] = f"{data['address_line']}, {data['city_state_zip']}"
    return data


ENV = load_env()


MENU_SECTIONS: list[dict[str, object]] = [
    {
        "slug": "sandwiches",
        "title": "Sandwiches & Wraps",
        "note": "Fast-moving handhelds with crisp texture, bright finishes, and big flavor.",
        "items": [
            {
                "name": "The Flux Capacitor",
                "price": "$11.50",
                "description": "Crispy chicken breast fried in coconut oil with Flux Ex sauce and pickles on toasted brioche.",
            },
            {
                "name": "The Velocity Sub",
                "price": "$13.50",
                "description": "Roasted chicken or smoked turkey breast with bean sprouts, pickled onions, and Flux Fire dusting on a toasted hoagie.",
            },
            {
                "name": "The Kinetic Wrap",
                "price": "$12.50",
                "description": "Grilled chicken, baby spinach, cucumber ribbons, and Flux Ex spread in a spinach tortilla.",
            },
            {
                "name": "The Hummus Pulse Wrap",
                "price": "$11.00",
                "description": "House hummus, bean sprouts, shredded purple cabbage, and bell peppers finished with Citrus Spark.",
            },
            {
                "name": "Classic Chicken Sub",
                "price": "$8.99",
                "description": "A straightforward toasted artisan roll option built for speed.",
            },
            {
                "name": "Gutbuster Sub",
                "price": "$10.49",
                "description": "A heartier toasted artisan roll built for a bigger appetite.",
            },
        ],
    },
    {
        "slug": "boxes",
        "title": "Boxes & Combos",
        "note": "Carryout-ready builds designed to move hot, fast, and satisfy on the first bite.",
        "items": [
            {
                "name": "The Heavyweight Flux Box",
                "price": "$17.50",
                "description": "Choose fried chicken, smoked turkey, or crispy tofu over a bed of fresh-cut Tornado Fries with Flux Ex and Citrus Spark.",
            },
            {
                "name": "The Stuffed Tornado Box",
                "price": "$15.00",
                "description": "Spiral-cut Tornado Fries stuffed with shredded protein and bean sprouts, dusted in Flux Fire.",
            },
            {
                "name": "The Unstuffed Tornado Box",
                "price": "$13.00",
                "description": "A mountain of coconut-oil-fried Tornado Fries topped with Flux Fire and a Flux Ex drizzle.",
            },
            {
                "name": "Crave Combo",
                "price": "$13.99",
                "description": "Choose tenders or whole chicken wings with signature slaw and a Lemon Shaker.",
            },
            {
                "name": "Workday Lunch Box",
                "price": "$9.99",
                "description": "Weekday lunch special with small slaw and a 12oz Lemon Shaker.",
            },
            {
                "name": "Family Crunch Pack",
                "price": "$14.99",
                "description": "Twelve tenders or twelve whole chicken wings with large slaw and a 64oz Lemon Shaker.",
            },
        ],
    },
    {
        "slug": "salads",
        "title": "Salads & Bowls",
        "note": "Fresh builds that keep the wellness-forward side of the brand visible without sacrificing flavor.",
        "items": [
            {
                "name": "Holistic Health Salad",
                "price": "$10.00 / $16.50",
                "description": "A nutrient-dense base of kale and bean sprouts topped with shredded carrots and radishes.",
            },
            {
                "name": "The Alkaline Flux Bowl",
                "price": "$11.50 / $18.50",
                "description": "Quinoa, baby spinach, cherry tomatoes, and cucumber ribbons with Citrus Spark vinaigrette.",
            },
            {
                "name": "The Crave Cleanse",
                "price": "$10.50 / $17.00",
                "description": "Purple cabbage, bell peppers, roasted chickpeas, Flux Fire, and a side of hummus.",
            },
            {
                "name": "The Tofu Torque",
                "price": "$12.00 / $19.00",
                "description": "Cubed crispy tofu, bean sprouts, kale, and bell peppers with a Flux Ex drizzle.",
            },
            {
                "name": "The Gobbler Glow",
                "price": "$12.50 / $19.50",
                "description": "Smoked turkey, baby spinach, radishes, and cucumbers with a Citrus Spark spritz.",
            },
            {
                "name": "The Sea Moss Super-Bowl",
                "price": "$14.00 / $22.00",
                "description": "A powerhouse mix of prep-table vegetables, quinoa, and a two-ounce dollop of raw sea moss gel.",
            },
            {
                "name": "House Salad",
                "price": "$6.99",
                "description": "Garden salad with cheese and croutons.",
            },
            {
                "name": "Full Meal Salad",
                "price": "$11.49",
                "description": "Choose grilled or crispy chicken on a full salad build.",
            },
            {
                "name": "Exclusive Chopped Salad & Sub Combo",
                "price": "$12.99",
                "description": "Half salad and half sub for a quick split-plate lunch.",
            },
        ],
    },
    {
        "slug": "wings",
        "title": "Whole Chicken Wings",
        "note": "Whole chicken wings built to order and packed for pickup or local delivery.",
        "items": [
            {
                "name": "Crispy Tenders - 3 Piece",
                "price": "$9.99",
                "description": "All-white meat, hand-breaded.",
            },
            {
                "name": "Crispy Tenders - 6 Piece",
                "price": "$19.99",
                "description": "All-white meat, hand-breaded.",
            },
            {
                "name": "Whole Fried Wings - 3 Piece",
                "price": "$6.99",
                "description": "Original, Lemon Pepper, or Teriyaki.",
            },
            {
                "name": "Whole Fried Wings - 6 Piece",
                "price": "$12.99",
                "description": "Original, Lemon Pepper, or Teriyaki.",
            },
            {
                "name": "Whole Fried Wings - Party Platter",
                "price": "$44.99",
                "description": "Twenty-four pieces for group orders and game-day runs.",
            },
        ],
    },
    {
        "slug": "sips",
        "title": "Sips",
        "note": "Cold signature pours that finish the order cleanly and keep the brand memorable.",
        "items": [
            {
                "name": "Lemon Shaker 32oz",
                "price": "$3.79",
                "description": "Bright, cold, citrus-forward refreshment built for carryout.",
            },
        ],
    },
    {
        "slug": "apothecary",
        "title": "Apothecary Boosters",
        "note": "Herbalist-informed add-ons and wellness-forward extensions that make the brand distinctive.",
        "items": [
            {
                "name": "Flux Sea Moss Gel",
                "price": "$15.00 (5oz) / $32.00 (12oz)",
                "description": "Wild-crafted, multi-mineral sea moss gel in Gold or Purple.",
            },
            {
                "name": "Medicinal Herbal Tinctures",
                "price": "$18.00 (2oz) / $38.00 (5oz)",
                "description": "High-potency extracts designed for immunity, energy, or focus.",
            },
            {
                "name": "Drink Drop-In",
                "price": "$3.00",
                "description": "Add an herbal drop-in to any drink.",
            },
        ],
    },
]


FEATURED_ITEMS = [
    "The Flux Capacitor",
    "The Velocity Sub",
    "The Heavyweight Flux Box",
    "The Alkaline Flux Bowl",
    "Crave Combo",
    "Flux Sea Moss Gel",
]


def flatten_items() -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for section in MENU_SECTIONS:
        for item in section["items"]:  # type: ignore[index]
            rows.append(
                {
                    "category": str(section["title"]),
                    "slug": str(section["slug"]),
                    "name": str(item["name"]),
                    "price": str(item["price"]),
                    "description": str(item["description"]),
                }
            )
    return rows


ALL_ITEMS = flatten_items()
FEATURED_LOOKUP = {item["name"]: item for item in ALL_ITEMS if item["name"] in FEATURED_ITEMS}


def make_dirs() -> None:
    safe_rmtree(DIST)
    (DIST / "assets" / "images").mkdir(parents=True, exist_ok=True)
    (DIST / "assets" / "data").mkdir(parents=True, exist_ok=True)
    (DIST / "menu").mkdir(parents=True, exist_ok=True)
    (DIST / "story").mkdir(parents=True, exist_ok=True)
    (DIST / "visit").mkdir(parents=True, exist_ok=True)
    (DIST / "online-ordering").mkdir(parents=True, exist_ok=True)


def save_logo_assets(flyer: Image.Image) -> None:
    wordmark = flyer.crop(LOGO_WORDMARK_BOX).resize((820, 190), Image.Resampling.LANCZOS)
    wordmark.save(DIST / "assets" / "images" / "flux-logo-wordmark.png")


def save_qr_asset(flyer: Image.Image) -> None:
    order_url = ENV["order_url"].strip()
    qr_path = DIST / "assets" / "images" / "qr-order.png"
    if order_url and qrcode is not None:
        qr = qrcode.QRCode(
            version=None,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=18,
            border=5,
        )
        qr.add_data(order_url)
        qr.make(fit=True)
        qr_image = qr.make_image(fill_color="black", back_color="white").convert("RGB")
        qr_image.save(qr_path)
        return

    qr_crop = flyer.crop(QR_FALLBACK_BOX).resize((960, 960), Image.Resampling.NEAREST)
    qr_crop.save(qr_path)


def write_assets() -> None:
    shutil.copy2(SITE_CSS, DIST / "assets" / "site.css")
    shutil.copy2(SITE_JS, DIST / "assets" / "site.js")
    shutil.copy2(SOURCE / "flux_3.png", DIST / "assets" / "images" / "flux-flyer.png")
    shutil.copy2(
        SOURCE / "Flux_n_crave_description_and_menu.pdf",
        DIST / "assets" / "Flux_n_crave_description_and_menu.pdf",
    )

    flyer = Image.open(SOURCE / "flux_3.png")
    crops = {
        "poster-left.png": (34, 55, 509, 844),
        "poster-right.png": (604, 55, 1089, 844),
        "hero-chicken.png": (26, 329, 527, 803),
        "hero-wrap.png": (585, 160, 1080, 620),
    }
    for filename, box in crops.items():
        flyer.crop(box).save(DIST / "assets" / "images" / filename)
    save_logo_assets(flyer)
    save_qr_asset(flyer)

    logo_svg = """
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 128 128" role="img" aria-label="Flux and Crave mark">
  <defs>
    <linearGradient id="ring" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#ffbf3f"/>
      <stop offset="100%" stop-color="#ff5339"/>
    </linearGradient>
  </defs>
  <rect width="128" height="128" rx="28" fill="#1a120d"/>
  <path d="M38 94c4-24 17-39 38-45-8 11-11 22-9 34 2 13 9 21 21 27-24 0-42-6-50-16z" fill="#ffd05f"/>
  <path d="M79 23c13 7 21 17 25 28 4 12 2 25-6 39-3-12-9-21-18-28-10-7-23-10-38-8 10-18 22-28 37-31z" fill="#ff5a3d"/>
  <path d="M27 75c7-12 17-18 30-20 11-1 22 2 34 10-10 2-18 7-24 15-7 9-10 20-8 34-21-10-32-23-32-39z" fill="url(#ring)"/>
</svg>
""".strip()
    (DIST / "assets" / "images" / "flux-mark.svg").write_text(logo_svg, encoding="utf-8")

    menu_payload = {
        "site": ENV["name"],
        "categories": [
            {
                "slug": section["slug"],
                "title": section["title"],
                "note": section["note"],
                "items": [
                    {
                        "name": item["name"],
                        "description": item["description"],
                    }
                    for item in section["items"]  # type: ignore[index]
                ],
            }
            for section in MENU_SECTIONS
        ],
        "address": ENV["address_full"],
        "phone": ENV["display_phone"],
    }
    (DIST / "assets" / "data" / "menu.json").write_text(
        json.dumps(menu_payload, indent=2),
        encoding="utf-8",
    )


def page_meta(title: str, description: str, route: str, image: str) -> str:
    canonical = f"{BASE_URL}{route}"
    image_url = f"{BASE_URL}{image}"
    return f"""<meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>{escape(title)}</title>
  <meta name="description" content="{escape(description)}" />
  <meta name="theme-color" content="#9d1208" />
  <meta name="robots" content="index,follow" />
  <meta name="keywords" content="Flux and Crave, Flux Crave Hannibal, Hannibal whole chicken wings, Hannibal carryout, Hannibal wraps, Hannibal salads, Hannibal online ordering, Quincy carryout, tri-state chicken, herbalist formulated flavor, coconut oil fried chicken" />
  <link rel="canonical" href="{escape(canonical)}" />
  <link rel="icon" href="/assets/images/flux-mark.svg" type="image/svg+xml" />
  <link rel="manifest" href="/manifest.webmanifest" />
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Manrope:wght@400;500;600;700;800&display=swap" rel="stylesheet" />
  <meta property="og:title" content="{escape(title)}" />
  <meta property="og:description" content="{escape(description)}" />
  <meta property="og:type" content="website" />
  <meta property="og:url" content="{escape(canonical)}" />
  <meta property="og:image" content="{escape(image_url)}" />
  <meta property="og:site_name" content="{escape(ENV['name'])}" />
  <meta property="og:locale" content="en_US" />
  <meta name="twitter:card" content="summary_large_image" />
  <meta name="twitter:title" content="{escape(title)}" />
  <meta name="twitter:description" content="{escape(description)}" />
  <meta name="twitter:image" content="{escape(image_url)}" />
  <link rel="stylesheet" href="/assets/site.css" />"""


def nav_html(current: str) -> str:
    links = [
        ("/", "Home", "home"),
        ("/menu/", "Menu", "menu"),
        ("/story/", "Story", "story"),
        ("/visit/", "Visit", "visit"),
    ]
    nav_items = []
    for href, label, slug in links:
        class_name = "nav-link is-current" if slug == current else "nav-link"
        nav_items.append(f'<a class="{class_name}" href="{href}">{label}</a>')
    return f"""
<header class="site-header">
  <div class="container header-shell">
    <a class="brand" href="/">
      <img class="brand-wordmark" src="/assets/images/flux-logo-wordmark.png" alt="{escape(ENV['name'])} logo" />
      <span>
        <strong>{escape(ENV['name'])}</strong>
        <small>Flavor in Motion</small>
      </span>
    </a>
    <button class="menu-toggle" type="button" aria-expanded="false" aria-controls="site-nav">
      <span></span><span></span><span></span>
    </button>
    <nav class="site-nav" id="site-nav">
      <div class="nav-links">{''.join(nav_items)}</div>
      <a class="button button-primary nav-order" href="/online-ordering/">Order Here</a>
    </nav>
  </div>
</header>
"""


def footer_html() -> str:
    return f"""
<footer class="site-footer">
  <div class="container footer-grid">
    <div>
      <p class="footer-kicker">Flux &amp; Crave</p>
      <h2>Eat different. Crave smart.</h2>
      <p>Bold carryout, clean ingredients, and herbalist-informed menu ideas built for Hannibal, Quincy, and the surrounding small-town corridor.</p>
    </div>
    <div>
      <h3>Visit</h3>
      <p>{escape(ENV['address_line'])}<br />{escape(ENV['city_state_zip'])}</p>
      <p><a href="tel:{escape(ENV['phone'])}">{escape(ENV['display_phone'])}</a></p>
    </div>
    <div>
      <h3>Quick links</h3>
      <ul class="footer-links">
        <li><a href="/menu/">Full menu</a></li>
        <li><a href="/story/">About the concept</a></li>
        <li><a href="/visit/">Pickup, delivery, and contact</a></li>
        <li><a href="/online-ordering/">Order online</a></li>
      </ul>
    </div>
  </div>
</footer>
<a class="floating-order" href="/online-ordering/">Order Here</a>
"""


def layout(title: str, description: str, current: str, route: str, image: str, body: str) -> str:
    schema = {
        "@context": "https://schema.org",
        "@type": "Restaurant",
        "name": ENV["name"],
        "url": f"{BASE_URL}{route}",
        "telephone": ENV["display_phone"],
        "servesCuisine": ["Chicken", "Wraps", "Salads", "Wellness-forward carryout"],
        "description": description,
        "address": {
            "@type": "PostalAddress",
            "streetAddress": ENV["address_line"],
            "addressLocality": "Hannibal",
            "addressRegion": "MO",
            "postalCode": "63401",
            "addressCountry": "US",
        },
        "areaServed": [
            {"@type": "City", "name": "Hannibal"},
            {"@type": "City", "name": "Quincy"},
            {"@type": "AdministrativeArea", "name": "Tri-state area"},
        ],
        "sameAs": [BASE_URL],
        "menu": f"{BASE_URL}/menu/",
    }
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  {page_meta(title, description, route, image)}
  <script type="application/ld+json">{json.dumps(schema)}</script>
</head>
<body>
  <div class="site-background">
    <div class="glow glow-one"></div>
    <div class="glow glow-two"></div>
    <div class="ribbon ribbon-one"></div>
    <div class="ribbon ribbon-two"></div>
    <img class="logo-orbit orbit-one" src="/assets/images/flux-mark.svg" alt="" />
    <img class="logo-orbit orbit-two" src="/assets/images/flux-mark.svg" alt="" />
    <img class="logo-orbit orbit-three" src="/assets/images/flux-mark.svg" alt="" />
  </div>
  {nav_html(current)}
  <main>{body}</main>
  {footer_html()}
  <script src="/assets/site.js"></script>
</body>
</html>
"""


def render_feature_cards() -> str:
    cards = []
    for name in FEATURED_ITEMS:
        item = FEATURED_LOOKUP[name]
        cards.append(
            f"""
<article class="menu-card reveal" data-category="{escape(item['category'])}">
  <div class="menu-card-top">
    <span class="menu-category">{escape(item['category'])}</span>
  </div>
  <h3>{escape(item['name'])}</h3>
  <p>{escape(item['description'])}</p>
</article>
"""
        )
    return "\n".join(cards)


def render_home() -> str:
    body = f"""
<section class="hero-section">
  <div class="container hero-grid">
    <div class="hero-copy">
      <span class="eyebrow">Herbalist-formulated flavor</span>
      <h1>Bold carryout that moves fast, eats clean, and keeps Hannibal craving smart.</h1>
      <p class="hero-summary">Flux &amp; Crave brings whole chicken wings, wraps, salads, bowls, and wellness-forward boosters together in one carryout-ready concept built for pickup, delivery, and repeat orders.</p>
      <div class="hero-actions">
        <a class="button button-primary" href="/online-ordering/">Order Here</a>
        <a class="button button-secondary" href="/menu/">See the menu</a>
      </div>
      <ul class="hero-points">
        <li>Fried in coconut oil</li>
        <li>No cow products</li>
        <li>Chicken, turkey, and tofu options</li>
        <li>Pickup and local delivery</li>
      </ul>
    </div>
    <div class="hero-visual reveal">
      <img class="hero-logo-ambient" src="/assets/images/flux-mark.svg" alt="" />
      <div class="hero-stack">
        <img class="hero-poster hero-poster-back" src="/assets/images/poster-left.png" alt="Flux and Crave flavor in motion poster" />
        <img class="hero-poster hero-poster-front" src="/assets/images/poster-right.png" alt="Flux and Crave highlight poster" />
      </div>
      <div class="hero-badge badge-top">Flavor in Motion</div>
      <div class="hero-badge badge-bottom">Clean ingredients. Stronger crave.</div>
    </div>
  </div>
</section>

<section class="impact-band">
  <div class="container impact-grid">
    <article class="impact-card reveal">
      <h2>Fast carryout with a sharper food story</h2>
      <p>Built for speed, reliability, and hot packaging without dropping the quality cues people remember.</p>
    </article>
    <article class="impact-card reveal">
      <h2>Wellness-forward without losing the bite</h2>
      <p>Cleaner ingredient decisions, bright sauces, and a founder-formulated edge give the menu a lane of its own.</p>
    </article>
    <article class="impact-card reveal">
      <h2>Tri-state appeal from Hannibal outward</h2>
      <p>Positioned for Hannibal, Quincy, and the surrounding towns with a catchy identity people can repeat and recommend.</p>
    </article>
  </div>
</section>

<section class="showcase-section">
  <div class="container split-grid">
    <div class="split-copy reveal">
      <span class="eyebrow">Why it hits different</span>
      <h2>Flavor that lands hard, ingredients that feel intentional.</h2>
      <p>Flux &amp; Crave is built around the kind of fast food customers talk about after the meal: crispy texture, bright finishes, memorable names, and a menu that feels smarter than the average carryout spot.</p>
      <div class="value-grid">
        <div class="value-chip">Faster than typical carryout</div>
        <div class="value-chip">Cleaner ingredients</div>
        <div class="value-chip">Stronger flavor payoff</div>
        <div class="value-chip">Wellness-informed menu mix</div>
      </div>
    </div>
    <div class="food-visual reveal">
      <img src="/assets/images/hero-wrap.png" alt="Grilled wrap and salad from Flux and Crave" />
      <div class="food-caption">
        <strong>Catchy enough to stop the scroll.</strong>
        <span>Clean enough to support the brand promise.</span>
      </div>
    </div>
  </div>
</section>

<section class="menu-section">
  <div class="container">
    <div class="section-heading">
      <span class="eyebrow">Featured menu</span>
      <h2>Signature plates, wraps, bowls, and boosters.</h2>
      <p>Lead with the items that give Flux &amp; Crave its own voice and keep the broader menu one tap away.</p>
    </div>
    <div class="menu-grid">
      {render_feature_cards()}
    </div>
  </div>
</section>

<section class="lane-section">
  <div class="container lane-grid">
    <article class="lane-card reveal">
      <h3>Chicken lane</h3>
      <p>Whole chicken wings, combo boxes, and sandwich builds that move fast and photograph well.</p>
    </article>
    <article class="lane-card reveal">
      <h3>Fresh lane</h3>
      <p>Bowls, wraps, salads, tofu options, and bright herbal finishes that keep the menu from feeling ordinary.</p>
    </article>
    <article class="lane-card reveal">
      <h3>Boost lane</h3>
      <p>Sea moss, tinctures, and functional add-ons that give the business a memorable differentiator in the region.</p>
    </article>
  </div>
</section>

<section class="story-section">
  <div class="container split-grid reverse">
    <div class="food-visual reveal">
      <img src="/assets/images/hero-chicken.png" alt="Crispy chicken and salad from Flux and Crave" />
    </div>
    <div class="split-copy reveal">
      <span class="eyebrow">The concept</span>
      <h2>Eat different. Crave smart.</h2>
      <p>Flux means movement, and the brand leans into that energy. This is a carryout-and-delivery concept designed to feel bold, modern, and memorable while still communicating cleaner ingredients and an herbalist-informed perspective.</p>
      <p>The result is a menu built to sell in multiple lanes: craveable comfort food, fast lunch, salad-first orders, and wellness-oriented add-ons that help the brand stand apart in the tri-state market.</p>
      <a class="text-link" href="/story/">Read the full story</a>
    </div>
  </div>
</section>

<section class="visit-section">
  <div class="container visit-grid">
    <div class="visit-card reveal">
      <span class="eyebrow">Visit Flux &amp; Crave</span>
      <h2>3827 Highway MM, Hannibal, Missouri</h2>
      <p>Built for local pickup, fast handoff, and a delivery footprint around the store. Use the QR, call direct, or jump straight into ordering.</p>
      <div class="visit-actions">
        <a class="button button-primary" href="/online-ordering/">Order Here</a>
        <a class="button button-secondary" href="/visit/">Directions &amp; details</a>
      </div>
      <div class="contact-strip">
        <a href="tel:{escape(ENV['phone'])}">{escape(ENV['display_phone'])}</a>
        <span>3-mile delivery radius</span>
        <span>Fast local handoff</span>
      </div>
    </div>
    <div class="qr-card reveal">
      <img src="/assets/images/qr-order.png" alt="Flux and Crave QR code" />
      <p>Scan to order from a phone, flyer, counter card, or event handout with a cleaner, easier-to-read code.</p>
    </div>
  </div>
</section>
"""
    return layout(
        title="Flux & Crave | Flavor in Motion in Hannibal, Missouri",
        description="Flux & Crave serves whole chicken wings, wraps, salads, bowls, and wellness-forward add-ons in Hannibal, Missouri.",
        current="home",
        route="/",
        image="/assets/images/flux-flyer.png",
        body=body,
    )


def render_menu_cards() -> str:
    rows = []
    for section in MENU_SECTIONS:
        for item in section["items"]:  # type: ignore[index]
            rows.append(
                f"""
<article class="menu-card reveal" data-filter="{escape(str(section['slug']))}">
  <div class="menu-card-top">
    <span class="menu-category">{escape(str(section['title']))}</span>
  </div>
  <h3>{escape(str(item['name']))}</h3>
  <p>{escape(str(item['description']))}</p>
</article>
"""
            )
    return "\n".join(rows)


def render_menu() -> str:
    filters = ['<button class="filter-pill is-active" type="button" data-filter="all">All</button>']
    sections_markup = []
    for section in MENU_SECTIONS:
        filters.append(
            f'<button class="filter-pill" type="button" data-filter="{escape(str(section["slug"]))}">{escape(str(section["title"]))}</button>'
        )
        sections_markup.append(
            f"""
<article class="category-callout reveal">
  <h3>{escape(str(section['title']))}</h3>
  <p>{escape(str(section['note']))}</p>
</article>
"""
        )

    body = f"""
<section class="subpage-hero">
  <div class="container subpage-hero-shell">
    <span class="eyebrow">Full menu</span>
    <h1>Everything worth craving, in one place.</h1>
    <p>From whole chicken wings and wraps to bowls, salads, and herbalist-informed boosters, the menu is built to win lunch, dinner, carryout, and local delivery traffic across Hannibal, Quincy, and the nearby small towns. Crowd anchors like The Flux Capacitor and the Lemon Shaker keep the lineup easy to remember on mobile and in person.</p>
    <div class="hero-actions">
      <a class="button button-primary" href="/online-ordering/">Order Here</a>
      <a class="button button-secondary" href="/visit/">Visit the shop</a>
    </div>
  </div>
</section>

<section class="category-section">
  <div class="container category-grid">
    {''.join(sections_markup)}
  </div>
</section>

<section class="filter-section">
  <div class="container">
    <div class="filter-pills">{''.join(filters)}</div>
    <div class="menu-grid" data-menu-grid>
      {render_menu_cards()}
    </div>
  </div>
</section>

<section class="detail-section">
  <div class="container detail-grid">
    <article class="detail-card reveal">
      <h2>Pickup &amp; delivery</h2>
      <p>Local delivery is built around the shop for fast handoff, simple ordering, and strong carryout quality.</p>
    </article>
    <article class="detail-card reveal">
      <h2>Good-to-know notes</h2>
      <p>Hot items are packed in heat-retaining packaging, cold items stay separate, and the menu keeps chicken, turkey, tofu, salads, and boosters in one brand story.</p>
    </article>
  </div>
</section>
"""
    return layout(
        title="Flux & Crave Menu | Whole Chicken Wings, Wraps, Bowls, and Boosters",
        description="Browse the Flux & Crave menu for whole chicken wings, wraps, bowls, salads, and wellness-forward boosters in Hannibal, Missouri.",
        current="menu",
        route="/menu/",
        image="/assets/images/poster-right.png",
        body=body,
    )


def render_story() -> str:
    body = """
<section class="subpage-hero">
  <div class="container subpage-hero-shell">
    <span class="eyebrow">The brand story</span>
    <h1>A faster carryout concept with a smarter angle.</h1>
    <p>Flux &amp; Crave was framed to feel energetic, modern, and community-ready while still carrying a wellness-forward point of view customers can remember.</p>
  </div>
</section>

<section class="story-columns">
  <div class="container story-grid">
    <article class="story-card reveal">
      <h2>Flavor first</h2>
      <p>The brand promise is simple: strong texture, sharp sauces, bright finishes, and food that looks as good on a flyer as it does when it lands at the table.</p>
    </article>
    <article class="story-card reveal">
      <h2>Herbalist-informed</h2>
      <p>The menu language leaves room for cleaner ingredients, coconut-oil frying, no cow products, and functional add-ons without turning the customer-facing experience into a lecture.</p>
    </article>
    <article class="story-card reveal">
      <h2>Built for the tri-state corridor</h2>
      <p>The concept is local to Hannibal, but the pitch travels well through Quincy and the surrounding small towns because the brand is clear, catchy, and easy to recommend.</p>
    </article>
  </div>
</section>

<section class="principles-section">
  <div class="container split-grid">
    <div class="split-copy reveal">
      <span class="eyebrow">Operating principles</span>
      <h2>Speed, heat retention, and repeat-order energy.</h2>
      <p>Flux &amp; Crave works best when the front-end brand and back-end operations line up. Fast pickup, reliable carryout packaging, a clean order path, and memorable menu names all reinforce the same business goal: get the order, deliver the hit, earn the repeat.</p>
      <ul class="bullet-list">
        <li>Menu names that are catchy without confusing the customer</li>
        <li>Visual identity that stops the scroll on mobile</li>
        <li>Ingredient cues that make the concept feel more intentional</li>
        <li>Order flow that moves fast from flyer to site to checkout</li>
      </ul>
    </div>
    <div class="poster-callout reveal">
      <img src="/assets/images/flux-flyer.png" alt="Flux and Crave flyer" />
    </div>
  </div>
</section>
"""
    return layout(
        title="Flux & Crave Story | A wellness-forward carryout concept",
        description="Learn how Flux & Crave combines bold chicken-shop energy with cleaner ingredient cues and a strong local brand story.",
        current="story",
        route="/story/",
        image="/assets/images/flux-flyer.png",
        body=body,
    )


def render_visit() -> str:
    body = f"""
<section class="subpage-hero">
  <div class="container subpage-hero-shell">
    <span class="eyebrow">Visit, call, or scan</span>
    <h1>Pickup-ready in Hannibal, with local delivery around the shop.</h1>
    <p>Use the online ordering flow for the fastest handoff, or call direct for location questions and current service details.</p>
  </div>
</section>

<section class="visit-layout">
  <div class="container visit-layout-grid">
    <article class="visit-panel reveal">
      <h2>Flux &amp; Crave</h2>
      <p>{escape(ENV['address_line'])}<br />{escape(ENV['city_state_zip'])}</p>
      <p><a href="tel:{escape(ENV['phone'])}">{escape(ENV['display_phone'])}</a></p>
      <div class="visit-actions">
        <a class="button button-primary" href="/online-ordering/">Order Here</a>
        <a class="button button-secondary" href="/menu/">Review the menu</a>
      </div>
      <ul class="bullet-list">
        <li>Fast pickup flow from the shop</li>
        <li>Simple online ordering path</li>
        <li>Built for carryout and local delivery</li>
        <li>Chicken, turkey, tofu, wraps, salads, and boosters</li>
      </ul>
    </article>
    <article class="visit-panel reveal">
      <h2>Scan in person</h2>
      <img class="qr-large" src="/assets/images/qr-order.png" alt="Flux and Crave QR code" />
      <p>Keep this on the site so the same scan-ready experience works across flyers, mobile traffic, and event handouts.</p>
    </article>
  </div>
</section>

<section class="seo-section">
  <div class="container seo-shell">
    <div class="seo-copy reveal">
      <span class="eyebrow">Local search positioning</span>
      <h2>Made to rank for Hannibal carryout, whole chicken wings, wraps, salads, and delivery.</h2>
      <p>Flux &amp; Crave is positioned as a bold carryout and delivery concept serving Hannibal, Quincy, and nearby small towns with whole chicken wings, wraps, salads, bowls, and wellness-forward menu extras. The site copy intentionally supports search intent around chicken carryout, smart-craving menu options, local wings, and online ordering in the tri-state area.</p>
    </div>
  </div>
</section>
"""
    return layout(
        title="Visit Flux & Crave | Hannibal pickup and local delivery",
        description="Visit Flux & Crave in Hannibal, Missouri for pickup-ready flavor, local delivery details, and direct ordering access.",
        current="visit",
        route="/visit/",
        image="/assets/images/qr-order.png",
        body=body,
    )


def write_page(path: Path, content: str) -> None:
    path.write_text(content, encoding="utf-8")


def write_php_redirect() -> None:
    target = ENV["order_url"].strip()
    php = """<?php
$target = %s;
if ($target) {
    header("Location: " . $target, true, 302);
    exit;
}
?><!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Order Online | Flux &amp; Crave</title>
  <meta http-equiv="refresh" content="0; url=/" />
</head>
<body>
  <p>Returning to Flux &amp; Crave.</p>
</body>
</html>
""" % json.dumps(target)
    write_page(DIST / "online-ordering" / "index.php", php)


def write_support_files() -> None:
    htaccess = "DirectoryIndex index.html index.php\nOptions -Indexes\n"
    write_page(DIST / ".htaccess", htaccess)

    robots = f"""User-agent: *
Allow: /

Sitemap: {BASE_URL}/sitemap.xml
"""
    write_page(DIST / "robots.txt", robots)

    sitemap = f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url><loc>{BASE_URL}/</loc></url>
  <url><loc>{BASE_URL}/menu/</loc></url>
  <url><loc>{BASE_URL}/story/</loc></url>
  <url><loc>{BASE_URL}/visit/</loc></url>
</urlset>
"""
    write_page(DIST / "sitemap.xml", sitemap)

    manifest = {
        "name": ENV["name"],
        "short_name": "FluxCrave",
        "start_url": "/",
        "display": "standalone",
        "background_color": "#1a120d",
        "theme_color": "#9d1208",
        "icons": [
            {
                "src": "/assets/images/flux-mark.svg",
                "sizes": "any",
                "type": "image/svg+xml",
            }
        ],
    }
    write_page(DIST / "manifest.webmanifest", json.dumps(manifest, indent=2))


def main() -> int:
    make_dirs()
    write_assets()
    write_page(DIST / "index.html", render_home())
    write_page(DIST / "menu" / "index.html", render_menu())
    write_page(DIST / "story" / "index.html", render_story())
    write_page(DIST / "visit" / "index.html", render_visit())
    write_php_redirect()
    write_support_files()
    print(f"Flux & Crave site built at {DIST}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
