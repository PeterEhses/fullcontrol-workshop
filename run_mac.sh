#!/bin/bash

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
MINICONDA_DIR="$SCRIPT_DIR/Miniconda3"

# Check if setup has been run
if [ ! -f "$MINICONDA_DIR/bin/conda" ]; then
    echo "========================================"
    echo "First Time Setup Required"
    echo "========================================"
    echo
    echo "Please run ./setup_mac.sh first to install Miniconda"
    echo "and create the workshop environment."
    echo
    exit 1
fi

# Check if environment exists
source "$MINICONDA_DIR/bin/activate" fullcontrol_env 2>/dev/null
if [ $? -ne 0 ]; then
    echo "========================================"
    echo "Environment Not Found"
    echo "========================================"
    echo
    echo "Please run ./setup_mac.sh to create the fullcontrol_env environment."
    echo
    exit 1
fi

echo "Starting FullControl Workshop..."
echo

# Launch Marimo
marimo edit "$SCRIPT_DIR/app.py"