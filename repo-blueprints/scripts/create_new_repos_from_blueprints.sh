#!/usr/bin/env bash
set -euo pipefail

OWNER="focusnegotiuminc-creator"
ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

require_cmd() {
  command -v "$1" >/dev/null 2>&1 || {
    echo "Missing required command: $1" >&2
    exit 1
  }
}

require_cmd git
require_cmd gh

gh auth status >/dev/null

create_and_push() {
  local repo_name="$1"
  local source_dir="$ROOT_DIR/$repo_name"
  local tmp_dir
  tmp_dir="$(mktemp -d)"

  if [[ ! -d "$source_dir" ]]; then
    echo "Blueprint not found: $source_dir" >&2
    exit 1
  fi

  echo "Creating $OWNER/$repo_name from $source_dir"
  gh repo create "$OWNER/$repo_name" --private --description "Focus AI blueprint: $repo_name" --confirm || true

  rsync -a --delete "$source_dir/" "$tmp_dir/"
  cd "$tmp_dir"
  git init
  git checkout -b main
  git add .
  git commit -m "Initial $repo_name scaffold from Operator OS blueprints"
  git remote add origin "https://github.com/$OWNER/$repo_name.git"
  git push -u origin main --force

  echo "Pushed https://github.com/$OWNER/$repo_name"
}

create_and_push "operator-os-agent-kernel"
create_and_push "focus-micro-alpha-trader"

echo "Done. Review both repos, add secrets in GitHub Settings, then run CI."
