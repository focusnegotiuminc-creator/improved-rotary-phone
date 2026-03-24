# Why you may still see an old format after publishing

If updates are public but your interface still looks outdated, it is usually one of these:

1. **Browser cache still serving old assets**
   - Fix: hard refresh and clear site data.
2. **CDN cache delay**
   - Fix: purge CDN cache and wait for edge propagation.
3. **Service worker holding stale files**
   - Fix: unregister service worker or bump asset version hash.
4. **Wrong deployment target/branch**
   - Fix: confirm production points to the correct repo branch and latest commit.
5. **Build artifact mismatch**
   - Fix: verify generated build files include the latest code.

## Professional deployment checklist

- Use hashed assets (`app.a1b2c3.js`) for cache busting.
- Bump app version in each production release.
- Automate post-deploy smoke tests for visual and functional checks.
- Include rollback tags for stable recovery.

## Immediate action sequence

1. Validate latest commit SHA in production logs.
2. Purge CDN + browser cache.
3. Verify service worker version and force update.
4. Re-run deploy pipeline.
5. Confirm with screenshot-based visual smoke test.

