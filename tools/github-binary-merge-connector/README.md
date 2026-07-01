# GitHub Binary + Merge Connector

This connector closes the two gaps in the current Zapier GitHub connector:

1. true binary file upload, including MP3s and images;
2. merge pull request action.

It exposes HTTP endpoints that can be called from Zapier Webhooks, ChatGPT Actions, an MCP server, iPhone Shortcuts, GitHub Codespaces, or a mobile terminal.

## Endpoints

### `GET /health`

Checks whether the connector is live.

### `POST /github/upload-binary`

Uploads or replaces a real binary file in GitHub using GitHub's Contents API.

Accepted inputs:

- multipart form field `file`; or
- JSON field `base64`.

Required fields:

- `path`
- optional `branch`, default `main`
- optional `owner`, default `focusnegotiuminc-creator`
- optional `repo`, default `improved-rotary-phone`
- optional `message`

Example with curl:

```bash
curl -X POST "$CONNECTOR_URL/github/upload-binary" \
  -H "x-focus-connector-key: $CONNECTOR_API_KEY" \
  -F "branch=focus-command-center-drive-import-2026-06-28" \
  -F "path=focus_ai/site/flux-crave/assets/audio/change-your-life-money.mp3" \
  -F "message=Upload real Flux Crave MP3 binary" \
  -F "file=@/path/to/Change your life money .mp3"
```

### `POST /github/delete-file`

Deletes a file from the target branch after resolving its SHA.

```bash
curl -X POST "$CONNECTOR_URL/github/delete-file" \
  -H "content-type: application/json" \
  -H "x-focus-connector-key: $CONNECTOR_API_KEY" \
  -d '{
    "branch":"focus-command-center-drive-import-2026-06-28",
    "path":"focus_ai/site/flux-crave/assets/flux-crave/audio/change-your-life-money.mp3",
    "message":"Remove incorrect pointer audio file"
  }'
```

### `POST /github/merge-pr`

Merges a pull request.

```bash
curl -X POST "$CONNECTOR_URL/github/merge-pr" \
  -H "content-type: application/json" \
  -H "x-focus-connector-key: $CONNECTOR_API_KEY" \
  -d '{"pull_number":7,"merge_method":"merge"}'
```

### `POST /vercel/deploy`

Optional deployment endpoint. Requires `VERCEL_TOKEN` and `VERCEL_PROJECT_ID`.

## Environment variables

Required:

```bash
GITHUB_TOKEN=github_pat_or_fine_grained_token
```

Recommended:

```bash
CONNECTOR_API_KEY=long_random_secret
DEFAULT_OWNER=focusnegotiuminc-creator
DEFAULT_REPO=improved-rotary-phone
VERCEL_TOKEN=optional
VERCEL_PROJECT_ID=optional
VERCEL_TEAM_ID=optional
```

The GitHub token needs permissions for repository contents and pull requests.

## Mobile setup options

### GitHub UI on iPhone

1. Open GitHub app or Safari.
2. Open the repository.
3. Open Pull Requests.
4. Open PR #7.
5. Confirm changed files.
6. Tap merge once checks pass.

### GitHub Codespaces from iPhone browser

1. Open the repo in Safari.
2. Tap Code.
3. Open Codespaces.
4. Start a codespace.
5. Use the terminal commands in `docs/mobile-github-cli-setup.md`.

### iSH / mobile terminal

Use iSH or a Linux shell that supports Git and GitHub CLI. Then authenticate with `gh auth login`, clone the repo, upload the MP3s, and merge PR #7 from the phone.
