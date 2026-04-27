from __future__ import annotations

from typing import Any


STACK_REGISTRY: dict[str, dict[str, Any]] = {
    "website_delivery_stack": {
        "label": "Website Delivery Stack",
        "objective": "Plan, draft, verify, and publish customer-facing website work.",
        "workflow_names": [
            "Website Design and Deployment",
            "Storefront and Stripe Offers",
        ],
        "primary_engine": "writing",
        "engine_sequence": ["research", "writing", "marketing", "publish", "automation"],
        "agents": ["website_delivery", "sales_ops"],
        "tools": ["github_workspace", "stripe_catalog", "figma_canvas", "creative_studio", "automation_router"],
    },
    "real_estate_development_stack": {
        "label": "Real Estate Development Stack",
        "objective": "Build decision-ready development, construction, and property-operation packets.",
        "workflow_names": [
            "Real Estate Development Packet",
            "Property Management Setup",
        ],
        "primary_engine": "construction",
        "engine_sequence": ["research", "geometry", "construction", "compliance", "writing", "automation"],
        "agents": ["research_verification", "diagram_brief", "website_delivery"],
        "tools": ["geometry_lab", "construction_specs", "knowledge_base", "automation_router"],
    },
    "media_release_stack": {
        "label": "Media Release Stack",
        "objective": "Package release campaigns, visual assets, and catalog handoffs.",
        "workflow_names": [
            "Release Campaign and Media Packaging",
        ],
        "primary_engine": "marketing",
        "engine_sequence": ["research", "writing", "ai_twin", "marketing", "publish", "automation"],
        "agents": ["sales_ops", "website_delivery"],
        "tools": ["creative_studio", "media_pipeline", "github_workspace", "publishing_router"],
    },
    "client_intake_stack": {
        "label": "Client Intake Stack",
        "objective": "Normalize client requests into scoped service, routing, and follow-up actions.",
        "workflow_names": [
            "Client Intake and Service Routing",
        ],
        "primary_engine": "research",
        "engine_sequence": ["research", "claims", "writing", "automation"],
        "agents": ["sales_ops", "research_verification"],
        "tools": ["knowledge_base", "crm_bridge", "automation_router"],
    },
    "sacred_geometry_book_stack": {
        "label": "Sacred Geometry Book Stack",
        "objective": "Research, verify, outline, draft, diagram, audit, and assemble nonfiction books with source discipline.",
        "workflow_names": [
            "Sacred Geometry Book Research and Publishing",
        ],
        "primary_engine": "research",
        "engine_sequence": ["research", "claims", "writing", "geometry", "construction", "compliance", "publish", "automation"],
        "agents": [
            "research_verification",
            "knowledge_extraction",
            "book_outline",
            "chapter_writer",
            "diagram_brief",
            "citation_audit",
            "manuscript_assembly",
        ],
        "tools": ["knowledge_base", "geometry_lab", "publishing_router", "github_workspace", "artifact_archive"],
    },
    "productivity_command_stack": {
        "label": "Productivity Command Stack",
        "objective": "Prioritize tasks, organize knowledge, and build operator-ready plans across business systems.",
        "workflow_names": [
            "Executive Planning and Prioritization",
        ],
        "primary_engine": "automation",
        "engine_sequence": ["research", "frequency", "writing", "automation"],
        "agents": ["sales_ops"],
        "tools": ["task_hub", "knowledge_base", "automation_router", "calendar_optimizer"],
    },
}


def list_stacks() -> list[dict[str, Any]]:
    return [{"id": stack_id, **definition} for stack_id, definition in STACK_REGISTRY.items()]


def resolve_stack(workflow: str, mission: str = "", explicit_stack: str | None = None) -> dict[str, Any]:
    if explicit_stack and explicit_stack in STACK_REGISTRY:
        return {"id": explicit_stack, **STACK_REGISTRY[explicit_stack]}

    for stack_id, definition in STACK_REGISTRY.items():
        if workflow in definition.get("workflow_names", []):
            return {"id": stack_id, **definition}

    text = mission.lower()
    if "book" in text or "manuscript" in text or "bibliography" in text:
        return {"id": "sacred_geometry_book_stack", **STACK_REGISTRY["sacred_geometry_book_stack"]}
    if "website" in text or "storefront" in text or "deployment" in text:
        return {"id": "website_delivery_stack", **STACK_REGISTRY["website_delivery_stack"]}
    if "property" in text or "construction" in text or "development" in text:
        return {"id": "real_estate_development_stack", **STACK_REGISTRY["real_estate_development_stack"]}
    if "release" in text or "campaign" in text or "media" in text:
        return {"id": "media_release_stack", **STACK_REGISTRY["media_release_stack"]}
    return {"id": "client_intake_stack", **STACK_REGISTRY["client_intake_stack"]}
