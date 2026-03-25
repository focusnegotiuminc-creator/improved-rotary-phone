#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
REPO=""
SOCKS_PORT="18080"
SKIP_MERGE="0"
NO_TUNNEL="0"

usage() {
  cat <<'EOF'
Usage: unblock_and_live.sh [options]

Creates/uses an outbound proxy path, then runs:
  1) gh install bootstrap
  2) merge open PRs
  3) full go-live pipeline

Options:
  --repo OWNER/REPO     Override GitHub repository for merge-prs.
  --socks-port PORT     Local SOCKS5 port for SSH tunnel (default: 18080).
  --skip-merge          Skip GitHub PR merge and only run go-live.
  --no-tunnel           Use existing HTTP(S)_PROXY/ALL_PROXY env vars only.
  -h, --help            Show help.

Environment variables (used when --no-tunnel is not set):
  BASTION_SSH           Required. SSH destination for outbound bridge, e.g. user@bastion.example.com
  SSH_KEY_FILE          Optional private key path; if set, script uses IdentitiesOnly mode.
  BASTION_SSH_FLAGS     Optional extra ssh flags, e.g. "-p 2222"

GitHub credentials:
  GH_TOKEN              Recommended for non-interactive gh auth / PR merge calls.
EOF
}


required_prompt() {
  cat <<'EOF' >&2
Missing required connection credentials. Provide at minimum:
  export BASTION_SSH=user@your-bastion-host
Optional secure auth controls:
  export SSH_KEY_FILE=~/.ssh/your_private_key
  export GH_TOKEN=<token-with-repo-scope>
Re-run after setting the values (do not hardcode secrets in repo files).
EOF
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --repo)
      REPO="${2:-}"
      shift 2
      ;;
    --socks-port)
      SOCKS_PORT="${2:-}"
      shift 2
      ;;
    --skip-merge)
      SKIP_MERGE="1"
      shift
      ;;
    --no-tunnel)
      NO_TUNNEL="1"
      shift
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      echo "Unknown option: $1" >&2
      usage >&2
      exit 2
      ;;
  esac
done

cleanup() {
  if [[ -n "${SSH_TUNNEL_PID:-}" ]]; then
    kill "${SSH_TUNNEL_PID}" >/dev/null 2>&1 || true
  fi
}
trap cleanup EXIT

if [[ "$NO_TUNNEL" != "1" ]]; then
  if [[ -z "${BASTION_SSH:-}" ]]; then
    required_prompt
    exit 2
  fi

  SSH_ARGS=( -N -D "${SOCKS_PORT}" )
  if [[ -n "${SSH_KEY_FILE:-}" ]]; then
    SSH_ARGS+=( -i "${SSH_KEY_FILE}" -o IdentitiesOnly=yes )
  fi
  if [[ -n "${BASTION_SSH_FLAGS:-}" ]]; then
    # shellcheck disable=SC2206
    EXTRA_FLAGS=( ${BASTION_SSH_FLAGS} )
    SSH_ARGS+=( "${EXTRA_FLAGS[@]}" )
  fi

  echo "Starting SSH SOCKS bridge on 127.0.0.1:${SOCKS_PORT} via ${BASTION_SSH}..."
  ssh "${SSH_ARGS[@]}" "${BASTION_SSH}" &
  SSH_TUNNEL_PID=$!
  sleep 2

  export ALL_PROXY="socks5h://127.0.0.1:${SOCKS_PORT}"
  export HTTPS_PROXY="${ALL_PROXY}"
  export HTTP_PROXY="${ALL_PROXY}"
  echo "Proxy env configured via ${ALL_PROXY}."
fi

echo "Installing gh (or verifying existing install)..."
bash "${ROOT_DIR}/focus_ai/scripts/install_gh_cli.sh"

if [[ "$SKIP_MERGE" != "1" ]]; then
  if [[ -z "${GH_TOKEN:-}" ]]; then
    echo "Warning: GH_TOKEN is not set. gh may require interactive auth." >&2
  fi
  echo "Merging all open pull requests..."
  MERGE_ARGS=( merge-prs )
  if [[ -n "$REPO" ]]; then
    MERGE_ARGS+=( --repo "$REPO" )
  fi
  python3 "${ROOT_DIR}/focus_ai/scripts/github_ops.py" "${MERGE_ARGS[@]}"
fi

echo "Running full go-live pipeline..."
python3 "${ROOT_DIR}/focus_ai/scripts/github_ops.py" go-live

echo "Unblock-and-live flow completed."
