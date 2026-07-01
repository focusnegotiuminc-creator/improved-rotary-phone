from focus_micro_alpha.risk import RiskGovernor, RiskRules
from focus_micro_alpha.signals import FibonacciSignal


def test_execution_is_disabled_by_default():
    decision = RiskGovernor().evaluate(
        confidence=1.0,
        notional_usd=1.0,
        spread_pct=0.01,
        daily_loss_usd=0.0,
        signals_today=0,
        requests_execution=True,
    )
    assert decision.approved is False
    assert "disabled" in decision.reason


def test_notional_limit_blocks_oversized_simulation():
    decision = RiskGovernor(RiskRules(max_position_notional_usd=2.0)).evaluate(
        confidence=1.0,
        notional_usd=3.0,
        spread_pct=0.01,
        daily_loss_usd=0.0,
        signals_today=0,
    )
    assert decision.approved is False


def test_fibonacci_levels_are_ordered():
    levels = FibonacciSignal().levels(10.0, 20.0)
    assert "0.618" in levels
    assert levels["0.236"] > levels["0.618"]
