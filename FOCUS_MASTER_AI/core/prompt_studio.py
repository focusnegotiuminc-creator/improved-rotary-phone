from __future__ import annotations

from typing import Any

try:
    from FOCUS_MASTER_AI.core.task_classifier import classify_task
    from FOCUS_MASTER_AI.integrations.openai_client import call_gpt
except ImportError:
    from core.task_classifier import classify_task
    from integrations.openai_client import call_gpt


ENGINE_PROFILES: dict[str, dict[str, Any]] = {
    "research": {
        "label": "Research Engine",
        "focus": "verified research, synthesis, constraints, and next-best actions",
        "deliverables": [
            "source-aware findings summary",
            "key risks and assumptions",
            "recommended next actions",
        ],
    },
    "claims": {
        "label": "Claims Engine",
        "focus": "claim extraction, verification paths, evidence priorities, and rebuttal logic",
        "deliverables": [
            "top claims list",
            "verification path per claim",
            "evidence gaps and confidence notes",
        ],
    },
    "writing": {
        "label": "Writing Engine",
        "focus": "clear, conversion-grade writing, structured drafts, and deliverable polish",
        "deliverables": [
            "high-quality draft output",
            "headline or framing options",
            "action checklist for the user",
        ],
    },
    "geometry": {
        "label": "Geometry Engine",
        "focus": "layout logic, dimensions assumptions, spatial constraints, and visual structure",
        "deliverables": [
            "spatial concept direction",
            "layout assumptions",
            "constraints and implementation notes",
        ],
    },
    "construction": {
        "label": "Construction Engine",
        "focus": "execution planning, milestones, dependencies, field risk, and build sequencing",
        "deliverables": [
            "build sequence",
            "dependency and risk register",
            "owner-facing summary",
        ],
    },
    "compliance": {
        "label": "Compliance Engine",
        "focus": "compliance guardrails, operational risks, approvals, and required review steps",
        "deliverables": [
            "compliance watchouts",
            "required approvals",
            "safe execution checklist",
        ],
    },
    "frequency": {
        "label": "Frequency Engine",
        "focus": "cadence design, operational rhythm, attention management, and execution routines",
        "deliverables": [
            "execution cadence",
            "daily or weekly ritual",
            "focus preservation rules",
        ],
    },
    "marketing": {
        "label": "Marketing Engine",
        "focus": "offer framing, channel strategy, message architecture, and KPI design",
        "deliverables": [
            "channel plan",
            "message angle",
            "offer positioning and KPIs",
        ],
    },
    "ai_twin": {
        "label": "AI Twin Video Engine",
        "focus": "avatar strategy, video twin scripting, shot prompts, scene sequencing, and distribution cuts",
        "deliverables": [
            "ai twin identity brief",
            "scene-by-scene video treatment",
            "voiceover and shot prompt stack",
        ],
        "video_stack": [
            "Avatar performance brief for HeyGen, Tavus, or a local recording workflow",
            "Scene prompts for Runway, Sora, or image-to-video tools",
            "Edit and caption pass for CapCut or DaVinci Resolve",
        ],
    },
    "publish": {
        "label": "Publishing Engine",
        "focus": "release packaging, launch surfaces, repo readiness, and downstream publishing handoff",
        "deliverables": [
            "release package summary",
            "publish checklist",
            "connector-ready handoff notes",
        ],
    },
    "automation": {
        "label": "Automation Engine",
        "focus": "connector routing, webhook handoff, remote execution, and ops-system continuation",
        "deliverables": [
            "automation route plan",
            "connector handoff payload",
            "remote execution notes",
        ],
    },
}

DEFAULT_DELIVERABLES = [
    "machine-grade prompt",
    "high-confidence output",
    "automation handoff",
]


def _normalize_primary_engine(task: str, preferred_engine: str | None = None) -> str:
    if preferred_engine in ENGINE_PROFILES:
        return preferred_engine

    task_type = classify_task(task)
    if task_type in ENGINE_PROFILES:
        return task_type
    if task_type == "multi":
        return "automation"
    return "writing"


def _should_include_ai_twin(task: str, primary_engine: str) -> bool:
    text = task.lower()
    twin_keywords = ("video", "avatar", "ai twin", "digital twin", "reel", "short-form", "voiceover")
    if any(keyword in text for keyword in twin_keywords):
        return True
    return primary_engine in {"marketing", "publish", "automation"}


def _build_engine_sequence(task: str, primary_engine: str) -> list[str]:
    text = task.lower()
    if any(keyword in text for keyword in ("full system", "master machine", "power house", "deploy architecture")):
        sequence = [
            "research",
            "claims",
            "writing",
            "geometry",
            "construction",
            "compliance",
            "marketing",
            "publish",
            "automation",
        ]
    elif primary_engine == "research":
        sequence = ["research", "writing", "automation"]
    elif primary_engine == "claims":
        sequence = ["research", "claims", "writing", "automation"]
    elif primary_engine == "writing":
        sequence = ["research", "writing", "automation"]
    elif primary_engine == "geometry":
        sequence = ["research", "geometry", "construction", "automation"]
    elif primary_engine == "construction":
        sequence = ["research", "geometry", "construction", "writing", "automation"]
    elif primary_engine == "compliance":
        sequence = ["research", "claims", "compliance", "automation"]
    elif primary_engine == "frequency":
        sequence = ["research", "frequency", "automation"]
    elif primary_engine == "marketing":
        sequence = ["research", "writing", "marketing", "publish", "automation"]
    elif primary_engine == "ai_twin":
        sequence = ["research", "writing", "ai_twin", "marketing", "automation"]
    elif primary_engine == "publish":
        sequence = ["research", "writing", "publish", "automation"]
    else:
        sequence = ["research", "writing", "automation"]

    if _should_include_ai_twin(task, primary_engine) and "ai_twin" not in sequence:
        insert_at = sequence.index("publish") if "publish" in sequence else max(len(sequence) - 1, 1)
        sequence.insert(insert_at, "ai_twin")

    deduped: list[str] = []
    for engine_key in sequence:
        if engine_key in ENGINE_PROFILES and engine_key not in deduped:
            deduped.append(engine_key)
    if deduped[-1] != "automation":
        deduped.append("automation")
    return deduped


def _connector_targets(task: str, sequence: list[str]) -> list[str]:
    text = task.lower()
    targets = ["OpenAI reasoning core"]
    if "automation" in sequence:
        targets.append("Make.com webhook automation")
        targets.append("Replit remote runner")
    if any(keyword in text for keyword in ("publish", "github", "repo", "release")) or "publish" in sequence:
        targets.append("GitHub publishing surface")
    if "ai_twin" in sequence:
        targets.append("AI twin video generation stack")
    return list(dict.fromkeys(targets))


def _experience_goals(primary_engine: str) -> list[str]:
    profile = ENGINE_PROFILES.get(primary_engine, ENGINE_PROFILES["writing"])
    return [
        f"Make the {profile['label']} feel decisive, high-quality, and ready for execution.",
        "Prefer free or low-cost tooling, reusable prompt packs, and automation-ready outputs.",
        "Deliver something the user can act on immediately without needing to re-brief the system.",
    ]


def build_engine_prompt(packet: dict[str, Any], engine_key: str) -> str:
    profile = ENGINE_PROFILES[engine_key]
    deliverables = "\n".join(f"- {item}" for item in profile["deliverables"])
    connectors = "\n".join(f"- {item}" for item in packet["connector_targets"])
    experience = "\n".join(f"- {item}" for item in packet["experience_goals"])

    return (
        f"You are the {profile['label']} inside the FOCUS MASTER AI machine.\n"
        f"Primary focus: {profile['focus']}.\n\n"
        f"User task:\n{packet['task']}\n\n"
        f"Mission brief:\n{packet['mission']}\n\n"
        f"Required deliverables:\n{deliverables}\n\n"
        f"Connector context:\n{connectors}\n\n"
        f"Experience standard:\n{experience}\n\n"
        "Execution rules:\n"
        "- Produce high-quality, detailed, structured output.\n"
        "- Make the result automation-ready and easy to hand off.\n"
        "- Prefer free or low-cost tool paths when possible.\n"
        "- Be specific, practical, and execution-oriented."
    )


def _fallback_output(packet: dict[str, Any], engine_key: str) -> str:
    profile = ENGINE_PROFILES[engine_key]
    deliverables = "\n".join(f"- {item}" for item in profile["deliverables"])
    automation = "\n".join(f"- {item}" for item in packet["automation_hooks"])
    return (
        f"# {profile['label']} Fallback Execution Brief\n\n"
        f"Task: {packet['task']}\n\n"
        f"Mission:\n{packet['mission']}\n\n"
        f"Priority Deliverables:\n{deliverables}\n\n"
        f"Execution Flow:\n- Primary engine: {packet['primary_engine_label']}\n"
        f"- Engine chain: {', '.join(packet['engine_sequence'])}\n"
        f"- User experience target: {packet['experience_goals'][0]}\n\n"
        f"Automation Handoff:\n{automation}\n"
    )


def run_llm_or_fallback(prompt: str, packet: dict[str, Any], engine_key: str) -> str:
    output = call_gpt(prompt)
    if output.startswith("[OpenAI unavailable]") or output.startswith("[OpenAI error]"):
        return _fallback_output(packet, engine_key)
    return output


def build_master_task_packet(task: str, preferred_engine: str | None = None) -> dict[str, Any]:
    primary_engine = _normalize_primary_engine(task, preferred_engine=preferred_engine)
    engine_sequence = _build_engine_sequence(task, primary_engine)
    connector_targets = _connector_targets(task, engine_sequence)
    primary_profile = ENGINE_PROFILES[primary_engine]
    deliverables = list(dict.fromkeys(primary_profile["deliverables"] + DEFAULT_DELIVERABLES))
    automation_hooks = [
        "Expand raw task input into a machine-grade prompt packet before execution.",
        "Run the most relevant engines in a deliberate sequence instead of one flat completion.",
        "Prepare connector-ready payloads for Make, Replit, GitHub, and any configured remotes.",
    ]
    if "ai_twin" in engine_sequence:
        automation_hooks.append("Generate an AI twin video brief with scene, voiceover, and distribution cutdown guidance.")

    mission = (
        f"Turn the user's request into a premium execution-ready system output led by the {primary_profile['label']}, "
        "with automation hooks, reusable prompts, and top-tier end-user clarity."
    )

    packet: dict[str, Any] = {
        "task": task.strip(),
        "primary_engine": primary_engine,
        "primary_engine_label": primary_profile["label"],
        "engine_sequence": engine_sequence,
        "connector_targets": connector_targets,
        "deliverables": deliverables,
        "automation_hooks": automation_hooks,
        "experience_goals": _experience_goals(primary_engine),
        "mission": mission,
        "master_prompt": "",
        "engine_prompts": {},
    }
    packet["master_prompt"] = (
        "You are FOCUS MASTER AI, a total execution machine.\n\n"
        f"User task:\n{packet['task']}\n\n"
        f"Primary engine: {packet['primary_engine_label']}\n"
        f"Engine chain: {', '.join(packet['engine_sequence'])}\n\n"
        "Required deliverables:\n"
        + "\n".join(f"- {item}" for item in packet["deliverables"])
        + "\n\nAutomation hooks:\n"
        + "\n".join(f"- {item}" for item in packet["automation_hooks"])
        + "\n\nExperience goals:\n"
        + "\n".join(f"- {item}" for item in packet["experience_goals"])
    )
    packet["engine_prompts"] = {
        engine_key: build_engine_prompt(packet, engine_key) for engine_key in engine_sequence
    }

    if "ai_twin" in engine_sequence:
        packet["video_twin_stack"] = ENGINE_PROFILES["ai_twin"]["video_stack"]

    return packet
