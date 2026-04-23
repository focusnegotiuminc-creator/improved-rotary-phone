from __future__ import annotations

BOOK_CATALOG = [
    {
        "source": "chakra_system_deep_dive.md",
        "slug": "chakra_system_deep_dive",
        "title": "Chakra System Deep Dive",
        "price_usd": 14.99,
        "tag": "Energy architecture",
        "summary": "A practical guide to chakra alignment, sacred geometry, and energetic structure for daily life and spatial design.",
        "buy_mode": "concierge",
    },
    {
        "source": "focus_on_coding_for_dummies_the_coding_bible.md",
        "slug": "focus_on_coding_for_dummies_the_coding_bible",
        "title": "Focus on Coding for Dummies: The Coding Bible",
        "price_usd": 14.99,
        "tag": "Builder mindset",
        "summary": "A motivational technical primer for turning scattered ideas into working code, systems, and repeatable execution habits.",
        "buy_mode": "concierge",
    },
    {
        "source": "focus_on_foundation.md",
        "slug": "focus_on_foundation",
        "title": "Focus on Foundation",
        "price_usd": 14.99,
        "tag": "Personal structure",
        "summary": "A grounding framework for discipline, identity, and long-term structure across business, health, and inner alignment.",
        "buy_mode": "concierge",
    },
    {
        "source": "focus_on_wtf_you_feel.md",
        "slug": "focus_on_wtf_you_feel",
        "title": "Focus on WTF You Feel",
        "price_usd": 14.99,
        "tag": "Emotional clarity",
        "summary": "A direct-language emotional decoding guide for naming internal states and transforming confusion into usable insight.",
        "buy_mode": "concierge",
    },
    {
        "source": "the_hidden_truths_of_sacred_geometry.md",
        "slug": "the_hidden_truths_of_sacred_geometry",
        "title": "The Hidden Truths of Sacred Geometry",
        "price_usd": 19.99,
        "tag": "Sacred systems",
        "summary": "An expanded sacred geometry narrative connecting pattern, architecture, symbolism, and human operating systems.",
        "buy_mode": "concierge",
    },
]


COMPANY_PROFILES = [
    {
        "id": "focus-records",
        "slug": "focus-records.html",
        "name": "Focus Records LLC",
        "eyebrow": "Creative campaigns and release architecture",
        "headline": "Creative direction, launch systems, and audience-facing brand execution.",
        "description": "Focus Records LLC turns raw creative work into launch-ready campaigns, branded content, and audience growth systems with a premium visual and narrative standard.",
        "proof_points": [
            "Release planning and rollout architecture",
            "Branded content systems for web, social, and launch pages",
            "Campaign messaging that aligns creative identity with conversion",
        ],
        "services": [
            {
                "title": "Artist or Brand Signal Session",
                "price_usd": 149,
                "summary": "A focused strategy call for release direction, messaging, and positioning clarity.",
            },
            {
                "title": "Content Campaign Sprint",
                "price_usd": 699,
                "summary": "A compact system for campaign copy, page direction, and short-form audience growth assets.",
            },
            {
                "title": "Launch System Buildout",
                "price_usd": 1800,
                "summary": "A full creative rollout package for release planning, branded assets, and conversion structure.",
            },
        ],
    },
    {
        "id": "royal-lee-construction",
        "slug": "royal-lee-construction.html",
        "name": "Royal Lee Construction Solutions LLC",
        "eyebrow": "Sacred geometry build strategy",
        "headline": "Consulting, design-planning, and construction strategy for aligned, buildable spaces.",
        "description": "Royal Lee Construction Solutions LLC bridges sacred geometry, practical build planning, and construction-ready strategy for clients who want spaces that feel intentional and structurally sound.",
        "proof_points": [
            "Sacred geometry planning for layouts and room flow",
            "Blueprint interpretation and construction strategy support",
            "Owner-facing documentation and premium package delivery",
        ],
        "services": [
            {
                "title": "Sacred Geometry Site Review",
                "price_usd": 249,
                "summary": "A paid consultation for reviewing the site, use case, and geometric alignment opportunities.",
            },
            {
                "title": "Blueprint and Scope Strategy Package",
                "price_usd": 1250,
                "summary": "A build-ready strategy packet with layout guidance, scope notes, and decision support.",
            },
            {
                "title": "Construction Planning Intensive",
                "price_usd": 4800,
                "summary": "A premium package for project structure, cost framing, and execution guidance before build kickoff.",
            },
        ],
    },
    {
        "id": "focus-negotium",
        "slug": "focus-negotium.html",
        "name": "Focus Negotium Inc",
        "eyebrow": "Operations, monetization, and business architecture",
        "headline": "Offer systems, negotiation support, automation mapping, and premium operating design.",
        "description": "Focus Negotium Inc helps founders and operators turn scattered ideas into monetizable systems, higher-trust service offers, and organized business infrastructure.",
        "proof_points": [
            "Offer architecture with premium pricing logic",
            "Automation planning without losing operator control",
            "Business system design across sales, delivery, and follow-up",
        ],
        "services": [
            {
                "title": "Offer Architecture Session",
                "price_usd": 199,
                "summary": "A paid strategy consult for pricing, positioning, and business-system direction.",
            },
            {
                "title": "Operations Automation Sprint",
                "price_usd": 1500,
                "summary": "A focused build sprint for workflows, assistant routing, and monetization structure.",
            },
            {
                "title": "Business OS Buildout",
                "price_usd": 5000,
                "summary": "A flagship engagement for full business-system design, launch structure, and execution support.",
            },
        ],
    },
]


BOOK_BY_SOURCE = {item["source"]: item for item in BOOK_CATALOG}
COMPANY_BY_ID = {item["id"]: item for item in COMPANY_PROFILES}
