# Focus Mobile Workbench QA Report

Generated: 2026-04-28T19:59:56.384034+00:00
Base URL: `https://focus-mobile-workbench.thefocuscorp.workers.dev`

| Check | Result | Detail |
| --- | --- | --- |
| unauthenticated status gate | PASS | status=401 |
| session login | PASS | status=200 |
| authenticated status payload | PASS | status=200, stacks=6, bridges=6 |
| fallback run execution | PASS | status=200, provider=fallback |
| live provider run execution | PASS | status=200, provider=workers_ai, mode=live |
