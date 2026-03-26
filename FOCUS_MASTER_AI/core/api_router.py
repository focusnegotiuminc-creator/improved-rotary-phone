"""API routing helpers.

This module generates templates only and never embeds credentials.
"""

from __future__ import annotations


def build_api_template(service: str, endpoint: str) -> dict:
    return {
        "service": service,
        "endpoint": endpoint,
        "method": "POST",
        "headers": {
            "Authorization": "Bearer ${SERVICE_API_KEY}",
            "Content-Type": "application/json",
        },
        "body": {"task": "${TASK}", "metadata": {"source": "FOCUS_MASTER_AI"}},
    }
