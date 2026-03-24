# Sacred AI Business Engine

Automated content and offer generation system for books, blueprint products, business systems, and marketing assets.

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
- `automation/marketing_engine.py` (creates conversion-focused marketing assets)

## Frontend Dashboard
Run:

```bash
pip install flask
python frontend/app.py
```

Open `http://localhost:3000` to trigger automation and preview generated outputs.

## GitHub Actions
Workflow: `.github/workflows/auto-generate.yml`
- Runs every 2 hours (`0 */2 * * *`)
- Executes `python automation/ai_generator.py`
- Commits and pushes generated updates automatically

## Monetization Channels
- KDP book publishing (book library generated in `book/`)
- Gumroad digital products (offers + blueprint assets)
- Service offers (business setup and automation systems)
