from __future__ import annotations

import os
import time
from typing import Any, Callable

import requests

try:
    from FOCUS_MASTER_AI.core.runtime_config import bootstrap_runtime_env
    from FOCUS_MASTER_AI.integrations.openai_client import generate_openai
except ImportError:  # pragma: no cover
    from core.runtime_config import bootstrap_runtime_env
    from integrations.openai_client import generate_openai

ENGINE_PROVIDER_PREFERENCES: dict[str, list[str]] = {
    "research": ["ollama", "anthropic", "openai", "gemini"],
    "claims": ["ollama", "anthropic", "openai", "gemini"],
    "writing": ["ollama", "openai", "anthropic", "gemini"],
    "geometry": ["ollama", "gemini", "openai", "anthropic"],
    "construction": ["ollama", "anthropic", "openai", "gemini"],
    "compliance": ["ollama", "anthropic", "openai", "gemini"],
    "frequency": ["ollama", "openai", "anthropic", "gemini"],
    "marketing": ["ollama", "openai", "anthropic", "gemini"],
    "ai_twin": ["ollama", "openai", "gemini", "anthropic"],
    "publish": ["ollama", "openai", "anthropic", "gemini"],
    "automation": ["ollama", "openai", "anthropic", "gemini"],
}
_OLLAMA_STATUS_CACHE: dict[str, object] = {"checked_at": 0.0, "available": False, "message": "Ollama not checked yet."}

def _default_model(provider: str) -> str:
    if provider == "ollama":
        return os.getenv("DEFAULT_OLLAMA_MODEL", "").strip() or os.getenv("OLLAMA_MODEL", "").strip() or "llama3.1:8b"
    if provider == "openai":
        return os.getenv("DEFAULT_OPENAI_MODEL", "").strip() or os.getenv("OPENAI_MODEL", "").strip() or "gpt-4.1-mini"
    if provider == "anthropic":
        return os.getenv("DEFAULT_ANTHROPIC_MODEL", "").strip() or "claude-sonnet-4-20250514"
    if provider == "gemini":
        return os.getenv("DEFAULT_GEMINI_MODEL", "").strip() or os.getenv("GEMINI_MODEL", "").strip() or "gemini-2.5-flash"
    return "unknown"


def _provider_key(provider: str) -> str:
    if provider == "ollama":
        return "OLLAMA_BASE_URL"
    if provider == "openai":
        return "OPENAI_API_KEY"
    if provider == "anthropic":
        return "ANTHROPIC_API_KEY"
    if provider == "gemini":
        return "GEMINI_API_KEY" if os.getenv("GEMINI_API_KEY", "").strip() else "GOOGLE_API_KEY"
    return ""


def _ollama_base_url() -> str:
    return os.getenv("OLLAMA_BASE_URL", "").strip() or "http://127.0.0.1:11434"


def _ollama_available() -> tuple[bool, str]:
    cache_ttl = float(os.getenv("OLLAMA_STATUS_CACHE_SECONDS", "30") or "30")
    if _OLLAMA_STATUS_CACHE["checked_at"] and (time.time() - float(_OLLAMA_STATUS_CACHE["checked_at"])) < cache_ttl:
        return bool(_OLLAMA_STATUS_CACHE["available"]), str(_OLLAMA_STATUS_CACHE["message"])
    try:
        response = requests.get(f"{_ollama_base_url().rstrip('/')}/api/tags", timeout=1.2)
        response.raise_for_status()
        _OLLAMA_STATUS_CACHE.update(
            {
                "checked_at": time.time(),
                "available": True,
                "message": "Local Ollama runtime is reachable.",
            }
        )
        return True, "Local Ollama runtime is reachable."
    except Exception as exc:  # pragma: no cover
        message = f"Ollama is not reachable: {exc}"
        _OLLAMA_STATUS_CACHE.update(
            {
                "checked_at": time.time(),
                "available": False,
                "message": message,
            }
        )
        return False, message


def provider_status() -> list[dict[str, Any]]:
    bootstrap_runtime_env()
    statuses: list[dict[str, Any]] = []
    for provider in ("ollama", "openai", "anthropic", "gemini"):
        key_name = _provider_key(provider)
        if provider == "ollama":
            configured, message = _ollama_available()
        else:
            configured = bool(key_name and os.getenv(key_name, "").strip())
            message = "Configured for live generation." if configured else f"{key_name or 'API key'} is not configured."
        statuses.append(
            {
                "provider": provider,
                "configured": configured,
                "key_name": key_name,
                "default_model": _default_model(provider),
                "state": "ready" if configured else "attention",
                "message": message,
            }
        )
    return statuses


def _ollama_generate(prompt: str, *, system: str | None, model: str, temperature: float) -> dict[str, Any]:
    available, message = _ollama_available()
    if not available:
        return {
            "ok": False,
            "provider": "ollama",
            "model": model,
            "mode": "unavailable",
            "content": f"[Ollama unavailable] {message}",
            "error": message,
        }

    full_prompt = prompt if not system else f"System:\n{system}\n\nUser:\n{prompt}"
    payload: dict[str, Any] = {
        "model": model,
        "prompt": full_prompt,
        "stream": False,
        "options": {
            "temperature": temperature,
        },
    }
    try:
        response = requests.post(
            f"{_ollama_base_url().rstrip('/')}/api/generate",
            json=payload,
            timeout=180,
        )
        response.raise_for_status()
        body = response.json()
        text = str(body.get("response", "")).strip()
        return {
            "ok": True,
            "provider": "ollama",
            "model": model,
            "mode": "local",
            "content": text or "[Ollama returned an empty response]",
        }
    except Exception as exc:  # pragma: no cover
        return {
            "ok": False,
            "provider": "ollama",
            "model": model,
            "mode": "error",
            "content": f"[Ollama error] {exc}",
            "error": str(exc),
        }


def _anthropic_generate(prompt: str, *, system: str | None, model: str, temperature: float) -> dict[str, Any]:
    api_key = os.getenv("ANTHROPIC_API_KEY", "").strip()
    if not api_key:
        return {
            "ok": False,
            "provider": "anthropic",
            "model": model,
            "mode": "unavailable",
            "content": "[Anthropic unavailable] ANTHROPIC_API_KEY is not set.",
            "error": "ANTHROPIC_API_KEY is not set.",
        }

    payload: dict[str, Any] = {
        "model": model,
        "max_tokens": 1600,
        "temperature": temperature,
        "messages": [{"role": "user", "content": prompt}],
    }
    if system:
        payload["system"] = system

    try:
        response = requests.post(
            "https://api.anthropic.com/v1/messages",
            headers={
                "x-api-key": api_key,
                "anthropic-version": "2023-06-01",
                "content-type": "application/json",
            },
            json=payload,
            timeout=60,
        )
        response.raise_for_status()
        body = response.json()
        text = "".join(
            block.get("text", "")
            for block in body.get("content", [])
            if isinstance(block, dict) and block.get("type") == "text"
        ).strip()
        return {
            "ok": True,
            "provider": "anthropic",
            "model": body.get("model", model),
            "mode": "live",
            "content": text or "[Anthropic returned an empty response]",
        }
    except Exception as exc:  # pragma: no cover
        return {
            "ok": False,
            "provider": "anthropic",
            "model": model,
            "mode": "error",
            "content": f"[Anthropic error] {exc}",
            "error": str(exc),
        }


def _gemini_generate(prompt: str, *, system: str | None, model: str, temperature: float) -> dict[str, Any]:
    api_key = os.getenv("GEMINI_API_KEY", "").strip() or os.getenv("GOOGLE_API_KEY", "").strip()
    if not api_key:
        return {
            "ok": False,
            "provider": "gemini",
            "model": model,
            "mode": "unavailable",
            "content": "[Gemini unavailable] GEMINI_API_KEY or GOOGLE_API_KEY is not set.",
            "error": "GEMINI_API_KEY or GOOGLE_API_KEY is not set.",
        }

    payload: dict[str, Any] = {
        "contents": [
            {
                "role": "user",
                "parts": [{"text": prompt}],
            }
        ],
        "generationConfig": {
            "temperature": temperature,
        },
    }
    if system:
        payload["systemInstruction"] = {"parts": [{"text": system}]}

    try:
        response = requests.post(
            f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent",
            params={"key": api_key},
            headers={"content-type": "application/json"},
            json=payload,
            timeout=60,
        )
        response.raise_for_status()
        body = response.json()
        candidates = body.get("candidates", [])
        parts = []
        if candidates:
            parts = candidates[0].get("content", {}).get("parts", [])
        text = "".join(part.get("text", "") for part in parts if isinstance(part, dict)).strip()
        return {
            "ok": True,
            "provider": "gemini",
            "model": model,
            "mode": "live",
            "content": text or "[Gemini returned an empty response]",
        }
    except Exception as exc:  # pragma: no cover
        return {
            "ok": False,
            "provider": "gemini",
            "model": model,
            "mode": "error",
            "content": f"[Gemini error] {exc}",
            "error": str(exc),
        }


def _provider_generator(provider: str) -> Callable[..., dict[str, Any]]:
    if provider == "ollama":
        return lambda prompt, system=None, model=None, temperature=0.2: _ollama_generate(
            prompt,
            system=system,
            model=model or _default_model("ollama"),
            temperature=temperature,
        )
    if provider == "openai":
        return lambda prompt, system=None, model=None, temperature=0.2: generate_openai(
            prompt,
            system=system,
            model=model or _default_model("openai"),
            temperature=temperature,
        )
    if provider == "anthropic":
        return lambda prompt, system=None, model=None, temperature=0.2: _anthropic_generate(
            prompt,
            system=system,
            model=model or _default_model("anthropic"),
            temperature=temperature,
        )
    if provider == "gemini":
        return lambda prompt, system=None, model=None, temperature=0.2: _gemini_generate(
            prompt,
            system=system,
            model=model or _default_model("gemini"),
            temperature=temperature,
        )
    raise KeyError(provider)


def _provider_candidates(engine_key: str, preferred_provider: str | None = None) -> list[str]:
    configured = [item["provider"] for item in provider_status() if item["configured"]]
    sequence: list[str] = []
    if preferred_provider:
        sequence.append(preferred_provider)
    sequence.extend(ENGINE_PROVIDER_PREFERENCES.get(engine_key, ["openai", "anthropic", "gemini"]))
    deduped = [provider for provider in dict.fromkeys(sequence) if provider in {"ollama", "openai", "anthropic", "gemini"}]
    return [provider for provider in deduped if provider in configured]


def generate_text(
    prompt: str,
    *,
    engine_key: str,
    system: str | None = None,
    preferred_provider: str | None = None,
    fallback_text: str,
    temperature: float = 0.2,
) -> dict[str, Any]:
    bootstrap_runtime_env()
    attempted: list[dict[str, str]] = []
    for provider in _provider_candidates(engine_key, preferred_provider=preferred_provider):
        generator = _provider_generator(provider)
        result = generator(prompt, system=system, temperature=temperature)
        attempted.append(
            {
                "provider": provider,
                "model": str(result.get("model", _default_model(provider))),
                "mode": str(result.get("mode", "unknown")),
            }
        )
        if result.get("ok"):
            result["attempted"] = attempted
            return result

    return {
        "ok": False,
        "provider": "fallback",
        "model": "templated-fallback",
        "mode": "fallback",
        "content": fallback_text,
        "attempted": attempted,
        "error": "No live provider succeeded for this task.",
    }
