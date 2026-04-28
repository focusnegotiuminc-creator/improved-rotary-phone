# Focus Mobile Workbench QA Report

Generated: 2026-04-28T06:15:46.162102+00:00
Base URL: `https://focus-mobile-workbench.thefocuscorp.workers.dev`

| Check | Result | Detail |
| --- | --- | --- |
| unauthenticated status gate | PASS | status=401 |
| session login | PASS | status=200 |
| authenticated status payload | PASS | status=200, stacks=6, bridges=6 |
| fallback run execution | PASS | status=200, provider=fallback |

## Notes

- Live deployment URL: `https://focus-mobile-workbench.thefocuscorp.workers.dev`
- Current Cloudflare version at verification time: `ddd70897-8109-42ea-839d-025f2a35f51a`
- The workbench is private by app-level passphrase and not linked from the public business websites.
- Current live provider posture is fallback-only because no OpenAI key is configured in the deployed worker secrets yet.
