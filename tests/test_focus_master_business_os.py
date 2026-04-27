from __future__ import annotations

import importlib.util
import sys
import time
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from FOCUS_MASTER_AI.api_server import create_app  # noqa: E402


def _load_build_public_site():
    script_path = ROOT / "focus_ai" / "scripts" / "build_public_site.py"
    spec = importlib.util.spec_from_file_location("build_public_site", script_path)
    module = importlib.util.module_from_spec(spec)
    assert spec is not None and spec.loader is not None
    spec.loader.exec_module(module)
    return module


def test_offers_and_mobile_config_endpoints(tmp_path, monkeypatch):
    monkeypatch.setenv("FOCUS_MASTER_RUNTIME_DIR", str(tmp_path / "runtime"))
    app = create_app()
    client = app.test_client()

    offers_response = client.get("/v1/offers")
    assert offers_response.status_code == 200
    offers = offers_response.get_json()["offers"]
    assert len(offers) == 3
    assert offers[0]["checkout_url"].startswith("https://buy.stripe.com/")

    mobile_response = client.get("/v1/mobile/config")
    assert mobile_response.status_code == 200
    payload = mobile_response.get_json()
    assert payload["app"]["app_name"] == "Focus Operations"
    assert payload["portal"]["site_name"] == "The Focus Corporation | Businesses, Services, and Store"

    private_console = client.get("/private-console")
    assert private_console.status_code == 200
    assert "Focus Private Operations Console" in private_console.get_data(as_text=True)


def test_high_risk_task_creates_readiness_pack(tmp_path, monkeypatch):
    monkeypatch.setenv("FOCUS_MASTER_RUNTIME_DIR", str(tmp_path / "runtime"))
    app = create_app()
    client = app.test_client()

    response = client.post("/v1/tasks", json={"task": "Prepare payroll submission for this week's employee hours"})
    assert response.status_code == 201
    task = response.get_json()["task"]
    assert task["status"] == "readiness_prepared"
    assert task["readiness_only"] is True
    assert task["readiness_pack_id"].startswith("payroll_readiness_")

    lookup = client.get(f"/v1/tasks/{task['id']}")
    assert lookup.status_code == 200
    assert lookup.get_json()["task"]["id"] == task["id"]


def test_content_generation_uses_related_knowledge(tmp_path, monkeypatch):
    monkeypatch.setenv("FOCUS_MASTER_RUNTIME_DIR", str(tmp_path / "runtime"))
    app = create_app()
    client = app.test_client()

    response = client.post("/v1/content/generate", json={"topic": "Focus AI offer ladder and ebook bundle"})
    assert response.status_code == 201
    job = response.get_json()["job"]
    assert job["status"] == "planned"
    assert job["brief"]["topic"] == "Focus AI offer ladder and ebook bundle"
    assert isinstance(job["related_artifacts"], list)


def test_public_site_build_exports_business_os_bundle():
    module = _load_build_public_site()
    assert module.build() == 0

    public_dir = ROOT / "focus_ai" / "published" / "public_site"
    products_html = (public_dir / "products.html").read_text(encoding="utf-8")
    business_os_json = (public_dir / "data" / "business_os.json").read_text(encoding="utf-8")

    assert (public_dir / "business_os.html").exists()
    assert "Stripe-connected offers" in products_html
    assert '"site_name": "The Focus Corporation | Businesses, Services, and Store"' in business_os_json


def test_private_runtime_status_endpoint(tmp_path, monkeypatch):
    monkeypatch.setenv("FOCUS_MASTER_RUNTIME_DIR", str(tmp_path / "runtime"))
    app = create_app()
    client = app.test_client()

    response = client.get("/v1/private/runtime")
    assert response.status_code == 200
    payload = response.get_json()["runtime"]
    assert payload["service"] == "focus_master_ai_private_runtime"
    assert any(item["provider"] == "openai" for item in payload["providers"])
    assert any(engine["id"] == "marketing" for engine in payload["engines"])


def test_private_run_creation_and_lookup(tmp_path, monkeypatch):
    monkeypatch.setenv("FOCUS_MASTER_RUNTIME_DIR", str(tmp_path / "runtime"))
    app = create_app()
    client = app.test_client()

    response = client.post(
        "/v1/private/runs",
        json={
            "business": "focus-negotium",
            "workflow": "Website Design and Deployment",
            "mission": "Prepare a private execution plan for a service-page refresh and deployment sequence.",
            "deliverables": ["Updated page map", "Deployment checklist"],
            "constraints": ["Do not expose internal systems publicly."],
            "context": ["Live site", "Private repo workspace"],
            "integrations": ["github", "stripe"],
            "execute_automation": False,
        },
    )
    assert response.status_code == 201
    run = response.get_json()["run"]
    assert run["status"] == "completed"
    assert run["engine_sequence"]
    assert "Final Summary" not in run["final_summary"]  # summary body only
    assert len(run["results"]) >= 1

    detail = client.get(f"/v1/private/runs/{run['id']}")
    assert detail.status_code == 200
    detail_run = detail.get_json()["run"]
    assert detail_run["id"] == run["id"]
    assert detail_run["final_summary_meta"]["mode"] in {"fallback", "live"}
    assert len(detail_run["artifacts"]) >= 4


def test_private_runtime_catalog_endpoints(tmp_path, monkeypatch):
    monkeypatch.setenv("FOCUS_MASTER_RUNTIME_DIR", str(tmp_path / "runtime"))
    app = create_app()
    client = app.test_client()

    stacks = client.get("/v1/private/stacks")
    assert stacks.status_code == 200
    stack_payload = stacks.get_json()["stacks"]
    assert any(item["id"] == "sacred_geometry_book_stack" for item in stack_payload)

    tools = client.get("/v1/private/tools")
    assert tools.status_code == 200
    tool_payload = tools.get_json()["tools"]
    assert any(item["id"] == "knowledge_base" for item in tool_payload)


def test_private_background_job_and_artifacts(tmp_path, monkeypatch):
    monkeypatch.setenv("FOCUS_MASTER_RUNTIME_DIR", str(tmp_path / "runtime"))
    app = create_app()
    client = app.test_client()

    response = client.post(
        "/v1/private/jobs",
        json={
            "business": "focus-records",
            "workflow": "Release Campaign and Media Packaging",
            "mission": "Queue a media release brief with rollout notes and asset handoff guidance.",
            "deliverables": ["campaign summary", "asset list"],
            "integrations": ["github", "media"],
            "execute_automation": False,
        },
    )
    assert response.status_code == 202
    run = response.get_json()["run"]

    deadline = time.time() + 10
    final_run = None
    while time.time() < deadline:
        detail = client.get(f"/v1/private/runs/{run['id']}")
        assert detail.status_code == 200
        final_run = detail.get_json()["run"]
        if final_run["status"] == "completed":
            break
        time.sleep(0.25)

    assert final_run is not None
    assert final_run["status"] == "completed"
    artifacts = client.get(f"/v1/private/runs/{run['id']}/artifacts")
    assert artifacts.status_code == 200
    artifact_payload = artifacts.get_json()["artifacts"]
    assert any(item["name"] == "final_summary" for item in artifact_payload)
