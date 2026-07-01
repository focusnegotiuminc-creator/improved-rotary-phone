from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol

from .core import CoordinateState, OperationMode, OperatorOSKernel


class Agent(Protocol):
    name: str

    def run(self, task: str, state: CoordinateState) -> str: ...


@dataclass(slots=True)
class PromptArchitectAgent:
    name: str = "prompt_architect"

    def run(self, task: str, state: CoordinateState) -> str:
        return OperatorOSKernel().render_prompt(task, state)


@dataclass(slots=True)
class GlobalConsistencyAgent:
    name: str = "global_consistency"

    def run(self, task: str, state: CoordinateState) -> str:
        result = OperatorOSKernel().global_consistency_check(task, state, {})
        status = "ALIGNED" if result.aligned else "MISALIGNED"
        warnings = "; ".join(result.warnings) if result.warnings else "none"
        return f"{status}: warnings={warnings}"


@dataclass(slots=True)
class RecodingGateAgent:
    """Prevents uncontrolled self-modification.

    This agent can recommend a code change, but the output is a PR instruction,
    not an instruction to mutate live execution directly.
    """

    name: str = "recoding_gate"

    def run(self, task: str, state: CoordinateState) -> str:
        return (
            "Create branch -> edit files -> run tests -> open PR -> wait for human approval. "
            "Never patch live execution directly."
        )


DEFAULT_AGENT_ROUTE = {
    OperationMode.NEUTRAL: [GlobalConsistencyAgent()],
    OperationMode.LOCAL: [PromptArchitectAgent(), RecodingGateAgent()],
    OperationMode.NON_LOCAL: [GlobalConsistencyAgent(), PromptArchitectAgent()],
    OperationMode.RECURSIVE: [GlobalConsistencyAgent(), RecodingGateAgent()],
    OperationMode.NAVIGATIONAL: [PromptArchitectAgent()],
    OperationMode.VOID: [GlobalConsistencyAgent()],
}
