# Secret Registry

This file intentionally stores secret names only. It does not store secret values.

## GitHub Actions Secrets

- `INFINITYFREE_FTP_HOST`
- `INFINITYFREE_FTP_USER`
- `INFINITYFREE_FTP_PASS`
- `INFINITYFREE_REMOTE_DIR`
- `REPLIT_DEPLOY_HOOK_URL`
- `REPLIT_DEPLOY_WEBHOOK_URL`
- `REPLIT_DEPLOY_TOKEN`

## GitHub Actions Variables

- `FOCUS_APP_URL`
- `FOCUS_APP_PATHS`
- `FOCUS_REQUIRE_ALL_PATHS`
- `FOCUS_SKIP_TLS_VERIFY`
- `INFINITYFREE_REMOTE_DIR_CANDIDATES`
- `INFINITYFREE_STRICT`
- `REPLIT_DEPLOY_METHOD`
- `REPLIT_DEPLOY_TIMEOUT`

## Usage Rule

- Future chats and automations should reference these keys by name.
- Secret values stay in GitHub Secrets, local ignored environment files, or approved secret stores only.
