# Focus AI Figma Design System Rules

Prepared: 2026-03-27

This document maps the current codebase into a Figma-ready implementation guide so design work stays aligned with the live portal, the customer iPhone app, and the Focus AI business operating system.

## 1. Token Definitions

Primary token source:
- `focus_ai/config/business_os.json`

Runtime surfaces:
- Web CSS tokens in `focus_ai/site/visual_preview.css`
- iOS theme tokens in `ios/FocusAIApp/App/Theme/FocusTheme.swift`

Current token categories:
- colors
- typography
- spacing
- motion
- motifs
- company accent variants

Example token structure from `focus_ai/config/business_os.json`:

```json
"colors": {
  "bg_900": "#050812",
  "bg_800": "#0A1329",
  "panel": "#0E1730",
  "ink": "#F6F8FF",
  "muted": "#C2CCE5",
  "gold": "#F2C96D",
  "teal": "#3EE4D6",
  "sky": "#7CC8FF",
  "ember": "#FF9B68",
  "line": "#7AA8FF"
}
```

Web token usage pattern from `focus_ai/site/visual_preview.css`:

```css
:root {
  --bg-900: #050812;
  --bg-800: #0a1329;
  --panel: rgba(12, 22, 44, 0.82);
  --ink: #f6f8ff;
  --muted: #c2cce5;
  --gold: #f2c96d;
  --teal: #3ee4d6;
  --sky: #7cc8ff;
}
```

iOS token usage pattern from `ios/FocusAIApp/App/Theme/FocusTheme.swift`:

```swift
enum FocusTheme {
    static let background = Color(red: 5 / 255, green: 8 / 255, blue: 18 / 255)
    static let panel = Color(red: 14 / 255, green: 23 / 255, blue: 48 / 255)
    static let ink = Color(red: 246 / 255, green: 248 / 255, blue: 1.0)
    static let gold = Color(red: 242 / 255, green: 201 / 255, blue: 109 / 255)
}
```

Figma rule:
- Treat `focus_ai/config/business_os.json` as the token source of truth.
- Mirror those tokens into Figma variables before creating new component styling.
- Keep the three company accent variants as theme overlays, not independent design systems.

## 2. Component Library

Current shared component vocabulary:
- `hero`
- `offer-card`
- `cta-row`
- `company-spotlight`
- `workflow-stage-grid`
- `intake-panel`
- `dashboard-strip`

Declared in:
- `focus_ai/config/business_os.json`

Web implementation surfaces:
- generated portal pages in `focus_ai/published/public_site/`
- CSS system in `focus_ai/site/visual_preview.css`

iOS implementation surfaces:
- `ios/FocusAIApp/App/Views/HomeView.swift`
- `ios/FocusAIApp/App/Views/OfferCardView.swift`
- `ios/FocusAIApp/App/Views/CompanyHighlightsView.swift`
- `ios/FocusAIApp/App/Views/IntakeFormView.swift`

SwiftUI composition pattern:

```swift
VStack(alignment: .leading, spacing: 14) {
    Text("Live Offers")
    ForEach(Array(store.offers.enumerated()), id: \\.element.id) { index, offer in
        OfferCardView(offer: offer, accent: ...)
    }
}
```

Figma rule:
- Build components in this order:
  1. foundational card shells
  2. CTA buttons
  3. offer cards
  4. company cards
  5. workflow blocks
  6. intake panels
  7. full-page hero compositions

## 3. Frameworks and Libraries

Observed frameworks:
- Python / Flask for the local operator API
- static HTML + CSS for the public portal build
- SwiftUI for the iPhone app

Key files:
- `FOCUS_MASTER_AI/api_server.py`
- `focus_ai/scripts/build_public_site.py`
- `ios/FocusAIApp/project.yml`

Styling stack:
- web: hand-authored CSS, no utility framework detected
- iOS: native SwiftUI colors, gradients, and rounded-shape composition

Figma rule:
- Do not produce React-style component assumptions.
- Design for static-site HTML/CSS on web and SwiftUI on mobile.
- Prefer layout primitives that translate cleanly into:
  - CSS grid and flexbox
  - SwiftUI `VStack`, `HStack`, `ScrollView`, and rounded cards

## 4. Asset Management

Relevant locations:
- site visuals and CSS: `focus_ai/site/`
- generated public bundle: `focus_ai/published/public_site/`
- construction package assets: `construction/rlc_office_pkg_extracted/assets/`
- iOS bundled business data: `ios/FocusAIApp/Resources/business_os.json`

Current pattern:
- source-of-truth data is JSON driven
- published web pages are generated outputs
- logos and traced sketches are stored as raster assets

Figma rule:
- Store export-ready logos with transparent backgrounds.
- Prefer named export groups for:
  - hero illustrations
  - sacred-geometry motifs
  - logo watermarks
  - social campaign crops

## 5. Icon and Symbol System

Current motif language is geometric rather than icon-heavy.

Observed visual symbols:
- orbital rings
- hexagonal linework
- sacred-geometry overlays
- gold/teal/sky beams

Source references:
- `focus_ai/site/visual_preview.html`
- `focus_ai/site/visual_preview.css`

Figma rule:
- Build a small symbolic library instead of a generic icon pack.
- Name symbols by motif and role:
  - `motif/orbital-ring`
  - `motif/hex-grid`
  - `motif/beam-vertical`
  - `brand/watermark-rlc`

## 6. Styling Approach

Web styling approach:
- global CSS file with root custom properties
- expressive gradients and layered background atmospherics
- direct component classes

Example:

```css
.btn {
  background: linear-gradient(115deg, var(--gold), #ffd88a 50%, var(--coral));
  border-radius: 12px;
}
```

Responsive approach:
- `clamp(...)` for type and spacing
- CSS grid for main split layouts
- flex-wrap for CTA rows and quick links

iOS styling approach:
- centralized theme constants
- rounded panel cards
- gradient CTA emphasis

Figma rule:
- Preserve the high-contrast poster composition.
- Avoid flat white canvases and generic SaaS cards.
- Keep background atmosphere, motion intent, and sacred-geometry overlays as first-class design elements.

## 7. Project Structure

Top-level organization:
- `focus_ai/` public portal, site generation, funnel assets
- `FOCUS_MASTER_AI/` operator API, workflow orchestration, runtime data
- `ios/FocusAIApp/` customer-facing mobile app
- `construction/` bid-package and blueprint work
- `marketing/` launch and campaign templates

Pattern guidance:
- Data-driven public experiences should originate from `focus_ai/config/business_os.json`.
- New visual work should map to a clear runtime surface:
  - web page
  - iOS screen
  - PDF/report asset
  - marketing creative

## 8. Figma-to-Code Rules

1. Start from shared tokens, never from ad hoc hex values.
2. Reuse one card family across offer, company, workflow, and intake blocks.
3. Maintain the sacred-geometry motif as an accent layer, not as dense decorative clutter.
4. Preserve the typography pairing:
   - display: Cormorant Garamond
   - body/UI: Space Grotesk
5. Keep mobile screens visually consistent with:
   - `HomeView.swift`
   - `OfferCardView.swift`
   - `FocusTheme.swift`
6. When designing for the public portal, validate against:
   - `focus_ai/published/public_site/index.html`
   - `focus_ai/published/public_site/products.html`
   - `focus_ai/published/public_site/business_os.html`

## 9. Immediate Figma Build Targets

Priority 1:
- token variables for color, type, spacing, motion labels
- offer card component set
- CTA button component set
- company spotlight cards

Priority 2:
- homepage hero composition
- product ladder page
- business OS overview page

Priority 3:
- iPhone app home screen
- intake form flow
- library screen

## 10. Open Gaps

- No dedicated Storybook or component-doc site detected.
- Web tokens exist partly in JSON and partly in CSS; keep them synchronized manually until a formal transform pipeline is added.
- Figma marketing output via Canva still needs an explicit brand-kit decision before fully automated Canva generation can proceed.
