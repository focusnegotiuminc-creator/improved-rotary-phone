from __future__ import annotations

import os
import time
from typing import Any, Optional

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
_LAST_OPENAI_FAILURE_TS = 0.0


def get_openai_runtime_status() -> dict[str, str]:
    return dict(_LAST_OPENAI_STATUS)


def generate_openai(
    prompt: str,
    *,
    system: Optional[str] = None,
    model: Optional[str] = None,
    temperature: float = 0.2,
) -> dict[str, Any]:
    global _LAST_OPENAI_FAILURE_TS
    bootstrap_runtime_env()
    api_key = os.getenv("OPENAI_API_KEY", "").strip()
    selected_model = model or os.getenv("DEFAULT_OPENAI_MODEL") or os.getenv("OPENAI_MODEL", "gpt-4.1-mini")
    cooldown_seconds = float(os.getenv("OPENAI_FAILURE_COOLDOWN_SECONDS", "30") or "30")

    if not api_key:
        _LAST_OPENAI_STATUS.update(
            {
                "state": "attention",
                "message": "OPENAI_API_KEY is not configured.",
            }
        )
        return {
            "ok": False,
            "provider": "openai",
            "model": selected_model,
            "mode": "unavailable",
            "content": "[OpenAI unavailable] OPENAI_API_KEY is not set.",
            "error": "OPENAI_API_KEY is not set.",
        }
    if OpenAI is None:
        _LAST_OPENAI_STATUS.update(
            {
                "state": "attention",
                "message": "The openai package is not installed.",
            }
        )
        return {
            "ok": False,
            "provider": "openai",
            "model": selected_model,
            "mode": "unavailable",
            "content": "[OpenAI unavailable] openai package is not installed.",
            "error": "openai package is not installed.",
        }

    if _LAST_OPENAI_FAILURE_TS and (time.time() - _LAST_OPENAI_FAILURE_TS) < cooldown_seconds:
        remaining = max(0.0, cooldown_seconds - (time.time() - _LAST_OPENAI_FAILURE_TS))
        _LAST_OPENAI_STATUS.update(
            {
                "state": "attention",
                "message": f"OpenAI retry cooldown active after the last failure ({remaining:.1f}s remaining).",
            }
        )
        return {
            "ok": False,
            "provider": "openai",
            "model": selected_model,
            "mode": "cooldown",
            "content": "[OpenAI cooldown] Skipping repeated live call after a recent failure.",
            "error": "OpenAI retry cooldown active.",
        }

    try:
        client = OpenAI(api_key=api_key)
        messages: list[dict[str, str]] = []
        if system:
            messages.append({"role": "system", "content": system})
        messages.append({"role": "user", "content": prompt})

        response = client.chat.completions.create(
            model=selected_model,
            messages=messages,
            temperature=temperature,
        )
        content = response.choices[0].message.content
        _LAST_OPENAI_STATUS.update(
            {
                "state": "ready",
                "message": f"Live generation is working on model {selected_model}.",
            }
        )
        return {
            "ok": True,
            "provider": "openai",
            "model": selected_model,
            "mode": "live",
            "content": content.strip() if content else "[OpenAI returned an empty response]",
        }
    except Exception as exc:  # pragma: no cover
        _LAST_OPENAI_FAILURE_TS = time.time()
        _LAST_OPENAI_STATUS.update(
            {
                "state": "attention",
                "message": f"OpenAI call failed: {exc}",
            }
        )
        return {
            "ok": False,
            "provider": "openai",
            "model": selected_model,
            "mode": "error",
            "content": f"[OpenAI error] {exc}",
            "error": str(exc),
        }


def call_gpt(prompt: str, model: Optional[str] = None) -> str:
    result = generate_openai(prompt, model=model)
    return str(result["content"])

