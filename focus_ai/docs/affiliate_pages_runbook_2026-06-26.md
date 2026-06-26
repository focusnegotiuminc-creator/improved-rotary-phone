# Affiliate Pages Deployment Runbook

## Build locally

```bash
python3 focus_ai/scripts/publish_ebooks.py
python3 focus_ai/scripts/build_public_site.py
python3 focus_ai/scripts/build_affiliate_pages.py
```

## Confirm generated files

```bash
ls focus_ai/published/public_site/rlcsolutions/index.html
ls focus_ai/published/public_site/focusrecords/index.html
ls focus_ai/published/public_site/waldenauto/index.html
ls focus_ai/published/public_site/WaldensTimberCarryingConstruction/index.html
cat focus_ai/published/public_site/affiliate-pages-manifest.json
```

## Deploy through existing public build workflow

The existing InfinityFree deployment workflow has been updated to build the affiliate pages after the main public site.

Run from GitHub Actions:

- Workflow: `Deploy TheFocusCorp Site`
- Branch: `main` after this PR is merged

## Verify live output

```bash
FOCUS_APP_URL="https://thefocuscorp.com" \
FOCUS_APP_PATHS="/,/booking.html,/services.html,/products.html,/ebooks/index.html,/rlcsolutions/,/focusrecords/,/waldenauto/,/WaldensTimberCarryingConstruction/" \
python3 focus_ai/scripts/verify_live_app.py
```

## CRM integration notes

Each page contains a visible CRM payload block for backend/API mapping. In production, route the same fields into:

- Make/Zapier MCP intake
- Focus Master AI task creation
- email draft generation
- CRM labels/tags
- quote follow-up queues

Keep payment, legal, filing, grant, tax, payroll, or financial actions behind explicit human approval.
