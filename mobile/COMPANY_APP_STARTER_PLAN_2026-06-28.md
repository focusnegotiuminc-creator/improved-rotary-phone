# Company App Starter Plan — 2026-06-28

Branch: `focus-command-center-drive-import-2026-06-28`
Status: planning and staging only. No App Store or Google Play registration has been completed from this file.

## Proposed Company App IDs

| Company | iOS Bundle ID | Android Package Name | App Name | Initial Purpose |
|---|---|---|---|---|
| The Focus Corp | `com.thefocuscorp.app` | `com.thefocuscorp.app` | The Focus Corp | company portal, services, updates, brand directory |
| Focus Negotium Inc | `com.focusnegotium.app` | `com.focusnegotium.app` | Focus Negotium | business command center, CRM, documents, automation dashboard |
| Flux & Crave | `com.fluxcrave.app` | `com.fluxcrave.app` | Flux & Crave | menu, ordering link, specials, loyalty, location, gallery, music/vibe player |
| RLC Solutions | `com.rlcsolutions.app` | `com.rlcsolutions.app` | RLC Solutions | construction services, estimates, project progress, contact forms, gallery |
| Focus Records LLC | `com.focusrecords.app` | `com.focusrecords.app` | Focus Records | artist/media hub, releases, videos, booking/contact, rollout calendar |
| Walden Auto | `com.waldenauto.app` | `com.waldenauto.app` | Walden Auto | repair estimate intake, service gallery, inspection-readiness documentation |
| Walden’s Timber Carrying Construction | `com.waldenstimber.app` | `com.waldenstimber.app` | Walden’s Timber | timber, hauling, construction support, project photos, quote requests |

Official registration requires the correct Apple Developer and Google Play Console accounts.

---

## Recommended Mobile Folder Structure

```text
mobile/
  shared/
    design-system/
    api-client/
    auth/
    media/
  apps/
    the-focus-corp/
    focus-negotium/
    flux-crave/
    rlc-solutions/
    focus-records/
    walden-auto/
    waldens-timber/
```

---

## Shared App Modules

- company profile
- service catalog
- gallery/photos
- contact form
- lead intake
- notification preferences
- website route/webview support
- media player for Flux & Crave
- admin-editable content source later

---

## Flux & Crave App v1

Priority features:

1. Home screen with Flux & Crave hero.
2. Menu preview.
3. Order Online link.
4. Location card.
5. Food gallery.
6. Sauce list.
7. Specials page.
8. Optional Flux audio vibe player using user-initiated playback.
9. Push-ready structure for specials and drops.
10. Basic loyalty placeholder.

---

## The Focus Corp App v1

Priority features:

1. Umbrella company landing page.
2. Business directory.
3. Focus Negotium service intake.
4. RLC Solutions project inquiry.
5. Focus Records media/artist page.
6. Walden Auto service request.
7. Walden’s Timber quote request.
8. News/work-progress timeline.
9. Contact/lead routing.

---

## Engineering Next Steps

1. Confirm final company names and domains.
2. Confirm developer account access.
3. Create app folders under `mobile/apps/`.
4. Generate a shared company config file.
5. Build Flux & Crave as the pilot app.
6. Build The Focus Corp as the umbrella app.
7. Generate app icons from approved logos.
8. Prepare store listing drafts after screenshots and privacy policy are ready.
