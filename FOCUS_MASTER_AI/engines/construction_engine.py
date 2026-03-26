from __future__ import annotations

from integrations.openai_client import call_gpt


def run(task: str) -> dict:
    prompt = (
        "Turn this request into a construction/build execution plan with milestones, "
        "risks, and dependencies.\n\n"
        f"Task: {task}"
    )
    output = call_gpt(prompt)
    return {
        "engine": "construction",
        "status": "completed",
        "output": output,
    }

