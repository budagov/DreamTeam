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
echo "Installed. Create project in a SEPARATE folder:"
echo "  cd ~/projects/my-app"
echo "  dreamteam new-project ."
echo ""
echo "Do NOT use DreamTeam folder as project — engine and project stay separate."
