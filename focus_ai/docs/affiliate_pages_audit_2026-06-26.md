# Affiliate Company Pages Build Audit — 2026-06-26

## Scope
This audit covers the public build integration for four company/affiliate routes under `thefocuscorp.com`:

- `/rlcsolutions/`
- `/focusrecords/`
- `/waldenauto/`
- `/WaldensTimberCarryingConstruction/`

## Generator strategy
The existing `focus_ai/scripts/build_public_site.py` is a large public-site generator responsible for the main storefront, services, books, command surfaces, and published assets. To avoid destabilizing the main generator, affiliate pages are implemented in a dedicated post-build generator:

- `focus_ai/scripts/build_affiliate_pages.py`

The deployment workflow now runs:

```bash
python3 focus_ai/scripts/publish_ebooks.py
python3 focus_ai/scripts/build_public_site.py
python3 focus_ai/scripts/build_affiliate_pages.py
```

This keeps the current public build intact while adding reproducible affiliate-company pages into `focus_ai/published/public_site`.

## Company data sources
Data was assembled from the active project context and prior website/business conversations.

### Royal Lee Construction Solutions LLC
- Route: `/rlcsolutions/`
- Contact: Reginald Hilton Jr.
- Phone: 217-257-6222
- Address context: 3930 New London Gravel Rd, Hannibal, MO 63401
- Business lane: construction planning, development planning, owner representation, concept packages, sacred-geometry planning.

### Focus Records LLC
- Route: `/focusrecords/`
- Contact: Reginald Hilton Jr.
- Phone: 217-257-6222
- Business lane: release systems, campaign packaging, media assets, licensing prep, digital products, and artist-service routes.

### Walden Auto
- Route: `/waldenauto/`
- Contact: Brian Lee Walden
- Phone: 844-392-5336
- Email: waldenauto1@gmail.com
- Address: 3269 Market Street, Hannibal, MO
- Business lane: auto repair, collision repair documentation, repair authorization, inspection-oriented repair planning, and vehicle-support packages.

### Waldens Timber Carrying Construction
- Route: `/WaldensTimberCarryingConstruction/`
- Contact: Brian Lee Walden
- Phone: 844-392-5336
- Email: waldenauto1@gmail.com
- Address: 3269 Market Street, Hannibal, MO
- Business lane: timber carrying, hauling, construction support, material movement, and local affiliate routing.

## SEO implementation
Each generated page includes:

- Unique HTML title and meta description
- Canonical URL
- Open Graph title, description, and URL
- LocalBusiness JSON-LD schema
- Keyword targeting
- Internal links to home, services, products, and booking

## Lead funnel implementation
Each page includes:

- Click-to-call CTA
- Email intake CTA
- Booking route CTA
- Service list
- Lead magnet list
- CRM payload block for Make, Zapier MCP, or custom backend routing

## Monetization implementation
Each page includes monetization paths appropriate to the company:

- Paid planning sessions
- Project/repair/hauling service leads
- Documentation package support
- Affiliate routing
- Digital product and media packages
- Future city/service page expansion

## Deployment integration
`.github/workflows/deploy-infinityfree.yml` now verifies the affiliate paths through `FOCUS_APP_PATHS` and runs `build_affiliate_pages.py` after `build_public_site.py`.

## Safety / approval controls
No secret values are stored in code. CRM and automation payloads reference approved environment-backed destinations and should remain behind human approval for sending, filing, account changes, payments, or legal/financial actions.

## Manual verification command
After deployment credentials are configured, run:

```bash
FOCUS_APP_URL="https://thefocuscorp.com" \
FOCUS_APP_PATHS="/,/booking.html,/services.html,/products.html,/ebooks/index.html,/rlcsolutions/,/focusrecords/,/waldenauto/,/WaldensTimberCarryingConstruction/" \
python3 focus_ai/scripts/verify_live_app.py
```
