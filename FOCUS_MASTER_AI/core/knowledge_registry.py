from __future__ import annotations

import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ALLOWED_EXTENSIONS = {".csv", ".html", ".json", ".md", ".txt", ".yaml", ".yml"}
KNOWLEDGE_DIRECTORIES = (
    "focus_ai/docs",
    "focus_ai/ebooks",
    "focus_ai/prompts",
    "focus_ai/engine",
    "book",
    "docs",
    "final_product",
    "marketing",
    "reports",
    "research",
)
COMPANY_TERMS = {
    "focus-records": ("focus records", "records", "release", "music", "media"),
    "royal-lee-construction": ("royal lee", "construction", "build", "geometry", "layout"),
    "focus-negotium": ("focus negotium", "negotium", "automation", "monetization", "operations"),
}
ENGINE_TERMS = {
    "intake": ("intake", "source analyst"),
    "context-load": ("context", "voice architect"),
    "architecture-framing": ("offer", "architecture", "strategist"),
    "prompt-assembly": ("prompt", "prompt pack"),
    "build-integrate": ("design", "copywriter", "build"),
    "verification": ("qa", "proof", "quality"),
    "deployment": ("deploy", "release", "launch"),
}
CAMPAIGN_TERMS = {
    "sales": ("sales", "offer", "upsell", "checkout"),
    "books": ("ebook", "book", "manuscript"),
    "funnel": ("funnel", "lead", "landing", "email"),
}
LEGAL_TERMS = ("legal", "trust", "payroll", "bank", "compliance", "508(c)(1)(a)")


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _read_sample(path: Path, limit: int = 4000) -> str:
    try:
        return path.read_text(encoding="utf-8", errors="ignore")[:limit]
    except OSError:
        return ""


def _title_for(path: Path, content: str) -> str:
    for line in content.splitlines():
        stripped = line.strip()
        if stripped.startswith("#"):
            return stripped.lstrip("#").strip()
    return path.stem.replace("_", " ").replace("-", " ").title()


def _match_tags(content: str, mapping: dict[str, tuple[str, ...]]) -> list[str]:
    text = content.lower()
    return [tag for tag, terms in mapping.items() if any(term in text for term in terms)]


def _asset_type(path: Path) -> str:
    suffix = path.suffix.lower()
    if suffix == ".md":
        return "markdown"
    if suffix == ".json":
        return "json"
    if suffix == ".csv":
        return "spreadsheet"
    if suffix in {".html", ".yaml", ".yml"}:
        return "config"
    return "document"


def build_knowledge_snapshot(repo_root: Path, limit: int | None = None) -> dict[str, Any]:
    artifacts: list[dict[str, Any]] = []

    for rel_dir in KNOWLEDGE_DIRECTORIES:
        folder = repo_root / rel_dir
        if not folder.exists():
            continue

        for path in sorted(folder.rglob("*")):
            if not path.is_file() or path.suffix.lower() not in ALLOWED_EXTENSIONS:
                continue

            content = _read_sample(path)
            relative = path.relative_to(repo_root).as_posix()
            title = _title_for(path, content)
            enriched_text = relative.lower() + "\n" + content

            artifacts.append(
                {
                    "id": re.sub(r"[^a-z0-9]+", "-", path.stem.lower()).strip("-"),
                    "title": title,
                    "path": relative,
                    "asset_type": _asset_type(path),
                    "company_tags": _match_tags(enriched_text, COMPANY_TERMS),
                    "engine_stages": _match_tags(enriched_text, ENGINE_TERMS),
                    "campaign_tags": _match_tags(enriched_text, CAMPAIGN_TERMS),
                    "legal_sensitivity": "high" if any(term in enriched_text for term in LEGAL_TERMS) else "standard",
                    "prompt_pack": "prompt" in enriched_text,
                    "provenance": {
                        "source": "local_repo",
                        "directory": rel_dir,
                    },
                }
            )

    if limit is not None:
        artifacts = artifacts[:limit]

    return {
        "generated_at": _utc_now(),
        "artifact_count": len(artifacts),
        "artifacts": artifacts,
    }


def find_related_artifacts(snapshot: dict[str, Any], topic: str, limit: int = 5) -> list[dict[str, Any]]:
    if not topic.strip():
        return snapshot.get("artifacts", [])[:limit]

    words = {word for word in re.findall(r"[a-z0-9]{3,}", topic.lower())}
    ranked: list[tuple[int, dict[str, Any]]] = []
    for artifact in snapshot.get("artifacts", []):
        haystack = " ".join(
            [
                artifact.get("title", ""),
                artifact.get("path", ""),
                " ".join(artifact.get("company_tags", [])),
                " ".join(artifact.get("campaign_tags", [])),
                " ".join(artifact.get("engine_stages", [])),
            ]
        ).lower()
        score = sum(1 for word in words if word in haystack)
        if score:
            ranked.append((score, artifact))

    ranked.sort(key=lambda item: item[0], reverse=True)
    return [artifact for _, artifact in ranked[:limit]]


def write_knowledge_snapshot(output_path: Path, snapshot: dict[str, Any]) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(snapshot, indent=2), encoding="utf-8")

