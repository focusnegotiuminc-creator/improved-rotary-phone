# Focus Micro Alpha Research Engine

Paper-first market research environment for very small starting capital.

This repo connects AI research agents, sacred-geometry-inspired signal hypotheses, broker-data adapters, risk governance, reporting, and branch-based code-improvement workflows. It is designed for simulation first and does not promise rapid profit.

## Default operating mode

```text
PAPER_MODE=true
EXECUTION_MODE=disabled
MAX_DAILY_LOSS_USD=0.50
MAX_POSITION_NOTIONAL_USD=2.00
MAX_SIGNALS_PER_DAY=3
ALLOW_MARGIN=false
ALLOW_DERIVATIVES=false
ALLOW_SHORTING=false
```

## Agent set

- Market Scanner Agent
- Sacred Geometry Signal Agent
- Risk Governor Agent
- Backtest Agent
- Paper Simulation Agent
- Execution Gatekeeper
- Recoding Agent
- Security Agent
- Reporting Agent

## Safety contract

- No guaranteed returns.
- Real-money order routing is disabled by default.
- No margin, derivatives, short selling, or leverage.
- No bypassing brokerage rules, KYC, age requirements, or platform controls.
- No credentials in GitHub.
- Recoding improvements must open branches/PRs and pass tests before adoption.

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e . pytest pyyaml
pytest
python -m focus_micro_alpha.runner
```

## Broker-data adapters

The scaffold is intentionally broker-neutral. Add any real brokerage integration only after testing and paper simulation are stable. Store credentials in environment variables or GitHub Actions secrets, never in source files.
