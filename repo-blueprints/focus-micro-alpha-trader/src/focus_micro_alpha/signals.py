from __future__ import annotations

from dataclasses import dataclass


FIBONACCI_RATIOS = (0.236, 0.382, 0.5, 0.618, 1.0, 1.618)


@dataclass(frozen=True, slots=True)
class SignalCandidate:
    symbol: str
    confidence: float
    thesis: str
    invalidation: str
    notional_usd: float
    spread_pct: float


class FibonacciSignal:
    """Research-only hypothesis helper.

    This class creates reviewable signal notes for simulation and backtesting.
    It does not place orders and does not guarantee outcomes.
    """

    def levels(self, low: float, high: float) -> dict[str, float]:
        if high <= low:
            raise ValueError("high must be greater than low")
        span = high - low
        return {str(r): round(high - span * r, 4) for r in FIBONACCI_RATIOS}

    def placeholder_candidate(self, symbol: str, notional_usd: float = 1.0, spread_pct: float = 0.0) -> SignalCandidate:
        return SignalCandidate(
            symbol=symbol.upper(),
            confidence=0.0,
            thesis="research placeholder; requires backtest and paper simulation",
            invalidation="no simulated action until data-quality and risk checks pass",
            notional_usd=notional_usd,
            spread_pct=spread_pct,
        )
