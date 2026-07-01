# Operator OS Agent Kernel

A reusable Python agent kernel for Operator OS / Toroidal Navigation workflows.

This repo turns the Operator OS documents into a practical software environment:

- state-coordinate modeling with `eta`, `theta`, and `psi/phi`
- explicit operation modes: neutral, local, non-local, recursive, navigational, and void
- loop stages: local update, global consistency check, local refinement, global collapse
- failure-mode detection: drift, compression lock, attractor capture, identity hijack, premature collapse
- prompt generation for ChatGPT, Codex, GitHub, Zapier, and other connected systems
- branch-based recoding design: improvement agents propose PRs, not uncontrolled live mutation

## Why this exists

The Operator OS reference treats toroidal coordinates as operational controls: `eta` = recursion depth / scale, `theta` = relational frame rotation, and `psi/phi` = phase redistribution inside the loop. This repo converts that language into deterministic agent objects, logs, YAML configs, and testable workflows.

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e . pytest pyyaml
pytest
python -m operator_os.core
```

## Core loop

```text
Local Update -> Global Consistency Check -> Local Refinement -> Global Collapse
```

## Repo contract

- This kernel does not claim supernatural authority.
- The software treats toroidal terms as operational metaphors, state labels, and coordination primitives.
- The human Operator remains the final coherence arbiter.
- Any automated recoding must happen in a branch or pull request.

## Downstream use

The trading repo `focus-micro-alpha-trader` can import these concepts for prompt routing and agent orchestration, but it should keep brokerage execution and financial risk logic separate.
