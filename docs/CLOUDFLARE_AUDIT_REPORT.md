# Cloudflare Audit Report

Generated from repository and Drive-imported file search for: Cloudflare, thefocuscorp, theFocusCorp@proton.me, wrangler, workers, pages, r2, d1, kv, audit, token, zone.

## Available findings
- Existing report `reports/2026-03-27_cloudflare_token_status.md` says 11 pasted Cloudflare API tokens were verified active, raw token values were not written to tracked files, and pasted tokens should be treated as exposed.
- Existing report `reports/2026-03-27_wordpress_root_fix.md` says `thefocuscorp.com` did not appear in the tested Cloudflare account zone lookup.
- Repository documentation references GitHub Pages, InfinityFree, Replit, token placeholders, and a policy to never commit raw credentials.

## Missing data
Live Cloudflare audit logs were not available in tracked files. To fetch them, provide a runtime `CLOUDFLARE_API_TOKEN` with account audit-log read permissions and the correct `CLOUDFLARE_ACCOUNT_ID`. Zone, Workers, Pages, KV, D1, and R2 checks require the matching Cloudflare account, zone, and resource IDs.

## Recommendation
Rotate any Cloudflare tokens previously pasted into chat, create least-privilege API tokens for CI, and store them only in Cloudflare/GitHub/Vercel secret managers.
