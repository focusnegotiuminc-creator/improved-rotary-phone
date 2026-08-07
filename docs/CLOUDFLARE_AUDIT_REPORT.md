# Cloudflare audit report

Generated from repo-visible files on 2026-07-07. No live Cloudflare audit logs or API secrets were available in tracked files.

## Available evidence
- `reports/2026-03-27_cloudflare_token_status.md` says prior masked token checks verified 11 active tokens, raw token values were not written, `thefocuscorp.com` did not appear in tested zone lookup results, and R2/Workers checks were limited by permissions or account setup.
- `docs/live_deployment_fix_2026-05-18.md` says Cloudflare API access was not authenticated in that session, so DNS/proxy and edge SSL changes could not be made.

## Missing-data report
To complete a live audit, provide a token with least-privilege access for account read, zone read, Workers read, Pages read, KV read, D1 read, R2 read, deployments read, and audit logs read. Set values only in a local `.env` or deployment secret store.

## Repo search terms covered
Cloudflare, thefocuscorp, theFocusCorp@proton.me, wrangler, workers, pages, r2, d1, kv, audit, token, zone.
