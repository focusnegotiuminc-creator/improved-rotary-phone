"""Content generation placeholder module for CREATE tasks."""

from __future__ import annotations


def generate_content_brief(topic: str) -> dict:
    return {
        "topic": topic,
        "artifact_types": ["book", "diagram", "campaign_copy"],
        "status": "planned",
    }
