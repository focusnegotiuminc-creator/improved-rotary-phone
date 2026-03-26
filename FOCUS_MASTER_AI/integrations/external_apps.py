from __future__ import annotations


def route_ai(task: str) -> str:
    text = task.lower()

    if "adobe" in text:
        return "Trigger Adobe API"
    if "clay" in text:
        return "Trigger Clay API"
    if "linear" in text:
        return "Create Linear ticket"
    if "mailchimp" in text:
        return "Send Mailchimp campaign"
    if "make" in text or "automation" in text or "webhook" in text:
        return "Trigger Make automation flow"

    return "No external AI app matched"

