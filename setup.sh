#!/bin/bash
# DreamTeam — one-command setup after clone
# Run from DreamTeam folder: ./setup.sh

set -e
echo "DreamTeam setup..."
pip install -e .
echo ""
echo "Verifying..."
python -m dreamteam
echo ""
if [ ! -d .dreamteam ]; then
    echo "Creating project..."
    python -m dreamteam new-project .
fi
echo ""
echo "Ready. For a CLEAN project: cd your-folder && dreamteam new-project ."
echo "  Or open this folder in Cursor for quick try: /start + goal, dreamteam run-next"
