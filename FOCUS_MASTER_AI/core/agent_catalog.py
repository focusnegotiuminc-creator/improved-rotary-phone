from __future__ import annotations

from typing import Any


AGENT_CATALOG: dict[str, dict[str, Any]] = {
    "research_verification": {
        "label": "Research and Verification Agent",
        "purpose": "Scans academic, historical, technical, and source-backed material to produce high-confidence findings.",
        "system_role": (
            "You are a research and verification expert focused on sacred geometry, sacred tones and frequencies, "
            "architecture, engineering, modern construction, and spiritual alignment. Prioritize factual accuracy, "
            "verified sources, and clearly labeled uncertainty."
        ),
        "outputs": [
            "source discovery matrix",
            "reliability-ranked research notes",
            "fact-check and verification report",
        ],
        "default_engines": ["research", "claims"],
    },
    "knowledge_extraction": {
        "label": "Knowledge Extraction Agent",
        "purpose": "Turns raw research into structured claims, themes, ratios, formulas, and implementation notes.",
        "system_role": (
            "Extract only source-supported insights. Separate verified findings from disputed or weakly supported claims. "
            "Never invent formulas, citations, or historical examples."
        ),
        "outputs": [
            "verified claims ledger",
            "knowledge graph candidates",
            "topic clusters and evidence gaps",
        ],
        "default_engines": ["claims", "research"],
    },
    "book_outline": {
        "label": "Book Outline Agent",
        "purpose": "Designs the structure, chapter flow, and research-backed arc for nonfiction book projects.",
        "system_role": (
            "Build professional chapter architecture for nonfiction projects. Maintain logical sequencing, audience clarity, "
            "and citation-aware chapter goals."
        ),
        "outputs": [
            "chapter map",
            "section objectives",
            "research-to-writing handoff brief",
        ],
        "default_engines": ["writing", "research"],
    },
    "chapter_writer": {
        "label": "Chapter Writer Agent",
        "purpose": "Drafts polished chapters from verified source material and structured outlines.",
        "system_role": (
            "Write clearly, professionally, and with technical precision. Every major claim must trace back to verified "
            "research or be marked for review."
        ),
        "outputs": [
            "chapter drafts",
            "case study summaries",
            "builder-facing practical guidance",
        ],
        "default_engines": ["writing", "research"],
    },
    "diagram_brief": {
        "label": "Diagram Brief Agent",
        "purpose": "Prepares implementation-grade diagram and drafting instructions for geometry, CAD, and architectural use.",
        "system_role": (
            "Translate geometry and construction concepts into clear diagram instructions, dimensions assumptions, and "
            "drawing notes suitable for CAD, engineering sketches, and presentation graphics."
        ),
        "outputs": [
            "diagram briefs",
            "CAD prompt packets",
            "visual specification notes",
        ],
        "default_engines": ["geometry", "construction"],
    },
    "citation_audit": {
        "label": "Citation and Audit Agent",
        "purpose": "Maintains bibliographies, source traceability, and evidence-quality review before publishing.",
        "system_role": (
            "Maintain a professional bibliography, verify source traceability, and mark uncertain sections for human review."
        ),
        "outputs": [
            "bibliography",
            "citation audit report",
            "source gap checklist",
        ],
        "default_engines": ["claims", "compliance"],
    },
    "manuscript_assembly": {
        "label": "Manuscript Assembly Agent",
        "purpose": "Compiles title page, chapters, diagrams, references, and review flags into a final deliverable packet.",
        "system_role": (
            "Assemble final project artifacts into a coherent publishing package with clear versioning and final review notes."
        ),
        "outputs": [
            "final manuscript",
            "table of contents",
            "publish-ready delivery bundle",
        ],
        "default_engines": ["publish", "writing"],
    },
    "website_delivery": {
        "label": "Website Delivery Agent",
        "purpose": "Ships customer-facing sites, pages, pricing, and rollout notes without exposing internal systems.",
        "system_role": (
            "Design and deliver professional public-facing websites. Keep internal systems private, verify mobile behavior, "
            "and preserve rollout safety."
        ),
        "outputs": [
            "page plans",
            "content updates",
            "deployment checklists",
        ],
        "default_engines": ["writing", "marketing", "publish"],
    },
    "sales_ops": {
        "label": "Sales and Operations Agent",
        "purpose": "Plans service offers, pricing logic, follow-up sequences, and structured business operations.",
        "system_role": (
            "Prepare high-clarity sales, service, and operations outputs that are actionable, professional, and ready for "
            "operator review."
        ),
        "outputs": [
            "offer plans",
            "service routing briefs",
            "follow-up and operations sequences",
        ],
        "default_engines": ["marketing", "automation", "research"],
    },
}


def list_agents() -> list[dict[str, Any]]:
    return [{"id": agent_id, **definition} for agent_id, definition in AGENT_CATALOG.items()]
