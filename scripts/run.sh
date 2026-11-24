#!/usr/bin/env bash

set -e

cd "$(dirname "$0")/.."

echo "===================================="
echo "    DEVICE MANAGEMENT SIMULATOR"
echo "===================================="

if [ -f ".venv/Scripts/python.exe" ]; then
    PYTHON=".venv/Scripts/python.exe"
elif [ -f ".venv/bin/python" ]; then
    PYTHON=".venv/bin/python"
else
    PYTHON="python3"
fi

echo "Starting application..."

"$PYTHON" -m streamlit run app.py