#!/bin/bash
# DreamTeam — quick setup after clone
# Run from DreamTeam folder: ./setup.sh

set -e
echo "DreamTeam setup..."
pip install -e .
echo ""
echo "Verifying..."
python -m dreamteam
echo ""
echo "OK. Use: python -m dreamteam new-project ."
echo "  or: dreamteam new-project <path>"
