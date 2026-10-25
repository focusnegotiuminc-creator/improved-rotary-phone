# Cloudflare Setup

Cloudflare Workers/Pages is the primary deployment target for Master OS. Vercel is the fallback target; Render and Fly.io can run compatible Node/static builds when Cloudflare is unavailable.

## Required environment variables
Copy `.env.example` to your local secret store and configure `CLOUDFLARE_API_TOKEN`, `CLOUDFLARE_ACCOUNT_ID`, `CLOUDFLARE_ZONE_ID`, `CLOUDFLARE_EMAIL`, `CLOUDFLARE_PROJECT_NAME`, `CLOUDFLARE_KV_NAMESPACE_ID`, `CLOUDFLARE_D1_DATABASE_ID`, and `CLOUDFLARE_R2_BUCKET`.

## Profiles
- `config/cloudflare.profile.greatmachevilli.ts` supports `thegreatmachevilli@icloud.com`.
- `config/cloudflare.profile.focuscorp.ts` supports `theFocusCorp@proton.me`, `Focusnegotiuminc@gmail.com`, `fninc@proton.me`, and `rlcsolutions@proton.me`.

## Deployment gates
Run connector health checks, security checks for exposed secrets, code review, preflight checks, deployment confirmation, deployment status checks, and post-deploy checks before routing production traffic.
