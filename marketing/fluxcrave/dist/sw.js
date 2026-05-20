const CACHE_NAME = "flux-crave-mobile-v1";
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
