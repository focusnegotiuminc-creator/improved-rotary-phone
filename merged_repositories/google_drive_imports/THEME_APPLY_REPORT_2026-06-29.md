# Focus Corp / Flux & Crave Theme Apply Report — 2026-06-29

Branch: `focus-command-center-drive-import-2026-06-28`

## Completed

### The Focus Corp
- Replaced the staged root `index.html` with actual animated sacred-geometry homepage HTML.
- Added animated canvas particles, rotating flower/mandala geometry, aurora gradients, neon cards, orbiting command-center system nodes, mobile responsive layout, and reduced-motion support.
- Added current company lanes from prior project context:
  - Focus Negotium Inc
  - Focus Records LLC
  - RLC Solutions / Royal Lee Construction Solutions
  - Flux & Crave
  - Walden Auto
  - Walden’s Timber Carrying Construction
  - Due2Live
  - Hannibal AI Development
- Used known contact/location details only:
  - Primary contact: Alexis Rogers, 217-257-6222
  - Flux & Crave: 3827 Highway MM, Hannibal, MO; 573-719-3159; fluxcrave.com

### Flux & Crave
- Added actual animated Flux & Crave theme HTML at `focus_ai/site/flux-crave/index.html`.
- Theme direction: fire/sauce/neon/Route 66, animated sparks, sauce-gradient motion, food orbit cards, ticker strip, menu blocks, gallery-use rules, and user-controlled music dock.
- Music player is wired for:
  - `assets/audio/change-your-life-money.mp3`
  - `assets/audio/be-your-menu.mp3`
- Browser-safe behavior: no forced autoplay; music starts from the Play button.

## Important asset note

The GitHub and Google Drive connectors accepted local MP3 paths as text instead of transferring binary audio files. The theme code is wired correctly, but the actual MP3 binaries still need to be uploaded to:

- `focus_ai/site/flux-crave/assets/audio/change-your-life-money.mp3`
- `focus_ai/site/flux-crave/assets/audio/be-your-menu.mp3`

A small incorrect pointer file was created at `focus_ai/site/flux-crave/assets/flux-crave/audio/change-your-life-money.mp3`; it should be removed or ignored during cleanup.

## Not live yet

These changes are on the staging branch. Production is not updated until the branch is merged and the deployment succeeds.

## Final QA checklist before live deployment

1. Confirm final Flux & Crave menu prices and hours.
2. Confirm whether “Open 24 Hours” is approved public copy.
3. Upload the two MP3 audio binaries to the final referenced asset paths.
4. Add/crop final Flux & Crave gallery images.
5. Run mobile, desktop, accessibility, and reduced-motion QA.
6. Merge to `main` and run production deployment.