"""Generate multi-channel marketing assets for books/products/services."""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from textwrap import dedent

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "marketing" / "marketing_assets.md"
EMAIL_OUT = ROOT / "marketing" / "email_automation.md"
FUNNEL_OUT = ROOT / "marketing" / "funnel_pages.md"


def build_marketing_drop() -> str:
    now = datetime.now(timezone.utc).isoformat()
    return dedent(
        f"""
        # Marketing Content Drop ({now})

        Hook → Insight → CTA (link in bio)

        ## Funnel Architecture
        Traffic -> Free Value (Lead Magnet) -> Email Capture -> Low Ticket ($20 Book)
        -> Mid Ticket ($49-$149) -> High Ticket ($299-$999) -> Automation + Follow-ups

        ## Short-Form Video Scripts (20 ideas)
        1. Three layout mistakes lowering property value.
        2. Golden ratio explained in under 60 seconds.
        3. Why design psychology affects buyer conversion.
        4. Blueprint monetization starter checklist.
        5. How to package a $49 starter offer.
        6. How to upsell from $49 to $299 ethically.
        7. The simplest KDP pipeline for authority building.
        8. Trust-building with transparent claims.
        9. How to turn one idea into five products.
        10. Funnel math for builders and consultants.
        11. Weekly content workflow for small teams.
        12. What to automate first in your business.
        13. Offer stack architecture in 5 minutes.
        14. Red flags in legal/financial marketing claims.
        15. High-trust CTA frameworks.
        16. Converting blueprint buyers into service clients.
        17. Packaging case studies without hype.
        18. How to structure recurring advisory offers.
        19. 90-day execution dashboard walkthrough.
        20. What to measure every week for growth.

        ## Scaling Math Example
        - 100 visitors/day
        - 10 opt-ins
        - 2 book sales ($40)
        - 1 upsell ($49)
        - Approx. $90/day baseline before higher-ticket closes
        """
    ).strip() + "\n"


def build_email_sequence() -> str:
    return dedent(
        """
        # Email Automation Sequence (Mailchimp or ConvertKit)

        ## ESP Setup
        - Create list/tag: `sacred-geometry-leads`
        - Trigger: new lead captured from `/landing`
        - Delay cadence: Day 0, 1, 3, 5, 7

        ### Email 1
        **Subject:** Your Blueprint is Inside
        Here's your Sacred Geometry Blueprint. This is the same system being used to design higher-value homes.
        If you want the full system, get it here: [Book Link]

        ### Email 2
        **Subject:** Why Most Homes Fail
        Most buildings are designed for cost - not value. That's why they feel off and sell average.
        See how the system fixes this: [Book Link]

        ### Email 3
        **Subject:** This changes everything
        AI + design + structure = a new income model. Use it to design homes, sell plans, and build recurring income.
        Get started: [Book Link]

        ### Email 4
        **Subject:** Want the actual designs?
        Concept is one thing. Execution is everything. Get the blueprint pack here: [Blueprint Link]

        ### Email 5
        **Subject:** Last chance
        If you're serious about building income systems, this is your entry point. [Offer Link]

        ## Automation Flow
        GitHub update -> create content -> publish to social -> capture leads -> email sequence -> sales + upsells.
        """
    ).strip() + "\n"


def build_funnel_pages() -> str:
    return dedent(
        """
        # Funnel Page Copy Blocks

        ## 1) Landing Page (Capture Leads)
        FREE DOWNLOAD: Sacred Geometry Wealth Blueprint.
        CTA: Download Now.

        ## 2) Delivery Page (Immediate Book Offer)
        Your Blueprint Is Ready + $19.99 book special offer.

        ## 3) Core Sales Page
        Use long-form book sales page and testimonials/case framing.

        ## 4) Upsell Page
        Sacred Geometry Blueprint Pack: $49 today-only positioning.

        ## 5) High-Ticket Page
        Done-For-You System at $999 with application CTA.

        ## 6) Scale Plan
        Target 500-1,000 visitors/day with consistent posting and multi-product ladder.
        """
    ).strip() + "\n"


def main() -> None:
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(build_marketing_drop(), encoding="utf-8")
    EMAIL_OUT.write_text(build_email_sequence(), encoding="utf-8")
    FUNNEL_OUT.write_text(build_funnel_pages(), encoding="utf-8")
    print(f"[MARKETING] Wrote {OUT}")
    print(f"[EMAIL] Wrote {EMAIL_OUT}")
    print(f"[FUNNEL] Wrote {FUNNEL_OUT}")


if __name__ == "__main__":
    main()
