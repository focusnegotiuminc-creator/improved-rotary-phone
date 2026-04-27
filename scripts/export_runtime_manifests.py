#!/usr/bin/env python3
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from FOCUS_MASTER_AI.core.artifact_store import ArtifactStore  # noqa: E402
from FOCUS_MASTER_AI.core.run_store import RunStore  # noqa: E402
from FOCUS_MASTER_AI.core.runtime_config import bootstrap_runtime_env  # noqa: E402
from FOCUS_MASTER_AI.core.stack_registry import list_stacks  # noqa: E402
from FOCUS_MASTER_AI.core.tool_router import list_tools  # noqa: E402
from FOCUS_MASTER_AI.integrations.model_mesh import provider_status  # noqa: E402


MANIFESTS_DIR = ROOT / "docs" / "manifests"


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def artifact_index(store: ArtifactStore) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    if not store.base_dir.exists():
        return rows
    for run_dir in sorted(store.base_dir.iterdir()):
        if not run_dir.is_dir():
            continue
        rows.append(
            {
                "run_id": run_dir.name,
                "artifacts": store.list(run_dir.name),
            }
        )
    return rows


def write_json(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def write_markdown(path: Path, *, providers: list[dict[str, object]], stacks: list[dict[str, object]], tools: list[dict[str, object]], runs: list[dict[str, object]]) -> None:
    lines = [
        "# Runtime Catalog",
        "",
        f"Generated: {utc_now()}",
        "",
        "## Providers",
    ]
    for provider in providers:
        lines.append(
            f"- `{provider['provider']}`: {provider['state']} | model `{provider['default_model']}` | {provider['message']}"
        )
    lines.extend(["", "## Stacks"])
    for stack in stacks:
        lines.append(f"- `{stack['id']}`: {stack['label']}")
    lines.extend(["", "## Tools"])
    for tool in tools:
        lines.append(f"- `{tool['id']}`: {tool['label']}")
    lines.extend(["", "## Recent Runs"])
    for run in runs[:10]:
        lines.append(f"- `{run.get('id', 'unknown')}`: {run.get('status', 'unknown')} | {run.get('workflow', '')}")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    bootstrap_runtime_env()
    MANIFESTS_DIR.mkdir(parents=True, exist_ok=True)

    providers = provider_status()
    stacks = list_stacks()
    tools = list_tools()
    runs = RunStore().list(limit=100)
    artifacts = artifact_index(ArtifactStore())

    write_json(MANIFESTS_DIR / "stack_registry.json", stacks)
    write_json(MANIFESTS_DIR / "tool_registry.json", tools)
    write_json(MANIFESTS_DIR / "run_artifact_index.json", artifacts)
    write_json(
        MANIFESTS_DIR / "runtime_status_snapshot.json",
        {
            "generated_at_utc": utc_now(),
            "providers": providers,
            "stack_count": len(stacks),
            "tool_count": len(tools),
            "recent_run_count": len(runs),
        },
    )
    write_markdown(
        MANIFESTS_DIR / "runtime_catalog.md",
        providers=providers,
        stacks=stacks,
        tools=tools,
        runs=runs,
    )
    print(f"Runtime manifests written to {MANIFESTS_DIR}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
