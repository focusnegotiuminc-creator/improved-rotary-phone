from __future__ import annotations

import importlib.util
import sys
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
