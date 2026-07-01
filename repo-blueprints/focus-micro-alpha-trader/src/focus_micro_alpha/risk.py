from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class RiskRules:
    max_daily_loss_usd: float = 0.50
    max_position_notional_usd: float = 2.00
    max_signals_per_day: int = 3
    min_confidence: float = 0.60
    max_spread_pct: float = 0.35
    paper_mode: bool = True
    execution_enabled: bool = False
    allow_margin: bool = False
    allow_derivatives: bool = False
    allow_shorting: bool = False


@dataclass(frozen=True, slots=True)
class RiskDecision:
    approved: bool
    reason: str


class RiskGovernor:
    def __init__(self, rules: RiskRules | None = None) -> None:
        self.rules = rules or RiskRules()

    def evaluate(
        self,
        *,
        confidence: float,
        notional_usd: float,
        spread_pct: float,
        daily_loss_usd: float,
        signals_today: int,
        requests_execution: bool = False,
        uses_margin: bool = False,
        uses_derivatives: bool = False,
        is_short: bool = False,
    ) -> RiskDecision:
        if requests_execution and not self.rules.execution_enabled:
            return RiskDecision(False, "execution disabled; simulation only")
        if uses_margin and not self.rules.allow_margin:
            return RiskDecision(False, "margin is not allowed")
        if uses_derivatives and not self.rules.allow_derivatives:
            return RiskDecision(False, "derivatives are not allowed")
        if is_short and not self.rules.allow_shorting:
            return RiskDecision(False, "short selling is not allowed")
        if confidence < self.rules.min_confidence:
            return RiskDecision(False, "confidence below threshold")
        if notional_usd > self.rules.max_position_notional_usd:
            return RiskDecision(False, "notional amount above limit")
        if spread_pct > self.rules.max_spread_pct:
            return RiskDecision(False, "spread too wide")
        if daily_loss_usd >= self.rules.max_daily_loss_usd:
            return RiskDecision(False, "daily loss limit reached")
        if signals_today >= self.rules.max_signals_per_day:
            return RiskDecision(False, "daily signal count limit reached")
        return RiskDecision(True, "risk rules satisfied for simulation")
