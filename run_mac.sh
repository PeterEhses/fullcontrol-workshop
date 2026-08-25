#!/usr/bin/env bash
# ./run_mac.sh                    -> opens lesson 01 as an app
# ./run_mac.sh 05-the-noodle      -> opens that lesson
# ./run_mac.sh 05-the-noodle edit -> opens it with the code visible and editable
set -e
cd "$(dirname "$0")"

LESSON="${1:-01-the-path}"
DIR="lessons/$LESSON"
[ -d "$DIR" ] || DIR="$LESSON"

if [ ! -d "$DIR" ]; then
    echo "No lesson called '$LESSON'. Available:"
    ls lessons
    exit 1
fi

NOTEBOOK=$(find "$DIR" -maxdepth 1 -name '*.py' | head -1)
if [ -z "$NOTEBOOK" ]; then
    echo "No notebook in $DIR"
    exit 1
fi

if [ "$2" = "edit" ]; then
    uv run marimo edit "$NOTEBOOK"
else
    uv run marimo run "$NOTEBOOK"
fi
