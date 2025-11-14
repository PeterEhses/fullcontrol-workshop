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

# Check if a lesson argument was provided, otherwise use lesson-01
LESSON="${1:-lesson-01-spiral-explorations}"
LESSON_PATH="$SCRIPT_DIR/lessons/$LESSON/notebook.py"

# Check if lesson exists
if [ ! -f "$LESSON_PATH" ]; then
    echo "Lesson not found: $LESSON"
    echo "Using default lesson-01..."
    LESSON_PATH="$SCRIPT_DIR/lessons/lesson-01-spiral-explorations/notebook.py"
fi

# Launch Marimo with the lesson notebook
marimo edit "$LESSON_PATH"