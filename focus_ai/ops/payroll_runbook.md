# Payroll Runbook

## Inputs Needed
- Approved `employee_hours_template.csv`
- Employee pay rates and pay schedule
- Contractor vs employee classification
- Tax and withholding setup in the payroll platform

## Weekly Flow
1. Export approved hours for the active pay period.
2. Validate totals, overtime, and missing approvals.
3. Enter hours into the payroll platform.
4. Confirm gross pay, deductions, and net pay totals.
5. Save payroll confirmation ID and payout date in the operations log.

## Controls
- Do not run payroll from estimated hours.
- Keep rate changes in writing before the payroll run.
- Reconcile Stripe sales and cash position before large payout commitments.
