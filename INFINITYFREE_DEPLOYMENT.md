# InfinityFree Deployment Runbook

This repository already has the live production content for:

- `thefocuscorp.com` — source: `/index.html`, `/site-status/`, `/flux-crave/`, and shared assets.
- `fluxcrave.com` — source: `/flux-crave/index.html` plus Flux & Crave audio assets.

## Current verified source files

- `/index.html` — Focus Corp glowing homepage.
- `/flux-crave/index.html` — Flux & Crave warm neon page.
- `/site-status/index.html` — live QA page.
- `/focus_ai/site/flux-crave/assets/audio/change-your-life-money.mp3` — verified real MP3 asset.
- `/focus_ai/site/flux-crave/assets/audio/be-your-menu.mp3` — verified real MP3 asset.

## Required InfinityFree FTP secrets

Do not paste these values into ChatGPT. Store them in GitHub repository secrets or a secured deployment tool.

For `thefocuscorp.com`:

- `INFINITYFREE_FOCUS_FTP_SERVER`
- `INFINITYFREE_FOCUS_FTP_USERNAME`
- `INFINITYFREE_FOCUS_FTP_PASSWORD`
- `INFINITYFREE_FOCUS_SERVER_DIR` — usually `htdocs/`, but confirm in the InfinityFree control panel.

For `fluxcrave.com`:

- `INFINITYFREE_FLUX_FTP_SERVER`
- `INFINITYFREE_FLUX_FTP_USERNAME`
- `INFINITYFREE_FLUX_FTP_PASSWORD`
- `INFINITYFREE_FLUX_SERVER_DIR` — usually `htdocs/`, but confirm in the InfinityFree control panel.

## Static package layout for InfinityFree

### thefocuscorp.com document root

Upload these to the InfinityFree document root for `thefocuscorp.com`:

```text
index.html
site-status/
flux-crave/
focus_ai/site/flux-crave/assets/audio/change-your-life-money.mp3
focus_ai/site/flux-crave/assets/audio/be-your-menu.mp3
```

### fluxcrave.com document root

Upload these to the InfinityFree document root for `fluxcrave.com`:

```text
index.html                    # copy from flux-crave/index.html
focus_ai/site/flux-crave/assets/audio/change-your-life-money.mp3
focus_ai/site/flux-crave/assets/audio/be-your-menu.mp3
```

## Optional .htaccess for each InfinityFree document root

```apache
DirectoryIndex index.html
Options -Indexes
ErrorDocument 404 /index.html
```

## GitHub workflow note

The connected GitHub app can update normal repository files, but creating files inside `.github/workflows/` requires GitHub workflow permission. If the current GitHub connector token lacks that permission, create the workflow manually in GitHub or update the connected GitHub token permissions.

Recommended workflow file path after permission is enabled:

```text
.github/workflows/infinityfree.yml
```

Use an FTP deployment action with separate jobs for `thefocuscorp.com` and `fluxcrave.com`, using the secrets above.

## DNS/domain note

The deployment cannot become live on the public custom domains until the domains point to the correct InfinityFree hosting account. After uploading files, confirm:

- `thefocuscorp.com` resolves to the InfinityFree site assigned to that account.
- `fluxcrave.com` resolves to the InfinityFree site assigned to that account.

If `fluxcrave.com` remains pointed to Wix, the InfinityFree upload will not be shown on that public domain until DNS is changed.
