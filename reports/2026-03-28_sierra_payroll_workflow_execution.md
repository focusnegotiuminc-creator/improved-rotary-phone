# Sierra Payroll Workflow Execution (Run on Device)

## What was executed now
1. Loaded prior payroll source data for Sierra from 2026-03-27 packet.
2. Created run input CSV for this cycle:
   - `reports/2026-03-28_sierra_payroll_run_input.csv`
3. Calculated confirmed subtotal from available lines: **$6,375.00**.
4. Generated prep output using:
   - `python3 focus_ai/scripts/run_sierra_payroll_prep.py`
   - Output: `reports/2026-03-28_sierra_payroll_prep_output.md`
5. Built free/low-cost app shortlist for payroll + EWA (earned wage access) setup.

## Confirmed Payroll Lines
- Focus Inc: 50 hours x $50.00 = $2,500.00
- Royal Lee Construction Solutions: 30 hours x $65.00 = $1,950.00
- Focus Negotium Inc: 35 hours x $55.00 = $1,925.00
- Confirmed subtotal: $6,375.00

## Blocking Item
- No unresolved hours/rate blockers remain in this working input.

## Free / Low-Cost Setup Candidates (to keep startup cost minimal)

### Payroll stack candidates
1. Payroll4Free (positioned as free payroll software; fee schedule shows potential paid add-ons depending on service choices).
2. SurePayroll (paid; listed as starting monthly + per-employee pricing).
3. Gusto (paid plans, with contractor-only promotional options shown on pricing pages).

### EWA candidates
1. DailyPay (materials state zero employer cost for implementation/offer and user fee model can vary by employer contract).
2. Payactiv (EWA provider with program-pricing and compliance pages; fee/disbursement model depends on program choices).

## EWA Requirements Checklist for your setup
- [ ] Payroll/time integration readiness (hours and earnings feed reliability).
- [ ] Written policy: eligibility, max withdrawal %, and repayment timing.
- [ ] Employee consent and disclosure acknowledgement.
- [ ] Confirm Illinois/Missouri handling with chosen provider and payroll stack.
- [ ] Pilot with one employee (Sierra) before broader rollout.

## Immediate Next Actions to complete payroll today
1. Approve all rows (replace `Pending Approval` with approver name).
2. Input run into selected payroll app and save confirmation number.
3. If enabling EWA, start with employer onboarding form from chosen provider after payroll profile is active.
