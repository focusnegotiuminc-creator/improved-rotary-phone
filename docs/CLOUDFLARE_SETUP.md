# Cloudflare setup

Cloudflare Workers/Pages is the primary deployment target. Vercel is the fallback target; Render and Fly.io can run compatible Node/static builds when Cloudflare is unavailable.

## Required environment
Copy `.env.example` to a local `.env` or platform secret store and set `CLOUDFLARE_API_TOKEN`, `CLOUDFLARE_ACCOUNT_ID`, `CLOUDFLARE_ZONE_ID`, `CLOUDFLARE_EMAIL`, `CLOUDFLARE_PROJECT_NAME`, `CLOUDFLARE_KV_NAMESPACE_ID`, `CLOUDFLARE_D1_DATABASE_ID`, and `CLOUDFLARE_R2_BUCKET`. Never commit real values.

## Profiles
- `config/cloudflare.profile.greatmachevilli.ts`: greatmachevilli account profile.
- `config/cloudflare.profile.focuscorp.ts`: FocusCorp profile with related business emails.

## Checks
Run token verification, account lookup, zone lookup, Workers subdomain check, Pages project check, KV, D1, R2, deployment status, and audit-log fetch through `CloudflareConnector.runHealthAudit()`.
