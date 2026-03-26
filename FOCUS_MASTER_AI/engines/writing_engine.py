from __future__ import annotations

from integrations.openai_client import call_gpt


def run(task: str) -> dict:
    prompt = (
        "Write a clear draft response for this task. "
        "Use a practical tone and include a short action checklist.\n\n"
        f"Task: {task}"
    )
    output = call_gpt(prompt)
    return {
        "engine": "writing",
        "status": "completed",
        "output": output,
    }

