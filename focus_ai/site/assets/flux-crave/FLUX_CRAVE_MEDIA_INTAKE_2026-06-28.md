# Flux & Crave Media Intake Manifest — 2026-06-28

Branch: `focus-command-center-drive-import-2026-06-28`
Target sites: `fluxcrave.com`, `thefocuscorp.com`
Status: staged for review, optimization, and site integration. No live deployment authorized.

## Uploaded Audio Assets

### `Change your life money .mp3`
- Approx. duration: 171 seconds
- Format: MP3, stereo, 44.1 kHz
- Approx. detected tempo: 101 BPM
- Use recommendation: optional background/vibe track, brand video bed, promo loop, intro splash, or social clip.
- Web rule: do not force autoplay with sound. Use a visible play/pause button or muted-first experience.

### `Be Your Menu.mp3`
- Approx. duration: 316 seconds
- Format: MP3, stereo, 44.1 kHz
- Approx. detected tempo: 148 BPM
- Use recommendation: higher-energy menu/promo track, ordering page ambience, short reel background, launch countdown.
- Web rule: use optional user-initiated audio only. Browsers usually block autoplay with sound, and forced sound can hurt user experience.

Recommended implementation:
- Add a small Flux & Crave audio toggle: `Play Flux Vibe` / `Pause`.
- Use 30–45 second optimized clips for the website and keep full-length MP3s for video/social production.
- Add controls, preload metadata only, and include a mute option.

---

## Uploaded Image Assets

### `menu_v1_full`
- Source dimensions: 1081×1455
- Type: menu graphic / brand board
- Status: usable as reference; verify prices and hours before publishing as current menu.
- Recommended use: menu preview, downloadable menu, internal reference, brand-history page.
- Notes: Includes full Flux & Crave board, address, phone, QR, hours, sauces, Little Cravers section, and menu prices. Price conflict exists with another menu variant.

### `menu_v2_full`
- Source dimensions: 1081×1455
- Type: menu graphic / brand board
- Status: usable as reference; verify prices and hours before publishing as current menu.
- Recommended use: menu preview or menu page after confirming wing pricing and hours.
- Notes: Contains a different 5-piece wing price than menu_v1. Do not publish both as current menus without clarification.

### `buffalo_wings_photo`
- Source dimensions: 1152×1536
- Type: real food photo
- Status: public usable
- Recommended use: food gallery, wings hero block, social post, menu detail card, “Crave the Wings” section.
- Suggested alt text: Sauced chicken wings in a takeout box from Flux & Crave.
- Suggested caption: Bold wings, sauced hot, packed fresh, and ready to crave.

### `menu_board_photo_blurry`
- Source dimensions: 960×1297
- Type: menu-board photo
- Status: reference only
- Recommended use: internal proof/history only unless sharpened or replaced.
- Notes: Too blurry for main website menu use.

### `neon_chicken_wings_sign`
- Source dimensions: 1152×1536
- Type: interior brand/atmosphere photo
- Status: public usable
- Recommended use: brand story, inside-the-spot gallery, Route 66 / Phillips 61 atmosphere section.
- Suggested alt text: Neon chicken wings sign inside the Flux & Crave food spot.
- Suggested caption: Inside the spot — hot wings, bold flavor, and Flux energy.

### `route66_open_24h_screenshot`
- Source dimensions: 230×405
- Type: promo screenshot
- Status: needs crop/rebuild
- Recommended use: reference for a rebuilt Route 66 / Phillips 61 promo graphic.
- Notes: Too small/partial for direct site hero use.

### `uniform_detail_screenshot`
- Source dimensions: 709×1536
- Type: apparel/detail promo screenshot
- Status: reference only until rebuilt
- Recommended use: brand-merch concept, staff/uniform reference.
- Notes: Contains mobile UI overlay buttons; do not publish as-is.

### `grab_and_go_screenshot`
- Source dimensions: 709×1536
- Type: grab-and-go promo screenshot
- Status: reference only until rebuilt
- Recommended use: ad copy and visual direction.
- Notes: Contains mobile UI overlay buttons; do not publish as-is.

### `delivery_bag_screenshot`
- Source dimensions: 709×1536
- Type: delivery/carryout promo screenshot
- Status: reference only until rebuilt
- Recommended use: delivery/carryout concept, bag design idea, site copy.
- Notes: Contains mobile UI overlay buttons; do not publish as-is.

### `brand_board_flux_crave`
- Source dimensions: 768×1365
- Type: brand board / visual identity collage
- Status: public usable with review
- Recommended use: brand-history section, investor/partner page, internal design direction, social carousel.
- Suggested alt text: Flux & Crave brand board showing menu graphics, Route 66 imagery, merchandise, and food packaging concepts.

---

## Site Content Direction

### FluxCrave.com homepage hero
Headline options:
1. `Bold Flavor. Made Fresh. Crave More.`
2. `Route 66 Flavor, Fresh From the Spot.`
3. `Sauce Is Our Super Power.`

Subcopy:
`Flux & Crave serves bold wings, wraps, bowls, sauces, and crave-worthy carryout inside Phillips 61 on Route 66 in Hannibal, Missouri.`

CTA options:
- `Order Online`
- `View Menu`
- `Find Us Inside Phillips 61`

### Gallery section
Use public-ready assets first:
- `buffalo_wings_photo`
- `neon_chicken_wings_sign`
- `brand_board_flux_crave`

Hold/rebuild before publishing:
- screenshots with UI overlays
- blurry menu-board photo
- partial Route 66 promo screenshot

### History / work progress section
Suggested copy:
`Flux & Crave is building a bold food brand from the inside out — menu concepts, sauce identity, Route 66 energy, carryout visuals, and real food photography from inside the Phillips 61 food spot in Hannibal.`

---

## Technical Implementation Notes

Recommended asset structure:

```text
focus_ai/site/assets/flux-crave/images/
focus_ai/site/assets/flux-crave/audio/
focus_ai/site/assets/flux-crave/raw/
focus_ai/site/assets/flux-crave/reference-only/
```

Recommended website audio markup:

```html
<section class="flux-audio-bar" aria-label="Flux & Crave background audio">
  <button id="fluxAudioToggle" type="button">Play Flux Vibe</button>
  <audio id="fluxVibeAudio" preload="metadata" loop>
    <source src="/assets/flux-crave/audio/be-your-menu-background-preview-32s.mp3" type="audio/mpeg">
  </audio>
</section>
```

Recommended JavaScript behavior:

```js
const button = document.getElementById('fluxAudioToggle');
const audio = document.getElementById('fluxVibeAudio');
button?.addEventListener('click', async () => {
  if (audio.paused) {
    await audio.play();
    button.textContent = 'Pause Flux Vibe';
  } else {
    audio.pause();
    button.textContent = 'Play Flux Vibe';
  }
});
```

Do not autoplay sound on page load.

---

## Next Action Required

1. Confirm current menu prices and hours.
2. Confirm whether Phillips 61 / Route 66 wording is approved for public site copy.
3. Upload or approve cleaned final versions of screenshots with UI overlays removed.
4. Add optimized assets to the branch using GitHub upload, direct local commit, or Drive sync.
5. Update `build_public_site.py` only after asset filenames and page placement are confirmed.
