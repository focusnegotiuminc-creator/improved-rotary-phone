#!/usr/bin/env bash
set -euo pipefail

echo "Initializing FOCUS MASTER AI..."

if [ ! -d ".venv" ]; then
  python -m venv .venv
fi

source .venv/bin/activate
pip install -r requirements.txt

if [ ! -f ".env" ]; then
  cp .env.example .env
  echo "Created .env from .env.example. Add your real keys before live integrations."
fi

echo "FOCUS MASTER AI ready. Run: python main.py"

