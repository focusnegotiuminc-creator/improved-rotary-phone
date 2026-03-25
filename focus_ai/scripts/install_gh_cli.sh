#!/usr/bin/env bash
set -euo pipefail

if command -v gh >/dev/null 2>&1; then
  echo "gh is already installed: $(gh --version | head -n1)"
  exit 0
fi

echo "Attempting to install GitHub CLI (gh) with apt..."
if sudo apt-get update && sudo apt-get install -y gh; then
  echo "Installed gh successfully: $(gh --version | head -n1)"
  exit 0
fi

cat <<'EOF'

Failed to install gh automatically.
Likely cause in this environment: outbound proxy/tunnel restriction returning HTTP 403.

To retry once tunnel/proxy is available:
  export HTTPS_PROXY=http://<proxy-host>:<proxy-port>
  export HTTP_PROXY=http://<proxy-host>:<proxy-port>
  sudo apt-get update
  sudo apt-get install -y gh

Then authenticate:
  gh auth login
EOF
exit 1
