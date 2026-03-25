#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
SESSION_NAME="${SESSION_NAME:-focus_ai_autopilot}"
INTERVAL_SECONDS="${INTERVAL_SECONDS:-900}"
REPO_OVERRIDE="${REPO_OVERRIDE:-}"
NO_LOOP="0"
SKIP_MERGE="0"

usage() {
  cat <<'HELP'
Usage: setup_autopilot.sh [options]

One-command bootstrap for a "keep it running" workflow:
  1) Verifies git remotes and fetches all remotes
  2) Bootstraps GitHub CLI install
  3) Starts a detached tmux loop that repeatedly runs merge-prs + go-live

Options:
  --repo OWNER/REPO      Optional owner/repo for merge-prs.
  --interval SECONDS     Loop interval (default: 900).
  --session NAME         tmux session name (default: focus_ai_autopilot).
  --skip-merge           Skip merge-prs and run go-live only.
  --no-loop              Run once and exit (no background tmux session).
  -h, --help             Show help.

Environment:
  GH_TOKEN               Recommended for non-interactive GitHub auth.
  HTTP_PROXY/HTTPS_PROXY Optional outbound proxy settings.
HELP
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --repo)
      REPO_OVERRIDE="${2:-}"
      shift 2
      ;;
    --interval)
      INTERVAL_SECONDS="${2:-}"
      shift 2
      ;;
    --session)
      SESSION_NAME="${2:-}"
      shift 2
      ;;
    --skip-merge)
      SKIP_MERGE="1"
      shift
      ;;
    --no-loop)
      NO_LOOP="1"
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

if ! command -v git >/dev/null 2>&1; then
  echo "git is required but not installed." >&2
  exit 1
fi

cd "$ROOT_DIR"

echo "Checking git remotes..."
if ! git remote -v; then
  echo "No git remotes configured." >&2
  exit 1
fi

echo "Refreshing all remotes (git fetch --all --prune)..."
git fetch --all --prune

echo "Bootstrapping GitHub CLI..."
bash "$ROOT_DIR/focus_ai/scripts/install_gh_cli.sh"

if [[ "$NO_LOOP" == "1" ]]; then
  echo "Running one-shot workflow..."
  if [[ "$SKIP_MERGE" != "1" ]]; then
    MERGE_ARGS=( merge-prs )
    if [[ -n "$REPO_OVERRIDE" ]]; then
      MERGE_ARGS+=( --repo "$REPO_OVERRIDE" )
    fi
    python3 "$ROOT_DIR/focus_ai/scripts/github_ops.py" "${MERGE_ARGS[@]}"
  fi
  python3 "$ROOT_DIR/focus_ai/scripts/github_ops.py" go-live
  echo "Done."
  exit 0
fi

if ! command -v tmux >/dev/null 2>&1; then
  echo "tmux not found. Install tmux or run with --no-loop." >&2
  exit 1
fi

WORKER_SCRIPT="$ROOT_DIR/focus_ai/scripts/.autopilot_worker.sh"
cat > "$WORKER_SCRIPT" <<WORKER
#!/usr/bin/env bash
set -euo pipefail
cd "$ROOT_DIR"
while true; do
  echo "[\$(date -u +%Y-%m-%dT%H:%M:%SZ)] autopilot tick"
  if [[ "$SKIP_MERGE" != "1" ]]; then
    MERGE_ARGS=( merge-prs )
    if [[ -n "$REPO_OVERRIDE" ]]; then
      MERGE_ARGS+=( --repo "$REPO_OVERRIDE" )
    fi
    python3 "$ROOT_DIR/focus_ai/scripts/github_ops.py" "\${MERGE_ARGS[@]}" || true
  fi
  python3 "$ROOT_DIR/focus_ai/scripts/github_ops.py" go-live || true
  sleep "$INTERVAL_SECONDS"
done
WORKER
chmod +x "$WORKER_SCRIPT"

if tmux has-session -t "$SESSION_NAME" 2>/dev/null; then
  echo "tmux session '$SESSION_NAME' already exists. Restarting it..."
  tmux kill-session -t "$SESSION_NAME"
fi

tmux new-session -d -s "$SESSION_NAME" "bash '$WORKER_SCRIPT'"

echo "Autopilot started in tmux session: $SESSION_NAME"
echo "View logs: tmux attach -t $SESSION_NAME"
echo "Stop autopilot: tmux kill-session -t $SESSION_NAME"
