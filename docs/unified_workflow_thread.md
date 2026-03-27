# Unified Workflow Thread

## Purpose

This document is the single handoff point for future chats, local work, and deployment sessions. It combines the current deployment truth, security rules, operating commands, and the company-routing model for Focus Records LLC, Royal Lee Construction Solutions LLC, and Focus Negotium Inc.

## Current Reality

- GitHub Actions is configured correctly at the repository level.
- Repository secrets and variables are present.
- Private and public visibility do not remove the current account-level GitHub billing lock.
- Direct local deployment to InfinityFree works and remains the current reliable path.

## Security Rules

- Do not paste secret values into chat threads.
- Do not duplicate secret values into repo files, Slack messages, or issue threads.
- Keep GitHub repository secrets as the source of truth for GitHub-based deployment.
- Keep local `.env` values only in ignored files.
- Future chats should reference the secret names in `docs/secret_registry.md`, not the secret values.

## Recommended Free Operating Model

If the goal is to keep source private while still publishing site changes publicly, use this model:

1. Keep source development in the private `Focus--Master` repository and on the local device.
2. Build public artifacts with `make public-build`.
3. Deploy only the built output to the live host with `make deploy-thefocuscorp` or `python3 focus_ai/scripts/github_ops.py go-live --deploy`.
4. If a separate public repo is ever needed, publish only built static artifacts there, not source code or secret-bearing workflow files.

## Codespaces Reality

- A public repository makes the code visible to the world.
- Codespaces does not hide source code if the repository itself is public.
- A private-repo Codespace still depends on GitHub account access and billing state.
- For now, the free and safe development path is local editing on this device plus direct deployment of built artifacts.

## Company Routing

- Focus Records LLC: creative direction, release strategy, media systems, audience rollout.
- Royal Lee Construction Solutions LLC: sacred-geometry build consulting, layout strategy, construction planning.
- Focus Negotium Inc: negotiation, automation design, monetization systems, business operations.
- Alexis Rogers: primary routing contact for meetings, product questions, and service selection.

## Site Flow

- Homepage: sacred geometry landing page with company routing.
- Booking page: direct entry for Alexis Rogers.
- Services page: compare the three company paths.
- Products page: digital products plus manual purchase routing while payment setup remains separate.
- Funnel pages: lead capture, delivery, low-ticket offer, upsell, high-ticket offer, and email sequence.

## Commands

```bash
make qa
make visual-check
make public-build
make deploy-thefocuscorp
```

## External Tools

- GitHub: version control, secrets, workflow storage.
- Stripe: future payment processor when product catalog and pricing are finalized.
- Slack: future notifications and routing summaries once a target workspace/channel is chosen.
- Figma and Canva: future design system and asset workflows as needed.
- Cloudflare: future DNS, edge, or Worker-based routing if the domain stack moves there.
- Linear: future project tracking only if an issue/project structure is desired.

## Next Safe Expansion

- Add a real booking integration when a scheduling platform is chosen.
- Add payment links when a live Stripe catalog is approved.
- Keep source private and publish only built outputs until the billing lock is cleared and GitHub Actions is usable again.
