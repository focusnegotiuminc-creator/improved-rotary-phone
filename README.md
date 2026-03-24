# Focus AI Engine

A local, device-controllable Sacred AI workflow system with 11 stages, prompt packs, publishing checklists, draft long-form content assets, and a visual preview page for design verification.

## Quick commands
- `make run` — run all workflow stages
- `make stage N=8` — run a specific stage
- `make qa` — syntax checks for scripts
- `make visual-check` — verify visual and phone-number content requirements
- `make publish` — publish eBooks as local HTML pages to `focus_ai/published/ebooks/`
- `make merge-gh OWNER=<github-org-or-user>` — merge all GitHub repositories from an owner into `merged_repositories/`
- `make merge-gh-dry-run OWNER=<github-org-or-user>` — preview repositories that would be merged
- `make setup-desktop-ai` — create `~/Desktop/focus-master-ai` with a runnable local AI web app

## Merge GitHub repositories and make them live
### Local/manual flow
1. Authenticate GitHub CLI: `gh auth login`
2. Run a dry run: `make merge-gh-dry-run OWNER=<github-org-or-user>`
3. Merge repositories: `make merge-gh OWNER=<github-org-or-user>`
4. Push to `main`.

### GitHub Actions “live” flow
1. Open **Actions → Merge repositories and deploy live hub**.
2. Click **Run workflow**, set `owner`, optional `repos` (comma-separated), and `squash`.
3. The workflow merges repositories, commits updates, and deploys `docs/` to GitHub Pages.


## Desktop Focus Master AI app
1. Run `make setup-desktop-ai`
2. Start the app:
   ```bash
   cd ~/Desktop/focus-master-ai
   python3 app.py
   ```
3. Open `http://127.0.0.1:8787` to use the local AI assistant.
