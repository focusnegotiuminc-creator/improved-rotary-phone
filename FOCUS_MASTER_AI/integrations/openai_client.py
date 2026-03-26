from __future__ import annotations

import os
from typing import Optional

try:
    from openai import OpenAI
except ImportError:  # pragma: no cover
    OpenAI = None


def call_gpt(prompt: str, model: Optional[str] = None) -> str:
    api_key = os.getenv("OPENAI_API_KEY", "").strip()
    selected_model = model or os.getenv("DEFAULT_OPENAI_MODEL", "gpt-4.1-mini")

    if not api_key:
        return "[OpenAI unavailable] OPENAI_API_KEY is not set."
    if OpenAI is None:
        return "[OpenAI unavailable] openai package is not installed."

    try:
        client = OpenAI(api_key=api_key)
        response = client.chat.completions.create(
            model=selected_model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2,
        )
        content = response.choices[0].message.content
        return content.strip() if content else "[OpenAI returned an empty response]"
    except Exception as exc:  # pragma: no cover
        return f"[OpenAI error] {exc}"

