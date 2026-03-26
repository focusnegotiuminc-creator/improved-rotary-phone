from __future__ import annotations


def _has_any(text: str, keywords: tuple[str, ...]) -> bool:
    return any(keyword in text for keyword in keywords)


def classify_task(task: str) -> str:
    text = task.lower().strip()

    if not text:
        return "unknown"

    if _has_any(
        text,
        (
            "build",
            "create architecture",
            "full system",
            "orchestrate",
            "multi-agent",
            "deploy architecture",
        ),
    ):
        return "multi"

    if _has_any(text, ("research", "analyze", "study")):
        return "research"
    if _has_any(text, ("claim", "fact-check", "evidence")):
        return "claims"
    if _has_any(text, ("write", "book", "script", "copy", "content")):
        return "writing"
    if _has_any(text, ("geometry", "design", "layout")):
        return "geometry"
    if _has_any(text, ("build", "construction", "blueprint")):
        return "construction"
    if _has_any(text, ("legal", "compliance", "code compliance", "regulation")):
        return "compliance"
    if _has_any(text, ("chakra", "frequency", "energy")):
        return "frequency"
    if _has_any(text, ("marketing", "sales", "campaign", "funnel")):
        return "marketing"
    if _has_any(text, ("publish", "release", "post", "launch")):
        return "publish"
    if _has_any(
        text,
        (
            "automate",
            "automation",
            "make",
            "mailchimp",
            "adobe",
            "clay",
            "linear",
            "webhook",
        ),
    ):
        return "automation"
    if _has_any(text, ("gpt", "chatgpt", "openai")):
        return "gpt"

    return "general"

