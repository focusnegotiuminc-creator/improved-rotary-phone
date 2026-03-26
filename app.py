from __future__ import annotations

import json
import os
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable

from dotenv import load_dotenv
from flask import Flask, jsonify, render_template, request, url_for

BASE_DIR = Path(__file__).resolve().parent
FOCUS_APP_DIR = BASE_DIR / "FOCUS_MASTER_AI"
OUTPUTS_DIR = FOCUS_APP_DIR / "outputs"

if str(FOCUS_APP_DIR) not in sys.path:
    sys.path.insert(0, str(FOCUS_APP_DIR))

from core.dispatcher import dispatch_task
from core.orchestrator import run_multi_engine_workflow
from engines import (
    automation_engine,
    claims_engine,
    compliance_engine,
    construction_engine,
    frequency_engine,
    geometry_engine,
    marketing_engine,
    publishing_engine,
    research_engine,
    writing_engine,
)
from integrations.make_webhook import trigger_make
from integrations.replit_runner import trigger_replit

load_dotenv()

app = Flask(
    __name__,
    template_folder=str(BASE_DIR / "templates"),
    static_folder=str(BASE_DIR / "static"),
)

ENGINE_CATALOG: dict[str, dict[str, str]] = {
    "research": {
        "label": "Research Engine",
        "glyph": "Orion Lens",
        "description": "Strategic discovery, source synthesis, and insight extraction.",
        "default_task": "research market shifts in sacred architecture for premium housing",
        "color": "teal",
    },
    "claims": {
        "label": "Claims Engine",
        "glyph": "Truth Prism",
        "description": "Claim extraction, verification maps, and evidence pathways.",
        "default_task": "claim check the top 5 assumptions in our launch strategy",
        "color": "amber",
    },
    "writing": {
        "label": "Writing Engine",
        "glyph": "Scribe Spiral",
        "description": "Long-form drafts, scripts, and conversion-grade messaging.",
        "default_task": "write a premium sales narrative for Akashic Geometry Homes",
        "color": "earth",
    },
    "geometry": {
        "label": "Geometry Engine",
        "glyph": "Merkaba Grid",
        "description": "Spatial logic, dimensional framing, and sacred layout prompts.",
        "default_task": "design a sacred geometry floor concept for a 3-bedroom luxury home",
        "color": "teal",
    },
    "construction": {
        "label": "Construction Engine",
        "glyph": "Temple Forge",
        "description": "Execution plans, milestone sequencing, and build dependencies.",
        "default_task": "build a 12-week construction execution timeline for phase one",
        "color": "earth",
    },
    "compliance": {
        "label": "Compliance Engine",
        "glyph": "Law Ring",
        "description": "Regulatory checks, safeguards, and policy guardrails.",
        "default_task": "review compliance risks for a multi-state modular build rollout",
        "color": "amber",
    },
    "frequency": {
        "label": "Frequency Engine",
        "glyph": "Harmonic Axis",
        "description": "Cadence architecture for focus, rhythm, and execution continuity.",
        "default_task": "create a daily frequency protocol for founder focus and delivery",
        "color": "teal",
    },
    "marketing": {
        "label": "Marketing Engine",
        "glyph": "Signal Bloom",
        "description": "Campaign strategy, channel mapping, and KPI design.",
        "default_task": "build a high-ticket omnichannel campaign with weekly metrics",
        "color": "amber",
    },
    "publish": {
        "label": "Publishing Engine",
        "glyph": "Beacon Gate",
        "description": "Release packaging, publishing checks, and distribution readiness.",
        "default_task": "publish launch assets and release notes for the focus master stack",
        "color": "earth",
    },
    "automation": {
        "label": "Automation Engine",
        "glyph": "Pulse Relay",
        "description": "Workflow triggers across Make, Replit, and external integrations.",
        "default_task": "automate outreach and trigger Make + Replit deployment hooks",
        "color": "teal",
    },
}

ENGINE_RUNNERS: dict[str, Callable[[str], dict[str, Any]]] = {
    "research": research_engine.run,
    "claims": claims_engine.run,
    "writing": writing_engine.run,
    "geometry": geometry_engine.run,
    "construction": construction_engine.run,
    "compliance": compliance_engine.run,
    "frequency": frequency_engine.run,
    "marketing": marketing_engine.run,
    "publish": publishing_engine.run,
    "automation": automation_engine.run,
}


def _json_error(message: str, status: int = 400):
    return jsonify({"ok": False, "error": message}), status


def _extract_task(default_task: str) -> str:
    payload = request.get_json(silent=True) or {}
    task = str(payload.get("task", "")).strip()
    return task or default_task


def _engine_links() -> list[dict[str, str]]:
    links: list[dict[str, str]] = []
    for engine_id, meta in ENGINE_CATALOG.items():
        links.append(
            {
                "id": engine_id,
                "label": meta["label"],
                "glyph": meta["glyph"],
                "description": meta["description"],
                "color": meta["color"],
                "url": url_for("engine_page", engine_id=engine_id),
            }
        )
    return links


def _persist_deploy_manifest(manifest: dict[str, Any]) -> str:
    OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    path = OUTPUTS_DIR / f"replit_deploy_manifest_{stamp}.json"
    path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    return str(path)


def _run_connector_action(action: str) -> tuple[dict[str, Any], int]:
    connector_script = BASE_DIR / "github_remote_connector.py"
    if not connector_script.exists():
        return {"status": "error", "message": "github_remote_connector.py is missing."}, 404

    github_user = os.getenv("GITHUB_USER", "thegreatmachevilli")
    github_token = os.getenv("GITHUB_TOKEN", "")
    base_path = os.getenv("BASE_PATH", "./github_repos")

    cmd = [
        sys.executable,
        str(connector_script),
        "--user",
        github_user,
        "--token",
        github_token,
        "--path",
        base_path,
        "--action",
        action,
    ]

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=False)
    except Exception as exc:  # pragma: no cover
        return {"status": "error", "message": str(exc)}, 500

    if result.returncode != 0:
        return {
            "status": "error",
            "message": result.stderr.strip() or "Connector action failed.",
        }, 500

    return {
        "status": "success",
        "action": action,
        "output": result.stdout.strip(),
    }, 200


@app.get("/")
def dashboard():
    return render_template(
        "index.html",
        engines=_engine_links(),
        engine_count=len(ENGINE_CATALOG),
    )


@app.get("/engine/<engine_id>")
def engine_page(engine_id: str):
    if engine_id not in ENGINE_CATALOG:
        return _json_error(f"Unknown engine '{engine_id}'.", status=404)

    return render_template(
        "engine.html",
        engine_id=engine_id,
        engine=ENGINE_CATALOG[engine_id],
        engines=_engine_links(),
    )


@app.get("/health")
def health():
    return jsonify(
        {
            "status": "ok",
            "service": "focus_master_akashic_os",
            "mode": "standard_full_mode",
            "engine_count": len(ENGINE_CATALOG),
            "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        }
    )


@app.get("/api/engines")
def list_engines():
    return jsonify({"ok": True, "engines": _engine_links()})


@app.post("/api/run")
def run_dispatch():
    payload = request.get_json(silent=True) or {}
    task = str(payload.get("task", "")).strip()
    if not task:
        return _json_error("task is required")

    result = dispatch_task(task)
    return jsonify({"ok": True, "mode": "dispatch", "task": task, "result": result})


@app.post("/api/engine/<engine_id>/run")
def run_engine(engine_id: str):
    if engine_id not in ENGINE_RUNNERS:
        return _json_error(f"Unknown engine '{engine_id}'.", status=404)

    task = _extract_task(ENGINE_CATALOG[engine_id]["default_task"])
    result = ENGINE_RUNNERS[engine_id](task)
    return jsonify({"ok": True, "engine": engine_id, "task": task, "result": result})


@app.post("/api/full-mode/run")
def run_full_mode():
    task = _extract_task("build full automation AI system and deploy architecture")
    result = run_multi_engine_workflow(task)
    return jsonify({"ok": True, "mode": "standard_full_mode", "task": task, "result": result})


@app.post("/api/launch-all")
def launch_all_engines():
    payload = request.get_json(silent=True) or {}
    seed_task = str(payload.get("seed_task", "")).strip()

    launched: list[dict[str, Any]] = []
    for engine_id, runner in ENGINE_RUNNERS.items():
        task = seed_task or ENGINE_CATALOG[engine_id]["default_task"]
        result = runner(task)
        launched.append({"engine": engine_id, "task": task, "result": result})

    return jsonify(
        {
            "ok": True,
            "mode": "launch_all_engines",
            "engine_count": len(launched),
            "results": launched,
        }
    )


@app.post("/api/replit/deploy")
def deploy_engine_apps():
    payload = request.get_json(silent=True) or {}
    requested_engines = payload.get("engines") or list(ENGINE_CATALOG.keys())

    if not isinstance(requested_engines, list):
        return _json_error("engines must be an array when provided")

    deployed_apps: list[dict[str, Any]] = []
    for engine_id in requested_engines:
        if engine_id not in ENGINE_CATALOG:
            continue

        launch_url = url_for("engine_page", engine_id=engine_id, _external=True)
        make_status = trigger_make(
            task=f"deploy_{engine_id}_engine_app",
            extra_payload={"engine": engine_id, "launch_url": launch_url},
        )
        replit_status = trigger_replit(f"Deploy {engine_id} Akashic engine app at {launch_url}")
        deployed_apps.append(
            {
                "engine": engine_id,
                "label": ENGINE_CATALOG[engine_id]["label"],
                "launch_url": launch_url,
                "make": make_status,
                "replit": replit_status,
            }
        )

    manifest = {
        "ok": True,
        "mode": "replit_engine_deploy",
        "theme": "akashic_sacred_geometry",
        "deployed_count": len(deployed_apps),
        "apps": deployed_apps,
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
    }
    manifest_path = _persist_deploy_manifest(manifest)
    manifest["manifest_file"] = manifest_path
    return jsonify(manifest)


@app.post("/sync")
def sync_repos():
    result, status = _run_connector_action("sync")
    return jsonify(result), status


@app.post("/clone")
def clone_repos():
    result, status = _run_connector_action("clone")
    return jsonify(result), status


@app.get("/report")
def get_report():
    result, status = _run_connector_action("report")
    return jsonify(result), status


if __name__ == "__main__":
    port = int(os.getenv("PORT", "5000"))
    app.run(host="0.0.0.0", port=port, debug=False)
