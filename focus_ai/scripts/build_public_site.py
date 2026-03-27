#!/usr/bin/env python3
import os
import shutil
import stat
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PUBLISHED = ROOT / "published" / "ebooks"
SITE = ROOT / "site"
PUBLIC = ROOT / "published" / "public_site"
PRIMARY_CONTACT_NAME = "Alexis Rogers"
PRIMARY_CONTACT_PHONE = "2172576222"
BOOK_BUNDLE_URL = os.getenv(
    "FOCUS_BOOK_BUNDLE_URL",
    "https://buy.stripe.com/bJe7sKh2B6ZQ8bP4II5os02",
)
BLUEPRINT_PACK_URL = os.getenv(
    "FOCUS_BLUEPRINT_PACK_URL",
    "https://buy.stripe.com/cNi4gy27H83U4ZD3EE5os03",
)
BUSINESS_ENGINE_URL = os.getenv(
    "FOCUS_BUSINESS_ENGINE_URL",
    "https://buy.stripe.com/4gMbJ0aEd97Y9fT2AA5os04",
)


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
    # Handles Windows/OneDrive read-only files during cleanup.
    os.chmod(path, stat.S_IWRITE)
    func(path)


def safe_rmtree(path: Path) -> None:
    if not path.exists():
        return
    shutil.rmtree(path, onerror=_on_rm_error)


def build() -> int:
    if not PUBLISHED.exists():
        print("Missing published ebooks. Run publish_ebooks.py first.")
        return 1

    if PUBLIC.exists():
        safe_rmtree(PUBLIC)
    PUBLIC.mkdir(parents=True, exist_ok=True)

    copy_tree(PUBLISHED, PUBLIC / "ebooks")

    preview_html = SITE / "visual_preview.html"
    preview_css = SITE / "visual_preview.css"
    if preview_html.exists():
        html = preview_html.read_text(encoding="utf-8")
        html = html.replace("../published/ebooks/index.html", "ebooks/index.html")
        html = html.replace("../published/public_site/landing.html", "landing.html")
        html = html.replace("../published/public_site/offers.html", "offers.html")
        html = html.replace("../published/public_site/funnel_landing.html", "funnel_landing.html")
        (PUBLIC / "index.html").write_text(html, encoding="utf-8")
    if preview_css.exists():
        shutil.copy2(preview_css, PUBLIC / "visual_preview.css")

    landing = PUBLIC / "landing.html"
    landing.write_text(
        """<!doctype html>
<html lang="en"><head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
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
    <div class="card">
      <p><a href="index.html">View visual preview homepage</a></p>
      <p><a href="offers.html">View live offers and checkout links</a></p>
      <p><a href="booking.html">Book with Alexis Rogers</a></p>
      <p><a href="services.html">View company services</a></p>
      <p><a href="products.html">Browse products and offers</a></p>
      <p><a href="ebooks/index.html">View published eBook library</a></p>
      <p><a href="funnel_landing.html">Enter the sales funnel</a></p>
    </div>
  </main>
</body></html>
""",
        encoding="utf-8",
    )

    funnel_css = PUBLIC / "funnel.css"
    funnel_css.write_text(
        """
body {
  font-family: Inter, Arial, sans-serif;
  margin: 0;
  background: #0d1022;
  color: #ecf0ff;
}
main {
  max-width: 860px;
  margin: 0 auto;
  padding: 2.5rem 1rem 4rem;
}
h1, h2, h3 { line-height: 1.2; }
.card {
  border: 1px solid #2b356d;
  border-radius: 14px;
  background: #171d3f;
  padding: 1.2rem 1.3rem;
  margin: 1rem 0;
}
.btn {
  display: inline-block;
  text-decoration: none;
  font-weight: 600;
  color: #0c1024;
  background: #9de6ff;
  padding: 0.7rem 1rem;
  border-radius: 10px;
}
.btn.secondary {
  background: transparent;
  color: #9de6ff;
  border: 1px solid #9de6ff;
}
ul { padding-left: 1.2rem; }
.small { opacity: 0.85; font-size: 0.95rem; }
.price { color: #ffd882; font-size: 1.2rem; font-weight: 700; }
.offer-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: 1rem;
}
input[type="email"] {
  width: min(520px, 95%);
  background: #0f1430;
  color: #ecf0ff;
  border: 1px solid #4352a0;
  border-radius: 8px;
  padding: 0.75rem;
  margin-bottom: 0.8rem;
}
nav a { color: #9de6ff; text-decoration: none; margin-right: 1rem; }
""".strip()
        + "\n",
        encoding="utf-8",
    )

    funnel_pages = {
        "booking.html": f"""<!doctype html>
<html lang="en"><head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Book with {PRIMARY_CONTACT_NAME}</title>
  <link rel="stylesheet" href="funnel.css" />
</head><body><main>
  <nav><a href="index.html">Home</a><a href="services.html">Services</a><a href="products.html">Products</a></nav>
  <p class="small">Primary contact and routing</p>
  <h1>Book with {PRIMARY_CONTACT_NAME}</h1>
  <div class="card">
    <p>{PRIMARY_CONTACT_NAME} is the central point of contact for Focus Records LLC, Royal Lee Construction Solutions LLC, and Focus Negotium Inc.</p>
    <p><strong>Call now:</strong> <a href="tel:{PRIMARY_CONTACT_PHONE}">{PRIMARY_CONTACT_PHONE}</a></p>
    <p><strong>Best use:</strong> strategy calls, service routing, project discovery, and product questions.</p>
  </div>
  <div class="card">
    <h2>Meeting options</h2>
    <ul>
      <li>Creative planning for Focus Records LLC</li>
      <li>Build and design planning for Royal Lee Construction Solutions LLC</li>
      <li>Automation, negotiation, and monetization planning for Focus Negotium Inc</li>
    </ul>
    <p class="small">Until calendar automation is connected, call or text to schedule the next open slot.</p>
  </div>
</main></body></html>
""",
        "services.html": f"""<!doctype html>
<html lang="en"><head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Services Across Three Companies</title>
  <link rel="stylesheet" href="funnel.css" />
</head><body><main>
  <nav><a href="index.html">Home</a><a href="booking.html">Booking</a><a href="products.html">Products</a></nav>
  <p class="small">Choose the right company path</p>
  <h1>Services</h1>
  <div class="card">
    <h2>Focus Records LLC</h2>
    <ul>
      <li>Creative direction and release support</li>
      <li>Visual rollout systems and branded content planning</li>
      <li>Audience growth and campaign structure</li>
    </ul>
  </div>
  <div class="card">
    <h2>Royal Lee Construction Solutions LLC</h2>
    <ul>
      <li>Sacred geometry build consulting</li>
      <li>Design and layout strategy</li>
      <li>Construction planning and execution support</li>
    </ul>
  </div>
  <div class="card">
    <h2>Focus Negotium Inc</h2>
    <ul>
      <li>Business systems and process design</li>
      <li>Negotiation support and offer architecture</li>
      <li>Automation and monetization workflow planning</li>
    </ul>
    <p><a class="btn" href="booking.html">Route me through {PRIMARY_CONTACT_NAME}</a></p>
  </div>
</main></body></html>
""",
        "products.html": f"""<!doctype html>
<html lang="en"><head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Products and Offers</title>
  <link rel="stylesheet" href="funnel.css" />
</head><body><main>
  <nav><a href="index.html">Home</a><a href="services.html">Services</a><a href="ebooks/index.html">eBooks</a></nav>
  <p class="small">Current product paths</p>
  <h1>Products and Offers</h1>
  <div class="card">
    <h2>Digital products</h2>
    <p>Published eBooks, sacred geometry guides, and workflow-driven business assets.</p>
    <p><a class="btn" href="ebooks/index.html">Browse published eBooks</a></p>
  </div>
  <div class="card">
    <h2>Live checkout ladder</h2>
    <p>Ready-to-buy offers now route through the Focus AI launch flow.</p>
    <p><a class="btn" href="offers.html">View live offers</a></p>
  </div>
  <div class="card">
    <h2>Service-backed offers</h2>
    <p>Strategy calls, build consulting, and automation planning available through the three-company network.</p>
    <p><a class="btn secondary" href="services.html">Compare services</a></p>
  </div>
  <div class="card">
    <h2>Manual purchase path</h2>
    <p>For now, purchases and custom invoices route through {PRIMARY_CONTACT_NAME} at <a href="tel:{PRIMARY_CONTACT_PHONE}">{PRIMARY_CONTACT_PHONE}</a>.</p>
    <p class="small">This keeps the flow live while payment processor setup remains separate.</p>
</div>
</main></body></html>
""",
        "offers.html": f"""<!doctype html>
<html lang="en"><head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Focus AI Offers</title>
  <link rel="stylesheet" href="funnel.css" />
</head><body><main>
  <nav><a href="landing.html">Home</a><a href="ebooks/index.html">eBooks</a><a href="funnel_landing.html">Funnel</a></nav>
  <p class="small">Live offer ladder</p>
  <h1>Focus AI Revenue Engine</h1>
  <p>Choose the fastest entry point for your build, content, and monetization workflow.</p>
  <div class="offer-grid">
    <section class="card">
      <h2>Focus AI eBook Bundle</h2>
      <p>Five published eBooks, sacred geometry prompts, and practical reading for founders and builders.</p>
      <p class="price">$49 one time</p>
      <p><a class="btn" href="{BOOK_BUNDLE_URL}">Buy the eBook Bundle</a></p>
    </section>
    <section class="card">
      <h2>Focus AI Blueprint Pack</h2>
      <p>Implementation materials, blueprint thinking, and business workflow assets for turning ideas into products.</p>
      <p class="price">$299 one time</p>
      <p><a class="btn" href="{BLUEPRINT_PACK_URL}">Buy the Blueprint Pack</a></p>
    </section>
    <section class="card">
      <h2>Focus AI Business Engine</h2>
      <p>The flagship premium system for AI workflows, launch assets, operating structure, and delivery support.</p>
      <p class="price">$5,000 one time</p>
      <p><a class="btn" href="{BUSINESS_ENGINE_URL}">Buy the Business Engine</a></p>
    </section>
  </div>
</main></body></html>
""",
        "funnel_landing.html": """<!doctype html>
<html lang="en"><head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Free Download - Sacred Geometry Wealth Blueprint</title>
  <link rel="stylesheet" href="funnel.css" />
</head><body><main>
  <nav><a href="landing.html">Home</a><a href="delivery.html">Delivery Page</a></nav>
  <p class="small">Goal: Capture Leads</p>
  <h1>FREE DOWNLOAD</h1>
  <h2>Sacred Geometry Wealth Blueprint</h2>
  <p>Discover how AI-designed homes are increasing property value and creating new income streams.</p>
  <div class="card">
    <ul>
      <li>Golden Ratio layout secrets</li>
      <li>High-value home design system</li>
      <li>AI-powered architecture strategy</li>
    </ul>
  </div>
  <p><a class="btn secondary" href="offers.html">Skip ahead to live offers</a></p>
  <h3>Get Instant Access</h3>
  <p>Enter your email to download:</p>
  <form action="delivery.html" method="get">
    <input type="email" placeholder="you@example.com" aria-label="Email address" required />
    <br />
    <button class="btn" type="submit">Download Now</button>
  </form>
  <p class="small">We respect your privacy.</p>
</main></body></html>
""",
        "delivery.html": """<!doctype html>
<html lang="en"><head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Your Blueprint Is Ready</title>
  <link rel="stylesheet" href="funnel.css" />
</head><body><main>
  <nav><a href="funnel_landing.html">Lead Magnet</a><a href="book_offer.html">Book Offer</a></nav>
  <h1>Your Blueprint Is Ready</h1>
  <p>Check your email for the download.</p>
  <div class="card">
    <h2>Want to Go Deeper?</h2>
    <h3>Focus AI eBook Bundle</h3>
    <ul>
      <li>Five published eBooks in one purchase</li>
      <li>Step-by-step wealth strategy</li>
      <li>Real-world applications and prompts</li>
    </ul>
    <p><strong>Special Offer (Today Only): $49</strong></p>
    <a class="btn" href="book_offer.html">Get the Bundle Now</a>
  </div>
</main></body></html>
""",
        "book_offer.html": f"""<!doctype html>
<html lang="en"><head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Focus AI eBook Bundle</title>
  <link rel="stylesheet" href="funnel.css" />
</head><body><main>
  <nav><a href="delivery.html">Back</a><a href="upsell.html">Next Offer</a></nav>
  <h1>Focus AI eBook Bundle</h1>
  <p>Entry offer with the published library, prompts, and strategy resources.</p>
  <div class="card">
    <ul>
      <li>Instant access to the published eBook library</li>
      <li>Foundational sacred geometry and focus frameworks</li>
      <li>Entry point into the larger Focus AI offer ladder</li>
    </ul>
    <p class="price">$49 one time</p>
    <p><a class="btn" href="{BOOK_BUNDLE_URL}">Purchase the Bundle</a></p>
    <p><a class="btn secondary" href="upsell.html">See the next offer</a></p>
  </div>
</main></body></html>
""",
        "upsell.html": f"""<!doctype html>
<html lang="en"><head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Upgrade Your System</title>
  <link rel="stylesheet" href="funnel.css" />
</head><body><main>
  <nav><a href="book_offer.html">Book</a><a href="high_ticket.html">Done-For-You</a></nav>
  <h1>Upgrade Your System</h1>
  <p>You now understand the concept. Now get the actual tools.</p>
  <div class="card">
    <h2>Focus AI Blueprint Pack</h2>
    <ul>
      <li>Business workflow assets</li>
      <li>Build-ready blueprint thinking</li>
      <li>Profit-focused implementation materials</li>
    </ul>
    <p class="price">$299 one time</p>
    <p><a class="btn" href="{BLUEPRINT_PACK_URL}">Buy the Blueprint Pack</a></p>
    <p><a class="btn secondary" href="high_ticket.html">See the premium system</a></p>
  </div>
</main></body></html>
""",
        "high_ticket.html": f"""<!doctype html>
<html lang="en"><head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Done-For-You System</title>
  <link rel="stylesheet" href="funnel.css" />
</head><body><main>
  <nav><a href="upsell.html">Upsell</a><a href="email_automation.html">Email Automation</a></nav>
  <h1>Want This Done For You?</h1>
  <ul>
    <li>Business structure and systems</li>
    <li>Product setup</li>
    <li>Monetization strategy</li>
  </ul>
  <div class="card">
    <h2>Focus AI Business Engine</h2>
    <p>The flagship operating system for prompts, workflows, offers, and launch support.</p>
    <p class="price">$5,000 one time</p>
    <p>Limited premium delivery capacity</p>
    <p><a class="btn" href="{BUSINESS_ENGINE_URL}">Buy the Business Engine</a></p>
    <p><a class="btn secondary" href="email_automation.html">View follow-up campaign</a></p>
  </div>
</main></body></html>
""",
        "email_automation.html": f"""<!doctype html>
<html lang="en"><head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Email Automation Sequence</title>
  <link rel="stylesheet" href="funnel.css" />
</head><body><main>
  <nav><a href="high_ticket.html">High Ticket</a><a href="funnel_landing.html">Restart Funnel</a></nav>
  <h1>Email Automation (Critical)</h1>
  <p>Recommended tools: <strong>Mailchimp</strong> or <strong>ConvertKit</strong>.</p>
  <div class="card">
    <h2>Email 1 - Your Blueprint is Inside</h2>
    <p>Here is your Sacred Geometry Blueprint. Get the full reading bundle: <a href="{BOOK_BUNDLE_URL}">Focus AI eBook Bundle</a></p>
  </div>
  <div class="card">
    <h2>Email 2 - Why Most Systems Fail</h2>
    <p>Most systems are designed for cost, not value. Show them the next step: <a href="{BOOK_BUNDLE_URL}">eBook Bundle</a></p>
  </div>
  <div class="card">
    <h2>Email 3 - This changes everything</h2>
    <p>AI + design + structure can become a working revenue model. Upgrade here: <a href="{BLUEPRINT_PACK_URL}">Blueprint Pack</a></p>
  </div>
  <div class="card">
    <h2>Email 4 - Want the actual system?</h2>
    <p>Concept is one thing. Execution is everything. Send them here: <a href="{BLUEPRINT_PACK_URL}">Blueprint Pack</a></p>
  </div>
  <div class="card">
    <h2>Email 5 - Last chance</h2>
    <p>If you are serious about building income systems, present the premium offer directly: <a href="{BUSINESS_ENGINE_URL}">Focus AI Business Engine</a></p>
  </div>
  <div class="card">
    <h2>Scale Targets</h2>
    <p>100 visitors/day -> 10 opt-ins -> 2 bundle sales -> 1 upsell.</p>
    <p>$5k+/week is possible with real traffic, consistent posting, strong follow-up, and multiple conversions. It is a target, not a guarantee.</p>
  </div>
</main></body></html>
""",
    }

    for page_name, page_content in funnel_pages.items():
        (PUBLIC / page_name).write_text(page_content, encoding="utf-8")

    print(f"Built public site at {PUBLIC}")
    return 0


if __name__ == "__main__":
    raise SystemExit(build())
