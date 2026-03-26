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
- `make public-build` — build a public-ready site bundle in `focus_ai/published/public_site/`
- `make deploy-infinityfree` — deploy the public bundle to InfinityFree over FTP
- `make replit-export` — export AI engine + prompt bundle for a Replit app
- `make full-check` — run a full local verification pass (compile, tests, engine, visual check, publish, public build, Replit export)
- `make backup` — create a timestamped backup archive in `focus_ai/backups/`
- `make verify-live` — verify deployed app endpoints using `FOCUS_APP_URL`
- `make merge-prs` — merge all currently open GitHub pull requests via `gh` CLI
- `make go-live` — run engine + publish + public build in sequence
- `make install-gh` — attempt to install GitHub CLI and print proxy/tunnel fallback instructions on failure
- `make unblock-live` — open an external SSH SOCKS bridge, install gh, merge PRs, and run go-live
- `make setup-autopilot` — one-command bootstrap: refresh remotes, install gh, and start a background tmux auto-runner

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
5. Optional: set `FOCUS_APP_PATHS` (comma-separated) and `FOCUS_REQUIRE_ALL_PATHS=0` if you only need partial endpoint success checks.

## Where to find your books
- Markdown source books: `focus_ai/ebooks/`
- Published HTML books: `focus_ai/published/ebooks/`
- Book index page: `focus_ai/published/ebooks/index.html`

## Credentials and backup workflow
- Store credentials as environment variables (never commit passwords to git).
- Optional local `.env` files should be ignored by git.
- Run `make backup` before major edits or deploys to generate a timestamped archive in `focus_ai/backups/`.


### Example live check
`FOCUS_APP_URL="https://thefocuscorp.com" FOCUS_APP_PATHS="/,/wp-admin" make verify-live`
## GitHub merge + 403 troubleshooting
Use `make install-gh` first to bootstrap GitHub CLI in fresh environments, then run `make merge-prs` (or `python3 focus_ai/scripts/github_ops.py merge-prs --repo OWNER/REPO`).

If you hit outbound restrictions / 403:
- Re-auth GitHub CLI (`gh auth login`) or provide a token with `repo` scope (`GH_TOKEN`).
- Route through your approved outbound proxy or tunnel:
  - `export HTTPS_PROXY=http://<proxy-host>:<proxy-port>`
  - `export HTTP_PROXY=http://<proxy-host>:<proxy-port>`
- Connect required VPN/SSH tunnel first, then rerun merge.

To run the full engine pipeline locally after merging:
- `make go-live`
- Optional deploy step: `python3 focus_ai/scripts/github_ops.py go-live --deploy`


## External bridge environment
If this runtime is blocked by outbound 403 policies, you can bridge through an external bastion host that is reachable from here and has unrestricted egress.

1. Prepare an external host (VM/server) with SSH access and outbound internet.
2. From this environment, set bridge variables:
   - `export BASTION_SSH=user@your-bastion-host`
   - optional: `export BASTION_SSH_FLAGS="-i ~/.ssh/id_rsa -p 22"`
3. Run `make unblock-live` (or `bash focus_ai/scripts/unblock_and_live.sh --repo OWNER/REPO`).

`unblock_and_live.sh` will:
- start an SSH SOCKS tunnel (`socks5h://127.0.0.1:18080`)
- export `HTTP_PROXY`/`HTTPS_PROXY`/`ALL_PROXY`
- run GH install bootstrap
- merge open PRs
- run full go-live pipeline

Use `--no-tunnel` if you already have proxy env vars configured, or `--skip-merge` to only run the engine pipeline.


## Credential safety for bridge runs
- Never commit raw credentials (emails, passwords, private keys, tokens) into repository files.
- Provide secrets at runtime via environment variables only (`BASTION_SSH`, `SSH_KEY_FILE`, `GH_TOKEN`).
- `focus_ai/scripts/unblock_and_live.sh` will prompt for missing required connection credentials and supports key-based SSH auth with `IdentitiesOnly`.


## One-command "keep it running" setup
For your GitHub + server workflow (including Termius sessions), run:

```bash
make setup-autopilot
```

What it does:
- checks your configured git remotes
- runs `git fetch --all --prune` to re-sync all remotes
- bootstraps GitHub CLI (`gh`)
- starts a detached `tmux` loop that repeatedly runs:
  - `python3 focus_ai/scripts/github_ops.py merge-prs`
  - `python3 focus_ai/scripts/github_ops.py go-live`

Useful options:
- one-shot only (no background loop):
  - `bash focus_ai/scripts/setup_autopilot.sh --no-loop`
- custom loop interval (seconds):
  - `INTERVAL_SECONDS=300 make setup-autopilot`
- choose GitHub repo explicitly for merge calls:
  - `bash focus_ai/scripts/setup_autopilot.sh --repo OWNER/REPO`
- skip auto-merging and only keep go-live running:
  - `bash focus_ai/scripts/setup_autopilot.sh --skip-merge`

Manage background runner:
- attach logs: `tmux attach -t focus_ai_autopilot`
- stop runner: `tmux kill-session -t focus_ai_autopilot`

> Note: "permanent" means as long as your server keeps running. For true reboot persistence, launch this command from your startup profile or a systemd service.

## Multi-agent runtime (new)

A modular multi-agent runtime is available with task routing, specialized engines, pipeline stages, and JSON-backed memory.

- Entry point: `core/orchestrator.py` (`run_task`, `run_parallel`)
- Routing: `core/dispatcher.py` + `core/task_classifier.py`
- Engines: `engines/*_engine/engine.py`
- Pipelines: `pipelines/stage_1_research.py` … `pipelines/stage_10_publish.py`
- Memory: `memory/task_history.json`, `memory/research_cache.json`, `memory/vector_store/`
- Integrations: `integrations/`
