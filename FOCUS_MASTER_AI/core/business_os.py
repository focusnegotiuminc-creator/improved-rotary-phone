from __future__ import annotations

import json
import os
import re
import uuid
from datetime import datetime, timezone
from pathlib import Path
from threading import RLock
from typing import Any

try:
    from FOCUS_MASTER_AI.core.content_engine import generate_content_brief
    from FOCUS_MASTER_AI.core.dispatcher import dispatch_task
    from FOCUS_MASTER_AI.core.knowledge_registry import build_knowledge_snapshot, find_related_artifacts
    from FOCUS_MASTER_AI.core.task_classifier import classify_task
except ImportError:
    from core.content_engine import generate_content_brief
    from core.dispatcher import dispatch_task
    from core.knowledge_registry import build_knowledge_snapshot, find_related_artifacts
    from core.task_classifier import classify_task

HIGH_RISK_TERMS = {
    "legal": ("legal", "entity", "trust", "compliance filing", "c corp", "llc"),
    "payroll": ("payroll", "timesheet", "employee hours", "wages", "salary"),
    "banking": ("bank", "banking", "wire", "move funds", "account opening", "treasury"),
}
MEDIUM_RISK_TERMS = (
    "deploy",
    "publish",
    "stripe",
    "campaign",
    "lead follow-up",
    "github",
    "slack",
    "linear",
    "schedule",
)


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


class JsonStore:
    def __init__(self, path: Path, default: Any) -> None:
        self.path = path
        self.default = default
        self.path.parent.mkdir(parents=True, exist_ok=True)
        if not self.path.exists():
            self.write(self.default)

    def read(self) -> Any:
        try:
            return json.loads(self.path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            return self.default

    def write(self, value: Any) -> None:
        self.path.write_text(json.dumps(value, indent=2), encoding="utf-8")

    def append(self, item: dict[str, Any]) -> dict[str, Any]:
        data = self.read()
        if not isinstance(data, list):
            data = []
        data.append(item)
        self.write(data)
        return item


class BusinessOperatingSystem:
    def __init__(self, repo_root: Path | None = None, runtime_dir: Path | None = None) -> None:
        self.repo_root = repo_root or Path(__file__).resolve().parents[2]
        configured_runtime = os.getenv("FOCUS_MASTER_RUNTIME_DIR", "").strip()
        self.runtime_dir = runtime_dir or (
            Path(configured_runtime)
            if configured_runtime
            else self.repo_root / "FOCUS_MASTER_AI" / "data" / "business_os_runtime"
        )
        self.catalog_path = self.repo_root / "focus_ai" / "config" / "business_os.json"
        self.integrations_path = self.repo_root / "FOCUS_MASTER_AI" / "config" / "integrations.json"
        self.tasks = JsonStore(self.runtime_dir / "tasks.json", [])
        self.leads = JsonStore(self.runtime_dir / "leads.json", [])
        self.readiness_packs = JsonStore(self.runtime_dir / "readiness_packs.json", [])
        self.content_jobs = JsonStore(self.runtime_dir / "content_jobs.json", [])
        self.knowledge_cache_path = self.runtime_dir / "knowledge_snapshot.json"
        self._mutation_lock = RLock()

    def _load_catalog(self) -> dict[str, Any]:
        if not self.catalog_path.exists():
            raise FileNotFoundError(f"Missing catalog: {self.catalog_path}")

        data = json.loads(self.catalog_path.read_text(encoding="utf-8"))
        data["offers"] = [self._resolve_offer(offer) for offer in data.get("offers", [])]
        data["connectors"] = self._resolve_connectors(data.get("connectors", []))
        return data

    @property
    def catalog(self) -> dict[str, Any]:
        return self._load_catalog()

    def _resolve_offer(self, offer: dict[str, Any]) -> dict[str, Any]:
        resolved = dict(offer)
        env_name = resolved.get("checkout_url_env", "")
        resolved["checkout_url"] = os.getenv(env_name, "").strip() or resolved.get("default_checkout_url", "")
        return resolved

    def _resolve_connectors(self, connectors: list[dict[str, Any]]) -> list[dict[str, Any]]:
        integration_envs: dict[str, list[str]] = {}
        if self.integrations_path.exists():
            try:
                raw = json.loads(self.integrations_path.read_text(encoding="utf-8"))
                for name, cfg in raw.get("integrations", {}).items():
                    integration_envs[name] = [value for key, value in cfg.items() if key.endswith("_env")]
            except (OSError, json.JSONDecodeError):
                integration_envs = {}

        resolved: list[dict[str, Any]] = []
        for connector in connectors:
            item = dict(connector)
            env_keys = list(dict.fromkeys(item.get("env_keys", []) + integration_envs.get(item["id"], [])))
            configured_keys = [key for key in env_keys if os.getenv(key, "").strip()]
            mode = item.get("mode", "api")
            if configured_keys:
                status = "configured"
            elif mode == "connected_app":
                status = "ready-via-connected-app"
            elif mode == "browser_login":
                status = "ready-via-browser-session"
            else:
                status = "manual-auth-required"

            item["env_keys"] = env_keys
            item["configured_keys"] = configured_keys
            item["status"] = status
            resolved.append(item)
        return resolved

    def _workflow_by_id(self, workflow_id: str) -> dict[str, Any] | None:
        for workflow in self.catalog.get("workflow_catalog", []):
            if workflow["id"] == workflow_id:
                return workflow
        return None

    def _classify_risk(self, task: str, workflow: dict[str, Any] | None = None) -> str:
        combined = " ".join(
            filter(
                None,
                [
                    task.lower(),
                    (workflow or {}).get("title", "").lower(),
                    (workflow or {}).get("description", "").lower(),
                    (workflow or {}).get("workflow_class", "").lower(),
                ],
            )
        )

        if workflow and workflow.get("risk") in {"low", "medium", "high"}:
            return str(workflow["risk"])

        for terms in HIGH_RISK_TERMS.values():
            if any(term in combined for term in terms):
                return "high"
        if any(term in combined for term in MEDIUM_RISK_TERMS):
            return "medium"
        return "low"

    def _classify_route(self, task: str, workflow: dict[str, Any] | None = None) -> str:
        if workflow and workflow.get("workflow_class"):
            return str(workflow["workflow_class"])
        return classify_task(task)

    def list_offers(self) -> list[dict[str, Any]]:
        return self.catalog.get("offers", [])

    def list_connectors(self) -> list[dict[str, Any]]:
        return self.catalog.get("connectors", [])

    def list_workflows(self) -> list[dict[str, Any]]:
        return self.catalog.get("workflow_catalog", [])

    def build_status(self) -> dict[str, Any]:
        return {
            "service": "focus_master_ai_business_os",
            "status": "ok",
            "generated_at": _utc_now(),
            "counts": {
                "offers": len(self.list_offers()),
                "workflows": len(self.list_workflows()),
                "tasks": len(self.tasks.read()),
                "leads": len(self.leads.read()),
                "readiness_packs": len(self.readiness_packs.read()),
            },
        }

    def _make_id(self, prefix: str) -> str:
        timestamp = datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S")
        return f"{prefix}_{timestamp}_{uuid.uuid4().hex[:8]}"

    def get_task(self, task_id: str) -> dict[str, Any] | None:
        for task in self.tasks.read():
            if task.get("id") == task_id:
                return task
        return None

    def update_task(
        self,
        task_id: str,
        *,
        status: str | None = None,
        notes: str | None = None,
        result_path: str | None = None,
        result_summary: str | None = None,
    ) -> dict[str, Any] | None:
        with self._mutation_lock:
            tasks = self.tasks.read()
            for task in tasks:
                if task.get("id") != task_id:
                    continue
                if status:
                    task["status"] = status
                    task["updated_at"] = _utc_now()
                    if status == "completed":
                        task["completed_at"] = _utc_now()
                if notes is not None:
                    task["notes"] = notes
                if result_path:
                    task["result_path"] = result_path
                if result_summary:
                    task["result_summary"] = result_summary
                self.tasks.write(tasks)
                return task
        return None

    def _checklist_for_kind(self, kind: str) -> dict[str, list[str]]:
        templates = {
            "legal": {
                "checklist": [
                    "Identify the entity, trust, or filing objective.",
                    "Collect the governing documents and current state summary.",
                    "Capture deadlines, jurisdictions, and approval owners.",
                    "Prepare questions for licensed legal review before execution."
                ],
                "next_actions": [
                    "Review the draft packet with counsel or an authorized operator.",
                    "Confirm the filing path, fee expectations, and signatory authority.",
                    "Approve or revise the execution plan."
                ],
            },
            "payroll": {
                "checklist": [
                    "Collect approved employee hours and pay-period dates.",
                    "Confirm wage rates, reimbursements, and exception notes.",
                    "Verify worker classifications and required approvals.",
                    "Prepare the payroll packet without submitting the run."
                ],
                "next_actions": [
                    "Review hours with the payroll approver.",
                    "Resolve exceptions before submission.",
                    "Submit only through the authorized payroll platform."
                ],
            },
            "banking": {
                "checklist": [
                    "Define the banking action and affected accounts.",
                    "Collect account-holder documents and required approvals.",
                    "Prepare the transfer, opening, or treasury review packet.",
                    "Stop before any money movement or account execution."
                ],
                "next_actions": [
                    "Review the packet with the authorized signer.",
                    "Verify institution-specific requirements.",
                    "Execute only inside the approved banking platform."
                ],
            },
        }
        return templates.get(
            kind,
            {
                "checklist": [
                    "Normalize the request.",
                    "Collect supporting documents.",
                    "Confirm decision owner and approval path."
                ],
                "next_actions": [
                    "Review the readiness pack.",
                    "Approve the next operator action."
                ],
            },
        )

    def _infer_readiness_kind(self, task: str, workflow: dict[str, Any] | None = None) -> str:
        text = " ".join(
            filter(
                None,
                [
                    task.lower(),
                    (workflow or {}).get("title", "").lower(),
                    (workflow or {}).get("description", "").lower(),
                ],
            )
        )
        for kind, terms in HIGH_RISK_TERMS.items():
            if any(term in text for term in terms):
                return kind
        return "general"

    def _build_readiness_pack(
        self,
        kind: str,
        request: str,
        context: dict[str, Any] | None = None,
        owner_task_id: str | None = None,
    ) -> dict[str, Any]:
        checklist = self._checklist_for_kind(kind)
        return {
            "id": self._make_id(f"{kind}_readiness"),
            "kind": kind,
            "request": request,
            "context": context or {},
            "owner_task_id": owner_task_id,
            "created_at": _utc_now(),
            "status": "prepared",
            "execution_policy": "readiness_only",
            "checklist": checklist["checklist"],
            "next_actions": checklist["next_actions"],
        }

    def create_task(self, payload: dict[str, Any]) -> dict[str, Any]:
        workflow = self._workflow_by_id(str(payload.get("workflow_id", "")).strip())
        task_text = str(payload.get("task", "")).strip() or (workflow or {}).get("title", "")
        if not task_text:
            raise ValueError("task or workflow_id is required")

        execution_mode = str(payload.get("execution_mode", "dry_run")).strip().lower() or "dry_run"
        risk = self._classify_risk(task_text, workflow)
        route = self._classify_route(task_text, workflow)
        task_record: dict[str, Any] = {
            "id": self._make_id("task"),
            "task": task_text,
            "company_id": str(payload.get("company_id", "")).strip() or None,
            "workflow_id": (workflow or {}).get("id"),
            "route": route,
            "risk": risk,
            "execution_mode": execution_mode,
            "created_at": _utc_now(),
            "status": "planned",
            "notes": payload.get("notes", ""),
        }

        with self._mutation_lock:
            if risk == "high":
                kind = self._infer_readiness_kind(task_text, workflow)
                readiness_pack = self._build_readiness_pack(
                    kind,
                    task_text,
                    payload,
                    owner_task_id=task_record["id"],
                )
                self.readiness_packs.append(readiness_pack)
                task_record["status"] = "readiness_prepared"
                task_record["readiness_pack_id"] = readiness_pack["id"]
                task_record["readiness_only"] = True
                task_record["execution_preview"] = {
                    "summary": "High-risk actions stop at readiness pack generation.",
                    "kind": kind,
                }
            elif payload.get("execute") and risk == "low":
                task_record["status"] = "completed"
                task_record["execution_preview"] = dispatch_task(task_text)
            elif risk == "medium":
                task_record["status"] = "live_ready" if execution_mode == "live_ready" else "queued"
                task_record["execution_preview"] = {
                    "summary": "Medium-risk workflows are staged for operator release.",
                    "workflow": (workflow or {}).get("title", route),
                    "mode": execution_mode,
                }
            else:
                task_record["status"] = "queued"
                task_record["execution_preview"] = {
                    "summary": "Low-risk workflow registered and ready for execution.",
                    "workflow": (workflow or {}).get("title", route),
                }

            self.tasks.append(task_record)
        return task_record

    def run_workflow(self, workflow_id: str, payload: dict[str, Any]) -> dict[str, Any]:
        workflow = self._workflow_by_id(workflow_id)
        if workflow is None:
            raise KeyError(f"Unknown workflow: {workflow_id}")
        task_payload = dict(payload)
        task_payload["workflow_id"] = workflow_id
        task_payload.setdefault("task", workflow["title"])
        return self.create_task(task_payload)

    def register_lead(self, payload: dict[str, Any]) -> dict[str, Any]:
        email = str(payload.get("email", "")).strip()
        if not email:
            raise ValueError("email is required")

        lead = {
            "id": self._make_id("lead"),
            "created_at": _utc_now(),
            "name": str(payload.get("name", "")).strip(),
            "email": email,
            "company_interest": str(payload.get("company_interest", "")).strip(),
            "offer_interest": str(payload.get("offer_interest", "")).strip(),
            "source": str(payload.get("source", "portal")).strip() or "portal",
            "notes": str(payload.get("notes", "")).strip(),
        }
        with self._mutation_lock:
            self.leads.append(lead)
        return lead

    def get_knowledge_snapshot(self, limit: int | None = 80) -> dict[str, Any]:
        snapshot = build_knowledge_snapshot(self.repo_root, limit=limit)
        self.knowledge_cache_path.write_text(json.dumps(snapshot, indent=2), encoding="utf-8")
        return snapshot

    def create_content_job(self, payload: dict[str, Any]) -> dict[str, Any]:
        topic = str(payload.get("topic", "")).strip()
        if not topic:
            raise ValueError("topic is required")

        knowledge = self.get_knowledge_snapshot(limit=120)
        related = find_related_artifacts(knowledge, topic, limit=5)
        brief = generate_content_brief(topic)
        job = {
            "id": self._make_id("content"),
            "created_at": _utc_now(),
            "company_id": str(payload.get("company_id", "")).strip() or None,
            "topic": topic,
            "brief": brief,
            "related_artifacts": related,
            "status": "planned",
        }
        with self._mutation_lock:
            self.content_jobs.append(job)
        return job

    def create_readiness_pack(self, kind: str, payload: dict[str, Any]) -> dict[str, Any]:
        request = str(payload.get("request", "")).strip()
        if not request:
            raise ValueError("request is required")
        pack = self._build_readiness_pack(kind, request, payload)
        with self._mutation_lock:
            self.readiness_packs.append(pack)
        return pack

    def mobile_config(self) -> dict[str, Any]:
        catalog = self.catalog
        return {
            "generated_at": _utc_now(),
            "app": catalog.get("mobile", {}),
            "portal": catalog.get("portal", {}),
            "companies": catalog.get("companies", []),
            "offers": catalog.get("offers", []),
            "workflow_stages": catalog.get("workflow_stages", []),
            "design_system": catalog.get("design_system", {}),
        }

    def daily_command_mode(self) -> dict[str, Any]:
        catalog = self.catalog
        return {
            "generated_at": _utc_now(),
            "headline": "Focus AI daily command mode",
            "tracks": catalog.get("portal", {}).get("tracks", []),
            "offers": [
                {
                    "title": offer["title"],
                    "price_usd": offer["price_usd"],
                    "checkout_url": offer["checkout_url"],
                }
                for offer in catalog.get("offers", [])
            ],
            "connector_status": [
                {"id": connector["id"], "status": connector["status"]}
                for connector in catalog.get("connectors", [])
            ],
            "ops_counts": self.build_status()["counts"],
        }
