# Android Trusted Web Activity Plan

## Build path

1. Install Node.js, Android Studio / Android command-line tools, and Bubblewrap on a build machine.
2. Initialize Bubblewrap from the live manifest:
   ```powershell
   npx @bubblewrap/cli init --manifest https://www.fluxcrave.com/manifest.webmanifest
   ```
3. Use package name: `com.fluxcrave.app`.
4. Build signed APK/AAB.
5. Add Digital Asset Links to:
   `https://www.fluxcrave.com/.well-known/assetlinks.json`
6. Upload to Google Play Internal Testing first.

## Important

Trusted Web Activity requires app/site ownership verification. If Digital Asset Links fails, Android opens the app as a Custom Tab instead of a full trusted app surface.

## Store testing sequence

- Internal testing: owner/devices only.
- Closed testing: small trusted customer set.
- Production: after screenshots, policy review, and privacy policy are finalized.
