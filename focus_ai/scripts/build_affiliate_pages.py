#!/usr/bin/env python3
"""Build affiliate company landing pages for the public Focus site.

This runs after build_public_site.py and writes route folders under
focus_ai/published/public_site so the deployed site serves clean paths like
/rlcsolutions/ and /waldenauto/.
"""

from __future__ import annotations

import json
from html import escape
from pathlib import Path
from textwrap import dedent

ROOT = Path(__file__).resolve().parents[1]
PUBLIC = ROOT / "published" / "public_site"
DOMAIN = "https://thefocuscorp.com"
ROUTING_PHONE = "217-257-6222"
WALDEN_PHONE = "844-392-5336"
WALDEN_EMAIL = "waldenauto1@gmail.com"

COMPANIES = [
    {
        "slug": "rlcsolutions",
        "canonical_path": "/rlcsolutions/",
        "name": "Royal Lee Construction Solutions LLC",
        "short_name": "RLC Solutions",
        "category": "Construction, development planning, owner representation, and sacred-geometry concept strategy",
        "headline": "Construction planning and owner-side execution systems for serious buildouts.",
        "description": "Royal Lee Construction Solutions LLC supports residential, commercial, and development planning work through organized preconstruction, scope review, sacred-geometry concept studies, owner representation, and project execution support.",
        "contact_name": "Reginald Hilton Jr.",
        "phone": ROUTING_PHONE,
        "email": "mrreginaldhilton@gmail.com",
        "address": "3930 New London Gravel Rd, Hannibal, MO 63401",
        "services": [
            "Preconstruction planning and scope organization",
            "Owner representation and contractor coordination",
            "Residential and commercial concept studies",
            "Sacred-geometry development layouts and investor-ready packages",
            "Repair, remodel, and construction document organization",
        ],
        "lead_magnets": [
            "Request a project scope review",
            "Book a development planning consult",
            "Ask for a bid-readiness checklist",
        ],
        "monetization": [
            "Paid project planning sessions",
            "Premium owner-representation retainers",
            "Investor package and concept-board production",
            "Construction affiliate referrals and vendor routing",
        ],
        "crm_tags": ["rlc", "construction", "development", "owner-rep", "hannibal"],
        "keywords": "Hannibal MO construction planning, Royal Lee Construction Solutions, owner representation, RLC Solutions, Missouri development planning",
    },
    {
        "slug": "focusrecords",
        "canonical_path": "/focusrecords/",
        "name": "Focus Records LLC",
        "short_name": "Focus Records",
        "category": "Music, media, release systems, licensing, visual campaigns, and creative commerce",
        "headline": "A media and release-system lane for artists, catalogs, campaigns, and creative business assets.",
        "description": "Focus Records LLC is the creative media affiliate for music rollout systems, campaign assets, cover-art direction, licensing preparation, merchandise paths, and digital product packaging.",
        "contact_name": "Reginald Hilton Jr.",
        "phone": ROUTING_PHONE,
        "email": "mrreginaldhilton@gmail.com",
        "address": "Hannibal, MO",
        "services": [
            "Release planning and campaign packaging",
            "Cover-art and visual campaign direction",
            "Catalog organization and licensing preparation",
            "Artist brand systems and rollout checklists",
            "Digital products, merch, and affiliate storefront routing",
        ],
        "lead_magnets": [
            "Request an artist rollout audit",
            "Download a release checklist",
            "Book a campaign packaging session",
        ],
        "monetization": [
            "Digital music and catalog products",
            "Artist-service packages",
            "Merchandise and affiliate product links",
            "Licensing preparation and media consulting",
        ],
        "crm_tags": ["focus-records", "music", "media", "artist-services", "licensing"],
        "keywords": "Focus Records LLC, music release planning, artist rollout, music marketing Hannibal MO, licensing preparation",
    },
    {
        "slug": "waldenauto",
        "canonical_path": "/waldenauto/",
        "name": "Walden Auto",
        "short_name": "Walden Auto",
        "category": "Auto repair, collision estimates, repair authorization, and vehicle-support documentation",
        "headline": "Affiliate auto repair and collision documentation support for vehicle repair approvals.",
        "description": "Walden Auto is listed as an affiliate repair-support company for collision repair estimates, repair authorization workflows, inspection-focused repair documentation, and vehicle repair coordination connected to approved payment or grant-support processes.",
        "contact_name": "Brian Lee Walden",
        "phone": WALDEN_PHONE,
        "email": WALDEN_EMAIL,
        "address": "3269 Market Street, Hannibal, MO",
        "services": [
            "Collision repair estimates and documentation",
            "Repair authorization paperwork",
            "Vehicle repair coordination after approved payment",
            "Inspection-oriented repair planning when applicable",
            "Photo documentation and repair package organization",
        ],
        "lead_magnets": [
            "Request a repair estimate intake",
            "Upload photos for a repair package",
            "Start a vehicle repair authorization checklist",
        ],
        "monetization": [
            "Repair estimate intake fees where appropriate",
            "Collision repair jobs",
            "Documentation package support",
            "Affiliate routing from Focus Corp service pages",
        ],
        "crm_tags": ["walden-auto", "auto-repair", "collision", "vehicle-support", "hannibal"],
        "keywords": "Walden Auto Hannibal MO, collision repair estimate, vehicle repair authorization, Hannibal auto repair, grant vehicle repair documentation",
    },
    {
        "slug": "WaldensTimberCarryingConstruction",
        "canonical_path": "/WaldensTimberCarryingConstruction/",
        "name": "Waldens Timber Carrying Construction",
        "short_name": "Waldens Timber Carrying Construction",
        "category": "Timber carrying, hauling, construction support, and heavy-material coordination",
        "headline": "Timber, hauling, and construction-support routing for projects that need material movement.",
        "description": "Waldens Timber Carrying Construction is positioned as an affiliate construction-support lane for timber carrying, hauling coordination, construction support, equipment-ready project intake, and jobsite material movement.",
        "contact_name": "Brian Lee Walden",
        "phone": WALDEN_PHONE,
        "email": WALDEN_EMAIL,
        "address": "3269 Market Street, Hannibal, MO",
        "services": [
            "Timber carrying and hauling coordination",
            "Construction material movement support",
            "Jobsite support and logistics intake",
            "Commercial support request routing",
            "Affiliate construction support referrals",
        ],
        "lead_magnets": [
            "Request hauling availability",
            "Submit timber or material movement details",
            "Ask for a construction-support callback",
        ],
        "monetization": [
            "Hauling and timber-carrying jobs",
            "Construction support contracts",
            "Affiliate referral routing",
            "Local service SEO lead generation",
        ],
        "crm_tags": ["waldens-timber", "hauling", "construction-support", "timber", "hannibal"],
        "keywords": "Waldens Timber Carrying Construction, Hannibal MO hauling, timber carrying, construction support, material movement",
    },
]


def _json_ld(company: dict[str, object]) -> str:
    data = {
        "@context": "https://schema.org",
        "@type": "LocalBusiness",
        "name": company["name"],
        "url": f"{DOMAIN}{company['canonical_path']}",
        "description": company["description"],
        "telephone": company["phone"],
        "email": company["email"],
        "address": company["address"],
        "areaServed": ["Hannibal MO", "Marion County MO", "Northeast Missouri"],
        "brand": {"@type": "Brand", "name": company["short_name"]},
        "parentOrganization": {"@type": "Organization", "name": "The Focus Corporation", "url": DOMAIN},
        "sameAs": [DOMAIN],
        "knowsAbout": company["services"],
    }
    return json.dumps(data, indent=2)


def _list(items: list[str]) -> str:
    return "\n".join(f"<li>{escape(item)}</li>" for item in items)


def _crm_payload(company: dict[str, object]) -> str:
    payload = {
        "source": "thefocuscorp_affiliate_page",
        "company": company["name"],
        "slug": company["slug"],
        "crm_tags": company["crm_tags"],
        "destination": "FOCUS_CRM_WEBHOOK_URL or MAKE_WEBHOOK_URL",
        "approval_required": True,
    }
    return json.dumps(payload, indent=2)


def render_page(company: dict[str, object]) -> str:
    title = f"{company['short_name']} | The Focus Corporation Affiliate Network"
    canonical = f"{DOMAIN}{company['canonical_path']}"
    return dedent(f"""\
    <!doctype html>
    <html lang="en">
      <head>
        <meta charset="utf-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <title>{escape(title)}</title>
        <meta name="description" content="{escape(str(company['description']))}" />
        <meta name="keywords" content="{escape(str(company['keywords']))}" />
        <link rel="canonical" href="{canonical}" />
        <meta property="og:title" content="{escape(title)}" />
        <meta property="og:description" content="{escape(str(company['description']))}" />
        <meta property="og:url" content="{canonical}" />
        <meta property="og:type" content="website" />
        <style>
          :root {{ --bg:#050812; --panel:#0e1730; --ink:#f6f8ff; --muted:#c2cce5; --gold:#f2c96d; --teal:#3ee4d6; --line:rgba(124,200,255,.22); }}
          * {{ box-sizing:border-box; }}
          body {{ margin:0; font-family:Manrope, Inter, system-ui, sans-serif; color:var(--ink); background:radial-gradient(circle at top left, rgba(62,228,214,.14), transparent 32%), linear-gradient(135deg,#050812,#0a1329 55%,#07101f); }}
          a {{ color:inherit; }}
          .shell {{ width:min(1180px,92vw); margin:0 auto; padding:34px 0 64px; }}
          .nav {{ display:flex; justify-content:space-between; gap:18px; align-items:center; margin-bottom:32px; color:var(--muted); }}
          .nav a {{ text-decoration:none; border:1px solid var(--line); padding:.72rem 1rem; border-radius:999px; background:rgba(255,255,255,.04); }}
          .hero, .card, .lead-box {{ border:1px solid var(--line); background:linear-gradient(155deg, rgba(14,23,48,.92), rgba(10,19,41,.82)); border-radius:30px; box-shadow:0 24px 80px rgba(0,0,0,.28); }}
          .hero {{ padding:clamp(28px,5vw,64px); display:grid; gap:24px; }}
          .eyebrow {{ color:var(--teal); text-transform:uppercase; letter-spacing:.18em; font-size:.78rem; font-weight:800; }}
          h1 {{ font-size:clamp(2.4rem,6vw,5rem); line-height:.94; margin:0; max-width:980px; }}
          h2 {{ font-size:clamp(1.45rem,3vw,2.35rem); margin:.2rem 0 1rem; }}
          p {{ color:var(--muted); line-height:1.75; max-width:820px; }}
          .actions {{ display:flex; flex-wrap:wrap; gap:12px; }}
          .btn {{ border:1px solid var(--line); padding:1rem 1.15rem; border-radius:999px; text-decoration:none; font-weight:800; background:rgba(255,255,255,.06); }}
          .btn.primary {{ color:#06101e; background:linear-gradient(135deg,var(--gold),#ff9b68); border:0; }}
          .grid {{ display:grid; grid-template-columns:repeat(3,minmax(0,1fr)); gap:16px; margin-top:18px; }}
          .two {{ grid-template-columns:repeat(2,minmax(0,1fr)); }}
          .card, .lead-box {{ padding:24px; }}
          ul {{ margin:0; padding-left:1.2rem; color:var(--muted); line-height:1.85; }}
          .contact {{ display:grid; gap:8px; color:var(--muted); }}
          .crm {{ white-space:pre-wrap; overflow:auto; padding:18px; border-radius:18px; background:#040a16; border:1px solid var(--line); color:#eaf2ff; font-family:ui-monospace, SFMono-Regular, Consolas, monospace; font-size:.86rem; }}
          .footer {{ margin-top:28px; color:var(--muted); font-size:.9rem; }}
          @media (max-width:900px) {{ .grid,.two {{ grid-template-columns:1fr; }} .nav {{ align-items:flex-start; flex-direction:column; }} }}
        </style>
        <script type="application/ld+json">{_json_ld(company)}</script>
      </head>
      <body>
        <main class="shell">
          <nav class="nav">
            <strong>The Focus Corporation Affiliate Network</strong>
            <span><a href="/">Home</a> <a href="/services.html">Services</a> <a href="/products.html">Products</a></span>
          </nav>
          <section class="hero">
            <div class="eyebrow">{escape(str(company['category']))}</div>
            <h1>{escape(str(company['headline']))}</h1>
            <p>{escape(str(company['description']))}</p>
            <div class="actions">
              <a class="btn primary" href="tel:{str(company['phone']).replace('-', '')}">Call {escape(str(company['phone']))}</a>
              <a class="btn" href="mailto:{escape(str(company['email']))}?subject={escape(str(company['short_name']))}%20Lead%20from%20TheFocusCorp.com">Email Intake</a>
              <a class="btn" href="/booking.html">Book Through Focus Corp</a>
            </div>
          </section>

          <section class="grid two">
            <article class="card">
              <div class="eyebrow">Services</div>
              <h2>What this page routes</h2>
              <ul>{_list(company['services'])}</ul>
            </article>
            <article class="card">
              <div class="eyebrow">Contact</div>
              <h2>Company intake details</h2>
              <div class="contact">
                <span><strong>Contact:</strong> {escape(str(company['contact_name']))}</span>
                <span><strong>Phone:</strong> {escape(str(company['phone']))}</span>
                <span><strong>Email:</strong> {escape(str(company['email']))}</span>
                <span><strong>Address:</strong> {escape(str(company['address']))}</span>
              </div>
            </article>
          </section>

          <section class="grid">
            <article class="card">
              <div class="eyebrow">Lead funnel</div>
              <h2>Capture path</h2>
              <ul>{_list(company['lead_magnets'])}</ul>
            </article>
            <article class="card">
              <div class="eyebrow">Monetization</div>
              <h2>Revenue paths</h2>
              <ul>{_list(company['monetization'])}</ul>
            </article>
            <article class="card">
              <div class="eyebrow">SEO automation</div>
              <h2>Search growth</h2>
              <ul>
                <li>LocalBusiness schema embedded on this route.</li>
                <li>Affiliate internal links route authority from The Focus Corporation.</li>
                <li>CRM tags enable follow-up automations and segmented campaigns.</li>
                <li>Future city/service pages can be generated from the same data object.</li>
              </ul>
            </article>
          </section>

          <section class="lead-box" style="margin-top:16px;">
            <div class="eyebrow">CRM hook payload</div>
            <h2>Automation handoff</h2>
            <p>Use this payload shape for Make, Zapier MCP, a custom backend, or the Focus Master AI operator runtime. Keep final sending and account changes behind human approval.</p>
            <div class="crm">{escape(_crm_payload(company))}</div>
          </section>
          <p class="footer">© The Focus Corporation. Affiliate page generated by the Focus AI public build pipeline.</p>
        </main>
      </body>
    </html>
    """)


def write_page(company: dict[str, object]) -> None:
    target = PUBLIC / str(company["slug"])
    target.mkdir(parents=True, exist_ok=True)
    (target / "index.html").write_text(render_page(company), encoding="utf-8")
    # Compatibility file for hosts or old links that prefer .html paths.
    redirect = f'<!doctype html><meta http-equiv="refresh" content="0; url=/{company["slug"]}/"><link rel="canonical" href="{DOMAIN}{company["canonical_path"]}">'
    (PUBLIC / f"{company['slug']}.html").write_text(redirect, encoding="utf-8")


def main() -> int:
    PUBLIC.mkdir(parents=True, exist_ok=True)
    for company in COMPANIES:
        write_page(company)
    manifest = {
        "generated": [f"{DOMAIN}{company['canonical_path']}" for company in COMPANIES],
        "count": len(COMPANIES),
        "source": "focus_ai/scripts/build_affiliate_pages.py",
    }
    (PUBLIC / "affiliate-pages-manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    print(json.dumps(manifest, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
