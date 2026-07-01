# Security and Compliance Guide

## Credentials

Never commit brokerage credentials, data provider keys, GitHub tokens, SSH keys, private keys, seed phrases, or account recovery material. Use local `.env` files and GitHub Secrets only.

## Execution control

The scaffold defaults to simulation. Any real-money order routing must remain disabled unless the human owner intentionally enables it and accepts the risk outside the code generator.

## Prohibited shortcuts

- Do not bypass KYC, identity checks, age limits, brokerage rules, or platform controls.
- Do not use someone else's brokerage identity.
- Do not hide account ownership or routing activity.
- Do not increase risk limits automatically after losses.

## Recoding agent rule

The recoding agent may:

- inspect logs
- propose code improvements
- create a branch
- add or update tests
- open a pull request

The recoding agent may not:

- push directly to protected/live branches
- enable execution mode
- change risk limits without a human-reviewed PR
- store credentials in code

## Audit trail

Every simulation cycle should produce:

- timestamp
- selected mode
- signal candidate
- reason for action or rejection
- risk decision
- code version / commit SHA
- next test or improvement
