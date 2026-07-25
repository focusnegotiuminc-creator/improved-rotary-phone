# Deployment

Primary target: Cloudflare Workers/Pages using `wrangler.toml` dev, staging, and production presets.

Fallback target: Vercel using `vercel.json`.

Compatibility notes:
- Render: serve the static dashboard or a Node API wrapper with environment variables injected through Render secrets.
- Fly.io: package the same app in a small Node container and map secrets through Fly secrets.

Workflow: INPUT → CLASSIFY → ROUTE → PLAN → EXECUTE → TEST → QUALITY CHECK → DEPLOY CHECK → LOG → REPORT.
