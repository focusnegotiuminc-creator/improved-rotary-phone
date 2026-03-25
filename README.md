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
