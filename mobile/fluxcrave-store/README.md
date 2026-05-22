# Flux & Crave Store Wrapper Readiness

This folder prepares Flux & Crave for Android and iOS store testing while preserving the current free web-app path:

- Live app: https://www.fluxcrave.com/app/
- Public PWA manifest: https://www.fluxcrave.com/manifest.webmanifest
- Android recommended route: Trusted Web Activity (TWA) generated with Bubblewrap.
- iOS recommended route: SwiftUI + WKWebView shell with native quick actions, not just a bare website wrapper.

## Why two approaches?

Android supports store-grade PWA wrapping through Trusted Web Activity when domain ownership is proven with Digital Asset Links.
Apple App Review requires the app to feel useful and app-like beyond a repackaged website, so the iOS shell should include native quick actions, offline fallback, call/directions, share, and owner-approved update surfaces.

## Current build status

Prepared locally:

- Android TWA configuration template.
- Digital Asset Links template.
- iOS SwiftUI wrapper scaffold.
- Store listing draft.
- Privacy policy draft.
- User-end QA checklist.

Blocked until account/hardware steps:

- Google Play Console account and signing key SHA-256.
- Apple Developer account/team ID and Mac/Xcode build environment.
- Owner approval for AI-generated imagery and final screenshots.
