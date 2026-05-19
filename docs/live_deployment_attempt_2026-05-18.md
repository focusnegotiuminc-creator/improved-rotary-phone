# Live Deployment Attempt — 2026-05-18

## Result
Local publish/build completed successfully, but live deployment did not complete.

## Completed
- Published 5 eBooks into `focus_ai/published/ebooks`.
- Built the public site into `focus_ai/published/public_site`.
- Verified local generated pages through `scripts/verify_thefocuscorp_public.py`.
- Ran test suite: `10 passed`.

## Blocker
- FTP upload to InfinityFree failed because the configured FTP host did not resolve: `getaddrinfo failed`.
- Live endpoint checks then failed due TLS/certificate verification errors.

## Safety note
Deployment credentials were loaded from the local env file but were not printed or written into this report.

## Next retry
Retry `focus_ai/scripts/deploy_local_live.py --env-file .secrets/focus_master.env` after confirming DNS/network access and the live certificate state for `thefocuscorp.com`.
