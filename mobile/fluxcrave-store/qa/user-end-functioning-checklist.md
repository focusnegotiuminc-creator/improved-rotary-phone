# Flux & Crave User-End Functioning Checklist

Use this before Play Internal Testing, TestFlight, and public release.

## PWA install test

- iPhone Safari opens `https://www.fluxcrave.com/app/`.
- Add to Home Screen works.
- Android Chrome install prompt/Add to Home Screen works.
- App launches standalone without broken layout.
- Menu search loads from `/assets/data/menu.json`.
- Order link opens expected ordering path.
- Call button opens dialer.
- Directions opens maps.
- Offline/service worker fallback does not trap users on stale content.

## Android TWA test

- Package name is `com.fluxcrave.app`.
- Digital Asset Links JSON is deployed and validates.
- App opens without Custom Tab browser bar after verification.
- Back button behavior is reasonable.
- Internal testing install works on at least two Android devices.

## iOS TestFlight test

- App opens Flux & Crave route.
- Native Order/Call/Directions/Share actions work.
- App does not crash when network is slow/offline.
- App has enough native utility to support App Review.
- Store screenshots match current approved brand visuals.

## Approval gate

Do not submit public production release until owner approves:

- Final app name/icon.
- Screenshots.
- Privacy policy URL.
- Support/contact URL.
- Exact public store descriptions.
