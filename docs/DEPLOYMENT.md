# Deployment

Workflow: INPUT → CLASSIFY → ROUTE → PLAN → EXECUTE → TEST → QUALITY CHECK → DEPLOY CHECK → LOG → REPORT.

## Cloudflare primary
Use `wrangler.toml` environments: default dev, `staging`, and `production`. Confirm before any production deploy.

## Vercel fallback
`vercel.json` provides a static/Node-compatible fallback. Use Vercel secrets for runtime values.

## Render / Fly.io notes
Render can deploy the same build output as a static site or web service. Fly.io can run a containerized Node server if one is added; keep secrets in platform secret stores.

## Quality gates
Preflight, code review, connector health, secret scan, tests, deployment dry-run, post-deploy smoke checks, audit trail logging, and rollback notes are required for every release.
