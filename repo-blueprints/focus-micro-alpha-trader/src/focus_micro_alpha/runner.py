from __future__ import annotations

from .risk import RiskGovernor, RiskRules
from .signals import FibonacciSignal


def main() -> None:
    rules = RiskRules()
    governor = RiskGovernor(rules)
    signal = FibonacciSignal().placeholder_candidate("DEMO", notional_usd=1.0, spread_pct=0.05)
    decision = governor.evaluate(
        confidence=signal.confidence,
        notional_usd=signal.notional_usd,
        spread_pct=signal.spread_pct,
        daily_loss_usd=0.0,
        signals_today=0,
        requests_execution=False,
    )
    print("Focus Micro Alpha Research Engine")
    print(f"symbol={signal.symbol} confidence={signal.confidence}")
    print(f"risk_decision={decision.approved} reason={decision.reason}")
    print("mode=simulation-only")


if __name__ == "__main__":
    main()
