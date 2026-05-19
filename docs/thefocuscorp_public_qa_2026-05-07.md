# TheFocusCorp Public QA Report

Date: 2026-05-07
Workspace used for build and deploy: E:\FOCUS_MASTER_AI_live

## Build and deploy
- `python E:\FOCUS_MASTER_AI_live\focus_ai\scripts\build_public_site.py`
- `python -m pytest -q E:\FOCUS_MASTER_AI_live\tests\test_focus_master_business_os.py -o cache_dir=E:\FOCUS_MASTER_AI_live\.pytest_cache\focus_public_site`
- `python E:\FOCUS_MASTER_AI_live\focus_ai\scripts\deploy_local_live.py --env-file E:\FOCUS_MASTER_AI_live\.secrets\focus_master.env`

Results:
- public site build passed
- focused public-site tests passed: `4 passed`
- live deploy passed
- endpoint verification passed for `/`, `/wp-admin`, `/ebooks/index.html`, `/landing.html`

## Public mobile checks
Verified on rendered public pages with iPhone-size viewport:
- `https://www.thefocuscorp.com/`
- `https://www.thefocuscorp.com/landing.html`
- `https://www.thefocuscorp.com/store.html`
- `https://www.thefocuscorp.com/books.html`
- `https://www.thefocuscorp.com/focus-negotium.html`
- `https://www.thefocuscorp.com/focus-records.html`
- `https://www.thefocuscorp.com/royal-lee-construction.html`

Confirmed:
- horizontal overflow: `0` on every checked page
- no public AI/internal copy terms found:
  - `ai engine`
  - `openai`
  - `anthropic`
  - `gemini`
  - `private console`
- customer routes remain present:
  - Home: `Open the store`, `Explore services`, `View the structure`
  - Landing: `Enter the storefront`, `See the books`
  - Store: `Shop books`, `Read the library`
  - Books: `Open full library`, `Buy the bundle`

## Layout adjustments applied
- restored the older public layout direction instead of the newer storefront-heavy redesign
- preserved books, shopping, and structure pages
- compacted the mobile header navigation into a horizontal chip rail instead of a stacked full-height list
- kept mobile overflow at zero
- increased motion quality with card entrance timing, hover lift, hero panel float, and reduced-motion fallback

## Supporting files
- `E:\FOCUS_MASTER_AI_live\docs\qa_screens\home_desktop.png`
- `E:\FOCUS_MASTER_AI_live\docs\qa_screens\home_mobile.png`
- `E:\FOCUS_MASTER_AI_live\FOCUS_MASTER_AI\docs\pipeline_status_2026-05-07.md`
