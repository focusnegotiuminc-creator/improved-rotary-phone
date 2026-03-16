# Focus AI Engine

A local, device-controllable Sacred AI workflow system with 11 stages, prompt packs, publishing checklists, draft long-form content assets, and a visual preview page for design verification.

## Quick commands
- `make run` — run all workflow stages
- `make stage N=8` — run a specific stage
- `make qa` — syntax checks for scripts
- `make visual-check` — verify visual and phone-number content requirements
- `make publish` — publish eBooks as local HTML pages to `focus_ai/published/ebooks/`
- `make public-build` — build a public-ready site bundle in `focus_ai/published/public_site/`

## Public deployment
- GitHub Actions workflow `.github/workflows/publish-pages.yml` builds and deploys `focus_ai/published/public_site/` to GitHub Pages on push.
- Public bundle includes visual preview homepage and published eBook library links.
