"""Generate 10 long-form book manuscripts priced at $19.99 each."""

from __future__ import annotations

from pathlib import Path
from textwrap import dedent

ROOT = Path(__file__).resolve().parents[1]
BOOK_DIR = ROOT / "book"

BOOKS = [
    "Sacred Geometry Architecture: Designing Homes That Generate Energy & Wealth",
    "The Golden Ratio Blueprint: AI-Designed Structures for Maximum Profit",
    "AI Real Estate Empire: Automated Property Design & Passive Income Systems",
    "Spiritual Engineering: Building Homes Aligned with Human Frequency",
    "The $1M Construction Method: High-Profit Building Systems Explained",
    "Automated Income Architecture: How AI Builds Wealth Systems",
    "Sacred Business Structures: LLCs, Trusts & Corporate Power Systems",
    "Blueprint to Wealth: Turning Designs into Cash Flow Machines",
    "AI Passive Income Systems: From Zero to Automated Revenue",
    "The Infinite Builder: Combining AI, Geometry, and Wealth Creation",
]


def slugify(title: str) -> str:
    keep = "-_.() "
    sanitized = "".join(c for c in title if c.isalnum() or c in keep).strip()
    return sanitized.replace(" ", "_") + ".md"


def chapter_block(chapter: int, title: str) -> str:
    return dedent(
        f"""
        ## Chapter {chapter}: {title}

        ### Positioning
        - **Audience:** Builders, operators, designers, and entrepreneurs who want practical systems.
        - **Problem Solved:** High-cost projects that fail to convert into premium value.
        - **Transformation:** A repeatable process that combines proportional design, business infrastructure, and AI workflows.

        ### Value Design
        1. Define the desired market and buyer profile.
        2. Map design constraints (budget, zoning, timeline, target margin).
        3. Apply measurable standards (daylight performance, circulation, operating cost).
        4. Build a monetization path (sale, rent, licensing, education, consulting).

        ### Differentiation
        This chapter prioritizes execution and measurable outcomes rather than abstract theory.

        ### Credibility Notes
        - Where claims are predictive, mark them as assumptions.
        - Validate assumptions with local market data, cost estimators, and permitting requirements.

        ### Monetization Layer
        - Entry: checklists and mini-guides.
        - Mid-tier: blueprint packs and calculators.
        - Premium: implementation consulting and done-for-you setup.

        ### Execution Sprint
        - **Day 1:** Scope and constraints.
        - **Day 2:** Draft concept + cost model.
        - **Day 3:** Offer design + market messaging.
        - **Day 4:** Distribution setup.
        - **Day 5:** Launch and feedback capture.
        """
    ).strip()


def generate_book(title: str) -> str:
    chapters = [
        "Sacred Geometry Fundamentals and Market Psychology",
        "AI-Assisted Layout Systems and Buildability",
        "Construction Economics and Risk Management",
        "Monetization Systems Across KDP, Gumroad, and Services",
        "Authority Building, Distribution, and Long-Term Scaling",
        "Automation SOPs and Metrics for Continuous Improvement",
        "Compliance, Ethics, and Client Trust Frameworks",
        "90-Day Implementation Plan and Expansion Roadmap",
    ]

    chapter_sections = "\n\n".join(chapter_block(i + 1, c) for i, c in enumerate(chapters))

    extra_note = ""
    if "Sacred Business Structures" in title:
        extra_note = "\n\n> Educational content only. Not legal, tax, or investment advice. Consult licensed professionals in your jurisdiction."

    return dedent(
        f"""
        # {title}

        **List Price:** $19.99 (rounded positioning: $20)

        ## Introduction
        This manuscript is designed as a premium long-form asset for founders, builders, and creators at the intersection
        of architecture, sacred geometry, and business systems. The goal is to convert ideas into ethical, measurable,
        and scalable value.

        ## Core Promise
        By applying the methods in this book, readers can improve decision quality, reduce waste, and build products
        and services with stronger margins and clearer differentiation.

        {chapter_sections}

        ## Publishing Notes
        - Format for KDP print, KDP ebook, and direct digital distribution.
        - Maintain transparent claims and cite data sources in final publication drafts.
        - Include worksheets, checklists, and implementation templates to increase reader outcomes.

        ## Conclusion
        Revenue durability comes from quality, trust, and disciplined distribution. Use this framework to create useful,
        responsible offers that help clients while building sustainable growth.
        {extra_note}
        """
    ).strip() + "\n"


def main() -> None:
    BOOK_DIR.mkdir(parents=True, exist_ok=True)
    for title in BOOKS:
        path = BOOK_DIR / slugify(title)
        path.write_text(generate_book(title), encoding="utf-8")
        print(f"[BOOK] Wrote {path.name}")


if __name__ == "__main__":
    main()
