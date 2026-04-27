from __future__ import annotations

from dataclasses import dataclass
from typing import Any

try:
    from FOCUS_MASTER_AI.core.agent_catalog import list_agents
    from FOCUS_MASTER_AI.core.artifact_store import ArtifactStore
    from FOCUS_MASTER_AI.core.business_os import BusinessOperatingSystem
    from FOCUS_MASTER_AI.core.connector_status import build_connector_status
    from FOCUS_MASTER_AI.core.engine_runtime import run_ai_engine
    from FOCUS_MASTER_AI.core.job_runner import EXECUTOR
    from FOCUS_MASTER_AI.core.prompt_studio import ENGINE_PROFILES, build_engine_prompt, build_master_task_packet
    from FOCUS_MASTER_AI.core.run_store import RunStore
    from FOCUS_MASTER_AI.core.stack_registry import list_stacks, resolve_stack
    from FOCUS_MASTER_AI.core.tool_router import build_tool_plan, execute_tool_plan, list_tools
    from FOCUS_MASTER_AI.integrations.model_mesh import generate_text, provider_status
except ImportError:  # pragma: no cover
    from core.agent_catalog import list_agents
    from core.artifact_store import ArtifactStore
    from core.business_os import BusinessOperatingSystem
    from core.connector_status import build_connector_status
    from core.engine_runtime import run_ai_engine
    from core.job_runner import EXECUTOR
    from core.prompt_studio import ENGINE_PROFILES, build_engine_prompt, build_master_task_packet
    from core.run_store import RunStore
    from core.stack_registry import list_stacks, resolve_stack
    from core.tool_router import build_tool_plan, execute_tool_plan, list_tools
    from integrations.model_mesh import generate_text, provider_status


WORKFLOW_ENGINE_HINTS = {
    "Website Design and Deployment": "writing",
    "Storefront and Stripe Offers": "marketing",
    "Real Estate Development Packet": "construction",
    "Property Management Setup": "automation",
    "Release Campaign and Media Packaging": "marketing",
    "Client Intake and Service Routing": "research",
    "Sacred Geometry Book Research and Publishing": "research",
    "Executive Planning and Prioritization": "automation",
}


@dataclass
class OperatorMission:
    business: str
    workflow: str
    mission: str
    deliverables: list[str]
    constraints: list[str]
    context: list[str]
    integrations: list[str]
    preferred_provider: str | None
    execute_automation: bool
    stack_id: str | None


class OperatorRuntime:
    def __init__(self) -> None:
        self.run_store = RunStore()
        self.artifact_store = ArtifactStore()
        self.business_os = BusinessOperatingSystem()

    def status(self) -> dict[str, Any]:
        recent = self.run_store.list(limit=5)
        engine_catalog = [
            {
                "id": engine_key,
                "label": profile["label"],
                "focus": profile["focus"],
                "deliverables": profile["deliverables"],
            }
            for engine_key, profile in ENGINE_PROFILES.items()
        ]
        return {
            "service": "focus_master_ai_private_runtime",
            "providers": provider_status(),
            "connectors": build_connector_status(),
            "engines": engine_catalog,
            "agents": list_agents(),
            "stacks": list_stacks(),
            "tools": list_tools(),
            "jobs": EXECUTOR.status_snapshot(),
            "recent_runs": recent,
            "workflow_catalog": self.business_os.list_workflows(),
        }

    def list_runs(self, limit: int = 20) -> list[dict[str, Any]]:
        return self.run_store.list(limit=limit)

    def get_run(self, run_id: str) -> dict[str, Any] | None:
        run = self.run_store.get(run_id)
        if run is None:
            return None
        run["artifacts"] = self.artifact_store.list(run_id)
        return run

    def list_artifacts(self, run_id: str) -> list[dict[str, Any]]:
        return self.artifact_store.list(run_id)

    def create_run(self, payload: dict[str, Any]) -> dict[str, Any]:
        mission = self._normalize_payload(payload)
        run = self._initialize_run(mission)
        return self._execute_run(run["id"], mission)

    def submit_run(self, payload: dict[str, Any]) -> dict[str, Any]:
        mission = self._normalize_payload(payload)
        run = self._initialize_run(mission)
        self.run_store.append_event(run["id"], "job_queued", "Background operator run queued.")
        EXECUTOR.submit(run["id"], lambda: self._execute_run(run["id"], mission))
        queued = self.run_store.update(run["id"], status="queued")
        return self.get_run(run["id"]) or queued or run

    def _initialize_run(self, mission: OperatorMission) -> dict[str, Any]:
        task = self._compose_task(mission)
        workflow_stack = resolve_stack(mission.workflow, mission.mission, explicit_stack=mission.stack_id)
        preferred_engine = workflow_stack.get("primary_engine") or WORKFLOW_ENGINE_HINTS.get(mission.workflow)
        packet = build_master_task_packet(task, preferred_engine=preferred_engine)
        packet["engine_sequence"] = self._stack_sequence(workflow_stack, packet["engine_sequence"])
        packet["engine_prompts"] = {
            engine_key: build_engine_prompt(packet, engine_key) for engine_key in packet["engine_sequence"]
        }
        tool_plan = build_tool_plan(workflow_stack, mission.integrations)

        run = self.run_store.create(
            {
                "business": mission.business,
                "workflow": mission.workflow,
                "mission": mission.mission,
                "deliverables": mission.deliverables,
                "constraints": mission.constraints,
                "context": mission.context,
                "integrations": mission.integrations,
                "preferred_provider": mission.preferred_provider,
                "execute_automation": mission.execute_automation,
                "task": task,
                "task_packet": packet,
                "engine_sequence": packet["engine_sequence"],
                "workflow_stack": workflow_stack,
                "tool_plan": tool_plan,
                "status": "queued",
                "results": [],
            }
        )
        self.run_store.append_event(run["id"], "run_initialized", "Private operator run initialized.", workflow=mission.workflow)
        self._write_initial_artifacts(run["id"], mission, packet, workflow_stack, tool_plan)
        return run

    def _execute_run(self, run_id: str, mission: OperatorMission) -> dict[str, Any]:
        run = self.run_store.get(run_id)
        if run is None:
            raise ValueError(f"run not found: {run_id}")

        packet = run["task_packet"]
        workflow_stack = run["workflow_stack"]
        tool_plan = run["tool_plan"]
        task = run["task"]
        self.run_store.update(run_id, status="running")
        self.run_store.append_event(run_id, "run_started", "Background execution started.")

        results: list[dict[str, Any]] = []
        for engine_key in packet["engine_sequence"]:
            self.run_store.append_event(run_id, "engine_started", f"Running {engine_key}.", engine=engine_key)
            result = run_ai_engine(
                engine_key,
                task,
                execute_automation=False,
                preferred_provider=mission.preferred_provider,
            )
            results.append(result)
            self._write_engine_artifact(run_id, result)
            self.run_store.append_event(
                run_id,
                "engine_completed",
                f"{engine_key} completed in {result.get('model_execution', {}).get('mode', 'fallback')} mode.",
                engine=engine_key,
                provider=result.get("model_execution", {}).get("provider", "fallback"),
            )

        tool_runs = execute_tool_plan(
            run_id,
            tool_plan,
            automation_allowed=mission.execute_automation,
            task_prompt=packet["master_prompt"],
        )
        self.artifact_store.create_json(run_id, name="tool_runs", payload=tool_runs, metadata={"kind": "tool_runs"})
        self.run_store.append_event(run_id, "tool_plan_completed", "Tool plan evaluated.", tool_count=len(tool_runs))

        summary = self._summarize_run(run, packet, results, workflow_stack=workflow_stack, tool_runs=tool_runs, preferred_provider=mission.preferred_provider)
        self.artifact_store.create(
            run_id,
            name="final_summary",
            content=summary["content"],
            metadata={"kind": "summary", "provider": summary.get("provider", "fallback")},
        )
        self.artifact_store.create_json(
            run_id,
            name="result_bundle",
            payload={
                "results": results,
                "tool_runs": tool_runs,
                "summary_meta": {
                    "provider": summary.get("provider", "fallback"),
                    "model": summary.get("model", "templated-fallback"),
                    "mode": summary.get("mode", "fallback"),
                    "attempted": summary.get("attempted", []),
                },
            },
            metadata={"kind": "result_bundle"},
        )

        final_run = self.run_store.update(
            run_id,
            status="completed",
            completed_at=self._latest_timestamp(),
            results=results,
            tool_runs=tool_runs,
            final_summary=summary["content"],
            final_summary_meta={
                "provider": summary.get("provider", "fallback"),
                "model": summary.get("model", "templated-fallback"),
                "mode": summary.get("mode", "fallback"),
                "attempted": summary.get("attempted", []),
            },
            connector_snapshot=build_connector_status(),
            provider_snapshot=provider_status(),
            artifacts=self.artifact_store.list(run_id),
        )
        self.run_store.append_event(run_id, "run_completed", "Private operator run completed successfully.")
        return self.get_run(run_id) or final_run or run

    def _normalize_payload(self, payload: dict[str, Any]) -> OperatorMission:
        mission = str(payload.get("mission", "")).strip()
        if not mission:
            raise ValueError("mission is required")

        workflow = str(payload.get("workflow", "")).strip() or "Website Design and Deployment"
        integrations = payload.get("integrations") or []
        if not isinstance(integrations, list):
            raise ValueError("integrations must be a list")

        def _as_lines(value: Any) -> list[str]:
            if isinstance(value, list):
                return [str(item).strip() for item in value if str(item).strip()]
            text = str(value or "").strip()
            return [line.strip() for line in text.splitlines() if line.strip()]

        return OperatorMission(
            business=str(payload.get("business", "focus-negotium")).strip() or "focus-negotium",
            workflow=workflow,
            mission=mission,
            deliverables=_as_lines(payload.get("deliverables")),
            constraints=_as_lines(payload.get("constraints")),
            context=_as_lines(payload.get("context")),
            integrations=[str(item).strip() for item in integrations if str(item).strip()],
            preferred_provider=(str(payload.get("preferred_provider", "")).strip() or None),
            execute_automation=bool(payload.get("execute_automation", True)),
            stack_id=(str(payload.get("stack_id", "")).strip() or None),
        )

    @staticmethod
    def _latest_timestamp() -> str:
        from datetime import datetime, timezone

        return datetime.now(timezone.utc).isoformat()

    @staticmethod
    def _stack_sequence(workflow_stack: dict[str, Any], default_sequence: list[str]) -> list[str]:
        raw = workflow_stack.get("engine_sequence") or default_sequence
        deduped = [engine for engine in raw if engine in ENGINE_PROFILES]
        if not deduped:
            deduped = list(default_sequence)
        if deduped[-1] != "automation":
            deduped.append("automation")
        return list(dict.fromkeys(deduped))

    def _compose_task(self, mission: OperatorMission) -> str:
        sections = [
            f"Business lane: {mission.business}",
            f"Workflow: {mission.workflow}",
            f"Mission: {mission.mission}",
        ]
        if mission.deliverables:
            sections.append("Deliverables: " + "; ".join(mission.deliverables))
        if mission.constraints:
            sections.append("Constraints: " + "; ".join(mission.constraints))
        if mission.context:
            sections.append("Context: " + "; ".join(mission.context))
        if mission.integrations:
            sections.append("Integrations: " + ", ".join(mission.integrations))
        return "\n".join(sections)

    def _write_initial_artifacts(
        self,
        run_id: str,
        mission: OperatorMission,
        packet: dict[str, Any],
        workflow_stack: dict[str, Any],
        tool_plan: list[dict[str, Any]],
    ) -> None:
        brief = (
            "# Private Operator Brief\n\n"
            f"Business: {mission.business}\n\n"
            f"Workflow: {mission.workflow}\n\n"
            f"Stack: {workflow_stack['label']}\n\n"
            f"Mission: {mission.mission}\n\n"
            "## Deliverables\n"
            + ("\n".join(f"- {item}" for item in mission.deliverables) if mission.deliverables else "- None listed")
            + "\n\n## Constraints\n"
            + ("\n".join(f"- {item}" for item in mission.constraints) if mission.constraints else "- None listed")
            + "\n\n## Context\n"
            + ("\n".join(f"- {item}" for item in mission.context) if mission.context else "- None listed")
        )
        self.artifact_store.create(run_id, name="run_brief", content=brief, metadata={"kind": "brief"})
        self.artifact_store.create_json(run_id, name="task_packet", payload=packet, metadata={"kind": "task_packet"})
        self.artifact_store.create_json(run_id, name="workflow_stack", payload=workflow_stack, metadata={"kind": "workflow_stack"})
        self.artifact_store.create_json(run_id, name="tool_plan", payload=tool_plan, metadata={"kind": "tool_plan"})

    def _write_engine_artifact(self, run_id: str, result: dict[str, Any]) -> None:
        execution = result.get("model_execution", {})
        body = (
            f"# {result['label']}\n\n"
            f"Engine: {result['engine']}\n"
            f"Provider: {execution.get('provider', 'fallback')}\n"
            f"Model: {execution.get('model', 'templated-fallback')}\n"
            f"Mode: {execution.get('mode', 'fallback')}\n\n"
            f"{result.get('output', '')}"
        )
        self.artifact_store.create(
            run_id,
            name=f"engine_{result['engine']}",
            content=body,
            metadata={"kind": "engine_output", "engine": result["engine"]},
        )

    def _summarize_run(
        self,
        run: dict[str, Any],
        packet: dict[str, Any],
        results: list[dict[str, Any]],
        *,
        workflow_stack: dict[str, Any],
        tool_runs: list[dict[str, Any]],
        preferred_provider: str | None,
    ) -> dict[str, Any]:
        bullet_results = "\n".join(
            f"- {item['label']} ({item.get('model_execution', {}).get('provider', 'fallback')} / "
            f"{item.get('model_execution', {}).get('mode', 'fallback')}): {item['output'][:900]}"
            for item in results
        )
        tool_result_block = "\n".join(
            f"- {tool['label']}: {tool['status']} ({tool['execution_mode']})" for tool in tool_runs
        )
        summary_prompt = (
            "You are the private operator synthesis layer for FOCUS MASTER AI.\n"
            "Turn the engine outputs into one decisive internal execution brief.\n\n"
            f"Mission:\n{run['mission']}\n\n"
            f"Workflow stack: {workflow_stack['label']}\n"
            f"Engine sequence: {', '.join(packet['engine_sequence'])}\n\n"
            "Return these sections:\n"
            "1. Executive summary\n"
            "2. Completed outputs\n"
            "3. Risks and watchouts\n"
            "4. Recommended next actions\n"
            "5. Suggested follow-up automations\n"
            "6. Artifact package status\n\n"
            f"Engine outputs:\n{bullet_results}\n\n"
            f"Tool results:\n{tool_result_block}"
        )
        fallback = (
            "# Private Execution Summary\n\n"
            f"Mission: {run['mission']}\n\n"
            "## Completed Outputs\n"
            + "\n".join(f"- {item['label']}: {item['status']}" for item in results)
            + "\n\n## Tool Routing\n"
            + ("\n".join(f"- {tool['label']}: {tool['status']}" for tool in tool_runs) or "- No tool runs captured.")
            + "\n\n## Recommended Next Actions\n"
            "- Review the engine outputs in order.\n"
            "- Approve publish or automation steps only after operator review.\n"
            "- Convert accepted outputs into deployment, client, or production work."
        )
        return generate_text(
            summary_prompt,
            engine_key="writing",
            preferred_provider=preferred_provider,
            fallback_text=fallback,
        )
