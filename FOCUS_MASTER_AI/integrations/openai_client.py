from __future__ import annotations

import os
from typing import Optional

try:
    from openai import OpenAI
except ImportError:  # pragma: no cover
    OpenAI = None

try:
    from FOCUS_MASTER_AI.core.runtime_config import bootstrap_runtime_env
except ImportError:  # pragma: no cover
    from core.runtime_config import bootstrap_runtime_env

_LAST_OPENAI_STATUS = {
    "state": "unknown",
    "message": "OpenAI has not been exercised in this runtime yet.",
}


def get_openai_runtime_status() -> dict[str, str]:
    return dict(_LAST_OPENAI_STATUS)


def call_gpt(prompt: str, model: Optional[str] = None) -> str:
    bootstrap_runtime_env()
    api_key = os.getenv("OPENAI_API_KEY", "").strip()
    selected_model = model or os.getenv("DEFAULT_OPENAI_MODEL") or os.getenv("OPENAI_MODEL", "gpt-4.1-mini")

    if not api_key:
        _LAST_OPENAI_STATUS.update(
            {
                "state": "attention",
                "message": "OPENAI_API_KEY is not configured.",
            }
        )
        return "[OpenAI unavailable] OPENAI_API_KEY is not set."
    if OpenAI is None:
        _LAST_OPENAI_STATUS.update(
            {
                "state": "attention",
                "message": "The openai package is not installed.",
            }
        )
        return "[OpenAI unavailable] openai package is not installed."

    try:
        client = OpenAI(api_key=api_key)
        response = client.chat.completions.create(
            model=selected_model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2,
        )
        content = response.choices[0].message.content
        _LAST_OPENAI_STATUS.update(
            {
                "state": "ready",
                "message": f"Live generation is working on model {selected_model}.",
            }
        )
        return content.strip() if content else "[OpenAI returned an empty response]"
    except Exception as exc:  # pragma: no cover
        _LAST_OPENAI_STATUS.update(
            {
                "state": "attention",
                "message": f"OpenAI call failed: {exc}",
            }
        )
        return f"[OpenAI error] {exc}"

