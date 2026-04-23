# WordPress Root Fix - 2026-03-27

## What was wrong
- The account has two parallel web roots on InfinityFree:
  - `htdocs`
  - `thefocuscorp.com/htdocs`
- The live WordPress site is the domain-scoped root at `thefocuscorp.com/htdocs`.
- The public site bundle had been published to `htdocs`, which updated a different root and left the WordPress-facing site partially stale.

## What was corrected
- Default InfinityFree deploy target was changed to prefer `thefocuscorp.com/htdocs`.
- GitHub Actions deploy defaults were updated to target `thefocuscorp.com/htdocs`.
- A repeatable theme deploy script was added:
  - `focus_ai/scripts/deploy_wordpress_theme.py`
- The active WordPress theme was backed up locally and mirrored into the repo:
  - `focus_ai/wordpress_theme_backups/2026-03-27/Sacred-Focus-Pro-Theme`
  - `focus_ai/wordpress_theme/Sacred-Focus-Pro-Theme`
- The active theme homepage was upgraded with a new portal-style front page:
  - `focus_ai/wordpress_theme/Sacred-Focus-Pro-Theme/front-page.php`

## Live file paths confirmed on FTP
- `thefocuscorp.com/htdocs/products.html`
- `thefocuscorp.com/htdocs/business_os.html`
- `thefocuscorp.com/htdocs/wp-content/themes/Sacred-Focus-Pro-Theme/front-page.php`
- `thefocuscorp.com/htdocs/wp-content/themes/Sacred-Focus-Pro-Theme/style.css`

## Edge / caching note
- Cloudflare account check returned no active `thefocuscorp.com` zone in the connected account.
- That means Cloudflare is not the active edge layer from this connected account's perspective.

## Archive path for later
- Packaging script:
  - `focus_ai/scripts/package_workspace.ps1`
- It creates a timestamped zip under:
  - `C:\Users\reggi\OneDrive\Desktop\Focus-AI-Archive\`
