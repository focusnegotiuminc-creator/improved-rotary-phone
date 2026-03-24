# Sacred AI Business Engine

Automated content and monetization engine for books, blueprint products, business offers, funnel pages, and email follow-ups.

## Repository Structure
- `research/`
- `claims/`
- `book/`
- `geometry/`
- `construction/`
- `compliance/`
- `alignment/`
- `marketing/`
- `final_product/`
- `automation/`
- `frontend/`

## Core Automation Scripts
- `automation/ai_generator.py` (orchestrates all generation)
- `automation/book_writer.py` (generates 10 complete books at $19.99)
- `automation/blueprint_generator.py` (creates blueprint product drops)
- `automation/business_generator.py` (creates business offers and catalogs)
- `automation/marketing_engine.py` (generates funnel copy + email automation assets)

## Funnel Logic
Traffic -> Free Value (Lead Magnet) -> Email Capture -> Low Ticket ($20 Book) -> Mid Ticket ($49-$149) -> High Ticket ($299-$999) -> Automation + Follow-ups.

## Frontend Dashboard + Funnel Pages
Run:

```bash
pip install flask
python frontend/app.py
```

Pages:
- Dashboard: `http://localhost:3000/`
- Lead capture: `http://localhost:3000/landing`
- Delivery: `http://localhost:3000/delivery`
- Upsell: `http://localhost:3000/upsell`
- High-ticket: `http://localhost:3000/high-ticket`

Lead emails are stored in `final_product/leads.csv`.

## GitHub Actions
Workflow: `.github/workflows/auto-generate.yml`
- Runs every 2 hours (`0 */2 * * *`)
- Executes `python automation/ai_generator.py`
- Commits and pushes generated updates automatically

## Monetization Channels
- KDP book publishing (`book/`)
- Gumroad digital products (`geometry/`, `final_product/`)
- Service offers and application funnel (`frontend/`, `marketing/`)
