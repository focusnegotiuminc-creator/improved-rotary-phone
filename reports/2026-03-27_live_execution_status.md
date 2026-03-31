# Live Execution Status

Prepared: 2026-03-27

## Completed Today

- Repaired the public publishing pipeline by removing stale merge-conflict blocks from:
  - `focus_ai/scripts/publish_ebooks.py`
  - `focus_ai/scripts/build_public_site.py`
- Rebuilt the public outputs:
  - eBook library in `focus_ai/published/ebooks/`
  - public portal bundle in `focus_ai/published/public_site/`
- Deployed the current public bundle to InfinityFree FTP target `htdocs`
- Restarted the local Focus AI operator API and verified the latest task update route is available
- Confirmed live payment support state:
  - Stripe checkout links are live in the shared catalog
  - Square support is now coded as a ready-for-links section in the site and config, pending actual Square payment URLs
- Extracted the RLC office package source archive from Downloads and generated an updated owner packet from the hand-drawn sketches
- Added a Figma operating-system workflow diagram and a repo-local Figma design system rules guide

## Task Registry Status

### Completed

- Tina Tenhouse reply draft prepared and attached
- RLC owner packet draft generated from extracted sketches and logos

### Readiness Prepared

- Hannibal legal-services reschedule workflow
- Vendor/net-terms onboarding packet
- Payroll readiness packet

### Waiting On Inputs

- Square activation
  - still needs real Square payment links or buy-button URLs
- Madison County filing packet
  - factual workflow and motion-outline draft prepared, but current official filing forms and operator review are still needed before submission

## Key Output Files

- `reports/2026-03-27_tina_tenhouse_reply.md`
- `reports/2026-03-27_madison_county_case_workflow.md`
- `reports/2026-03-27_madison_county_factual_motion_outline.md`
- `reports/2026-03-27_payroll_readiness_packet.md`
- `reports/2026-03-27_payroll_and_ewa_options_memo.md`
- `reports/2026-03-27_vendor_account_setup_checklist.md`
- `docs/figma_design_system_rules.md`
- `construction/rlc_bid_input_checklist.md`
- `construction/rlc_bid_package_template.md`
- `construction/rlc_material_takeoff_template.csv`
- `construction/rlc_office_pkg_extracted/output/RLC_Quincy_Office_Package.pdf`
- `construction/rlc_office_pkg_extracted/output/RLC_Quincy_Blueprints_24x36.pdf`
- `construction/rlc_office_pkg_extracted/output/material_list.csv`
- `construction/rlc_office_pkg_extracted/output/bid_summary.json`

## Live Operator Endpoints

- `http://127.0.0.1:8000/operator`
- `http://127.0.0.1:8000/health`
- `http://127.0.0.1:8000/v1/tasks`
- `http://127.0.0.1:8000/v1/readiness`

## Payment Links

- Focus AI eBook Bundle: `https://buy.stripe.com/bJe7sKh2B6ZQ8bP4II5os02`
- Focus AI Blueprint Pack: `https://buy.stripe.com/cNi4gy27H83U4ZD3EE5os03`
- Focus AI Business Engine: `https://buy.stripe.com/4gMbJ0aEd97Y9fT2AA5os04`

## Visual Plugin Outputs

- Figma operating diagram:
  - `https://www.figma.com/online-whiteboard/create-diagram/3c7b9534-6c75-4f09-9db1-09bbd4016dc7?utm_source=other&utm_content=edit_in_figjam&oai_id=&request_id=1d69e6a9-d7ce-420b-aede-a25de12828e3`
- Repo-local Figma rules:
  - `docs/figma_design_system_rules.md`

## Guardrails Still In Effect

- Payroll remains readiness-only from this system
- Legal, banking, and court filings still require final human review and the correct official filing path
- No sensitive identity data should be stored in repo files
