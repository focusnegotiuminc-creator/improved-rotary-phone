# Live Stack Report

- Timestamp (UTC): 2026-03-27T06:38:25.415435+00:00
- Secrets file loaded: yes

## Core Pipeline
- go_live: ok
- verify_visuals: ok
- build_final_system: ok
- export_replit_bundle: ok

## Engine Smoke
- orchestrator_parallel: ok (processed=10)

## API Probe
- sk-pro...f7IA: failed (http_429)
- sk-pro...NccA: failed (http_429)
- sk-pro...LboA: failed (http_429)
- sk-pro...ACYA: failed (http_429)
- sk-pro...nI4A: failed (http_429)
- sk-pro...7RAA: failed (http_429)

## GitHub PR Merge
- merge_prs: blocked (gh not authenticated)
  - detail: You are not logged into any GitHub hosts. To log in, run: gh auth login

## Deployment
- infinityfree_deploy: failed (1)
  - detail: ftplib.error_perm: 530 Login authentication failed

## Summary
- Core stack is live locally and deployment artifacts are refreshed.
