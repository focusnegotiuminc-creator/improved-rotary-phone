# iOS Flux & Crave Wrapper Scaffold

This is a lightweight SwiftUI/WKWebView scaffold designed to test user-end function on iPhone while adding native value beyond a plain browser wrapper:

- Native navigation title.
- Native quick actions: Order, Directions, Call, Share.
- Live Flux & Crave PWA loaded with an iOS source tag.

## Build requirements

- Mac with Xcode.
- Apple Developer account.
- XcodeGen if using `project.yml`.
- Replace `DEVELOPMENT_TEAM` in `project.yml`.

## Local build

```bash
xcodegen generate
open FluxCraveApp.xcodeproj
```

Run on device first, then TestFlight.

## App Review note

Before public App Store submission, add enough native/offline utility to avoid being treated as only a repackaged website. Recommended next additions:

- Offline fallback card with menu/contact info.
- Saved favorite menu items.
- Native push notification opt-in only if owner approves.
- Native screenshots using fresh approved assets.
