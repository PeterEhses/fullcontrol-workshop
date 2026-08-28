#!/usr/bin/env bash
# ./run.sh              day 1, part A, as an app
# ./run.sh 1 b          day 1, part b  (./run.sh 1b works too)
# ./run.sh 3 e          day 3, the exercise
# ./run.sh browse       the marimo editor with the file sidebar
#
# Names are matched by prefix, so as long as it's unique, as little as you like.
set -e
cd "$(dirname "$0")"

APP_NOTEBOOK="lessons/1-tiles/a-points.py"

if [ -z "$1" ]; then
    exec uv run marimo run "$APP_NOTEBOOK"
fi

if [ "$1" = "browse" ]; then
    exec uv run marimo edit .
fi

DAY="$1"
PART="$2"

# "1b" as one word, as long as it isn't a full folder name like "1-tiles"
if [ -z "$PART" ] && [ "${#DAY}" -gt 1 ] && [ "${DAY:1:1}" != "-" ]; then
    PART="${DAY:1}"
    DAY="${DAY:0:1}"
fi

matches=(lessons/"$DAY"*/)
if [ ! -d "${matches[0]}" ]; then
    echo "No day matching '$DAY'. Available:"
    ls lessons
    exit 1
fi
if [ "${#matches[@]}" -gt 1 ]; then
    echo "'$DAY' matches more than one day:"
    printf '   %s\n' "${matches[@]%/}"
    exit 1
fi
DIR="${matches[0]%/}"

if [ -z "$PART" ]; then
    echo "Which notebook? In $DIR:"
    for f in "$DIR"/*.py; do echo "   $(basename "$f" .py)"; done
    exit 1
fi

notebooks=("$DIR/$PART"*.py)
if [ ! -f "${notebooks[0]}" ]; then
    echo "Nothing matching '$PART' in $DIR:"
    for f in "$DIR"/*.py; do echo "   $(basename "$f" .py)"; done
    exit 1
fi
if [ "${#notebooks[@]}" -gt 1 ]; then
    echo "'$PART' matches more than one notebook:"
    for f in "${notebooks[@]}"; do echo "   $(basename "$f" .py)"; done
    exit 1
fi
NOTEBOOK="${notebooks[0]}"

# a-points is the one notebook meant to be driven rather than read
if [ "$NOTEBOOK" = "$APP_NOTEBOOK" ] && [ "$3" != "edit" ]; then
    exec uv run marimo run "$NOTEBOOK"
fi

exec uv run marimo edit "$NOTEBOOK"
