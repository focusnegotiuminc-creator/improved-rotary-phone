"""Public, hosted status endpoint for ALL FOCUS_MASTER_AI connectors.

This is a self-contained Vercel Python serverless function (no Flask import)
so it stays fast and reliable in the serverless runtime. It reports the
configuration + optional live status of every connector defined in
FOCUS_MASTER_AI/config/integrations.json.

Routes (via vercel.json):
  GET /api/connectors        -> JSON status for all connectors
  GET /connectors            -> same (pretty alias)

Query params:
  ?ping=1                    -> attempt lightweight live checks (GitHub, webhooks)
"""

from __future__ import annotations

import json
import os
import urllib.error
import urllib.request
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler
from pathlib import Path
from urllib.parse import urlparse, parse_qs

# Canonical registry path (bundled via vercel.json includeFiles).
_CONFIG_PATH = (
    Path(__file__).resolve().parents[1]
    / "FOCUS_MASTER_AI"
    / "config"
    / "integrations.json"
)

# Fallback registry if the config file is not bundled for any reason.
_FALLBACK_REGISTRY: dict[str, dict[str, str]] = {
    "openai": {"label": "OpenAI Reasoning Core", "env": "OPENAI_API_KEY", "kind": "api_key"},
    "github": {"label": "GitHub Publish Surface", "env": "GITHUB_TOKEN", "kind": "token"},
    "mailchimp": {"label": "Mailchimp Audience", "env": "MAILCHIMP_API_KEY", "kind": "api_key"},
    "make": {"label": "Make Automation Webhook", "env": "MAKE_WEBHOOK_URL", "kind": "webhook"},
    "replit": {"label": "Replit Remote Runner", "env": "REPLIT_ENDPOINT", "kind": "endpoint"},
}

# Friendly labels + the env-var key for each integration discovered in config.
_ENV_KEY_FIELDS = ("api_key_env", "token_env", "webhook_env", "endpoint_env")
_LABELS = {
    "openai": "OpenAI Reasoning Core",
    "github": "GitHub Publish Surface",
    "mailchimp": "Mailchimp Audience",
    "make": "Make Automation Webhook",
    "replit": "Replit Remote Runner",
}
_KIND_BY_FIELD = {
    "api_key_env": "api_key",
    "token_env": "token",
    "webhook_env": "webhook",
    "endpoint_env": "endpoint",
}


def _load_registry() -> dict[str, dict[str, str]]:
    """Build a {id: {label, env, kind}} map from integrations.json, with fallback."""
    try:
        raw = json.loads(_CONFIG_PATH.read_text(encoding="utf-8"))
        integrations = raw.get("integrations", {})
        registry: dict[str, dict[str, str]] = {}
        for conn_id, spec in integrations.items():
            env_key = ""
            kind = "secret"
            for field in _ENV_KEY_FIELDS:
                if field in spec:
                    env_key = spec[field]
                    kind = _KIND_BY_FIELD.get(field, "secret")
                    break
            registry[conn_id] = {
                "label": _LABELS.get(conn_id, conn_id.replace("_", " ").title()),
                "env": env_key,
                "kind": kind,
            }
        return registry or _FALLBACK_REGISTRY
    except Exception:
        return _FALLBACK_REGISTRY


def _ping_github(token: str) -> dict[str, object]:
    req = urllib.request.Request(
        "https://api.github.com/user",
        headers={
            "Authorization": f"Bearer {token}",
            "User-Agent": "focus-connector-status",
            "Accept": "application/vnd.github+json",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=4) as resp:
            return {"live": resp.status == 200, "http_status": resp.status}
    except urllib.error.HTTPError as exc:
        return {"live": False, "http_status": exc.code}
    except Exception as exc:  # network/timeout
        return {"live": False, "error": type(exc).__name__}


def _ping_url(url: str) -> dict[str, object]:
    """Lightweight reachability check for webhook/endpoint URLs."""
    try:
        parsed = urlparse(url)
        if parsed.scheme not in ("http", "https") or not parsed.netloc:
            return {"live": False, "error": "invalid_url"}
        req = urllib.request.Request(url, method="GET", headers={"User-Agent": "focus-connector-status"})
        with urllib.request.urlopen(req, timeout=4) as resp:
            return {"live": 200 <= resp.status < 500, "http_status": resp.status}
    except urllib.error.HTTPError as exc:
        # A 4xx still means the host is reachable.
        return {"live": True, "http_status": exc.code}
    except Exception as exc:
        return {"live": False, "error": type(exc).__name__}


def build_payload(do_ping: bool) -> dict[str, object]:
    registry = _load_registry()
    connectors: list[dict[str, object]] = []

    for conn_id, spec in registry.items():
        env_key = spec.get("env", "")
        value = os.getenv(env_key, "").strip() if env_key else ""
        configured = bool(value)
        item: dict[str, object] = {
            "id": conn_id,
            "label": spec.get("label", conn_id),
            "kind": spec.get("kind", "secret"),
            "env_var": env_key,
            "configured": configured,
            "state": "ready" if configured else "attention",
            "message": (
                f"{spec.get('label', conn_id)} is configured."
                if configured
                else f"Set {env_key or 'the required env var'} to enable this connector."
            ),
        }

        if do_ping and configured:
            if conn_id == "github":
                item["live_check"] = _ping_github(value)
            elif spec.get("kind") in ("webhook", "endpoint"):
                item["live_check"] = _ping_url(value)

        connectors.append(item)

    ready = sum(1 for c in connectors if c["configured"])
    return {
        "ok": True,
        "service": "focus_master_connectors",
        "endpoint": "/api/connectors",
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "summary": {
            "total": len(connectors),
            "ready": ready,
            "attention": len(connectors) - ready,
        },
        "connectors": connectors,
    }


class handler(BaseHTTPRequestHandler):
    def do_GET(self):  # noqa: N802 (Vercel/BaseHTTPRequestHandler contract)
        query = parse_qs(urlparse(self.path).query)
        do_ping = query.get("ping", ["0"])[0] in ("1", "true", "yes")
        payload = build_payload(do_ping)

        body = json.dumps(payload, indent=2).encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Cache-Control", "no-store")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(body)
