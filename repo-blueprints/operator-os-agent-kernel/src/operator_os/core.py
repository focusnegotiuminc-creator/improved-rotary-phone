from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Iterable


class OperationMode(str, Enum):
    NEUTRAL = "neutral"
    LOCAL = "local"
    NON_LOCAL = "non_local"
    RECURSIVE = "recursive"
    NAVIGATIONAL = "navigational"
    VOID = "void"


class LoopStage(str, Enum):
    LOCAL_UPDATE = "local_update"
    GLOBAL_CONSISTENCY_CHECK = "global_consistency_check"
    LOCAL_REFINEMENT = "local_refinement"
    GLOBAL_COLLAPSE = "global_collapse"


@dataclass(slots=True)
class CoordinateState:
    """Operational coordinate state for an Operator OS cycle.

    eta: recursion depth / scale of engagement.
    theta: relational frame angle in degrees.
    psi_phi: phase redistribution or temporal loop angle in degrees.
    mode: selected operation mode.
    notes: compact human-readable context.
    """

    eta: str = "compressed"
    theta: int = 0
    psi_phi: int = 0
    mode: OperationMode = OperationMode.NEUTRAL
    notes: str = ""

    def normalized(self) -> "CoordinateState":
        return CoordinateState(
            eta=self.eta.strip().lower(),
            theta=self.theta % 360,
            psi_phi=self.psi_phi % 360,
            mode=self.mode,
            notes=self.notes.strip(),
        )


@dataclass(slots=True)
class CycleResult:
    stage: LoopStage
    coordinate_state: CoordinateState
    aligned: bool
    output: str
    warnings: list[str] = field(default_factory=list)


class OperatorOSKernel:
    """Deterministic loop coordinator for prompts, agents, and repo work."""

    def __init__(self, invariants: Iterable[str] | None = None) -> None:
        self.invariants = list(invariants or [
            "operator_sovereignty",
            "no_secret_commitment",
            "branch_based_recoding",
            "human_final_approval",
        ])
        self.history: list[CycleResult] = []

    def run_cycle(self, task: str, state: CoordinateState | None = None, context: dict[str, Any] | None = None) -> list[CycleResult]:
        if not task or not task.strip():
            raise ValueError("task must be a non-empty string")

        context = context or {}
        state = (state or CoordinateState()).normalized()
        results = [
            self.local_update(task, state, context),
            self.global_consistency_check(task, state, context),
            self.local_refinement(task, state, context),
            self.global_collapse(task, state, context),
        ]
        self.history.extend(results)
        return results

    def local_update(self, task: str, state: CoordinateState, context: dict[str, Any]) -> CycleResult:
        output = f"Task received: {task.strip()} | mode={state.mode.value} eta={state.eta} theta={state.theta} psi_phi={state.psi_phi}"
        return CycleResult(LoopStage.LOCAL_UPDATE, state, True, output)

    def global_consistency_check(self, task: str, state: CoordinateState, context: dict[str, Any]) -> CycleResult:
        warnings = []
        lower = task.lower()
        if "secret" in lower or "api key" in lower or "private key" in lower:
            warnings.append("Potential secret-handling request detected. Use environment variables or secret manager only.")
        if "guarantee" in lower or "guaranteed" in lower:
            warnings.append("Guaranteed-outcome language detected. Replace with tested probability and risk limits.")
        aligned = not any("Guaranteed" in w for w in warnings)
        return CycleResult(LoopStage.GLOBAL_CONSISTENCY_CHECK, state, aligned, "Consistency check complete.", warnings)

    def local_refinement(self, task: str, state: CoordinateState, context: dict[str, Any]) -> CycleResult:
        refined = (
            "Refine by reducing scope, defining file outputs, creating tests, "
            "and routing any recoding through a reviewable branch."
        )
        return CycleResult(LoopStage.LOCAL_REFINEMENT, state, True, refined)

    def global_collapse(self, task: str, state: CoordinateState, context: dict[str, Any]) -> CycleResult:
        return CycleResult(
            LoopStage.GLOBAL_COLLAPSE,
            state,
            True,
            "Resolution: produce the smallest executable artifact that advances the system without increasing hidden risk.",
        )

    def render_prompt(self, task: str, state: CoordinateState | None = None) -> str:
        state = (state or CoordinateState()).normalized()
        return (
            "You are an Operator OS execution agent.\n"
            f"Task: {task.strip()}\n"
            f"Coordinates: eta={state.eta}, theta={state.theta}, psi_phi={state.psi_phi}, mode={state.mode.value}.\n"
            "Loop: Local Update -> Global Consistency Check -> Local Refinement -> Global Collapse.\n"
            "Rules: no secrets, no uncontrolled live mutation, no unsupported certainty, human final approval.\n"
        )


if __name__ == "__main__":
    kernel = OperatorOSKernel()
    for item in kernel.run_cycle("Create a safe repo scaffold for a new AI agent environment."):
        print(f"[{item.stage.value}] {item.output}")
        for warning in item.warnings:
            print(f"WARNING: {warning}")
