# Sierra Fast-Funds Options (3 Paths) for Current Stack

## Context
Goal: let Sierra access earnings as fast as possible while using your current Bluevine/Square/Stripe operating stack.

## Important Security Constraint
- This workflow does **not** extract hidden credentials from chat history or secret stores.
- It uses only configured environment secrets and provider onboarding forms.

## Path 1 — Square Payroll first, then EWA provider
- Why: you already use Square, so setup friction is usually lowest.
- Typical setup inputs: company EIN/legal info, employee profile, bank account for funding.
- Fast-funds route: pair payroll with an EWA provider after payroll feed is active.

## Path 2 — Gusto payroll + EWA add-on/provider
- Why: mainstream payroll onboarding and broad support ecosystem.
- Typical setup inputs: business + employee onboarding profile and payroll calendar.
- Fast-funds route: connect EWA after first payroll profile sync.

## Path 3 — EWA-first provider onboarding (Payactiv / DailyPay) with payroll integration
- Why: purpose-built for pre-payday earned access.
- Typical setup inputs: employer profile, payroll provider connection, employee consent/disclosures.
- Fast-funds route: employee can request earned funds after earnings feed is live.

## What is already prepared on this device
- Payroll input file ready with all 3 company lines:
  - `reports/2026-03-28_sierra_payroll_run_input.csv`
- Computed subtotal and blocker status:
  - `reports/2026-03-28_sierra_payroll_prep_output.md`

## Minimal Data Checklist (what you asked for)
- Company contact and legal business details
- Employee identity/onboarding details (Sierra)
- Payroll hours and rates (now filled in this workspace)
- Funding account details for disbursement timing rules

## Immediate execution sequence
1. Choose one of the 3 paths.
2. Submit Sierra payroll run using the prepared CSV values.
3. Save payroll confirmation ID and payout timing.
4. Complete EWA provider onboarding and employee invitation.
5. Validate first earned-access transaction and reconciliation.
