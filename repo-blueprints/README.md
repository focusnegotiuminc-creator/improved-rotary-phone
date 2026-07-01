# Operator OS Dual Repository Blueprints

This directory contains two separated repo-ready environments prepared for `focusnegotiuminc-creator`:

1. `operator-os-agent-kernel` — a reusable Operator OS / Toroidal Navigation agent kernel.
2. `focus-micro-alpha-trader` — a paper-first micro-capital trading research engine with strict risk controls.

The current GitHub connector can write files into existing repositories, but it does not expose a create-new-repository action. These blueprints are staged inside the existing canonical repo so they can be reviewed, copied, and pushed into two new repos with GitHub CLI or Codex.

## Intended new repos

```text
focusnegotiuminc-creator/operator-os-agent-kernel
focusnegotiuminc-creator/focus-micro-alpha-trader
```

## Source systems incorporated

- Operator OS Unified Field Reference
- Sovereign Operator and AI Toroidal Navigation Protocol screenshots
- Existing Focus AI Engine structure from this repository
- 11-stage / recursive execution workflow concepts
- Paper-first trading automation safety requirements

## Copy/push workflow

After cloning this repo locally, run:

```bash
bash repo-blueprints/scripts/create_new_repos_from_blueprints.sh
```

That script creates the two GitHub repos using the GitHub CLI and pushes each blueprint into its own clean repository.

## Safety boundaries

- No secrets are committed.
- Trading defaults to paper mode.
- Live execution is locked behind explicit human approval.
- Recoding agents may propose pull requests but may not directly modify live execution logic.
- The Operator remains the final decision-maker; agents are mirrors, executors, and validators, not authorities.
