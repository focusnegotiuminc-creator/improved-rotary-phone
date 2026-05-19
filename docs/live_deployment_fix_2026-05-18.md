# Live Deployment Fix — 2026-05-18

## What was fixed
- FTP DNS path: the default local resolver could not resolve `ftpupload.net`, even though public DNS resolved it.
- Deploy proxy path: this Codex shell had HTTP/HTTPS proxy variables pointed at a dead local proxy, which caused live endpoint verification to fail through `127.0.0.1:9`.
- Deployment script resilience: `deploy_infinityfree.py` now adds fallback DNS IP candidates when local DNS fails, and `deploy_local_live.py` clears the known-broken local proxy values before deployment.

## Deployment result
A live FTP deployment succeeded during this pass after disabling the broken proxy variables and using resolved InfinityFree FTP IP fallback routing.

Result:
- Published 5 eBooks.
- Built public site bundle.
- Uploaded 55 files and 8 directories to the configured `thefocuscorp.com/htdocs` path.

## Live verification
- `verify_live_app.py` passed with TLS verification skipped.
- Headless Edge confirmed the live homepage renders the new public content after InfinityFree's JavaScript gate, including:
  - The Focus Corporation restored layout language
  - Focus Negotium Inc
  - Focus Records LLC
  - Royal Lee Construction Solutions LLC
  - Public phone route `2172576222`
  - Quincy Veterans Home / Wentzville portfolio references

## Remaining cert blocker
The origin certificate for `thefocuscorp.com` and `www.thefocuscorp.com` still presents as self-signed from direct HTTPS checks. That is a hosting/control-panel or DNS-proxy issue, not an FTP file-upload issue.

Cloudflare API access was not authenticated in this session, so I could not switch DNS/proxy mode or enable Cloudflare edge SSL from here.

## Required next action for real certificate fix
Use one of these hosting-level paths:
1. Enable/renew the SSL certificate in the InfinityFree control panel for both `thefocuscorp.com` and `www.thefocuscorp.com`; or
2. Move DNS to an authenticated Cloudflare zone and proxy `thefocuscorp.com` / `www` through Cloudflare with an edge certificate enabled.

## Security note
A local env audit exposed existing WordPress/hosting password values in tool output earlier in the session. Rotate those credentials after this deployment pass.
