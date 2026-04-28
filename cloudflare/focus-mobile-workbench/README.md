# Focus Mobile Workbench

Private Cloudflare-hosted mobile operator surface for Focus.

## Purpose

- Give iPhone access to a private task console without relying on the public site
- Keep lightweight workspace state on-device instead of clogging the laptop with extra artifacts
- Provide a secure session gate plus cloud-run task orchestration for approved workflows
- Offer a VS Code-inspired workbench layout, not a literal clone of proprietary VS Code internals or third-party plugins

## What it is

- A Cloudflare Worker app with static assets
- Password-gated private UI
- Mobile-first editor/workbench with:
  - stack chooser
  - prompt/workspace editor
  - plugin-bridge registry
  - task runner
  - run output panel

## What it is not

- Not a reproduction of VS Code source or marketplace plugins
- Not an unrestricted model shell
- Not a replacement for local desktop engineering when filesystem-heavy work is required

## Local development

```bash
npm install
npm run dev
```

## Required secrets

- `PRIVATE_APP_PASSWORD`
- `APP_SESSION_SECRET`

Optional:

- `OPENAI_API_KEY`
- `OPENAI_MODEL`

## Deploy

```bash
npm run deploy
```

If Cloudflare auth is not available in Wrangler yet, complete auth first and then deploy.
