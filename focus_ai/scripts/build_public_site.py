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
        html = preview_html.read_text(encoding="utf-8")
        html = html.replace("../published/ebooks/index.html", "ebooks/index.html")
        html = html.replace("../published/public_site/landing.html", "landing.html")
        (PUBLIC / "index.html").write_text(html, encoding="utf-8")
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
      <p><a href=\"index.html\">View sacred geometry homepage</a></p>
      <p><a href=\"ebooks/index.html\">View published eBook library</a></p>
      <p><a href=\"funnel_landing.html\">View sales funnel pages</a></p>
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
        "funnel_landing.html": """<!doctype html>
<html lang="en"><head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Free Download — Sacred Geometry Wealth Blueprint</title>
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
    <h3>Sacred Geometry Architecture Book</h3>
    <ul>
      <li>Complete design system</li>
      <li>Step-by-step wealth strategy</li>
      <li>Real-world applications</li>
    </ul>
    <p><strong>Special Offer (Today Only): $19.99</strong></p>
    <a class="btn" href="book_offer.html">Get the Book Now</a>
  </div>
</main></body></html>
""",
        "book_offer.html": """<!doctype html>
<html lang="en"><head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Sacred Geometry Architecture Book</title>
  <link rel="stylesheet" href="funnel.css" />
</head><body><main>
  <nav><a href="delivery.html">Back</a><a href="upsell.html">Next Offer</a></nav>
  <h1>Sacred Geometry Architecture Book</h1>
  <p>Low-ticket entry offer with complete system and strategy.</p>
  <div class="card">
    <p><strong>$19.99</strong></p>
    <a class="btn" href="upsell.html">Purchase + Continue</a>
  </div>
</main></body></html>
""",
        "upsell.html": """<!doctype html>
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
    <h2>Sacred Geometry Blueprint Pack</h2>
    <ul>
      <li>Real house plans</li>
      <li>Build-ready layouts</li>
      <li>Profit-focused designs</li>
    </ul>
    <p><strong>Today Only: $49 (normally $99)</strong></p>
    <a class="btn" href="high_ticket.html">Upgrade Now</a>
  </div>
</main></body></html>
""",
        "high_ticket.html": """<!doctype html>
<html lang="en"><head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Done-For-You System</title>
  <link rel="stylesheet" href="funnel.css" />
</head><body><main>
  <nav><a href="upsell.html">Upsell</a><a href="email_automation.html">Email Automation</a></nav>
  <h1>Want This Done For You?</h1>
  <ul>
    <li>Business structure (LLC + systems)</li>
    <li>Product setup</li>
    <li>Monetization strategy</li>
  </ul>
  <div class="card">
    <h2>Done-For-You System</h2>
    <p><strong>$999</strong></p>
    <p>Limited availability</p>
    <a class="btn" href="email_automation.html">Apply Now</a>
  </div>
</main></body></html>
""",
        "email_automation.html": """<!doctype html>
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
    <h2>Email 1 — Your Blueprint is Inside</h2>
    <p>Here’s your Sacred Geometry Blueprint... get the full system: [Book Link]</p>
  </div>
  <div class="card">
    <h2>Email 2 — Why Most Homes Fail</h2>
    <p>Most buildings are designed for cost — not value... See how: [Book Link]</p>
  </div>
  <div class="card">
    <h2>Email 3 — This changes everything</h2>
    <p>AI + design + structure = new income model... Get started: [Link]</p>
  </div>
  <div class="card">
    <h2>Email 4 — Want the actual designs?</h2>
    <p>Concept is one thing. Execution is everything. [Blueprint Link]</p>
  </div>
  <div class="card">
    <h2>Email 5 — Last chance</h2>
    <p>If you’re serious about building income systems... [Offer Link]</p>
  </div>
  <div class="card">
    <h2>Scale Targets</h2>
    <p>100 visitors/day → 10 opt-ins → 2 book sales → 1 upsell ≈ $90/day.</p>
    <p>Scale to $5k+/week with 500–1,000 visitors/day, consistent posting, and multiple products.</p>
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
