from __future__ import annotations

from integrations.openai_client import call_gpt


def run(task: str) -> dict:
    prompt = (
        "Provide geometry/design guidance for this request. "
        "Include layout logic, dimensions assumptions, and constraints.\n\n"
        f"Task: {task}"
    )
    output = call_gpt(prompt)
    return {
        "engine": "geometry",
        "status": "completed",
        "output": output,
    }

