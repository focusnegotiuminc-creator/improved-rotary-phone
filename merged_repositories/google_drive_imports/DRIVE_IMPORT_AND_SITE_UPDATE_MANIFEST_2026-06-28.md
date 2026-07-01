# Google Drive Import + Site Update Manifest — 2026-06-28

Branch: `focus-command-center-drive-import-2026-06-28`
Primary repo: `focusnegotiuminc-creator/improved-rotary-phone`
Source of truth: GitHub repo on `main`
Import source: Google Drive saved code, Master OS documents, public-site assets, and upcoming user-uploaded photos

## Purpose
This manifest prepares a safe, non-destructive import and update lane for:

1. Google Drive saved code and documents.
2. Upcoming site edits for `thefocuscorp.com` and `fluxcrave.com`.
3. New uploaded photos for each company.
4. AI-edited content and generated business copy for:
   - Flux & Crave
   - RLC Solutions
   - Focus Records LLC
   - Walden Auto
   - Walden’s Timber Carrying Construction
   - Focus Negotium Inc
   - The Focus Corp

No production deployment is authorized by this manifest. This branch is for staging, review, QA, and pull-request preparation only.

---

## Safety Rules

- Do not overwrite `main` directly.
- Do not deploy to live hosting from this branch without explicit approval.
- Do not delete Drive files, GitHub files, branches, or production assets.
- Do not import `research_cache.json`, `task_history.json`, or other cache/history files until checked for secrets, personal information, stale runtime state, and private data.
- Do not overwrite `focus_ai/scripts/build_public_site.py` from Drive. The GitHub copy appears newer/larger and remains canonical until an exact diff proves otherwise.
- Place imported Drive artifacts under a non-destructive staging folder first.
- Keep all generated copy labeled as draft until approved.
- New uploaded photos must be classified by company, usage rights, page destination, crop ratio, and alt text before being inserted into site pages.

---

## Primary GitHub Codebase

Repository: `focusnegotiuminc-creator/improved-rotary-phone`
Default branch: `main`
Working branch: `focus-command-center-drive-import-2026-06-28`
Known live/homepage reference: `https://improved-rotary-phone-two.vercel.app`

Important paths already identified:

- `app.py`
- `app.js`
- `index.html`
- `FOCUS_MASTER_AI/`
- `focus_ai/`
- `engine/`
- `engines/`
- `automation/`
- `pipelines/`
- `integrations/`
- `scripts/`
- `focus_ai/scripts/build_public_site.py`
- `focus_ai/scripts/deploy_infinityfree.py`
- `focus_ai/scripts/deploy_local_live.py`
- `focus_ai/scripts/deploy_replit.py`
- `focus_ai/scripts/deploy_wordpress_theme.py`
- `focus_ai/scripts/github_ops.py`
- `focus_ai/scripts/sync_drive_assets.py`
- `focus_ai/scripts/verify_live_app.py`
- `focus_ai/scripts/verify_visuals.py`
- `scripts/verify_thefocuscorp_public.py`

---

## Google Drive Source Manifest

Drive files discovered as import candidates:

| Drive file | Type | Intended review target |
|---|---|---|
| `build_public_site.py` | Python | Compare only against `focus_ai/scripts/build_public_site.py` |
| `verify_thefocuscorp_public.py` | Python | Compare with `scripts/verify_thefocuscorp_public.py` and verification scripts |
| `openai_client.py` | Python | Review for reusable API client logic; check secrets before import |
| `test_openai_client.py` | Python test | Stage under tests after review |
| `test_focus_master_business_os.py` | Python test | Stage under tests after review |
| `test_build_public_site.py` | Python test | Stage under tests after review |
| `publish_ebooks.py` | Python script | Compare with ebook/publishing scripts |
| `export_focus_books.py` | Python script | Compare with ebook/export scripts |
| `prompt_studio.py` | Python script | Candidate for prompt tooling |
| `business_os.json` | JSON config | Review for secrets/private data before import |
| `store_catalog.json` | JSON config | Candidate for public product/site catalog after review |
| `research_cache.json` | JSON cache | Do not import until privacy/staleness review |
| `task_history.json` | JSON history | Do not import until privacy/staleness review |
| `focus-negotium.html` | HTML | Compare with generated/public site templates |
| `focus-records.html` | HTML | Compare with generated/public site templates |
| `thefocuscorp_public_qa_rendered.md` | Markdown QA | Stage under reports after review |
| `thefocuscorp_public_qa_rendered.json` | JSON QA | Stage under reports after review |
| `pipeline_status_2026-05-07.md` | Markdown status | Stage under reports after review |
| `system_quality_review_2026-05-07.md` | Markdown QA | Stage under reports after review |
| `focus_public_site` | Folder | Review as public-site asset folder |
| `GitHub` | Folder | Review as repo/export source folder |

Drive retrieve actions provided metadata/download links, but raw code content was not directly exposed through the basic retrieve-by-ID action. Exact merge requires content download/export or authenticated file retrieval before diffing.

---

## Photo Upload Intake Plan

When photos are uploaded, classify each photo by:

1. Company/brand:
   - Flux & Crave
   - RLC Solutions
   - Focus Records LLC
   - Walden Auto
   - Walden’s Timber Carrying Construction
   - Focus Negotium Inc
   - The Focus Corp
2. Intended site:
   - `thefocuscorp.com`
   - `fluxcrave.com`
   - both
3. Page destination:
   - home hero
   - services
   - gallery
   - about/history
   - work progress
   - menu/food item
   - repair/project proof
   - team/brand story
4. AI edit type:
   - lighting correction
   - crop/straighten
   - background cleanup
   - brand color treatment
   - web compression
   - alt text generation
   - caption generation
   - before/after pairing
5. Required output formats:
   - web JPG/WebP
   - social square
   - vertical reel/story crop
   - thumbnail
   - print-ready export only if requested

---

## Site Update Prep — thefocuscorp.com

Planned update areas:

- The Focus Corp umbrella homepage
- Focus Negotium Inc business automation/command center section
- RLC Solutions construction/project support section
- Focus Records LLC music/media/creative ownership section
- Walden Auto repair/documentation/inspection-readiness section
- Walden’s Timber Carrying Construction field-service section
- Work progress/history timeline
- Photo gallery and proof-of-work sections
- Cross-links to Flux & Crave and other Focus businesses

Required content blocks:

- hero headline
- short brand statement
- services overview
- project history/work progress
- proof/gallery section
- call-to-action
- SEO title/meta description
- image alt text
- JSON-LD schema where appropriate

---

## Site Update Prep — fluxcrave.com

Planned update areas:

- home hero
- menu/food visuals
- specials/content drops
- location/local brand story
- work progress/history
- food gallery
- social media CTA
- Due2Live/Focus ecosystem cross-link if appropriate

Required content blocks:

- hero headline
- menu teaser copy
- food item captions
- brand story
- local Hannibal positioning
- gallery alt text
- social CTA
- SEO title/meta description

---

## Draft Content Lanes

### Flux & Crave
Theme: bold food, local flavor, visual menu drops, Hannibal community energy.

### RLC Solutions
Theme: construction knowledge, reliable project support, property improvement, planning and execution.

### Focus Records LLC
Theme: independent music, artist development, ownership, rollout strategy, media production.

### Walden Auto
Theme: repair documentation, transportation reliability, estimates, inspection-readiness support.

### Walden’s Timber Carrying Construction
Theme: timber, hauling, construction-site support, field work, materials movement.

### Focus Negotium Inc
Theme: business command center, automation, documents, content systems, negotiation, CRM, operational execution.

### The Focus Corp
Theme: umbrella system connecting business, AI, construction, media, food, auto, and development.

---

## Merge Ledger Template

| Source app | Source file/folder | Source ID/path | Target repo path | Status | Risk | Action needed |
|---|---|---|---|---|---|---|
| Google Drive | `build_public_site.py` | `1X3up7c4RKH34VadAY-0LpzeC2YmHPMPX` | `focus_ai/scripts/build_public_site.py` | compare only | overwrite risk | retrieve content and diff |
| Google Drive | `verify_thefocuscorp_public.py` | `1OPti9qyNlEB0PfWMgREG3wZRYusi3oBW` | `scripts/verify_thefocuscorp_public.py` | compare only | duplicate/version risk | retrieve content and diff |
| Google Drive | `business_os.json` | `17RoDm5diqIoNp5ICz0z26v1Zgr5Mm9V8` | `focus_ai/config/` or `memory/` | hold | secrets/PII risk | inspect before import |
| Google Drive | `focus-negotium.html` | `1NHUb6MbBRMLFP49OqWjnplMaVGTWAetq` | `focus_ai/site/` or templates | hold | stale generated HTML | compare against generator output |
| Google Drive | `focus-records.html` | `1awT5BcIYYym8EFm9xrMjzhNwV8Jp_cnT` | `focus_ai/site/` or templates | hold | stale generated HTML | compare against generator output |
| User upload | company photos | pending | `static/`, `focus_ai/site/assets/`, or generated output | pending | rights/quality/crop risk | classify after upload |

---

## Immediate Next Steps

1. Upload photos grouped by company.
2. For each photo, assign brand/page/use case.
3. Generate alt text, captions, gallery copy, and update notes.
4. Retrieve actual Drive file contents where possible.
5. Build exact diff ledger between Drive code and GitHub code.
6. Stage safe imports under `merged_repositories/google_drive_imports/`.
7. Create PR only after review.
8. Deploy only after explicit approval.
