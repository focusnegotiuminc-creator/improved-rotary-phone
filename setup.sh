#!/bin/bash

# GitHub Remote Connector - Codex Deployment Setup
# This script sets up the connector and initializes remotes for all repos

set -e

GITHUB_USER="thegreatmachevilli"
GITHUB_TOKEN="${GITHUB_TOKEN:-}"
BASE_PATH="${BASE_PATH:-.github_repos}"

echo "🚀 GitHub Remote Connector - Codex Deployment"
echo "=============================================="
echo "User: $GITHUB_USER"
echo "Base Path: $BASE_PATH"
echo ""

if [ -z "$GITHUB_TOKEN" ]; then
    echo "❌ Error: GITHUB_TOKEN environment variable not set"
    echo "Please set: export GITHUB_TOKEN='your_personal_access_token'"
    exit 1
fi

# Install dependencies
echo "📦 Installing dependencies..."
pip install requests --quiet

# Run the connector
echo "🔗 Initializing GitHub remote connector..."
python3 github_remote_connector.py \
    --user "$GITHUB_USER" \
    --token "$GITHUB_TOKEN" \
    --path "$BASE_PATH" \
    --action clone

echo ""
echo "🪞 Creating unified mirror..."
python3 github_remote_connector.py \
    --user "$GITHUB_USER" \
    --token "$GITHUB_TOKEN" \
    --path "$BASE_PATH" \
    --action mirror

echo ""
echo "📋 Generating repository report..."
python3 github_remote_connector.py \
    --user "$GITHUB_USER" \
    --token "$GITHUB_TOKEN" \
    --path "$BASE_PATH" \
    --action report

echo ""
echo "✅ Deployment complete!"
echo "Repository remotes are now connected and ready for operations."
echo "All repos cloned to: $BASE_PATH"
echo "Check $BASE_PATH/connector_log.txt for detailed logs"