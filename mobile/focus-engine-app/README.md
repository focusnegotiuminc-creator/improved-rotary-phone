# Focus Engine Mobile App Plan

Developer/account note: `thegreatmachevilli@icloud.com` is the intended Apple/developer identity to use when owner is ready to sign and submit builds.

## Goal

A private mobile command center for Reginald / Focus operators that can:

- submit tasks into the Focus AI Engine;
- select business lane: Focus Negotium, Focus Records, RLC, Flux & Crave, partner company;
- run architect/builder/critic debate;
- review generated assets, code diffs, social copy, outreach drafts, and deployment plans;
- approve or reject high-impact actions;
- inspect audit logs and traffic snapshots.

## Recommended technical route

### Phase 1 — Mobile web dashboard

Use the static prototype at:

`frontend/focus-engine-command-center/index.html`

Then connect it to a local Flask/FastAPI endpoint around `focus_ai.private_engine.orchestrator`.

### Phase 2 — Private installable PWA

Add manifest + service worker, protected by login/VPN/local network rules.

### Phase 3 — Native wrappers

- Android: TWA/Capacitor wrapper.
- iOS: SwiftUI/WKWebView wrapper with native approval notifications and Face ID/local auth.

## Security rules

- Do not store model/API tokens in mobile app code.
- Mobile app calls a local/private backend.
- Use HTTPS or private tunnel.
- Require explicit confirmation before actions leave the device/workspace.
