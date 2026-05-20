from __future__ import annotations

import csv
import html
import json
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont


ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / "marketing" / "fluxcrave" / "dist"
IMG = DIST / "assets" / "images"
ROLL = ROOT / "marketing" / "fluxcrave" / "rollout" / "2026-05-20-fresh-mobile-social-pass"
HUB = Path(r"D:\TheFocusFiles\MasterPromptOS_CommandHub") / "04_flux_crave_rollout"


def load_font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    candidates = [
        r"C:\Windows\Fonts\arialbd.ttf" if bold else r"C:\Windows\Fonts\arial.ttf",
        r"C:\Windows\Fonts\segoeuib.ttf" if bold else r"C:\Windows\Fonts\segoeui.ttf",
        r"C:\Windows\Fonts\calibrib.ttf" if bold else r"C:\Windows\Fonts\calibri.ttf",
    ]
    for candidate in candidates:
        if Path(candidate).exists():
            return ImageFont.truetype(candidate, size=size)
    return ImageFont.load_default()


def wrapped(draw: ImageDraw.ImageDraw, text: str, font: ImageFont.ImageFont, width: int) -> list[str]:
    words = text.split()
    lines: list[str] = []
    current = ""
    for word in words:
        test = f"{current} {word}".strip()
        if draw.textbbox((0, 0), test, font=font)[2] <= width or not current:
            current = test
        else:
            lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def gradient(size: tuple[int, int], top=(20, 13, 9), bottom=(112, 17, 8)) -> Image.Image:
    width, height = size
    image = Image.new("RGB", size, top)
    pixels = image.load()
    for y in range(height):
        t = y / max(1, height - 1)
        color = tuple(int(top[i] * (1 - t) + bottom[i] * t) for i in range(3))
        for x in range(width):
            pixels[x, y] = color
    return image


def rounded_rect(draw: ImageDraw.ImageDraw, xy, radius: int, fill, outline=None, width: int = 1) -> None:
    draw.rounded_rectangle(xy, radius=radius, fill=fill, outline=outline, width=width)


def fit_image(path: Path, box: tuple[int, int], crop: bool = True) -> Image.Image:
    image = Image.open(path).convert("RGBA")
    box_w, box_h = box
    scale = max(box_w / image.width, box_h / image.height) if crop else min(box_w / image.width, box_h / image.height)
    resized = image.resize((int(image.width * scale), int(image.height * scale)), Image.LANCZOS)
    canvas = Image.new("RGBA", (box_w, box_h), (0, 0, 0, 0))
    canvas.alpha_composite(resized, ((box_w - resized.width) // 2, (box_h - resized.height) // 2))
    return canvas.crop((0, 0, box_w, box_h)) if crop else canvas


def paste_rounded(base: Image.Image, image: Image.Image, xy: tuple[int, int], radius: int = 40) -> None:
    x, y = xy
    mask = Image.new("L", image.size, 0)
    draw = ImageDraw.Draw(mask)
    draw.rounded_rectangle((0, 0, image.width, image.height), radius=radius, fill=255)
    shadow = Image.new("RGBA", image.size, (0, 0, 0, 150))
    base.paste(shadow, (x + 12, y + 18), mask.filter(ImageFilter.GaussianBlur(18)))
    base.paste(image, (x, y), mask)


def draw_logo(base: Image.Image, x: int, y: int, max_w: int) -> tuple[int, int]:
    logo = Image.open(IMG / "flux-logo-wordmark.png").convert("RGBA")
    ratio = max_w / logo.width
    logo = logo.resize((int(logo.width * ratio), int(logo.height * ratio)), Image.LANCZOS)
    base.alpha_composite(logo, (x, y))
    return logo.size


def create_social(
    name: str,
    size: tuple[int, int],
    title: str,
    subtitle: str,
    hook: str,
    cta: str,
    photo: str | None = None,
    story: bool = False,
) -> Path:
    width, height = size
    base = gradient(size).convert("RGBA")
    draw = ImageDraw.Draw(base)

    for cx, cy, radius, color in [
        (int(width * 0.08), int(height * 0.12), int(width * 0.34), (255, 203, 70, 55)),
        (int(width * 0.94), int(height * 0.22), int(width * 0.42), (255, 80, 52, 58)),
        (int(width * 0.50), int(height * 0.90), int(width * 0.50), (255, 138, 36, 35)),
    ]:
        blob = Image.new("RGBA", size, (0, 0, 0, 0))
        blob_draw = ImageDraw.Draw(blob)
        blob_draw.ellipse((cx - radius, cy - radius, cx + radius, cy + radius), fill=color)
        base.alpha_composite(blob.filter(ImageFilter.GaussianBlur(55)))

    for index in range(-2, 4):
        y = int(height * 0.18) + index * int(height * 0.18)
        draw.line((-width * 0.15, y, width * 1.2, y - int(height * 0.22)), fill=(255, 203, 70, 42), width=max(18, width // 40))

    margin = int(width * 0.07)
    draw_logo(base, margin, margin, int(width * 0.43))

    tag_font = load_font(max(24, width // 34), True)
    headline_font = load_font(max(68, width // 11), True)
    subtitle_font = load_font(max(33, width // 27), False)
    cta_font = load_font(max(31, width // 28), True)
    micro_font = load_font(max(22, width // 42), False)

    if photo:
        if story:
            photo_box = (int(width * 0.82), int(height * 0.41))
            x, y = int(width * 0.09), int(height * 0.41)
        else:
            photo_box = (int(width * 0.38), int(height * 0.58))
            x, y = int(width * 0.56), int(height * 0.25)
        paste_rounded(base, fit_image(IMG / photo, photo_box, crop=True), (x, y), radius=int(width * 0.045))

    panel = (
        margin,
        int(height * 0.18 if story else height * 0.19),
        width - margin if story else int(width * 0.54),
        int(height * 0.38 if story else height * 0.84),
    )
    rounded_rect(draw, panel, int(width * 0.045), (22, 13, 9, 178), (255, 255, 255, 42), 2)
    px, py = panel[0] + int(width * 0.035), panel[1] + int(width * 0.035)

    draw.text((px, py), hook.upper(), font=tag_font, fill=(255, 203, 70, 255))
    py += int(height * 0.047)
    for line in wrapped(draw, title, headline_font, panel[2] - panel[0] - int(width * 0.07))[:4]:
        draw.text((px, py), line, font=headline_font, fill=(255, 244, 232, 255), stroke_width=1, stroke_fill=(56, 20, 7, 255))
        py += int(headline_font.size * 1.02)

    py += int(height * 0.018)
    for line in wrapped(draw, subtitle, subtitle_font, panel[2] - panel[0] - int(width * 0.07))[:4]:
        draw.text((px, py), line, font=subtitle_font, fill=(248, 213, 191, 255))
        py += int(subtitle_font.size * 1.25)

    cta_w = min(panel[2] - panel[0] - int(width * 0.07), int(width * 0.7))
    pill = (px, panel[3] - int(height * 0.09), px + cta_w, panel[3] - int(height * 0.03))
    rounded_rect(draw, pill, int(height * 0.03), (255, 203, 70, 245))
    draw.text((pill[0] + int(width * 0.03), pill[1] + int(height * 0.012)), cta, font=cta_font, fill=(25, 14, 8, 255))

    draw.text(
        (margin, height - int(height * 0.055)),
        "FluxCrave.com  •  Hannibal, MO  •  Flavor in Motion",
        font=micro_font,
        fill=(255, 231, 163, 230),
    )

    output = ROLL / name
    base.convert("RGB").save(output, quality=95)
    return output


def create_icon(size: int, filename: str) -> None:
    base = gradient((size, size), (33, 20, 12), (157, 18, 8)).convert("RGBA")
    draw = ImageDraw.Draw(base)
    draw.ellipse(
        (int(size * 0.09), int(size * 0.09), int(size * 0.91), int(size * 0.91)),
        fill=(255, 203, 70, 48),
        outline=(255, 203, 70, 210),
        width=max(3, size // 34),
    )
    draw.rounded_rectangle(
        (int(size * 0.13), int(size * 0.13), int(size * 0.87), int(size * 0.87)),
        radius=int(size * 0.18),
        outline=(255, 255, 255, 62),
        width=max(2, size // 64),
    )
    logo = Image.open(IMG / "flux-logo-wordmark.png").convert("RGBA")
    ratio = (size * 0.72) / logo.width
    logo = logo.resize((int(logo.width * ratio), int(logo.height * ratio)), Image.LANCZOS)
    base.alpha_composite(logo, ((size - logo.width) // 2, int(size * 0.40)))
    font = load_font(max(18, size // 15), True)
    text = "APP"
    text_w = draw.textbbox((0, 0), text, font=font)[2]
    draw.text(((size - text_w) // 2, int(size * 0.63)), text, font=font, fill=(255, 231, 163, 240))
    base.save(IMG / filename)


def write_mobile_app() -> None:
    app_dir = DIST / "app"
    app_dir.mkdir(parents=True, exist_ok=True)
    app_html = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover" />
  <title>Flux &amp; Crave App | Order, Menu, Pickup, and Local Cravings</title>
  <meta name="description" content="Use the free Flux &amp; Crave mobile app experience for quick ordering, menu discovery, local pickup, directions, and social rollout updates." />
  <meta name="theme-color" content="#9d1208" />
  <meta name="robots" content="index,follow" />
  <link rel="canonical" href="https://www.fluxcrave.com/app/" />
  <link rel="icon" href="/assets/images/flux-mark.svg" type="image/svg+xml" />
  <link rel="apple-touch-icon" href="/assets/images/app-icon-180.png" />
  <link rel="manifest" href="/manifest.webmanifest" />
  <meta name="apple-mobile-web-app-capable" content="yes" />
  <meta name="apple-mobile-web-app-title" content="FluxCrave" />
  <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent" />
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Manrope:wght@400;500;600;700;800&display=swap" rel="stylesheet" />
  <meta property="og:title" content="Flux &amp; Crave App | Flavor in Motion" />
  <meta property="og:description" content="A phone-first Flux &amp; Crave app experience for ordering, menu discovery, pickup, and local cravings." />
  <meta property="og:type" content="website" />
  <meta property="og:url" content="https://www.fluxcrave.com/app/" />
  <meta property="og:image" content="https://www.fluxcrave.com/assets/images/flux-flyer.png" />
  <link rel="stylesheet" href="/assets/site.css" />
</head>
<body class="app-body">
  <div class="site-background">
    <div class="glow glow-one"></div>
    <div class="glow glow-two"></div>
    <div class="ribbon ribbon-one"></div>
    <div class="ribbon ribbon-two"></div>
    <img class="logo-orbit orbit-one" src="/assets/images/flux-mark.svg" alt="" />
    <img class="logo-orbit orbit-two" src="/assets/images/flux-mark.svg" alt="" />
    <img class="logo-orbit orbit-three" src="/assets/images/flux-mark.svg" alt="" />
  </div>
  <header class="site-header app-header">
    <div class="container header-shell">
      <a class="brand" href="/" aria-label="Flux &amp; Crave home">
        <img class="brand-wordmark" src="/assets/images/flux-logo-wordmark.png" alt="Flux &amp; Crave logo" width="568" height="108" />
      </a>
      <button class="menu-toggle" type="button" aria-expanded="false" aria-controls="site-nav"><span></span><span></span><span></span></button>
      <nav class="site-nav" id="site-nav">
        <div class="nav-links"><a class="nav-link" href="/">Home</a><a class="nav-link" href="/menu/">Menu</a><a class="nav-link" href="/story/">Story</a><a class="nav-link" href="/visit/">Visit</a><a class="nav-link is-current" href="/app/">App</a></div>
        <a class="button button-primary nav-order" href="/online-ordering/">Order Here</a>
      </nav>
    </div>
  </header>
  <main class="app-main">
    <section class="app-hero">
      <div class="container app-hero-card reveal">
        <div class="app-phone-frame">
          <img src="/assets/images/poster-right.png" alt="Flux and Crave mobile food poster preview" />
          <div class="app-phone-bar">Order &bull; Menu &bull; Directions</div>
        </div>
        <div class="app-hero-copy">
          <span class="eyebrow">iPhone + Android friendly</span>
          <h1>Flux &amp; Crave, built for the phone in your hand.</h1>
          <p>Free to install and free to use: fast menu browsing, one-tap ordering, call, directions, and save-for-later cravings in a clean mobile web app.</p>
          <div class="app-actions">
            <a class="button button-primary" href="/online-ordering/">Order now</a>
            <a class="button button-secondary" href="tel:5737193159">Call Flux &amp; Crave</a>
            <button class="button button-secondary" type="button" data-install-app>Install free app</button>
          </div>
          <p class="app-install-note">No paid download. No subscription. On iPhone: tap Share, then Add to Home Screen. On Android: tap Install App when prompted.</p>
        </div>
      </div>
    </section>
    <section class="app-quick-actions" aria-label="Quick actions">
      <div class="container app-action-grid">
        <a class="app-action-card reveal" href="/online-ordering/"><strong>Order</strong><span>Jump into online ordering.</span></a>
        <a class="app-action-card reveal" href="/menu/"><strong>Menu</strong><span>Browse the full crave lineup.</span></a>
        <a class="app-action-card reveal" href="tel:5737193159"><strong>Call</strong><span>Reach the shop in one tap.</span></a>
        <a class="app-action-card reveal" href="https://www.google.com/maps/search/?api=1&amp;query=3827%20Highway%20MM%2C%20Hannibal%2C%20MO%2063401"><strong>Directions</strong><span>Open maps for pickup.</span></a>
      </div>
    </section>
    <section class="app-crave-builder">
      <div class="container app-panel reveal">
        <div class="app-panel-heading">
          <span class="eyebrow">Crave builder</span>
          <h2>Find the item that matches your mood.</h2>
          <p>Search or filter the menu, then order when the craving gets loud.</p>
        </div>
        <div class="app-search-row">
          <label class="sr-only" for="app-menu-search">Search Flux &amp; Crave menu</label>
          <input id="app-menu-search" class="app-search" type="search" placeholder="Search wings, wraps, bowls, lemonade..." autocomplete="off" />
        </div>
        <div class="app-category-pills" id="app-category-pills" aria-label="Menu categories"></div>
        <div class="app-menu-grid" id="app-menu-grid" aria-live="polite"></div>
      </div>
    </section>
    <section class="app-social-loop">
      <div class="container app-social-grid">
        <article class="app-feature-card reveal"><span class="eyebrow">Today's push</span><h2>What makes it different?</h2><p>Use today's social angle to show the clean crave lane: bold flavor, intentional ingredients, and visuals that people remember.</p></article>
        <article class="app-feature-card app-feature-hot reveal"><span class="eyebrow">Free app</span><h2>Order, call, directions &mdash; all in one place.</h2><p>Free to install and free to use. Perfect for stories, QR cards, counter signage, and repeat customers.</p></article>
      </div>
    </section>
  </main>
  <nav class="mobile-app-nav" aria-label="Flux &amp; Crave mobile app navigation">
    <a href="/app/" aria-current="page">App</a><a href="/menu/">Menu</a><a href="/online-ordering/">Order</a><a href="tel:5737193159">Call</a>
  </nav>
  <script src="/assets/site.js"></script>
  <script src="/assets/app.js"></script>
</body>
</html>
"""
    (app_dir / "index.html").write_text(app_html, encoding="utf-8")


def write_app_js() -> None:
    app_js = """const fluxAppReady = (fn) => {
  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", fn, { once: true });
  } else {
    fn();
  }
};

fluxAppReady(() => {
  const grid = document.querySelector("#app-menu-grid");
  const pills = document.querySelector("#app-category-pills");
  const search = document.querySelector("#app-menu-search");
  let categories = [];
  let active = "all";
  let query = "";

  const esc = (value) => String(value).replace(/[&<>"']/g, (char) => ({
    "&": "&amp;", "<": "&lt;", ">": "&gt;", "\\"": "&quot;", "'": "&#39;"
  }[char]));

  const render = () => {
    if (!grid || !pills) return;
    const items = categories.flatMap((category) =>
      category.items.map((item) => ({ ...item, category: category.title, slug: category.slug }))
    ).filter((item) => {
      const matchesCategory = active === "all" || item.slug === active;
      const haystack = `${item.name} ${item.description} ${item.category}`.toLowerCase();
      return matchesCategory && haystack.includes(query);
    });

    grid.innerHTML = items.map((item) => `
      <article class="app-menu-item">
        <span>${esc(item.category)}</span>
        <h3>${esc(item.name)}</h3>
        <p>${esc(item.description)}</p>
        <a href="/online-ordering/" aria-label="Order ${esc(item.name)}">Order this</a>
      </article>
    `).join("") || `<p class="app-empty">No menu items match that search yet. Try wings, wraps, bowl, lemonade, or Flux.</p>`;
  };

  fetch("/assets/data/menu.json")
    .then((response) => response.json())
    .then((data) => {
      categories = data.categories || [];
      if (pills) {
        pills.innerHTML = [`<button class="is-active" type="button" data-category="all">All</button>`]
          .concat(categories.map((category) => `<button type="button" data-category="${esc(category.slug)}">${esc(category.title)}</button>`))
          .join("");
        pills.addEventListener("click", (event) => {
          const button = event.target.closest("button[data-category]");
          if (!button) return;
          active = button.dataset.category;
          pills.querySelectorAll("button").forEach((node) => node.classList.toggle("is-active", node === button));
          render();
        });
      }
      render();
    })
    .catch(() => {
      if (grid) grid.innerHTML = `<p class="app-empty">Menu could not load. Use the full menu page or order link.</p>`;
    });

  if (search) {
    search.addEventListener("input", () => {
      query = search.value.trim().toLowerCase();
      render();
    });
  }
});
"""
    (DIST / "assets" / "app.js").write_text(app_js, encoding="utf-8")


def write_sw_and_manifest() -> None:
    sw = """const CACHE_NAME = "flux-crave-mobile-v1";
const CORE_ASSETS = [
  "/", "/app/", "/menu/", "/story/", "/visit/",
  "/assets/site.css", "/assets/site.js", "/assets/app.js", "/assets/data/menu.json",
  "/assets/images/flux-logo-wordmark.png", "/assets/images/flux-mark.svg",
  "/assets/images/app-icon-180.png", "/assets/images/app-icon-192.png", "/assets/images/app-icon-512.png",
  "/assets/images/hero-chicken.png", "/assets/images/hero-wrap.png", "/assets/images/poster-right.png",
  "/manifest.webmanifest"
];

self.addEventListener("install", (event) => {
  event.waitUntil(caches.open(CACHE_NAME).then((cache) => cache.addAll(CORE_ASSETS)).then(() => self.skipWaiting()));
});

self.addEventListener("activate", (event) => {
  event.waitUntil(caches.keys()
    .then((keys) => Promise.all(keys.filter((key) => key !== CACHE_NAME).map((key) => caches.delete(key))))
    .then(() => self.clients.claim()));
});

self.addEventListener("fetch", (event) => {
  const request = event.request;
  if (request.method !== "GET") return;
  const url = new URL(request.url);
  if (url.origin !== self.location.origin) return;
  event.respondWith(
    caches.match(request).then((cached) => cached || fetch(request).then((response) => {
      const copy = response.clone();
      caches.open(CACHE_NAME).then((cache) => cache.put(request, copy));
      return response;
    }).catch(() => caches.match("/app/") || caches.match("/")))
  );
});
"""
    (DIST / "sw.js").write_text(sw, encoding="utf-8")

    manifest = {
        "id": "/app/",
        "name": "Flux & Crave Mobile",
        "short_name": "FluxCrave",
        "description": "A free, phone-first Flux & Crave app experience for menu browsing, ordering, pickup, calls, directions, and local craving updates.",
        "start_url": "/app/?source=pwa",
        "scope": "/",
        "display": "standalone",
        "display_override": ["window-controls-overlay", "standalone", "browser"],
        "orientation": "portrait",
        "background_color": "#1a120d",
        "theme_color": "#9d1208",
        "categories": ["food", "lifestyle", "business"],
        "icons": [
            {"src": "/assets/images/app-icon-180.png", "sizes": "180x180", "type": "image/png"},
            {"src": "/assets/images/app-icon-192.png", "sizes": "192x192", "type": "image/png", "purpose": "any maskable"},
            {"src": "/assets/images/app-icon-512.png", "sizes": "512x512", "type": "image/png", "purpose": "any maskable"},
            {"src": "/assets/images/flux-mark.svg", "sizes": "any", "type": "image/svg+xml"},
        ],
        "shortcuts": [
            {"name": "Order Now", "short_name": "Order", "url": "/online-ordering/", "description": "Jump to Flux & Crave online ordering."},
            {"name": "Menu", "short_name": "Menu", "url": "/menu/", "description": "Browse the Flux & Crave menu."},
            {"name": "Visit", "short_name": "Visit", "url": "/visit/", "description": "View pickup, directions, and contact details."},
        ],
    }
    (DIST / "manifest.webmanifest").write_text(json.dumps(manifest, indent=2), encoding="utf-8")


def update_site_js() -> None:
    site_js_path = DIST / "assets" / "site.js"
    site_js = site_js_path.read_text(encoding="utf-8")
    install_block = """

ready(() => {
  if ("serviceWorker" in navigator && location.protocol !== "file:") {
    navigator.serviceWorker.register("/sw.js").catch(() => {});
  }

  window.fluxInstallPrompt = null;
  window.addEventListener("beforeinstallprompt", (event) => {
    event.preventDefault();
    window.fluxInstallPrompt = event;
    document.querySelectorAll("[data-install-app]").forEach((button) => button.classList.add("is-ready"));
  });

  document.querySelectorAll("[data-install-app]").forEach((button) => {
    button.addEventListener("click", async () => {
      if (window.fluxInstallPrompt) {
        window.fluxInstallPrompt.prompt();
        await window.fluxInstallPrompt.userChoice.catch(() => null);
        window.fluxInstallPrompt = null;
      } else {
        button.classList.add("is-helping");
        button.textContent = /iphone|ipad|ipod/i.test(navigator.userAgent)
          ? "Use Share > Add to Home Screen"
          : "Use browser menu > Install app";
      }
    });
  });
});
"""
    if "window.fluxInstallPrompt" not in site_js:
        site_js = site_js.rstrip() + install_block + "\n"
    site_js = site_js.replace("Use Share → Add to Home Screen", "Use Share > Add to Home Screen")
    site_js = site_js.replace("Use browser menu → Install app", "Use browser menu > Install app")
    site_js_path.write_text(site_js, encoding="utf-8")


def update_css() -> None:
    css_path = DIST / "assets" / "site.css"
    css = css_path.read_text(encoding="utf-8")
    if "Flux & Crave mobile app layer — 2026-05-20" in css:
        return
    css_append = """

/* Flux & Crave mobile app layer — 2026-05-20 */
.sr-only{position:absolute;width:1px;height:1px;padding:0;margin:-1px;overflow:hidden;clip:rect(0,0,0,0);white-space:nowrap;border:0}
.app-body{padding-bottom:calc(5.4rem + env(safe-area-inset-bottom))}
.app-main{overflow:hidden}
.app-hero{padding:clamp(3rem,7vw,6rem) 0 2rem}
.app-hero-card{display:grid;grid-template-columns:minmax(16rem,.72fr) minmax(0,1fr);gap:clamp(1.5rem,4vw,4rem);align-items:center;padding:clamp(1.2rem,4vw,3rem);border:1px solid rgba(255,255,255,.1);border-radius:38px;background:radial-gradient(circle at 20% 10%,rgba(255,203,70,.22),transparent 18rem),linear-gradient(135deg,rgba(42,23,14,.9),rgba(110,18,8,.82));box-shadow:var(--shadow)}
.app-phone-frame{position:relative;max-width:24rem;margin:0 auto;padding:.8rem;border-radius:42px;border:1px solid rgba(255,255,255,.16);background:#0d0907;box-shadow:0 28px 80px rgba(0,0,0,.45);transform:rotate(-2deg)}
.app-phone-frame:before{content:"";position:absolute;top:.6rem;left:50%;width:5rem;height:.45rem;transform:translateX(-50%);border-radius:999px;background:rgba(255,255,255,.18);z-index:2}
.app-phone-frame img{border-radius:32px;min-height:32rem;object-fit:cover}
.app-phone-bar{position:absolute;left:1.4rem;right:1.4rem;bottom:1.4rem;padding:.85rem 1rem;border-radius:999px;background:rgba(13,9,7,.86);color:var(--accent-2);font-weight:900;text-align:center;backdrop-filter:blur(16px)}
.app-hero-copy h1,.app-panel-heading h2,.app-feature-card h2{font-family:"Bebas Neue",sans-serif;font-size:clamp(3.4rem,8vw,7.8rem);line-height:.86;letter-spacing:.01em;margin:.45rem 0 1rem}
.app-hero-copy p,.app-panel-heading p,.app-feature-card p,.app-install-note{color:var(--muted);font-size:clamp(1rem,2vw,1.18rem);line-height:1.65}
.app-actions,.app-search-row{display:flex;flex-wrap:wrap;gap:.85rem;margin-top:1.3rem}
button.button{cursor:pointer}
[data-install-app].is-ready:after{content:"•";margin-left:.2rem;color:var(--accent-2)}
.app-quick-actions,.app-crave-builder,.app-social-loop{padding:clamp(1.5rem,5vw,4rem) 0}
.app-action-grid,.app-social-grid{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:1rem}
.app-action-card,.app-feature-card,.app-panel{border:1px solid rgba(255,255,255,.1);background:rgba(24,14,9,.8);box-shadow:0 18px 50px rgba(0,0,0,.25)}
.app-action-card{min-height:9.5rem;padding:1.25rem;border-radius:24px;display:flex;flex-direction:column;justify-content:space-between}
.app-action-card strong{font-family:"Bebas Neue",sans-serif;font-size:2.5rem;letter-spacing:.03em}
.app-action-card span,.app-menu-item p,.app-empty{color:var(--muted);line-height:1.5}
.app-panel{border-radius:34px;padding:clamp(1.2rem,4vw,2.6rem)}
.app-search{width:min(100%,38rem);min-height:3.4rem;border-radius:999px;border:1px solid rgba(255,255,255,.12);background:rgba(255,255,255,.06);color:var(--text);padding:0 1.2rem;font:inherit;outline:none}
.app-search::placeholder{color:rgba(255,244,232,.55)}
.app-category-pills{display:flex;flex-wrap:wrap;gap:.7rem;margin:1.35rem 0}
.app-category-pills button{border:1px solid rgba(255,255,255,.11);background:rgba(255,255,255,.05);color:var(--text);border-radius:999px;padding:.7rem 1rem;font-weight:800;cursor:pointer}
.app-category-pills button.is-active{background:var(--accent-2);color:#190e09}
.app-menu-grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:1rem}
.app-menu-item{border:1px solid rgba(255,255,255,.09);border-radius:22px;padding:1.1rem;background:rgba(255,255,255,.045)}
.app-menu-item span{color:var(--accent-2);font-weight:900;font-size:.78rem;text-transform:uppercase;letter-spacing:.12em}
.app-menu-item h3{margin:.6rem 0 .45rem;font-size:1.15rem}
.app-menu-item a{display:inline-flex;margin-top:.6rem;color:var(--accent-2);font-weight:900}
.app-social-grid{grid-template-columns:1fr 1fr}
.app-feature-card{border-radius:30px;padding:clamp(1.2rem,4vw,2.4rem)}
.app-feature-hot{background:radial-gradient(circle at 85% 15%,rgba(255,203,70,.26),transparent 16rem),linear-gradient(135deg,rgba(157,18,8,.82),rgba(24,14,9,.86))}
.mobile-app-nav{position:fixed;z-index:60;left:max(.8rem,env(safe-area-inset-left));right:max(.8rem,env(safe-area-inset-right));bottom:max(.65rem,env(safe-area-inset-bottom));display:grid;grid-template-columns:repeat(4,1fr);gap:.4rem;padding:.45rem;border:1px solid rgba(255,255,255,.12);border-radius:999px;background:rgba(13,9,7,.9);box-shadow:0 20px 60px rgba(0,0,0,.45);backdrop-filter:blur(20px)}
.mobile-app-nav a{display:inline-flex;justify-content:center;align-items:center;min-height:2.8rem;border-radius:999px;color:var(--muted);font-weight:900;font-size:.9rem}
.mobile-app-nav a[aria-current=page],.mobile-app-nav a:hover,.mobile-app-nav a:focus-visible{background:linear-gradient(135deg,var(--accent),var(--accent-2));color:#190e09}
@media (min-width:820px){.mobile-app-nav{display:none}.app-body{padding-bottom:0}}
@media (max-width:900px){.app-hero-card,.app-action-grid,.app-social-grid,.app-menu-grid{grid-template-columns:1fr}.app-phone-frame{max-width:19rem;transform:none}.app-phone-frame img{min-height:25rem}}
@media (max-width:580px){.app-hero{padding-top:2rem}.app-hero-card,.app-panel,.app-feature-card{border-radius:24px}.app-hero-copy h1,.app-panel-heading h2,.app-feature-card h2{font-size:clamp(3rem,17vw,4.7rem)}.app-actions .button{width:100%}}
"""
    css_path.write_text(css.rstrip() + css_append + "\n", encoding="utf-8")


def update_existing_html() -> None:
    html_files = [DIST / "index.html", DIST / "menu" / "index.html", DIST / "story" / "index.html", DIST / "visit" / "index.html"]
    for path in html_files:
        text = path.read_text(encoding="utf-8")
        if "apple-touch-icon" not in text:
            text = text.replace(
                '<link rel="manifest" href="/manifest.webmanifest" />',
                '<link rel="manifest" href="/manifest.webmanifest" />\n'
                '  <link rel="apple-touch-icon" href="/assets/images/app-icon-180.png" />\n'
                '  <meta name="apple-mobile-web-app-capable" content="yes" />\n'
                '  <meta name="apple-mobile-web-app-title" content="FluxCrave" />\n'
                '  <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent" />',
            )
        if 'href="/app/">App</a>' not in text:
            text = text.replace(
                '<a class="nav-link" href="/visit/">Visit</a>',
                '<a class="nav-link" href="/visit/">Visit</a><a class="nav-link" href="/app/">App</a>',
            )
            text = text.replace(
                '<a class="nav-link is-current" href="/visit/">Visit</a>',
                '<a class="nav-link is-current" href="/visit/">Visit</a><a class="nav-link" href="/app/">App</a>',
            )
        if '<li><a href="/app/">Mobile app</a></li>' not in text:
            text = text.replace(
                '<li><a href="/online-ordering/">Order online</a></li>',
                '<li><a href="/online-ordering/">Order online</a></li>\n        <li><a href="/app/">Mobile app</a></li>',
            )
        path.write_text(text, encoding="utf-8")


def write_docs(socials: list[Path]) -> None:
    ROLL.mkdir(parents=True, exist_ok=True)
    HUB.mkdir(parents=True, exist_ok=True)
    social_lines = "\n".join(f"- `{path.name}`" for path in socials)
    rollout_md = f"""# Flux & Crave Fresh Mobile + Social Rollout Pass

Generated: 2026-05-20  
System: Master Prompt OS → Flux & Crave Rollout Agent → Branding Algorithm Agent → AI Creative + Video Beat Agent → App Connector Agent → Quality Gate Agent

## Objective
Create a fresh, attractive, free-to-install, free-to-use mobile-first Flux & Crave rollout package that supports iPhone and Android users, keeps the public brand consistent, and prepares Adobe Express / Canva / Photoshop / Illustrator handoffs without posting unverified claims.

## Output created

### Mobile application layer
- New PWA route: `/app/`
- Installable app manifest upgraded: `/manifest.webmanifest`
- Offline/cache support added: `/sw.js`
- App-specific menu/search behavior added: `/assets/app.js`
- iPhone/Android app icons added:
  - `/assets/images/app-icon-180.png`
  - `/assets/images/app-icon-192.png`
  - `/assets/images/app-icon-512.png`

### Social rollout graphics
{social_lines}

## Creative direction
- Visual language: flame red, golden yellow, dark food-cinematic background, neon crave energy.
- Tone: bold, local, clean, fast, high-flavor, phone-first.
- Avoid: disease/medical claims, guaranteed health outcomes, unverified DoorDash/order claims, unapproved addresses/phone changes.

## Fresh 10-piece social rollout

| Asset | Platform | Hook | Caption Core | Creative Direction | Gate |
|---|---|---|---|---|---|
| Day 8 differentiator carousel | IG/FB carousel | This is not basic food marketing. | Flux & Crave is built around bold flavor, intentional ingredients, and visuals people remember. | Logo + wrap/chicken + three differentiator cards | Verify photos/logo |
| Day 9 local awareness story | Stories/Snap | Hannibal, this is for you. | Fast pickup, clean crave energy, ordering made phone-simple. | Map/phone-style story frame | Verify address/phone |
| Day 10 menu poll | IG poll/FB | Which craving should hit first? | Wings, wraps, bowls, lemonade, or the Flux Capacitor? | Split menu card with poll stickers | Verify menu item availability |
| Mobile app launch | IG/FB/Snap | Your craving now lives on your phone. | Open FluxCrave.com/app and add it to your home screen. | App screen + QR/order visual | Verify app route before posting |
| Save-this card | IG/FB static | Save this for your next craving. | One tap to menu, ordering, contact, and local pickup. | Square save card | Verify order/contact links |
| Website walkthrough reel | Reels/Shorts | Here’s how to tap into Flux & Crave. | 10-second screen recording of app/menu/order flow. | Phone screen capture + kinetic text | Verify site path live |
| Food hero reel | Reels/Stories | The craving does not leave quietly. | Closeups + bite pull + logo outro. | Food montage with warm contrast | Needs approved iPhone footage |
| Behind-the-brand post | FB/IG | The brand is being built piece by piece. | Every photo, caption, video, and website edit builds recognition. | Editing/process screenshots | No private screens/secrets |
| Weekly Crave Feature | IG/FB | Weekly Crave Feature starts now. | Spotlight one menu item each week. | Repeatable template | Verify item availability |
| Social proof request | Stories/FB | Your reaction helps build the brand. | Tag, photo, comment, or review-style feedback. | UGC frame | Do not imply reviews before received |

## Adobe / Canva / Photoshop / Illustrator handoff

### Adobe Express
Search/use templates in these categories:
- bold restaurant launch social media post
- fiery food menu Instagram story
- modern takeout flyer red yellow black
- phone app launch announcement food brand

### Photoshop
Use for:
- food photo cleanup: crop, contrast, warmth, sharpening
- story/reel cover effects: bloom, grain, tritone, subtle glitch
- background cleanup on menu/food assets

### Illustrator
Use for:
- vector logo cleanup
- signage-ready brand mark export
- 1080x1080, 1080x1920, 8.5x11 artboards
- layered source file with background, logo, hero food, headline, CTA, footer/legal notes

### Canva
Use for:
- fast resizing into IG post, story, FB post, flyer, phone wallpaper
- editable campaign calendar templates
- publishing handoff drafts after final approval

## Quality Gate
- App route opens and is mobile responsive.
- Menu search/filter works without console errors.
- Manifest validates as installable basics: start_url, scope, icons, theme color.
- No outreach/posting done automatically.
- Public claims that need verification remain gated: address, phone, DoorDash, order status, nutrition/health claims.
"""
    (ROLL / "README.md").write_text(rollout_md, encoding="utf-8")
    (HUB / "flux_crave_mobile_social_rollout_2026-05-20.md").write_text(rollout_md, encoding="utf-8")

    with (ROLL / "production_matrix.csv").open("w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["asset", "platform", "format", "status", "path", "approval_gate"])
        for path in socials:
            writer.writerow([path.stem, "Instagram/Facebook/Snapchat", "PNG", "Draft generated", str(path), "Final logo/photos/contact/order verification before posting"])
        writer.writerow(["mobile_app_pwa", "iPhone/Android web app", "HTML/CSS/JS/PWA", "Built locally", str(DIST / "app" / "index.html"), "Deploy approval before public release"])
        writer.writerow(["service_worker", "iPhone/Android web app", "JS", "Built locally", str(DIST / "sw.js"), "QA before public release"])

    briefs = {
        "master_prompt_os_route": ["INPUT", "ENRICH", "STRUCTURE", "ROUTE", "EXECUTE", "TRACK", "IMPROVE"],
        "business_lane": "Flux & Crave",
        "outputs": [str(path) for path in socials] + [str(DIST / "app" / "index.html")],
        "quality_gate": {
            "no_auto_publish": True,
            "requires_verification": ["address", "phone", "DoorDash/order state", "final logo/photos", "health/wellness claims"],
            "mobile_targets": ["iPhone Safari add-to-home-screen", "Android Chrome install prompt", "responsive browser"],
        },
        "adobe_account_requested": "thejmillercomany@gmail.com",
        "note": "Account email noted for user context only; no password or sensitive account action performed.",
    }
    (ROLL / "creative_briefs.json").write_text(json.dumps(briefs, indent=2), encoding="utf-8")


def main() -> None:
    ROLL.mkdir(parents=True, exist_ok=True)
    HUB.mkdir(parents=True, exist_ok=True)
    socials = [
        create_social("fluxcrave_day8_differentiators_instagram_1080x1350.png", (1080, 1350), "Not basic food marketing.", "Bold flavor, intentional ingredients, and visuals people remember.", "DAY 8 • DIFFERENT BY DESIGN", "Save + follow the rollout", "hero-wrap.png"),
        create_social("fluxcrave_day9_local_awareness_story_1080x1920.png", (1080, 1920), "Hannibal, this is for you.", "Fast pickup, clean crave energy, and ordering made phone-simple.", "LOCAL AWARENESS", "Tap in at FluxCrave.com", "poster-right.png", story=True),
        create_social("fluxcrave_day10_menu_poll_instagram_1080x1350.png", (1080, 1350), "Which craving should hit first?", "Wings, wraps, bowls, lemonade, or the Flux Capacitor?", "MENU POLL", "Comment your craving", "hero-chicken.png"),
        create_social("fluxcrave_mobile_app_launch_1080x1350.png", (1080, 1350), "Your craving now lives on your phone.", "Open FluxCrave.com/app and add it to your home screen.", "MOBILE APP PREVIEW", "Order • Call • Directions", "qr-order.png"),
        create_social("fluxcrave_save_this_card_1080x1080.png", (1080, 1080), "Save this for your next craving.", "One tap to menu, ordering, contact, and local pickup details.", "SAVE CARD", "FluxCrave.com/app", "flux-flyer.png"),
    ]
    for size, filename in [(180, "app-icon-180.png"), (192, "app-icon-192.png"), (512, "app-icon-512.png")]:
        create_icon(size, filename)
    write_mobile_app()
    write_app_js()
    write_sw_and_manifest()
    update_site_js()
    update_css()
    update_existing_html()
    write_docs(socials)

    print("created_socials")
    for path in socials:
        print(path)
    print("created_app", DIST / "app" / "index.html")
    print("updated_manifest", DIST / "manifest.webmanifest")
    print("updated_hub", HUB / "flux_crave_mobile_social_rollout_2026-05-20.md")


if __name__ == "__main__":
    main()
