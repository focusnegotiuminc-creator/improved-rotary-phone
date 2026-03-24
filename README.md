# Focus AI Engine

A local, device-controllable Sacred AI workflow system with 11 stages, prompt packs, publishing checklists, draft long-form content assets, and a visual preview page for design verification.

## Quick commands
- `make run` — run all workflow stages
- `make stage N=8` — run a specific stage
- `make qa` — syntax checks for scripts
- `make visual-check` — verify visual and phone-number content requirements
- `make publish` — publish eBooks as local HTML pages to `focus_ai/published/ebooks/`
- `make public-build` — build a public-ready site bundle in `focus_ai/published/public_site/`
- `make deploy-infinityfree` — deploy the public bundle to InfinityFree over FTP
- `make replit-export` — export AI engine + prompt bundle for a Replit app
- `make full-check` — run a full local verification pass (compile, tests, engine, visual check, publish, public build, Replit export)
- `make backup` — create a timestamped backup archive in `focus_ai/backups/`
- `make verify-live` — verify deployed app endpoints using `FOCUS_APP_URL`

## Public deployment
- GitHub Actions workflow `.github/workflows/publish-pages.yml` builds and deploys `focus_ai/published/public_site/` to GitHub Pages on push.
- Public bundle includes visual preview homepage and published eBook library links.

## InfinityFree deployment
Set these environment variables, then run `make deploy-infinityfree`:
- `INFINITYFREE_FTP_HOST`
- `INFINITYFREE_FTP_USER`
- `INFINITYFREE_FTP_PASS`
- `INFINITYFREE_REMOTE_DIR` (optional, defaults to `htdocs`)

## Replit bundle
Run `make replit-export` to generate `focus_ai/published/replit_bundle/` with the AI engine scripts, prompt pack, workflow doc, and eBook outputs for direct import into a Replit app.

### GitHub Actions secrets (recommended)
To deploy from GitHub using previously stored repo credentials, set repository secrets:
- `INFINITYFREE_FTP_HOST`
- `INFINITYFREE_FTP_USER`
- `INFINITYFREE_FTP_PASS`
- `INFINITYFREE_REMOTE_DIR` (optional)

Then run the workflow `.github/workflows/deploy-infinityfree.yml` (manual dispatch) or push to `work/main/master`.

## How to use the app
1. Run `make full-check` to validate and build assets locally.
2. Run `make public-build` to generate the deployable site in `focus_ai/published/public_site/`.
3. Deploy with `make deploy-infinityfree` after setting FTP credentials in environment variables.
4. After deployment, run `FOCUS_APP_URL="https://your-live-url" make verify-live` to confirm live availability.

## Where to find your books
- Markdown source books: `focus_ai/ebooks/`
- Published HTML books: `focus_ai/published/ebooks/`
- Book index page: `focus_ai/published/ebooks/index.html`

## Credentials and backup workflow
- Store credentials as environment variables (never commit passwords to git).
- Optional local `.env` files should be ignored by git.
- Run `make backup` before major edits or deploys to generate a timestamped archive in `focus_ai/backups/`.
