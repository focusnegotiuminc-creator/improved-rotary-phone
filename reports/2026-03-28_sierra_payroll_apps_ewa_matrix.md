# Sierra Payroll + EWA Matrix (3 Company Paths)

## Objective
Pick the easiest path to let Sierra access wages as quickly as possible with your current Bluevine/Square/Stripe operations context.

| Path | Primary Company | Setup Complexity | What You Need | Fast-Funds Readiness |
|---|---|---|---|---|
| 1 | Square Payroll | Low (best if already in Square ecosystem) | Company + employee onboarding + payroll schedule | High once payroll run is active |
| 2 | Gusto | Medium | Company profile, employee onboarding, bank funding, tax profile | Medium/High depending on payroll timing settings |
| 3 | Payactiv or DailyPay (EWA) | Medium | Employer setup + payroll integration + employee consent | High after earnings feed is connected |

## Data Already Ready in This Repo
- `reports/2026-03-28_sierra_payroll_run_input.csv`
- `reports/2026-03-28_sierra_payroll_prep_output.md`
- `reports/2026-03-28_payroll_completion_execution.md`

## Decision Rule
- If speed and least friction are priority: start with **Path 1 (Square Payroll)**.
- If you want dedicated earned-access UX quickly after payroll activation: choose **Path 3**.
