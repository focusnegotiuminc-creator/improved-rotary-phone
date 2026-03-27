# Focus AI iPhone App

This is a SwiftUI iPhone app scaffold for the customer-facing Focus AI experience.

## What it includes

- Shared offer catalog consumption from `https://thefocuscorp.com/data/business_os.json`
- Fallback bundled catalog for offline previews
- Home, library, and intake tabs
- Offer cards with external checkout handoff
- Shared company highlights and workflow messaging

## Generate an Xcode project

This scaffold uses XcodeGen so the source can stay clean in git.

```bash
xcodegen generate
open FocusAIApp.xcodeproj
```

## Notes

- Deployment target: iOS 17.0
- Bundle seed: `com.thefocuscorp.focusai`
- The app is designed to mirror the live portal and consume the same public data bundle.

