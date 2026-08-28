#!/usr/bin/env bash
# One-time setup. Installs uv if you don't have it, then the workshop dependencies.
set -e
cd "$(dirname "$0")"

if ! command -v uv >/dev/null 2>&1; then
    echo "Installing uv..."
    curl -LsSf https://astral.sh/uv/install.sh | sh
    export PATH="$HOME/.local/bin:$PATH"
fi

echo "Installing dependencies (this downloads Python too, if needed)..."
uv sync

echo
echo "Done. Now run:  ./run.sh"
